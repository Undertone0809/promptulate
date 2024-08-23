"""A Agent with duckduckgo search"""

from promptulate.agents import ToolAgent
from promptulate.tools import DuckDuckGoTool


def main():
    while True:
        tools = [DuckDuckGoTool()]
        prompt = input("Input your question:")
        agent = ToolAgent(tools=tools)
        print(agent.run(prompt))


if __name__ == "__main__":
    main()
