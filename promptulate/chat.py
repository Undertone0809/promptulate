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
from promptulate.chat_utils import convert_messages, chat_by_custom_llm, add_output_format
from promptulate.utils.logger import logger
from promptulate.chat_utils import chat_by_litellm

T = TypeVar("T", bound=BaseModel)


from promptulate.chat_utils import convert_messages

def parse_content(chunk) -> (str, str):
    content = chunk.choices[0].delta.content
    ret_data = json.loads(chunk.json())
    return content, ret_data


def chat(
        )
        messages[-1]["content"] += f"\n{instruction}"

    logger.debug(f"[pne chat] messages: {messages}")

    convert_messages(messages)
    # TODO add BaseLLM support
    # chat by custom LLM and get response
response = chat_by_litellm(custom_llm, model, messages, kwargs)

    if kwargs.get("stream", None):
        return StreamIterator(
            response_stream=response,
            parse_content=parse_content,
            return_raw_response=return_raw_response,
        )
    else:
        response = AssistantMessage(content=response.choices[0].message.content,
                                    additional_kwargs=response.json()
                                        if isinstance(response.json(), dict)
                                        else json.loads(response.json()),
                                    )
    

    logger.debug(f"[pne chat] response: {response}")

    # return output format if provide
    if output_schema:
        logger.info("[pne chat] return output format.")
        return formatting_result(
            pydantic_obj=output_schema, llm_output=response.content
        )

    return response if return_raw_response else response.content
