from typing import Dict, List, Optional, TypeVar, Union

from promptulate.agents.base import BaseAgent
from promptulate.agents.tool_agent.agent import ToolAgent
from promptulate.beta.agents.assistant_agent import AssistantAgent
from promptulate.llms import BaseLLM
from promptulate.llms.factory import LLMFactory
from promptulate.output_formatter import formatting_result, get_formatted_instructions
from promptulate.pydantic_v1 import BaseModel
from promptulate.schema import (
    AssistantMessage,
    BaseMessage,
    MessageSet,
    StreamIterator,
    SystemMessage,
)
from promptulate.tools.base import BaseTool, ToolTypes
from promptulate.utils.logger import logger

T = TypeVar("T", bound=BaseModel)


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
            {"content": messages, "role": "user"},
        ]
    if isinstance(messages, list):
        messages: MessageSet = MessageSet.from_listdict_data(messages)

    return messages


def _get_llm(
    model: Optional[str] = None,
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
    if (model or custom_llm) is None:
        raise ValueError("model or custom_llm must be provided.")

    if model and custom_llm:
        raise ValueError("model and custom_llm can't be provided at the same time.")

    if model_config and custom_llm:
        raise ValueError(
            "model_config and custom_llm can't be provided at the same time."
        )

    if custom_llm:
        return custom_llm

    return LLMFactory.build(model, model_config=model_config)


class AIChat:
    def __init__(
        self,
        model: Optional[str] = None,
        model_config: Optional[dict] = None,
        tools: Optional[List[ToolTypes]] = None,
        custom_llm: Optional[BaseLLM] = None,
        enable_plan: bool = False,
        enable_memory: bool = False,
    ):
        """Initialize the AIChat.

        Args:
            model(str): LLM model name, eg: "gpt-3.5-turbo".
            model_config(Optional[dict]): LLM model config.
            tools(Optional[List[ToolTypes]]): specified tools for llm, if exists, AIChat
                will use Agent to run.
            custom_llm(Optional[BaseLLM]): custom LLM instance.
            enable_plan(bool): use Agent with plan ability if True.
            enable_memory(bool): enable memory if True.
        """
        self.llm: BaseLLM = _get_llm(model, model_config, custom_llm)
        self.tools: Optional[List[ToolTypes]] = tools
        self.agent: Optional[BaseAgent] = None

        self.enable_memory: bool = enable_memory
        self.memory: MessageSet = MessageSet(messages=[])

        if tools:
            if enable_plan:
                self.agent = AssistantAgent(tools=self.tools, llm=self.llm)
                logger.info("[pne chat] invoke AssistantAgent with plan ability.")
            else:
                self.agent = ToolAgent(tools=self.tools, llm=self.llm)
                logger.info("[pne chat] invoke ToolAgent.")

    def run(
        self,
        messages: Union[List[Dict[str, str]], MessageSet, str],
        output_schema: Optional[type(BaseModel)] = None,
        examples: Optional[List[BaseModel]] = None,
        return_raw_response: bool = False,
        stream: bool = False,
        **kwargs,
    ) -> Union[str, BaseMessage, T, List[BaseMessage], StreamIterator]:
        """Run the AIChat, AIChat use self.memory to store chat messages.

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

        if not self.enable_memory:
            self.memory: MessageSet = MessageSet(messages=[])

        _: MessageSet = _convert_message(messages)
        self.memory.add_from_message_set(_)

        # initialize memory with system message if it is empty
        if len(self.memory.messages) == 1:
            self.memory.messages = [
                SystemMessage(content="You are a helpful assistant"),
                *self.memory.messages,
            ]

        if self.agent:
            response: Union[str, BaseModel] = self.agent.run(
                self.memory.string_messages, output_schema=output_schema
            )
            self.memory.add_ai_message(response)

            return response

        # add output format into the last prompt if provide
        if output_schema:
            instruction: str = get_formatted_instructions(
                json_schema=output_schema, examples=examples
            )
            self.memory.messages[-1].content += f"\n{instruction}"
        logger.info(f"[pne chat] messages: {messages}")

        response: Union[AssistantMessage, StreamIterator] = self.llm.predict(
            self.memory, stream=stream, **kwargs
        )

        # TODO: add stream memory support
        if stream:
            return response

        logger.info(
            f"[pne chat] response: {response.additional_kwargs or response.content}"
        )
        self.memory.add_ai_message(response.content)

        # return output format if provide
        if output_schema:
            return formatting_result(
                pydantic_obj=output_schema, llm_output=response.content
            )

        return response if return_raw_response else response.content


def chat(
    messages: Union[List, MessageSet, str],
    *,
    model: Optional[str] = None,
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
