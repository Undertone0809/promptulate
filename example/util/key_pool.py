from promptulate.llms import OpenAI
from promptulate.utils import export_openai_key_pool

keys = [
    {"model": "gpt-3.5-turbo", "key": "xxxxx"},
    {"model": "gpt-3.5-turbo", "key": "xxxxx"},
    {"model": "gpt-3.5-turbo", "key": "xxxxx"},
    {"model": "gpt-4.0", "key": "xxxxx"},
]

export_openai_key_pool(keys)
llm = OpenAI()
for i in range(50):
    print(llm("你好"))
