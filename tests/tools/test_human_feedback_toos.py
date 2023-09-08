from unittest import TestCase

from promptulate.tools.human_feedback import HumanFeedBackTool


class TestHumanFeedBackTool(TestCase):
    def test_run(self):
        tool = HumanFeedBackTool()
        result = tool.run("我好冷")
        print(result)
