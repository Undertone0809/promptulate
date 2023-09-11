from unittest import TestCase

from promptulate.tools.human_feedback import HumanFeedBackTool


class TestHumanFeedBackTool(TestCase):
    def prompt_func(self, content: str) -> None:
        print(content)

    def input_func(self):
        return input()

    def test_run(self):
        tool = HumanFeedBackTool(
            prompt_func=self.prompt_func, input_func=self.input_func
        )
        result = tool.run("我好冷")
        print(result)
