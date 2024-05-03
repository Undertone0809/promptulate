import promptulate as pne
from promptulate.tools import DuckDuckGoTool, calculator


def main():
    tools = [
        DuckDuckGoTool(),
        calculator,
    ]
    agent = pne.ToolAgent(tools=tools, llm=pne.ChatOpenAI(model="gpt-4-1106-preview"))
    prompt = """Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"""  # noqa
    agent.run(prompt)


if __name__ == "__main__":
    main()
