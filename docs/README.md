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

`Promptulate AI` 专注于构建大语言模型应用与 AI Agent 的开发者平台，致力于为开发者和企业提供构建、扩展、评估大语言模型应用的能力。`Promptulate` 是 `Promptulate AI` 旗下的大语言模型自动化与应用开发框架，旨在帮助开发者通过更小的成本构建行业级的大模型应用，其包含了LLM领域应用层开发的大部分常用组件，如外部工具组件、模型组件、Agent 智能代理、外部数据源接入模块、数据存储模块、生命周期模块等。 通过 `Promptulate`，你可以用 pythonic 的方式轻松构建起属于自己的 LLM 应用程序。

更多地，为构建一个强大而灵活的 LLM 应用开发平台与 AI Agent 构建平台，以创建能够自动化各种任务和应用程序的自主代理，`Promptulate` 通过Core
AI Engine、Agent System、Tools Provider、Multimodal Processing、Knowledge Base 和 Task-specific Modules
6个组件实现自动化AI平台。 Core AI Engine 是该框架的核心组件，负责处理和理解各种输入，生成输出和作出决策。Agent
System 是提供高级指导和控制AI代理行为的模块；APIs and Tools Provider 提供工具和服务交互的API和集成库；Multimodal
Processing 是一组处理和理解不同数据类型（如文本、图像、音频和视频）的模块，使用深度学习模型从不同数据模式中提取有意义的信息；Knowledge
Base 是一个存储和组织世界信息的大型结构化知识库，使AI代理能够访问和推理大量的知识；Task-specific
Modules 是一组专门设计用于执行特定任务的模块，例如情感分析、机器翻译或目标检测等。通过这些组件的组合，框架提供了一个全面、灵活和强大的平台，能够实现各种复杂任务和应用程序的自动化。

## 特性

- 大语言模型支持：支持不同类型的大语言模型的扩展接口
- 对话终端：提供简易对话终端，直接体验与大语言模型的对话
- AgentGroup：提供WebAgent、ToolAgent、CodeAgent等不同的Agent，进行复杂能力处理
- 长对话模式：支持长对话聊天，支持多种方式的对话持久化
- 外部工具：集成外部工具能力，可以进行网络搜索、执行Python代码等强大的功能
- KEY池：提供API key池，彻底解决key限速的问题
- 智能代理：集成 ReAct，self-ask 等 Prompt 框架，结合外部工具赋能 LLM
- 中文优化：针对中文语境进行特别优化，更适合中文场景
- 数据导出：支持 Markdown 等格式的对话导出
- Hook与生命周期：提供 Agent，Tool，llm 的生命周期及 Hook 系统
- 高级抽象：支持插件扩展、存储扩展、大语言模型扩展

## 快速开始

- [快速上手/官方文档](https://undertone0809.github.io/promptulate/#/)
- [当前开发计划](https://undertone0809.github.io/promptulate/#/other/plan)
- [参与贡献/开发者手册](https://undertone0809.github.io/promptulate/#/other/contribution)
- [常见问题](https://undertone0809.github.io/promptulate/#/other/faq)
- [pypi仓库](https://pypi.org/project/promptulate/)

- 打开终端，输入以下命令安装框架：

```shell script
pip install -U promptulate  
```

- 通过下面这个简单的程序开始你的 “HelloWorld”。

```python
import os
import promptulate as pne

os.environ['OPENAI_API_KEY'] = "your-key"

agent = pne.WebAgent()
answer = agent.run("What is the temperature tomorrow in Shanghai")
print(answer)
```

```
The temperature tomorrow in Shanghai is expected to be 23°C.
```

> 大多数时候我们会将 promptulate 称之为 pne,其中 p 和 e 表示 promptulate 开头和结尾的单词，而 n 表示 9，即 p 和 e 中间的九个单词的简写。

更多详细资料，请查看[快速上手/官方文档](https://undertone0809.github.io/promptulate/#/)

## 基础架构

当前`promptulate`正处于快速开发阶段，仍有许多内容需要完善与讨论，十分欢迎大家的讨论与参与，而其作为一个大语言模型自动化与应用开发框架，主要由以下几部分组成：

- 大语言模型支持：支持不同类型的大语言模型的扩展接口
- AI Agent：提供WebAgent、ToolAgent、CodeAgent等不同的Agent以及自定Agent能力，进行复杂能力处理
- 对话终端：提供简易对话终端，直接体验与大语言模型的对话
- 角色预设：提供预设角色，以不同的角度调用LLM
- 长对话模式：支持长对话聊天，支持多种方式的对话持久化
- 外部工具：集成外部工具能力，可以进行网络搜索、执行Python代码等强大的功能
- KEY池：提供API key池，彻底解决key限速的问题
- 智能代理：集成ReAct，self-ask等高级Agent，结合外部工具赋能LLM
- 中文优化：针对中文语境进行特别优化，更适合中文场景
- 数据导出：支持 Markdown 等格式的对话导出
- 高级抽象：支持插件扩展、存储扩展、大语言模型扩展
- 格式化输出：原生支持大模型的格式化输出，大大提升复杂场景下的任务处理能力与鲁棒性
- Hook与生命周期：提供Agent，Tool，llm的生命周期及Hook系统
- 物联网能力：框架为物联网应用开发提供了多种工具，方便物联网开发者使用大模型能力。


<img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20230704180202.png"/>

## 设计原则

promptulate框架的设计原则包括：模块化、可扩展性、互操作性、鲁棒性、可维护性、安全性、效率和可用性。

- 模块化是指以模块为基本单位，允许方便地集成新的组件、模型和工具。
- 可扩展性是指框架能够处理大量数据、复杂任务和高并发的能力。
- 互操作性是指该框架与各种外部系统、工具和服务兼容，并且能够实现无缝集成和通信。
- 鲁棒性是指框架具备强大的错误处理、容错和恢复机制，以确保在各种条件下可靠地运行。
- 安全性是指框架采用了严格的安全措施，以保护框架、其数据和用户免受未经授权访问和恶意行为的侵害。
- 效率是指优化框架的性能、资源使用和响应时间，以确保流畅和敏锐的用户体验。
- 可用性是指该框架采用用户友好的界面和清晰的文档，使其易于使用和理解。

以上原则的遵循，以及最新的人工智能技术的应用，`promptulate`旨在为创建自动化代理提供强大而灵活的大语言模型应用开发框架。

## 交流群

欢迎加入群聊一起交流讨论有关LLM相关的话题，链接过期了可以issue或email提醒一下作者。

<div style="width: 250px;margin: 0 auto;">
    <img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20240307033904.png"/>
</div>

## 贡献

本人正在尝试一些更加完善的抽象模式，以更好地兼容该框架，如果你有更好的建议，欢迎一起讨论交流。
如果你想为这个项目做贡献，请先查看[当前开发计划](https://undertone0809.github.io/promptulate/#/other/plan)
和[参与贡献/开发者手册](https://undertone0809.github.io/promptulate/#/other/contribution)。我很高兴看到更多的人参与并优化它。
