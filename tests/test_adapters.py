from __future__ import annotations

import json
import sys
import types
from subprocess import CompletedProcess
from unittest import TestCase
from unittest.mock import patch

from pne.adapters import (
    _coerce_text,
    _messages_to_openai,
    _tool_calls_from_payload,
    _turn_from_json_data,
    build_adapter,
    claude_code_adapter,
    codex_adapter,
    CommandAdapter,
    openai_adapter,
    anthropic_adapter,
)
from pne.types import ChatMessage, ToolCall, ToolSpec


class _FakeOpenAIFunc:
    def __init__(self) -> None:
        self.last_kwargs = None

    def create(self, **kwargs) -> object:
        self.last_kwargs = kwargs
        return types.SimpleNamespace(
            choices=[
                types.SimpleNamespace(
                    message=types.SimpleNamespace(
                        content="ok",
                        tool_calls=[
                            types.SimpleNamespace(
                                id="tool-1",
                                function=types.SimpleNamespace(
                                    name="calculator",
                                    arguments='{"expression": "1+2"}',
                                ),
                            )
                        ],
                    )
                )
            ]
        )


class _FakeOpenAIChat:
    def __init__(self) -> None:
        self.completions = _FakeOpenAIFunc()


class _FakeOpenAIClient:
    def __init__(self) -> None:
        self.chat = _FakeOpenAIChat()


class _FakeAnthropicMessage:
    def __init__(self) -> None:
        self.last_kwargs = None

    def create(self, **kwargs) -> object:
        self.last_kwargs = kwargs
        return types.SimpleNamespace(
            content=[
                types.SimpleNamespace(type="text", text="done"),
                types.SimpleNamespace(
                    type="tool_use",
                    id="tool-1",
                    name="calculator",
                    input={"expression": "1+2"},
                ),
            ]
        )


class _FakeAnthropicMessages:
    def __init__(self) -> None:
        self.create = _FakeAnthropicMessage().create


class _FakeAnthropicClient:
    def __init__(self, *args, **kwargs) -> None:
        self.messages = _FakeAnthropicMessages()


