# Custom LLM
This guide details the process of creating a custom Language Model (LLM) wrapper for use with LangChain. To integrate your own LLM or an alternative to the supported wrappers, your custom LLM class must implement two essential methods.

Below is a template for a custom LLM class:



```python
from promptulate.llms.base import BaseLLM
from promptulate.schema import MessageSet, AssistantMessage


class MyLLM(BaseLLM):
    def _predict(self, messages: MessageSet, *args, **kwargs) -> AssistantMessage:
        return AssistantMessage(content="This is predict reply")

    def __call__(self, instruction: str, *args, **kwargs):
        return "This is call reply"
```

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
    
