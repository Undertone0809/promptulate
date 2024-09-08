# Introduction

At times, you might want LLM to output data in a specific format, such as JSON or List types. Promptulate provides an output formatter (OutputFormatter) for LLM's output, allowing you to easily get LLM to return data in a specified format.

## Usage in LLM

The following example demonstrates how to use OutputFormatter in the llm module to get all provinces in China and ensure llm strictly returns a list, writing the provinces into the list.

```python
from typing import List
from promptulate.output_formatter import OutputFormatter
from promptulate.llms import ChatOpenAI
from pydantic import BaseModel, Field

class LLMResponse(BaseModel):
    provinces: List[str] = Field(description="All provinces in China")

def main():
    llm = ChatOpenAI()
    formatter = OutputFormatter(LLMResponse)

    prompt = f"Please tell me all provinces in China. \n{formatter.get_formatted_instructions()}"
    llm_output = llm(prompt)
    print(llm_output)

    response: LLMResponse = formatter.formatting_result(llm_output)
    print(response.provinces)


if __name__ == "__main__":
    main()
```

```
['Anhui', 'Fujian', 'Gansu', 'Guangdong', 'Guizhou', 'Hainan', 'Hebei', 'Heilongjiang', 'Henan', 'Hubei', 'Hunan', 'Jiangsu', 'Jiangxi', 'Jilin', 'Liaoning', 'Qinghai', 'Shaanxi', 'Shandong', 'Shanxi', 'Sichuan', 'Yunnan', 'Zhejiang', 'Guangxi', 'Nei Mongol', 'Ningxia', 'Xinjiang', 'Xizang', 'Beijing', 'Chongqing', 'Shanghai', 'Tianjin', 'Hong Kong', 'Macau']
```

Have LLM tell a joke and strictly return data of type LLMResponse.

```python
from pydantic import BaseModel, Field

from promptulate.output_formatter import OutputFormatter
from promptulate.llms import ChatOpenAI


class LLMResponse(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")


def main():
    llm = ChatOpenAI()
    formatter = OutputFormatter(LLMResponse)

    question = "Tell me a joke."
    prompt = question + "\n" + formatter.get_formatted_instructions()
    llm_output = llm(prompt)
    print(llm_output)

    response: LLMResponse = formatter.formatting_result(llm_output)
    print(response)


if __name__ == "__main__":
    main()

```

The output is as follows:

```python
LLMResponse(setup='Why did the chicken cross the road?', punchline='To get to the other side!')
```

In the example above, the LLMResponse class is defined, and the property declarations indicate the expected data type that the LLM needs to return. Essentially, it adds formatter.get_formatted_instructions() to the prompt, telling the LLM the output format it should follow.

After the llm output, we use formatter.formatting_result to parse the llm output, and finally instantiate it into an LLMResponse class.

The llm output is actually in json schema format, and pne converts it into an LLMResponse class and instantiates it.

Sometimes, the LLM output may not be very accurate, and providing the LLM with some examples (few-shot) can increase its output accuracy. The following example demonstrates how to add examples to achieve this effect.

```python
from pydantic import BaseModel, Field

from promptulate.output_formatter import OutputFormatter
from promptulate.llms import ChatOpenAI


class Response(BaseModel):
    city: str = Field(description="City name")
    temperature: float = Field(description="Temperature in Celsius")


def main():
    llm = ChatOpenAI()
    examples = [
        Response(city="Shanghai", temperature=25),
        Response(city="Beijing", temperature=30),
    ]
    formatter = OutputFormatter(pydantic_obj=Response, examples=examples)

    prompt = f"Shanghai today temperature is 28.2 degrees.\n{formatter.get_formatted_instructions()}"
    llm_output = llm(prompt)
    print(llm_output)

    response: Response = formatter.formatting_result(llm_output)
    print(response)


if __name__ == "__main__":
    main()

```

## Usage in Agent

Using OutputFormatter in Agent is a straightforward process, as you do not need to explicitly define an OutputFormatter. Instead, you can pass your expected return format when calling agent.run(), as demonstrated in the following example.

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

![img.png](/images/output_formatter_webagent_output.png)

If you also want to include examples in Agent, you can pass them as parameters using the `agent.run(prompt=prompt, output_schema=Response)` method.

## Usage in pne.chat()

Refer to [pne.chat usage](/use_cases/chat_usage.md)
