import json
import warnings
from abc import ABC
from typing import Any, Dict, List, Optional

import requests

from promptulate.config import pne_config
from promptulate.error import LLMError
from promptulate.llms import BaseLLM
from promptulate.preset_roles.prompt import PRESET_SYSTEM_PROMPT_ERNIE
from promptulate.schema import AssistantMessage, LLMType, MessageSet, UserMessage
from promptulate.utils.logger import logger


class ErnieBot(BaseLLM, ABC):
    llm_type: LLMType = LLMType.ErnieBot
    """Used to MessageSet data convert"""
    model: str = "ernie-bot-4"
    """Model name to use."""
    temperature: float = 0.7
    """What sampling temperature to use."""
    top_p: float = 0.8
    """variety of text"""
    stream: bool = False
    """Whether to stream the results or not."""
    disable_search: bool = True
    """disable baidu search"""
    default_system_prompt: str = ""
    """ernie-bot system message"""
    enable_default_system_prompt: bool = True
    """enable use preset description"""
    penalty_score: float = 1.0
    system: str = ""
    api_param_keys: List[str] = [
        "temperature",
        "top_p",
        "stream",
        "stop",
        "system",
        "disable_search",
        "penalty_score",
    ]
    base_url: str = ""
    """set your base_url"""

    def __call__(
        self, instruction: str, stop: Optional[List[str]] = None, *args, **kwargs
    ) -> str:
        preset = (
            self.default_system_prompt
            if self.default_system_prompt != ""
            else PRESET_SYSTEM_PROMPT_ERNIE
        )
        if not self.enable_default_system_prompt:
            preset = ""
        self.system = preset
        message_set = MessageSet(
            messages=[
                UserMessage(content=instruction),
            ]
        )
        return self.predict(message_set, stop).content

    def _predict(
        self, prompts: MessageSet, stop: Optional[List[str]] = None, *args, **kwargs
    ) -> AssistantMessage:
        """
        Predicts the response using the ERNIE model.

        Args:
            prompts (MessageSet): The set of prompts to generate a response.
            stop (Optional[List[str]], optional): List of stop words to stop the
            generation. Defaults to None.

        Returns:
            AssistantMessage: The generated response.
        """
        warnings.warn(
            "QianFan class is online ,this module will deprecated", DeprecationWarning
        )
        headers = {"Content-Type": "application/json"}
        models = {
            "ernie-bot-turbo": pne_config.ernie_bot_turbo_url,
            "ernie-bot-4": pne_config.ernie_bot_4_url,
            "ernie-bot": pne_config.ernie_bot_url,
        }

        if self.base_url:
            url = self.base_url
        else:
            if models.__contains__(self.model):
                url = models[self.model]
            else:
                raise ValueError("pne not found this model")

        body: Dict[str, Any] = self._build_api_params_dict(prompts, stop)
        response = requests.post(
            url=url + "?access_token=" + pne_config.get_ernie_token(),
            headers=headers,
            json=body,
            proxies=pne_config.proxies,
        )
        logger.debug(f"[pne ernie url] {url}")
        logger.debug(f"[pne ernie body] {body}")
        if response.status_code == 200:
            # todo enable stream mode
            # for chunk in response.iter_content(chunk_size=None):
            #     logger.debug(chunk)
            ret_data = response.json()
            logger.debug(f"[pne ernie response] {json.dumps(ret_data)}")

            if ret_data.get("error_code", None):
                raise LLMError(ret_data)

            content: str = ret_data["result"]
            """ernie-bot official support stop,deprecated"""
            """if stop:
                    length: int = 1000000  # very large integer +inf
                    temp: str = ""
                    for s in stop:
                        temp_len = len(content.split(s)[0])
                        if temp_len < length:
                            temp = content.split(s)[0]
                            length = temp_len
                    content = temp"""
            logger.debug(f"[pne ernie answer] {content}")
            return AssistantMessage(content=content, additional_kwargs=ret_data)

    def _build_api_params_dict(
        self,
        prompts: MessageSet,
        stop: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Build api parameters to put it inside the body."""
        # print(prompts.type_)
        dic = {
            "messages": prompts.to_llm_prompt(self.llm_type),
        }

        if stop:
            dic.update({"stop": stop})

        for key in self.api_param_keys:
            if key in self.__dict__:
                dic.update({key: self.__dict__[key]})
        return dic
