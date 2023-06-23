# Framework

> 文档完善中...

### 简介

本文将会介绍对话模型Conversation、Prompt框架ReAct、self-ask，tree-of-thoughts的基本使用。

### Conversation

LLM组件只提供了最基础的对话生成内容，但是其并不提供上下文对话、文章总结、角色预设等更加复杂的功能，所以接下来我们介绍功能更为强大的`Conversation`。

`Conversation` 是`framework`中最基础的组件，其支持prompt生成、上下文对话、对话存储、角色预设的基本功能，此外，`provider`
为其提供了语言翻译、markdown数据导出、对话总结、标题总结等扩展功能。

接下来，我们先从对基础的对话开始，使用`Conversation`可以开始一段对话，使用其`predict()`函数可以生成回答。

```python
from promptulate import Conversation

conversation = Conversation()
conversation.predict("你知道鸡哥的《只因你太美》吗？")
```

```text
'是的，鸡哥的《只因你太美》是这几年非常流行的一首歌曲。'
```

`Conversation`默认使用`OpenAI GPT3.5`作为LLM，当然，因为其架构设计，`Conversation`
还可以轻松扩展其他类型的llm。

下面是一个更复杂的示例，展示了使用OpenAI作为大语言模型进行对话，使用本地文件进行存储，进行文章总结与标题总结的功能。

```python
from promptulate import Conversation
from promptulate.memory import LocalCacheChatMemory
from promptulate.llms import OpenAI


def main():
    memory = LocalCacheChatMemory()
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

- `LocalCacheChatMemory()`进行聊天记录的本地化文件存储，文件存储形式默认是以json的形式进行存储的，保存在`cache`中。
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
conversation.predict_by_translate("你知道鸡哥会什么技能吗？", country='America', enable_embed_message=True)
```

如果你设置了`enable_embed_message=True`, 那么这一次的predict将保存进历史对话中，provider提供的函数默认是不会将预测结果存入对话中的哦，这一点需要注意一下。
