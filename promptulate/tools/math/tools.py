import json
import math
import re

import numexpr

from promptulate.llms.base import BaseLLM
from promptulate.llms.openai import ChatOpenAI
from promptulate.tools.base import Tool
from promptulate.tools.math.prompt import prompt_template


def _evaluate_expression(expression: str) -> str:
    """
    Parse numexpr expression.

    This function takes a string expression, evaluates it using numexpr.evaluate,
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
    """
    A Math operator.

    This class is a tool for evaluating mathematical expressions. It uses the
    _evaluate_expression and _is_valid_expression functions to evaluate expressions
    and check their validity. It also uses the BaseLLM class to generate prompts
    for the user.

    Attributes:
        name (str): The name of the tool.
        description (str): A description of the tool.
        llm (BaseLLM): An instance of the BaseLLM class.
    """

    name: str = "math-calculator"
    description: str = (
        "Useful for when you need to answer questions about math.You input is a nature"
        "language of math expression. Attention: Expressions can not exist variables!"
        "eg: (current age)^0.43 is wrong, you should use 18^0.43 instead."
    )

    def __init__(self, llm: BaseLLM = None, **kwargs):
        """
        Initialize the Calculator class.

        This method initializes the Calculator class with an instance of the BaseLLM
        class and any additional keyword arguments.

        Args:
            llm (BaseLLM, optional): An instance of the BaseLLM class. Defaults to None.
        """
        self.llm: BaseLLM = llm or ChatOpenAI(
            temperature=0, enable_default_system_prompt=False
        )
        super().__init__(**kwargs)

    def _run(self, question: str) -> str:
        """
        Run the Calculator tool.

        This method takes a prompt from the user, checks if it is a valid expression,
        and evaluates it if it is. If it is not a valid expression, it generates a
        new prompt using the BaseLLM class and evaluates the resulting expression.

        Args:
            question (str): The math problem of user.

        Returns:
            str: The result of the evaluation.

        Raises:
            ValueError: If the evaluation fails.
        """
        if _is_valid_expression(question):
            return _evaluate_expression(question)

        prompt: str = prompt_template.format(question=question)
        llm_output: str = self.llm(prompt)
        try:
            expression = json.loads(llm_output).get("expression")
            return _evaluate_expression(expression)
        except Exception as e:
            raise ValueError(f"Unknown format from LLM: {llm_output}, error: {e}")


def calculator(expression: str):
    """Evaluate a mathematical expression.

    Args:
        expression: A mathematical expression, eg: 18^0.43

    Attention:
        Expressions can not exist variables!
        eg: (current age)^0.43 is wrong, you should use 18^0.43 instead.

    Returns:
        The result of the evaluation.
    """
    return Calculator().run(expression)
