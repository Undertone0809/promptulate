# 智谱系列模型

> 从 `v1.16.0` 版本开始，不在使用 llm 的概念，LLM 所有的功能都可以用 [pne.chat()](use_cases/chat_usage.md#chat) 来代替。只有当你需要自定义模型的时候，需要学习 [Custom LLM](modules/llm/custom_llm.md#custom-llm) 的使用方式。

本文将会介绍智谱系列大模型的使用，要使用其能力，你需要前往[智谱AI大模型MaaS开放平台](https://maas.aminer.cn)创建大模型应用并获取相应的key

### KEY配置

在使用智谱AI大模型MaaS开放平台系列的LLM之前，你需要先导入你的`API Key`,具体请查看智谱官方文档(https://maas.aminer.cn/dev/api#auth)

**方法一（不推荐）**

```python
import os

os.environ["ZHIPUAI_API_KEY"] = "your api key"
```

在你第一次使用的时候，需要使用`os.environ["ZHIPUAI_API_KEY"]` 导入"ZHIPUAI_API_KEY"的环境变量，但是在第一运行之后`promptulate`会进行缓存，即后面再运行就不需要再导入key了。

如果你的key过期了，可以尝试重新按照上面的方法导入key，或者你也可以把 `cache` 文件给删除掉，通过以下代码可以获取到缓存文件的位置:

```python
from promptulate.utils import get_default_storage_path

print(get_default_storage_path())
```

**方法二（推荐）**

方法二是 promptulate 官方推荐的最佳实践，你可以通过创建 `.env` 的方式来导入 key，与上面的配置效果是等价的。 [env 的使用方式](https://github.com/theskumar/python-dotenv)

在项目根目录下创建 `.env` 文件，然后填入你的 key:

```text
ZHIPUAI_API_KEY = xxx
```

### LLM快速上手

`promptulate`的架构设计可以轻松兼容不同的大语言模型扩展，在`promptulate`中，llm负责最基本的内容生成部分，因此为最基础的组件。

下面的示例展示了如何使用智谱AI的大语言模型进行交互。

如果你想使用智谱AI系列模型，只需要 ZhiPu()进行初始化，你还可以使用ZhiPu(model="glm-4")来具体选择对应的模型，目前框架基本支持所有的智谱AI系列语言模型，分别是

**GLM-4**

新一代基座大模型GLM-4，整体性能相比GLM3全面提升60%，逼近GPT-4；支持更长上下文；更强的多模态；支持更快推理速度，更多并发，大大降低推理成本；同时GLM-4增强了智能体能力。

**GLM-3-Turbo**

适用于对知识量、推理能力、创造力要求较高的场景，比如广告文案、小说写作、知识类写作、代码生成等。

本框架默认为性能更加强大的glm-4模型。

你可以使用如下方式切换模型：

```python
from promptulate.llms import ZhiPu

llm = ZhiPu(model="glm-3-turbo") 
answer = llm("请解释一下引力波的放射与广义相对论的必然关系")
print(answer)
```

### 参数配置

智谱相关模型的参数请查看[官方接口文档](https://maas.aminer.cn/dev/api#language)

你可以使用如下方式进行参数配置：

```python
from promptulate.llms import ZhiPu

model_config = {"temperature": 0.1, "top_p": 0.8}

llm = ZhiPu(model_config=model_config) 
answer = llm("请解释一下引力波的放射与广义相对论的必然关系")
print(answer)
```

### stop停词
你也许知道使用OpenAI的LLM的时候，可以进行stop(停词)，什么是stop呢？

事实上，stop是一个字符串数组，如`["action", "observation"]`，在LLM生成文本的过程中，如果检测到LLM当前生成本文为stop数组里的内容，则LLM就会停止文本生成，该功能一般用于一些复杂应用程序的开发上，下面的示例展示了stop的使用。

```python
from promptulate.llms import ZhiPu

model_config = {"temperature": 0.1, "stop": ["a"]}
llm = ZhiPu(model_config=model_config)
prompt = """
Please strictly output the following content.
[start] This is a test [end]
"""
result = llm(prompt)
print(result)
```

输出结果如下：

```text
[start] This is a
```

### 流式输出

如果你想要流形式输出，你可以按照如下方式进行流输出

```python
from promptulate.llms import ZhiPu

model_config = {"stream": True}
llm = ZhiPu(model_config=model_config)

response = llm("Who are you?")

for chuck in response:
    print(chuck)
```

ZhiPu()将返回一个迭代器，您可以使用next()或for each来获取响应。
如果您想获取元数据，可以使用return_raw_response=True来获取pne包装的原始响应。助理消息。元数据将存储在pne.AssistantMessage.additional_kwargs。

```python
from promptulate.llms import ZhiPu

model_config = {"stream": True, "return_raw_response": True}
llm = ZhiPu(model_config=model_config)

response = llm("Who are you?")
for chuck in response:
    print(chuck.content)
    print(chuck.additional_kwargs)
```
