import json
import time
from abc import ABC
from json import JSONDecodeError
from typing import Any, Dict, Iterator, List, Optional, TypeVar, Union

import jwt
import requests
from pydantic import BaseModel

from promptulate.config import pne_config
from promptulate.error import NetWorkError
from promptulate.llms import BaseLLM
from promptulate.preset_roles.prompt import PRESET_SYSTEM_PROMPT
from promptulate.schema import (
    AssistantMessage,
    BaseMessage,
    LLMType,
    MessageSet,
    StreamIterator,
    SystemMessage,
    UserMessage,
)
from promptulate.utils import logger

T = TypeVar("T", bound=BaseModel)


def parse_content(chunk) -> (str, str):
    try:
        ret_data = json.loads(chunk.replace("data: ", ""))
    except JSONDecodeError:
        return None, None
    content: Optional[str] = ret_data["choices"][0]["delta"]["content"]
    return content, ret_data


class ZhiPu(BaseLLM, ABC):
    llm_type: LLMType = LLMType.ZhiPu
    """Used to MessageSet data convert"""
    model: str = "glm-4"
    """Model name to use."""
    enable_private_api_key: bool = False
    """Enable to provide a separate api for openai llm """
    private_api_key: str = ""
    """Store private api key"""
    default_system_prompt: str = ""
    """ernie-bot system message"""
    enable_default_system_prompt: bool = True
    """enable use preset description"""
    exp_seconds: int = 3600
    """set your token expire time"""
    model_config = {}
    """model parameters"""

    @property
    def api_key(self):
        """Select api key to use. private_api_key, openai_api_key, key_pool key is
        optional."""
        if self.enable_private_api_key and self.private_api_key != "":
            return self.private_api_key
        return pne_config.get_zhipuai_api_key()

    def set_private_api_key(self, value: str):
        self.enable_private_api_key = True
        self.private_api_key = value

    def generate_token(self, api_key: str, exp_seconds: int):
        try:
            id, secret = api_key.split(".")
        except Exception as e:
            raise Exception("invalid apikey", e)

        payload = {
            "api_key": id,
            "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
            "timestamp": int(round(time.time() * 1000)),
        }

        return jwt.encode(
            payload,
            secret,
            algorithm="HS256",
            headers={"alg": "HS256", "sign_type": "SIGN"},
        )

    def __call__(
        self, instruction: str, *args, **kwargs
    ) -> Union[str, BaseMessage, T, List[BaseMessage], StreamIterator]:
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

        result = self.predict(message_set, **self.model_config)
        if isinstance(result, AssistantMessage):
            return result.content
        else:
            return result

    def _predict(
        self,
        prompts: MessageSet,
        stream: bool = False,
        return_raw_response: bool = False,
        *args,
        **kwargs,
    ) -> Union[str, BaseMessage, T, List[BaseMessage], StreamIterator]:
        """
        Predicts the response using the zhipuai platform.

        Args:
            prompts (MessageSet): The set of prompts to generate a response.
            stream (bool): The set to enable stream.
            return_raw_response (bool): return completion result if true
            **kwargs: zhipu_sdk kwargs

        Returns:
              Return string normally, it means enable_original_return is default False.
              Return BaseMessage if enable_original_return is True.
              Return List[BaseMessage] if stream is True.
              Return T if output_schema is provided.
              Return ZhiPuStreamIterator if stream is enable
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.generate_token(self.api_key, self.exp_seconds),
        }
        body: Dict[str, Any] = self._build_api_params_dict(prompts)
        logger.debug(f"[pne zhipu request] {json.dumps(body, indent=2)}")
        response = requests.post(
            url=pne_config.zhipu_model_url,
            headers=headers,
            stream=stream,
            json=body,
        )
        # return stream
        if stream:
            return StreamIterator(
                response_stream=response.iter_lines(decode_unicode=True),
                parse_content=parse_content,
                return_raw_response=return_raw_response,
            )
        else:
            if response.status_code == 200:
                ret_data = response.json()
                logger.debug(f"[pne zhipu response] {json.dumps(ret_data, indent=2)}")
                content = ret_data["choices"][0]["message"]["content"]
                return AssistantMessage(content=content, additional_kwargs=ret_data)
            else:
                raise NetWorkError(str(response.status_code))

    def _build_api_params_dict(self, prompts: MessageSet) -> Dict[str, Any]:
        dic = {
            "messages": prompts.to_llm_prompt(self.llm_type),
        }
        dic.update({"model": self.model})
        for key in self.model_config:
            if key is not None:
                dic.update({key: self.model_config[key]})
        return dic
