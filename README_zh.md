<h1 align="center">
    Promptulate
</h1>

<p align="center">
    <a target="_blank" href="">
        <img src="https://img.shields.io/github/license/Undertone0809/promptulate.svg?style=flat-square" />
    </a>
    <a target="_blank" href=''>
        <img src="https://img.shields.io/github/release/Undertone0809/promptulate/all.svg?style=flat-square"/>
    </a>
    <a target="_blank" href=''>
        <img src="https://bestpractices.coreinfrastructure.org/projects/3018/badge"/>
   </a>
    <a target="_blank" href=''>
        <img src="https://static.pepy.tech/personalized-badge/promptulate?period=month&units=international_system&left_color=grey&right_color=blue&left_text=Downloads/Week"/>
    </a>
</p>

<p align="center">
  <img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/promptulate_logo_new.png"/>
</p>

## Overview

**Promptulate** 是 **Cogit Lab** 打造的 AI Agent 应用开发框架，通过 Pythonic 的开发范式，旨在为开发者们提供一种极其简洁而高效的 Agent 应用构建体验。 🛠️ Promptulate 的核心理念在于借鉴并融合开源社区的智慧，集成各种开发框架的亮点，以此降低开发门槛并统一开发者的共识。通过 Promptulate，你可以用最简洁的代码来操纵 LLM, Agent, Tool, RAG 等组件，大多数任务仅需几行代码即可轻松完成。🚀

## 💡特性

- 🐍 Pythonic Code Style: 采用 Python 开发者的习惯，提供 Pythonic 的 SDK 调用方式，一切尽在掌握，仅需一个 pne.chat 函数便可封装所有必需功能。
- 🧠 模型兼容性: 支持市面上几乎所有类型的大模型，并且可以轻松自定义模型以满足特定需求。
- 🤖 取代OpenAI SDK：你不再需要使用 openai sdk，核心功能都可以使用 pne.chat 来替代，并且提供增强特性，简化开发难度。
- 🕵️‍♂️ 多样化 Agent: 提供 WebAgent、ToolAgent、CodeAgent 等多种类型的 Agent，具备计划、推理、行动等处理复杂问题的能力，原子化 Planner 等组件。
- 🔗 低成本集成: 轻而易举地集成如 LangChain 等不同框架的工具，大幅降低集成成本。
- 🔨 函数即工具: 将任意 Python 函数直接转化为 Agent 可用的工具，简化了工具的创建和使用过程。
- 🪝 生命周期与钩子: 提供丰富的 Hook 和完善的生命周期管理，允许在 Agent、Tool、LLM 的各个阶段插入自定义代码。
- 💻 终端集成: 轻松集成应用终端，自带客户端支持，提供 prompt 的快速调试能力。
- ⏱️ Prompt 缓存: 提供 LLM Prompt 缓存机制，减少重复工作，提升开发效率。

> 下面用 pne 表示 promptulate，pne 是 Promptulate 的昵称，其中 p 和 e 分别代表 promptulate 的开头和结尾，n 代表 9，即 p 和 e 中间的九个字母的简写。

## 支持的基础模型

