"""Core agent implementations for PNE."""

from __future__ import annotations

import ast
import asyncio
import json
import inspect
from datetime import datetime, timezone
from typing import Any, AsyncIterator, Callable, Sequence

from .adapters import build_adapter
from .skills import LocalSkill, skill_context
from .types import (
    AgentEvent,
    ChatMessage,
    ModelAdapter,
    ModelTurn,
    ToolCall,
    ToolSpec,
    serialize_output,
)


def _safe_calculate(expression: str) -> int | float:
    """Evaluate a simple arithmetic expression safely."""

    allowed_binops: dict[type[ast.AST], Callable[[Any, Any], Any]] = {
        ast.Add: lambda a, b: a + b,
        ast.Sub: lambda a, b: a - b,
        ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: a / b,
        ast.FloorDiv: lambda a, b: a // b,
        ast.Mod: lambda a, b: a % b,
        ast.Pow: lambda a, b: a**b,
    }
    allowed_unaryops: dict[type[ast.AST], Callable[[Any], Any]] = {
        ast.UAdd: lambda a: a,
        ast.USub: lambda a: -a,
    }

    def evaluate(node: ast.AST) -> Any:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp):
            operator = allowed_binops.get(type(node.op))
            if operator is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            return operator(evaluate(node.left), evaluate(node.right))
        if isinstance(node, ast.UnaryOp):
            operator = allowed_unaryops.get(type(node.op))
            if operator is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            return operator(evaluate(node.operand))
        raise ValueError(f"Unsupported expression: {type(node).__name__}")

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree)


def calculator_tool() -> ToolSpec:
    return ToolSpec(
        name="calculator",
        description="Evaluate a simple arithmetic expression using +, -, *, /, //, %, ** and parentheses.",
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Arithmetic expression to evaluate.",
                }
            },
            "required": ["expression"],
            "additionalProperties": False,
        },
        handler=lambda args: {"result": _safe_calculate(args["expression"])},
    )


def utc_now_tool() -> ToolSpec:
    return ToolSpec(
        name="utc_now",
        description="Return the current UTC time in ISO 8601 format.",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        handler=lambda args: {"utc_now": datetime.now(timezone.utc).isoformat()},
    )


def _with_skill_context(
    instructions: str,
    skills: Sequence[LocalSkill] | None = None,
) -> str:
    if not skills:
        return instructions

    context = skill_context(skills)
    if not context:
        return instructions

    return f"{instructions}\n\n{context}"


