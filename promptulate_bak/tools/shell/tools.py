import sys
import warnings

from promptulate.tools.base import Tool
from promptulate.tools.shell.api_wrapper import ShellAPIWrapper


def _get_platform() -> str:
    """Get platform."""
    system = sys.platform
    if system == "Darwin":
        return "MacOS"
    return system


class ShellTool(Tool):
    """Tool to run shell commands."""

    name: str = "terminal"
    description: str = f"Run shell commands on this {_get_platform()} machine."

    def _run(self, command: str) -> str:
        warnings.warn(
            "The shell tool has no safeguards by default. Use at your own risk."
        )
        """Run commands and return final output."""
        return ShellAPIWrapper.run(command)
