import os
from abc import ABC
from typing import Iterator, List, Optional, TypeVar, Union

from pydantic import BaseModel

from promptulate.config import pne_config
from promptulate.llms import BaseLLM
from promptulate.preset_roles.prompt import PRESET_SYSTEM_PROMPT_ERNIE
from promptulate.schema import (
    AssistantMessage,
    BaseMessage,
    LLMType,
    MessageSet,
    UserMessage,
)
from promptulate.utils import logger

T = TypeVar("T", bound=BaseModel)


class QianFanStreamIterator:
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
        content: Optional[str] = chunk["result"]
        if content is None:
            return None

        if self.return_raw_response:
            additional_kwargs: dict = chunk["body"]
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
    ) -> Union[str, BaseMessage, T, List[BaseMessage], QianFanStreamIterator]:
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
    ) -> Union[str, BaseMessage, T, List[BaseMessage], QianFanStreamIterator]:
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
            return QianFanStreamIterator(
                response_stream=response, return_raw_response=return_raw_response
            )
        else:
            if response.code == 200:
                ret_data = response.body
                logger.debug(f"[pne ernie response] {ret_data}")
                content: str = ret_data["result"]
                logger.debug(f"[pne ernie answer] {content}")
                return AssistantMessage(content=content, additional_kwargs=ret_data)
