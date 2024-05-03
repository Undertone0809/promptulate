import pytest

from promptulate.tools import calculator


@pytest.fixture
def mock():
    # Configure the mock to return a specific value when called
    mock.return_value = '{"expression": "2 + 2"}'
    return mock


def test_run_valid_expression(mocker):
    # Mock the _is_valid_expression to return True
    with mocker.patch(
        "promptulate.tools.math.tools._is_valid_expression", return_value=True
    ):
        # Mock the _evaluate_expression to return a specific value
        with mocker.patch(
            "promptulate.tools.math.tools._evaluate_expression", return_value="4"
        ):
            # Call the calculator function with a valid expression
            result = calculator("2 + 2")
            # Assert that the result is as expected
            assert result == "4"


def test_run_invalid_expression(mocker):
    # Mock the _is_valid_expression to return False
    with mocker.patch(
        "promptulate.tools.math.tools._is_valid_expression", return_value=False
    ):
        # Call the calculator function with an invalid expression
        with pytest.raises(ValueError):
            calculator("some invalid expression")