class Agent:
    """A generic tool-calling agent with step-by-step model/action loops."""

    agent_type = "Agent"

    def __init__(
        self,
        *,
        adapter: ModelAdapter | None = None,
        instructions: str | None = None,
        temperature: float = 0.0,
        tools: Sequence[ToolSpec] | None = None,
        skills: Sequence[LocalSkill] | None = None,
    ) -> None:
        self.adapter = adapter or build_adapter("auto")
        self.instructions = _with_skill_context(
            instructions
            or (
                "You are a practical agent. Use tools when they help, "
                "then answer succinctly."
            ),
            skills,
        )
        self.temperature = temperature
        self._tools: dict[str, ToolSpec] = {tool.name: tool for tool in (tools or [])}

    def register_tool(self, tool: ToolSpec) -> None:
        self._tools[tool.name] = tool

    def _tool_payload(self) -> list[ToolSpec]:
        return list(self._tools.values())

    def _emit_event(
        self,
        event: AgentEvent,
        *,
        on_step: Callable[[dict[str, Any]], None] | None = None,
        verbose: bool = False,
    ) -> None:
        if on_step is not None:
            on_step(event)
        if verbose:
            print(json.dumps(event, ensure_ascii=False, indent=2))

    def _step_start_event(self, step: int, messages: list[ChatMessage]) -> AgentEvent:
        return {
            "type": "step_start",
            "agent": self.agent_type,
            "step": step,
            "messages": len(messages),
        }

    def _model_turn_event(
        self,
        step: int,
        turn_content: str | None,
        tool_calls: Sequence[ToolCall],
    ) -> AgentEvent:
        return {
            "type": "model_turn",
            "step": step,
            "agent": self.agent_type,
            "content": turn_content,
            "tool_calls": [
                {"name": call.name, "id": call.id, "arguments": call.arguments}
                for call in tool_calls
            ],
        }

    def _tool_call_event(self, step: int, call: ToolCall) -> AgentEvent:
        return {
            "type": "tool_call",
            "agent": self.agent_type,
            "step": step,
            "tool_call": {
                "id": call.id,
                "name": call.name,
                "arguments": call.arguments,
            },
        }

    def _tool_output_event(self, step: int, tool: str, output: str) -> AgentEvent:
        return {
            "type": "tool_output",
            "agent": self.agent_type,
            "step": step,
            "tool": tool,
            "output": output,
        }

    def _final_event(self, step: int, final_text: str) -> AgentEvent:
        return {
            "type": "final",
            "agent": self.agent_type,
            "step": step,
            "content": final_text,
        }

    async def _call_model(self, **kwargs: Any) -> ModelTurn:
        step_async = getattr(self.adapter, "step_async", None)
        if step_async is not None:
            result = step_async(**kwargs)
            if inspect.isawaitable(result):
                return await result
            return result
        return await asyncio.to_thread(self.adapter.step, **kwargs)

    async def _call_tool(self, handler: Callable[[dict[str, Any]], Any], arguments: dict[str, Any]) -> Any:
        if inspect.iscoroutinefunction(handler):
            return await handler(arguments)
        result = handler(arguments)
        if inspect.isawaitable(result):
            return await result
        return await asyncio.to_thread(handler, arguments)

    def run(
        self,
        prompt: str,
        *,
        max_steps: int = 8,
        verbose: bool = False,
        on_step: Callable[[dict[str, Any]], None] | None = None,
    ) -> str:
        """Run the agent until it produces a final answer or hits max_steps."""

        messages: list[ChatMessage] = [ChatMessage(role="user", content=prompt)]

        for step in range(1, max_steps + 1):
            self._emit_event(
                self._step_start_event(step=step, messages=messages),
                on_step=on_step,
                verbose=verbose,
            )
            turn = self.adapter.step(
                instructions=self.instructions,
                messages=messages,
                tools=self._tool_payload(),
                temperature=self.temperature,
            )
            self._emit_event(
                self._model_turn_event(
                    step=step, turn_content=turn.content, tool_calls=turn.tool_calls
                ),
                on_step=on_step,
                verbose=verbose,
            )
            if turn.content is not None:
                messages.append(
                    ChatMessage(
                        role="assistant",
                        content=turn.content,
                        tool_calls=list(turn.tool_calls),
                    )
                )
            if not turn.tool_calls:
                final_text = (turn.content or "").strip()
                if final_text:
                    self._emit_event(
                        self._final_event(step=step, final_text=final_text),
                        on_step=on_step,
                        verbose=verbose,
                    )
                    return final_text
                raise RuntimeError("The model returned no final text and no tool calls.")

            for call in turn.tool_calls:
                tool = self._tools.get(call.name)
                if tool is None:
                    raise KeyError(f"Unknown tool requested by model: {call.name}")

                self._emit_event(
                    self._tool_call_event(step=step, call=call),
                    on_step=on_step,
                    verbose=verbose,
                )
                output = serialize_output(tool.handler(call.arguments))
                self._emit_event(
                    self._tool_output_event(step=step, tool=call.name, output=output),
                    on_step=on_step,
                    verbose=verbose,
                )
                messages.append(
                    ChatMessage(
                        role="tool",
                        content=output,
                        name=call.name,
                        tool_call_id=call.id,
                    )
                )

        raise RuntimeError(
            f"Reached max_steps={max_steps} without producing a final answer."
        )

    async def run_stream(
        self,
        prompt: str,
        *,
        max_steps: int = 8,
        verbose: bool = False,
        on_step: Callable[[dict[str, Any]], None] | None = None,
    ) -> AsyncIterator[AgentEvent]:
        """Run the agent and emit events as an async iterator."""

        messages: list[ChatMessage] = [ChatMessage(role="user", content=prompt)]

        for step in range(1, max_steps + 1):
            step_start_event = self._step_start_event(step=step, messages=messages)
            self._emit_event(
                step_start_event,
                on_step=on_step,
                verbose=verbose,
            )
            yield step_start_event

            turn = await self._call_model(
                instructions=self.instructions,
                messages=messages,
                tools=self._tool_payload(),
                temperature=self.temperature,
            )
            model_turn_event = self._model_turn_event(
                step=step, turn_content=turn.content, tool_calls=turn.tool_calls
            )
            self._emit_event(
                model_turn_event,
                on_step=on_step,
                verbose=verbose,
            )
            yield model_turn_event

            if turn.content is not None:
                messages.append(
                    ChatMessage(
                        role="assistant",
                        content=turn.content,
                        tool_calls=list(turn.tool_calls),
                    )
                )

            if not turn.tool_calls:
                final_text = (turn.content or "").strip()
                if final_text:
                    final_event = self._final_event(step=step, final_text=final_text)
                    self._emit_event(
                        final_event,
                        on_step=on_step,
                        verbose=verbose,
                    )
                    yield final_event
                    return
                raise RuntimeError("The model returned no final text and no tool calls.")

            for call in turn.tool_calls:
                tool = self._tools.get(call.name)
                if tool is None:
                    raise KeyError(f"Unknown tool requested by model: {call.name}")

                tool_call_event = self._tool_call_event(step=step, call=call)
                self._emit_event(
                    tool_call_event,
                    on_step=on_step,
                    verbose=verbose,
                )
                yield tool_call_event

                output = serialize_output(
                    await self._call_tool(tool.handler, call.arguments)
                )
                tool_output_event = self._tool_output_event(
                    step=step,
                    tool=call.name,
                    output=output,
                )
                self._emit_event(
                    tool_output_event,
                    on_step=on_step,
                    verbose=verbose,
                )
                yield tool_output_event

                messages.append(
                    ChatMessage(
                        role="tool",
                        content=output,
                        name=call.name,
                        tool_call_id=call.id,
                    )
                )

        raise RuntimeError(
            f"Reached max_steps={max_steps} without producing a final answer."
        )


