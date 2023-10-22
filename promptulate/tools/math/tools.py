import math
import re

import numexpr

from promptulate.llms.base import BaseLLM
from promptulate.llms.openai import ChatOpenAI
from promptulate.tools.base import Tool
from promptulate.tools.math.prompt import prompt_template
from promptulate.utils.string_template import StringTemplate


class Calculator(Tool):
    """A Math operator"""

    name: str = "math-calculator"
    description: str = (
        "Useful for when you need to answer questions about math.You input is a nature"
        "language of math expression."
    )
    llm_prompt_template: StringTemplate = prompt_template

    def __init__(self, llm: BaseLLM = None, **kwargs):
        self.llm: BaseLLM = llm or ChatOpenAI(
            temperature=0, enable_default_system_prompt=False
        )
        super().__init__(**kwargs)

    def _run(self, prompt: str) -> str:
        prompt = self.llm_prompt_template.format(question=prompt)
        llm_output = self.llm(prompt, stop=["```output"])

        return self._process_llm_result(llm_output)

    def _process_llm_result(self, llm_output: str) -> str:
        llm_output = llm_output.strip()
        text_match = re.search(r"^```text(.*?)```", llm_output, re.DOTALL)
        if text_match:
            expression = text_match.group(1)
            output = self._evaluate_expression(expression)
            answer = output
        elif llm_output.startswith("Answer:"):
            answer = llm_output.split("Answer:")[-1]
        elif "Answer:" in llm_output:
            answer = llm_output.split("Answer:")[-1]
        else:
            raise ValueError(f"unknown format from LLM: {llm_output}")
        return answer

    def _evaluate_expression(self, expression: str) -> str:
        """Parse numexpr expression."""
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
                f'LLMMathChain._evaluate("{expression}") raised error: {e}.'
                " Please try again with a valid numerical expression"
            )

        # Remove any leading and trailing brackets from the output
        return re.sub(r"^\[|\]$", "", output)
