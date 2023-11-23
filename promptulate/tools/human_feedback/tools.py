from typing import Callable

from promptulate.tools import Tool
from promptulate.utils.color_print import print_text


def _print_func(llm_question: str) -> None:
    """Default way to show llm question when llm using HumanFeedBackTool."""
    print_text(f"[Agent ask] {llm_question}", "blue")


class HumanFeedBackTool(Tool):
    """A tool for human feedback"""

    name: str = "human_feedback"
    description: str = (
        "Human feedback tools are used to collect human feedback information."
        "Please only use this tool in situations where relevant contextual information"
        "is lacking or reasoning cannot continue. Please enter the content you wish for"
        "human feedback and interaction, but do not ask for knowledge or let humans reason."  # noqa
    )

    def __init__(
        self,
        output_func: Callable[[str], None] = _print_func,
        input_func: Callable = input,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.output_func = output_func
        self.input_func = input_func

    def _run(self, content: str, *args, **kwargs) -> str:
        self.output_func(content)
        return self.input_func()
