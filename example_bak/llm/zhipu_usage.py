"""
This demo show how to use Zhipu model in promptulate.
"""

import os

import promptulate as pne

os.environ["ZHIPUAI_API_KEY"] = "xxxxxx"


def main():
    model_config = {"stream": True, "return_raw_response": True}
    ai = pne.AIChat(model="zhipu/glm-4", model_config=model_config)

    while True:
        prompt = input("[User Input] ")
        answer = ai.run(prompt)

        for chunk in answer:
            print(chunk.content)
            print(chunk.additional_kwargs)


if __name__ == "__main__":
    main()
