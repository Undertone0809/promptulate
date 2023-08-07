# FQA

## OpenAI key遇到限速问题怎么办？

`promptulate`为OpenAI进行特别优化，构建了Key池，如果你使用的是`GPT3.5`
5美元的账号，一定会遇到限速的问题，这个时候，如果你有一堆Key，就可以很好的解决这个问题。`promptulate`的LRU
KEY轮询机制巧妙的解决了限速的问题，你可以使用LLM随意地进行提问（前提是你有够多的key）。此外，如果你既有`GPT4`和`GPT3.5`
的KEY，KEY池也可以不同模型的KEY调度，你可以按照下面的方式将key导入到你的key池中。

```python
from promptulate.llms import ChatOpenAI
from promptulate.utils import export_openai_key_pool

keys = [
    {"model": "gpt-3.5-turbo", "key": "xxxxx"},
    {"model": "gpt-3.5-turbo", "key": "xxxxx"},
    {"model": "gpt-3.5-turbo", "key": "xxxxx"},
    {"model": "gpt-4", "key": "xxxxx"},
]

export_openai_key_pool(keys)

llm = ChatOpenAI()
for i in range(10):
    llm("你好")
```

## 使用Agent、tool等复杂工具的时候无法看到中间过程？

你可以使用[Hook系统](modules/hook.md#what-is-hook)构建一个定制化的中间过程监测系统。


