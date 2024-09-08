# Quick Start

Through this section of the tutorial, you can quickly get a comprehensive understanding of Promptulate, learn the basic usage of some commonly used modules. 

After reading this section, you can continue to read [Use Cases](/use_cases/intro.md#use-cases) and [example](https://github.com/Undertone0809/promptulate/tree/main/example) to learn some best practices for promptulate, to see how each module is used in case of a problem, Also welcome you in [issue](https://github.com/Undertone0809/promptulate/issues) for promptulate provide better advice.

## 1. Installation

Open a terminal and enter the following command to download the latest version of `promptulate`. `-U` means to update to the latest version. 

> If you have already downloaded the old version of `promptulate`, executing this command will update to the latest version. `promptulate` is currently in a rapid development stage, so you may need to update to the latest version frequently to enjoy the latest results.

```shell script
pip install -U pne
```

## 2. Basic Usage And Components

You don't need to know all the components of `promptulate` to get started. This section will introduce the basic usage of some commonly used components in `promptulate`, helping you quickly understand the architecture of `promptulate`. The quick start section only provides the simplest usage. If you have the need to develop complex applications, please jump to each module to read the detailed functions.

The following diagram shows the core architecture of `promptulate`:

![promptulate-architecture](../images/pne_arch.png)

### 2.1 Chat something by pne.chat()

`pne.chat()` is the most powerful function in pne. In actual LLM Agent application development, 90% of the functions can be built using it.

Now let's see how to use `pne.chat()` to chat with the model. The following example we use `gpt-4-turbo` to chat with the model.

```python
import os
import pne

os.environ["OPENAI_API_KEY"] = "your-api-key"

response: str = pne.chat(messages="What is the capital of China?", model="gpt-4-turbo")
```

```python
Beijing
```

It's easy, right?

For environment variable `OPENAI_API_KEY`, you can also import the key by creating a `.env` file, which is equivalent to the above configuration. [How to use env](https://github.com/theskumar/python-dotenv)

Create a `.env` file in the project root directory and fill in your key:

```text
OPENAI_API_KEY=sk-xxx
```

> For more pne.chat usage, see [here](/use_cases/chat_usage.md#chat).

### 2.2 Chat with structured output

The output of LLM has strong uncertainty. Pne provide the ability to get a structured object by LLM. The following example shows that if LLM strictly returns you an array listing all provinces in China. Here we use Pydantic to build a structured object.

```python
from typing import List
import promptulate as pne
from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    provinces: List[str] = Field(description="All provinces in China")


response: LLMResponse = pne.chat(
    messages="Please tell me all provinces in China.",
    model= "gpt-4-turbo",
    output_schema=LLMResponse
)
print(response.provinces)
```

```python
['Anhui', 'Fujian', 'Gansu', 'Guangdong', 'Guizhou', 'Hainan', 'Hebei', 'Heilongjiang', 'Henan', 'Hubei', 'Hunan', 'Jiangsu', 'Jiangxi', 'Jilin', 'Liaoning', 'Qinghai', 'Shaanxi', 'Shandong', 'Shanxi', 'Sichuan', 'Yunnan', 'Zhejiang', 'Taiwan', 'Guangxi', 'Nei Mongol', 'Ningxia', 'Xinjiang', 'Xizang', 'Beijing', 'Chongqing', 'Shanghai', 'Tianjin', 'Hong Kong', 'Macao']

```

### 2.3 Support for third-party models

You may wonder how to use `pne.chat()` to chat with other models, such as cohere or deepseek.

Promptulate integrates the capabilities of [litellm](https://github.com/BerriAI/litellm), supporting nearly all types of large models on the market, including but not limited to the following models:

| Provider                                                                            | [Completion](https://docs.litellm.ai/docs/#basic-usage) | [Streaming](https://docs.litellm.ai/docs/completion/stream#streaming-responses)  | [Async Completion](https://docs.litellm.ai/docs/completion/stream#async-completion)  | [Async Streaming](https://docs.litellm.ai/docs/completion/stream#async-streaming)  | [Async Embedding](https://docs.litellm.ai/docs/embedding/supported_embedding)  | [Async Image Generation](https://docs.litellm.ai/docs/image_generation)  | 
|-------------------------------------------------------------------------------------| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| [openai](https://docs.litellm.ai/docs/providers/openai)                             | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| [azure](https://docs.litellm.ai/docs/providers/azure)                               | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| [aws - sagemaker](https://docs.litellm.ai/docs/providers/aws_sagemaker)             | ✅ | ✅ | ✅ | ✅ | ✅ |
| [aws - bedrock](https://docs.litellm.ai/docs/providers/bedrock)                     | ✅ | ✅ | ✅ | ✅ |✅ |
| [google - vertex_ai [Gemini]](https://docs.litellm.ai/docs/providers/vertex)        | ✅ | ✅ | ✅ | ✅ |
| [google - palm](https://docs.litellm.ai/docs/providers/palm)                        | ✅ | ✅ | ✅ | ✅ |
| [google AI Studio - gemini](https://docs.litellm.ai/docs/providers/gemini)          | ✅ |  | ✅ |  | |
| [mistral ai api](https://docs.litellm.ai/docs/providers/mistral)                    | ✅ | ✅ | ✅ | ✅ | ✅ |
| [cloudflare AI Workers](https://docs.litellm.ai/docs/providers/cloudflare_workers)  | ✅ | ✅ | ✅ | ✅ |
| [cohere](https://docs.litellm.ai/docs/providers/cohere)                             | ✅ | ✅ | ✅ | ✅ | ✅ |
| [anthropic](https://docs.litellm.ai/docs/providers/anthropic)                       | ✅ | ✅ | ✅ | ✅ |
| [huggingface](https://docs.litellm.ai/docs/providers/huggingface)                   | ✅ | ✅ | ✅ | ✅ | ✅ |
| [replicate](https://docs.litellm.ai/docs/providers/replicate)                       | ✅ | ✅ | ✅ | ✅ |
| [together_ai](https://docs.litellm.ai/docs/providers/togetherai)                    | ✅ | ✅ | ✅ | ✅ |
| [openrouter](https://docs.litellm.ai/docs/providers/openrouter)                     | ✅ | ✅ | ✅ | ✅ |
| [ai21](https://docs.litellm.ai/docs/providers/ai21)                                 | ✅ | ✅ | ✅ | ✅ |
| [baseten](https://docs.litellm.ai/docs/providers/baseten)                           | ✅ | ✅ | ✅ | ✅ |
| [vllm](https://docs.litellm.ai/docs/providers/vllm)                                 | ✅ | ✅ | ✅ | ✅ |
| [nlp_cloud](https://docs.litellm.ai/docs/providers/nlp_cloud)                       | ✅ | ✅ | ✅ | ✅ |
| [aleph alpha](https://docs.litellm.ai/docs/providers/aleph_alpha)                   | ✅ | ✅ | ✅ | ✅ |
| [petals](https://docs.litellm.ai/docs/providers/petals)                             | ✅ | ✅ | ✅ | ✅ |
| [ollama](https://docs.litellm.ai/docs/providers/ollama)                             | ✅ | ✅ | ✅ | ✅ |
| [deepinfra](https://docs.litellm.ai/docs/providers/deepinfra)                       | ✅ | ✅ | ✅ | ✅ |
| [perplexity-ai](https://docs.litellm.ai/docs/providers/perplexity)                  | ✅ | ✅ | ✅ | ✅ |
| [Groq AI](https://docs.litellm.ai/docs/providers/groq)                              | ✅ | ✅ | ✅ | ✅ |
| [anyscale](https://docs.litellm.ai/docs/providers/anyscale)                         | ✅ | ✅ | ✅ | ✅ |
| [voyage ai](https://docs.litellm.ai/docs/providers/voyage)                          |  |  |  |  | ✅ |
| [xinference [Xorbits Inference]](https://docs.litellm.ai/docs/providers/xinference) |  |  |  |  | ✅ |
| [deepseek](https://www.deepseek.com/)                            | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

The powerful model support of pne allows you to easily build any third-party model calls.

Now let's see how to run local llama3 models of ollama with pne.

```python
import pne

resp: str = pne.chat(model="ollama/llama2", messages=[{"content": "Hello, how are you?", "role": "user"}])
```

Use `provider/model_name` to call the model, and you can easily build any third-party model calls.

For more models, please visit the [litellm documentation](https://docs.litellm.ai/docs/providers).

You can easily build any third-party model calls using the following method:


### Using tools

In pne, you can easily integrate various types of tools from different frameworks (such as LangChain, llama-index) as external tools, such as web search, calculators, etc. In the example below, we use LangChain's duckduckgo search tool to get tomorrow's weather in Shanghai.

```python
import os
import pne
from langchain.agents import load_tools

os.environ["OPENAI_API_KEY"] = "your-key"

tools: list = load_tools(["ddg-search", "arxiv"])
resp: str = pne.chat(model="gpt-4-1106-preview", messages = [{ "content": "What is the temperature tomorrow in Shanghai","role": "user"}], tools=tools)
```

In this example, pne internally integrates the [ReAct](https://arxiv.org/abs/2210.03629) research with reasoning and reflection capabilities, encapsulated as ToolAgent, which has powerful reasoning and tool invocation capabilities. It can choose appropriate tools to call, thereby obtaining more accurate results.

```python
The temperature tomorrow in Shanghai is expected to be 23°C.
```

Furthermore, influenced by the [Plan-and-Solve](https://arxiv.org/abs/2305.04091) paper, pne also allows developers to build Agents with the ability to plan, reason, and act to handle complex problems. Through the enable_plan parameter, you can enable the Agent's planning capability.

![plan-and-execute.png](./docs/images/plan-and-execute.png)

In this example, we use [Tavily](https://app.tavily.com/) as the search engine. It's a powerful search engine that can search for information from the web. To use Tavily, you need to obtain an API key from Tavily.

```python
import os

os.environ["TAVILY_API_KEY"] = "your_tavily_api_key"
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
```

In this example, we use the TavilySearchResults Tool packaged by LangChain.

```python
from langchain_community.tools.tavily_search import TavilySearchResults

tools = [TavilySearchResults(max_results=5)]
```

```python
import promptulate as pne

pne.chat("what is the hometown of the 2024 Australia open winner?", model="gpt-4-1106-preview", enable_plan=True)
```


```python
[Agent] Assistant Agent start...

[User instruction] what is the hometown of the 2024 Australia open winner?

[Plan] {"goals": ["Find the hometown of the 2024 Australian Open winner"], "tasks": [{"task_id": 1, "description": "Identify the winner of the 2024 Australian Open."}, {"task_id": 2, "description": "Research the identified winner to find their place of birth or hometown."}, {"task_id": 3, "description": "Record the hometown of the 2024 Australian Open winner."}], "next_task_id": 1}

[Agent] Tool Agent start...

[User instruction] Identify the winner of the 2024 Australian Open.

[Thought] Since the current date is March 26, 2024, and the Australian Open typically takes place in January, the event has likely concluded for the year. To identify the winner, I should use the Tavily search tool to find the most recent information on the 2024 Australian Open winner.

[Action] tavily_search_results_json args: {'query': '2024 Australian Open winner'}

[Observation] [{'url': 'https://ausopen.com/articles/news/sinner-winner-italian-takes-first-major-ao-2024', 'content': 'The agile right-hander, who had claimed victory from a two-set deficit only once previously in his young career, is the second Italian man to achieve singles glory at a major, following Adriano Panatta in1976.With victories over Andrey Rublev, 10-time AO champion Novak Djokovic, and Medvedev, the Italian is the youngest player to defeat top 5 opponents in the final three matches of a major since Michael Stich did it at Wimbledon in 1991 – just weeks before Sinner was born.\n He saved the only break he faced with an ace down the tee, and helped by scoreboard pressure, broke Medvedev by slamming a huge forehand to force an error from his more experienced rival, sealing the fourth set to take the final to a decider.\n Sensing a shift in momentum as Medvedev served to close out the second at 5-3, Sinner set the RLA crowd alight with a pair of brilliant passing shots en route to creating a break point opportunity, which Medvedev snuffed out with trademark patience, drawing a forehand error from his opponent. "We are trying to get better every day, even during the tournament we try to get stronger, trying to understand every situation a little bit better, and I'm so glad to have you there supporting me, understanding me, which sometimes it's not easy because I am a little bit young sometimes," he said with a smile.\n Medvedev, who held to love in his first three service games of the second set, piled pressure on the Italian, forcing the right-hander to produce his best tennis to save four break points in a nearly 12-minute second game.\n'}, {'url': 'https://www.cbssports.com/tennis/news/australian-open-2024-jannik-sinner-claims-first-grand-slam-title-in-epic-comeback-win-over-daniil-medvedev/', 'content': '"\nOur Latest Tennis Stories\nSinner makes epic comeback to win Australian Open\nSinner, Sabalenka win Australian Open singles titles\n2024 Australian Open odds, Sinner vs. Medvedev picks\nSabalenka defeats Zheng to win 2024 Australian Open\n2024 Australian Open odds, Sabalenka vs. Zheng picks\n2024 Australian Open odds, Medvedev vs. Zverev picks\nAustralian Open odds: Djokovic vs. Sinner picks, bets\nAustralian Open odds: Gauff vs. Sabalenka picks, bets\nAustralian Open odds: Zheng vs. Yastremska picks, bets\nNick Kyrgios reveals he\'s contemplating retirement\n© 2004-2024 CBS Interactive. Jannik Sinner claims first Grand Slam title in epic comeback win over Daniil Medvedev\nSinner, 22, rallied back from a two-set deficit to become the third ever Italian Grand Slam men\'s singles champion\nAfter almost four hours, Jannik Sinner climbed back from a two-set deficit to win his first ever Grand Slam title with an epic 3-6, 3-6, 6-4, 6-4, 6-3 comeback victory against Daniil Medvedev. Sinner became the first Italian man to win the Australian Open since 1976, and just the eighth man to successfully come back from two sets down in a major final.\n He did not drop a single set until his meeting with Djokovic, and that win in itself was an accomplishment as Djokovic was riding a 33-match winning streak at the Australian Open and had never lost a semifinal in Melbourne.\n @janniksin • @wwos • @espn • @eurosport • @wowowtennis pic.twitter.com/DTCIqWoUoR\n"We are trying to get better everyday, and even during the tournament, trying to get stronger and understand the situation a little bit better," Sinner said.'}, {'url': 'https://www.bbc.com/sport/tennis/68120937', 'content': 'Live scores, results and order of play\nAlerts: Get tennis news sent to your phone\nRelated Topics\nTop Stories\nFA Cup: Blackburn Rovers v Wrexham - live text commentary\nRussian skater Valieva given four-year ban for doping\nLinks to Barcelona are \'totally untrue\' - Arteta\nElsewhere on the BBC\nThe truth behind the fake grooming scandal\nFeaturing unseen police footage and interviews with the officers at the heart of the case\nDid their father and uncle kill Nazi war criminals?\n A real-life murder mystery following three brothers in their quest for the truth\nWhat was it like to travel on the fastest plane?\nTake a behind-the-scenes look at the supersonic story of the Concorde\nToxic love, ruthless ambition and shocking betrayal\nTell Me Lies follows a passionate college relationship with unimaginable consequences...\n "\nMarathon man Medvedev runs out of steam\nMedvedev is the first player to lose two Grand Slam finals after winning the opening two sets\nSo many players with the experience of a Grand Slam final have talked about how different the occasion can be, particularly if it is the first time, and potentially overwhelming.\n Jannik Sinner beats Daniil Medvedev in Melbourne final\nJannik Sinner is the youngest player to win the Australian Open men\'s title since Novak Djokovic in 2008\nJannik Sinner landed the Grand Slam title he has long promised with an extraordinary fightback to beat Daniil Medvedev in the Australian Open final.\n "\nSinner starts 2024 in inspired form\nSinner won the first Australian Open men\'s final since 2005 which did not feature Roger Federer, Rafael Nadal or Novak Djokovic\nSinner was brought to the forefront of conversation when discussing Grand Slam champions in 2024 following a stunning end to last season.\n'}]

[Execute Result] {'thought': "The search results have provided consistent information about the winner of the 2024 Australian Open. Jannik Sinner is mentioned as the winner in multiple sources, which confirms the answer to the user's question.", 'action_name': 'finish', 'action_parameters': {'content': 'Jannik Sinner won the 2024 Australian Open.'}}

[Execute] Execute End.

[Revised Plan] {"goals": ["Find the hometown of the 2024 Australian Open winner"], "tasks": [{"task_id": 2, "description": "Research Jannik Sinner to find his place of birth or hometown."}, {"task_id": 3, "description": "Record the hometown of Jannik Sinner, the 2024 Australian Open winner."}], "next_task_id": 2}

[Agent] Tool Agent start...

[User instruction] Research Jannik Sinner to find his place of birth or hometown.

[Thought] To find Jannik Sinner's place of birth or hometown, I should use the search tool to find the most recent and accurate information.

[Action] tavily_search_results_json args: {'query': 'Jannik Sinner place of birth hometown'}

[Observation] [{'url': 'https://www.sportskeeda.com/tennis/jannik-sinner-nationality', 'content': "During the semifinal of the Cup, Sinner faced Djokovic for the third time in a row and became the first player to defeat him in a singles match. Jannik Sinner Nationality\nJannik Sinner is an Italian national and was born in Innichen, a town located in the mainly German-speaking area of South Tyrol in northern Italy. A. Jannik Sinner won his maiden Masters 1000 title at the 2023 Canadian Open defeating Alex de Minaur in the straight sets of the final.\n Apart from his glorious triumph at Melbourne Park in 2024, Jannik Sinner's best Grand Slam performance came at the 2023 Wimbledon, where he reached the semifinals. In 2020, Sinner became the youngest player since Novak Djokovic in 2006 to reach the quarter-finals of the French Open."}, {'url': 'https://en.wikipedia.org/wiki/Jannik_Sinner', 'content': "At the 2023 Australian Open, Sinner lost in the 4th round to eventual runner-up Stefanos Tsitsipas in 5 sets.[87]\nSinner then won his seventh title at the Open Sud de France in Montpellier, becoming the first player to win a tour-level title in the season without having dropped a single set and the first since countryman Lorenzo Musetti won the title in Naples in October 2022.[88]\nAt the ABN AMRO Open he defeated top seed and world No. 3 Stefanos Tsitsipas taking his revenge for the Australian Open loss, for his biggest win ever.[89] At the Cincinnati Masters, he lost in the third round to Félix Auger-Aliassime after being up a set, a break, and 2 match points.[76]\nSeeded 11th at the US Open, he reached the fourth round after defeating Brandon Nakashima in four sets.[77] Next, he defeated Ilya Ivashka in a five set match lasting close to four hours to reach the quarterfinals for the first time at this Major.[78] At five hours and 26 minutes, it was the longest match of Sinner's career up until this point and the fifth-longest in the tournament history[100] as well as the second longest of the season after Andy Murray against Thanasi Kokkinakis at the Australian Open.[101]\nHe reached back to back quarterfinals in Wimbledon after defeating Juan Manuel Cerundolo, Diego Schwartzman, Quentin Halys and Daniel Elahi Galan.[102] He then reached his first Major semifinal after defeating Roman Safiullin, before losing to Novak Djokovic in straight sets.[103] In the following round in the semifinals, he lost in straight sets to career rival and top seed Carlos Alcaraz who returned to world No. 1 following the tournament.[92] In Miami, he reached the quarterfinals of this tournament for a third straight year after defeating Grigor Dimitrov and Andrey Rublev, thus returning to the top 10 in the rankings at world No. In the final, he came from a two-set deficit to beat Daniil Medvedev to become the first Italian player, male or female, to win the Australian Open singles title, and the third man to win a Major (the second of which is in the Open Era), the first in 48 years.[8][122]"}, {'url': 'https://www.thesportreview.com/biography/jannik-sinner/', 'content': 'â€¢ Date of birth: 16 August 2001\nâ€¢ Age: 22 years old\nâ€¢ Place of birth: San Candido, Italy\nâ€¢ Nationality: Italian\nâ€¢ Height: 188cm / 6ft 2ins\nâ€¢ Weight: 76kg / 167lbs\nâ€¢ Plays: Right-handed\nâ€¢ Turned Pro: 2018\nâ€¢ Career Prize Money: US$ 4,896,338\nâ€¢ Instagram: @janniksin\nThe impressive 22-year-old turned professional back in 2018 and soon made an impact on the tour, breaking into the top 100 in the world rankings for the first time in 2019.\n Jannik Sinner (Photo: Dubai Duty Free Tennis Championships)\nSinner ended the season as number 78 in the world, becoming the youngest player since Rafael Nadal in 2003 to end the year in the top 80.\n The Italian then ended the 2019 season in style, qualifying for the 2019 Next Gen ATP Finals and going on to win the tournament with a win over Alex de Minaur in the final.\n Sinner then reached the main draw of a grand slam for the first time at the 2019 US Open, when he came through qualifying to reach the first round, where he lost to Stan Wawrinka.\n Asked to acknowledge some of the key figures in his development, Sinner replied: "I think first of all, my family who always helped me and gave me the confidence to actually change my life when I was 13-and-a-half, 14 years old.\n'}]

[Execute Result] {'thought': 'The search results have provided two different places of birth for Jannik Sinner: Innichen and San Candido. These are actually the same place, as San Candido is the Italian name and Innichen is the German name for the town. Since the user asked for the place of birth or hometown, I can now provide this information.', 'action_name': 'finish', 'action_parameters': {'content': 'Jannik Sinner was born in San Candido (Italian) / Innichen (German), Italy.'}}

[Execute] Execute End.

[Revised Plan] {"goals": ["Find the hometown of the 2024 Australian Open winner"], "tasks": [], "next_task_id": null}

[Agent Result] Jannik Sinner was born in San Candido (Italian) / Innichen (German), Italy.

[Agent] Agent End.

```

### Client

`promptulate` provides a simple terminal for large language model conversations. After installing `promptulate`, you can easily use this simple terminal for some conversations, including:

- **Simple conversations** based on large models
- **Agent conversations** using specific tools
- **Web search-based conversations** using LLM + WebSearch

![](../images/client_result_2.png)

**Quick Start**

- Open the terminal console and enter the following command to start a simple conversation:

```shell
pne-chat
```

- Then you can follow `pne`'s guidance to operate

![](../images/client_result_1.png)

```text
Hi there, here is promptulate chat terminal.
? Choose a chat terminal: Web Agent Chat
? Choose a llm model: OpenAI
[User] 
What's the temperature in Shanghai tomorrow?
[agent]  The weather forecast for Shanghai tomorrow is expected to be partly cloudy with late night showers or thunderstorms. The temperature is expected to peak
 at 89 °F. Sun protection is strongly recommended as the UV index will be 8.
```

### Agent

Agent is one of the core components of `promptulate`. Its core idea is to build a proxy that can handle complex capabilities using components such as llm, Tool, Memory, Provider, Output Formatter, etc.

The following example shows how to use `ToolAgent` in combination with Tool.

```python
import pne
from promptulate.tools import (
    DuckDuckGoTool,
    Calculator,
)


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

The running result is as follows:

<img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20230828030207.png"/>

```python
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

To integrate a variety of external tools, including web search, calculators, and more, into your Python application, you can use the promptulate library alongside langchain. The langchain library allows you to build a ToolAgent with a collection of tools, such as an image generator based on OpenAI's DALL-E model. 

Below is an example of how to use the promptulate and langchain libraries to create an image from a text description:

> You need to set the `OPENAI_API_KEY` environment variable to your OpenAI API key. Click [here](https://undertone0809.github.io/promptulate/#/modules/tools/langchain_tool_usage?id=langchain-tool-usage) to see the detail.

```python
import pne
from langchain.agents import load_tools

tools: list = load_tools(["dalle-image-generator"])
agent = pne.ToolAgent(tools=tools)
output = agent.run("Create an image of a halloween night at a haunted museum")
```

```python
Here is the generated image: [![Halloween Night at a Haunted Museum](https://oaidalleapiprodscus.blob.core.windows.net/private/org-OyRC1wqD0EP6oWMS2n4kZgVi/user-JWA0mHqDqYh3oPpQtXbWUPgu/img-SH09tWkWZLJVltxifLi6jFy7.png)]

```

![Halloween Night at a Haunted Museum](./docs/images/dall-e-gen.png)

### Structured Output

The output of LLM has strong uncertainty. Pne provide the ability to get a structured object by LLM. The following example shows that if LLM strictly returns you an array listing all provinces in China. Here we use Pydantic to build a structured object.


```python
from typing import List
import promptulate as pne
from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    provinces: List[str] = Field(description="All provinces in China")


response: LLMResponse = pne.chat(
    messages="Please tell me all provinces in China.",
    model= "gpt-4-turbo",
    output_schema=LLMResponse
)
print(response.provinces)
```

```python
['Anhui', 'Fujian', 'Gansu', 'Guangdong', 'Guizhou', 'Hainan', 'Hebei', 'Heilongjiang', 'Henan', 'Hubei', 'Hunan', 'Jiangsu', 'Jiangxi', 'Jilin', 'Liaoning', 'Qinghai', 'Shaanxi', 'Shandong', 'Shanxi', 'Sichuan', 'Yunnan', 'Zhejiang', 'Taiwan', 'Guangxi', 'Nei Mongol', 'Ningxia', 'Xinjiang', 'Xizang', 'Beijing', 'Chongqing', 'Shanghai', 'Tianjin', 'Hong Kong', 'Macao']

```


For Agent, you can use the `output_schema` parameter to specify the output schema. The following example demonstrates the best practice of using formatted output in WebAgent:

```python
import pne
from pydantic import BaseModel, Field


class Response(BaseModel):
    city: str = Field(description="City name")
    temperature: float = Field(description="Temperature in Celsius")


def main():
    agent = pne.WebAgent()
    prompt = f"What is the temperature in Shanghai tomorrow?"
    response: Response = agent.run(prompt=prompt, output_schema=Response)
    print(response.city, response.temperature)


if __name__ == "__main__":
    main()
```

![img.png](../images/output_formatter_webagent_output.png)

## 3. Local Development

> You can go to [here](/other/contribution.md#contributing-to-promptulate) to see the detail.

**Environment Requirements**
- Python >= 3.8
- make

> This project uses make to build project supporting facilities, easily integrating running test, lint and other modules through the capability of makefile. Please make sure your computer has installed make.
> 
> [how to install and use make in windows?](https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows)


Run the following command:

```shell
git clone https://github.com/Undertone0809/promptulate 
```

After downloading to local, install third-party libraries

```shell
pip install poetry
make install
```

This project is equipped with code syntax checking tools. If you want to submit a PR, you need to run `make polish-codestyle` before committing to format the code specifications, and run `make lint` to pass the syntax and unit test checks.

## 4. More

This article only demonstrates some simple uses of `promtptulate`. For specific function details, please check the documentation for specific implementations.