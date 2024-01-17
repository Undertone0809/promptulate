import os

import promptulate as pne

os.environ["QIANFAN_ACCESS_KEY"] = "xxxxxx"
os.environ["QIANFAN_SECRET_KEY"] = "xxxxxx"


def main():
    llm = pne.llms.QianFan(
        stream=True, model="ERNIE-Bot-turbo", return_raw_response=True
    )
    while True:
        prompt = input("[User Input] ")
        answer = llm(prompt)
        for chuck in answer:
            print(chuck.content)
            print(chuck.additional_kwargs)


if __name__ == "__main__":
    main()
