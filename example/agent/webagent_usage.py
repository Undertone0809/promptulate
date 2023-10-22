from promptulate.agents import WebAgent


def main():
    agent = WebAgent()
    response = agent.run("What is the temperature tomorrow in Shanghai")
    print(response)


if __name__ == "__main__":
    main()
