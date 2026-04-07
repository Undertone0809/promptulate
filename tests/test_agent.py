from __future__ import annotations

import asyncio
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import patch

from pne.agent import (
    Agent,
    ReActAgent,
    _safe_calculate,
    build_agent,
    build_react_agent,
    calculator_tool,
    utc_now_tool,
)
from pne.skills import LocalSkill
from pne.types import ModelTurn, ToolCall


class _FakeAdapter:
    def __init__(self, turns: list[ModelTurn]):
        self._turns = list(turns)
        self.calls: list[tuple[str, list[Any], list[Any], float]] = []

    def step(
        self,
        *,
        instructions: str,
        messages: list[Any],
        tools: list[Any],
        temperature: float,
    ) -> ModelTurn:
        self.calls.append((instructions, messages, tools, temperature))
        return self._turns.pop(0)


class TestAgent(TestCase):
    def test_build_agent_defaults_have_builtin_tools(self) -> None:
        adapter = _FakeAdapter([ModelTurn(content="ok")])
        agent = build_agent(adapter=adapter)
        self.assertEqual({"calculator", "utc_now"}, set(agent._tools.keys()))

    def test_agent_run_without_tool_calls_returns_final(self) -> None:
        adapter = _FakeAdapter([ModelTurn(content="final answer")])
        agent = build_agent(adapter=adapter)
        got = agent.run("What is 2 + 2?", max_steps=2, verbose=False)

        self.assertEqual("final answer", got)
        self.assertEqual(1, len(adapter.calls))
        _, messages, _tools, temperature = adapter.calls[0]
        self.assertEqual("What is 2 + 2?", messages[0].content)
        self.assertEqual(0.0, temperature)

    def test_agent_runs_tool_then_returns_final(self) -> None:
        adapter = _FakeAdapter(
            [
                ModelTurn(
                    content=None,
                    tool_calls=(
                        ToolCall(
                            id="t1",
                            name="calculator",
                            arguments={"expression": "1+2"},
                        ),
                    ),
                ),
                ModelTurn(content="3"),
            ]
        )
        agent = build_agent(adapter=adapter)
        got = agent.run("Compute 1+2", max_steps=2, verbose=False)

        self.assertEqual("3", got)
        self.assertEqual(2, len(adapter.calls))
        second_messages = adapter.calls[1][1]
        tool_messages = [
            message
            for message in second_messages
            if message.role == "tool"
        ]
        self.assertEqual(1, len(tool_messages))
        self.assertEqual("calculator", tool_messages[0].name)
        self.assertEqual("t1", tool_messages[0].tool_call_id)

    def test_agent_unknown_tool_returns_error_payload_then_can_finish(self) -> None:
        adapter = _FakeAdapter(
            [
                ModelTurn(
                    content=None,
                    tool_calls=(ToolCall(id="bad", name="Skill", arguments={}),),
                ),
                ModelTurn(content="No Skill tool in this host; answering directly."),
            ]
        )
        agent = Agent(adapter=adapter, tools=[])
        got = agent.run("Hello", max_steps=3, verbose=False)

        self.assertEqual("No Skill tool in this host; answering directly.", got)
        second_messages = adapter.calls[1][1]
        tool_msgs = [m for m in second_messages if m.role == "tool"]
        self.assertEqual(1, len(tool_msgs))
        self.assertEqual("Skill", tool_msgs[0].name)
        self.assertIn("unknown_tool", tool_msgs[0].content)
        self.assertIn("Skill", tool_msgs[0].content)

    def test_agent_runs_until_max_steps_and_raises(self) -> None:
        adapter = _FakeAdapter(
            [
                ModelTurn(
                    content=None,
                    tool_calls=(
                        ToolCall(
                            id="loop-1",
                            name="calculator",
                            arguments={"expression": "1+1"},
                        ),
                    ),
                ),
                ModelTurn(
                    content=None,
                    tool_calls=(
                        ToolCall(
                            id="loop-2",
                            name="calculator",
                            arguments={"expression": "2+2"},
                        ),
                    ),
                ),
            ]
        )
        agent = build_agent(adapter=adapter, tools=[calculator_tool(), utc_now_tool()])
        with self.assertRaisesRegex(RuntimeError, "Reached max_steps=2"):
            agent.run("Keep asking for tools", max_steps=2)

    def test_build_react_agent_is_experimental_variant(self) -> None:
        adapter = _FakeAdapter([ModelTurn(content="ok")])
        agent = build_react_agent(adapter=adapter)
        got = agent.run("status")

        self.assertEqual("ok", got)
        self.assertIsInstance(agent, ReActAgent)
        self.assertEqual("ReACT", agent.agent_type)
        self.assertIn("ReACT", agent.instructions)

    def test_build_agent_includes_skills_instructions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "skill"
            skill_dir.mkdir()
            manifest = skill_dir / "SKILL.md"
            manifest.write_text("name: test\ndescription: desc\n\ndesc\n", encoding="utf-8")

            skill = LocalSkill(
                name="test",
                description="desc",
                root=skill_dir,
                manifest_path=manifest,
                instructions="desc",
            )
            adapter = _FakeAdapter([ModelTurn(content="ok")])
            build_agent(adapter=adapter, skills=[skill]).run("x")

            instructions, *_ = adapter.calls[0]
            self.assertIn("Available local skills", instructions)
            self.assertIn("- test: desc", instructions)

    def test_agent_on_step_callback_receives_events(self) -> None:
        adapter = _FakeAdapter([ModelTurn(content="final")])
        events: list[dict[str, Any]] = []
        agent = build_agent(adapter=adapter)

        result = agent.run("hello", on_step=lambda event: events.append(event))
        self.assertEqual("final", result)
        self.assertEqual("step_start", events[0]["type"])
        self.assertEqual("model_turn", events[1]["type"])
        self.assertEqual("final", events[2]["type"])

    def test_run_remains_sync_compatible(self) -> None:
        adapter = _FakeAdapter([ModelTurn(content="legacy final")])
        agent = build_agent(adapter=adapter)

        got = agent.run("Hello")

        self.assertEqual("legacy final", got)
        self.assertEqual(1, len(adapter.calls))
        self.assertEqual("legacy final", got)

    def test_safe_calculate_supports_arithmetic(self) -> None:
        self.assertEqual(7, _safe_calculate("1 + 2 * 3"))
        self.assertEqual(3, _safe_calculate("10 // 3"))
        self.assertEqual(4, _safe_calculate("2 ** 2"))

    def test_safe_calculate_rejects_unsupported_expression(self) -> None:
        with self.assertRaises(ValueError):
            _safe_calculate("1 << 2")

    def test_calculator_tool_returns_expected_result(self) -> None:
        got = calculator_tool().handler({"expression": "4 // 2"})
        self.assertEqual({"result": 2}, got)

    def test_utc_now_tool_returns_iso_timestamp(self) -> None:
        result = utc_now_tool().handler({})
        utc_value = result["utc_now"]
        parsed = datetime.fromisoformat(utc_value)
        self.assertEqual("UTC", parsed.tzinfo.tzname(parsed))


