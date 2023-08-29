from promptulate.agents import ToolAgent
from promptulate.tools import (
    DuckDuckGoTool,
    Calculator,
    SleepTool
)
from promptulate.utils.logger import enable_log

enable_log()


def main():
    tools = [
        DuckDuckGoTool(),
        Calculator(),
        SleepTool()
    ]
    agent = ToolAgent(tools)
    prompt = """stop 5s"""
    agent.run(prompt)


if __name__ == "__main__":
    main()
