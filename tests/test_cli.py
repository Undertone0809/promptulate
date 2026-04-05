from __future__ import annotations

import io
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from unittest import TestCase
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from pne_cli.__main__ import (
    AgentEvent,
    _build_parser,
    _build_tools,
    _consume_events,
    _load_trace_writer,
)
from pne import ToolSpec


class _FakeAgent:
    def __init__(self, events: list[AgentEvent]):
        self._events = list(events)

    async def run_stream(self, *args, **kwargs):
        for event in self._events:
            yield event


class TestCLI(TestCase):
    def test_build_parser_has_chat_and_ask(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["chat", "--max-steps", "5"])
        self.assertEqual("chat", args.command)
        self.assertEqual(5, args.max_steps)

        args = parser.parse_args(["ask", "--allow-write", "hello"])
        self.assertEqual("ask", args.command)
        self.assertEqual("hello", " ".join(args.prompt))

    def test_trace_writer_can_be_disabled(self) -> None:
        write, close = _load_trace_writer(None)
        self.assertIsNone(write({}))
        close()

    def test_trace_writer_appends_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "trace.jsonl"
            write, close = _load_trace_writer(str(path))
            try:
                write({"type": "final", "content": "x"})
                write({"type": "model_turn", "tool_calls": []})
            finally:
                close()
            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(2, len(lines))
            self.assertIn('"content": "x"', lines[0])

    def test_build_tools_wraps_command_and_write_with_confirmation(self) -> None:
        tools = [
            ToolSpec(
                name="run_command",
                description="",
                parameters={},
                handler=lambda args: {"status": "ran"},
            ),
            ToolSpec(
                name="write_file",
                description="",
                parameters={},
                handler=lambda args: {"status": "written"},
            ),
            ToolSpec(name="calculator", description="", parameters={}, handler=lambda args: {"ok": True}),
        ]
        with patch("pne_cli.__main__.build_local_tools", return_value=tools):
            with patch("pne_cli.__main__._prompt_once", side_effect=["n", "y"]):
                wrapped = _build_tools(
                    base_dir="/tmp",
                    allow_write=True,
                    approve_commands=True,
                )
                wrapped_by_name = {tool.name: tool for tool in wrapped}
                self.assertEqual({"status": "rejected", "tool": "run_command"}, wrapped_by_name["run_command"].handler({}))
                self.assertEqual({"status": "written"}, wrapped_by_name["write_file"].handler({}))
                self.assertEqual({"ok": True}, wrapped_by_name["calculator"].handler({}))

class TestCLIAsync(IsolatedAsyncioTestCase):
    async def test_consume_events_prints_step_tool_and_final(self) -> None:
        events = [
            {"type": "step_start", "agent": "agent", "step": 1, "messages": 0},
            {"type": "model_turn", "step": 1, "tool_calls": [{"id": "1", "name": "calculator", "arguments": {}}]},
            {"type": "tool_call", "step": 1, "tool_call": {"name": "calculator", "id": "1", "arguments": {}}},
            {"type": "tool_output", "step": 1, "tool": "calculator", "output": "2"},
            {"type": "final", "step": 1, "content": "done"},
        ]
        agent = _FakeAgent(events)
        out = io.StringIO()

        with redirect_stdout(out):
            final_text = await _consume_events(
                prompt="hello",
                agent=agent,
                max_steps=2,
                on_step=lambda event: None,
                quiet=False,
                history=[],
            )
        self.assertEqual("done", final_text)
        text = out.getvalue()
        self.assertIn("[step 1]", text)
        self.assertIn("assistant: thinking...", text)
        self.assertIn("tool_output: 2", text)
        self.assertIn("final: done", text)
