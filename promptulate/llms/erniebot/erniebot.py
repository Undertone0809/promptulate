import json
import logging
from abc import ABC
from typing import List, Optional, Dict, Any

import requests

from promptulate.config import Config
from promptulate.llms import BaseLLM
from promptulate.schema import (
    LLMType,
    MessageSet,
    UserMessage,
    AssistantMessage,
    BaseMessage,
)
from promptulate.tips import LLMError
from promptulate.utils import get_logger

CFG = Config()
logger = get_logger()


class ErnieBot(BaseLLM, ABC):
    llm_type: LLMType = LLMType.ErnieBot
    """Used to MessageSet data convert"""
    model: str = "ernie-bot-turbo"
    """Model name to use."""
    temperature: float = 0.7
    """What sampling temperature to use."""
    top_p: float = 0.8
    """variety of text"""
    stream: bool = False
    """Whether to stream the results or not."""
    penalty_score: float = 1.0
    api_param_keys: List[str] = [
        "temperature",
        "top_p",
        "stream",
        "penalty_score",
    ]
    url: str = CFG.ernie_bot_url

    def __call__(
        self, prompt: str, stop: Optional[List[str]] = None, *args, **kwargs
    ) -> str:
        message_set = MessageSet(
            messages=[
                UserMessage(content=prompt),
            ]
        )
        return self.predict(message_set, stop).content

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _predict(
        self, prompts: MessageSet, stop: Optional[List[str]] = None, *args, **kwargs
    ) -> BaseMessage:
        """llm generate prompt"""
        headers = {"Content-Type": "application/json"}
        if self.model == "ernie-bot-turbo":
            logging.debug("[pne use ernie-bot-turbo]")
        elif self.model == "ernie-bot":
            self.url = CFG.ernie_bot_url
            logging.debug("[pne use ernie-bot]")
        body: Dict[str, Any] = self._build_api_params_dict(prompts)
        response = requests.post(
            url=self.url + "?access_token=" + CFG.get_ernie_token(),
            headers=headers,
            json=body,
            proxies=CFG.proxies,
        )
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
            if stop:
                length: int = 1000000  # very large integer +inf
                temp: str = ""
                for s in stop:
                    temp_len = len(content.split(s)[0])
                    if temp_len < length:
                        temp = content.split(s)[0]
                        length = temp_len
                content = temp
            logger.debug(f"[pne ernie answer] {content}")
            return AssistantMessage(content=content)

    def _build_api_params_dict(self, prompts: MessageSet) -> Dict[str, Any]:
        """Build api parameters to put it inside the body."""
        dic = {
            "messages": prompts.to_llm_prompt(self.llm_type),
        }
        for key in self.api_param_keys:
            if key in self.__dict__:
                dic.update({key: self.__dict__[key]})
        return dic
