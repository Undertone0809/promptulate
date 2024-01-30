"""
TODO add test: test_stream, test pne's llm, test litellm llm
"""
from typing import Optional

import pytest
from pydantic import BaseModel, Field

import promptulate as pne
from promptulate import chat
from promptulate.llms import BaseLLM
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


class LLMResponse(BaseModel):
    city: str = Field(description="city name")
    temperature: float = Field(description="temperature")


def test_custom_llm_chat():
    llm = FakeLLM()

    # test general chat
    answer = chat("hello", model="fake", custom_llm=llm)
    assert answer == "fake response"

    # test messages is MessageSet
    messages = MessageSet(
        messages=[UserMessage(content="hello"), AssistantMessage(content="fake")]
    )
    answer = chat(messages, model="fake", custom_llm=llm)
    assert answer == "fake response"

    # Add test case with a different role
    user_message = UserMessage(content="hello")
    assistant_message = AssistantMessage(content="fake")
    messages = MessageSet(messages=[user_message, assistant_message])
    answer = chat(messages, model="fake", custom_llm=llm)
    assert answer == "fake response"
    answer = chat(messages, model="fake", custom_llm=llm)
    assert answer == "fake response"
    messages = [{"content": "Hello, how are you?", "role": "user"}]
    answer = chat(messages, model="fake", custom_llm=llm)
    assert answer == "fake response"

    # add additional unit tests for different scenarios and edge cases
    # Add a new test case with a different role
    user_message = UserMessage(content="hello")
    assistant_message = AssistantMessage(content="fake")
    messages = MessageSet(messages=[user_message, assistant_message])
    answer = chat(messages, model="fake", custom_llm=llm)
    assert answer == "fake response"


def test_custom_llm_chat_response_and_new_logic():
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

        # Add test case for formatter response with examples
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
def test_stream():
    class LLMResponse(BaseModel):
        data: Optional[str] = None

    # stream and output_schema and not exist at the same time.
    with pytest.raises(ValueError):
        pne.chat("hello", stream=True, output_schema=LLMResponse)
def test_stream():
    class LLMResponse(BaseModel):
        data: Optional[str] = None

    # stream and output_schema and not exist at the same time.
    with pytest.raises(ValueError):
        pne.chat("hello", stream=True, output_schema=LLMResponse)
def test_stream():
    class LLMResponse(BaseModel):
        data: Optional[str] = None

    # stream and output_schema and not exist at the same time.
    with pytest.raises(ValueError):
        pne.chat("hello", stream=True, output_schema=LLMResponse)