class TestAgentStream(IsolatedAsyncioTestCase):
    async def test_run_stream_yields_step_events_and_final(self) -> None:
        adapter = _FakeAdapter([ModelTurn(content="final in stream")])
        agent = build_agent(adapter=adapter)
        events: list[dict[str, Any]] = []

        async for event in agent.run_stream("Hello", max_steps=3):
            events.append(event)

        self.assertEqual("final", events[-1]["type"])
        self.assertEqual("final in stream", events[-1]["content"])
        self.assertEqual("final in stream", events[-1]["content"])
        self.assertIn("model_delta", [event["type"] for event in events])
        self.assertEqual("step_start", events[0]["type"])
        self.assertEqual("model_turn", events[1]["type"])

    async def test_run_stream_yields_tool_call_and_tool_output(self) -> None:
        adapter = _FakeAdapter(
            [
                ModelTurn(
                    content=None,
                    tool_calls=(
                        ToolCall(
                            id="t-1",
                            name="calculator",
                            arguments={"expression": "1+2"},
                        ),
                    ),
                ),
                ModelTurn(content="3"),
            ]
        )
        agent = build_agent(adapter=adapter)
        events: list[dict[str, Any]] = []

        async for event in agent.run_stream("Use calculator", max_steps=2):
            events.append(event)

        self.assertIn("tool_call", [event["type"] for event in events])
        self.assertIn("tool_output", [event["type"] for event in events])
        self.assertEqual("3", events[-1]["content"])

    async def test_run_stream_with_max_steps_timeout(self) -> None:
        adapter = _FakeAdapter(
            [
                ModelTurn(
                    content=None,
                    tool_calls=(ToolCall(id="loop-1", name="calculator", arguments={"expression": "1+1"}),),
                ),
                ModelTurn(
                    content=None,
                    tool_calls=(ToolCall(id="loop-2", name="calculator", arguments={"expression": "2+2"}),),
                ),
            ]
        )
        agent = build_agent(adapter=adapter)

        with self.assertRaisesRegex(RuntimeError, "Reached max_steps=2"):
            async for _ in agent.run_stream("Loop", max_steps=2):
                pass

    async def test_run_stream_emits_model_delta_events(self) -> None:
        adapter = _FakeAdapter([ModelTurn(content="streaming answer")])
        agent = build_agent(adapter=adapter)
        events: list[dict[str, Any]] = []

        async for event in agent.run_stream("Hello", max_steps=1):
            events.append(event)

        types = [event["type"] for event in events]
        self.assertIn("model_delta", types)
        self.assertTrue(any("streaming" in str(event.get("delta", "")) for event in events if event["type"] == "model_delta"))

    async def test_run_stream_wraps_sync_adapter_in_thread(self) -> None:
        adapter = _FakeAdapter(
            [
                ModelTurn(
                    content=None,
                    tool_calls=(ToolCall(id="t1", name="calculator", arguments={"expression": "1+2"}),),
                ),
                ModelTurn(content="3"),
            ]
        )
        agent = build_agent(adapter=adapter)
        calls: list[Any] = []
        original_to_thread = asyncio.to_thread

        async def fake_to_thread(func: Any, *args: Any, **kwargs: Any):
            calls.append(func)
            return await original_to_thread(func, *args, **kwargs)

        with patch("pne.agent.asyncio.to_thread", side_effect=fake_to_thread):
            async for _ in agent.run_stream("Hello"):
                pass

        self.assertGreaterEqual(len(calls), 2)

    async def test_run_stream_unknown_tool_emits_tool_output_with_error(self) -> None:
        adapter = _FakeAdapter(
            [
                ModelTurn(
                    content=None,
                    tool_calls=(ToolCall(id="x1", name="Skill", arguments={"name": "x"}),),
                ),
                ModelTurn(content="Recovered."),
            ]
        )
        agent = Agent(adapter=adapter, tools=[])
        events: list[dict[str, Any]] = []

        async for event in agent.run_stream("Hi", max_steps=3):
            events.append(event)

        tool_outputs = [e for e in events if e["type"] == "tool_output"]
        self.assertEqual(1, len(tool_outputs))
        self.assertIn("unknown_tool", str(tool_outputs[0].get("output", "")))
        self.assertEqual("final", events[-1]["type"])
        self.assertEqual("Recovered.", events[-1]["content"])
