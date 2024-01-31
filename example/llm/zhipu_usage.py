import os

import promptulate as pne

os.environ["ZHIPUAI_API_KEY"] = "xxxxxx"


def main():
    model_config = {"stream": True, "return_raw_response": True}
    llm = pne.llms.ZhiPu(model_config=model_config)
    while True:
        prompt = input("[User Input] ")
        answer = llm(prompt)
        for chunk in answer:
            print(chunk.content)
            print(chunk.additional_kwargs)


if __name__ == "__main__":
    main()
