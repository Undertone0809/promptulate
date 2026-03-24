from enum import Enum, auto
from typing import Dict, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel

from pne.llm.base import LLM, LLMFactory
from pne.message import AssistantMessage, BaseMessage, MessageSet, UserMessage
from pne.tools.base import ToolTypes

T = TypeVar("T", bound=BaseModel)
ChatInput = Union[str, MessageSet, List[Dict], List[BaseMessage]]


def _normalize_messages(messages: ChatInput) -> MessageSet:
    if isinstance(messages, str):
        return MessageSet(messages=[UserMessage(content=messages)])

    if isinstance(messages, MessageSet):
        return messages

    if not isinstance(messages, list) or not messages:
        raise ValueError(
            "messages must be a non-empty string, MessageSet, or message list."
        )

    first_message = messages[0]
    if isinstance(first_message, dict):
        return MessageSet.from_raw(messages)
    if isinstance(first_message, BaseMessage):
        return MessageSet(messages=messages)

    raise ValueError(f"Unsupported message type: {type(first_message)!r}")


class Mode(Enum):
    CHAT = auto()
    REACT = auto()
    PLANED_REACT = auto()
    PLANED_REACT_WITHOUT_REEDBACK = auto()
    TOOL = auto()


def _get_llm(
    *,
    model: Optional[str] = None,
    model_config: Optional[dict] = None,
    custom_llm: Optional[LLM] = None,
    callbacks: Optional[List] = None,
) -> LLM:
    if model and custom_llm:
        raise ValueError("model and custom_llm cannot be provided at the same time.")

    if model_config and custom_llm:
        raise ValueError(
            "model_config and custom_llm cannot be provided at the same time."
        )

    if custom_llm is not None:
        return custom_llm

    if model is None:
        raise ValueError("model or custom_llm must be provided.")

    return LLMFactory.build(
        model_name=model,
        model_config=model_config,
        callbacks=callbacks,
    )


def _raise_if_deferred(
    *,
    tools: Optional[List[ToolTypes]] = None,
    enable_plan: bool = False,
    enable_memory: bool = False,
    mode: Mode = Mode.CHAT,
    stream: bool = False,
) -> None:
    if tools:
        raise NotImplementedError("tools are deferred for Promptulate v2 P0.")
    if enable_plan:
        raise NotImplementedError("enable_plan is deferred for Promptulate v2 P0.")
    if enable_memory:
        raise NotImplementedError("enable_memory is deferred for Promptulate v2 P0.")
    if mode is not Mode.CHAT:
        raise NotImplementedError("Only Mode.CHAT is supported for Promptulate v2 P0.")
    if stream:
        raise NotImplementedError("stream is deferred for Promptulate v2 P0.")


class AIChat:
    def __init__(
        self,
        model: Optional[str] = None,
        model_config: Optional[dict] = None,
        tools: Optional[List[ToolTypes]] = None,
        custom_llm: Optional[LLM] = None,
        enable_plan: bool = False,
        enable_memory: bool = False,
        mode: Mode = Mode.CHAT,
        callbacks: Optional[List] = None,
    ):
        _raise_if_deferred(
            tools=tools,
            enable_plan=enable_plan,
            enable_memory=enable_memory,
            mode=mode,
        )
        self.llm = _get_llm(
            model=model,
            model_config=model_config,
            custom_llm=custom_llm,
            callbacks=callbacks,
        )

    def run(
        self,
        messages: ChatInput,
        *,
        output_schema: Optional[Type[T]] = None,
        examples: Optional[List[BaseModel]] = None,
        return_raw_response: bool = False,
        stream: bool = False,
    ) -> Union[str, AssistantMessage, T]:
        _raise_if_deferred(stream=stream)
        normalized_messages = _normalize_messages(messages)

        if output_schema is not None:
            return self.llm.run_with_structured(
                normalized_messages,
                response_format=output_schema,
                examples=examples,
            )

        response = self.llm.run(normalized_messages)
        return response if return_raw_response else str(response.content)

    def chat(self, messages: ChatInput, **kwargs) -> Union[str, AssistantMessage, T]:
        return self.run(messages, **kwargs)

    def bind_tools(self, tools: List[ToolTypes], *args, **kwargs):
        _raise_if_deferred(tools=tools)

    @classmethod
    def from_chat(cls, *args, **kwargs) -> "AIChat":
        return cls(*args, **kwargs)


def chat(
    messages: ChatInput,
    *,
    model: Optional[str] = None,
    model_config: Optional[dict] = None,
    tools: Optional[List[ToolTypes]] = None,
    output_schema: Optional[Type[T]] = None,
    examples: Optional[List[BaseModel]] = None,
    return_raw_response: bool = False,
    custom_llm: Optional[LLM] = None,
    enable_plan: bool = False,
    enable_memory: bool = False,
    mode: Mode = Mode.CHAT,
    callbacks: Optional[List] = None,
    stream: bool = False,
) -> Union[str, AssistantMessage, T]:
    ai = AIChat.from_chat(
        model=model,
        model_config=model_config,
        tools=tools,
        custom_llm=custom_llm,
        enable_plan=enable_plan,
        enable_memory=enable_memory,
        mode=mode,
        callbacks=callbacks,
    )
    return ai.run(
        messages,
        output_schema=output_schema,
        examples=examples,
        return_raw_response=return_raw_response,
        stream=stream,
    )
