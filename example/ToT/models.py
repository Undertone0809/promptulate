import os
import pne

api_key = os.getenv("DEEPSEEK_API_KEY", "")
if api_key != "":
    api_key = api_key
else:
    print("Warning: API_KEY is not set")

# api_base = os.getenv("OPENAI_API_BASE", "")
# if api_base != "":
#     print("Warning: OPENAI_API_BASE is set to {}".format(api_base))
#     api_base = api_base


def completions_with_backoff(**kwargs):
    response = pne.chat(**kwargs)
    print(f"1111{response}")
    return response


def gpt(prompt, model="deepseek/deepseek-chat", temperature=0.7, max_tokens=1000, n=1,
        stop=None) -> list:
    messages = [{"role": "user", "content": prompt}]
    return chatgpt(messages, model=model, temperature=temperature,
                   max_tokens=max_tokens, n=n, stop=stop)


def chatgpt(messages, model="deepseek/deepseek-chat", temperature=0.7, max_tokens=1000, n=1,
            stop=None) -> list:
    outputs = []
    while n > 0:
        cnt = min(n, 20)
        n -= cnt
        res = completions_with_backoff(model=model, messages=messages,
                                       temperature=temperature, max_tokens=max_tokens,
                                       n=cnt, stop=stop)
        print(f"222res{res}")

        # for choice in res.choices:
        #     print(f"3333content{choice.message.content}")

        outputs.extend([res])
        print(f"6666outputs{outputs}")
    return outputs

