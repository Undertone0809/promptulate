from unittest import TestCase

from promptulate.tools.shell import ShellTool
from promptulate.tools.shell.api_wrapper import ShellAPIWrapper


class TestShellReplAPIWrapper(TestCase):
    def test_run(self):
        api_wrapper = ShellAPIWrapper()
        command = """echo hello"""
        result = api_wrapper.run(command)
        print(result)
        self.assertEqual("hello\r\n", result)


class TestShellReplTool(TestCase):
    def test_run(self):
        tool = ShellTool()
        print(tool.description)
        command = """echo hello"""
        result = tool.run(command)
        print(result)
