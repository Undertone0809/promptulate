from abc import ABC, abstractmethod
from typing import Any, Callable, List, Optional

from promptulate.hook import Hook, HookTable
from promptulate.llms import BaseLLM
from promptulate.output_formatter import OutputFormatter
from promptulate.pydantic_v1 import BaseModel


class BaseAgent(ABC):
    """Base class of Agent."""

    def __init__(self, hooks: Optional[List[Callable]] = None, *args, **kwargs):
        hooks = hooks or []
        for hook in hooks:
            Hook.mount_instance_hook(hook, self)

        self._agent_type: str = kwargs.get("agent_type", "Agent")
        self._from = kwargs.get("_from", None)

        Hook.call_hook(HookTable.ON_AGENT_CREATE, self, *args, **kwargs)

    def run(
        self,
        instruction: str,
        output_schema: Optional[type(BaseModel)] = None,
        examples: Optional[List[BaseModel]] = None,
        *args,
        **kwargs,
    ) -> Any:
        """run the tool including specified function and hooks"""
        Hook.call_hook(
            HookTable.ON_AGENT_START,
            self,
            instruction,
            output_schema,
            *args,
            agent_type=self._agent_type,
            **kwargs,
        )

        # get original response from LLM
        result: str = self._run(instruction, *args, **kwargs)

        # Return Pydantic instance if output_schema is specified
        if output_schema:
            formatter = OutputFormatter(output_schema, examples)
            prompt = (
                f"{formatter.get_formatted_instructions()}\n##User input:\n{result}"
            )
            json_response = self.get_llm()(prompt)
            return formatter.formatting_result(json_response)

        Hook.call_hook(
            HookTable.ON_AGENT_RESULT,
            mounted_obj=self,
            result=result,
            agent_type=self._agent_type,
            _from=self._from,
        )
        return result

    @abstractmethod
    def _run(self, instruction: str, *args, **kwargs) -> str:
        """Run the detail agent, implemented by subclass."""
        raise NotImplementedError()

    @abstractmethod
    def get_llm(self) -> BaseLLM:
        """Get the llm when necessary."""
        raise NotImplementedError()
