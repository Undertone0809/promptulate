# Custom LLM
This guide details the process of creating a custom Language Model (LLM) wrapper for use with Promptulate. To integrate your own LLM or an alternative to the supported wrappers, your custom LLM class must implement two essential methods.

The following example shows how to create a custom LLM and use LLM to output a response to a user query. Here we wrap the OpenAI API to create a custom LLM.



```python
import os

from openai import OpenAI
from pydantic import Field

from promptulate.llms.base import BaseLLM
from promptulate.schema import MessageSet, AssistantMessage

os.environ["OPENAI_API_KEY"] = "your key"


class MyLLM(BaseLLM):
    model: str = "gpt-3.5-turbo"
    client: OpenAI = Field(default_factory=OpenAI)

    def _predict(self, messages: MessageSet, *args, **kwargs) -> AssistantMessage:
        resp = self.client.chat.completions.create(model=self.model, messages=messages.listdict_messages, temperature=0.0)
        return AssistantMessage(content=resp.choices[0].message.content, additional_kwargs=resp)
```

If you custom a LLM class, you need to implement the following methods:

1. `_predict` Method: This method is used to make predictions using your LLM. It should return an `AssistantMessage` object.
2. `__call__` Method: This method is used to interact with your LLM as if it were a function. It should return a string.


## Using Your Custom LLM

You can interact with your custom LLM in two ways:

1. Using the __call__ Method:
This allows you to invoke your LLM as if it were a function:


```python
llm = MyLLM()
resp: str = llm("How is everything going?")
print(resp)
```

    This is call reply
    

2. Using the `predict` Method:

This method is used to get a structured response from your LLM:


```python
from promptulate.schema import AssistantMessage, MessageSet, SystemMessage

messages = MessageSet([
    SystemMessage(content="You are a helpful assistant.")
])

llm = MyLLM()
resp_message: AssistantMessage = llm.predict(messages)
print(resp_message.content)
```

    This is predict reply
    
