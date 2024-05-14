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
    <a target="_blank" href=''>
        <img src="docs/images/coverage.svg"/>
    </a>
</p>

[English](/README.md) [中文](/README_zh.md)

<p align="center">
  <img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/promptulate_logo_new.png"/>
</p>

## Overview

**Promptulate** is an AI Agent application development framework crafted by **Cogit Lab**, which offers developers an extremely concise and efficient way to build Agent applications through a Pythonic development paradigm. The core philosophy of Promptulate is to borrow and integrate the wisdom of the open-source community, incorporating the highlights of various development frameworks to lower the barrier to entry and unify the consensus among developers. With Promptulate, you can manipulate components like LLM, Agent, Tool, RAG, etc., with the most succinct code, as most tasks can be easily completed with just a few lines of code. 🚀

## 💡 Features

- 🐍 Pythonic Code Style: Embraces the habits of Python developers, providing a Pythonic SDK calling approach, putting everything within your grasp with just one `pne.chat` function to encapsulate all essential functionalities.
- 🧠 Model Compatibility: Supports nearly all types of large models on the market and allows for easy customization to meet specific needs.
- 🕵️‍♂️ Diverse Agents: Offers various types of Agents, such as WebAgent, ToolAgent, CodeAgent, etc., capable of planning, reasoning, and acting to handle complex problems. Atomize the Planner and other components to simplify the development process.
- 🔗 Low-Cost Integration: Effortlessly integrates tools from different frameworks like LangChain, significantly reducing integration costs.
- 🔨 Functions as Tools: Converts any Python function directly into a tool usable by Agents, simplifying the tool creation and usage process.
- 🪝 Lifecycle and Hooks: Provides a wealth of Hooks and comprehensive lifecycle management, allowing the insertion of custom code at various stages of Agents, Tools, and LLMs.
- 💻 Terminal Integration: Easily integrates application terminals, with built-in client support, offering rapid debugging capabilities for prompts.
- ⏱️ Prompt Caching: Offers a caching mechanism for LLM Prompts to reduce repetitive work and enhance development efficiency.
- 🤖 Powerful OpenAI Wrapper: With pne, you no longer need to use the openai sdk, the core functions can be replaced with pne.chat, and provides enhanced features to simplify development difficulty.

> Below, `pne` stands for Promptulate, which is the nickname for Promptulate. The `p` and `e` represent the beginning and end of Promptulate, respectively, and `n` stands for 9, which is a shorthand for the nine letters between `p` and `e`.

## Supported Base Models

