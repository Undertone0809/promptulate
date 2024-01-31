import os
from abc import ABC
from typing import Iterator, List, Optional, TypeVar, Union

from pydantic import BaseModel

from promptulate.config import pne_config
from promptulate.error import NetWorkError
from promptulate.llms import BaseLLM
from promptulate.preset_roles.prompt import PRESET_SYSTEM_PROMPT_ERNIE
from promptulate.schema import (
    AssistantMessage,
    BaseMessage,
    LLMType,
    MessageSet,
    StreamIterator,
    UserMessage,
)
from promptulate.utils import logger

T = TypeVar("T", bound=BaseModel)


def parse_content(chunk) -> (str, str):
    content = chunk["result"]
    ret_data = chunk["body"]
    return content, ret_data


class QianFan(BaseLLM, ABC):
    llm_type: LLMType = LLMType.QianFan
    """Used to MessageSet data convert"""
    model: str = "ERNIE-Bot-4"
    """Model name to use."""
    default_system_prompt: str = ""
    """ernie-bot system message"""
    enable_default_system_prompt: bool = True
    """enable use preset description"""
    model_config: dict = {}
    """model parameters"""

    def __call__(
        self, instruction: str, *args, **kwargs
    ) -> Union[str, BaseMessage, T, List[BaseMessage], StreamIterator]:
        preset = (
            self.default_system_prompt
            if self.default_system_prompt != ""
            else PRESET_SYSTEM_PROMPT_ERNIE
        )
        if not self.enable_default_system_prompt:
            preset = ""
        system = preset
        message_set = MessageSet(
            messages=[
                UserMessage(content=instruction),
            ]
        )
        result = self.predict(message_set, system, **self.model_config)
        if isinstance(result, AssistantMessage):
            return result.content
        else:
            return result

    def _predict(
        self,
        prompts: MessageSet,
        system: str = "",
        return_raw_response: bool = False,
        *args,
        **kwargs,
    ) -> Union[str, BaseMessage, T, List[BaseMessage], StreamIterator]:
        """
        Predicts the response using the qinfan platform.

        Args:
            prompts (MessageSet): The set of prompts to generate a response.
            system (str): The set of system to generate a response.
            return_raw_response (bool): return completion result if true
            **kwargs: qianfan_sdk kwargs

        Returns:
              Return string normally, it means enable_original_return is default False.
              Return BaseMessage if enable_original_return is True.
              Return List[BaseMessage] if stream is True.
              Return T if output_schema is provided.
              Return QianFanStreamIterator if stream enable
        """
        try:
            import qianfan  # noqa
        except ImportError:
            raise ImportError(
                "Could not import qianfan python package. "
                "This is needed in order to for QianFan. "
                "Please install it with `pip install qianfan`."
            )
        os.environ["QIANFAN_ACCESS_KEY"] = pne_config.get_qianfan_ak()
        os.environ["QIANFAN_SECRET_KEY"] = pne_config.get_qianfan_sk()
        chat_comp = qianfan.ChatCompletion()
        response = chat_comp.do(
            model=self.model,
            system=system,
            messages=prompts.listdict_messages,
            **kwargs,
        )
        # return stream
        if kwargs.get("stream", None):
            return StreamIterator(
                response_stream=response,
                parse_content=parse_content,
                return_raw_response=return_raw_response,
            )
        else:
            if response.code == 200:
                ret_data = response.body
                logger.debug(f"[pne ernie response] {ret_data}")
                content: str = ret_data["result"]
                logger.debug(f"[pne ernie answer] {content}")
                return AssistantMessage(content=content, additional_kwargs=ret_data)
            else:
                raise NetWorkError(str(response.code))
