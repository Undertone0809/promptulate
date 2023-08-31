from promptulate.agents import WebAgent
from promptulate.llms import ErnieBot


def main():
    llm = ErnieBot()
    agent = WebAgent(llm=llm)
    agent.run("南昌明天多少度？")


if __name__ == "__main__":
    main()
