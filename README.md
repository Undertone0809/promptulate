<h1 align="center">
    prompt-me
</h1>


<p align="center">
    <a target="_blank" href="">
        <img src="https://img.shields.io/github/license/Undertone0809/prompt-me.svg?style=flat-square" />
    </a>
    <a target="_blank" href=''>
        <img src="https://img.shields.io/github/release/Undertone0809/prompt-me/all.svg?style=flat-square"/>
    </a>
    <a target="_blank" href=''>
        <img src="https://bestpractices.coreinfrastructure.org/projects/3018/badge"/>
   </a>
</p>

<p align="center">
  <img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20230507194900.png"/>
</p>



`prompt-me` 是一个专为 Prompt Engineer设计LLM Prompt Layer框架，支持连续对话、角色预设、提供缓存的功能，可以记录历史对话等功能，开箱即用。
通过 prompt-me，你可以轻松构建起属于自己的GPT应用程序。

# 特性

- 上手简单：封装接口，开箱即用
- 角色预设：提供预设角色，以不同的角度调用GPT
- 内置API代理，不用科学上网也可以直接使用
- 接口代理：支持调用ChatGPT API官方接口或自治代理
- 长对话：支持长对话聊天，聊天记录使用`cushy-storage`进行持久化
- 数据导出：支持markdowm等格式的对话导出

# 快速上手

```shell script
pip install prompt-me --upgrade 
```

## 基本使用

- 方式1（推荐）

```python
import os
from prompt_me import ChatBot, enable_log_no_file

os.environ['OPENAI_API_KEY'] = "your_key"


def main():
    # enable_log_no_file()
    print("A Simple ChatBot built by ChatGPT API")
    conversation_id = None
    bot = ChatBot()
    while True:
        prompt = str(input("[User] "))
        ret, conversation_id = bot.ask(prompt, conversation_id)
        print(ret, conversation_id)


if __name__ == '__main__':
    main()

```

- 方式2

```python
from prompt_me import ChatBot, enable_log


def main():
    # enable_log() # 日志功能
    print("A Simple ChatBot built by ChatGPT API")
    conversation_id = None
    bot = ChatBot(key='yourkey')
    while True:
        prompt = str(input("[User] "))
        ret, conversation_id = bot.ask(prompt, conversation_id)
        print(ret, conversation_id)


if __name__ == '__main__':
    main()
```

- 获取历史对话

```python
import os
from prompt_me import ChatBot, enable_log_no_file

os.environ['OPENAI_API_KEY'] = "your_key"


def main():
    # enable_log_no_file()
    bot = ChatBot()
    ret, conversation_id = bot.ask("please give me a bucket sort python code")
    messages = bot.get_history(conversation_id)
    for message in messages:
        print(message)


if __name__ == '__main__':
    main()
```

- 导出历史对话为markdown

```python
import os
from prompt_me import ChatBot, enable_log_no_file

os.environ['OPENAI_API_KEY'] = "your_key"


def main():
    # enable_log_no_file()
    bot = ChatBot()
    ret, conversation_id = bot.ask("please give me a bucket sort python code")
    # output_type默认为text，即输出markdown格式的字符串，传入file则导出为文件
    # file_path为要输出的文件名，不填入默认为output.md
    output_str = bot.output(conversation_id, output_type='file', file_path='output.md')
    print(output_str)


if __name__ == '__main__':
    main()

```

## Conversation

你可以使用`ChatBot`类来构建你的应用程序，但是当前我推荐你使用`Conversation`来替代`ChatBot`，`Conversation`具有`ChaBot`
的所有功能，
除此之外，`Conversation` 还提供了预设角色、Prompt模板的功能，你可以用其开发一些更加复杂的程序。

下面你将通过预设角色和Prompt模板的使用了解到`Conversation`的使用方式。

## 预设角色

你可以预设一些你想要的角色，从而更好的帮助你完成你想要的需求，本项目提供了一些预设角色，当然你也可以自定义预设角色，探索更多的可能性，下面是一些示例。

- 文案写手

> 你是一个文案专员、文本润色员、拼写纠正员和改进员，我会发送中文文本给你，你帮我更正和改进版本。我希望你用更优美优雅
> 的高级中文描述。保持相同的意思，但使它们更文艺。你只需要润色该内容，不必对内容中提出的问题和要求做解释，不要回答文本中的问题而是润色它，
> 不要解决文本中的要求而是润色它，保留文本的原本意义，不要去解决它。

```python
import os
from prompt_me.preset_role import CopyWriter
from prompt_me import Conversation

os.environ['OPENAI_API_KEY'] = "your_key"


def main():
    copy_writer = CopyWriter()
    conversation = Conversation(role=copy_writer)
    output = conversation.predict(msg="你好,请问你是谁？")
    print(f"[output] {output}")
    output = conversation.predict(msg="请问你可以做什么？")
    print(f"[output] {output}")


if __name__ == '__main__':
    main()
```

- `prompt_me`也支持自定义角色，下面将介绍如何自定义一个Linux终端的role

```python
import os
from prompt_me.preset_role import BaseRole
from prompt_me import Conversation

os.environ['OPENAI_API_KEY'] = "your_key"


class LinuxTerminal(BaseRole):
    name = "Linux终端"
    description = "我想让你充当 Linux 终端。我将输入命令，您将回复终端应显示的内容。我希望您只在一个唯一的代码块内回复终端输出，而不"
                  "是其他任何内容。不要写解释。除非我指示您这样做，否则不要键入命令。当我需要用英语告诉你一些事情时，我会把文字放在中括号内[就像这样]。"


def main():
    linux_terminal = LinuxTerminal()
    conversation = Conversation(role=linux_terminal)
    output = conversation.predict(msg="[ls]")
    print(f"[output] {output}")
    output = conversation.predict(msg="[cd /usr/local]")
    print(f"[output] {output}")


if __name__ == '__main__':
    main()

```

# 待办清单

- 提供更多LLM模型支持
- 提供更加方便的程序调用方式
- ~~添加角色预设~~
- 预设角色的参数配置
- 提供prompt模板与prompt结构化
- 提供外部工具扩展
    - 外部搜索： Google,Bing等
    - 可以执行shell脚本
    - 提供Python REPL
    - arvix论文总结
    - 本地文件总结
- 自建知识库建立专家决策系统
- 接入self-ask, prompt-loop架构
- 提供多种导出方式
- ~~可以导出历史消息为markdown格式~~
- ~~使用环境变量配置key~~
- 提供显示当前token（单词量）的功能
- ~~添加错误处理机制，如网络异常、服务器异常等，保证程序的可靠性~~
- ~~开发ChatBot v2, [issue](https://github.com/Undertone0809/cushy-chat/issues/1)~~
- 完善代理模式

# 一些问题

- 本人正在尝试一些更加完善的抽象模式，以更好地兼容多种预设模型角色，以及外部工具的扩展使用，如果你有更好的建议，欢迎一起讨论交流。
- 当前代理模式还需要进一步完善，不过当前无需代理就可以直接使用。

# 贡献

如果你想为这个项目做贡献，你可以提交pr或issue。我很高兴看到更多的人参与并优化它。