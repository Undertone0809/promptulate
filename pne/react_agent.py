"""Minimal ReACT agent built on OpenAI's Responses API.

This uses the official Responses API function-calling loop:
user prompt -> model -> function call(s) -> tool output(s) -> model -> final answer.
"""

from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable

from openai import OpenAI

JsonObject = dict[str, Any]
ToolHandler = Callable[[JsonObject], Any]


def _json_default(value: Any) -> str:
    return str(value)


def _serialize_output(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, default=_json_default)


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


def calculator_tool() -> "ToolSpec":
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


def utc_now_tool() -> "ToolSpec":
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


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    parameters: JsonObject
    handler: ToolHandler
    strict: bool = True

    def as_openai_tool(self) -> JsonObject:
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "strict": self.strict,
        }


class ReActAgent:
    """A small ReACT agent that loops through model calls and local tools."""

    agent_type = "ReACT"

    def __init__(
        self,
        *,
        client: OpenAI | None = None,
        model: str = "gpt-5.1",
        instructions: str | None = None,
        reasoning_effort: str | None = "low",
        temperature: float = 0.0,
        tools: list[ToolSpec] | None = None,
    ) -> None:
        self.client = client or OpenAI()
        self.model = model
        self.instructions = instructions or (
            "You are a ReACT agent. Use tools when they help. "
            "Think privately, call tools one step at a time, and answer succinctly."
        )
        self.reasoning_effort = reasoning_effort
        self.temperature = temperature
        self._tools: dict[str, ToolSpec] = {tool.name: tool for tool in (tools or [])}

    def register_tool(self, tool: ToolSpec) -> None:
        self._tools[tool.name] = tool

    def _tool_payload(self) -> list[JsonObject]:
        return [tool.as_openai_tool() for tool in self._tools.values()]

    def run(self, prompt: str, *, max_steps: int = 8) -> str:
        """Run the agent until it produces a final answer or hits max_steps."""

        previous_response_id: str | None = None
        input_items: list[JsonObject] = [
            {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": prompt}],
            }
        ]

        for _ in range(max_steps):
            request: JsonObject = {
                "model": self.model,
                "instructions": self.instructions,
                "input": input_items,
                "tools": self._tool_payload(),
                "tool_choice": "auto",
                "parallel_tool_calls": False,
                "temperature": self.temperature,
            }
            if previous_response_id is not None:
                request["previous_response_id"] = previous_response_id
            if self.reasoning_effort is not None:
                request["reasoning"] = {"effort": self.reasoning_effort}

            response = self.client.responses.create(**request)
            previous_response_id = response.id

            tool_calls = [
                item
                for item in response.output
                if getattr(item, "type", None) == "function_call"
            ]
            if not tool_calls:
                final_text = (response.output_text or "").strip()
                if final_text:
                    return final_text
                raise RuntimeError(
                    "The model returned no final text and no tool calls."
                )

            input_items = []
            for call in tool_calls:
                tool = self._tools.get(call.name)
                if tool is None:
                    raise KeyError(f"Unknown tool requested by model: {call.name}")

                try:
                    arguments = json.loads(call.arguments or "{}")
                except json.JSONDecodeError as exc:
                    raise ValueError(
                        f"Invalid JSON arguments from tool call {call.name}: {call.arguments}"
                    ) from exc

                output = _serialize_output(tool.handler(arguments))
                input_items.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": output,
                    }
                )

        raise RuntimeError(
            f"Reached max_steps={max_steps} without producing a final answer."
        )


def build_agent(
    *,
    client: OpenAI | None = None,
    model: str = "gpt-5.1",
    reasoning_effort: str | None = "low",
) -> ReActAgent:
    return ReActAgent(
        client=client,
        model=model,
        reasoning_effort=reasoning_effort,
        tools=[calculator_tool(), utc_now_tool()],
    )
