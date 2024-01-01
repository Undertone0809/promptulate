from abc import ABC, abstractmethod
from typing import Any, Callable, List, Optional

from pydantic import BaseModel

from promptulate.hook import Hook, HookTable
from promptulate.llms import BaseLLM
from promptulate.output_formatter import OutputFormatter


class BaseAgent(ABC):
    """Base class of Agent."""

    def __init__(self, hooks: List[Callable] = None, *args, **kwargs):
        if hooks:
            for hook in hooks:
                Hook.mount_instance_hook(hook, self)
        Hook.call_hook(HookTable.ON_AGENT_CREATE, self, *args, **kwargs)

    def run(
        self,
        prompt: str,
        output_schema: Optional[type(BaseModel)] = None,
        examples: Optional[List[BaseModel]] = None,
        *args,
        **kwargs,
    ) -> Any:
        """run the tool including specified function and hooks"""
        Hook.call_hook(
            HookTable.ON_AGENT_START, self, prompt, output_schema, *args, **kwargs
        )

        # get original response from LLM
        result: str = self._run(prompt, *args, **kwargs)

        # Return Pydantic instance if output_schema is specified
        if output_schema:
            formatter = OutputFormatter(output_schema, examples)
            prompt = (
                f"{formatter.get_formatted_instructions()}\n##User input:\n{result}"
            )
            json_response = self.get_llm()(prompt)
            return formatter.formatting_result(json_response)

        Hook.call_hook(HookTable.ON_AGENT_RESULT, self, result=result)
        return result

    @abstractmethod
    def _run(self, prompt: str, *args, **kwargs) -> str:
        """Run the detail agent, implemented by subclass."""
        raise NotImplementedError()

    @abstractmethod
    def get_llm(self) -> BaseLLM:
        """Get the llm when necessary."""
        raise NotImplementedError()