Promptulate integrates the capabilities of [litellm](https://github.com/BerriAI/litellm), supporting nearly all types of large models on the market, including but not limited to the following models:

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

For more models, please visit the [litellm documentation](https://docs.litellm.ai/docs/providers).

You can easily build any third-party model calls using the following method:


```python
import promptulate as pne

resp: str = pne.chat(model="ollama/llama2", messages=[{"content": "Hello, how are you?", "role": "user"}])
```

🌟 2024.5.14 OpenAI launched their newest "omni" model, offering improved speed and pricing compared to turbo.

You can use the available multimodal capabilities of it in any of your promptulate applications!

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

You can see how to use pne.chat in the [Getting Started/Official Documentation](https://undertone0809.github.io/promptulate/#/get_started/quick_start?id=quick-start).

## 📗 Related Documentation

- [Getting Started/Official Documentation](https://undertone0809.github.io/promptulate/#/)
- [Current Development Plan](https://undertone0809.github.io/promptulate/#/other/plan)
- [Contributing/Developer's Manual](https://undertone0809.github.io/promptulate/#/other/contribution)
- [Frequently Asked Questions](https://undertone0809.github.io/promptulate/#/other/faq)
- [PyPI Repository](https://pypi.org/project/promptulate/)

## 📝 Examples

- [Build a math application with agent [Steamlit, ToolAgent, Hooks].](https://github.com/Undertone0809/promptulate/tree/main/example/build-math-application-with-agent)
- [A Mulitmodal Robot Agent framework of ROS2 and Promptulate [Agent]](https://github.com/Undertone0809/Athena)
- [Use streamlit and pne to compare different model a playground. [Streamlit]](https://github.com/Undertone0809/pne-playground-model-comparison)

## 🛠 Quick Start

- Open the terminal and enter the following command to install the framework:

```shell script
pip install -U promptulate  
```

> Note: Your Python version should be 3.8 or higher.

Even though pne provides many modules, in 90% of LLM application development scenarios, you only need to use the pne.chat () function, so you only need to start with chat to understand the use of pne, and when you need to use additional modules, you can learn more about the features and use of other modules.

### Chat like OpenAI

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

### Replace the OpenAI SDK

Many third party libraries can use OpenAI SDK calls their models, such as [Deepseek](https://www.deepseek.com/). In pne, you can directly use `pne.chat()` function to call these models, It does not need to use the OpenAI SDK, and provides enhanced features to simplify the development difficulty. Use the `openai/xxx` provider prefix in the model, and you can use the OpenAI model to make calls.

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

### Structured Output

Robust output formatting is a fundamental basis for LLM application development. We hope that LLMs can return stable data. With pne, you can easily perform formatted output. In the following example, we use Pydantic's BaseModel to encapsulate a data structure that needs to be returned.

```python
from typing import List
import promptulate as pne
from pydantic import BaseModel, Field

class LLMResponse(BaseModel):
    provinces: List[str] = Field(description="List of provinces' names")

resp: LLMResponse = pne.chat("Please tell me all provinces in China.", output_schema=LLMResponse)
print(resp)
```

**Output:**

```text
provinces=['Anhui', 'Fujian', 'Gansu', 'Guangdong', 'Guizhou', 'Hainan', 'Hebei', 'Heilongjiang', 'Henan', 'Hubei', 'Hunan', 'Jiangsu', 'Jiangxi', 'Jilin', 'Liaoning', 'Qinghai', 'Shaanxi', 'Shandong', 'Shanxi', 'Sichuan', 'Yunnan', 'Zhejiang', 'Taiwan', 'Guangxi', 'Nei Mongol', 'Ningxia', 'Xinjiang', 'Xizang', 'Beijing', 'Chongqing', 'Shanghai', 'Tianjin', 'Hong Kong', 'Macao']
```

### Agent with Plan, Tool-Using and Reflection

Additionally, influenced by the [Plan-and-Solve](https://arxiv.org/abs/2305.04091) paper, pne also allows developers to build Agents capable of dealing with complex problems through planning, reasoning, and action. The Agent's planning abilities can be activated using the `enable_plan` parameter.

![plan-and-execute.png](./docs/images/plan-and-execute.png)

In this example, we use [Tavily](https://app.tavily.com/) as the search engine, which is a powerful tool for searching information on the web. To use Tavily, you need to obtain an API key from Tavily.

```python
import os

os.environ["TAVILY_API_KEY"] = "your_tavily_api_key"
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
```

In this case, we are using the TavilySearchResults Tool wrapped by LangChain.

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

### Atomize the Agent structure

In the scenario of Agent development, we often need to split many atomic components of agents to achieve better customization. pne provides atomized Agent components, such as Planner. The following example shows the use of a separate Planner component for task planning.

```python
import promptulate as pne

model = pne.LLMFactory.build("gpt-4-turbo")
planner = pne.Planner(model, system_prompt="You are a planner")
plans = planner.run("Plan a trip to Paris")
print(plans)
```

**Output:**

```text
('goals', ['Plan a trip to Paris'])
('tasks', [Task(task_id=1, description='Check passport validity', status=<TaskStatus.TODO: 'todo'>), Task(task_id=2, description='Determine travel dates', status=<TaskStatus.TODO: 'todo'>), Task(task_id=3, description='Research and book flights', status=<TaskStatus.TODO: 'todo'>), Task(task_id=4, description='Book accommodations', status=<TaskStatus.TODO: 'todo'>), Task(task_id=5, description='Plan itinerary for the trip', status=<TaskStatus.TODO: 'todo'>), Task(task_id=6, description='Investigate and purchase travel insurance', status=<TaskStatus.TODO: 'todo'>), Task(task_id=7, description='Set a budget for the trip', status=<TaskStatus.TODO: 'todo'>), Task(task_id=8, description='Pack luggage', status=<TaskStatus.TODO: 'todo'>), Task(task_id=9, description='Notify bank of international travel', status=<TaskStatus.TODO: 'todo'>), Task(task_id=10, description='Check weather forecast and pack accordingly', status=<TaskStatus.TODO: 'todo'>)])
('next_task_id', 1)
```

For more detailed information, please check the [Getting Started/Official Documentation](https://undertone0809.github.io/promptulate/#/).

## 📚 Design Principles

The design principles of the pne framework include modularity, extensibility, interoperability, robustness, maintainability, security, efficiency, and usability.

- Modularity refers to using modules as the basic unit, allowing for easy integration of new components, models, and tools.
- Extensibility refers to the framework's ability to handle large amounts of data, complex tasks, and high concurrency.
- Interoperability means the framework is compatible with various external systems, tools, and services and can achieve seamless integration and communication.
- Robustness indicates the framework has strong error handling, fault tolerance, and recovery mechanisms to ensure reliable operation under various conditions.
- Security implies the framework has implemented strict measures to protect against unauthorized access and malicious behavior.
- Efficiency is about optimizing the framework's performance, resource usage, and response times to ensure a smooth and responsive user experience.
- Usability means the framework uses user-friendly interfaces and clear documentation, making it easy to use and understand.

Following these principles and applying the latest artificial intelligence technologies, `pne` aims to provide a powerful and flexible framework for creating automated agents.

## 💌 Contact

For more information, please contact: [zeeland4work@gmail.com](mailto:zeeland4work@gmail.com)

## ⭐ Contribution

We appreciate your interest in contributing to our open-source initiative. We have provided a [Developer's Guide](https://undertone0809.github.io/promptulate/#/other/contribution) outlining the steps to contribute to Promptulate. Please refer to this guide to ensure smooth collaboration and successful contributions. Additionally, you can view the [Current Development Plan](https://undertone0809.github.io/promptulate/#/other/plan) to see the latest development progress 🤝🚀
