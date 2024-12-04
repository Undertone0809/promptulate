import json
import math
import re

from promptulate.llms.base import BaseLLM
from promptulate.llms.openai import ChatOpenAI
from promptulate.tools.base import Tool
from promptulate.tools.math.prompt import prompt_template


def _evaluate_expression(expression: str) -> str:
    """
    Parse numexpr expression.

    This function takes a string expression, evaluates it using `numexpr.evaluate`,
    and returns the result as a string. It also handles exceptions and raises a
    ValueError with a custom error message if the evaluation fails.

    Args:
        expression (str): The expression to evaluate.

    Returns:
        str: The result of the evaluation.

    Raises:
        ValueError: If the evaluation fails.
    """
    try:
        import numexpr
    except ImportError:
        raise ValueError(
            " Please install the numexpr package using `pip install numexpr`."
        )

    try:
        local_dict = {"pi": math.pi, "e": math.e}
        output = str(
            numexpr.evaluate(
                expression.strip(),
                global_dict={},  # restrict access to globals
                local_dict=local_dict,  # add common mathematical functions
            )
        )
    except Exception as e:
        raise ValueError(
            f'Calculator._evaluate_expression("{expression}") raised error: {e}.'
            " Please try again with a valid numerical expression"
        )

    # Remove any leading and trailing brackets from the output
    return re.sub(r"^\[|\]$", "", output)


def _is_valid_expression(expression: str) -> bool:
    """Check if the expression is valid."""
    try:
        _evaluate_expression(expression)
        return True
    except ValueError:
        return False


class Calculator(Tool):
    """A Math operator.

    This class is a tool for evaluating mathematical expressions. It uses the
    _evaluate_expression function to evaluate expressions.

    Attributes:
        name (str): The name of the tool.
        description (str): A description of the tool.
    """

    name: str = "math-calculator"
    description: str = (
        "Useful for when you need to evaluate mathematical expressions. "
        "Input should be a valid mathematical expression without variables. "
        "For example: '18^0.43' is valid, but '(current age)^0.43' is not."
    )

    def __init__(self, **kwargs):
        """Initialize the Calculator class.This method initializes the Calculator class
        with any additional keyword arguments.
        """
        super().__init__(**kwargs)

    def _run(self, expression: str) -> str:
        """
        Run the Calculator tool.

        This method takes a mathematical expression from the user and evaluates it.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            str: The result of the evaluation.

        Raises:
            ValueError: If the evaluation fails.
        """
        return _evaluate_expression(expression)


def calculator(expression: str):
    """Evaluate a mathematical expression.

    This function takes a string expression, evaluates it using `numexpr.evaluate`,
    and returns the result as a string. It also handles exceptions and raises a
    ValueError with a custom error message if the evaluation fails.

    Args:
        expression: A mathematical expression, eg: 18^0.43

    Attention:
        Expressions can not exist variables!
        bad example: (current age)^0.43, (number)^(1/5)
        good example: 18^0.43, 37593**(1/5)

    Returns:
        The result of the evaluation.
    """
    return _evaluate_expression(expression)
