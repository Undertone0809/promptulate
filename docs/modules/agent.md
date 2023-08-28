# Agent

Agent是`promptulate`的核心组件之一，其核心思想是使用llm、Tool、Memory、Provider,Output Parser等组件来构建起的一个可以处理复杂能力的代理。

## ToolAgent

下面的示例展示了如何使用`ToolAgent`结合Tool进行使用。

```python
from promptulate.tools import (
    DuckDuckGoTool,
    Calculator,
)
from promptulate.agents import ToolAgent


def main():
    tools = [
        DuckDuckGoTool(),
        Calculator(),
    ]
    agent = ToolAgent(tools)
    prompt = """Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"""
    agent.run(prompt)


if __name__ == "__main__":
    main()

```

运行结果如下：

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

Agent默认使用OpenAI的`gpt-3.5-turbo-16k`模型，如果你想要切换为其他模型，你可以使用如下方式进行配置：

```python
from promptulate.tools import (
    DuckDuckGoTool,
    Calculator,
)
from promptulate.llms import ErnieBot
from promptulate.agents import ToolAgent


def main():
    llm = ErnieBot(temperature=0.0)
    tools = [
        DuckDuckGoTool(),
        Calculator(),
    ]
    agent = ToolAgent(tools=tools,llm=llm)
    prompt = """Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"""
    agent.run(prompt)


if __name__ == "__main__":
    main()
```

## Tool

关于Tool的使用以及Promptulate兼容的工具，详情请查看[Tool 外部工具扩展](modules/tools.md#简介)


## 其他

控制台带有颜色输出的内容由`StdOutHook`驱动，你可以使用如下方式关闭：

```python
from promptulate.config import turn_off_stdout_hook

turn_off_stdout_hook()
```

如果你想要定制自己的独特Print或者对关键步骤进行逻辑处理，跳转 [Hook的使用](modules/hook.md#what-is-hook)

> 如果你当前正处在开发模式，十分推荐你使用enable_log()开启debug模式，从而查看最详细的底层日志信息，以便更好地记录运行过程。