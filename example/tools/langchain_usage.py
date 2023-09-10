from langchain.tools import DuckDuckGoSearchRun

from promptulate.agents import ToolAgent
from promptulate.tools import LangchainTool


def example():
    tools = [LangchainTool(DuckDuckGoSearchRun())]
    agent = ToolAgent(tools)
    agent.run("Shanghai weather tomorrow")


if __name__ == "__main__":
    example()
