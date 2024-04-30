"""Docs: https://docs.litellm.ai/docs/"""
import json
from typing import Optional, TypeVar, Union

import litellm

from promptulate.llms import BaseLLM
from promptulate.pydantic_v1 import BaseModel
from promptulate.schema import (
    AssistantMessage,
    MessageSet,
    StreamIterator,
)
from promptulate.utils.logger import logger

T = TypeVar("T", bound=BaseModel)


def parse_content(chunk) -> (str, str):
    """Parse the litellm chunk.
    Args:
        chunk: litellm chunk.

    Returns:
        content: The content of the chunk.
        ret_data: The additional data of the chunk.
    """
    content = chunk.choices[0].delta.content
    ret_data = json.loads(chunk.json())
    return content, ret_data


class LiteLLM(BaseLLM):
    def __init__(self, model: str, model_config: Optional[dict] = None, **kwargs):
        logger.info(f"[pne chat] init LiteLLM, model: {model} config: {model_config}")
        super().__init__(**kwargs)
        self._model: str = model
        self._model_config: dict = model_config or {}

    def _predict(
        self, messages: MessageSet, stream: bool = False, *args, **kwargs
    ) -> Union[AssistantMessage, StreamIterator]:
        logger.info(f"[pne chat] prompts: {messages.string_messages}")
        temp_response = litellm.completion(
            model=self._model, messages=messages.listdict_messages, **self._model_config
        )

        if stream:
            return StreamIterator(
                response_stream=temp_response,
                parse_content=parse_content,
                return_raw_response=False,
            )

        response = AssistantMessage(
            content=temp_response.choices[0].message.content,
            additional_kwargs=temp_response.json()
            if isinstance(temp_response.json(), dict)
            else json.loads(temp_response.json()),
        )
        logger.debug(
            f"[pne chat] response: {json.dumps(response.additional_kwargs, indent=2)}"
        )
        return response

    def __call__(self, instruction: str, *args, **kwargs) -> str:
        return self._predict(
            MessageSet.from_listdict_data(
                [
                    {"content": "You are a helpful assistant.", "role": "system"},
                    {"content": instruction, "role": "user"},
                ]
            )
        ).content
