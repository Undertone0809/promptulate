"""Core agent implementations for PNE."""

from __future__ import annotations

import asyncio
import json
import inspect
from typing import Any, AsyncIterator, Callable, Sequence

from .adapters import build_adapter
from .skills import LocalSkill, skill_context
from .tools import _safe_calculate, calculator_tool, utc_now_tool
from .types import (
    AgentEvent,
    ChatMessage,
    ModelAdapter,
    ModelTurn,
    ToolCall,
    ToolSpec,
    serialize_output,
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

    def _model_delta_event(self, step: int, delta: str) -> AgentEvent:
        return {
            "type": "model_delta",
            "agent": self.agent_type,
            "step": step,
            "delta": delta,
        }

    @staticmethod
    def _iter_chunks(text: str, size: int = 24) -> list[str]:
        if size <= 0:
            return [text]
        return [text[index : index + size] for index in range(0, len(text), size)]

    def _final_event(self, step: int, final_text: str) -> AgentEvent:
        return {
            "type": "final",
            "agent": self.agent_type,
            "step": step,
            "content": final_text,
        }

    def _unknown_tool_payload(self, requested: str) -> dict[str, Any]:
        """Structured error when the model requests a tool we did not register."""
        return {
            "status": "error",
            "error": "unknown_tool",
            "requested_tool": requested,
            "available_tools": sorted(self._tools.keys()),
            "message": (
                f"Tool {requested!r} is not registered in this session. "
                "Use only tools listed in available_tools."
            ),
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

    @staticmethod
    def _prepare_messages(
        prompt: str,
        *,
        history: Sequence[ChatMessage] | None = None,
    ) -> list[ChatMessage]:
        messages: list[ChatMessage] = list(history or [])
        messages.append(ChatMessage(role="user", content=prompt))
        return messages

    def run(
        self,
        prompt: str,
        *,
        max_steps: int = 8,
        verbose: bool = False,
        on_step: Callable[[dict[str, Any]], None] | None = None,
        history: Sequence[ChatMessage] | None = None,
    ) -> str:
        """Run the agent until it produces a final answer or hits max_steps."""
        messages = self._prepare_messages(prompt, history=history)

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
                self._emit_event(
                    self._tool_call_event(step=step, call=call),
                    on_step=on_step,
                    verbose=verbose,
                )
                if tool is None:
                    output = serialize_output(self._unknown_tool_payload(call.name))
                else:
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
        history: Sequence[ChatMessage] | None = None,
    ) -> AsyncIterator[AgentEvent]:
        """Run the agent and emit events as an async iterator."""
        messages = self._prepare_messages(prompt, history=history)

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

            if turn.content:
                for delta in self._iter_chunks(turn.content, 24):
                    model_delta_event = self._model_delta_event(step=step, delta=delta)
                    self._emit_event(
                        model_delta_event,
                        on_step=on_step,
                        verbose=verbose,
                    )
                    yield model_delta_event
                    await asyncio.sleep(0)

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
                tool_call_event = self._tool_call_event(step=step, call=call)
                self._emit_event(
                    tool_call_event,
                    on_step=on_step,
                    verbose=verbose,
                )
                yield tool_call_event

                if tool is None:
                    output = serialize_output(self._unknown_tool_payload(call.name))
                else:
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
