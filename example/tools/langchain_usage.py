from langchain.agents import load_tools

import promptulate as pne

if __name__ == "__main__":
    tools = load_tools(["arxiv"])
    agent = pne.ToolAgent(tools=tools)
    agent.run("What's the paper 1605.08386 about?")
