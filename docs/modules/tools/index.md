# Tool

## What is Tool?

The tools module provides LLM with the ability to extend external tools, which can be said to be the first step towards intelligence. Through tools, a perception feedback system can be built for LLM, providing more possibilities for LLM application development.

For example, when you want to `let LLM query the weather in Shanghai tomorrow`, you can define a python function, then let the large model output the word "Shanghai", and pass it as a parameter to the function you defined, and call it back to the large model.

The prompt maybe like this:

`"You are a weather query assistant. When the user inputs the city name, please return the weather information of that city."`

At this point, you need to use a tool to implement this functionality

:::info
You can refer to the function call and tool call in the [OpenAI Documentation](https://platform.openai.com/docs/guides/function-calling). The tool module in `pne` can implement these two functions more simply.
:::

## Usage

### Basic Usage

Using a tool in `pne` is very simple. To solve the problem of `What is the temperature in Shanghai tomorrow?`, the following code is enough.

Here we use `wttr.in` to get weather information.

```python
import pne
import requests


def query_weather(city: str) -> str:
    """
    Query the weather information of the specified city through wttr.in.
    Ref: https://github.com/chubin/wttr.in

    Args:
        city(str): City name, eg: London, Shanghai

    Returns:
        str: Weather information description
    """
    # wttr.in supports Chinese city names, use format=j1 to get JSON format data
    try:
        response = requests.get(f"https://wttr.in/{city}?format=j1")
        data = response.json()

        tomorrow = data["weather"][1]  # Index 1 is tomorrow's forecast
        temp_min = tomorrow["mintempC"]
        temp_max = tomorrow["maxtempC"]
        weather_desc = tomorrow["hourly"][4]["weatherDesc"][0]["value"]

        return (
            f"Tomorrow's weather in {city}:\n"
            f"Temperature: {temp_min}°C to {temp_max}°C\n"
            f"Weather: {weather_desc}"
        )

    except Exception as e:
        return f"An error occurred while getting weather information: {str(e)}"


response: str = pne.chat(
    model="gpt-4o",
    messages="What is the temperature in Shanghai tomorrow?",
    tools=[query_weather],
)

print(response)

```

Output:

```
The temperature in Shanghai tomorrow will be between 18°C and 22°C.
```

Easy to use, right?

`pne` will automatically convert your function into parameters that LLM can recognize, and then call the function you defined.

### Best Practices

How to write a good function, so that the large model can better understand your function? The most important concept is to `introduce your function to the large model just like you would to a human, and introduce it as detailed as possible.
`
::: info TIP
It is very important that you write a good function comment, formal parameter and corresponding data type, this way you can make LLM understand your function better.
:::

**Bad example 1: No function comment**

```python
def query_weather(city: str):
    ...
```

::: warning WARN
Lack of function comments will make the large model very confused. It can only guess the specific function of this function through the function name and the meaning of the parameters.

However, when the function becomes complex, LLM will find it difficult to understand the function of this function.
:::

**Bad example 2: No parameter type**

```python
def get_user_by_id(id):
    ...
```

::: warning WARN
Lack of parameter type will make the large model unable to determine the specific type of the parameter, and it will be difficult to pass the parameter correctly.

Here, the parameter `id` is a `string` or an `integer`, but the large model cannot determine which one it is.

**If pass a error id type, the function will report an error.**
:::

**Good example1: detailed function and parameter comments, data types**

```python{2-11}
def query_weather(city): # [!code --]
def query_weather(city: str) -> str: # [!code ++]
    """ # [!code ++]
    Query the weather information of the specified city through wttr.in.  # [!code ++]
    Ref: https://github.com/chubin/wttr.in  # [!code ++]

    Args:  # [!code ++]
        city(str): City name, eg: London, Shanghai  # [!code ++]

    Returns:  # [!code ++]
        str: Weather information description  # [!code ++]
    """  # [!code ++]
    ...
```

In the function comments, examples of possible parameters are explained, which will better help LLM understand your function. Here we use `eg: London, Shanghai` to explain the possible parameters.

Some time you can also `add some bad case` examples to help LLM understand your function better. For example:

```python
def query_weather(city: str) -> str:
    """
    Query the weather information of the specified city through wttr.in.
    Ref: https://github.com/chubin/wttr.in

    Args:
        city(str): City name, eg: London, Shanghai  # [!code --]
        city(str): City name, eg: London, Shanghai, bad case: 上海. # [!code ++]
        English only, do not input other languages. # [!code ++]

    Returns:
        str: Weather information description
    """
    ...
```

**Please introduce your function to LLM in detail, just like you would to a human.**

**Good example2: Provide return value**

```python
def write_file(file_path: str, content: str) -> str:
    """Write content to a file in current workspace path.

    Args:
        file_path (str): The absolute file path to write to. Eg: /Users/user/workspace/main.py
        content (str): The content to write to the file.
    """
    with open(file_path, "a+") as file:
        file.write(content)

    return f"File {file_path} has been written successfully." # [!code ++]
```

When your function doesn't have a clear return value, such as when writing to a file, you can return a fixed string to indicate success. For example, `"File has been written successfully."` informs LLM that the operation was completed.

**Good example3: Record exceptions**

```python
def get_user_by_id(id: str) -> str:
    try:
        ...
    except Exception as e:
        return f"User with id {id} not found."
```

When executing a function, unexpected situations may arise. For instance, the function above might throw an exception indicating that the user ID does not exist. In such cases, customizing the exception's return information can significantly improve LLM's understanding of your function.

Although `pne` has built-in exception handling, which allows the program to return exception information to LLM for retry when an exception occurs, it is still recommended to handle exceptions manually. This approach provides more detailed exception handling information, enabling LLM to better comprehend your function.

In many cases, the issue lies with the function itself, rather than LLM's input. Therefore, simply retrying the function may not resolve the error. To avoid low-level errors, it is essential to ensure that your function is thoroughly covered by unit tests.

::: info TIP
You don't need to care how `pne` convert your function into a tool.

If you really want to know, you can use the following method to get the data transmitted to the bottom layer of the large model.

```python
from promptulate.tools import function_to_tool_schema

schema = function_to_tool_schema(query_weather)
print(schema)
```

Then you can see the following output:

```json
{
    "properties": {
        "city": {
            "type": "string"
        }
    },
    "required": [
        "city"
    ],
    "type": "object",
    "description": "\n    Query trequestser information of the specified city through wttr.in.\n    Ref: https://github.com/chubin/wttr.in\n\n    Args:\n        city(str): City name, eg: London, Shanghai\n\n    Returns:\n        str: Weather information description\n    ",
    "name": "query_weather"
}
```

:::

### Usage with AIChat

You can also use `pne.AIChat()` to run tools.

```python{7-15}
import pne

# use the same function as above
def query_weather(city: str):
    ...

ai = pne.AIChat(
    model="deepseek/deepseek-chat",
    model_config={
        "api_base": "https://api.deepseek.com",
        "api_key": "sk-6414d63db95844beaf2fc264d2a0acc1",
    },
    tools=[query_weather],
)
response: str = ai.run(messages="What is the temperature in Shanghai tomorrow?")

print(response)
```

Output:

```text
The temperature in Shanghai tomorrow will be between 18°C and 22°C.
```

### Tool State Management

Sometimes, your tools require state management, `such as file read and write operations, which require declaring a workspace first.`

At this point, you may need to declare a class instance to maintain this state, and this functional declaration can also be used on class methods.

The example below demonstrates how to write a Python file to the current directory workspace.

::: info TIP
Remember the best practices we mentioned above, including a clear function name, detailed function comments, parameter types, and return value types.
:::

```python
import pne
from typing import Callable, List


class FileToolKit:
    def __init__(self, workspace: str) -> None:
        """Initialize the FileToolKit.

        Args:
            workspace (str): The workspace path of the tool.
        """
        self.workspace: str = workspace

    def write_file(self, file_name: str, content: str):
        """Write content to a file in current workspace path.

        Args:
            file_name (str): The file name to write to. Eg: main.py, src/main.py
            content (str): The content to write to the file.
        """
        with open(f"{self.workspace}/{file_name}", "a+") as file:
            file.write(content)

        return f"File {file_name} has been written successfully."

    def read_file(self, file_name: str) -> str:
        """Read content from a file in current workspace path.

        Args:
            file_name (str): The file name to read from. Eg: main.py, src/main.py

        Returns:
            str: The content of the file
        """
        with open(f"{self.workspace}/{file_name}", "r") as file:
            return file.read()

    def get_tools(self) -> List[Callable]:
        return [self.write_file, self.read_file]


tool_kit = FileToolKit("./")
ai = pne.AIChat(
    model="deepseek/deepseek-chat",
    tools=tool_kit.get_tools(),
)

instruction = "Write a python bubble sort algorithm in bubble_sort.py and show me the content of the file."
response: str = ai.run(messages=instruction)

print(response)
```

### ReAct Reasoning

**ReAct is a prompting technique** that combines reasoning and acting. It is a simple but effective way to improve the performance of LLMs.

::: info TIP
You can see [Paper](https://arxiv.org/abs/2210.03629) or [Prompting Guide](https://www.promptingguide.ai/techniques/react) for more information about ReAct.
:::

You can easily use `pne` to solve problems with the ReAct framework. But before that, let me show the difference between solving a problem with and without the ReAct framework.

::: info Problem
Calculate how many apples and bananas can be bought with $20 if apples cost $2 each and bananas cost $1.50 each. Buy equal numbers of each fruit.
:::

**Without ReAct**

```text
Since we need equal numbers, let's say we buy x of each.
Cost equation: 2x + 1.50x = 20
3.50x = 20
x = 5.71
Since we can't buy partial fruits, we'll buy 5 of each.
Final answer: 5 apples and 5 bananas for $17.50 total.
```

**With ReAct**

```text
Thought: Need to set up equation with equal quantities
Action: Write equation 2x + 1.50x = 20 (where x is number of each fruit)
Observation: Combined term is 3.50x = 20

Thought: Solve for x
Action: Divide 20 by 3.50
Observation: x = 5.71 fruits

Thought: Can't buy partial fruits
Action: Round down to 5 fruits each
Observation: 5 apples ($10) + 5 bananas ($7.50) = $17.50

Thought: Check if under budget
Action: Verify $17.50 < $20
Observation: Solution valid

Final answer: Buy 5 apples and 5 bananas for $17.50
```

The ReAct approach makes the reasoning process explicit and systematic, breaking down the problem into clear steps of thinking, acting, and observing results.

The following example demonstrates how to use the ReAct framework to solve the problem.

Firstly, we need to define a calculator tool:

```python
def calculator(expression: str) -> str:
    """
    A simple calculator that evaluates mathematical expressions.
    
    Args:
        expression (str): A mathematical expression to evaluate, e.g. "2 + 2" or "3.50 * 5"
        
    Returns:
        str: The result of the calculation
    """
    try:
        # Safely evaluate the mathematical expression
        result = eval(expression)
        return f"{result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"
```

Then, we need to define the problem:

```python
question = """
Calculate how many apples and bananas can be bought with $20 if apples cost $2 each 
and bananas cost $1.50 each. Buy equal numbers of each fruit.
"""
```

Finally, we can use the `pne.chat()` method to solve the problem, here we use `normal chat`:

```python
import pne

response: str = pne.chat(
    model="gpt-4o",
    messages=question,
    tools=[calculator],
)
print(response) # With $20, you can buy 5 apples and 5 bananas.
```

Output:

```text
With $20, you can buy 5 apples and 5 bananas.
```

If we don't pass the `mode` parameter, `pne` will use the `normal chat` mode by default.

Now, we use the `ReAct` mode to solve the problem:

```python
import pne

response: str = pne.chat(
    model="gpt-4o",
    tools=[calculator],
    messages=question,
    mode=pne.Mode.REACT,
)

print(response) # With $20, you can buy 5 apples and 5 bananas.
```

Output:

> The last line is the print output, while the rest are agent outputs to the terminal for debugging purposes

```text{1-12}
[Agent] Tool Agent start...
[User instruction] You are a helpful assistant

Calculate how many apples and bananas can be bought with $20 if apples cost $2 each 
and bananas cost $1.50 each. Buy equal numbers of each fruit.


[Thought] To determine how many apples and bananas can be bought with $20, given that apples cost $2 each and bananas cost $1.50 each, and we need to buy equal numbers of each fruit, we can set up the equation: 2x + 1.5x = 20, where x is the number of apples and bananas. We need to solve for x.
[Action] calculator args: {'expression': '20 / (2 + 1.5)'}
[Observation] 5.714285714285714
[Agent Result] With $20, you can buy 5 apples and 5 bananas.
[Agent] Agent End.
With $20, you can buy 5 apples and 5 bananas.
```

### Plan and ReAct Reasoning

::: info TIP
You can see [https://arxiv.org/abs/2305.04091](https://arxiv.org/abs/2305.04091) for more information about it.
:::

::: info Problem
What is the hometown of the 2024 Australia open winner?
:::

To address this, we first need to identify the winner of the 2024 Australia Open. Subsequently, we need to determine the hometown of this player. Utilizing a web search is sufficient to resolve this issue.

```text
[Agent] Assistant Agent start... 
[User instruction] What's the temperature in Shanghai tomorrow? 
[Plan] {"goals": ["Find out the temperature in Shanghai tomorrow."], "tasks": [{"task_id": 1, "description": "Open a web browser on your device.", "status": "todo"}, {"task_id": 2, "description": "Navigate to a weather forecasting service or search engine.", "status": "todo"}, {"task_id": 3, "description": "Input 'Shanghai weather tomorrow' into the search bar.", "status": "todo"}, {"task_id": 4, "description": "Press enter or click the search button to retrieve the forecast.", "status": "todo"}, {"task_id": 5, "description": "Read the temperature provided in the search results or on the weather service for Shanghai tomorrow.", "status": "todo"}], "next_task_id": 1} 
[Agent] Tool Agent start... 
[User instruction] Open a web browser on your device. 
[Execute Result] {'thought': "The user seems to be asking for an action that is outside the scope of my capabilities. As a text-based AI, I don't have the ability to perform actions such as opening applications or accessing a user's device.", 'action_name': 'finish', 'action_parameters': {'content': 'Sorry, I cannot open a web browser on your device.'}} 
[Execute] Execute End. 
[Revised Plan] {"goals": ["Find out the temperature in Shanghai tomorrow."], "tasks": [{"task_id": 1, "description": "Open a web browser on your device.", "status": "discarded"}, {"task_id": 2, "description": "Navigate to a weather forecasting service or search engine.", "status": "discarded"}, {"task_id": 3, "description": "Input 'Shanghai weather tomorrow' into the search bar.", "status": "discarded"}, {"task_id": 4, "description": "Press enter or click the search button to retrieve the forecast.", "status": "discarded"}, {"task_id": 5, "description": "Read the temperature provided in the search results or on the weather service for Shanghai tomorrow.", "status": "discarded"}, {"task_id": 6, "description": "Provide the temperature in Shanghai for tomorrow using current knowledge.", "status": "todo"}], "next_task_id": 6} 
[Agent] Tool Agent start... [User instruction] Provide the temperature in Shanghai for tomorrow using current knowledge. 
[Thought] I need to use a tool to find the temperature in Shanghai for tomorrow. Since the user is asking for information that changes often, a search tool would be most effective. 
[Action] tavily_search_results_json args: {'query': 'Shanghai temperature forecast March 30, 2024'} 
[Observation] [{'url': 'https://en.climate-data.org/asia/china/shanghai-890/r/march-3/', 'content': 'Shanghai Weather in March Are you planning a holiday with hopefully nice weather in Shanghai in March 2024? Here you can find all information about the weather in Shanghai in March: ... 30.7 °C (87.3) °F. 27 °C (80.5) °F. 22.5 °C (72.5) °F. 17 °C (62.6) °F. 10.8 °C (51.4) °F.'}, {'url': 'https://www.meteoprog.com/weather/Szanghaj/month/march/', 'content': 'Shanghai (China) weather in March 2024 ☀️ Accurate weather forecast for Shanghai in March ⛅ Detailed forecast By month Current temperature "near me" Weather news ⊳ Widget of weather ⊳ Water temperature | METEOPROG. ... 30 March +17 °+11° 31 March +16° ...'}, {'url': 'https://www.accuweather.com/en/cn/shanghai/106577/march-weather/106577', 'content': 'Get the monthly weather forecast for Shanghai, Shanghai, China, including daily high/low, historical averages, to help you plan ahead.'}, {'url': 'https://world-weather.info/forecast/china/shanghai/march-2024/', 'content': 'Extended weather forecast in Shanghai. Hourly Week 10 days 14 days 30 days Year. Detailed ⚡ Shanghai Weather Forecast for March 2024 - day/night 🌡️ temperatures, precipitations - World-Weather.info.'}, {'url': 'https://www.weather25.com/asia/china/shanghai?page=month&month=March', 'content': "Our weather forecast can give you a great sense of what weather to expect in Shanghai in March 2024. If you're planning to visit Shanghai in the near future, we highly recommend that you review the 14 day weather forecast for Shanghai before you arrive. Temperatures. 59 ° / 44 °. Rainy Days."}] 
[Thought] The search results provided URLs with general March weather information and historical data for Shanghai, but haven't provided a specific forecast for tomorrow's temperature. I need to refine my search to get the weather forecast specifically for March 30, 2024, in Shanghai. 
[Action] tavily_search_results_json args: {'query': 'Shanghai weather forecast for March 30, 2024'} 
[Observation] [{'url': 'https://www.accuweather.com/en/cn/shanghai/106577/march-weather/106577', 'content': 'Get the monthly weather forecast for Shanghai, Shanghai, China, including daily high/low, historical averages, to help you plan ahead.'}, {'url': 'https://world-weather.info/forecast/china/shanghai/march-2024/', 'content': 'Extended weather forecast in Shanghai. Hourly Week 10 days 14 days 30 days Year. Detailed ⚡ Shanghai Weather Forecast for March 2024 - day/night 🌡️ temperatures, precipitations - World-Weather.info.'}, {'url': 'https://www.weather-atlas.com/en/china/shanghai-weather-march', 'content': "In Shanghai, China, in March, the average water temperature is 8°C (46.4°F). Swimming in 8°C (46.4°F) is considered life-threatening. Even a few minutes in 13°C (55.4°F) water is uncomfortable, and swimming below 10°C (50°F) may cause total loss of breathing control and cold shock, depending on a person's physique."}, {'url': 'https://www.meteoprog.com/weather/Szanghaj/month/march/', 'content': 'Shanghai (China) weather in March 2024 ☀️ Accurate weather forecast for Shanghai in March ⛅ Detailed forecast By month Current temperature "near me" Weather news ⊳ Widget of weather ⊳ Water temperature | METEOPROG. ... 30 March +17 °+11° 31 March +16° ...'}, {'url': 'https://www.weather25.com/asia/china/shanghai?page=month&month=March', 'content': "Our weather forecast can give you a great sense of what weather to expect in Shanghai in March 2024. If you're planning to visit Shanghai in the near future, we highly recommend that you review the 14 day weather forecast for Shanghai before you arrive. Temperatures. 59 ° / 44 °. Rainy Days."}] 
[Execute Result] {'thought': "The search has returned a specific forecast for March 30, 2024, which indicates that the temperatures are expected to be +17 °C for the high and +11 °C for the low. This information is sufficient to answer the user's question.", 'action_name': 'finish', 'action_parameters': {'content': 'The temperature in Shanghai for tomorrow, March 30, 2024, is expected to be a high of +17 °C and a low of +11 °C.'}} 
[Execute] Execute End. 
[Revised Plan] {"goals": ["Find out the temperature in Shanghai tomorrow."], "tasks": [{"task_id": 6, "description": "Provide the temperature in Shanghai for tomorrow using current knowledge.", "status": "done"}], "next_task_id": null} [Agent Result] The temperature in Shanghai for tomorrow, March 30, 2024, is expected to be a high of +17 °C and a low of +11 °C. 
[Agent] Agent End. The temperature in Shanghai for tomorrow, March 30, 2024, is expected to be a high of +17 °C and a low of +11 °C.
```

## Supported Tools

Currently, `promptulate` has integrated the following tools:

- DuckDuckGo Search: DDG search engine
- Calculator: calculator
- Shell: can execute shell commands (compatible with Windows, Mac, and Linux operating systems)
- LangchainTool: ported Langchain-related tools, can be perfectly compatible for use
- HuggingFaceTool: HuggingFace-related tools, can be perfectly compatible for use
- IotSwitchMqtt: iot tool, can send mqtt messages to iot devices
- HumanFeedBackTool: introduces human feedback at appropriate times
- Arxiv: Arxiv paper search tool
- Semantic Scholar: Semantic Scholar paper search tool, can search papers, query paper references, and query papers citing this paper
- Python REPL: can execute python scripts
- FileManager: can perform file read and write operations
- Sleep: can pause, which is very helpful for users who need time control in the agent to control the time interval of event execution

## Using Tool in Agent

The primary function of the Tool module is to provide tool capability support for Agent, see details in [Agent](/modules/agent.md#agent).

## Custom Tool

See details in [Custom Tool](/modules/tools/custom_tool_usage.md#custom-tool).

## Tool Usage

In most cases, tools are used for Agent usage, and Tool can also be separated from Agent for standalone use. The following example demonstrates how to use a DuckDuckGo for external search.

```python
from promptulate.tools import DuckDuckGoTool

tool = DuckDuckGoTool()
tool.run("what is promptulate?")
```

In promptulate, all tools can be run using the tool.run() method.

Additionally, with the same import method, you can also import the following tools:

```python
from promptulate.tools import (
    DuckDuckGoTool,
    DuckDuckGoReferenceTool,
    Calculator,
    ArxivQueryTool,
    ArxivSummaryTool,
    PaperSummaryTool,
    PythonREPLTool,
    SemanticScholarQueryTool,
    SemanticScholarCitationTool,
    SemanticScholarReferenceTool,
    HumanFeedBackTool,
    IotSwitchTool,
    LangchainTool,
    HuggingFaceTool
)
```

All tools inherit from `Tool`, so you can use the `tool.run(prompt)` method to call them.

## Using LangChain Tool

Promptulate is compatible with all LangChain tools and perfectly compatible with Promptulate's hooks system. See the details in [LangChain Tool usage](/modules/tools/langchain_tool_usage.md)

## Tools with LLM Capabilities

In Promptulate, some tools provided to the Agent also have the ability to call large language models, which generally have some simple capability processing functions. If you need to, you can directly use these tools with LLM capabilities, and the next section will demonstrate how to use them.

Here are some tools with LLM capabilities:

- ArxivSummaryTool: Arxiv paper summary tool, can provide the paper's summary, key insights, lessons learned, references, and related suggestions
- PaperSummaryTool: A powerful paper summary tool, retrieves data from Semantic Scholar and Arxiv, can provide the paper's summary, key insights, lessons learned, references, and related suggestions
- EnhancedSearchTool: Enhanced search engine summary tool, can call multiple search engines for data processing at the same time.
- IotSwitchMqtt: Can intelligently recognize whether the input natural language conforms to the control rule table.
- Calculator: Calculator, mainly used for accurate recognition and analysis of user input

## Using Tool Independently

If you want to do some other interesting applications, you can also execute the tool directly. Using Promptulate to execute tools is very simple, and for all tools, you can use the `run()` method to run them.

### Basic Capability Tools

The following example demonstrates using ArxivQueryTool to search for Arxiv-related papers.

```text
entry_id:http://arxiv.org/abs/2306.05212v1 title:RETA-LLM: A Retrieval-Augmented Large Language Model Toolkit authors:[arxiv.Result.Author('Jiongnan Liu'), arxiv.Result.Author('Jiajie Jin'), arxiv.Result.Author('Zihan Wang'), arxiv.Result.Author('Jiehan Cheng'), arxiv.Result.Author('Zhicheng Dou'), arxiv.Result.Author('Ji-Rong Wen')] summary:Although Large Language Models (LLMs) have demonstrated extraordinary
capabilities in many domains, they still have a tendency to hallucinate and
generate fictitious responses to user requests. This problem can be alleviated
by augmenting LLMs with information retrieval (IR) systems (also known as
retrieval-augmented LLMs). Applying this strategy, LLMs can generate more
factual texts in response to user input according to the relevant content
retrieved by IR systems from external corpora as references. In addition, by
incorporating external knowledge, retrieval-augmented LLMs can answer in-domain
questions that cannot be answered by solely relying on the world knowledge
stored in parameters. To support research in this area and facilitate the
development of retrieval-augmented LLM systems, we develop RETA-LLM, a
{RET}reival-{A}ugmented LLM toolkit. In RETA-LLM, we create a complete pipeline
to help researchers and users build their customized in-domain LLM-based
systems. Compared with previous retrieval-augmented LLM systems, RETA-LLM
provides more plug-and-play modules to support better interaction between IR
systems and LLMs, including {request rewriting, document retrieval, passage
extraction, answer generation, and fact checking} modules. Our toolkit is
publicly available at https://github.com/RUC-GSAI/YuLan-IR/tree/main/RETA-LLM. ;

entry_id:http://arxiv.org/abs/2305.12720v1 title:llm-japanese-dataset v0: Construction of Japanese Chat Dataset for Large Language Models and its Methodology authors:[arxiv.Result.Author('Masanori Hirano'), arxiv.Result.Author('Masahiro Suzuki'), arxiv.Result.Author('Hiroki Sakaji')] summary:This study constructed a Japanese chat dataset for tuning large language
models (LLMs), which consist of about 8.4 million records. Recently, LLMs have
been developed and gaining popularity. However, high-performing LLMs are
usually mainly for English. There are two ways to support languages other than
English by those LLMs: constructing LLMs from scratch or tuning existing
models. However, in both ways, datasets are necessary parts. In this study, we
focused on supporting Japanese in those LLMs and making a dataset for training
or tuning LLMs in Japanese. The dataset we constructed consisted of various
tasks, such as translation and knowledge tasks. In our experiment, we tuned an
existing LLM using our dataset and evaluated the performance qualitatively. The
results suggest that our dataset is possibly beneficial for LLMs. However, we
also revealed some difficulties in constructing LLMs in languages other than
English. ;

entry_id:http://arxiv.org/abs/2305.05176v1 title:FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance authors:[arxiv.Result.Author('Lingjiao Chen'), arxiv.Result.Author('Matei Zaharia'), arxiv.Result.Author('James Zou')] summary:There is a rapidly growing number of large language models (LLMs) that users
can query for a fee. We review the cost associated with querying popular LLM
APIs, e.g. GPT-4, ChatGPT, J1-Jumbo, and find that these models have
heterogeneous pricing structures, with fees that can differ by two orders of
magnitude. In particular, using LLMs on large collections of queries and text
can be expensive. Motivated by this, we outline and discuss three types of
strategies that users can exploit to reduce the inference cost associated with
using LLMs: 1) prompt adaptation, 2) LLM approximation, and 3) LLM cascade. As
an example, we propose FrugalGPT, a simple yet flexible instantiation of LLM
cascade which learns which combinations of LLMs to use for different queries in
order to reduce cost and improve accuracy. Our experiments show that FrugalGPT
can match the performance of the best individual LLM (e.g. GPT-4) with up to
98% cost reduction or improve the accuracy over GPT-4 by 4% with the same cost.
The ideas and findings presented here lay a foundation for using LLMs
sustainably and efficiently. ;

entry_id:http://arxiv.org/abs/2306.08302v2 title:Unifying Large Language Models and Knowledge Graphs: A Roadmap authors:[arxiv.Result.Author('Shirui Pan'), arxiv.Result.Author('Linhao Luo'), arxiv.Result.Author('Yufei Wang'), arxiv.Result.Author('Chen Chen'), arxiv.Result.Author('Jiapu Wang'), arxiv.Result.Author('Xindong Wu')] summary:Large language models (LLMs), such as ChatGPT and GPT4, are making new waves
in the field of natural language processing and artificial intelligence, due to
their emergent ability and generalizability. However, LLMs are black-box
models, which often fall short of capturing and accessing factual knowledge. In
contrast, Knowledge Graphs (KGs), Wikipedia and Huapu for example, are
structured knowledge models that explicitly store rich factual knowledge. KGs
can enhance LLMs by providing external knowledge for inference and
interpretability. Meanwhile, KGs are difficult to construct and evolving by
nature, which challenges the existing methods in KGs to generate new facts and
represent unseen knowledge. Therefore, it is complementary to unify LLMs and
KGs together and simultaneously leverage their advantages. In this article, we
present a forward-looking roadmap for the unification of LLMs and KGs. Our
roadmap consists of three general frameworks, namely, 1) KG-enhanced LLMs,
which incorporate KGs during the pre-training and inference phases of LLMs, or
for the purpose of enhancing understanding of the knowledge learned by LLMs; 2)
LLM-augmented KGs, that leverage LLMs for different KG tasks such as embedding,
completion, construction, graph-to-text generation, and question answering; and
3) Synergized LLMs + KGs, in which LLMs and KGs play equal roles and work in a
mutually beneficial way to enhance both LLMs and KGs for bidirectional
reasoning driven by both data and knowledge. We review and summarize existing
efforts within these three frameworks in our roadmap and pinpoint their future
research directions. ;

entry_id:http://arxiv.org/abs/2303.10130v4 title:GPTs are GPTs: An Early Look at the Labor Market Impact Potential of Large Language Models authors:[arxiv.Result.Author('Tyna Eloundou'), arxiv.Result.Author('Sam Manning'), arxiv.Result.Author('Pamela Mishkin'), arxiv.Result.Author('Daniel Rock')] summary:We investigate the potential implications of large language models (LLMs),
such as Generative Pre-trained Transformers (GPTs), on the U.S. labor market,
focusing on the increased capabilities arising from LLM-powered software
compared to LLMs on their own. Using a new rubric, we assess occupations based
on their alignment with LLM capabilities, integrating both human expertise and
GPT-4 classifications. Our findings reveal that around 80% of the U.S.
workforce could have at least 10% of their work tasks affected by the
introduction of LLMs, while approximately 19% of workers may see at least 50%
of their tasks impacted. We do not make predictions about the development or
adoption timeline of such LLMs. The projected effects span all wage levels,
with higher-income jobs potentially facing greater exposure to LLM capabilities
and LLM-powered software. Significantly, these impacts are not restricted to
industries with higher recent productivity growth. Our analysis suggests that,
with access to an LLM, about 15% of all worker tasks in the US could be
completed significantly faster at the same level of quality. When incorporating
software and tooling built on top of LLMs, this share increases to between 47
and 56% of all tasks. This finding implies that LLM-powered software will have
a substantial effect on scaling the economic impacts of the underlying models.
We conclude that LLMs such as GPTs exhibit traits of general-purpose
technologies, indicating that they could have considerable economic, social,
and policy implications. ;
```

### Tool with LLM Capability

Next, we will demonstrate the performance of a Tool after being empowered with LLM using the PaperSummaryTool. The following example shows the result of searching for the paper "Attention Is All You Need" using the PaperSummaryTool:

```python
from promptulate.tools.paper.tools import PaperSummaryTool


def main():
    tool = PaperSummaryTool()
    result = tool.run("Attention Is All You Need")
    # you can also input an arxiv id as follows
    # result = tool.run("2303.09014")
    print(result)


if __name__ == "__main__":
    main()
```

The output result is as follows

```text
Title: Attention Is All You Need

Summary: The current mainstream sequence transformation models are based on complex recurrent or convolutional neural networks, adopting an encoder-decoder structure. The best-performing models also use attention mechanisms to connect the encoder and decoder. We propose a new simple network architecture—the Transformer, which is solely based on attention mechanisms, completely discarding recurrence and convolution. Experiments on two machine translation tasks demonstrate that these models outperform other models in quality, while being easier to parallelize, significantly reducing training time. Our model achieves a score of 28.4 BLEU on the WMT 2014 English-to-German translation task, surpassing the current best result, including ensemble models, by 2 BLEU points. On the WMT 2014 English-to-French translation task, our model achieves a new single-model best BLEU score of 41.8 after training for 3.5 days on 8 GPUs, with training costs being only a fraction of the best model in the literature. We prove that the Transformer has good generalization capabilities, successfully applying it to English constituent parsing, regardless of the scale or limitation of the training data.

Keywords: Transformer, attention mechanism, machine translation, BLEU score, parallelizable, training time, generalization.

Key Insights:
- Traditional sequence transformation models are based on complex recurrent or convolutional neural networks, while the best models use attention mechanisms to connect the encoder and decoder.
- This paper proposes a new simple network architecture—the Transformer, which is solely based on attention mechanisms, completely discarding recurrence and convolution. On machine translation tasks, this model performs better in quality, while being easier to parallelize, significantly reducing training time.
- This paper's model achieves a score of 28.4 BLEU on the WMT 2014 English-to-German translation task and a score of 41.8 BLEU on the WMT 2014 English-to-French translation task, becoming the best single-model result.

Lessons Learned:
- Attention mechanisms are an effective way to connect the encoder and decoder, which can improve the performance of sequence transformation models.
- Simple network architectures can also achieve good results, not necessarily requiring complex recurrent or convolutional structures.
- The Transformer model has good generalization capabilities, successfully applying it to other tasks, such as English constituent parsing.

Recommendations:
- Further explore the optimization methods of the Transformer network structure to improve its performance on different tasks.
- Attempt to apply the Transformer to other natural language processing tasks, such as text classification, named entity recognition, etc.
- Research how to introduce external knowledge, such as knowledge graphs, into the Transformer to improve its understanding and expression of semantics.
- Explore how to apply the Transformer to multilingual translation tasks to achieve more efficient and accurate cross-language translation.
- Research how to introduce adversarial training methods into the Transformer to improve its robustness against adversarial attacks.

Related Papers:

[1] [Convolutional Sequence to Sequence Learning](https://www.semanticscholar.org/paper/43428880d75b3a14257c3ee9bda054e61eb869c0)

[2] [Massive Exploration of Neural Machine Translation Architectures](https://www.semanticscholar.org/paper/4550a4c714920ef57d19878e31c9ebae37b049b2)

[3] [A Structured Self-attentive Sentence Embedding](https://www.semanticscholar.org/paper/204a4a70428f3938d2c538a4d74c7ae0416306d8)

[4] [Factorization tricks for LSTM networks](https://www.semanticscholar.org/paper/79baf48bd560060549998d7b61751286de062e2a)

[5] [Structured Attention Networks](https://www.semanticscholar.org/paper/13d9323a8716131911bfda048a40e2cde1a76a46)

[6] [Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](https://www.semanticscholar.org/paper/510e26733aaff585d65701b9f1be7ca9d5afc586)

[7] [Neural Machine Translation in Linear Time](https://www.semanticscholar.org/paper/98445f4172659ec5e891e031d8202c102135c644)

[8] [Can Active Memory Replace Attention?](https://www.semanticscholar.org/paper/735d547fc75e0772d2a78c46a1cc5fad7da1474c)

[9] [Xception: Deep Learning with Depthwise Separable Convolutions](https://www.semanticscholar.org/paper/5b6ec746d309b165f9f9def873a2375b6fb40f3d)

[10] [Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation](https://www.semanticscholar.org/paper/dbde7dfa6cae81df8ac19ef500c42db96c3d1edd)


```

The output result is formatted in markdown format, making it suitable for rendering and display.

Furthermore, the example above involves multiple steps of LLM inference (four inference processes) and multiple API calls (retrieving paper and citation data from Arxiv and Semantic Scholar), but the event bus parallel mechanism of `prompulate` greatly simplifies the total inference time, maintaining an average inference time of around ten seconds (specific events depend on the network environment).

Due to the use of parallel mechanisms, when using a Tool or Agent with LLM capabilities, you will rapidly make multiple API calls simultaneously. If you encounter rate limit issues with your key, we recommend using the [key-pool](/modules/llm/llm.md#key-pool) to solve key rate limit problems (if you have a $5 key).