pne 集成了 [litellm](https://github.com/BerriAI/litellm) 的能力，支持几乎市面上所有类型的大模型，包括但不限于以下模型：

| Provider      | [Completion](https://docs.litellm.ai/docs/#basic-usage) | [Streaming](https://docs.litellm.ai/docs/completion/stream#streaming-responses)  | [Async Completion](https://docs.litellm.ai/docs/completion/stream#async-completion)  | [Async Streaming](https://docs.litellm.ai/docs/completion/stream#async-streaming)  | [Async Embedding](https://docs.litellm.ai/docs/embedding/supported_embedding)  | [Async Image Generation](https://docs.litellm.ai/docs/image_generation)  | 
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| [openai](https://docs.litellm.ai/docs/providers/openai)  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| [azure](https://docs.litellm.ai/docs/providers/azure)  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| [aws - sagemaker](https://docs.litellm.ai/docs/providers/aws_sagemaker)  | ✅ | ✅ | ✅ | ✅ | ✅ |
| [aws - bedrock](https://docs.litellm.ai/docs/providers/bedrock)  | ✅ | ✅ | ✅ | ✅ |✅ |
| [google - vertex_ai [Gemini]](https://docs.litellm.ai/docs/providers/vertex)  | ✅ | ✅ | ✅ | ✅ |
| [google - palm](https://docs.litellm.ai/docs/providers/palm)  | ✅ | ✅ | ✅ | ✅ |
| [google AI Studio - gemini](https://docs.litellm.ai/docs/providers/gemini)  | ✅ |  | ✅ |  | |
| [mistral ai api](https://docs.litellm.ai/docs/providers/mistral)  | ✅ | ✅ | ✅ | ✅ | ✅ |
| [cloudflare AI Workers](https://docs.litellm.ai/docs/providers/cloudflare_workers)  | ✅ | ✅ | ✅ | ✅ |
| [cohere](https://docs.litellm.ai/docs/providers/cohere)  | ✅ | ✅ | ✅ | ✅ | ✅ |
| [anthropic](https://docs.litellm.ai/docs/providers/anthropic)  | ✅ | ✅ | ✅ | ✅ |
| [huggingface](https://docs.litellm.ai/docs/providers/huggingface)  | ✅ | ✅ | ✅ | ✅ | ✅ |
| [replicate](https://docs.litellm.ai/docs/providers/replicate)  | ✅ | ✅ | ✅ | ✅ |
| [together_ai](https://docs.litellm.ai/docs/providers/togetherai)  | ✅ | ✅ | ✅ | ✅ |
| [openrouter](https://docs.litellm.ai/docs/providers/openrouter)  | ✅ | ✅ | ✅ | ✅ |
| [ai21](https://docs.litellm.ai/docs/providers/ai21)  | ✅ | ✅ | ✅ | ✅ |
| [baseten](https://docs.litellm.ai/docs/providers/baseten)  | ✅ | ✅ | ✅ | ✅ |
| [vllm](https://docs.litellm.ai/docs/providers/vllm)  | ✅ | ✅ | ✅ | ✅ |
| [nlp_cloud](https://docs.litellm.ai/docs/providers/nlp_cloud)  | ✅ | ✅ | ✅ | ✅ |
| [aleph alpha](https://docs.litellm.ai/docs/providers/aleph_alpha)  | ✅ | ✅ | ✅ | ✅ |
| [petals](https://docs.litellm.ai/docs/providers/petals)  | ✅ | ✅ | ✅ | ✅ |
| [ollama](https://docs.litellm.ai/docs/providers/ollama)  | ✅ | ✅ | ✅ | ✅ |
| [deepinfra](https://docs.litellm.ai/docs/providers/deepinfra)  | ✅ | ✅ | ✅ | ✅ |
| [perplexity-ai](https://docs.litellm.ai/docs/providers/perplexity)  | ✅ | ✅ | ✅ | ✅ |
| [Groq AI](https://docs.litellm.ai/docs/providers/groq)  | ✅ | ✅ | ✅ | ✅ |
| [anyscale](https://docs.litellm.ai/docs/providers/anyscale)  | ✅ | ✅ | ✅ | ✅ |
| [voyage ai](https://docs.litellm.ai/docs/providers/voyage)  |  |  |  |  | ✅ |
| [xinference [Xorbits Inference]](https://docs.litellm.ai/docs/providers/xinference)  |  |  |  |  | ✅ |

更多支持的模型，可以在 [litellm documentation](https://docs.litellm.ai/docs/providers) 查看。

你可以使用下面的方式十分轻松的构建起任何第三方模型的调用。

```python
import promptulate as pne

resp: str = pne.chat(model="ollama/llama2", messages = [{ "content": "Hello, how are you?","role": "user"}])
```

### News 

🌟 2024.5.14 OpenAI 推出了他们最新的 “omni” 模型，与 turbo 相比，它提供了更高的速度和价格，你可以在任何 pne 应用程序中使用它的多模态功能。

```python
import promptulate as pne

messages=[
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image_url",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
            },
        ],
    }
]

resp = pne.chat(model="gpt-4o", messages=messages)
print(resp)
```

## 📗 相关文档

- [快速上手/官方文档](https://undertone0809.github.io/promptulate/#/)
- [当前开发计划](https://undertone0809.github.io/promptulate/#/other/plan)
- [参与贡献/开发者手册](https://undertone0809.github.io/promptulate/#/other/contribution)
- [常见问题](https://undertone0809.github.io/promptulate/#/other/faq)
- [pypi仓库](https://pypi.org/project/promptulate/)

## 📝 Examples

- [Build a math application with agent [Steamlit, ToolAgent, Hooks].](https://github.com/Undertone0809/promptulate/tree/main/example/build-math-application-with-agent)
- [A Mulitmodal Robot Agent framework of ROS2 and Promptulate [Agent]](https://github.com/Undertone0809/Athena)
- [Use streamlit and pne to compare different model a playground. [Streamlit]](https://github.com/Undertone0809/pne-playground-model-comparison)

## 🛠 快速开始

- 打开终端，输入以下命令安装框架：

```shell script
pip install -U promptulate  
```

> 注意：Your Python version should be 3.8 or higher.

### 结构化输出

格式化输出是 LLM 应用开发鲁棒性的重要基础，我们希望 LLM 可以返回稳定的数据，使用 pne，你可以轻松的进行格式化输出，下面的示例中，我们使用 pydantic 的 BaseModel 封装起一个需要返回的数据结构。

```python
from typing import List
import promptulate as pne
from pydantic import BaseModel, Field

class LLMResponse(BaseModel):
    provinces: List[str] = Field(description="List of provinces name")

resp: LLMResponse = pne.chat("Please tell me all provinces in China.?", output_schema=LLMResponse)
print(resp)
```

**Output:**

```text
provinces=['Anhui', 'Fujian', 'Gansu', 'Guangdong', 'Guizhou', 'Hainan', 'Hebei', 'Heilongjiang', 'Henan', 'Hubei', 'Hunan', 'Jiangsu', 'Jiangxi', 'Jilin', 'Liaoning', 'Qinghai', 'Shaanxi', 'Shandong', 'Shanxi', 'Sichuan', 'Yunnan', 'Zhejiang', 'Taiwan', 'Guangxi', 'Nei Mongol', 'Ningxia', 'Xinjiang', 'Xizang', 'Beijing', 'Chongqing', 'Shanghai', 'Tianjin', 'Hong Kong', 'Macao']
```

### 取代 OpenAI SDK

很多第三方库可以使用 OpenAI SDK 调用它们的模型，如 [Deepseek](https://www.deepseek.com/)，有了 pne，你可以直接使用 pne.chat 函数来调用这些模型，而不需要再使用 OpenAI SDK，并且提供增强特性，简化开发难度，在 model 中使用 openai/xxx 的 provider 前缀，即可使用 OpenAI 的模型进行调用。

```python
import os
import promptulate as pne

os.environ["DEEPSEEK_API_KEY"] = "your api key"

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "How are you?"},
]
response = pne.chat(
    messages=messages,
    model="openai/deepseek-chat",
)
print(response)
```

当然，如果你想使用 Deepseek 的模型，你可以直接使用 `response = pne.chat(messages=messages, model="deepseek/deepseek-chat")` 的方式进行调用。

### 🧰 外部工具集成

在 pne，你可以轻松集成各种不同类型不同框架（如LangChain，llama-index）的 tools，如网络搜索、计算器等在外部工具，下面的示例中，我们使用 LangChain 的 duckduckgo 的搜索工具，来获取明天上海的天气。

```python
import os
import promptulate as pne
from langchain.agents import load_tools

os.environ["OPENAI_API_KEY"] = "your-key"

tools: list = load_tools(["ddg-search", "arxiv"])
resp: str = pne.chat(model="gpt-4-1106-preview", messages = [{ "content": "What is the temperature tomorrow in Shanghai","role": "user"}], tools=tools)
```

### 🤖 具有规划、工具调用、反思等能力的Agent

在这个示例中，pne 内部集成了拥有推理和反思能力的 [ReAct](https://arxiv.org/abs/2210.03629) 研究，封装成 ToolAgent，拥有强大的推理能力和工具调用能力，可以选择合适的工具进行调用，从而获取更加准确的结果。

**Output:**

```text
The temperature tomorrow in Shanghai is expected to be 23°C.
```

此外，受到 [Plan-and-Solve](https://arxiv.org/abs/2305.04091) 论文的影响，pne 还允许开发者构建具有计划、推理、行动等处理复杂问题的能力的 Agent，通过 enable_plan 参数，可以开启 Agent 的计划能力。

![plan-and-execute.png](./docs/images/plan-and-execute.png)

在这个例子中，我们使用 [Tavily](https://app.tavily.com/) 作为搜索引擎，它是一个强大的搜索引擎，可以从网络上搜索信息。要使用 Tavily，您需要从 Tavily 获得一个API密钥。

```python
import os

os.environ["TAVILY_API_KEY"] = "your_tavily_api_key"
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
```

在这个例子中，我们使用 LangChain 封装好的 TavilySearchResults Tool。

```python
from langchain_community.tools.tavily_search import TavilySearchResults

tools = [TavilySearchResults(max_results=5)]
```

```python
import promptulate as pne

pne.chat("what is the hometown of the 2024 Australia open winner?", model="gpt-4-1106-preview", enable_plan=True)
```

**Output:**

```text
[Agent] Assistant Agent start...
[User instruction] what is the hometown of the 2024 Australia open winner?
[Plan] {"goals": ["Find the hometown of the 2024 Australian Open winner"], "tasks": [{"task_id": 1, "description": "Identify the winner of the 2024 Australian Open."}, {"task_id": 2, "description": "Research the identified winner to find their place of birth or hometown."}, {"task_id": 3, "description": "Record the hometown of the 2024 Australian Open winner."}], "next_task_id": 1}
[Agent] Tool Agent start...
[User instruction] Identify the winner of the 2024 Australian Open.
[Thought] Since the current date is March 26, 2024, and the Australian Open typically takes place in January, the event has likely concluded for the year. To identify the winner, I should use the Tavily search tool to find the most recent information on the 2024 Australian Open winner.
[Action] tavily_search_results_json args: {'query': '2024 Australian Open winner'}
[Observation] [{'url': 'https://ausopen.com/articles/news/sinner-winner-italian-takes-first-major-ao-2024', 'content': 'The agile right-hander, who had claimed victory from a two-set deficit only once previously in his young career, is the second Italian man to achieve singles glory at a major, following Adriano Panatta in1976.With victories over Andrey Rublev, 10-time AO champion Novak Djokovic, and Medvedev, the Italian is the youngest player to defeat top 5 opponents in the final three matches of a major since Michael Stich did it at Wimbledon in 1991 – just weeks before Sinner was born.\n He saved the only break he faced with an ace down the tee, and helped by scoreboard pressure, broke Medvedev by slamming a huge forehand to force an error from his more experienced rival, sealing the fourth set to take the final to a decider.\n Sensing a shift in momentum as Medvedev served to close out the second at 5-3, Sinner set the RLA crowd alight with a pair of brilliant passing shots en route to creating a break point opportunity, which Medvedev snuffed out with trademark patience, drawing a forehand error from his opponent. “We are trying to get better every day, even during the tournament we try to get stronger, trying to understand every situation a little bit better, and I’m so glad to have you there supporting me, understanding me, which sometimes it’s not easy because I am a little bit young sometimes,” he said with a smile.\n Medvedev, who held to love in his first three service games of the second set, piled pressure on the Italian, forcing the right-hander to produce his best tennis to save four break points in a nearly 12-minute second game.\n'}, {'url': 'https://www.cbssports.com/tennis/news/australian-open-2024-jannik-sinner-claims-first-grand-slam-title-in-epic-comeback-win-over-daniil-medvedev/', 'content': '"\nOur Latest Tennis Stories\nSinner makes epic comeback to win Australian Open\nSinner, Sabalenka win Australian Open singles titles\n2024 Australian Open odds, Sinner vs. Medvedev picks\nSabalenka defeats Zheng to win 2024 Australian Open\n2024 Australian Open odds, Sabalenka vs. Zheng picks\n2024 Australian Open odds, Medvedev vs. Zverev picks\nAustralian Open odds: Djokovic vs. Sinner picks, bets\nAustralian Open odds: Gauff vs. Sabalenka picks, bets\nAustralian Open odds: Zheng vs. Yastremska picks, bets\nNick Kyrgios reveals he\'s contemplating retirement\n© 2004-2024 CBS Interactive. Jannik Sinner claims first Grand Slam title in epic comeback win over Daniil Medvedev\nSinner, 22, rallied back from a two-set deficit to become the third ever Italian Grand Slam men\'s singles champion\nAfter almost four hours, Jannik Sinner climbed back from a two-set deficit to win his first ever Grand Slam title with an epic 3-6, 3-6, 6-4, 6-4, 6-3 comeback victory against Daniil Medvedev. Sinner became the first Italian man to win the Australian Open since 1976, and just the eighth man to successfully come back from two sets down in a major final.\n He did not drop a single set until his meeting with Djokovic, and that win in itself was an accomplishment as Djokovic was riding a 33-match winning streak at the Australian Open and had never lost a semifinal in Melbourne.\n @janniksin • @wwos • @espn • @eurosport • @wowowtennis pic.twitter.com/DTCIqWoUoR\n"We are trying to get better everyday, and even during the tournament, trying to get stronger and understand the situation a little bit better," Sinner said.'}, {'url': 'https://www.bbc.com/sport/tennis/68120937', 'content': 'Live scores, results and order of play\nAlerts: Get tennis news sent to your phone\nRelated Topics\nTop Stories\nFA Cup: Blackburn Rovers v Wrexham - live text commentary\nRussian skater Valieva given four-year ban for doping\nLinks to Barcelona are \'totally untrue\' - Arteta\nElsewhere on the BBC\nThe truth behind the fake grooming scandal\nFeaturing unseen police footage and interviews with the officers at the heart of the case\nDid their father and uncle kill Nazi war criminals?\n A real-life murder mystery following three brothers in their quest for the truth\nWhat was it like to travel on the fastest plane?\nTake a behind-the-scenes look at the supersonic story of the Concorde\nToxic love, ruthless ambition and shocking betrayal\nTell Me Lies follows a passionate college relationship with unimaginable consequences...\n "\nMarathon man Medvedev runs out of steam\nMedvedev is the first player to lose two Grand Slam finals after winning the opening two sets\nSo many players with the experience of a Grand Slam final have talked about how different the occasion can be, particularly if it is the first time, and potentially overwhelming.\n Jannik Sinner beats Daniil Medvedev in Melbourne final\nJannik Sinner is the youngest player to win the Australian Open men\'s title since Novak Djokovic in 2008\nJannik Sinner landed the Grand Slam title he has long promised with an extraordinary fightback to beat Daniil Medvedev in the Australian Open final.\n "\nSinner starts 2024 in inspired form\nSinner won the first Australian Open men\'s final since 2005 which did not feature Roger Federer, Rafael Nadal or Novak Djokovic\nSinner was brought to the forefront of conversation when discussing Grand Slam champions in 2024 following a stunning end to last season.\n'}]
[Execute Result] {'thought': "The search results have provided consistent information about the winner of the 2024 Australian Open. Jannik Sinner is mentioned as the winner in multiple sources, which confirms the answer to the user's question.", 'action_name': 'finish', 'action_parameters': {'content': 'Jannik Sinner won the 2024 Australian Open.'}}
[Execute] Execute End.
[Revised Plan] {"goals": ["Find the hometown of the 2024 Australian Open winner"], "tasks": [{"task_id": 2, "description": "Research Jannik Sinner to find his place of birth or hometown."}, {"task_id": 3, "description": "Record the hometown of Jannik Sinner, the 2024 Australian Open winner."}], "next_task_id": 2}
[Agent] Tool Agent start...
[User instruction] Research Jannik Sinner to find his place of birth or hometown.
[Thought] To find Jannik Sinner's place of birth or hometown, I should use the search tool to find the most recent and accurate information.
[Action] tavily_search_results_json args: {'query': 'Jannik Sinner place of birth hometown'}
[Observation] [{'url': 'https://www.sportskeeda.com/tennis/jannik-sinner-nationality', 'content': "During the semifinal of the Cup, Sinner faced Djokovic for the third time in a row and became the first player to defeat him in a singles match. Jannik Sinner Nationality\nJannik Sinner is an Italian national and was born in Innichen, a town located in the mainly German-speaking area of South Tyrol in northern Italy. A. Jannik Sinner won his maiden Masters 1000 title at the 2023 Canadian Open defeating Alex de Minaur in the straight sets of the final.\n Apart from his glorious triumph at Melbourne Park in 2024, Jannik Sinner's best Grand Slam performance came at the 2023 Wimbledon, where he reached the semifinals. In 2020, Sinner became the youngest player since Novak Djokovic in 2006 to reach the quarter-finals of the French Open."}, {'url': 'https://en.wikipedia.org/wiki/Jannik_Sinner', 'content': "At the 2023 Australian Open, Sinner lost in the 4th round to eventual runner-up Stefanos Tsitsipas in 5 sets.[87]\nSinner then won his seventh title at the Open Sud de France in Montpellier, becoming the first player to win a tour-level title in the season without having dropped a single set and the first since countryman Lorenzo Musetti won the title in Naples in October 2022.[88]\nAt the ABN AMRO Open he defeated top seed and world No. 3 Stefanos Tsitsipas taking his revenge for the Australian Open loss, for his biggest win ever.[89] At the Cincinnati Masters, he lost in the third round to Félix Auger-Aliassime after being up a set, a break, and 2 match points.[76]\nSeeded 11th at the US Open, he reached the fourth round after defeating Brandon Nakashima in four sets.[77] Next, he defeated Ilya Ivashka in a five set match lasting close to four hours to reach the quarterfinals for the first time at this Major.[78] At five hours and 26 minutes, it was the longest match of Sinner's career up until this point and the fifth-longest in the tournament history[100] as well as the second longest of the season after Andy Murray against Thanasi Kokkinakis at the Australian Open.[101]\nHe reached back to back quarterfinals in Wimbledon after defeating Juan Manuel Cerundolo, Diego Schwartzman, Quentin Halys and Daniel Elahi Galan.[102] He then reached his first Major semifinal after defeating Roman Safiullin, before losing to Novak Djokovic in straight sets.[103] In the following round in the semifinals, he lost in straight sets to career rival and top seed Carlos Alcaraz who returned to world No. 1 following the tournament.[92] In Miami, he reached the quarterfinals of this tournament for a third straight year after defeating Grigor Dimitrov and Andrey Rublev, thus returning to the top 10 in the rankings at world No. In the final, he came from a two-set deficit to beat Daniil Medvedev to become the first Italian player, male or female, to win the Australian Open singles title, and the third man to win a Major (the second of which is in the Open Era), the first in 48 years.[8][122]"}, {'url': 'https://www.thesportreview.com/biography/jannik-sinner/', 'content': 'â€¢ Date of birth: 16 August 2001\nâ€¢ Age: 22 years old\nâ€¢ Place of birth: San Candido, Italy\nâ€¢ Nationality: Italian\nâ€¢ Height: 188cm / 6ft 2ins\nâ€¢ Weight: 76kg / 167lbs\nâ€¢ Plays: Right-handed\nâ€¢ Turned Pro: 2018\nâ€¢ Career Prize Money: US$ 4,896,338\nâ€¢ Instagram: @janniksin\nThe impressive 22-year-old turned professional back in 2018 and soon made an impact on the tour, breaking into the top 100 in the world rankings for the first time in 2019.\n Jannik Sinner (Photo: Dubai Duty Free Tennis Championships)\nSinner ended the season as number 78 in the world, becoming the youngest player since Rafael Nadal in 2003 to end the year in the top 80.\n The Italian then ended the 2019 season in style, qualifying for the 2019 Next Gen ATP Finals and going on to win the tournament with a win over Alex de Minaur in the final.\n Sinner then reached the main draw of a grand slam for the first time at the 2019 US Open, when he came through qualifying to reach the first round, where he lost to Stan Wawrinka.\n Asked to acknowledge some of the key figures in his development, Sinner replied: “I think first of all, my family who always helped me and gave me the confidence to actually change my life when I was 13-and-a-half, 14 years old.\n'}]
[Execute Result] {'thought': 'The search results have provided two different places of birth for Jannik Sinner: Innichen and San Candido. These are actually the same place, as San Candido is the Italian name and Innichen is the German name for the town. Since the user asked for the place of birth or hometown, I can now provide this information.', 'action_name': 'finish', 'action_parameters': {'content': 'Jannik Sinner was born in San Candido (Italian) / Innichen (German), Italy.'}}
[Execute] Execute End.
[Revised Plan] {"goals": ["Find the hometown of the 2024 Australian Open winner"], "tasks": [], "next_task_id": null}
[Agent Result] Jannik Sinner was born in San Candido (Italian) / Innichen (German), Italy.
[Agent] Agent End.
```

### 原子化 Agent 结构

在 Agent 开发的场景下，很多时候我们需要拆分出很多 Agent 的原子话组件，以达到更好地定制化效果，pne 提供了原子化的 Agent 组件，如 Planner，下面的实例展示了使用单独的 Planner 组件进行任务规划。

```python
import promptulate as pne

model = pne.LLMFactory.build("gpt-4-turbo")
planner = pne.Planner(model, system_prompt="You are a planner")
plans = planner.run("Plan a trip to Paris")
print(plans)
```

**输出：**

```text
('goals', ['Plan a trip to Paris'])
('tasks', [Task(task_id=1, description='Check passport validity', status=<TaskStatus.TODO: 'todo'>), Task(task_id=2, description='Determine travel dates', status=<TaskStatus.TODO: 'todo'>), Task(task_id=3, description='Research and book flights', status=<TaskStatus.TODO: 'todo'>), Task(task_id=4, description='Book accommodations', status=<TaskStatus.TODO: 'todo'>), Task(task_id=5, description='Plan itinerary for the trip', status=<TaskStatus.TODO: 'todo'>), Task(task_id=6, description='Investigate and purchase travel insurance', status=<TaskStatus.TODO: 'todo'>), Task(task_id=7, description='Set a budget for the trip', status=<TaskStatus.TODO: 'todo'>), Task(task_id=8, description='Pack luggage', status=<TaskStatus.TODO: 'todo'>), Task(task_id=9, description='Notify bank of international travel', status=<TaskStatus.TODO: 'todo'>), Task(task_id=10, description='Check weather forecast and pack accordingly', status=<TaskStatus.TODO: 'todo'>)])
('next_task_id', 1)
```

更多详细资料，请查看[快速上手/官方文档](https://undertone0809.github.io/promptulate/#/)

## 📚 设计原则

pne 框架的设计原则包括：模块化、可扩展性、互操作性、鲁棒性、可维护性、安全性、效率和可用性。

- 模块化是指以模块为基本单位，允许方便地集成新的组件、模型和工具。
- 可扩展性是指框架能够处理大量数据、复杂任务和高并发的能力。
- 互操作性是指该框架与各种外部系统、工具和服务兼容，并且能够实现无缝集成和通信。
- 鲁棒性是指框架具备强大的错误处理、容错和恢复机制，以确保在各种条件下可靠地运行。
- 安全性是指框架采用了严格的安全措施，以保护框架、其数据和用户免受未经授权访问和恶意行为的侵害。
- 效率是指优化框架的性能、资源使用和响应时间，以确保流畅和敏锐的用户体验。
- 可用性是指该框架采用用户友好的界面和清晰的文档，使其易于使用和理解。

以上原则的遵循，以及最新的人工智能技术的应用，`pne` 旨在为创建自动化代理提供强大而灵活的大语言模型应用开发框架。

## 💌 联系

欢迎加入群聊一起交流讨论 LLM & AI Agent 相关的话题，群里会不定期进行技术分享，链接过期了可以 issue 或 email 提醒一下作者。

<div style="width: 250px;margin: 0 auto;">
    <img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/pne_group.png"/>
</div>

For more information please contact: [zeeland4work@gmail.com](zeeland4work@gmail.com)

## ⭐ 贡献

我们感谢你有兴趣为我们的开源计划做出贡献。我们提供了[开发者指南](https://undertone0809.github.io/promptulate/#/other/contribution)，其中概述了为 Promptulate 做出贡献的步骤。请参阅本指南，以确保顺利合作和成功贡献，此外，你也可以查看[当前开发计划](https://undertone0809.github.io/promptulate/#/other/plan)查看最新的开发进展 🤝🚀
