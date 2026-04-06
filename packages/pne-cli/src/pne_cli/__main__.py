"""CLI entrypoint for interactive Pne sessions."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Callable, Sequence

from pne import (
    ChatMessage,
    AgentEvent,
    ToolSpec,
    build_adapter,
    build_agent,
    build_local_tools,
    build_advanced_tools,
    analyze_bash_command,
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
            "--allow-shell",
            action="store_true",
            help="Expose shell in toolset.",
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
        # New flags
        command_parser.add_argument(
            "--allow-bash",
            action="store_true",
            help="Expose bash tool in toolset (with safety analysis).",
        )
        command_parser.add_argument(
            "--allow-repl",
            action="store_true",
            help="Expose Python repl tool in toolset.",
        )
        command_parser.add_argument(
            "--allow-mcp",
            action="store_true",
            help="Expose MCP tools in toolset.",
        )
        command_parser.add_argument(
            "--mcp-servers",
            default=None,
            help="Semicolon-separated list of MCP server commands (e.g., 'npx -y @modelcontextprotocol/server-filesystem /tmp').",
        )
        command_parser.add_argument(
            "--allow-ask",
            action="store_true",
            help="Expose AskUserQuestion tool in toolset.",
        )
        command_parser.add_argument(
            "--advanced-tools",
            action="store_true",
            help="Use the advanced toolset (FileRead, FileEdit, Glob, Grep, etc.) instead of the basic one.",
        )
        command_parser.add_argument(
            "--permission-mode",
            choices=["bypass", "ask"],
            default=None,
            help="Permission mode: bypass (no confirmations) or ask (confirm dangerous operations).",
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


def _prompt_once(message: str) -> str:
    return input(f"{message} [y/N]: ").strip().lower()


def _needs_confirmation(tool_name: str) -> bool:
    """Determine if a tool should prompt for confirmation based on its name."""
    return tool_name in {"run_command", "write_file", "FileEdit", "FileWrite", "NotebookEdit", "bash"}


def _tool_wrapper(
    tool: ToolSpec,
    *,
    permission_mode: str = "ask",
) -> ToolSpec:
    """Wrap a tool with permission checking based on the permission mode."""
    if permission_mode == "bypass":
        return tool

    if not _needs_confirmation(tool.name):
        return tool

    def _handler(args: dict) -> object:
        # Special handling for bash tool - check safety analysis
        if tool.name == "bash":
            command = str(args.get("command", ""))
            analysis = analyze_bash_command(command)
            if analysis.get("needs_confirmation"):
                concerns = "; ".join(analysis.get("concerns", []))
                print(f"\n[Security Warning] bash command detected concerns: {concerns}")
                if _prompt_once("Execute this command?") != "y":
                    return {"status": "rejected", "tool": tool.name, "concerns": concerns}
            return tool.handler(args)

        # Standard confirmation for other tools
        if _prompt_once(f"Allow {tool.name}?") != "y":
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


def _resolve_permission_mode(args: argparse.Namespace) -> str:
    """Resolve the permission mode from args or interactive prompt."""
    if args.permission_mode is not None:
        return args.permission_mode

    # Interactive prompt
    print("\nPermission mode:")
    print("  1) bypass - Run all tools without confirmation")
    print("  2) ask    - Confirm before dangerous operations (default)")
    choice = input("Choose [1/2] (default: 2): ").strip()
    if choice == "1":
        print("Permission mode: bypass")
        return "bypass"
    print("Permission mode: ask")
    return "ask"


def _build_local_tools(
    *,
    base_dir: str,
    allow_write: bool,
    allow_shell: bool,
    approve_commands: bool,
    advanced_tools: bool,
    allow_bash: bool,
    allow_repl: bool,
    allow_ask: bool,
) -> list[ToolSpec]:
    """Build the local toolset (without MCP tools)."""
    if advanced_tools or allow_bash or allow_repl or allow_ask:
        tools = build_advanced_tools(
            base_path=base_dir,
            allow_write=allow_write,
            allow_bash=allow_bash,
            allow_repl=allow_repl,
            allow_ask=allow_ask,
        )
    else:
        tools = build_local_tools(
            base_path=base_dir,
            allow_write=allow_write,
            allow_shell=allow_shell,
            allow_command=approve_commands,
        )
    return tools


def _wrap_tools(tools: list[ToolSpec], *, permission_mode: str) -> list[ToolSpec]:
    """Wrap tools with permission checking."""
    return [_tool_wrapper(tool, permission_mode=permission_mode) for tool in tools]


async def _connect_mcp_clients(mcp_servers: str | None) -> list:
    """Connect to MCP servers and return connected clients."""
    if not mcp_servers:
        return []

    try:
        from pne.mcp import McpClient
    except ImportError:
        print("Warning: MCP support requires 'pne[mcp]' to be installed.", file=sys.stderr)
        return []

    clients = []
    for server_cmd in mcp_servers.split(";"):
        server_cmd = server_cmd.strip()
        if not server_cmd:
            continue
        try:
            client = McpClient(server_cmd.split())
            await client.connect()
            clients.append(client)
            print(f"Connected to MCP server: {server_cmd}")
        except Exception as exc:
            print(f"Failed to connect to MCP server '{server_cmd}': {exc}", file=sys.stderr)

    return clients


async def _disconnect_mcp_clients(clients: list) -> None:
    """Disconnect from all MCP servers."""
    for client in clients:
        try:
            await client.disconnect()
        except Exception:
            pass


def _build_agent_sync(
    args: argparse.Namespace,
    permission_mode: str,
    mcp_clients: list,
) -> object:
    """Build the agent with local tools and optional MCP tools."""
    tools = _build_local_tools(
        base_dir=args.base_dir,
        allow_write=args.allow_write,
        allow_shell=args.allow_shell,
        approve_commands=args.approve_commands,
        advanced_tools=args.advanced_tools,
        allow_bash=args.allow_bash,
        allow_repl=args.allow_repl,
        allow_ask=args.allow_ask,
    )

    # Add MCP tools from connected clients
    if mcp_clients:
        from pne.mcp import build_mcp_tools
        for client in mcp_clients:
            tools.extend(build_mcp_tools(client))

    # Wrap with permission checking
    tools = _wrap_tools(tools, permission_mode=permission_mode)

    return build_agent(
        adapter=build_adapter(args.backend, model=args.model),
        tools=tools,
    )


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
            output = event.get("output")
            output_str = str(output) if output is not None else ""
            if len(output_str) > 500:
                output_str = output_str[:500] + "... [truncated]"
            print(f"  - tool_output: {output_str}")
        elif event_type == "final":
            final_text = str(event.get("content") or "")
            if streaming:
                print()
                streaming = False
            print(f"final: {final_text}")

    return final_text


async def _run_single(
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

    return await _consume_events(
        prompt=prompt,
        agent=agent,
        max_steps=max_steps,
        on_step=_on_step,
        quiet=quiet,
        history=history,
    )


async def _handle_chat_async(args: argparse.Namespace) -> int:
    """Async handler for chat command with MCP lifecycle."""
    permission_mode = _resolve_permission_mode(args)

    # Connect MCP clients
    mcp_clients = await _connect_mcp_clients(args.mcp_servers)

    try:
        agent = _build_agent_sync(args, permission_mode, mcp_clients)
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

                final_text = await _run_single(
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
    finally:
        await _disconnect_mcp_clients(mcp_clients)

    return 0


async def _handle_ask_async(args: argparse.Namespace) -> int:
    """Async handler for ask command with MCP lifecycle."""
    permission_mode = _resolve_permission_mode(args)

    # Connect MCP clients
    mcp_clients = await _connect_mcp_clients(args.mcp_servers)

    try:
        agent = _build_agent_sync(args, permission_mode, mcp_clients)
        trace_write, trace_close = _load_trace_writer(args.trace_json)

        try:
            prompt = " ".join(args.prompt)
            final_text = await _run_single(
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
    finally:
        await _disconnect_mcp_clients(mcp_clients)

    return 0


def _handle_chat(args: argparse.Namespace) -> int:
    return asyncio.run(_handle_chat_async(args))


def _handle_ask(args: argparse.Namespace) -> int:
    return asyncio.run(_handle_ask_async(args))


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
