"""
There are 2 kinds of model in OpenAI, namely text generative and conversational.
"""

import json
import warnings
from abc import ABC
from typing import Any, Dict, List, Optional

import requests

from promptulate.config import pne_config
from promptulate.error import OpenAIError
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
from promptulate.utils.logger import logger


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
    max_tokens: Optional[int] = None
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
    """Retry if API failed to get response. You can enable retry when you have a rate
    limited API."""
    retry_times: int = 5
    """If llm(like OpenAI) unable to obtain data, retry request until the data is
    obtained. You should enable retry if you want to use retry times."""
    retry_counter: int = 0
    """Used in conjunction with retry_times. Refresh when get data successfully."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.retry_times = pne_config.get_key_retry_times(self.model)

    @property
    def api_key(self):
        """Select api key to use. private_api_key, openai_api_key, key_pool key is
        optional."""
        if self.enable_private_api_key and self.private_api_key != "":
            return self.private_api_key
        return pne_config.get_openai_api_key(self.model)

    def set_private_api_key(self, value: str):
        self.enable_private_api_key = True
        self.private_api_key = value


class OpenAI(BaseOpenAI):
    """https://platform.openai.com/docs/api-reference/chat/create"""

    llm_type: LLMType = LLMType.OpenAI
    """Used to MessageSet data convert"""
    model: str = "text-davinci-003"
    """Model name to use."""
    max_tokens: Optional[int] = None
    """The maximum number of tokens to generate in the completion.
    -1 returns as many tokens as possible given the prompt and
    the models maximal context size."""

    def __call__(
        self, instruction: str, stop: Optional[List[str]] = None, *args, **kwargs
    ) -> str:
        # Loading OpenAI API parameters
        for key in self.api_param_keys:
            if key in kwargs:
                setattr(self, key, kwargs[key])

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
        return self.predict(message_set, stop).content

    def _predict(
        self, messages: MessageSet, stop: Optional[List[str]] = None, *args, **kwargs
    ) -> Optional[AssistantMessage]:
        """Run openai llm with custom message context."""
        if self.model == "text-davinci-003":
            warnings.warn(
                "This model(text-davinci-003) version is deprecated. Migrate before January 4, 2024 to "  # noqa
                "avoid disruption of service. gpt-3.5-turbo is recommended.",
                DeprecationWarning,
            )

        for key in self.api_param_keys:
            if key in kwargs:
                setattr(self, key, kwargs[key])

        api_key = self.api_key
        logger.debug(f"[pne openai key] sk-....{api_key[-6:]}")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        body: Dict[str, Any] = self._build_api_params_dict(messages, stop)

        logger.debug(f"[pne openai request] {json.dumps(body, indent=2)}")
        logger.debug(
            f"[pne openai request] url: {pne_config.openai_completion_request_url} proxies: {pne_config.proxies}"  # noqa: E501
        )
        response = requests.post(
            url=pne_config.openai_completion_request_url,
            headers=headers,
            json=body,
            proxies=pne_config.proxies,
        )
        if response.status_code == 200:
            # todo enable stream mode
            # for chunk in response.iter_content(chunk_size=None):
            #     logger.debug(chunk)
            self.retry_counter = 0
            ret_data = response.json()
            logger.debug(f"[pne openai response] {json.dumps(ret_data, indent=2)}")
            content = ret_data["choices"][0]["text"]
            return AssistantMessage(content=content, additional_kwargs=ret_data)

        logger.error(
            f"[pne OpenAI] <key sk-....{api_key[-6:]}>Failed to get data. Please check your network or api key."  # noqa: E501
        )
        logger.debug("[promptulate OpenAI] retry to get response")
        if self.enable_retry and self.retry_counter < self.retry_times:
            self.retry_counter += 1
            return self._predict(messages, stop)

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
    seed: Optional[int] = None
    """This feature is in Beta. If specified, our system will make a best effort to
    sample deterministically, such that repeated requests with the same seed and
    parameters should return the same result. Determinism is not guaranteed, and you
    should refer to the system_fingerprint response parameter to monitor changes in
    the backend."""
    response_format: Optional[dict] = None
    """An object specifying the format that the model must output. Compatible with
    gpt-4-1106-preview and gpt-3.5-turbo-1106. Setting to { "type": "json_object" }
    enables JSON mode, which guarantees the message the model generates is valid JSON.

    Important: when using JSON mode, you must also instruct the model to produce JSON
    yourself via a system or user message. Without this, the model may generate an
    unending stream of whitespace until the generation reaches the token limit,
    resulting in a long-running and seemingly "stuck" request. Also note that the
    message content may be partially cut off if finish_reason="length", which indicates
    the generation exceeded max_tokens or the conversation exceeded the max context
    length.

    type must be text or json_object.
    """
    tools: Optional[List[Dict[str, str]]] = None
    """A list of tools the model may call. Currently, only functions are supported as a
    tool. Use this to provide a list of functions the model may generate JSON inputs
    for."""
    function_call: Optional[int] = None
    """Controls which (if any) function is called by the model. none means the model
    will not call a function and instead generates a message. auto means the model can
    pick between generating a message or calling a function. Specifying a particular
    function via {"name": "my_function"} forces the model to call that function.

    none is the default when no functions are present. auto is the default if functions
    are present."""
    functions: Optional[List[Dict[str, str]]] = None
    """A list of functions the model may generate JSON inputs for."""
    base_url: str = None
    """set your base_url"""
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
        "seed",
        "response_format",
        "tools",
        "function_call",
        "function",
    ]
    """The key of openai api parameters."""

    def __call__(
        self, instruction: str, stop: Optional[List[str]] = None, *args, **kwargs
    ) -> str:
        for key in self.api_param_keys:
            if key in kwargs:
                setattr(self, key, kwargs[key])

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
        return self.predict(message_set, stop).content

    def _predict(
        self, prompts: MessageSet, stop: Optional[List[str]] = None, *args, **kwargs
    ) -> Optional[AssistantMessage]:
        for key in self.api_param_keys:
            if key in kwargs:
                setattr(self, key, kwargs[key])

        api_key = self.api_key
        logger.debug(f"[pne openai key] sk-....{api_key[-6:]}")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        body: Dict[str, Any] = self._build_api_params_dict(prompts, stop)

        logger.debug(f"[pne openai request] {json.dumps(body, indent=2)}")
        url = self.base_url or pne_config.openai_chat_api_url
        logger.debug(f"[pne openai request] url: {url} proxies: {pne_config.proxies}")
        response = requests.post(
            url=url,
            headers=headers,
            json=body,
            proxies=pne_config.proxies,
        )
        if response.status_code == 200:
            # todo enable stream mode
            # for chunk in response.iter_content(chunk_size=None):
            #     logger.debug(chunk)
            self.retry_counter = 0
            ret_data = response.json()
            logger.debug(f"[pne openai response] {json.dumps(ret_data, indent=2)}")
            content = ret_data["choices"][0]["message"]["content"]

            response.close()

            return AssistantMessage(content=content, additional_kwargs=ret_data)

        logger.error(
            f"[pne OpenAI] <key sk-....{api_key[-6:]}>Failed to get data. Please check your network or api key."  # noqa: E501
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
