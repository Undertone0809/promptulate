from promptulate.agents import ToolAgent
from promptulate.tools import Calculator, DuckDuckGoTool


def main():
    tools = [
        DuckDuckGoTool(),
        Calculator(),
    ]
    agent = ToolAgent(tools=tools)
    prompt = """Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"""  # noqa
    agent.run(prompt)


if __name__ == "__main__":
    main()
