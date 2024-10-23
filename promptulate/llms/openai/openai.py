"""
OpenAI API wrapper using the official OpenAI SDK.
"""

import os
import warnings
from abc import ABC
from typing import Dict, List, Optional

from openai import OpenAI as OpenAIClient
from pydantic import Field

from promptulate.llms.base import BaseLLM
from promptulate.preset_roles.prompt import PRESET_SYSTEM_PROMPT
from promptulate.schema import (
    AssistantMessage,
    CompletionMessage,
    LLMType,
    MessageSet,
    SystemMessage,
    UserMessage,
)


class BaseOpenAI(BaseLLM, ABC):
    """Base class for OpenAI models."""

    llm_type: LLMType
    model: str
    temperature: float = 1.0
    top_p: float = 1
    stream: bool = False
    frequency_penalty: float = 0
    presence_penalty: float = 0
    n: int = 1
    max_tokens: Optional[int] = None
    default_system_prompt: str = ""
    enable_default_system_prompt: bool = True
    api_key: str = Field(default_factory=lambda: os.environ.get("OPENAI_API_KEY"))

    client: OpenAIClient = Field(
        default_factory=lambda self: OpenAIClient(api_key=self.api_key)
    )


class OpenAI(BaseOpenAI):
    """Wrapper for OpenAI's completion models."""

    llm_type: LLMType = LLMType.OpenAI
    model: str = "text-davinci-003"

    def __call__(
        self, instruction: str, stop: Optional[List[str]] = None, **kwargs
    ) -> str:
        preset = (
            self.default_system_prompt
            if self.default_system_prompt != ""
            else PRESET_SYSTEM_PROMPT
        )
        if not self.enable_default_system_prompt:
            preset = ""
        message_set = MessageSet(
            messages=[
                CompletionMessage(content=preset),
                CompletionMessage(content=instruction),
            ]
        )
        return self.predict(message_set, stop, **kwargs).content

    def _predict(
        self, messages: MessageSet, stop: Optional[List[str]] = None, **kwargs
    ) -> Optional[AssistantMessage]:
        if self.model == "text-davinci-003":
            warnings.warn(
                "This model(text-davinci-003) version is deprecated. Migrate before January 4, 2024 to "  # noqa
                "avoid disruption of service. gpt-3.5-turbo is recommended.",
                DeprecationWarning,
            )

        params = {
            "model": self.model,
            "prompt": messages.string_messages,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "n": self.n,
            "stream": self.stream,
            "stop": stop,
            "max_tokens": self.max_tokens,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            **kwargs,
        }

        response = self.client.completions.create(**params)

        content = response.choices[0].text
        return AssistantMessage(
            content=content, additional_kwargs=response.model_dump()
        )


class ChatOpenAI(BaseOpenAI):
    """Wrapper for OpenAI's chat models."""

    llm_type: LLMType = LLMType.ChatOpenAI
    model: str = "gpt-3.5-turbo"
    seed: Optional[int] = None
    response_format: Optional[dict] = None
    tools: Optional[List[Dict[str, str]]] = None
    function_call: Optional[int] = None
    functions: Optional[List[Dict[str, str]]] = None

    def __call__(
        self, instruction: str, stop: Optional[List[str]] = None, **kwargs
    ) -> str:
        system_message = (
            self.default_system_prompt
            if self.default_system_prompt != ""
            else PRESET_SYSTEM_PROMPT
        )
        if not self.enable_default_system_prompt:
            system_message = ""

        message_set = MessageSet(
            messages=[
                SystemMessage(content=system_message),
                UserMessage(content=instruction),
            ]
        )
        return self.predict(message_set, stop, **kwargs).content

    def _predict(
        self, prompts: MessageSet, stop: Optional[List[str]] = None, **kwargs
    ) -> Optional[AssistantMessage]:
        warnings.warn(
            "ChatOpenAI is deprecated in v1.16.0. Please use pne.LLMFactory instead. \n"
            "See the detail in https://undertone0809.github.io/promptulate/#/modules/llm/llm?id=llm",
            DeprecationWarning,
        )

        params = {
            "model": self.model,
            "messages": prompts.listdict_messages,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "n": self.n,
            "stream": self.stream,
            "stop": stop,
            "max_tokens": self.max_tokens,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "seed": self.seed,
            "response_format": self.response_format,
            "tools": self.tools,
            "function_call": self.function_call,
            "functions": self.functions,
            **kwargs,
        }

        response = self.client.chat.completions.create(**params)

        content = response.choices[0].message.content
        return AssistantMessage(
            content=content, additional_kwargs=response.model_dump()
        )
