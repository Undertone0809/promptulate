from unittest import TestCase

from langchain.tools.shell.tool import ShellTool

from promptulate.tools.langchain.tools import LangchainTool


class TestLangchainTool(TestCase):
    def test_shell_run(self):
        tool = LangchainTool(ShellTool())
        result = tool._run("echo HelloWorld")
        print(result)
        self.assertIsNotNone(result)
