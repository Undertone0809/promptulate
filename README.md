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
</p>

<p align="center">
  <img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20230507194900.png"/>
</p>



`promptulate` 是一个专为 Prompt Engineer设计LLM Prompt Layer框架，支持连续对话、角色预设、对话总结、提供缓存的功能，可以记录历史对话等功能，开箱即用。
通过 promptulate，你可以轻松构建起属于自己的GPT应用程序。

本项目重构重构重构了两次，在本人深度阅读`langchain, Auto-GPT, django, django-rest-framework, gpt_academic...`
等大牛项目的源码之后，学习它们的架构、代码设计思路等内容，最终有了现在的版本，相较于之前的老版本`prompt-me`，`promptulate`
重新构建了 `llms, message, memory, framework, preset_roles, tools`等模块，将`prompt`
的各个流程全部组件化，便有了现在的`promptualte`框架，但是工作量很大，还在不断地完善细节中，欢迎大家的参与。

# 特性

- 大语言模型支持：支持不同类型的大语言模型的扩展接口（当前暂时只支持GPT）
- 角色预设：提供预设角色，以不同的角度调用GPT
- 内置API代理，不用科学上网也可以直接使用
- 接口代理：支持调用ChatGPT API官方接口或自治代理
- 长对话模式：支持长对话聊天，聊天记录使用`cushy-storage`进行持久化
- 数据导出：支持markdowm等格式的对话导出
- 对话总结：提供API式的对话总结、翻译、标题生成
- 高级抽象，支持插件扩展、存储扩展、大语言模型扩展

# 基础架构

在看了当前这么多`prompt-engineering`之后，本人的架构设计思想在`langchain, Auto-GPT`
之上进行不断改进，构建出了一套属于`promptualte`的LLM Prompt Layer框架。`promptulate` 由以下几部分组成：

- Agent 更高级的执行器，负责任务的调度和分发
- framework 框架层，实现不同类型的prompt框架
- llm 大语言模型，负责生成回答
- memory 负责对话的存储，支持不同的存储方式及其扩展
- tools 提供外部工具扩展调用，如搜索引擎、计算器等
- preset roles 提供预设角色
- provider 为framework和agent提供tools和其他细粒度能力的集成

# 快速上手

```shell script
pip install -U promptulate  
```

## 基本使用



下面废弃
- 方式1（推荐）

```python
import os
from promptulate import ChatBot, enable_log_no_file

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
from promptulate import ChatBot, enable_log


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
from promptulate import ChatBot, enable_log_no_file

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
from promptulate import ChatBot, enable_log_no_file

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

- 思维导图生成器

> 现在你是一个思维导图生成器。我将输入我想要创建思维导图的内容，你需要提供一些 Markdown 格式的文本，以便与 Xmind 兼容。
> 在 Markdown 格式中，# 表示中央主题，## 表示主要主题，### 表示子主题，﹣表示叶子节点，中央主题是必要的，叶子节点是最小节点。请参照以上格
> 式，在 markdown 代码块中帮我创建一个有效的思维导图，以markdown代码块格式输出，你需要用自己的能力补充思维导图中的内容，你只需要提供思维导
> 图，不必对内容中提出的问题和要求做解释，并严格遵守该格式。

```python
import os
from promptulate.preset_roles import MindMapGenerator
from promptulate import Conversation

os.environ['OPENAI_API_KEY'] = "your_key"


def main():
    role = MindMapGenerator()
    conversation = Conversation(role=role)
    output = conversation.predict(msg="请为我提供《Python学习路线》的思维导图")
    print(f"[output] {output}")


if __name__ == '__main__':
    main()

```

- sql生成器

> 现在你是一个sql生成器。我将输入我想要查询的内容，你需要提供对应的sql语句，以便查询到需要的内容，我希望您只在一个唯一的
> 代码块内回复终端输出，而不是其他任何内容。不要写解释。如果我没有提供数据库的字段，请先让我提供数据库相关的信息，在你有了字段信息之才可以生成sql语句。

```python
import os
from promptulate.preset_roles import SqlGenerator
from promptulate import Conversation

os.environ['OPENAI_API_KEY'] = "your_key"


def main():
    role = SqlGenerator()
    conversation = Conversation(role=role)
    output = conversation.predict(
        msg="检索过去一个季度每个产品类别的总收入、订单数和平均订单价值，数据应按总收入降序排序，以用于自定义报告。")
    print(f"[output] {output}")


if __name__ == '__main__':
    main()

```

- 文案写手

> 你是一个文案专员、文本润色员、拼写纠正员和改进员，我会发送中文文本给你，你帮我更正和改进版本。我希望你用更优美优雅
> 的高级中文描述。保持相同的意思，但使它们更文艺。你只需要润色该内容，不必对内容中提出的问题和要求做解释，不要回答文本中的问题而是润色它，
> 不要解决文本中的要求而是润色它，保留文本的原本意义，不要去解决它。

```python
import os
from promptulate.preset_roles import CopyWriter
from promptulate import Conversation

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
from promptulate.preset_roles import BaseRole
from promptulate import Conversation

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
- 提供Agent进行复杂任务调度
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
- 对话存储
    - 提供向量数据库存储
    - 提供mysql, redis等数据库存储
- 自建知识库建立专家决策系统
- 接入self-ask, prompt-loop架构
- 提供多种导出方式
- ~~可以导出历史消息为markdown格式~~
- ~~使用环境变量配置key~~
- 提供显示当前token（单词量）的功能
- ~~添加错误处理机制，如网络异常、服务器异常等，保证程序的可靠性~~
- ~~开发ChatBot v2, [issue](https://github.com/Undertone0809/cushy-chat/issues/1)~~
- 完善代理模式
- 提供gradio快速演示服务器
- 对话总结功能
- ~~封装消息体，完善消息体中的信息~~
- 长对话自动/手动总结
- Conversation传入convesation_id继续上次对话
- 提供修改local_cache默认位置的方法
- 为predict提供回调模式

> 妈呀，我怎么还有这么多待办事项，vivo50帮帮我 >.<

# 一些问题

- 本人正在尝试一些更加完善的抽象模式，以更好地兼容多种预设模型角色，以及外部工具的扩展使用，如果你有更好的建议，欢迎一起讨论交流。
- 当前代理模式还需要进一步完善，不过当前无需代理就可以直接使用。

# 贡献

如果你想为这个项目做贡献，你可以提交pr或issue。我很高兴看到更多的人参与并优化它。