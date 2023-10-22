"""
There are 2 kinds of model in OpenAI, namely text generative and conversational.
"""

import json
import logging
import warnings
from abc import ABC
from typing import Optional, Any, Dict, List

import requests

from promptulate.config import Config
from promptulate.llms.base import BaseLLM
from promptulate.preset_roles.prompt import PRESET_SYSTEM_PROMPT
from promptulate.schema import (
    LLMType,
    MessageSet,
    UserMessage,
    SystemMessage,
    AssistantMessage,
    CompletionMessage,
)
from promptulate.tips import OpenAIError

CFG = Config()
logger = logging.getLogger(__name__)


class BaseOpenAI(BaseLLM, ABC):
    """https://platform.openai.com/docs/api-reference/chat/create"""

    llm_type: LLMType
    """Used to MessageSet data convert"""
    model: str
    """Model name to use."""
    temperature: float = 1.0
    """What sampling temperature to use."""
    top_p: float = 1
    """Total probability mass of tokens to consider at each step."""
    stream: bool = False
    """Whether to stream the results or not."""
    frequency_penalty: float = 0
    """Penalizes repeated tokens according to frequency."""
    presence_penalty: float = 0
    """Penalizes repeated tokens."""
    n: int = 1
    """How many completions to generate for each prompt."""
    max_tokens: int = 3000
    """The maximum number of tokens to generate in the completion.
    -1 returns as many tokens as possible given the prompt and
    the models maximal context size."""
    api_param_keys: List[str] = [
        "model",
        "temperature",
        "top_p",
        "stream",
        "stop",
        "frequency_penalty",
        "presence_penalty",
        "n",
        "max_tokens",
    ]
    """The key of openai api parameters"""
    default_system_prompt: str = ""
    """OpenAI system message"""
    enable_default_system_prompt: bool = True
    """enable use preset description"""
    enable_private_api_key: bool = False
    """Enable to provide a separate api for openai llm """
    private_api_key: str = ""
    """Store private api key"""
    enable_retry: bool = True
    """Retry if API failed to get response. You can enable retry when you have a rate limited API."""
    retry_times: int = 5
    """If llm(like OpenAI) unable to obtain data, retry request until the data is obtained. You should
    enable retry if you want to use retry times."""
    retry_counter: int = 0
    """Used in conjunction with retry_times. Refresh when get data successfully."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.retry_times = CFG.get_key_retry_times(self.model)

    @property
    def api_key(self):
        """Select api key to use. private_api_key, openai_api_key, key_pool key is optional."""
        if self.enable_private_api_key and self.private_api_key != "":
            return self.private_api_key
        return CFG.get_openai_api_key(self.model)

    def set_private_api_key(self, value: str):
        self.enable_private_api_key = True
        self.private_api_key = value


class OpenAI(BaseOpenAI):
    """https://platform.openai.com/docs/api-reference/chat/create"""

    llm_type: LLMType = LLMType.OpenAI
    """Used to MessageSet data convert"""
    model: str = "text-davinci-003"
    """Model name to use."""
    max_tokens: int = 800
    """The maximum number of tokens to generate in the completion.
    -1 returns as many tokens as possible given the prompt and
    the models maximal context size."""

    def __call__(
        self, prompt: str, stop: Optional[List[str]] = None, *args, **kwargs
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
                CompletionMessage(content=prompt),
            ]
        )
        return self.predict(message_set, stop).content

    def _predict(
        self, prompts: MessageSet, stop: Optional[List[str]] = None, *args, **kwargs
    ) -> Optional[AssistantMessage]:
        """Run openai llm with custom message context."""
        if self.model == "text-davinci-003":
            warnings.warn(
                "This model(text-davinci-003) version is deprecated. Migrate before January 4, 2024 to "
                "avoid disruption of service. gpt-3.5-turbo is recommended.",
                DeprecationWarning,
            )
        api_key = self.api_key
        logger.debug(f"[pne openai key] sk-....{api_key[-6:]}")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        body: Dict[str, Any] = self._build_api_params_dict(prompts, stop)

        logger.debug(f"[pne openai params] body {json.dumps(body)}")
        logger.debug(
            f"[pne openai request] url: {CFG.openai_completion_request_url} proxies: {CFG.proxies}"
        )
        response = requests.post(
            url=CFG.openai_completion_request_url,
            headers=headers,
            json=body,
            proxies=CFG.proxies,
        )
        if response.status_code == 200:
            # todo enable stream mode
            # for chunk in response.iter_content(chunk_size=None):
            #     logger.debug(chunk)
            self.retry_counter = 0
            ret_data = response.json()
            logger.debug(f"[pne openai response] {json.dumps(ret_data)}")
            content = ret_data["choices"][0]["text"]
            logger.debug(f"[pne openai answer] {content}")
            return AssistantMessage(content=content)

        logger.error(
            f"[pne OpenAI] <key sk-....{api_key[-6:]}>Failed to get data. Please check your network or api key."
        )
        logger.debug("[promptulate OpenAI] retry to get response")
        if self.enable_retry and self.retry_counter < self.retry_times:
            self.retry_counter += 1
            return self._predict(prompts, stop)

        logger.error(f"[pne OpenAI] Has retry {self.retry_times}, but all failed.")
        raise OpenAIError(json.dumps(response.content))

    def _build_api_params_dict(
        self, prompts: MessageSet, stop: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Build api parameters to put it inside the body."""
        dic = {"prompt": prompts.string_messages}

        if stop:
            dic.update({"stop": stop})

        for key in self.api_param_keys:
            if key in self.__dict__:
                dic.update({key: self.__dict__[key]})
        return dic


class ChatOpenAI(BaseOpenAI):
    """https://platform.openai.com/docs/api-reference/chat/create"""

    llm_type: LLMType = LLMType.ChatOpenAI
    """Used to MessageSet data convert"""
    model: str = "gpt-3.5-turbo"
    """Model name to use."""
    functions: Optional[List[Dict[str, str]]] = None
    """A list of functions the model may generate JSON inputs for."""
    api_param_keys: List[str] = [
        "model",
        "temperature",
        "top_p",
        "stream",
        "stop",
        "frequency_penalty",
        "presence_penalty",
        "n",
        "max_tokens",
    ]
    """The key of openai api parameters"""

    def __call__(
        self, prompt: str, stop: Optional[List[str]] = None, *args, **kwargs
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
                UserMessage(content=prompt),
            ]
        )
        return self.predict(message_set, stop).content

    def _predict(
        self, prompts: MessageSet, stop: Optional[List[str]] = None, *args, **kwargs
    ) -> Optional[AssistantMessage]:
        api_key = self.api_key
        logger.debug(f"[pne openai key] sk-....{api_key[-6:]}")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        body: Dict[str, Any] = self._build_api_params_dict(prompts, stop)

        logger.debug(f"[pne openai params] body {json.dumps(body)}")
        logger.debug(
            f"[pne openai request] url: {CFG.openai_chat_request_url} proxies: {CFG.proxies}"
        )
        response = requests.post(
            url=CFG.openai_chat_request_url,
            headers=headers,
            json=body,
            proxies=CFG.proxies,
        )
        if response.status_code == 200:
            # todo enable stream mode
            # for chunk in response.iter_content(chunk_size=None):
            #     logger.debug(chunk)
            self.retry_counter = 0
            ret_data = response.json()
            logger.debug(f"[pne openai response] {json.dumps(ret_data)}")
            content = ret_data["choices"][0]["message"]["content"]
            logger.debug(f"[pne openai answer] {content}")
            return AssistantMessage(content=content)

        logger.error(
            f"[pne OpenAI] <key sk-....{api_key[-6:]}>Failed to get data. Please check your network or api key."
        )
        logger.debug("[promptulate OpenAI] retry to get response")
        if self.enable_retry and self.retry_counter < self.retry_times:
            self.retry_counter += 1
            return self._predict(prompts, stop)

        logger.error(f"[pne OpenAI] Has retry {self.retry_times}, but all failed.")
        raise OpenAIError(json.dumps(json.loads(response.content)))

    def _build_api_params_dict(
        self, prompts: MessageSet, stop: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        dic = {
            "messages": prompts.to_llm_prompt(self.llm_type),
        }

        if stop:
            dic.update({"stop": stop})

        for key in self.api_param_keys:
            if key in self.__dict__ and self.__dict__[key] is not None:
                dic.update({key: self.__dict__[key]})
        return dic
