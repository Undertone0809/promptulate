import warnings
from ctypes import Union
import sys
from typing import List

from pydantic import Field

from promptulate.tools import BaseTool
from promptulate.tools.shell.api_wrapper import ShellAPIWrapper


def _get_platform() -> str:
    """Get platform."""
    system = sys.platform
    if system == "Darwin":
        return "MacOS"
    return system


class ShellTool(BaseTool):
    """Tool to run shell commands."""

    name: str = "terminal"
    """Name of tool."""

    description: str = f"Run shell commands on this {_get_platform()} machine."
    """Description of tool."""

    api_wrapper: ShellAPIWrapper = Field(default_factory=ShellAPIWrapper)

    def _run(
        self,
        command: str,
    ) -> str:
        warnings.warn(
            "The shell tool has no safeguards by default. Use at your own risk."
        )
        """Run commands and return final output."""
        return self.api_wrapper.run(command)
