from typing import Dict, List, Optional, Union

from litellm import completion
from pydantic import BaseModel

from promptulate.llms import BaseLLM
from promptulate.output_formatter import formatting_result, get_formatted_instructions
from promptulate.schema import AssistantMessage, BaseMessage, MessageSet


def chat(
    messages: Union[List, MessageSet, str],
    *,
    model: str = "gpt-3.5-turbo",
    output_schema: Optional[type(BaseModel)] = None,
    examples: Optional[List[BaseModel]] = None,
    is_message_return_type: bool = False,
    custom_llm: Optional[BaseLLM] = None,
    **kwargs,
) -> Union[str, BaseMessage]:
    """A universal chat method, you can chat any model like OpenAI completion.
    It should be noted that chat() is only support chat model currently.

    Args:
        messages: chat messages. OpenAI API completion, str or MessageSet type is
            optional.
        model(str): LLM model. Currently only support chat model.
        output_schema(BaseModel): specified return type. See detail on: OutputFormatter.
        examples(List[BaseModel]): examples for output_schema. See detail
            on: OutputFormatter.
        is_message_return_type(bool): return OpenAI completion result if true, otherwise
            return string type data.
        custom_llm(BaseLLM): You can use custom LLM if you have.
        *args: litellm args
        **kwargs: litellm kwargs

    Returns:
        Return string normally, it means enable_original_return is default False.
        Return BaseMessage if enable_original_return is True.
    """
    # messages covert, covert to OpenAI API type completion
    if isinstance(messages, MessageSet):
        messages: List[Dict[str, str]] = messages.listdict_messages
    elif isinstance(messages, str):
        messages = [{"content": messages, "role": "user"}]

    # output formatter if provide
    if output_schema:
        instruction = get_formatted_instructions(
            pydantic_obj=output_schema, examples=examples
        )
        messages[-1]["content"] += f"\n{instruction}"

    # chat by custom LLM and get response
    if custom_llm:
        response: BaseMessage = custom_llm.predict(
            MessageSet.from_listdict_data(messages), **kwargs
        )

    # chat by universal llm get response
    else:
        temp_response: Dict = completion(model, messages, **kwargs)
        response: BaseMessage = AssistantMessage(
            content=temp_response["choices"][0]["message"]["content"],
            additional_kwargs=temp_response,
        )

    # return output format if provide
    if output_schema:
        print(response.content)
        return formatting_result(
            pydantic_obj=output_schema, llm_output=response.content
        )

    return response if is_message_return_type else response.content
