# LLM

::: info

1. pne will separate the meaning of LLM from llm, LLM stands for large language model, llm stands for llm module in 'promptulate'.
2. Starting with v1.11.0, we recommend that you use  [pne.chat()](/use_cases/chat_usage.md#chat)  for LLM calls.
3. Starting from v1.16.0, the concept of llm is no longer used, and all functions of LLM can be replaced by  [pne.chat()](/use_cases/chat_usage.md#chat). Only when you need to customize the model, You need to learn how to use [Custom LLM](/modules/llm/custom_llm.md#custom-llm) and [LLMFactory](/modules/llm/llm-factory-usage#LLMFactory).
:::

## Introduction

llm is a component in pne that makes up the smallest unit of a large model, can do large model inference, and supports the construction of almost all large models on the market, of course, you can also customize local models. It integrates the ability of [litellm](https://github.com/BerriAI/litellm). It means you can call all LLM APIs using the OpenAI format. Use Bedrock, Azure, OpenAI, Cohere, Anthropic, Ollama, Sagemaker, HuggingFace, Replicate (100+ LLMs). Now let's take a look at how to use it.

## When will this module be used?

In general, we do not use the llm module directly, because in most cases we can directly use pne.chat() to complete the business, only when the custom model and the Agent are used.

### How to use?

There are some ways to teach you how to use llm module:

- [Use LLMFactory to create a language model](/modules/llm/llm-factory-usage#LLMFactory)
- [How to write model name?](/other/how_to_write_model_name.md#how-to-write-model-name)
- [Custom your llm](/modules/llm/custom_llm.md#custom-llm)
