from __future__ import annotations

from datetime import datetime
from unittest import TestCase

from pne.types import ChatMessage, ModelTurn, ToolCall, ToolSpec, serialize_output


class TestTypes(TestCase):
    def test_tool_spec_payloads(self) -> None:
        tool = ToolSpec(
            name="echo",
            description="echo tool",
            parameters={"type": "object"},
            handler=lambda args: args,
            strict=False,
        )
        self.assertEqual(
            {
                "type": "function",
                "name": "echo",
                "description": "echo tool",
                "parameters": {"type": "object"},
                "strict": False,
            },
            tool.as_tool_payload(),
        )
        self.assertEqual(tool.as_openai_tool(), tool.as_tool_payload())

    def test_serialize_output(self) -> None:
        self.assertEqual("hello", serialize_output("hello"))
        self.assertEqual('{"a": 1}', serialize_output({"a": 1}))

    def test_serialize_output_with_unknown_object(self) -> None:
        class Item:
            def __str__(self) -> str:
                return "item"

        self.assertEqual('"item"', serialize_output(Item()))

    def test_dataclass_defaults(self) -> None:
        msg = ChatMessage(role="system")
        self.assertIsNone(msg.content)
        self.assertIsNone(msg.name)
        self.assertIsNone(msg.tool_call_id)
        self.assertEqual([], msg.tool_calls)

        model_turn = ModelTurn()
        self.assertIsNone(model_turn.content)
        self.assertEqual((), model_turn.tool_calls)

    def test_tool_call_fields(self) -> None:
        call = ToolCall(name="x", arguments={"a": 1}, id="1")
        self.assertEqual("x", call.name)
        self.assertEqual("1", call.id)
