from unittest import TestCase

from promptulate.tools import Calculator
from promptulate.utils.logger import enable_log

enable_log()


class TestCalculator(TestCase):
    def test_run(self):
        calculator = Calculator()
        result = calculator.run("16.5^0.43")
        print(result)
