from typing import Callable

from promptulate.tools import Tool
from promptulate.utils.color_print import print_text


def _print_func(content) -> None:
    print_text(f"[Agent ask] {content}", "blue")


class HumanFeedBackTool(Tool):
    """A tool for human feedback"""

    name: str = "human_feedback"
    description: str = (
        "Human feedback tools are used to collect human feedback information."
        "Please only use this tool in situations where relevant contextual information is lacking or reasoning cannot "
        "continue."
        "Please enter the content you wish for human feedback and interaction, but do not ask for knowledge or let "
        "humans reason. "
    )

    def __init__(
        self,
        prompt_func: Callable[[str], None] = _print_func,
        input_func: Callable = input,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.prompt_func = prompt_func
        self.input_func = input_func

    def _run(self, content: str, *args, **kwargs) -> str:
        self.prompt_func(content)
        return self.input_func()
