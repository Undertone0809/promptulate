import re
from time import sleep


def sleep_tool(sleep_time: str) -> str:
    """Make agent sleep for a specified number of seconds.
       Input is a number. eg: Sleep for 5s and enter 5
    Args:
        sleep_time: Sleep for sleep_time

    Returns:
        str: Agent slept seconds.
    """
    sleep_time = re.findall(r"\d+", sleep_time)
    sleep(int(sleep_time[0]))
    return f"Agent slept for {sleep_time[0]} seconds."
