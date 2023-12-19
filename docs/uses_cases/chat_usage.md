# Chat
`pne.chat()` is an awesome function, you can use **tools, formatted output, different llm** in this function. 

`pne.chat()` integrate the ability of [litellm](https://github.com/BerriAI/litellm). It means you can call all LLM APIs using the OpenAI format. Use Bedrock, Azure, OpenAI, Cohere, Anthropic, Ollama, Sagemaker, HuggingFace, Replicate (100+ LLMs). Now let's take a look at how to use it.

## Chat like OpenAI
You can use `pne.chat()` to chat like openai. OpenAI chat API document: [https://platform.openai.com/docs/api-reference/chat](https://platform.openai.com/docs/api-reference/chat)


```python
import promptulate as pne

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who are you?"},
]
response: str = pne.chat(messages=messages)
print(response)
```

    I am a helpful assistant designed to assist you with any questions or tasks you may have. How can I assist you today?
    

Moreover, you can only pass a string to `pne.chat()`, it will automatically convert it to the OpenAI format.


```python
import promptulate as pne

response = pne.chat(
    messages="When is your knowledge up to?",
    model="gpt-4-1106-preview"
)
print(response)
```

    My knowledge is up to date as of March 2021. Any events or developments occurring after that date would not be included in my responses. If you're asking for any recent information or updates, I recommend checking the latest sources as my information might not be current.
    

## Return type
`pne.chat()` return string by default.

If you want to do more complex thing, metadata is important. You can use `return_raw_response=True` to get the raw response wrapped by `pne.AssistantMessage`. Metadata will store in `pne.AssistantMessage.additional_kwargs`.


> About `pne.AssistantMessage`, you can see [here](modules/schema.md#Schema).


```python
import promptulate as pne

response: pne.AssistantMessage = pne.chat("Who are you?", return_raw_response=True)
print(response.content)  # response string
print(response.additional_kwargs)  # metadata
```

    I am an AI assistant here to help you with any questions or tasks you may have. How can I assist you today?
    {'id': 'chatcmpl-8UK0tfwlkixWyaxKJ2XWNGMVGFPo0', 'choices': [{'finish_reason': 'stop', 'index': 0, 'message': {'content': 'I am an AI assistant here to help you with any questions or tasks you may have. How can I assist you today?', 'role': 'assistant'}}], 'created': 1702237461, 'model': 'gpt-3.5-turbo-0613', 'object': 'chat.completion', 'system_fingerprint': None, 'usage': {'completion_tokens': 25, 'prompt_tokens': 20, 'total_tokens': 45}, '_response_ms': 2492.372}
    

## Using any model
You can call 100+ LLMs using the same Input/Output Format(OpenAI format) in `pne.chat()`. The follow example show how to use `claude-2`, make sure you have key ANTHROPIC_API_KEY.


```python
import os
import promptulate as pne

os.environ["ANTHROPIC_API_KEY"] = "your-api-key"

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who are you?"},
]
response = pne.chat(messages=messages, model="claude-2")
print(response)
```

### HuggingFace
This example show how to use HuggingFace LLMs in `pne.chat()`. Make sure you have key HUGGINGFACE_API_KEY.


```python
import os
import promptulate as pne

os.environ["HUGGINGFACE_API_KEY"] = "your-api-key"

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who are you?"},
]
response = pne.chat(
    messages=messages,
    model="huggingface/WizardLM/WizardCoder-Python-34B-V1.0",
    api_base="https://my-endpoint.huggingface.cloud"
)
print(response)
```

### Azure OpenAI
This example show how to use Azure OpenAI LLMs in `pne.chat()`. Make sure you have relevant key.


```python
import os
import promptulate as pne

os.environ["AZURE_API_KEY"] = ""
os.environ["AZURE_API_BASE"] = ""
os.environ["AZURE_API_VERSION"] = ""

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who are you?"},
]
response = pne.chat(
    messages=messages,
    model="azure/<your_deployment_name>",
)
print(response)
```

### Custom LLM
You can use `pne.llms.BaseLLM` to create your own LLM. The follow example show how to create a custom LLM and use it in `pne.chat()`.


```python
import promptulate as pne
from typing import Optional


class CustomLLM(pne.llms.BaseLLM):
    """
    This is a custom LLM, here we wrap OpenAI API to implement it.
    """
    llm_type: str = "custom_llm"
    llm = pne.ChatOpenAI()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _predict(self, prompts: pne.MessageSet, *args, **kwargs) -> Optional[
        pne.AssistantMessage]:
        return self.llm.predict(prompts, *args, **kwargs)

    def __call__(self, prompt: str, *args, **kwargs):
        return self.llm(prompt, *args, **kwargs)


messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who are you?"},
]
response = pne.chat(
    messages=messages,
    custom_llm=CustomLLM(),
)
print(response)
```

    I am a helpful assistant designed to provide information, answer questions, and assist with various tasks. How can I assist you today?
    

## Output Format
The output of LLM has strong uncertainty. Pne provide the ability to get a formatted object by LLM. The following example shows that if LLM strictly returns you an array listing all provinces in China. 


```python
from typing import List
import promptulate as pne
from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    provinces: List[str] = Field(description="All provinces in China")


response: LLMResponse = pne.chat(
    messages="Please tell me all provinces in China.",
    output_schema=LLMResponse
)
print(response.provinces)
```

    ['Anhui', 'Beijing', 'Chongqing', 'Fujian', 'Gansu', 'Guangdong', 'Guangxi', 'Guizhou', 'Hainan', 'Hebei', 'Heilongjiang', 'Henan', 'Hubei', 'Hunan', 'Jiangsu', 'Jiangxi', 'Jilin', 'Liaoning', 'Ningxia', 'Qinghai', 'Shaanxi', 'Shandong', 'Shanghai', 'Shanxi', 'Sichuan', 'Tianjin', 'Tibet', 'Xinjiang', 'Yunnan', 'Zhejiang']
    

As you can see, `pne.chat()` return a LLMResponse object. The value of provinces is all provinces in China. If you are building a complex Agent project, formatting output is a necessary measure to improve system robustness. The follow example show how to use `pne.chat()` to get the weather in Shanghai tomorrow.


```python
from datetime import datetime
import promptulate as pne
from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    city_name: str = Field(description="city name")
    queried_date: datetime = Field(description="date of timestamp")


current_time = datetime.now()
response: LLMResponse = pne.chat(
    messages=f"What's the temperature in Shanghai tomorrow? {current_time}",
    output_schema=LLMResponse
)
print(response)
print(response.city_name)
print(response.queried_date)
```

    city_name='Shanghai' queried_date=datetime.datetime(2023, 12, 11, 13, 2, 35, 722348, tzinfo=datetime.timezone.utc)
    Shanghai
    2023-12-11 13:02:35.722348+00:00
    

## Using tool
You can use `pne.tools` to add some tools to chat. Now we have `pne.tools.duckduckgo.DuckDuckGoTool()`, it can help you to get the answer from DuckDuckGo.

> ⚠ There are some tiny bugs if you use tools, we are fixing it. We are ready to release the first version of `pne.tools` in the next version.


```python
tools = [pne.tools.duckduckgo.DuckDuckGoTool()]
response = pne.chat(
    messages="What's the temperature in Shanghai tomorrow?",
    tools=tools
)
print(response)
```

## Streaming
`pne.chat()` support streaming, you can use `pne.chat()` to chat with your assistant in real time.


```python
import promptulate as pne

response = pne.chat("Who are you?", stream=True)

for chuck in response:
    print(chuck)
```

    I
     am
     a
     virtual
     assistant
     designed
     to
     provide
     information
     and
     assistance
    .
     Is
     there
     something
     specific
     you
     would
     like
     help
     with
    ?
    

`pne.chat()` by stream will return an iterator, you can use `next()` or `for each` to get the response.

If you want to get metadata, you can use `return_raw_response=True` to get the raw response wrapped by `pne.AssistantMessage`. Metadata will store in `pne.AssistantMessage.additional_kwargs`.


```python
import promptulate as pne

response = pne.chat("Who are you?", stream=True, return_raw_response=True)

for chuck in response:
    print(chuck.content)
    print(chuck.additional_kwargs)
```

## Retrieve && RAG
**RAG(Retrieval-Augmented Generation)** is a important data retrieve method. You can use `pne.chat()` to retrieve data from your database.

You can use lots of methods to retrieve data, pne plan to support the following source:
- [ ] VectorStore Retrieval
- [ ] Relational Database Retrieval
- [ ] Web Search Retrieval
- [ ] Knowledge Graph Retrieval
- [ ] Document Retrieval
    - [ ] PDF Retrieval
    - [ ] Docx Retrieval
    - [ ] CSV/Excel Retrieval
- [ ] Image Retrieval

🌟**We are currently building infrastructure, please stay tuned!**
