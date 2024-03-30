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
</p>

<p align="center">
  <img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/promptulate_logo_new.png"/>
</p>

## Overview

**Promptulate** is an AI Agent application development framework crafted by **Cogit Lab**, which offers developers an extremely concise and efficient way to build Agent applications through a Pythonic development paradigm. The core philosophy of Promptulate is to borrow and integrate the wisdom of the open-source community, incorporating the highlights of various development frameworks to lower the barrier to entry and unify the consensus among developers. With Promptulate, you can manipulate components like LLM, Agent, Tool, RAG, etc., with the most succinct code, as most tasks can be easily completed with just a few lines of code. 🚀

## 💡 Features

- 🐍 Pythonic Code Style: Embraces the habits of Python developers, providing a Pythonic SDK calling approach, putting everything within your grasp with just one `pne.chat` function to encapsulate all essential functionalities.
- 🧠 Model Compatibility: Supports nearly all types of large models on the market and allows for easy customization to meet specific needs.
- 🕵️‍♂️ Diverse Agents: Offers various types of Agents, such as WebAgent, ToolAgent, CodeAgent, etc., capable of planning, reasoning, and acting to handle complex problems.
- 🔗 Low-Cost Integration: Effortlessly integrates tools from different frameworks like LangChain, significantly reducing integration costs.
- 🔨 Functions as Tools: Converts any Python function directly into a tool usable by Agents, simplifying the tool creation and usage process.
- 🪝 Lifecycle and Hooks: Provides a wealth of Hooks and comprehensive lifecycle management, allowing the insertion of custom code at various stages of Agents, Tools, and LLMs.
- 💻 Terminal Integration: Easily integrates application terminals, with built-in client support, offering rapid debugging capabilities for prompts.
- ⏱️ Prompt Caching: Offers a caching mechanism for LLM Prompts to reduce repetitive work and enhance development efficiency.

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

For more details, please visit the [litellm documentation](https://docs.litellm.ai/docs/providers).

You can easily build any third-party model calls using the following method:

```python
import promptulate as pne

resp: str = pne.chat(model="ollama/llama2", messages=[{"content": "Hello, how are you?", "role": "user"}])
```

## 📗 Related Documentation

- [Getting Started/Official Documentation](https://undertone0809.github.io/promptulate/#/)
- [Current Development Plan](https://undertone0809.github.io/promptulate/#/other/plan)
- [Contributing/Developer's Manual](https://undertone0809.github.io/promptulate/#/other/contribution)
- [Frequently Asked Questions](https://undertone0809.github.io/promptulate/#/other/faq)
- [PyPI Repository](https://pypi.org/project/promptulate/)

## 🛠 Quick Start

- Open the terminal and enter the following command to install the framework:

```shell script
pip install -U promptulate  
```

> Note: Your Python version should be 3.8 or higher.

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

... (The content continues as in the original text, including examples and output results) ...

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

Feel free to join the group chat to discuss topics related to LLM & AI Agents. There will be occasional technical shares in the group. If the link expires, please remind the author via issue or email.

<div style="width: 250px;margin: 0 auto;">
    <img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20240331034649.png"/>
</div>

For more information, please contact: [zeeland4work@gmail.com](mailto:zeeland4work@gmail.com)

## ⭐ Contribution

We appreciate your interest in contributing to our open-source initiative. We have provided a [Developer's Guide](https://undertone0809.github.io/promptulate/#/other/contribution) outlining the steps to contribute to Promptulate. Please refer to this guide to ensure smooth collaboration and successful contributions. Additionally, you can view the [Current Development Plan](https://undertone0809.github.io/promptulate/#/other/plan) to see the latest development progress 🤝🚀
