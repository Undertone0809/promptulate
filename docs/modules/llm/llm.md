# LLM

### 简介

> Attention:
> 1. `promptulate`中会把LLM与llm的意思分开来，LLM表示大语言模型，llm表示`promptulate`中的llm模块。
> 2. 从 `v1.11.0` 的版本开始，我们推荐你使用 [pne.chat()](use_cases/chat_usage.md#chat) 的方式进行 LLM 的调用。

本文将会介绍llm模块的**基本使用方式，API KEY、KEY池、代理的配置方式**。

LLM指大语言模型，当前市面上常见的大语言模型有GPT3.5, GPT4, LLaMa, InstructGPT等大语言模型。`promptulate`可以支持不同类型的大语言模型调用。

当前`promptulate`重点适配了OpenAI的相关的大语言模型(GPT-3.5, GPT-4.0, text-davinci-003)与百度文心系列大模型，其他模型正在逐步适配中（如ChatGLM适配中），如果你有想用的LLM或者更好的想法，欢迎提出你的想法。


### 相关教程

- [OpenAI快速上手](modules/llm/openai.md#openai)
- [百度文心大模型快速上手](modules/llm/erniebot.md#百度文心erniebot)
