# Agent

The Agent is one of the core components of `promptulate`, its core idea is to build a proxy that can handle complex capabilities using components such as llm, Tool, Memory, Provider, and Output Formatter.

## ToolAgent

The following example demonstrates how to use `ToolAgent` in conjunction with Tool.

```python
import promptulate as pne
from promptulate.tools import DuckDuckGoTool, Calculator


def main():
    tools = [
        DuckDuckGoTool(),
        Calculator(),
    ]
    agent = pne.ToolAgent(tools=tools)
    prompt = """Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"""
    agent.run(prompt)


if __name__ == "__main__":
    main()

```

The output is as follows:

<img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20230828030207.png"/>

```text
Agent Start...
[user] Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?
[Action] ddg-search args: Leo DiCaprio's girlfriend
[Observation] Sarah Stier // Getty Images March 2021: They enjoy a beachside getaway. DiCaprio and Morrone headed to Malibu with friends for brief holiday. The actress shared photos from their trip to... His last relationship, with actor and model Camila Morrone, ended this past August, shortly after she turned 25. If there are two things people love, it's observing patterns, and having those... Celebrities. Vanessa Bryant remembers late husband, Kobe, on what would have been his 45th birthday Leonardo DiCaprio has once more found love. Aligning with his established preferences, the... Who is Leonardo DiCaprio's girlfriend? It's unknown if Leonardo DiCaprio is dating anyone at this time. However, he was spotted at Coachella dancing with model Irina Shayk. Shayk is Bradley... After more than four years of dating, Leonardo DiCaprio and Camila Morrone are going their separate ways. In August, multiple sources told PEOPLE that the longtime couple has broken up. The...
[Action] ddg-search args: Camila Morrone age
[Observation] Camila Morrone: her birthday, what she did before fame, her family life, fun trivia facts, popularity rankings, and more. Fun facts: before fame, family life, popularity rankings, and more. popular trending video trivia random Camila Morrone. Actress: Death Wish. Camila Morrone is an American model and actress. Morrone was born in Los Angeles, California to Argentine parents Lucila Solá and Máximo Morrone. Her mother is a former model and was a companion to actor Al Pacino, who is also her stepfather. Morrone started her career as a model and has appeared on the cover page of Vogue Turkey in 2016. However, Morrone — who is 23 years younger than DiCaprio — did comment on their age difference in December 2019, telling the Los Angeles Times, "I just think anyone should be able to date who... Two months ago she turned 25 and until recently she was in a relationship with Oscar winning actor Leonardo DiCaprio. In December 2017 her name went around the world, when rumors of romance with the actor began and especially because of the age difference between them. DiCaprio tends to date women between the ages of 20 and 25, prompting some to lose their minds over the mere possibility of his next girlfriend being born in the 2000s. "there's no phenomenon on...
[Action] math-calculator args: 25^0.43
[Observation] 3.991298452658078
[Agent Result]  Camila Morrone's current age raised to the 0.43 power is approximately 3.99.
Agent End.
```

If you want to switch to another model, you can configure it as follows using the latest `pne.LLMFactory` usage:

```python
import promptulate as pne
from promptulate.tools import DuckDuckGoTool, Calculator


def main():
    model = pne.LLMFactory.build(model_name="deepseek/deepseek", model_config={"temperature": 0.1})
    tools = [
        DuckDuckGoTool(),
        Calculator(),
    ]
    agent = pne.ToolAgent(tools=tools, llm=model)
    prompt = """Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"""
    agent.run(prompt)


if __name__ == "__main__":
    main()

## Tool

For more information on using Tool and compatible tools with Promptulate, please refer to [Tool External Tool Extension](modules/tools.md#简介)

## Other

The console output with color is driven by `StdOutHook`, which can be disabled as follows:

```python
from promptulate.config import turn_off_stdout_hook

turn_off_stdout_hook()
```

If you want to customize your own unique print or handle key steps logically, jump to [Hook Usage](/modules/hook.md#what-is-hook)

## WebAgent

The WebAgent encapsulated by `promptulate` allows you to easily access search engines and query related data. The following demonstrates its usage:

```python
import promptulate as pne


def main():
    agent = pne.WebAgent()
    agent.run("What's the temperature tomorrow in Shanghai?")


if __name__ == "__main__":
    main()

```

The output is as follows:

![](../images/agent_webagent_output.png)

## Custom Agent

You can customize an Agent as follows, which has a high degree of freedom. By inheriting `BaseAgent`, you can get the Hook lifecycle, making your custom Agent naturally have the AgentHook lifecycle. The following example demonstrates a simple custom Agent:

```python
import promptulate as pne

class CustomAgent(pne.BaseAgent):
    def __init__(self, llm: pne.BaseLLM, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.llm = llm

    def get_llm(self) -> pne.BaseLLM:
        return self.llm
        
    def _run(self, prompt: str, *args, **kwargs) -> str:
        return self.llm(prompt)


def main():
    llm = pne.ChatOpenAI()
    agent = CustomAgent(llm=llm)
    agent.run("The inevitable relationship between gravitational wave radiation and general relativity")


if __name__ == "__main__":
    main()
```

Inheriting `BaseAgent` requires implementing the `get_llm()` and `_run()` methods. The `get_llm()` method returns an LLM object, and the `_run()` method receives a prompt string, which is the user's input prompt for `agent.run()`, and returns the final result output by the Agent to the user.

The output is as follows:

![](../images/agent_custom_agent_output.png)

> In actual projects, you can freely extend the capabilities and boundaries of the Agent according to your business needs.
