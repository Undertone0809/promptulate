# Client

`promptulate` provides a simple terminal for large language model dialogues, making it very convenient to use this simple terminal for some dialogues after you install `promptulate`, including:

- **Simple dialogue** based on large models
- **Agent dialogue** with specific tool selection
- **Dialogue based on web search** with LLM + WebSearch

![](../images/client_result_2.png)

## Quick Start

- Open a terminal console and run the following command to query the basic information of the current project

```bash
pne
```

**output**

```
🌟 Welcome to Promptulate! 😀
Version: 1.18.3
Github repo: https://github.com/Undertone0809/promptulate
Official document: https://undertone0809.github.io/promptulate/#/
```


- Open a terminal console and enter the following command to start a simple dialogue

```shell
pne-chat --openai_api_key your_key_here --proxy_mode promptulate
```

```text

--openai_api_key your openai_api_key
--proxy_mode proxy mode, currently only supports off and promptulate modes, if you choose promptulate mode, you will find that you can access without a VPN, this is because promptulate has a built-in proxy. (More details will be introduced later)

```

- Of course, it's not necessary to input such a long content every time you run, because after you run the terminal for the first time, `promptulate` will cache your configuration information, so the next time you run, you only need to enter the following command to start a dialogue:

```shell
pne-chat
```

- Then you can follow the guide of `pne` to operate

![](../images/client_result_1.png)

```text
Hi there, here is promptulate chat terminal.
? Choose a chat terminal: Web Agent Chat
? Choose a llm model: OpenAI
[User] 
Shanghai tomorrow how many degrees？
[agent]  The weather forecast for Shanghai tomorrow is expected to be partly cloudy with late night showers or thunderstorms. The temperature is expected to peak
 at 89 °F. Sun protection is strongly recommended as the UV index will be 8.
```

