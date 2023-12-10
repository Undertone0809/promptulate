import promptulate as pne


def main():
    agent = pne.WebAgent()
    response = agent.run("What is the temperature tomorrow in Shanghai")
    print(response)


if __name__ == "__main__":
    main()
