import json
from typing import Dict, Iterator, List, Optional, TypeVar, Union

from pydantic import BaseModel

from promptulate.llms import BaseLLM
from promptulate.output_formatter import formatting_result, get_formatted_instructions
from promptulate.schema import (
    AssistantMessage,
    BaseMessage,
    MessageSet,
)
from promptulate.tools.base import BaseTool
from promptulate.utils.logger import logger

T = TypeVar("T", bound=BaseModel)


class LitellmStreamIterator:
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
        content: Optional[str] = chunk.choices[0].delta.content
        if content is None:
            return None

        if self.return_raw_response:
            additional_kwargs: dict = json.loads(chunk.json())
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
) -> Union[str, BaseMessage, T, List[BaseMessage], LitellmStreamIterator]:
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
            return LitellmStreamIterator(
                response_stream=temp_response, return_raw_response=return_raw_response
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
