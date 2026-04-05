"""Minimal ReACT agent core."""

from __future__ import annotations

import ast
from datetime import datetime, timezone
from typing import Any, Callable, Sequence

from .adapters import build_adapter
from .types import ChatMessage, ModelAdapter, ToolSpec, serialize_output


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


class ReActAgent:
    """A small ReACT agent that loops through model calls and local tools."""

    agent_type = "ReACT"

    def __init__(
        self,
        *,
        adapter: ModelAdapter | None = None,
        instructions: str | None = None,
        temperature: float = 0.0,
        tools: Sequence[ToolSpec] | None = None,
    ) -> None:
        self.adapter = adapter or build_adapter("auto")
        self.instructions = instructions or (
            "You are a ReACT agent. Use tools when they help. "
            "Think privately, call tools one step at a time, and answer succinctly."
        )
        self.temperature = temperature
        self._tools: dict[str, ToolSpec] = {tool.name: tool for tool in (tools or [])}

    def register_tool(self, tool: ToolSpec) -> None:
        self._tools[tool.name] = tool

    def _tool_payload(self) -> list[ToolSpec]:
        return list(self._tools.values())

    def run(self, prompt: str, *, max_steps: int = 8) -> str:
        """Run the agent until it produces a final answer or hits max_steps."""

        messages: list[ChatMessage] = [ChatMessage(role="user", content=prompt)]

        for _ in range(max_steps):
            turn = self.adapter.step(
                instructions=self.instructions,
                messages=messages,
                tools=self._tool_payload(),
                temperature=self.temperature,
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
                    return final_text
                raise RuntimeError("The model returned no final text and no tool calls.")

            for call in turn.tool_calls:
                tool = self._tools.get(call.name)
                if tool is None:
                    raise KeyError(f"Unknown tool requested by model: {call.name}")

                output = serialize_output(tool.handler(call.arguments))
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


def build_agent(
    *,
    adapter: ModelAdapter | None = None,
    tools: Sequence[ToolSpec] | None = None,
) -> ReActAgent:
    return ReActAgent(
        adapter=adapter,
        tools=tools or [calculator_tool(), utc_now_tool()],
    )
