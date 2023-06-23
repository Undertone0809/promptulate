# tools

文档完善中...

## 简介

tools模块为LLM提供了调用外部工具扩展的能力，可以说tools是走向智能化的第一步，通过tools来为LLM构建一套感知反馈系统，可以为LLM应用开发提供更多的可能性。本文将会介绍`promptulate`
当前支持的外部工具，以及外部工具、工具套件的基本使用方式，最后还会介绍当前正在开发的一些工具套件。

## 支持的工具

当前`promptulate`支持以下几种工具：

- DuckDuckGo Search
- Arxiv
- Python REPL
- FileManager
- ...