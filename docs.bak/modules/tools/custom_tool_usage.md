# Custom Tool
Tool is a very important part of Agent. Agent can use tool to do many things, such as get data, process data, and so on. Agent has many built-in tools, but sometimes we need to customize our own tools. Now we will introduce how to custom tool in promptulate.

In promptulate, there are some methods to create tool for agent. Now we will introduce them one by one.


We aim to create the most straightforward development approach for developers. To integrate a tool with the language learning model (LLM), you may follow these steps:

In OpenAI's framework:
1. **Implement the tool's logic**: Write the code that defines what your tool does.
2. **Declare the tool's schema**: Specify the structure and parameters of your tool.

In Langchain:
1. **Extend the `Tool` class**: Create a new class that inherits from `Tool`.
2. **Implement the `_run()` method**: This method should contain the operational logic of your tool.
3. **Define `name` and `description` attributes**: These should clearly describe your tool's purpose and functionality.

In Promptulate:
1. **Provide your function**: Simply pass your function to Promptulate.
2. **Let Promptulate handle the rest**: Promptulate automatically takes care of the necessary configurations and integrations for your tool.

Promptulate simplifies the process, requiring minimal effort from the developer to make a tool functional with LLM. This is an awesome attempt we made, and we hope you will enjoy it! 

## Define your tool

We are going to use the following method to declare your tool. The following example show how to custom a web_search tool by function declared and use tool in ToolAgent. Here we use duckduckgo as search engine.


```python
import promptulate as pne
from promptulate.tools.duckduckgo.tools import DuckDuckGoTool


def web_search(keyword: str) -> str:
    """search by keyword in web.
    Args:
        keyword: keyword to search

    Returns:
        str: search result
    """
    return DuckDuckGoTool().run(keyword)


agent = pne.ToolAgent(tools=[web_search])
resp: str = agent.run("How will the temperature be in New York tomorrow?")
```

```text
Agent Start...
[User] What's the weather in NewYork tomorrow?
[Thought] I need to find out the weather in New York tomorrow.
[Action] web_search args: {'keyword': 'weather forecast New York tomorrow'}
[Observation] Hourly 10-Day Calendar History Wundermap access_time 6:06 PM EST on January 7, 2024 (GMT -5) | Updated 36 minutes ago --° | 33° 36 °F like 36° Cloudy N 0 Tomorrow's temperature is forecast to... News Headlines Briefing on the Winter Storm for this Weekend MY FORECAST Central Park NY Fair 32°F 0°C Today Sunny High: 38°F Tonight Increasing Clouds Low: 29°F change location New York, NY Weather Forecast Office NWS Forecast Office New York, NY Weather.gov > New York, NY Current Hazards Current Conditions Radar Forecasts Rivers and Lakes The National Weather Service issued winter storm warnings for a number of counties in the tri-state area, including Warren, Sussex, Morris, and northern Bergen counties, along with Rockland,... New York (United States of America) weather - Met Office Search Today 2° -3° Partly cloudy changing to clear by nighttime. Sunrise: 07:21 Sunset: 16:42 L UV Sat 6 Jan 2° 1° Sun 7 Jan 3° 0° Mon... New York detailed weather forecast for tomorrow hourly, Weather in New York tomorrow - accurate weather forecast. En Es . Widgets for website . Weather in United States New York . Today Tomorrow 3 Days 7 Days 10 Days Weekend . Weather in New York tomorrow. Sunday, 31 December 2023 . Day 1:00 PM
[Agent Result] The weather in New York tomorrow will be partly cloudy changing to clear by nighttime.
Agent End.
```

As you can see, the only you need to do is to provide a function to Promptulate. Promptulate will automatically convert it to a tool that can be used by the language learning model (LLM). The final presentation result it presents to LLM is an OpenAI type JSON schema declaration.

Actually, Promptulate will analysis function name, parameters type, parameters attribution, annotations and docs when you provide the function. We strongly recommend that you use the official best practices of Template for function writing. The best implementation of a function requires adding type declarations to its parameters and providing function level annotations. Ideally, declare the meaning of each parameter within the annotations. 

If you want to see json schema of your function, you can use the following method to get it.


```python
import json
from promptulate.tools.base import function_to_tool_schema


def web_search(keyword: str) -> str:
    """search by keyword in web.
    Args:
        keyword: keyword to search

    Returns:
        str: search result
    """
    return "web search result"


schema = function_to_tool_schema(web_search)
print(json.dumps(schema, indent=2))
```

    {
      "type": "object",
      "properties": {
        "keyword": {
          "type": "string"
        }
      },
      "required": [
        "keyword"
      ],
      "description": "search by keyword in web.\n    Args:\n        keyword: keyword to search\n\n    Returns:\n        str: search result\n    ",
      "name": "web_search"
    }
    
