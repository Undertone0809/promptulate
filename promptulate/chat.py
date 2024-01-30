import json
from typing import Tuple, Dict, List, Optional, TypeVar, Union

from pydantic import BaseModel

from promptulate.llms import BaseLLM
from promptulate.output_formatter import formatting_result, get_formatted_instructions
from promptulate.schema import (
    AssistantMessage,
    BaseMessage,
    MessageSet,
    StreamIterator,
)
from promptulate.tools.base import BaseTool
from promptulate.utils.logger import logger

T = TypeVar("T", bound=BaseModel)


def parse_content(chunk) -> (str, str):
    content = chunk.choices[0].delta.content
    ret_data = json.loads(chunk.json())
    return content, ret_data


def chat(
        )
        messages[-1]["content"] += f"\n{instruction}"

    logger.debug(f"[pne chat] messages: {messages}")

    # TODO add assistant Agent
    # TODO add BaseLLM support
    # chat by custom LLM and get response
    if custom_llm:
        response: BaseMessage = custom_llm.predict(
            MessageSet.from_listdict_data(messages), **kwargs
        )
    # chat by universal llm get response
    else:
        import litellm

        logger.info("[pne chat] chat by litellm.")
        temp_response = litellm.completion(model, messages, **kwargs)

        # return stream
        if kwargs.get("stream", None):
            return StreamIterator(
                response_stream=temp_response,
                parse_content=parse_content,
                return_raw_response=return_raw_response,
            )
        else:
            response: BaseMessage = AssistantMessage(
                content=temp_response.choices[0].message.content,
                additional_kwargs=temp_response.json()
                if isinstance(temp_response.json(), dict)
                else json.loads(temp_response.json()),
            )

    logger.debug(f"[pne chat] response: {response}")

    # return output format if provide
    if output_schema:
        logger.info("[pne chat] return output format.")
        return formatting_result(
            pydantic_obj=output_schema, llm_output=response.content
        )

    return response if return_raw_response else response.content
