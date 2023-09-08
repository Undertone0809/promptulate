from promptulate.tools import BaseTool
from promptulate.utils.color_print import print_text


class HumanFeedBackTool(BaseTool):
    """A tool for running python code in a REPL."""

    name: str = "human_feedback"
    description: str = (
        "Human feedback tools are used to collect human feedback information."
        "Please only use this tool in situations where relevant contextual information is lacking or reasoning cannot "
        "continue."
        "Please enter the content you wish for human feedback and interaction, but do not ask for knowledge or let "
        "humans reason. "
    )

    def _run(self, content: str, *args, **kwargs) -> str:
        print_text(f"[Agent ask] {content}", "blue")
        return input()
