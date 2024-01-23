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
from promptulate.preset_roles.prompt import PRESET_SYSTEM_PROMPT_ZhiPU
from promptulate.schema import (
    AssistantMessage,
    BaseMessage,
    LLMType,
    MessageSet,
    SystemMessage,
    UserMessage,
)
from promptulate.utils import logger

T = TypeVar("T", bound=BaseModel)


class ZhiPuStreamIterator:
    """
    This class is an iterator for the response stream from the LLM model.

    Attributes:
        response_stream: The stream of responses from the LLM model.
        return_raw_response: A boolean indicating whether to return the raw response
        or not.
    """

    def __init__(self, response_stream, return_raw_response: bool = False):
        """
        The constructor for LitellmStreamIterator class.

        Parameters:
            response_stream: The stream of responses from the LLM model.
            return_raw_response (bool): A flag indicating whether to return the raw
            response or not.
        """
        self.response_stream = response_stream
        self.return_raw_response = return_raw_response

    def __iter__(self) -> Union[Iterator[BaseMessage], Iterator[str]]:
        """
        The iterator method for the LitellmStreamIterator class.

        Returns:
            self: An instance of the LitellmStreamIterator class.
        """
        return self

    def parse_chunk(self, chunk) -> Optional[Union[str, BaseMessage]]:
        """
        This method is used to parse a chunk from the response stream. It returns
        None if the chunk is empty, otherwise it returns the parsed chunk.

        Parameters:
            chunk: The chunk to be parsed.

        Returns:
            Optional: The parsed chunk or None if the chunk is empty.
        """
        try:
            ret_data = json.loads(chunk.replace("data: ", ""))
        except JSONDecodeError:
            return None
        content: Optional[str] = ret_data["choices"][0]["delta"]["content"]
        if content is None:
            return None

        if self.return_raw_response:
            additional_kwargs: dict = ret_data
            message = AssistantMessage(
                content=content,
                additional_kwargs=additional_kwargs,
            )
            return message

        return content

    def __next__(self) -> Union[str, BaseMessage]:
        """
        The next method for the LitellmStreamIterator class.

        This method is used to get the next response from the LLM model. It iterates
        over the response stream and parses each chunk using the parse_chunk method.
        If the parsed chunk is not None, it returns the parsed chunk as the next
        response. If there are no more messages in the response stream, it raises a
        StopIteration exception.

        Returns:
            Union[str, BaseMessage]: The next response from the LLM model. If
            return_raw_response is True, it returns an AssistantMessage instance,
            otherwise it returns the content of the response as a string.
        """
        for chunk in self.response_stream:
            message = self.parse_chunk(chunk)
            if message is not None:
                return message

        # If there are no more messages, stop the iteration
        raise StopIteration


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
    ) -> Union[str, BaseMessage, T, List[BaseMessage], ZhiPuStreamIterator]:
        system_message = (
            self.default_system_prompt
            if self.default_system_prompt != ""
            else PRESET_SYSTEM_PROMPT_ZhiPU
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
    ) -> Union[str, BaseMessage, T, List[BaseMessage], ZhiPuStreamIterator]:
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
            return ZhiPuStreamIterator(
                response_stream=response.iter_lines(decode_unicode=True),
                return_raw_response=return_raw_response,
            )
        else:
            if response.status_code == 200:
                # todo enable stream mode
                # for chunk in response.iter_content(chunk_size=None):
                #     logger.debug(chunk)
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
