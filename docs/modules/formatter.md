# 简介

在某些时候，你可能想要让 LLM 输出指令类型格式的数据，如 JSON 类型的数据， Promptulate 为 LLM 的输出提供了输出格式化器（OutputFormatter），你可以轻易让 LLM 返回指定格式的数据。

## llm with OutputFormatter

下面的示例展示了如何在 llm 模块中使用 OutputFormatter。

```python
from pydantic import BaseModel, Field

from promptulate.output_formatter import OutputFormatter
from promptulate.llms import ChatOpenAI


class Response(BaseModel):
    city: str = Field(description="City name")
    temperature: float = Field(description="Temperature in Celsius")


def main():
    llm = ChatOpenAI()
    formatter = OutputFormatter(Response)

    prompt = f"Shanghai today temperature is 28.2 degrees.\n{formatter.get_formatted_instructions()}"
    llm_output = llm(prompt)
    print(llm_output)

    response: Response = formatter.formatting_result(llm_output)
    print(response)


if __name__ == "__main__":
    main()

```

上面的示例中定义了 Response 类，里面的属性声明表示预期的LLM需要返回的数据。 如果你将 OutputFormatter 搭配 llm 使用，则需要在 prompt 中添加你的输出要求，以便 llm 按照你的格式要求进行输出。

在 llm 输出之后，我们使用 formatter.formatting_result 对 llm 的输出进行解析，最后实例化成 Response 类。

输出结果如下所示：

![img.png](../images/output_formatter_llm_output.png)

可以看到，llm 实际上是输出的内容是 json schema 格式的数据，promptulate 将其转换为 Response 类并实例化。

如果你希望返回的结果是一个数据，下面是一个示例。

```python
from typing import List

from pydantic import BaseModel, Field


from promptulate.output_formatter import OutputFormatter
from promptulate.llms import ChatOpenAI


class Response(BaseModel):
    provinces: List[str] = Field(description="List of provinces name")


def main():
    llm = ChatOpenAI()
    formatter = OutputFormatter(Response)

    prompt = f"Please tell me the names of provinces in China.\n{formatter.get_formatted_instructions()}"
    llm_output = llm(prompt)
    response: Response = formatter.formatting_result(llm_output)
    print(response)


if __name__ == "__main__":
    main()

```

返回结果：

```
provinces=['Anhui', 'Fujian', 'Gansu', 'Guangdong', 'Guizhou', 'Hainan', 'Hebei', 'Heilongjiang', 'Henan', 'Hubei', 'Hunan', 'Jiangsu', 'Jiangxi', 'Jilin', 'Liaoning', 'Qinghai', 'Shaanxi', 'Shandong', 'Shanxi', 'Sichuan', 'Yunnan', 'Zhejiang', 'Guangxi', 'Nei Mongol', 'Ningxia', 'Xinjiang', 'Xizang', 'Beijing', 'Chongqing', 'Shanghai', 'Tianjin', 'Hong Kong', 'Macau']
```

## Agent with OutputFormatter

在 Agent 上使用 OutputFormatter 是一件很轻松的事情，因为你并不需要显式的定义一个 OutputFormatter，在 agent.run() 的时候传入你预期的返回格式即可，下面的示例展示了 OutputFormatter 在 Agent 中的使用方式。

```python
from pydantic import BaseModel, Field

from promptulate.agents import WebAgent


class Response(BaseModel):
    city: str = Field(description="City name")
    temperature: float = Field(description="Temperature in Celsius")


def main():
    agent = WebAgent()
    prompt = f"What is the temperature in Shanghai tomorrow?"
    response: Response = agent.run(prompt=prompt, output_schema=Response)
    print(response)


if __name__ == "__main__":
    main()
```

![img.png](../images/output_formatter_webagent_output.png)