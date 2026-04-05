"""OpenAI Responses API agent with local shell skill support."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from typing import Any, Callable, Sequence

from .skills import LocalSkill, skill_context


def _item_type(item: Any) -> str | None:
    if isinstance(item, dict):
        value = item.get("type")
        return str(value) if value is not None else None
    value = getattr(item, "type", None)
    return str(value) if value is not None else None


def _item_get(item: Any, key: str, default: Any = None) -> Any:
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def _truncate_text(text: str, max_length: int) -> str:
    if max_length <= 0 or len(text) <= max_length:
        return text
    return text[: max_length - 1] + "…"


def _response_text(response: Any) -> str:
    text = getattr(response, "output_text", None)
    if isinstance(text, str) and text.strip():
        return text.strip()

    output = getattr(response, "output", None) or []
    parts: list[str] = []
    for item in output:
        if _item_type(item) == "message":
            for content in _item_get(item, "content", []) or []:
                if _item_type(content) == "output_text":
                    value = _item_get(content, "text")
                    if isinstance(value, str):
                        parts.append(value)
    return "".join(parts).strip()


@dataclass
class LocalShellExecutor:
    """Runs shell commands for OpenAI shell call outputs."""

    def run(self, command: str, *, timeout_ms: int, max_output_length: int) -> dict[str, Any]:
        timeout_seconds = max(timeout_ms, 1) / 1000
        try:
            completed = subprocess.run(
                command,
                shell=True,
                text=True,
                capture_output=True,
                timeout=timeout_seconds,
                check=False,
            )
            stdout = _truncate_text(completed.stdout or "", max_output_length)
            stderr = _truncate_text(completed.stderr or "", max_output_length)
            return {
                "stdout": stdout,
                "stderr": stderr,
                "outcome": {
                    "type": "exit",
                    "exit_code": completed.returncode,
                },
            }
        except subprocess.TimeoutExpired as exc:
            stdout = _truncate_text(exc.stdout or "", max_output_length)
            stderr = _truncate_text(exc.stderr or "", max_output_length)
            return {
                "stdout": stdout,
                "stderr": stderr,
                "outcome": {
                    "type": "timeout",
                },
            }


@dataclass
class OpenAIResponsesAgent:
    """OpenAI agent that uses the Responses API and local shell skills."""

    model: str = "gpt-5.4"
    client: Any | None = None
    instructions: str | None = None
    skills: Sequence[LocalSkill] = ()
    shell_timeout_ms: int = 60_000
    shell_max_output_length: int = 8_192
    shell_executor: LocalShellExecutor = field(default_factory=LocalShellExecutor)
    agent_type: str = "OpenAI"

    def __post_init__(self) -> None:
        if self.client is None:
            try:
                from openai import OpenAI
            except ImportError as exc:  # pragma: no cover - only when package missing
                raise RuntimeError(
                    "OpenAI agent requested but the `openai` package is not installed."
                ) from exc

            self.client = OpenAI()

        if self.instructions is None:
            self.instructions = (
                "You are an OpenAI agent. Use the shell tool when it helps. "
                "Think privately and answer succinctly."
            )

    def _instructions(self) -> str:
        context = skill_context(self.skills)
        if not context:
            return self.instructions or ""
        return f"{self.instructions}\n\n{context}"

    def _shell_tool(self) -> dict[str, Any]:
        return {"type": "shell", "environment": {"type": "local"}}

    def _execute_shell_call(self, item: Any) -> dict[str, Any]:
        action = _item_get(item, "action", {}) or {}
        commands = _item_get(action, "commands", []) or []
        timeout_ms = int(_item_get(action, "timeout_ms") or self.shell_timeout_ms)
        max_output_length = int(
            _item_get(action, "max_output_length") or self.shell_max_output_length
        )
        results = [
            self.shell_executor.run(
                command,
                timeout_ms=timeout_ms,
                max_output_length=max_output_length,
            )
            for command in commands
        ]
        return {
            "type": "shell_call_output",
            "call_id": _item_get(item, "call_id") or _item_get(item, "id"),
            "output": results,
            "max_output_length": max_output_length,
        }

    def run(
        self,
        prompt: str,
        *,
        max_steps: int = 8,
        verbose: bool = False,
        on_step: Callable[[dict[str, Any]], None] | None = None,
    ) -> str:
        response = self.client.responses.create(
            model=self.model,
            instructions=self._instructions(),
            input=prompt,
            tools=[self._shell_tool()],
        )

        def emit(event: dict[str, Any]) -> None:
            if on_step is not None:
                on_step(event)
            if verbose:
                print(json.dumps(event, ensure_ascii=False, indent=2))

        for step in range(1, max_steps + 1):
            emit(
                {
                    "type": "step_start",
                    "agent": self.agent_type,
                    "step": step,
                }
            )
            output_items = getattr(response, "output", None) or []
            shell_calls = [item for item in output_items if _item_type(item) == "shell_call"]
            if not shell_calls:
                final_text = _response_text(response)
                if final_text:
                    emit(
                        {
                            "type": "final",
                            "agent": self.agent_type,
                            "step": step,
                            "content": final_text,
                        }
                    )
                    return final_text
                raise RuntimeError("OpenAI agent returned no final text and no shell calls.")

            emit(
                {
                    "type": "shell_call_batch",
                    "agent": self.agent_type,
                    "step": step,
                    "count": len(shell_calls),
                }
            )
            input_items = [self._execute_shell_call(item) for item in shell_calls]
            emit(
                {
                    "type": "shell_results",
                    "agent": self.agent_type,
                    "step": step,
                    "results": input_items,
                }
            )
            response = self.client.responses.create(
                model=self.model,
                previous_response_id=getattr(response, "id", None),
                input=input_items,
                tools=[self._shell_tool()],
            )

        raise RuntimeError(f"Reached max_steps={max_steps} without producing a final answer.")


def build_openai_agent(
    *,
    skills: Sequence[LocalSkill] | None = None,
    model: str = "gpt-5.4",
    client: Any | None = None,
    instructions: str | None = None,
    shell_timeout_ms: int = 60_000,
    shell_max_output_length: int = 8_192,
) -> OpenAIResponsesAgent:
    return OpenAIResponsesAgent(
        model=model,
        client=client,
        instructions=instructions,
        skills=skills or (),
        shell_timeout_ms=shell_timeout_ms,
        shell_max_output_length=shell_max_output_length,
    )
