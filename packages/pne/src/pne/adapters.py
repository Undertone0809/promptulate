"""Model adapters for the PNE ReACT agent."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import shutil
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from .types import ChatMessage, ModelAdapter, ModelTurn, ToolCall, ToolSpec


def _coerce_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "".join(parts)
    return str(content)


def _extract_json_candidate(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 3:
            body = lines[1:]
            if body and body[-1].strip().startswith("```"):
                body = body[:-1]
            return "\n".join(body).strip()
    return stripped


def _messages_to_openai(messages: Sequence[ChatMessage]) -> list[dict[str, Any]]:
    payload: list[dict[str, Any]] = []
    for message in messages:
        item: dict[str, Any] = {"role": message.role}
        if message.content is not None:
            item["content"] = message.content
        if message.role == "assistant" and message.tool_calls:
            item["tool_calls"] = [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.name,
                        "arguments": json.dumps(tool_call.arguments, ensure_ascii=False),
                    },
                }
                for tool_call in message.tool_calls
            ]
        if message.role == "tool":
            item["tool_call_id"] = message.tool_call_id
            if message.name:
                item["name"] = message.name
        if message.role == "system" and item.get("content") is None:
            item["content"] = ""
        payload.append(item)
    return payload


def _tool_calls_from_openai(raw_tool_calls: Any) -> tuple[ToolCall, ...]:
    tool_calls: list[ToolCall] = []
    for call in raw_tool_calls or []:
        function = getattr(call, "function", None)
        name = getattr(function, "name", None)
        arguments = getattr(function, "arguments", "{}")
        tool_calls.append(
            ToolCall(
                id=getattr(call, "id", uuid.uuid4().hex),
                name=name or "",
                arguments=json.loads(arguments or "{}"),
            )
        )
    return tuple(tool_calls)


def _tool_calls_from_payload(payload: Any) -> tuple[ToolCall, ...]:
    tool_calls: list[ToolCall] = []
    for item in payload or []:
        if not isinstance(item, dict):
            continue
        arguments = item.get("arguments") or {}
        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments)
            except json.JSONDecodeError:
                arguments = {"value": arguments}
        tool_calls.append(
            ToolCall(
                id=str(item.get("id") or uuid.uuid4().hex),
                name=str(item.get("name") or item.get("tool_name") or ""),
                arguments=arguments if isinstance(arguments, dict) else {"value": arguments},
            )
        )
    return tuple(tool_calls)


def _turn_from_json_data(data: Any) -> ModelTurn:
    if isinstance(data, dict):
        if "choices" in data:
            choices = data.get("choices") or []
            if choices:
                message = choices[0].get("message") or {}
                return ModelTurn(
                    content=_coerce_text(message.get("content")).strip() or None,
                    tool_calls=_tool_calls_from_openai(message.get("tool_calls")),
                )

        message = data.get("message")
        if isinstance(message, dict):
            return ModelTurn(
                content=_coerce_text(message.get("content")).strip() or None,
                tool_calls=_tool_calls_from_openai(message.get("tool_calls")),
            )

        content = data.get("content")
        if content is None:
            content = data.get("text")
        if content is None and "result" in data:
            content = data.get("result")

        if isinstance(content, str):
            nested_text = _extract_json_candidate(content)
            if nested_text[:1] in {"{", "["}:
                try:
                    nested_turn = _turn_from_json_data(json.loads(nested_text))
                except json.JSONDecodeError:
                    nested_turn = None
                else:
                    if nested_turn.content is not None or nested_turn.tool_calls:
                        return nested_turn

        tool_calls = data.get("tool_calls")
        if tool_calls is None and isinstance(data.get("tool_call"), dict):
            tool_calls = [data["tool_call"]]

        return ModelTurn(
            content=_coerce_text(content).strip() or None,
            tool_calls=_tool_calls_from_payload(tool_calls),
        )

    if isinstance(data, list) and data:
        first = data[0]
        if isinstance(first, dict):
            return _turn_from_json_data(first)
        return ModelTurn(content=_coerce_text(first).strip() or None)

    if isinstance(data, str):
        text = data.strip()
        return ModelTurn(content=text or None)

    return ModelTurn()


@dataclass
class OpenAIChatAdapter:
    """OpenAI chat-completions adapter."""

    model: str = "gpt-5.1"
    client: Any | None = None
    adapter_type: str = "openai-chat"

    def __post_init__(self) -> None:
        if self.client is None:
            from openai import OpenAI

            self.client = OpenAI()

    def step(
        self,
        *,
        instructions: str,
        messages: Sequence[ChatMessage],
        tools: Sequence[ToolSpec],
        temperature: float,
    ) -> ModelTurn:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": instructions},
                *_messages_to_openai(messages),
            ],
            tools=[tool.as_tool_payload() for tool in tools],
            tool_choice="auto",
            temperature=temperature,
        )
        message = response.choices[0].message
        return ModelTurn(
            content=_coerce_text(getattr(message, "content", None)).strip() or None,
            tool_calls=_tool_calls_from_openai(getattr(message, "tool_calls", None)),
        )


def openai_adapter(*, model: str = "gpt-5.1", client: Any | None = None) -> OpenAIChatAdapter:
    return OpenAIChatAdapter(model=model, client=client)


def anthropic_adapter(
    *,
    model: str = "claude-sonnet-4-20250514",
    api_key: str | None = None,
) -> ModelAdapter:
    try:
        import anthropic
    except ImportError as exc:  # pragma: no cover - exercised only when package missing
        raise RuntimeError(
            "Anthropic backend requested but the `anthropic` package is not installed."
        ) from exc

    adapter_model = model
    adapter_api_key = api_key

    @dataclass
    class AnthropicMessagesAdapter:
        model: str = adapter_model
        client: Any | None = None
        adapter_type: str = "anthropic"

        def __post_init__(self) -> None:
            if self.client is None:
                self.client = anthropic.Anthropic(
                    api_key=adapter_api_key or os.getenv("ANTHROPIC_API_KEY")
                )

        def step(
            self,
            *,
            instructions: str,
            messages: Sequence[ChatMessage],
            tools: Sequence[ToolSpec],
            temperature: float,
        ) -> ModelTurn:
            anthropic_messages: list[dict[str, Any]] = []
            for message in messages:
                if message.role == "system":
                    continue
                if message.role == "user":
                    anthropic_messages.append(
                        {"role": "user", "content": message.content or ""}
                    )
                    continue
                if message.role == "assistant":
                    content_blocks: list[dict[str, Any]] = []
                    if message.content:
                        content_blocks.append({"type": "text", "text": message.content})
                    for tool_call in message.tool_calls:
                        content_blocks.append(
                            {
                                "type": "tool_use",
                                "id": tool_call.id,
                                "name": tool_call.name,
                                "input": tool_call.arguments,
                            }
                        )
                    anthropic_messages.append({"role": "assistant", "content": content_blocks})
                    continue
                if message.role == "tool":
                    anthropic_messages.append(
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": message.tool_call_id,
                                    "content": message.content or "",
                                }
                            ],
                        }
                    )

            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=instructions,
                messages=anthropic_messages,
                tools=[
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.parameters,
                    }
                    for tool in tools
                ],
                temperature=temperature,
            )
            content: list[str] = []
            tool_calls: list[ToolCall] = []
            for block in response.content:
                block_type = getattr(block, "type", None)
                if block_type == "text":
                    content.append(getattr(block, "text", ""))
                elif block_type == "tool_use":
                    tool_calls.append(
                        ToolCall(
                            id=getattr(block, "id", uuid.uuid4().hex),
                            name=getattr(block, "name", ""),
                            arguments=getattr(block, "input", {}) or {},
                        )
                    )
            return ModelTurn(content="".join(content).strip() or None, tool_calls=tuple(tool_calls))

    return AnthropicMessagesAdapter()


@dataclass
class CommandAdapter:
    """Adapter for local command-line agents such as Codex or Claude Code."""

    command: tuple[str, ...]
    prompt_mode: str = "arg"
    output_last_message: bool = False
    adapter_type: str = "command"

    def _build_prompt(
        self,
        *,
        instructions: str,
        messages: Sequence[ChatMessage],
        tools: Sequence[ToolSpec],
    ) -> str:
        payload = {
            "instructions": instructions,
            "messages": [
                {
                    "role": message.role,
                    "content": message.content,
                    "name": message.name,
                    "tool_call_id": message.tool_call_id,
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "name": tool_call.name,
                            "arguments": tool_call.arguments,
                        }
                        for tool_call in message.tool_calls
                    ],
                }
                for message in messages
            ],
            "tools": [tool.as_tool_payload() for tool in tools],
        }
        return (
            "You are a ReACT agent.\n"
            "Return exactly one JSON object with this schema:\n"
            '{ "content": string | null, "tool_calls": ['
            '{ "id": string, "name": string, "arguments": object }'
            "] }\n"
            "If you need a tool, set content to null and include one or more tool calls.\n"
            "If you are done, set tool_calls to an empty array.\n\n"
            f"INPUT:\n{json.dumps(payload, ensure_ascii=False)}"
        )

    def _invoke(self, prompt: str) -> subprocess.CompletedProcess[str]:
        command = list(self.command)
        last_message_path: Path | None = None
        if self.output_last_message:
            fd, tmp_path = tempfile.mkstemp(prefix="pne-last-message-", suffix=".txt")
            os.close(fd)
            last_message_path = Path(tmp_path)
            command.extend(["--output-last-message", str(last_message_path)])
        if self.prompt_mode == "stdin":
            completed = subprocess.run(
                command,
                input=prompt,
                text=True,
                capture_output=True,
                check=False,
            )
        else:
            completed = subprocess.run(
                [*command, prompt],
                text=True,
                capture_output=True,
                check=False,
            )

        if last_message_path is not None and last_message_path.exists():
            file_text = last_message_path.read_text(encoding="utf-8").strip()
            if file_text:
                completed = subprocess.CompletedProcess(
                    args=completed.args,
                    returncode=completed.returncode,
                    stdout=file_text,
                    stderr=completed.stderr,
                )
            try:
                last_message_path.unlink()
            except FileNotFoundError:
                pass

        return completed

    def _parse_stdout(self, stdout: str) -> ModelTurn:
        text = stdout.strip()
        if not text:
            return ModelTurn()

        try:
            return _turn_from_json_data(json.loads(text))
        except json.JSONDecodeError:
            pass

        last_turn = ModelTurn()
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                last_turn = _turn_from_json_data(json.loads(line))
            except json.JSONDecodeError:
                continue

        if last_turn.content is not None or last_turn.tool_calls:
            return last_turn

        return ModelTurn(content=text)

    def step(
        self,
        *,
        instructions: str,
        messages: Sequence[ChatMessage],
        tools: Sequence[ToolSpec],
        temperature: float,
    ) -> ModelTurn:
        prompt = self._build_prompt(
            instructions=instructions,
            messages=messages,
            tools=tools,
        )
        completed = self._invoke(prompt)
        if completed.returncode != 0:
            raise RuntimeError(
                "Command adapter failed with exit code "
                f"{completed.returncode}: {completed.stderr.strip()}"
            )
        return self._parse_stdout(completed.stdout)


def claude_code_adapter(
    *,
    command: Sequence[str] | None = None,
    prompt_mode: str = "arg",
) -> CommandAdapter:
    return CommandAdapter(
        command=tuple(command or ("claude", "-p", "--output-format", "json")),
        prompt_mode=prompt_mode,
        adapter_type="claude-code",
    )


def codex_adapter(
    *,
    command: Sequence[str] | None = None,
    prompt_mode: str = "arg",
) -> CommandAdapter:
    return CommandAdapter(
        command=tuple(command or ("codex", "exec", "--json")),
        prompt_mode=prompt_mode,
        output_last_message=True,
        adapter_type="codex",
    )


def build_adapter(
    backend: str = "auto",
    *,
    model: str | None = None,
    api_key: str | None = None,
    command: Sequence[str] | None = None,
    prompt_mode: str = "arg",
) -> ModelAdapter:
    backend_name = backend.lower()
    if backend_name == "auto":
        if importlib.util.find_spec("openai") is not None:
            return openai_adapter(model=model or "gpt-5.1")
        if importlib.util.find_spec("anthropic") is not None:
            return anthropic_adapter(model=model or "claude-sonnet-4-20250514", api_key=api_key)
        if shutil.which("claude") is not None:
            return claude_code_adapter(command=command, prompt_mode=prompt_mode)
        if shutil.which("codex") is not None:
            return codex_adapter(command=command, prompt_mode=prompt_mode)
        raise RuntimeError(
            "No supported backend detected. Install `openai` or `anthropic`, or ensure `claude`/`codex` is on PATH."
        )
    if backend_name == "openai":
        return openai_adapter(model=model or "gpt-5.1")
    if backend_name == "anthropic":
        return anthropic_adapter(model=model or "claude-sonnet-4-20250514", api_key=api_key)
    if backend_name in {"claude", "claude-code"}:
        return claude_code_adapter(command=command, prompt_mode=prompt_mode)
    if backend_name == "codex":
        return codex_adapter(command=command, prompt_mode=prompt_mode)
    raise ValueError(f"Unknown backend: {backend}")
