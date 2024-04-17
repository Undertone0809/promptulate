import json
from typing import Dict, List, Optional, TypeVar, Union

import litellm

from promptulate.agents.base import BaseAgent
from promptulate.agents.tool_agent.agent import ToolAgent
from promptulate.beta.agents.assistant_agent import AssistantAgent
from promptulate.llms import BaseLLM
from promptulate.output_formatter import formatting_result, get_formatted_instructions
from promptulate.pydantic_v1 import BaseModel
from promptulate.schema import (
    AssistantMessage,
    BaseMessage,
    MessageSet,
    StreamIterator,
    ToolTypes,
)
from promptulate.tools.base import BaseTool
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


class _LiteLLM(BaseLLM):
    def __init__(
        self, model: str, model_config: Optional[dict] = None, *args, **kwargs
    ):
        logger.info(f"[pne chat] init LiteLLM, model: {model} config: {model_config}")
        super().__init__(*args, **kwargs)
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


def _convert_message(messages: Union[List, MessageSet, str]) -> MessageSet:
    """Convert str or List[Dict] to MessageSet.

    Args:
        messages(Union[List, MessageSet, str]): chat messages. It can be str or OpenAI
            API type data(List[Dict]) or MessageSet type.

    Returns:
        Return MessageSet type data.
    """
    if isinstance(messages, str):
        messages: List[Dict] = [
            {"content": "You are a helpful assistant", "role": "system"},
            {"content": messages, "role": "user"},
        ]
    if isinstance(messages, list):
        messages: MessageSet = MessageSet.from_listdict_data(messages)

    return messages


def _get_llm(
    model: str = "gpt-3.5-turbo",
    model_config: Optional[dict] = None,
    custom_llm: Optional[BaseLLM] = None,
) -> BaseLLM:
    """Get LLM instance.

    Args:
        model(str): LLM model.
        model_config(dict): LLM model config.
        custom_llm(BaseLLM): custom LLM instance.

    Returns:
        Return LLM instance.
    """
    if custom_llm:
        return custom_llm

    return _LiteLLM(model=model, model_config=model_config)


class AIChat:
    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        model_config: Optional[dict] = None,
        tools: Optional[List[ToolTypes]] = None,
        custom_llm: Optional[BaseLLM] = None,
        enable_plan: bool = False,
    ):
        """Initialize the AIChat.

        Args:
            model(str): LLM model name, eg: "gpt-3.5-turbo".
            model_config(Optional[dict]): LLM model config.
            tools(Optional[List[ToolTypes]]): specified tools for llm, if exists, AIChat
                will use Agent to run.
            custom_llm(Optional[BaseLLM]): custom LLM instance.
            enable_plan(bool): use Agent with plan ability if True.
        """
        self.llm: BaseLLM = _get_llm(model, model_config, custom_llm)
        self.tools: Optional[List[ToolTypes]] = tools
        self.agent: Optional[BaseAgent] = None

        if tools:
            if enable_plan:
                self.agent = AssistantAgent(tools=self.tools, llm=self.llm)
                logger.info("[pne chat] invoke AssistantAgent with plan ability.")
            else:
                self.agent = ToolAgent(tools=self.tools, llm=self.llm)
                logger.info("[pne chat] invoke ToolAgent.")

    def run(
        self,
        messages: Union[List, MessageSet, str],
        output_schema: Optional[type(BaseModel)] = None,
        examples: Optional[List[BaseModel]] = None,
        return_raw_response: bool = False,
        stream: bool = False,
        **kwargs,
    ) -> Union[str, BaseMessage, T, List[BaseMessage], StreamIterator]:
        """Run the AIChat.

        Args:
            messages(Union[List, MessageSet, str]): chat messages. It can be str or
                OpenAI.
            API type data(List[Dict]) or MessageSet type.
            output_schema(BaseModel): specified return type. See detail on in
                OutputFormatter module.
            examples(List[BaseModel]): examples for output_schema. See detail
                on: OutputFormatter.
            return_raw_response(bool): return OpenAI completion result if true,
                otherwise return string type data.
            stream(bool): return stream iterator if True.

        Returns:
            Return string normally, it means enable_original_return is default False. if
                tools is provided, agent return string type data.
            Return BaseMessage if enable_original_return is True and not in agent mode.
            Return List[BaseMessage] if stream is True.
            Return T if output_schema is provided.
        """
        if stream and (output_schema or self.tools):
            raise ValueError(
                "stream, tools and output_schema can't be True at the same time, "
                "because stream is used to return Iterator[BaseMessage]."
            )

        if self.agent:
            return self.agent.run(messages, output_schema=output_schema)

        messages: MessageSet = _convert_message(messages)

        # add output format into the last prompt if provide
        if output_schema:
            instruction: str = get_formatted_instructions(
                json_schema=output_schema, examples=examples
            )
            messages.messages[-1].content += f"\n{instruction}"

        logger.info(f"[pne chat] messages: {messages}")

        response: AssistantMessage = self.llm.predict(messages, stream=stream, **kwargs)

        logger.info(f"[pne chat] response: {response.additional_kwargs}")

        # return output format if provide
        if output_schema:
            logger.info("[pne chat] return formatted response.")
            return formatting_result(
                pydantic_obj=output_schema, llm_output=response.content
            )

        return response if return_raw_response else response.content


def chat(
    messages: Union[List, MessageSet, str],
    *,
    model: str = "gpt-3.5-turbo",
    model_config: Optional[dict] = None,
    tools: Optional[List[ToolTypes]] = None,
    output_schema: Optional[type(BaseModel)] = None,
    examples: Optional[List[BaseModel]] = None,
    return_raw_response: bool = False,
    custom_llm: Optional[BaseLLM] = None,
    enable_plan: bool = False,
    stream: bool = False,
    **kwargs,
) -> Union[str, BaseMessage, T, List[BaseMessage], StreamIterator]:
    """A universal chat method, you can chat any model like OpenAI completion.
    It should be noted that chat() is only support chat model currently.

    Args:
        messages(Union[List, MessageSet, str]): chat messages. It can be str or OpenAI
            API type data(List[Dict]) or MessageSet type.
        model(str): LLM model. Currently only support chat model.
        model_config(Optional[dict]): LLM model config.
        tools(List[BaseTool] | None): specified tools for llm.
        output_schema(BaseModel): specified return type. See detail on: OutputFormatter.
        examples(List[BaseModel]): examples for output_schema. See detail
            on: OutputFormatter.
        return_raw_response(bool): return OpenAI completion result if true, otherwise
            return string type data.
        custom_llm(BaseLLM): You can use custom LLM if you have.
        enable_plan(bool): use Agent with plan ability if True.
        stream(bool): return stream iterator if True.
        **kwargs: litellm kwargs

    Returns:
        Return string normally, it means enable_original_return is default False.
        Return BaseMessage if enable_original_return is True.
        Return List[BaseMessage] if stream is True.
        Return T if output_schema is provided.
    """
    return AIChat(
        model=model,
        model_config=model_config,
        tools=tools,
        custom_llm=custom_llm,
        enable_plan=enable_plan,
    ).run(
        messages=messages,
        output_schema=output_schema,
        examples=examples,
        return_raw_response=return_raw_response,
        stream=stream,
        **kwargs,
    )
