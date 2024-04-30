# LLMFactory

> We recommend use pne.chat() to create your LLM application after v1.16.0. pne.ChatOpenAI, pne.ZhipuAI and pne.Qianfan... will be deprecated in the future. Now we use LLMFactory to create any LLM.

## Features

- LLMFactory is a factory class to create LLM model. 
- It is the basic component of the pne.chat model driver for creating LLM models.
- It integrates the ability of [litellm](https://github.com/BerriAI/litellm). It means you can call all LLM APIs using the OpenAI format. Use Bedrock, Azure, OpenAI, Cohere, Anthropic, Ollama, Sagemaker, HuggingFace, Replicate (100+ LLMs). Now let's take a look at how to use it.

The following example show how to create an OpenAI model and chat.


```python
import os

import promptulate as pne

os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
model = pne.LLMFactory.build(model_name="gpt-3.5-turbo", model_config={
    "temperature": 0.5,
})
```


```python
resp: str = model("hello, how are you?")
print(resp)
```

    Hello! I'm just a computer program, so I don't have feelings, but I'm here and ready to help you. How can I assist you today?
    

## What's different between LLMFactory and pne.chat() ? 

LLMFactory is the basic component of the pne.chat model driver for creating LLM models. So at most time, you don't need to use LLMFactory directly. If you are developing a chatbot, you need to use pne.chat() to chat and make a structure of response. Eg:

```python
from typing import List
import promptulate as pne
from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    provinces: List[str] = Field(description="All provinces in China")


response: LLMResponse = pne.chat(
    messages="Please tell me all provinces in China.",
    output_schema=LLMResponse,
    model="gpt-4-1106-preview"
)
print(response.provinces)
```

pne.chat() covers 90% of development scenarios, so we recommend using pne.chat() if there are no special needs.

- If you want to use OpenAI, HuggingFace, Bedrock, Azure, Cohere, Anthropic, Ollama, Sagemaker, Replicate, etc., please use pne.chat() directly. It's a simple and easy way to chat.
- If you want to use a custom LLM model, please read [CustomLLM](https://undertone0809.github.io/promptulate/#/modules/llm/custom_llm?id=custom-llm)

## Why show LLMFactory here?

We just want you know the basic component of the pne.chat model driver for creating LLM models. If you are a developer, you can learn something from this design. If you are a user, you can know how pne.chat works.
