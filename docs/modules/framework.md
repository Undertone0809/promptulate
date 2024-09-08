# Framework

> 请注意，Framework 在 v2.0.0 版本后将不再维护，该模块将被废弃！Agent 模块将逐渐取代的当前模块的所有功能。

## 简介

本文将会介绍对话模型`Conversation`、Prompt框架ReAct、self-ask，tree-of-thoughts的基本使用。

下面，将会介绍`Conversation`和`Chain`两种framework，在[llm](/modules/llm/llm.md#llm的类型)的部分我们介绍过文本推理型与对话型llm的区别，事实上，`Chain`就是**文本推理型llm**的增强版，而`Conversation`是**对话型llm**的增强版，这里的增强主要体现在：

- 增加memory进行交互信息的持久化存储
- 提供provider进行多种mixin能力的集成嵌入，如语言翻译、markdown数据导出、对话总结、标题总结等功能


## Conversation

llm组件只提供了最基础的对话生成内容，但是其并不提供上下文对话、文章总结、角色预设等更加复杂的功能，所以接下来我们介绍功能更为强大的`Conversation`。

`Conversation` 是`framework`中最基础的组件，其支持prompt生成、上下文对话、对话存储、角色预设的基本功能，此外，`provider`为其提供了语言翻译、markdown数据导出、对话总结、标题总结等扩展功能。

### 基本使用

接下来，我们先从对基础的对话开始，使用`Conversation`可以开始一段对话，使用其`predict()`函数可以生成回答。

```python
from promptulate import Conversation

conversation = Conversation()
conversation.predict("请解释一下引力波的放射与广义相对论的必然关系")
```

```text
广义相对论是一种描述引力如何影响时空的物理学理论，它指出当物质和能量聚集在一起时，它们弯曲了周围的时空，引起了引力。质量和能量更大的物体会导致更大
的时空弯曲，这就是为什么地球会围绕太阳旋转。根据广义相对论，当物质或能量在空间中运动时，它们会产生引力波，就像在水面上产生涟漪一样。引力波是一种类
似电磁波的波动，但它们是由物质和能量的弯曲引起的，而电磁波是由电荷的振动引起的。引力波是极微弱的，但是当强烈的引力场存在（例如在引力天体碰撞或超新
星爆炸等事件中），它们可以被探测到。事实上，2015年，激光干涉引力波天文台利用引力波探测器直接探测到了引力波，并为广义相对论提供了强有力的证据。因
此，引力波的放射与广义相对论必然关系紧密。通过引力波，我们可以更加深入地了解时空的性质，并进一步验证这个理论。
```

`Conversation`默认使用`OpenAI GPT3.5`作为LLM，当然，因为其架构设计，`Conversation`
还可以轻松扩展其他类型的llm。

### 扩展功能

下面是一个更复杂的示例，展示了使用OpenAI作为大语言模型进行对话，使用本地文件进行存储，进行文章总结与标题总结的功能。

```python
from promptulate import Conversation
from promptulate.memory import FileChatMemory
from promptulate.llms import OpenAI


def main():
    memory = FileChatMemory()
    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.9, top_p=1, stream=False, presence_penalty=0, n=1)
    conversation = Conversation(llm=llm, memory=memory)
    ret = conversation.predict("你知道鸡哥的著作《只因你太美》吗？")
    print(f"[predict] {ret}")
    ret = conversation.predict_by_translate("你知道鸡哥会什么技能吗？", country='America')
    print(f"[translate output] {ret}")
    ret = conversation.summary_content()
    print(f"[summary content] {ret}")
    ret = conversation.summary_topic()
    print(f"[summary topic] {ret}")
    ret = conversation.export_message_to_markdown(output_type="file", file_path="output.md")
    print(f"[export markdown] {ret}")


if __name__ == '__main__':
    main()

```

```text
[predict] 是的，我知道《只因你太美》这本书，是中国知名作家鸡肋（江南）所著的一篇言情小说。这本小说讲述了一个富家千金与一个贫穷男孩之间的爱情故事，情节曲折动人，深受读者喜爱。该小说在出版后得到了很高的评价和反响，并被改编成电影和电视剧等多种形式进行推广。
[translate output] I'm sorry, I cannot determine what you mean by "鸡哥" or what skills they may possess without additional context. Can you please provide more information or clarify your question?
[summary content] 在之前的对话中，用户询问我是否知道鸡哥的著作《只因你太美》。我回答了肯定的，解释了该小说的情节大致概括和其受欢迎的原因。我也提到了该小说的广泛影响，包括被改编成电影和电视剧等多种形式进行推广。
[summary topic] 鸡哥的小说。
```

上面的示例中，我们使用

- `FileChatMemory()`进行聊天记录的本地化文件存储，文件存储形式默认是以json的形式进行存储的，保存在`cache`中。
- `OpenAI(model="gpt-3.5-turbo", temperature=0.9, top_p=1, stream=False, presence_penalty=0, n=1)`
  进行初始化一个大模型，里面是OpenAI需要传入的一些参数，具体可以查看[https://platform.openai.com/docs/api-reference/chat/create](https://platform.openai.com/docs/api-reference/chat/create)
  查看具体含义，这里不做详细讲解，如果你不想理会这些参数，你也可以直接`llm = OpenAI()`就好啦，默认使用`gpt-3.5-turbo`
  作为大语言模型，其他参数使用默认的就好了。
- `conversation.predict_by_translate("你知道鸡哥会什么技能吗？", country='America')`
  这个功能为使用特定语言进行预测，`provider`为其提供了`TranslatorMixin`，让`Conversation`
  得以拥有此功能。对于这个方法，你只需要传入prompt和你需要转换的语言的国家名称就好了。
- `conversation.summary_content()`这个函数可以直接总结上面的对话内容。
- `conversation.summary_topic()` 这个函数可以直接总结上面的对话，并提供一个标题。
- `conversation.export_message_to_markdown(output_type="file", file_path="output.md")`
  这个函数可以将对话记录导出为markdown文件，如果`output_type="text"`，则只返回markdown对话的内容。

`provider`为`Conversation`提供了 `SummarizerMixin, TranslatorMixin, DeriveHistoryMessageMixin`
，让其拥有了总结对话、总结标题、翻译、markdown导出的能力，provider提供的函数中一般都提供了一个`enable_embed_message`
的参数，这个参数的意思是：是否将本次对话保存进历史对话中，下面我们来看一个demo。

```python
from promptulate import Conversation

conversation = Conversation()
conversation.predict_by_translate("引力波的放射与广义相对论的必然关系", country='America', enable_embed_message=True)
```

如果你设置了`enable_embed_message=True`, 那么这一次的predict将保存进历史对话中，provider提供的函数默认是不会将预测结果存入对话中的哦，这一点需要注意一下。

### 继续上一次运行的对话

如果你使用LocalCacheChatMemory进行本地文件的Conversation数据存储，那么你可以轻松基于原有的对话开始继续对话。

下面的示例中展示了如何继续上一次运行时的对话。

- 第一次运行

```python
from promptulate import Conversation
from promptulate.memory.file import FileChatMemory

conversation = Conversation(memory=FileChatMemory())
result = conversation.predict("现在我要开一家人工智能工具，请帮我取5个名字")
print(f"<{conversation.conversation_id}> {result}")
```

从上面的代码可以看到，通过`conversation.conversation_id`的方式可以获取conversation_id，便于下一次运行使用。下面为一次的运行结果。

```text
<1687704464> 当然可以！以下是我为您提供的五个可能的名字：

1. BrainWave AI
2. Intellibot Pro
3. ThinkSmart Intelligence
4. SmartMind AI Solutions
5. AI InnovateX
```

- 第二次运行

```python
from promptulate import Conversation
from promptulate.memory import FileChatMemory

conversation = Conversation(conversation_id="1687704464", memory=FileChatMemory())
result = conversation.predict("再帮我取5个名字")
print(f"<{conversation.conversation_id}> {result}")

```

下面为第二次运行结果，可以看到通过传入conversation_id，就可以方便地就上一次运行的结果继续推理。

```text
<1687704464> 当然，我很乐意为您提供更多的建议。以下是另外5个选项：

1. 智慧之脑
2. AI启迪
3. 智慧赋能
4. 全息AI
5. 深度思维AI
```

### 获取历史数据

在某些时候，你或许有需要导出数据的需求，幸运的是，`promptulate`在`v1.3.0`版本之后升级了内部的统一消息结构，`framework` `agent` `memory`组件都可以使用`MessageSet`来读取导出历史对话数据，并且可以用`MessageSet`完成不同类型LLM之间的API转换。下面一个示例展示了如何在`Conversation`对话中用`MessageSet`获取所有的对话数据。

```python
from promptulate import Conversation
from promptulate.schema import MessageSet

conversation = Conversation()
result = conversation.predict("引力波")
messages: MessageSet = conversation.memory.load_message_set_from_memory()
list(map(lambda message: print(messages), messages.listdict_messages))
```

输出结果如下：

```text
{'role': 'system', 'content': '\nYou are an assistant to a human, powered by a large language model trained by OpenAI.\nYou are designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, you are able to generate human-like text based on the input you receive, allowing you to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.\nOverall, you are a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether the human needs help with a specific question or just wants to have a conversation about a particular topic, you are here to assist.\n'}
{'role': 'user', 'content': '引力波'}
{'role': 'assistant', 'content': '引力波是物理学中一种重要的现象，它是由爱因斯坦的广义相对论所预言和描述的。引力波是在时空中传播的扰动，它是由于质量和能量分布的变化而产生的，并且在空间中传播着能量和动量。与电磁波不同，引力波会扰动时空本身，而不是扰动电磁场。\n\n引力波最早于2015年由LIGO科学合作组织通过直接探测实验首次成功地被探测到。这次事件也被称为“重力波爆发”。这一重大的突破验证了爱因斯坦广义相对论的重要预言，并为天文学和物理学带来了革命性的变革。\n\n引力波的发现让科学家们有机会以一种前所未有的方式观测宇宙。由于引力波传播的是时空本身的扰动，它们可以透过天空中的物质和辐射传递，提供与传统观测方法不同的信息。通过观测引力波，科学家们可以研究黑洞、中子星和其他极端天体的性质，甚至可以通过引力波探测到宇宙的起源和演化过程。\n\n引力波的研究正在快速发展中，未来还有更多令人兴奋的发现和进展可以期待。通过不断改进探测技术和增加观测灵敏度，我们有望进一步了解宇宙中引力波的起源和性质，从而提供更深入的理解宇宙的工具和洞察力。'}
```


如果你仔细看过`promptulate`的源码，你会发现在`v1.3.0`版本升级之后，`llm`的功能变强了，因为其`predict`可以接受一个MessageSet作为参数，这意味着在某些时候，你可以使用`llm`代替`Conversation`使用，下面的示例展示了这种实现。

```python
import json

from promptulate.llms.openai import OpenAI
from promptulate.schema import (
    SystemMessage,
    UserMessage,
    AssistantMessage,
    MessageSet,
)

messages = [
    SystemMessage(content="Answer the following questions as best you can."),
    UserMessage(content="Joe平均每分钟出拳25次。一场战斗持续5轮，每轮3分钟。他打了多少拳？ 让我们一步一步地思考。"),
    AssistantMessage(
        content="""好的，让我们来解决这个问题。
首先，一轮战斗持续3分钟，Joe每分钟出拳25次，那么一轮他出拳的次数是25乘以3等于75次。
接下来，我们将五轮的数量相加，即75乘以5等于 <<75*5=375>>375。
因此，Joe在这场战斗中打了375次拳。"""
    ),
    UserMessage(
        content="""请输出最终答案，你的输出格式为：
{answer}
除此之外，不能输出其他任何内容，否则你将被惩罚。
"""
    ),
]
chat_history = MessageSet(messages=messages)

llm = OpenAI(temperature=0)
answer: AssistantMessage = llm.predict(chat_history)
chat_history.messages.append(answer)
print(json.dumps(chat_history.listdict_messages))
```

> 后续我们会专门开设一篇文档介绍MessageSet，如果你有更好的建议，我们非常期待你的想法！欢迎提出issue。

