from unittest import TestCase

from promptulate.tools.shell import ShellTool


class TestPythonReplTool(TestCase):
    def test_run(self):
        tool = ShellTool()
        print(tool.description)
        command = """ls"""
        result = tool.run(command)
        print(result)
