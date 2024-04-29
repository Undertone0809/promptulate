> All your need is a `pne.chat()` function. A powerful and easy-to-use function covers 90% of LLM application scenarios.

# Chat
`pne.chat()` is an awesome function, you can use **tools, formatted output, different llm** in this function. 

## Best Practice

Here are some tips for using `pne.chat()`. Even though pne provides many modules, in 90% of LLM application development scenarios, you only need to use the pne.chat () function, so you only need to start with chat to understand the use of pne, and when you need to use additional modules, you can learn more about the features and use of other modules.

`pne.chat()` integrate the ability of [litellm](https://github.com/BerriAI/litellm). It means you can call all LLM APIs using the OpenAI format. Use Bedrock, Azure, OpenAI, Cohere, Anthropic, Ollama, Sagemaker, HuggingFace, Replicate (100+ LLMs). Now let's take a look at how to use it.

## Chat like OpenAI
You can use `pne.chat()` to chat like openai. OpenAI chat API document: [https://platform.openai.com/docs/api-reference/chat](https://platform.openai.com/docs/api-reference/chat)


```python
import promptulate as pne

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who are you?"},
]
response: str = pne.chat(messages=messages, model="gpt-4-turbo")
print(response)
```

    I am a helpful assistant designed to assist you with any questions or tasks you may have. How can I assist you today?
    

Moreover, you can only pass a string to `pne.chat()`, it will automatically convert it to the OpenAI format.


```python
import promptulate as pne

response = pne.chat(
    messages="When is your knowledge up to?",
    model="gpt-4-turbo"
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

response: pne.AssistantMessage = pne.chat(messages="Who are you?", model="gpt-4-turbo",
                                          return_raw_response=True)
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
    model_config={"api_base": "https://my-endpoint.huggingface.cloud"}
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
from pydantic import BaseModel, Field
import promptulate as pne


class LLMResponse(BaseModel):
    provinces: List[str] = Field(description="All provinces in China")


resp: LLMResponse = pne.chat(
    messages="Please tell me all provinces in China.",
    output_schema=LLMResponse
)

print(resp)
```

    provinces=['Anhui', 'Fujian', 'Gansu', 'Guangdong', 'Guizhou', 'Hainan', 'Hebei', 'Heilongjiang', 'Henan', 'Hubei', 'Hunan', 'Jiangsu', 'Jiangxi', 'Jilin', 'Liaoning', 'Qinghai', 'Shaanxi', 'Shandong', 'Shanxi', 'Sichuan', 'Yunnan', 'Zhejiang', 'Guangxi', 'Inner Mongolia', 'Ningxia', 'Xinjiang', 'Tibet', 'Beijing', 'Chongqing', 'Shanghai', 'Tianjin', 'Hong Kong', 'Macau']
    


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
    messages=f"What's the temperature in Shanghai tomorrow? current time: {current_time}",
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

The Tool feature in `pne.chat()` allows the language model to use specialized tools to assist in providing answers. For instance, when the language model recognizes the need to obtain weather information, it can invoke a predefined function for this purpose.

This is facilitated by a ToolAgent, which operates within the ReAct framework. The [ReAct](https://react-lm.github.io/) framework endows the ToolAgent with the ability to reason, think, and execute tools.

To illustrate, if the language model needs to find out the weather forecast for Shanghai tomorrow, it can make use of the DuckDuckGoTool through the ToolAgent to retrieve this information.


```python
import promptulate as pne

websearch = pne.tools.DuckDuckGoTool()
response = pne.chat(
    messages="What's the temperature in Shanghai tomorrow?",
    tools=[websearch]
)
print(response)
```

    {"tool": {"tool_name": "web_search", "tool_params": {"query": "Weather Shanghai tomorrow"}}, "thought": "I will use the web_search tool to find the temperature in Shanghai tomorrow.", "final_answer": null}
    

## Custom Tool

Moreover, you can customize your function easily. The follow example show how to create a custom tool and use it in `pne.chat()`. Here we also we ddg websearch to wrap the function.


```python
import promptulate as pne


def websearch(query: str) -> str:
    """Search the web for the query.
    
    Args:
        query(str): The query word. 

    Returns:
        str: The search result.
    """
    return pne.tools.DuckDuckGoTool().run(query)


response = pne.chat(
    messages="What's the temperature in Shanghai tomorrow?",
    tools=[websearch]
)
print(response)
```

    [31;1m[1;3m[Agent] Tool Agent start...[0m
    [36;1m[1;3m[User instruction] What's the temperature in Shanghai tomorrow?[0m
    [33;1m[1;3m[Thought] I should use the websearch tool to find the weather forecast of Shanghai tomorrow.[0m
    [33;1m[1;3m[Action] websearch args: {'query': 'Shanghai weather forecast tomorrow'}[0m
    [33;1m[1;3m[Observation] 25° / 14°. 1.7 mm. 7 m/s. Open hourly forecast. Updated 18:30. How often is the weather forecast updated? Forecast as PDF Forecast as SVG. Shanghai Weather Forecast. Providing a local hourly Shanghai weather forecast of rain, sun, wind, humidity and temperature. The Long-range 12 day forecast also includes detail for Shanghai weather today. Live weather reports from Shanghai weather stations and weather warnings that include risk of thunder, high UV index and forecast gales. Everything you need to know about today's weather in Shanghai, Shanghai, China. High/Low, Precipitation Chances, Sunrise/Sunset, and today's Temperature History. 上海 (Shanghai) ☀ Weather forecast for 10 days, information from meteorological stations, webcams, sunrise and sunset, wind and precipitation maps for this place ... 00:00 tomorrow 01:00 tomorrow 02:00 tomorrow 03:00 tomorrow 04:00 tomorrow 05:00 tomorrow 06:00 tomorrow 07:00 tomorrow 08:00 tomorrow 09:00 tomorrow Shanghai 7 day weather forecast including weather warnings, temperature, rain, wind, visibility, humidity and UV[0m
    [32;1m[1;3m[Agent Result] The weather forecast for Shanghai tomorrow is 25° / 14° with 1.7 mm of rain and 7 m/s wind speed. The weather information is updated at 18:30 daily.[0m
    [38;5;200m[1;3m[Agent] Agent End.[0m
    The weather forecast for Shanghai tomorrow is 25° / 14° with 1.7 mm of rain and 7 m/s wind speed. The weather information is updated at 18:30 daily.
    

## chat with Plan-Execute-Reflect Agent

Additionally, you can enhance the capabilities of the ToolAgent by setting enable_plan=True, which activates its ability to handle more complex issues. In the pne framework, this action triggers the AssistantAgent, which can be thought of as a planning-capable ToolAgent. Upon receiving user instructions, the AssistantAgent proactively constructs a feasible plan, executes it, and then reflects on each action post-execution. If the outcome doesn't meet the expected results, the AssistantAgent will recalibrate and re-plan accordingly.

This example we need to solve the problem of "what is the hometown of the 2024 Australia open winner?" Here we can integrate the LangChain tools to solve the problem.

> pne support all LangChain Tools, you can see [here](/modules/tools/langchain_tool_usage?id=langchain-tool-usage). Of course, it is really easy to create your own tools - see documentation [here](https://undertone0809.github.io/promptulate/#/modules/tools/custom_tool_usage?id=custom-tool) on how to do that.

Firstly, we need to install necessary packages.
```bash
pip install langchain_community
```

We use [Tavily](https://app.tavily.com/) as a search engine, which is a powerful search engine that can search for information from the web. To use Tavily, you need to get an API key from Tavily.

```python
import os

os.environ["TAVILY_API_KEY"] = "your_tavily_api_key"
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
```


```python
from langchain_community.tools.tavily_search import TavilySearchResults

websearch = TavilySearchResults()
```


```python
import promptulate as pne

response = pne.chat(
    model="gpt-4-1106-preview",
    messages="What's the temperature in Shanghai tomorrow?",
    tools=[websearch],
    enable_plan=True
)
print(response)
```

[Agent] Assistant Agent start...
[User instruction] What's the temperature in Shanghai tomorrow?
[Plan] {"goals": ["Find out the temperature in Shanghai tomorrow."], "tasks": [{"task_id": 1, "description": "Open a web browser on your device.", "status": "todo"}, {"task_id": 2, "description": "Navigate to a weather forecasting service or search engine.", "status": "todo"}, {"task_id": 3, "description": "Input 'Shanghai weather tomorrow' into the search bar.", "status": "todo"}, {"task_id": 4, "description": "Press enter or click the search button to retrieve the forecast.", "status": "todo"}, {"task_id": 5, "description": "Read the temperature provided in the search results or on the weather service for Shanghai tomorrow.", "status": "todo"}], "next_task_id": 1}
[Agent] Tool Agent start...
[User instruction] Open a web browser on your device.
[Execute Result] {'thought': "The user seems to be asking for an action that is outside the scope of my capabilities. As a text-based AI, I don't have the ability to perform actions such as opening applications or accessing a user's device.", 'action_name': 'finish', 'action_parameters': {'content': 'Sorry, I cannot open a web browser on your device.'}}
[Execute] Execute End.
[Revised Plan] {"goals": ["Find out the temperature in Shanghai tomorrow."], "tasks": [{"task_id": 1, "description": "Open a web browser on your device.", "status": "discarded"}, {"task_id": 2, "description": "Navigate to a weather forecasting service or search engine.", "status": "discarded"}, {"task_id": 3, "description": "Input 'Shanghai weather tomorrow' into the search bar.", "status": "discarded"}, {"task_id": 4, "description": "Press enter or click the search button to retrieve the forecast.", "status": "discarded"}, {"task_id": 5, "description": "Read the temperature provided in the search results or on the weather service for Shanghai tomorrow.", "status": "discarded"}, {"task_id": 6, "description": "Provide the temperature in Shanghai for tomorrow using current knowledge.", "status": "todo"}], "next_task_id": 6}
[Agent] Tool Agent start...
[User instruction] Provide the temperature in Shanghai for tomorrow using current knowledge.
[Thought] I need to use a tool to find the temperature in Shanghai for tomorrow. Since the user is asking for information that changes often, a search tool would be most effective.
[Action] tavily_search_results_json args: {'query': 'Shanghai temperature forecast March 30, 2024'}
[Observation] [{'url': 'https://en.climate-data.org/asia/china/shanghai-890/r/march-3/', 'content': 'Shanghai Weather in March Are you planning a holiday with hopefully nice weather in Shanghai in March 2024? Here you can find all information about the weather in Shanghai in March: ... 30.7 °C (87.3) °F. 27 °C (80.5) °F. 22.5 °C (72.5) °F. 17 °C (62.6) °F. 10.8 °C (51.4) °F.'}, {'url': 'https://www.meteoprog.com/weather/Szanghaj/month/march/', 'content': 'Shanghai (China) weather in March 2024 ☀️ Accurate weather forecast for Shanghai in March ⛅ Detailed forecast By month Current temperature "near me" Weather news ⊳ Widget of weather ⊳ Water temperature | METEOPROG. ... 30 March +17 °+11° 31 March +16° ...'}, {'url': 'https://www.accuweather.com/en/cn/shanghai/106577/march-weather/106577', 'content': 'Get the monthly weather forecast for Shanghai, Shanghai, China, including daily high/low, historical averages, to help you plan ahead.'}, {'url': 'https://world-weather.info/forecast/china/shanghai/march-2024/', 'content': 'Extended weather forecast in Shanghai. Hourly Week 10 days 14 days 30 days Year. Detailed ⚡ Shanghai Weather Forecast for March 2024 - day/night 🌡️ temperatures, precipitations - World-Weather.info.'}, {'url': 'https://www.weather25.com/asia/china/shanghai?page=month&month=March', 'content': "Our weather forecast can give you a great sense of what weather to expect in Shanghai in March 2024. If you're planning to visit Shanghai in the near future, we highly recommend that you review the 14 day weather forecast for Shanghai before you arrive. Temperatures. 59 ° / 44 °. Rainy Days."}]
[Thought] The search results provided URLs with general March weather information and historical data for Shanghai, but haven't provided a specific forecast for tomorrow's temperature. I need to refine my search to get the weather forecast specifically for March 30, 2024, in Shanghai.
[Action] tavily_search_results_json args: {'query': 'Shanghai weather forecast for March 30, 2024'}
[Observation] [{'url': 'https://www.accuweather.com/en/cn/shanghai/106577/march-weather/106577', 'content': 'Get the monthly weather forecast for Shanghai, Shanghai, China, including daily high/low, historical averages, to help you plan ahead.'}, {'url': 'https://world-weather.info/forecast/china/shanghai/march-2024/', 'content': 'Extended weather forecast in Shanghai. Hourly Week 10 days 14 days 30 days Year. Detailed ⚡ Shanghai Weather Forecast for March 2024 - day/night 🌡️ temperatures, precipitations - World-Weather.info.'}, {'url': 'https://www.weather-atlas.com/en/china/shanghai-weather-march', 'content': "In Shanghai, China, in March, the average water temperature is 8°C (46.4°F). Swimming in 8°C (46.4°F) is considered life-threatening. Even a few minutes in 13°C (55.4°F) water is uncomfortable, and swimming below 10°C (50°F) may cause total loss of breathing control and cold shock, depending on a person's physique."}, {'url': 'https://www.meteoprog.com/weather/Szanghaj/month/march/', 'content': 'Shanghai (China) weather in March 2024 ☀️ Accurate weather forecast for Shanghai in March ⛅ Detailed forecast By month Current temperature "near me" Weather news ⊳ Widget of weather ⊳ Water temperature | METEOPROG. ... 30 March +17 °+11° 31 March +16° ...'}, {'url': 'https://www.weather25.com/asia/china/shanghai?page=month&month=March', 'content': "Our weather forecast can give you a great sense of what weather to expect in Shanghai in March 2024. If you're planning to visit Shanghai in the near future, we highly recommend that you review the 14 day weather forecast for Shanghai before you arrive. Temperatures. 59 ° / 44 °. Rainy Days."}]
[Execute Result] {'thought': "The search has returned a specific forecast for March 30, 2024, which indicates that the temperatures are expected to be +17 °C for the high and +11 °C for the low. This information is sufficient to answer the user's question.", 'action_name': 'finish', 'action_parameters': {'content': 'The temperature in Shanghai for tomorrow, March 30, 2024, is expected to be a high of +17 °C and a low of +11 °C.'}}
[Execute] Execute End.
[Revised Plan] {"goals": ["Find out the temperature in Shanghai tomorrow."], "tasks": [{"task_id": 6, "description": "Provide the temperature in Shanghai for tomorrow using current knowledge.", "status": "done"}], "next_task_id": null}
[Agent Result] The temperature in Shanghai for tomorrow, March 30, 2024, is expected to be a high of +17 °C and a low of +11 °C.
[Agent] Agent End.
The temperature in Shanghai for tomorrow, March 30, 2024, is expected to be a high of +17 °C and a low of +11 °C.


## Output Formatter

The output formatter is a powerful feature in pne. It can help you format the output of LLM. The follow example show how to use the output formatter to format the output of LLM.


```python
from typing import List
import promptulate as pne
from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    provinces: List[str] = Field(description="List of provinces name")


resp: LLMResponse = pne.chat("Please tell me all provinces in China.?",
                             output_schema=LLMResponse)
print(resp)
```

    provinces=['Anhui', 'Fujian', 'Gansu', 'Guangdong', 'Guizhou', 'Hainan', 'Hebei', 'Heilongjiang', 'Henan', 'Hubei', 'Hunan', 'Jiangsu', 'Jiangxi', 'Jilin', 'Liaoning', 'Qinghai', 'Shaanxi', 'Shandong', 'Shanxi', 'Sichuan', 'Yunnan', 'Zhejiang', 'Taiwan', 'Guangxi', 'Nei Mongol', 'Ningxia', 'Xinjiang', 'Xizang', 'Beijing', 'Chongqing', 'Shanghai', 'Tianjin', 'Hong Kong', 'Macao']
    

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

## AIChat

If you have multi-conversation and only use one LLM, you can use `pne.AIChat` init a chat object. It will save the LLM object and you can use it to chat.

The follow example show how to use `pne.AIChat` to chat.


```python
import promptulate as pne

ai_chat = pne.AIChat(model="gpt-4-1106-preview", model_config={"temperature": 0.5})
resp: str = ai_chat.run("Hello")
print(resp)
```

    Hello! How can I assist you today?
    

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
