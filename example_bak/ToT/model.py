import os

import promptulate as pne

api_key = os.getenv("API_KEY", "")
if api_key != "":
    api_key = api_key
else:
    print("Warning: API_KEY is not set")


def gpt(
    prompt,
    model="deepseek/deepseek-chat",
    temperature=0.7,
    max_tokens=1000,
    n=1,
    stop=None,
) -> list:
    messages = [{"role": "user", "content": prompt}]
    return chatgpt(
        messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        n=n,
        stop=stop,
    )


def chatgpt(
    messages,
    model="deepseek/deepseek-chat",
    temperature=0.7,
    max_tokens=1000,
    n=1,
    stop=None,
) -> list:
    outputs = []
    while n > 0:
        cnt = min(n, 20)
        n -= cnt
        res = pne.chat(
            model=model,
            model_config={"api_key": api_key},
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            n=cnt,
            stop=stop,
        )

        outputs.extend([res])
    return outputs
