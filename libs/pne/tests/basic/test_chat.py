from types import SimpleNamespace

import pytest
from pydantic import BaseModel

import pne
from pne.chat import Mode


def _mock_completion_response(content: str):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
        json=lambda: {"id": "resp_123"},
    )


def test_public_chat_normalizes_string_input(mocker):
    mock_completion = mocker.patch(
        "litellm.completion",
        return_value=_mock_completion_response("hello from the model"),
    )

    response = pne.chat(
        "Hello there",
        model="openai/gpt-4o-mini",
        model_config={"temperature": 0.2},
    )

    assert response == "hello from the model"
    mock_completion.assert_called_once()
    assert mock_completion.call_args.kwargs == {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": "Hello there",
                "function_call": None,
                "tool_calls": None,
            }
        ],
        "temperature": 0.2,
        "stream": False,
    }


def test_public_chat_supports_output_schema(mocker):
    class StructuredResponse(BaseModel):
        cities: list[str]

    mock_completion = mocker.patch(
        "litellm.completion",
        return_value=_mock_completion_response('{"cities":["Shanghai","Beijing"]}'),
    )

    response = pne.chat(
        [{"role": "user", "content": "List two cities in China."}],
        model="openai/gpt-4o-mini",
        output_schema=StructuredResponse,
    )

    assert response == StructuredResponse(cities=["Shanghai", "Beijing"])
    assert (
        "## Output format"
        in mock_completion.call_args.kwargs["messages"][-1]["content"]
    )


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"enable_plan": True}, "enable_plan"),
        ({"enable_memory": True}, "enable_memory"),
        ({"mode": Mode.REACT}, "Mode.CHAT"),
        ({"stream": True}, "stream"),
    ],
)
def test_public_chat_rejects_deferred_p0_features(kwargs, message):
    with pytest.raises(NotImplementedError, match=message):
        pne.chat("Hello", model="openai/gpt-4o-mini", **kwargs)


def test_root_exports_aichat():
    assert pne.AIChat is not None
