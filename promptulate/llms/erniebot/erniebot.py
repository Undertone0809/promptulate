import json
import logging
from abc import ABC
from typing import List, Optional, Dict, Any

import requests

from promptulate.config import Config
from promptulate.hook import Hook, HookTable
from promptulate.llms import BaseLLM
from promptulate.schema import (
    LLMType,
    MessageSet,
    UserMessage,
    AssistantMessage,
    BaseMessage,
)
from promptulate.utils import get_logger

CFG = Config()
logger = get_logger()


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": CFG.get_ernie_api_key(),
        "client_secret": CFG.get_ernie_api_secret(),
    }
    return str(requests.post(url, params=params).json().get("access_token"))


class ErnieBot(BaseLLM, ABC):
    llm_type: LLMType = LLMType.ErnieBot
    """Used to MessageSet data convert"""
    model: str = "ernie-bot-turbo"
    """Model name to use."""
    temperature: float = 1.0
    """What sampling temperature to use."""
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
        response = requests.request(
            "POST",
            self.url + "?access_token=" + get_access_token(),
            headers=headers,
            json=body,
        )
        logger.debug(f"[pne ernie body] {body}")
        if response.status_code == 200:
            # todo enable stream mode
            # for chunk in response.iter_content(chunk_size=None):
            #     logger.debug(chunk)
            ret_data = response.json()
            logger.debug(f"[pne ernie response] {json.dumps(ret_data)}")
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
        return dic