class TestAdapters(TestCase):
    @staticmethod
    def _calculator_tool() -> ToolSpec:
        return ToolSpec(
            name="calculator",
            description="math",
            parameters={},
            handler=lambda args: args,
        )

    def test_openai_adapter_step_parses_tool_calls(self) -> None:
        fake_module = types.SimpleNamespace(OpenAI=_FakeOpenAIClient)
        with patch.dict(sys.modules, {"openai": fake_module}):
            adapter = openai_adapter(model="gpt-5-test")
            turn = adapter.step(
                instructions="i",
                messages=[ChatMessage(role="user", content="x")],
                tools=[self._calculator_tool()],
                temperature=0.1,
            )

            self.assertEqual("ok", turn.content)
            tool = list(turn.tool_calls)[0]
            self.assertEqual("calculator", tool.name)
            self.assertEqual({"expression": "1+2"}, tool.arguments)

    def test_openai_adapter_builds_expected_payload(self) -> None:
        fake_module = types.SimpleNamespace(OpenAI=_FakeOpenAIClient)
        with patch.dict(sys.modules, {"openai": fake_module}):
            adapter = openai_adapter(model="gpt-5-test")
            adapter.step(
                instructions="system-instruction",
                messages=[ChatMessage(role="user", content="x")],
                tools=[self._calculator_tool()],
                temperature=0.2,
            )

            fake_create = adapter.client.chat.completions  # type: ignore[attr-defined]
            self.assertEqual("gpt-5-test", fake_create.last_kwargs["model"])
            self.assertEqual(0.2, fake_create.last_kwargs["temperature"])
            self.assertEqual("auto", fake_create.last_kwargs["tool_choice"])
            self.assertEqual(
                "system-instruction", fake_create.last_kwargs["messages"][0]["content"]
            )

    def test_anthropic_adapter_step_parses_text_and_tools(self) -> None:
        fake_module = types.SimpleNamespace(Anthropic=_FakeAnthropicClient)
        with patch.dict(sys.modules, {"anthropic": fake_module}):
            adapter = anthropic_adapter(model="claude-test", api_key="x")
            turn = adapter.step(
                instructions="i",
                messages=[ChatMessage(role="user", content="x")],
                tools=[self._calculator_tool()],
                temperature=0.0,
            )

            self.assertEqual("done", turn.content)
            tool_calls = list(turn.tool_calls)
            self.assertEqual(1, len(tool_calls))
            self.assertEqual("calculator", tool_calls[0].name)
            self.assertEqual({"expression": "1+2"}, tool_calls[0].arguments)

    def test_command_adapter_parses_tool_call_output(self) -> None:
        with patch("pne.adapters.subprocess.run") as run:
            run.return_value = CompletedProcess(
                args=["echo", "payload"],
                returncode=0,
                stdout=json.dumps(
                    {
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "tool-1",
                                "name": "calculator",
                                "arguments": {"expression": "1+2"},
                            }
                        ],
                    }
                ),
                stderr="",
            )
            adapter = CommandAdapter(command=("echo",), prompt_mode="arg")
            turn = adapter.step(
                instructions="i",
                messages=[ChatMessage(role="user", content="x")],
                tools=[],
                temperature=0.0,
            )

            self.assertEqual("calculator", list(turn.tool_calls)[0].name)
            self.assertEqual({"expression": "1+2"}, turn.tool_calls[0].arguments)

    def test_command_adapter_raises_for_non_zero_exit(self) -> None:
        with patch("pne.adapters.subprocess.run") as run:
            run.return_value = CompletedProcess(
                args=["echo", "payload"],
                returncode=1,
                stdout="",
                stderr="boom",
            )
            adapter = CommandAdapter(command=("echo",), prompt_mode="arg")
            with self.assertRaisesRegex(RuntimeError, "Command adapter failed with exit code 1"):
                adapter.step(
                    instructions="i",
                    messages=[ChatMessage(role="user", content="x")],
                    tools=[],
                    temperature=0.0,
                )

    def test_messages_to_openai_converts_tool_calls(self) -> None:
        messages = [
            ChatMessage(role="user", content="x"),
            ChatMessage(
                role="assistant",
                content="think",
                tool_calls=[
                    ToolCall(id="a", name="calculator", arguments={"expression": "1+1"})
                ],
            ),
            ChatMessage(
                role="tool",
                content='{"result": 2}',
                name="calculator",
                tool_call_id="a",
            ),
        ]
        payload = _messages_to_openai(messages)
        self.assertEqual("user", payload[0]["role"])
        self.assertEqual("assistant", payload[1]["role"])
        self.assertEqual("tool", payload[2]["role"])
        self.assertEqual("a", payload[2]["tool_call_id"])
        self.assertEqual("calculator", payload[2]["name"])

    def test_tool_calls_from_payload_json_argument_str(self) -> None:
        payload = [
            {
                "id": "tool-1",
                "name": "calculator",
                "arguments": '{"expression": "2+2"}',
            }
        ]
        calls = _tool_calls_from_payload(payload)
        self.assertEqual("calculator", calls[0].name)
        self.assertEqual({"expression": "2+2"}, calls[0].arguments)

    def test_turn_from_nested_json(self) -> None:
        wrapped = _turn_from_json_data({"content": "{\"content\": \"value\"}"})
        self.assertEqual("value", wrapped.content)

    def test_coerce_text_collects_text_parts(self) -> None:
        got = _coerce_text([
            {"text": "a"},
            "b",
            {"no_text": 1},
            3,
        ])
        self.assertEqual("ab", got)

    def test_build_adapter_auto_prefers_openai_when_available(self) -> None:
        with patch("pne.adapters.importlib.util.find_spec") as find_spec:
            find_spec.side_effect = lambda name: object() if name == "openai" else None
            with patch("pne.adapters.openai_adapter") as fake_openai_adapter:
                fake_openai_adapter.return_value = "OPENAI"
                self.assertEqual("OPENAI", build_adapter("auto"))

    def test_build_adapter_auto_falls_back_to_anthropic(self) -> None:
        with patch("pne.adapters.importlib.util.find_spec") as find_spec:
            find_spec.side_effect = lambda name: None if name == "openai" else (
                object() if name == "anthropic" else None
            )
            with patch("pne.adapters.anthropic_adapter") as fake_anthropic_adapter:
                fake_anthropic_adapter.return_value = "ANTHROPIC"
                self.assertEqual("ANTHROPIC", build_adapter("auto"))

    def test_build_adapter_auto_falls_back_to_claude_and_codex(self) -> None:
        with patch("pne.adapters.importlib.util.find_spec") as find_spec:
            find_spec.side_effect = lambda name: None
            with patch("pne.adapters.shutil.which") as which:
                which.side_effect = lambda cmd: "/usr/bin/" + cmd if cmd == "claude" else None
                adapter = build_adapter("auto")
                self.assertEqual("claude-code", adapter.adapter_type)

                which.side_effect = lambda cmd: "/usr/bin/" + cmd if cmd == "codex" else None
                adapter = build_adapter("auto")
                self.assertEqual("codex", adapter.adapter_type)

    def test_build_adapter_explicit_backends(self) -> None:
        with patch("pne.adapters.openai_adapter") as openai_backend, patch(
            "pne.adapters.anthropic_adapter"
        ) as anthropic_backend:
            openai_backend.return_value = "OPENAI"
            anthropic_backend.return_value = "ANTHROPIC"
            self.assertEqual("OPENAI", build_adapter("openai"))
            self.assertEqual("ANTHROPIC", build_adapter("anthropic"))

    def test_build_adapter_unknown_backend(self) -> None:
        with self.assertRaises(ValueError):
            build_adapter("unknown")

    def test_alias_adapters_are_configured(self) -> None:
        claude = claude_code_adapter()
        self.assertEqual("claude-code", claude.adapter_type)
        self.assertEqual("arg", claude.prompt_mode)

        codex = codex_adapter()
        self.assertEqual("codex", codex.adapter_type)
        self.assertTrue(codex.output_last_message)

    def test_build_adapter_without_backend_raises(self) -> None:
        with patch("pne.adapters.importlib.util.find_spec", return_value=None):
            with patch("pne.adapters.shutil.which", return_value=None):
                with self.assertRaises(RuntimeError):
                    build_adapter("auto")
