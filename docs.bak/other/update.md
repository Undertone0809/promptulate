# Update

## Upgrade Version

Please update the latest version.

```bash
pip install -U promptulate
```

## 1.8.0 2023-10-23
- `feat` 构建输出格式化器，让 LLM 可以根据指定格式进行输出

## 1.7.0 2023-10-25
- `feat` 兼容所有 langchain tool
- `feat` 兼容 huggingface

## 1.4.0 2023-08-28
- `feat` 提供百度文心大模型模型支持 [https://github.com/Undertone0809/promptulate/pull/27](https://github.com/Undertone0809/promptulate/pull/27)
- `fix` 修复ToolAgent经常遇到None Tool的问题 
- `pref` 优化pne-chat client的使用


## 1.3.0 2023-08-08

#### Features

1. 提供完善的ToolAgent,提供Agent进行复杂任务调度 
2. 优化message的消息存储结构 
3. 优化Memory架构 
4. 构建Agent，Tool，llm的生命周期 
5. 构建Hook系统，用于在Agent，Tool，llm的生命周期实现定制化功能 
6. 提供prompt模板化构建方式 
7. promptulate-chat增加多行输入 
8. 构建ToolManager，可以通过简单的方式进行工具集成

#### Optimize

1. 优化Openai API KEY Pool



## 1.2.0 2023-06-25

#### Features

1. 增加semantic scholar查询与引用查询工具
2. 完善key_pool单元测试
3. 增加paper-summary tool

## v1.1.0 2023-06-23

#### Features

1. 增加arxiv工具
2. 增加DuckDuckGo Search网络搜索
3. 增加Python REPL，可以运行Python脚本
4. 增加API KEY池的功能 [文档](modules/llm/llm.md#key池)
