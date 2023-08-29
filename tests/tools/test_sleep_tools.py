from unittest import TestCase

from promptulate import enable_log
from promptulate.tools import SleepTool
from promptulate.utils import get_logger

enable_log()
logger = get_logger()


class TestSleepTool(TestCase):
    def test_run(self):
        tool = SleepTool()
        seconds = 10
        result = tool.run(seconds)
        print(result)

