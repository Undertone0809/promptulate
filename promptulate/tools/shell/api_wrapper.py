import os
import sys
from io import StringIO


class ShellAPIWrapper:
    """Simulates a standalone shell"""

    @staticmethod
    def run(command: str) -> str:
        try:
            result = os.popen(command)
            output = result.read()
            result.close()
        except Exception as e:
            output = repr(e)
        return output
