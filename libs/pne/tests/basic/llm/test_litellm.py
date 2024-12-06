# from unittest.mock import MagicMock, patch

# import pytest

# from pne.callbacks.base import CallbackHandler
# from pne.llm._litellm import LiteLLM
# from pne.message import MessageSet, UserMessage


# class TestCallbackHandler(CallbackHandler):
#     def __init__(self):
#         self.tokens = []
#         self.errors = []

#     def on_llm_new_token(self, token: str, **kwargs):
#         self.tokens.append(token)

#     def on_llm_error(self, error: Exception, **kwargs):
#         self.errors.append(error)


# @pytest.fixture
# def callback_handler():
#     return TestCallbackHandler()


# @pytest.fixture
# def lite_llm(callback_handler):
#     return LiteLLM(
#         model="gpt-3.5-turbo",
#         callbacks=[callback_handler],
#     )


# def test_stream_callback(lite_llm, callback_handler):
#     messages = MessageSet([UserMessage(content="Hello")])

#     # Mock the litellm.completion response
#     mock_chunks = [
#         MagicMock(choices=[MagicMock(delta=MagicMock(content="Hello"))]),
#         MagicMock(choices=[MagicMock(delta=MagicMock(content=" World"))]),
#     ]

#     with patch("litellm.completion") as mock_completion:
#         mock_completion.return_value = mock_chunks
#         response = lite_llm._run(messages, stream=True)

#         # Consume the stream
#         list(response)

#         # Verify callbacks were called with correct tokens
#         assert callback_handler.tokens == ["Hello", " World"]
#         assert len(callback_handler.errors) == 0


# def test_error_callback(lite_llm, callback_handler):
#     messages = MessageSet([UserMessage(content="Hello")])

#     # Mock an error in litellm.completion
#     with patch("litellm.completion") as mock_completion:
#         mock_completion.side_effect = Exception("API Error")

#         with pytest.raises(Exception):
#             lite_llm._run(messages, stream=True)

#         # Verify error callback was called
#         assert len(callback_handler.errors) == 1
#         assert str(callback_handler.errors[0]) == "API Error"


# def test_non_stream_response(lite_llm):
#     messages = MessageSet([UserMessage(content="Hello")])

#     mock_response = MagicMock()
#     mock_response.choices = [
#         MagicMock(message=MagicMock(content="Hello, how can I help?"))
#     ]
#     mock_response.json.return_value = {"id": "test-id", "usage": {"total_tokens": 10}}

#     with patch("litellm.completion") as mock_completion:
#         mock_completion.return_value = mock_response
#         response = lite_llm._run(messages, stream=False)

#         assert response.content == "Hello, how can I help?"
#         assert response.additional_kwargs["id"] == "test-id"
#         assert response.additional_kwargs["usage"]["total_tokens"] == 10
