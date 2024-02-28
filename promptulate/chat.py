import json
from typing import Dict, List, Optional, TypeVar, Union

from promptulate.llms import BaseLLM
from promptulate.output_formatter import formatting_result, get_formatted_instructions
from promptulate.pydantic_v1 import BaseModel
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
    messages: Union[List, MessageSet, str],
    *,
    model: str = "gpt-3.5-turbo",
    tools: Optional[List[BaseTool]] = None,
    output_schema: Optional[type(BaseModel)] = None,
    examples: Optional[List[BaseModel]] = None,
    return_raw_response: bool = False,
    custom_llm: Optional[BaseLLM] = None,
    **kwargs,
) -> Union[str, BaseMessage, T, List[BaseMessage], StreamIterator]:
    """A universal chat method, you can chat any model like OpenAI completion.
    It should be noted that chat() is only support chat model currently.

    Args:
        messages: chat messages. OpenAI API completion, str or MessageSet type is
            optional.
        model(str): LLM model. Currently only support chat model.
        tools(List[BaseTool] | None): specified tools for llm.
        output_schema(BaseModel): specified return type. See detail on: OutputFormatter.
        examples(List[BaseModel]): examples for output_schema. See detail
            on: OutputFormatter.
        return_raw_response(bool): return OpenAI completion result if true, otherwise
            return string type data.
        custom_llm(BaseLLM): You can use custom LLM if you have.
        **kwargs: litellm kwargs

    Returns:
        Return string normally, it means enable_original_return is default False.
        Return BaseMessage if enable_original_return is True.
        Return List[BaseMessage] if stream is True.
        Return T if output_schema is provided.
    """
    if kwargs.get("stream", None) and output_schema:
        raise ValueError(
            "stream and output_schema can't be True at the same time, "
            "because stream is used to return Iterator[BaseMessage]."
        )

    # messages covert, covert to OpenAI API type chat completion
    if isinstance(messages, MessageSet):
        messages: List[Dict[str, str]] = messages.listdict_messages
    elif isinstance(messages, str):
        messages = [
            {"content": "You are a helpful assistant", "role": "system"},
            {"content": messages, "role": "user"},
        ]

    # add output format into system prompt if provide
    if output_schema:
        instruction = get_formatted_instructions(
            json_schema=output_schema, examples=examples
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

    logger.debug(f"[pne chat] response: {response.additional_kwargs}")

    # return output format if provide
    if output_schema:
        logger.info("[pne chat] return output format.")
        return formatting_result(
            pydantic_obj=output_schema, llm_output=response.content
        )

    return response if return_raw_response else response.content
