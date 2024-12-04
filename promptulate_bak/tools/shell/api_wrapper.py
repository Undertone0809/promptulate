import subprocess


class ShellAPIWrapper:
    """Simulates a standalone shell"""

    @staticmethod
    def run(command: str) -> str:
        """
        Runs a command in a subprocess and returns
        the output.

        Args:
            command: The command to run
        """
        try:
            output = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            ).stdout.decode()
        except subprocess.CalledProcessError as e:
            output = repr(e)
        return output
