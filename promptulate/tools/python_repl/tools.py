import sys
from io import StringIO
from typing import Dict, Optional

from promptulate.pydantic_v1 import BaseModel, Field
from promptulate.tools.base import Tool


class Parameters(BaseModel):
    command: str = Field(
        ...,
        description="The python command to be executed",
        example="print('hello world')",
    )


class PythonREPLTool(Tool):
    """A tool for running python code in a REPL."""

    name: str = "Python_REPL"
    description: str = (
        "A Python shell. Use this to execute python commands. "
        "Input should be a valid python command. "
        "If you want to see the output of a value, you should print it out "
        "with `print(...)`."
    )
    parameters: BaseModel = Parameters

    def __init__(
        self,
        _globals: Optional[Dict] = None,
        _locals: Optional[Dict] = None,
        *args,
        **kwargs,
    ):
        self.globals = _globals or {}
        self.locals = _locals or {}

        super().__init__(*args, **kwargs)

    def _run(self, command: str, *args, **kwargs) -> str:
        """Run command with own globals/locals and returns anything printed."""
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            exec(command, self.globals, self.locals)
            sys.stdout = old_stdout
            output = mystdout.getvalue()
        except Exception as e:
            sys.stdout = old_stdout
            output = repr(e)
        return output
