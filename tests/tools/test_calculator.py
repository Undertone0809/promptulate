import pytest

from promptulate.llms.base import BaseLLM
from promptulate.tools import Calculator


@pytest.fixture
def mock_llm(mocker):
    # Create a mock instance of BaseLLM
    mock = mocker.MagicMock(spec=BaseLLM)
    # Configure the mock to return a specific value when called
    mock.return_value = '{"expression": "2 + 2"}'
    return mock


def test_run_valid_expression(mocker, mock_llm):
    # Instantiate the Calculator with the mocked LLM
    calculator = Calculator(llm=mock_llm)

    # Mock the _is_valid_expression to return True
    with mocker.patch(
        "promptulate.tools.math.tools._is_valid_expression", return_value=True
    ):
        # Mock the _evaluate_expression to return a specific value
        with mocker.patch(
            "promptulate.tools.math.tools._evaluate_expression", return_value="4"
        ):
            # Call the _run method with a valid expression
            result = calculator._run("2 + 2")
            # Assert that the result is as expected
            assert result == "4"


def test_run_invalid_expression(mocker, mock_llm):
    # Instantiate the Calculator with the mocked LLM
    calculator = Calculator(llm=mock_llm)

    # Mock the _is_valid_expression to return False
    with mocker.patch(
        "promptulate.tools.math.tools._is_valid_expression", return_value=False
    ):
        # Call the _run method with an invalid expression
        result = calculator._run("some invalid expression")
        # Assert that the result is as expected, which is the mocked LLM output
        assert result == "4"  # Assuming that the mocked LLM output evaluates to 4
