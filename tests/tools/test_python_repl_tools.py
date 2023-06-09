from unittest import TestCase

from promptulate.utils.logger import get_logger, enable_log
from promptulate.tools.python_repl.api_wrapper import PythonREPLAPIWrapper
from promptulate.tools.python_repl.tools import PythonREPLTool

enable_log()
logger = get_logger()


class TestPythonReplAPIWrapper(TestCase):
    def test_run(self):
        api_wrapper = PythonREPLAPIWrapper()
        command = """print("helloworld")"""
        result = api_wrapper.run(command)
        self.assertEqual("helloworld\n", result)


class TestPythonReplTool(TestCase):
    def test_run(self):
        api_wrapper = PythonREPLTool()
        command = """print("helloworld")"""
        result = api_wrapper.run(command)
        self.assertEqual("helloworld\n", result)
