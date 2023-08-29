from promptulate.agents import ToolAgent
from promptulate.llms import ErnieBot
from promptulate.tools import (
    DuckDuckGoTool,
    Calculator,
)
from promptulate.utils.logger import enable_log

enable_log()


def main():
    tools = [
        DuckDuckGoTool(),
        Calculator(),
    ]
    llm = ErnieBot()
    agent = ToolAgent(tools=tools,llm=llm)
    prompt = """Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"""
    agent.run(prompt)


if __name__ == "__main__":
    main()
