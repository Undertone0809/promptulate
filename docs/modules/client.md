# Client

`promptulate`为大语言模型对话提供了一个简易终端，在你安装了了 `promptulate` 之后，你可以非常方便的使用这个简易终端进行一些对话，使用方式如下：

- 打开终端控制台，输入以下命令，就可以开启一个简易的对话

```shell
promptulate-chat --openai_api_key your_key_here --proxy_mode promptulate
```

```text

--openai_api_key 你的openai_api_key
--proxy_mode 代理模式，当前暂时只支持off和promptulate模式，如果你选择promptulate模式，你会发现你不用科学の上网也能访问，这是因为promptulate内置了代理。（后面会详细介绍）

```

- 当然并不是每次运行都要输入这么长的内容，因为在你第一次运行终端之后 `promptulate`
  会对你的配置信息进行缓存，因此下一次运行的时候，你只需要输入下面的命令就可以开始一段对话了

```shell
promptulate-chat
```

- 然后你就可以

```text
Hi there, here is promptulate chat terminal.
[User] 你好
[output] 你好！有什么我可以帮助你的吗？
[User] 只因你太美
[output] 谢谢夸奖，但作为一个语言模型，我没有真正的美丽，只有能力提供信息和帮助。那么，有什么问题或者需求我可以帮你解决 吗？
[User] 这真是太棒了
[output] 很高兴你觉得如此，我会尽力为您提供最佳的服务。有任何需要帮助的问题，请尽管问我。
```

> 需要注意的是，当前client只支持OpenAI的LLM，后续将会开放更多LLM，详情请查看[开发计划](../other/plan.md)
