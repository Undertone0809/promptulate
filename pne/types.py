"""Shared types for the PNE SDK."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable, Literal, Protocol, Sequence

JsonObject = dict[str, Any]
ToolHandler = Callable[[JsonObject], Any]


def _json_default(value: Any) -> str:
    return str(value)


def serialize_output(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, default=_json_default)


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    parameters: JsonObject
    handler: ToolHandler
    strict: bool = True

    def as_tool_payload(self) -> JsonObject:
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "strict": self.strict,
        }

    def as_openai_tool(self) -> JsonObject:
        return self.as_tool_payload()


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: JsonObject
    id: str


@dataclass
class ChatMessage:
    role: Literal["system", "user", "assistant", "tool"]
    content: str | None = None
    name: str | None = None
    tool_call_id: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)


@dataclass(frozen=True)
class ModelTurn:
    content: str | None = None
    tool_calls: tuple[ToolCall, ...] = ()


class ModelAdapter(Protocol):
    adapter_type: str

    def step(
        self,
        *,
        instructions: str,
        messages: Sequence[ChatMessage],
        tools: Sequence[ToolSpec],
        temperature: float,
    ) -> ModelTurn:
        """Generate one turn of model output."""

