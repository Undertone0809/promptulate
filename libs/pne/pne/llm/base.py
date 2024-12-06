"""
TODO:

- [ ] support run_with_structured stream mode
- [ ] support tool call

model.bind_tools()
model.run("", response_format="")
"""

import json
from abc import ABC, abstractmethod
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    TypedDict,
    TypeVar,
    Union,
    overload,
    Type,
)

import litellm
from pydantic import BaseModel

from pne.callbacks.base import CallbackHandler
from pne.callbacks.manager import CallbackManager
from pne.message import AssistantMessage, BaseMessage, MessageSet, StreamMessageIterator
from pne.output_formatter import get_formatted_instructions, formatting_result
from pne.tools.base import ToolTypes
from pne.tools.manager import ToolManager
from pne.utils.logger import logger

T = TypeVar("T", bound=BaseModel)


class LLM(ABC):
    def __init__(
        self,
        callbacks: Optional[List[CallbackHandler]] = None,
        tools: Optional[List[ToolTypes]] = None,
        **kwargs,
    ):
        """Initialize LLM with optional callbacks."""
        self.callback_manager = CallbackManager(callbacks=callbacks)
        self.tool_manager = ToolManager(tools=tools if tools else [])

    @property
    def enable_tool(self) -> bool:
        """Check if tools are enabled."""
        return bool(self.tool_manager.tools)

    def run(
        self,
        messages: Union[List[Dict], MessageSet, List[BaseMessage]],
        tools: Optional[List[ToolTypes]] = None,
    ) -> AssistantMessage:
        """Run the LLM with the given messages.

        Args:
            messages: Input messages in various formats (List[Dict], MessageSet, or List[BaseMessage])
            tools: Optional list of tools to use
            stream: Whether to stream the response

        Returns:
            AssistantMessage: The response from the LLM

        Raises:
            ValueError: If messages is in an invalid format
        """
        messages_set: MessageSet = self._convert_to_message_set(messages)
        return self.generate(messages_set, tools)

    def run_stream(
        self,
        messages: Union[List[dict], MessageSet, List[BaseMessage]],
    ):
        """Run the LLM in streaming mode.

        Args:
            messages: Input messages in various formats (List[dict], MessageSet, or List[BaseMessage])

        Returns:
            Generator yielding response tokens from the LLM

        Raises:
            ValueError: If messages is in an invalid format
        """
        messages_set: MessageSet = self._convert_to_message_set(messages)
        return self.generate_stream(messages_set)

    def run_with_structured(
        self,
        messages: Union[List[dict], MessageSet, List[BaseMessage]],
        response_format: Type[T],
        examples: Optional[List[BaseModel]] = None,
    ) -> T:
        """Run the LLM with the given messages and response format."""
        if self.enable_tool:
            raise ValueError(
                "run_with_structured does not support tools, please use run instead"
            )

        message_set: MessageSet = self._convert_to_message_set(messages)

        instruction: str = get_formatted_instructions(
            json_schema=response_format, examples=examples
        )
        message_set.messages[-1].content += f"\n{instruction}"

        response: AssistantMessage = self.generate(message_set)
        return formatting_result(
            pydantic_obj=response_format, llm_output=str(response.content)
        )

    @abstractmethod
    def generate(
        self,
        messages: MessageSet,
        tools: Optional[List[ToolTypes]] = None,
    ) -> AssistantMessage:
        """Generate a response from the LLM in normal (non-streaming) mode.

        This method should be implemented by subclasses to handle the actual LLM call.
        """
        raise NotImplementedError

    @abstractmethod
    def generate_stream(
        self,
        messages: MessageSet,
    ) -> StreamMessageIterator:
        """Generate a streaming response from the LLM.

        This method should be implemented by subclasses to handle streaming responses.
        """
        raise NotImplementedError

    @abstractmethod
    def bind_tools(self, tools: List[ToolTypes]):
        """Bind tools to the LLM."""
        # TODO: Can this be implemented directly in the LLM class?
        raise NotImplementedError

    def _convert_to_message_set(
        self, messages: Union[List[Dict], MessageSet, List[BaseMessage]]
    ) -> MessageSet:
        """Convert input messages to MessageSet format.

        Args:
            messages: Input messages in various formats

        Returns:
            MessageSet: Converted messages

        Raises:
            ValueError: If messages is in an invalid format
        """
        if isinstance(messages, MessageSet):
            return messages

        try:
            if isinstance(messages[0], dict):
                return MessageSet.from_raw(messages)
            elif isinstance(messages[0], BaseMessage):
                return MessageSet(messages)
            else:
                raise ValueError(
                    f"[pne LLM] Unsupported message type: {type(messages[0])}"
                )
        except (IndexError, AttributeError) as e:
            raise ValueError(f"[pne LLM] Invalid message format: {e}")


class LLMFactory:
    @classmethod
    def build(
        cls, model_name: str, model_config: Optional[Dict[str, Any]] = None, **kwargs
    ) -> LLM: ...
