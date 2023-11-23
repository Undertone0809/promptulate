from promptulate.agents import ToolAgent
from promptulate.tools import Calculator, DuckDuckGoTool
from promptulate.utils.logger import enable_log

enable_log()


def main():
    tools = [
        DuckDuckGoTool(),
        Calculator(),
    ]
    agent = ToolAgent(tools)
    prompt = """Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"""  # noqa
    agent.run(prompt)


if __name__ == "__main__":
    main()
