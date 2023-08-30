import os
import sys
from io import StringIO
from typing import Dict, Optional
from pydantic import BaseModel, Field


class ShellAPIWrapper(BaseModel):
    """Simulates a standalone shell"""
    @staticmethod
    def run(command: str) -> str:
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            os.system(command)
            sys.stdout = old_stdout
            output = mystdout.getvalue()
        except Exception as e:
            sys.stdout = old_stdout
            output = repr(e)
        return output
