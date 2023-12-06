import os

import promptulate as pne

os.environ["ERNIE_API_KEY"] = "your api key"
os.environ["ERNIE_API_SECRET"] = "your secret key"


def main():
    llm = pne.llms.ErnieBot()
    while True:
        prompt = input("[User Input] ")
        answer = llm(prompt)
        print(answer)


if __name__ == "__main__":
    main()
