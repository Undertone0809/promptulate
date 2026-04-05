"""CLI entrypoint for interactive Pne sessions."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Callable, Iterable, Sequence

from pne import (
    ChatMessage,
    AgentEvent,
    ToolSpec,
    build_adapter,
    build_agent,
    build_local_tools,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pne", description="Pne agent CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def _add_common_options(command_parser: argparse.ArgumentParser) -> None:
        command_parser.add_argument(
            "--backend",
            default="auto",
            help="Backend name: auto/openai/anthropic/claude-code/codex",
        )
        command_parser.add_argument("--model", default=None, help="Backend model name")
        command_parser.add_argument(
            "--allow-write",
            action="store_true",
            help="Expose write_file in toolset.",
        )
        command_parser.add_argument(
            "--approve-commands",
            action="store_true",
            help="Expose and execute run_command after confirmation.",
        )
        command_parser.add_argument(
            "--base-dir",
            default=".",
            help="Filesystem base directory for local tools.",
        )
        command_parser.add_argument(
            "--trace-json",
            default=None,
            help="Write raw step events to JSONL for debugging.",
        )
        command_parser.add_argument(
            "--quiet",
            action="store_true",
            help="Only print final result instead of full event stream.",
        )

    def _add_command_parser(name: str, help_text: str, *, has_prompt: bool = False) -> argparse.ArgumentParser:
        sub = subparsers.add_parser(name, help=help_text)
        sub.set_defaults(command=name)
        sub.add_argument(
            "--max-steps", type=int, default=8, help="Maximum tool loops per turn"
        )
        _add_common_options(sub)
        if has_prompt:
            sub.add_argument("prompt", nargs="+", help="Prompt to ask")
        return sub

    _add_command_parser("chat", "Start an interactive chat session")
    ask_parser = _add_command_parser(
        "ask",
        "Send one prompt and exit",
        has_prompt=True,
    )
    ask_parser.set_defaults(command="ask")
    return parser


def _tool_wrapper(
    tool: ToolSpec,
    *,
    confirm: Callable[[str], bool] | None = None,
    confirm_prompt: str | None = None,
) -> ToolSpec:
    if confirm is None:
        return tool

    def _handler(args: dict) -> object:
        if confirm_prompt:
            if not confirm(confirm_prompt):
                return {"status": "rejected", "tool": tool.name}
        return tool.handler(args)

    return ToolSpec(
        name=tool.name,
        description=tool.description,
        parameters=tool.parameters,
        handler=_handler,
        strict=tool.strict,
    )


def _load_trace_writer(path: str | None) -> tuple[Callable[[dict[str, object]], None], Callable[[], None]]:
    if path is None:
        return (lambda _event: None, lambda: None)

    handle = Path(path).open("a", encoding="utf-8")

    def _write(event: dict[str, object]) -> None:
        json.dump(event, handle, ensure_ascii=False)
        handle.write("\n")
        handle.flush()

    def _close() -> None:
        handle.close()

    return _write, _close


def _prompt_once(message: str) -> str:
    return input(f"{message} [y/N]: ").strip().lower()


def _build_tools(
    *,
    base_dir: str,
    allow_write: bool,
    approve_commands: bool,
) -> list[ToolSpec]:
    tools = build_local_tools(
        base_path=base_dir,
        allow_write=allow_write,
        allow_command=approve_commands,
    )
    wrapped: list[ToolSpec] = []
    for tool in tools:
        if tool.name == "run_command":
            wrapped.append(
                _tool_wrapper(
                    tool,
                    confirm=lambda *_: _prompt_once("Run command? (y/N)") == "y",
                    confirm_prompt="Run command?",
                )
            )
            continue
        if tool.name == "write_file":
            wrapped.append(
                _tool_wrapper(
                    tool,
                    confirm=lambda *_: _prompt_once("Write file? (y/N)") == "y",
                    confirm_prompt="Write file?",
                )
            )
            continue
        wrapped.append(tool)
    return wrapped


async def _consume_events(
    *,
    prompt: str,
    agent: object,
    max_steps: int,
    on_step: Callable[[AgentEvent], None],
    quiet: bool,
    history: Sequence[ChatMessage],
) -> str:
    final_text = ""
    streaming = False
    async for event in agent.run_stream(prompt, max_steps=max_steps, on_step=on_step, history=history):
        event_type = event.get("type")
        if quiet and event_type != "final":
            continue

        if event_type == "step_start":
            print(f"\n[step {event['step']}]")
            streaming = False
        elif event_type == "model_turn":
            has_tools = bool(event.get("tool_calls"))
            if has_tools:
                print("assistant: thinking...")
            elif event.get("content"):
                print("assistant: ", end="", flush=True)
                streaming = True
            else:
                print("assistant: ")
                streaming = False
        elif event_type == "model_delta":
            delta = str(event.get("delta") or "")
            if delta:
                if not streaming:
                    print("assistant: ", end="", flush=True)
                    streaming = True
                print(delta, end="", flush=True)
        elif event_type == "tool_call":
            if streaming:
                print()
                streaming = False
            tool_call = event.get("tool_call", {})
            name = tool_call.get("name")
            args = tool_call.get("arguments")
            print("  - tool_call")
            print(f"    name: {name}")
            print(f"    args: {json.dumps(args, ensure_ascii=False)}")
        elif event_type == "tool_output":
            if streaming:
                print()
                streaming = False
            print(f"  - tool_output: {event.get('output')}")
        elif event_type == "final":
            final_text = str(event.get("content") or "")
            if streaming:
                print()
                streaming = False
            print(f"final: {final_text}")

    return final_text


def _run_single(
    agent,
    prompt: str,
    *,
    max_steps: int,
    trace_writer: Callable[[dict[str, object]], None],
    quiet: bool,
    history: list[ChatMessage],
) -> str:
    def _on_step(event: dict[str, object]) -> None:
        trace_writer(event)

    return asyncio.run(
        _consume_events(
            prompt=prompt,
            agent=agent,
            max_steps=max_steps,
            on_step=_on_step,
            quiet=quiet,
            history=history,
        )
    )


def _build_agent(args: argparse.Namespace) -> object:
    tools = _build_tools(
        base_dir=args.base_dir,
        allow_write=args.allow_write,
        approve_commands=args.approve_commands,
    )
    return build_agent(
        adapter=build_adapter(args.backend, model=args.model),
        tools=tools,
    )


def _handle_chat(args: argparse.Namespace) -> int:
    agent = _build_agent(args)
    trace_write, trace_close = _load_trace_writer(args.trace_json)
    history: list[ChatMessage] = []

    try:
        while True:
            try:
                text = input("pne> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not text:
                continue
            if text == "/quit":
                break
            if text == "/reset":
                history.clear()
                print("history reset.")
                continue
            if text == "/help":
                print("/quit exit the session")
                print("/reset clear the history")
                continue

            final_text = _run_single(
                agent=agent,
                prompt=text,
                max_steps=args.max_steps,
                trace_writer=trace_write,
                quiet=args.quiet,
                history=history,
            )
            history.append(ChatMessage(role="user", content=text))
            history.append(ChatMessage(role="assistant", content=final_text))
    finally:
        trace_close()
    return 0


def _handle_ask(args: argparse.Namespace) -> int:
    agent = _build_agent(args)
    trace_write, trace_close = _load_trace_writer(args.trace_json)

    try:
        prompt = " ".join(args.prompt)
        final_text = _run_single(
            agent=agent,
            prompt=prompt,
            max_steps=args.max_steps,
            trace_writer=trace_write,
            quiet=args.quiet,
            history=[],
        )
        if args.quiet:
            print(final_text)
    finally:
        trace_close()
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command == "chat":
        return _handle_chat(args)
    if args.command == "ask":
        return _handle_ask(args)
    raise SystemExit("Unknown command")


if __name__ == "__main__":
    raise SystemExit(main())
