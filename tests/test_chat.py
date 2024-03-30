"""
TODO add test: test_stream, test pne's llm, test litellm llm
"""
from typing import Optional

import pytest

import promptulate as pne
from promptulate import chat
from promptulate.llms import BaseLLM
from promptulate.pydantic_v1 import BaseModel, Field
from promptulate.schema import AssistantMessage, BaseMessage, MessageSet, UserMessage


class FakeLLM(BaseLLM):
    llm_type: str = "fake"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, instruction: str, *args, **kwargs):
        return "fake response"

    def _predict(self, messages: MessageSet, *args, **kwargs) -> BaseMessage:
        content = "fake response"

        if "Output format" in messages.messages[-1].content:
            content = """{"city": "Shanghai", "temperature": 25}"""

        return AssistantMessage(content=content)


def mock_tool():
    """This is mock tool"""
    return "mock tool"


class LLMResponse(BaseModel):
    city: str = Field(description="city name")
    temperature: float = Field(description="temperature")


def test_init():
    llm = FakeLLM()

    # stream and output_schema and not exist at the same time.
    with pytest.raises(ValueError):
        chat("hello", custom_llm=llm, output_schema=LLMResponse, stream=True)

    # stream and tools and not exist at the same time.
    with pytest.raises(ValueError):
        chat("hello", custom_llm=llm, tools=[mock_tool], stream=True)

    # It is not allowed to pass MessageSet or List[Dict] type messages when using tools.
    with pytest.raises(ValueError):
        chat(
            MessageSet(messages=[UserMessage(content="hello")]),
            custom_llm=llm,
            tools=[mock_tool],
        )
        chat([], custom_llm=llm, tools=[mock_tool])


def test_custom_llm_chat():
    llm = FakeLLM()

    # test general chat
    answer = chat("hello", custom_llm=llm)
    assert answer == "fake response"

    # test messages is MessageSet
    messages = MessageSet(
        messages=[UserMessage(content="hello"), AssistantMessage(content="fake")]
    )
    answer = chat(messages, custom_llm=llm)
    assert answer == "fake response"

    # test messages is list
    messages = [{"content": "Hello, how are you?", "role": "user"}]
    answer = chat(messages, custom_llm=llm)
    assert answer == "fake response"


def test_custom_llm_chat_response():
    llm = FakeLLM()

    # test original response
    answer = chat("hello", model="fake", custom_llm=llm, return_raw_response=True)
    assert isinstance(answer, BaseMessage)
    assert answer.content == "fake response"

    # test formatter response
    answer = chat(
        "what's weather tomorrow in shanghai?",
        model="fake",
        output_schema=LLMResponse,
        custom_llm=llm,
    )
    assert isinstance(answer, LLMResponse)
    assert getattr(answer, "city", None) == "Shanghai"
    assert getattr(answer, "temperature", None) == 25

    # test formatter response with examples
    examples = [
        LLMResponse(city="Shanghai", temperature=25),
        LLMResponse(city="Beijing", temperature=30),
    ]
    answer = chat(
        "what's weather tomorrow in shanghai?",
        model="fake",
        output_schema=LLMResponse,
        examples=examples,
        custom_llm=llm,
    )
    assert isinstance(answer, LLMResponse)
    assert getattr(answer, "city", None) == "Shanghai"
    assert getattr(answer, "temperature", None) == 25


def test_stream():
    class LLMResponse(BaseModel):
        data: Optional[str] = None

    # stream and output_schema and not exist at the same time.
    with pytest.raises(ValueError):
        pne.chat("hello", stream=True, output_schema=LLMResponse)
