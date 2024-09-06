# Client

`promptulate`为大语言模型对话提供了一个简易终端，在你安装了 `promptulate` 之后，你可以非常方便的使用这个简易终端进行一些对话，具体包括：

- 基于大模型的**简单对话**
- 选择特定工具进行 **Agent 对话**
- LLM + WebSearch 进行**基于网络搜索的对话**

![](../images/client_result_2.png)

## 快速上手

- 打开终端控制台，输入以下命令，可以查询当前项目的基本信息

```bash
pne
```

**output**

```
🌟 Welcome to Promptulate! 😀
Version: 1.9.1
Github repo: https://github.com/Undertone0809/promptulate
Official document: https://undertone0809.github.io/promptulate/#/
```


- 打开终端控制台，输入以下命令，就可以开启一个简易的对话

```shell
pne-chat --openai_api_key your_key_here --proxy_mode promptulate
```

```text

--openai_api_key 你的openai_api_key
--proxy_mode 代理模式，当前暂时只支持off和promptulate模式，如果你选择promptulate模式，你会发现你不用科学の上网也能访问，这是因为promptulate内置了代理。（后面会详细介绍）

```

- 当然并不是每次运行都要输入这么长的内容，因为在你第一次运行终端之后 `promptulate` 会对你的配置信息进行缓存，因此下一次运行的时候，你只需要输入下面的命令就可以开始一段对话了。如果你在代码运行中已经配置过相关的key参数，则可以直接使用以下方式运行：

```shell
pne-chat
```

- 然后你就可以随着 `pne`的引导进行操作

![](../images/client_result_1.png)

```text
Hi there, here is promptulate chat terminal.
? Choose a chat terminal: Web Agent Chat
? Choose a llm model: OpenAI
[User] 
上海明天多少度？
[agent]  The weather forecast for Shanghai tomorrow is expected to be partly cloudy with late night showers or thunderstorms. The temperature is expected to peak
 at 89 °F. Sun protection is strongly recommended as the UV index will be 8.
```

