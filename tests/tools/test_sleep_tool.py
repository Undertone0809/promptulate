import time
from unittest import TestCase

from promptulate import enable_log
from promptulate.tools import SleepTool

enable_log()


class TestSleepTool(TestCase):
    def test_run(self):
        tool = SleepTool()
        seconds = "1s"
        start_time = time.time()
        tool.run(seconds)
        duration = time.time() - start_time
        self.assertAlmostEqual(1, duration, delta=0.1)
