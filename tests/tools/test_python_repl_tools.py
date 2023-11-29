from unittest import TestCase

from promptulate.tools.python_repl.api_wrapper import PythonREPLAPIWrapper
from promptulate.tools.python_repl.tools import PythonREPLTool
from promptulate.utils.logger import enable_log

enable_log()


class TestPythonReplAPIWrapper(TestCase):
    def test_run(self):
        api_wrapper = PythonREPLAPIWrapper()
        command = """print("helloworld")"""
        result = api_wrapper.run(command)
        self.assertEqual("helloworld\n", result)


class TestPythonReplTool(TestCase):
    def test_run(self):
        tool = PythonREPLTool()
        command = """print(16.5 ** 0.43)"""
        result = tool.run(command)
        print(result)
