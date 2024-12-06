import sys
from datetime import datetime
from pathlib import Path

import pytest

from pne.message import (
    AssistantMessage,
    FunctionMessage,
    MessageSet,
    SystemMessage,
    ToolMessage,
    UserMessage,
)


def test_system_message():
    content = "You are a helpful assistant"
    msg = SystemMessage(content=content)
    assert msg.content == content
    assert msg.type == "system"
    assert isinstance(msg.created_at, datetime)


def test_user_message():
    content = "What's the weather like?"
    msg = UserMessage(content=content)
    assert msg.content == content
    assert msg.type == "user"


def test_assistant_message():
    content = "I'll check the weather for you"
    msg = AssistantMessage(
        content=content,
        function_call={"name": "get_weather", "arguments": '{"location": "London"}'},
    )
    assert msg.content == content
    assert msg.type == "assistant"
    assert msg.function_call["name"] == "get_weather"

    # Test with tool calls
    msg_with_tools = AssistantMessage(
        content="Let me search that for you",
        tool_calls=[
            {
                "id": "call_123",
                "type": "function",
                "function": {
                    "name": "search",
                    "arguments": '{"query": "weather London"}',
                },
            }
        ],
    )
    assert len(msg_with_tools.tool_calls) == 1
    assert msg_with_tools.tool_calls[0]["id"] == "call_123"


def test_function_message():
    content = "The weather in London is sunny and 22°C"
    msg = FunctionMessage(
        content=content,
        name="get_weather",
        arguments={"location": "London"},
    )
    assert msg.content == content
    assert msg.type == "function"
    assert msg.name == "get_weather"
    assert msg.arguments["location"] == "London"
    assert msg.status == "success"

    # Test with error status
    error_msg = FunctionMessage(
        content="API request failed",
        name="get_weather",
        arguments={"location": "Invalid"},
        status="error",
    )
    assert error_msg.status == "error"


def test_tool_message():
    content = "Search results for weather in London"
    msg = ToolMessage(
        content=content,
        name="search",
        tool_call_id="call_123",
        arguments={"query": "weather London"},
    )
    assert msg.content == content
    assert msg.type == "tool"
    assert msg.name == "search"
    assert msg.tool_call_id == "call_123"
    assert msg.arguments["query"] == "weather London"
    assert msg.status == "success"


def test_message_set():
    messages_data = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "What's the weather like?"},
        {
            "role": "assistant",
            "content": "Let me check the weather for you",
            "function_call": {
                "name": "get_weather",
                "arguments": '{"location": "London"}',
            },
        },
        {
            "role": "function",
            "name": "get_weather",
            "content": "The weather in London is sunny and 22°C",
            "arguments": {"location": "London"},
        },
    ]

    metadata = {"session_id": "test_123"}
    message_set = MessageSet.from_raw(messages_data, metadata=metadata)

    assert len(message_set.messages) == 4
    assert message_set.metadata["session_id"] == "test_123"
    assert isinstance(message_set.created_at, datetime)

    # Check each message type
    assert isinstance(message_set.messages[0], SystemMessage)
    assert isinstance(message_set.messages[1], UserMessage)
    assert isinstance(message_set.messages[2], AssistantMessage)
    assert isinstance(message_set.messages[3], FunctionMessage)

    # Check function call details
    assistant_msg = message_set.messages[2]
    assert assistant_msg.function_call["name"] == "get_weather"

    function_msg = message_set.messages[3]
    assert function_msg.name == "get_weather"
    assert function_msg.arguments["location"] == "London"


def test_message_set_with_tool_calls():
    messages_data = [
        {"role": "user", "content": "Search for weather in London"},
        {
            "role": "assistant",
            "content": "I'll search that for you",
            "tool_calls": [
                {
                    "id": "call_123",
                    "type": "function",
                    "function": {
                        "name": "search",
                        "arguments": '{"query": "weather London"}',
                    },
                }
            ],
        },
        {
            "role": "tool",
            "name": "search",
            "tool_call_id": "call_123",
            "content": "Found weather information for London",
            "arguments": {"query": "weather London"},
        },
    ]

    message_set = MessageSet.from_raw(messages_data)

    assert len(message_set.messages) == 3
    assert isinstance(message_set.messages[1], AssistantMessage)
    assert isinstance(message_set.messages[2], ToolMessage)

    # Check tool call details
    assistant_msg = message_set.messages[1]
    assert len(assistant_msg.tool_calls) == 1
    assert assistant_msg.tool_calls[0]["id"] == "call_123"

    tool_msg = message_set.messages[2]
    assert tool_msg.name == "search"
    assert tool_msg.tool_call_id == "call_123"
    assert tool_msg.arguments["query"] == "weather London"


def test_user_message_with_multimodal_content():
    content = [
        {"type": "text", "text": "What's in this image?"},
        {
            "type": "image_url",
            "image_url": {
                "url": "https://example.com/image.jpg",
            },
        },
    ]
    msg = UserMessage(content=content)
    assert msg.content == content
    assert msg.type == "user"
    assert isinstance(msg.content, list)
    assert len(msg.content) == 2
    assert msg.content[0]["type"] == "text"
    assert msg.content[1]["type"] == "image_url"


def test_system_message_with_list_content():
    content = [
        {"type": "text", "text": "You are a helpful assistant"},
        {"type": "text", "text": "You can process both text and images"},
    ]
    msg = SystemMessage(content=content)
    assert msg.content == content
    assert msg.type == "system"
    assert isinstance(msg.content, list)
    assert len(msg.content) == 2
    assert all(item["type"] == "text" for item in msg.content)