class ReActAgent(Agent):
    """Experimental ReACT agent implementation."""

    agent_type = "ReACT"

    def __init__(
        self,
        *,
        adapter: ModelAdapter | None = None,
        instructions: str | None = None,
        temperature: float = 0.0,
        tools: Sequence[ToolSpec] | None = None,
        skills: Sequence[LocalSkill] | None = None,
    ) -> None:
        super().__init__(
            adapter=adapter,
            instructions=instructions
            or (
                "You are a ReACT agent. Use tools when they help. "
                "Think privately, call tools one step at a time, and answer succinctly."
            ),
            temperature=temperature,
            tools=tools,
            skills=skills,
        )


def build_agent(
    *,
    adapter: ModelAdapter | None = None,
    tools: Sequence[ToolSpec] | None = None,
    instructions: str | None = None,
    temperature: float = 0.0,
    skills: Sequence[LocalSkill] | None = None,
) -> Agent:
    return Agent(
        adapter=adapter,
        tools=tools or [calculator_tool(), utc_now_tool()],
        instructions=instructions,
        temperature=temperature,
        skills=skills,
    )


def build_react_agent(
    *,
    adapter: ModelAdapter | None = None,
    tools: Sequence[ToolSpec] | None = None,
    instructions: str | None = None,
    temperature: float = 0.0,
    skills: Sequence[LocalSkill] | None = None,
) -> ReActAgent:
    return ReActAgent(
        adapter=adapter,
        tools=tools or [calculator_tool(), utc_now_tool()],
        instructions=instructions,
        temperature=temperature,
        skills=skills,
    )
