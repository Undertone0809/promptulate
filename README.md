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
    <a target="_blank" href=''>
        <img src="docs/images/coverage.svg"/>
    </a>
</p>

[English](/README.md) [中文](/README_zh.md)

<p align="center">
  <img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/promptulate_logo_new.png"/>
</p>

# What is Promptulate?
`Promptulate AI` focuses on building a developer platform for large language model applications, dedicated to providing developers and businesses with the ability to build, extend, and evaluate large language model applications. `Promptulate` is a large language model automation and application development framework under `Promptulate AI`, designed to help developers build industry-level large model applications at a lower cost. It includes most of the common components for application layer development in the LLM field, such as external tool components, model components, Agent intelligent agents, external data source integration modules, data storage modules, and lifecycle modules. With `Promptulate`, you can easily build your own LLM applications.

# Envisage
To create a powerful and flexible LLM application development platform for creating autonomous agents that can automate various tasks and applications, `Promptulate` implements an automated AI platform through six components: Core AI Engine, Agent System, APIs and Tools Provider, Multimodal Processing, Knowledge Base, and Task-specific Modules. The Core AI Engine is the core component of the framework, responsible for processing and understanding various inputs, generating outputs, and making decisions. The Agent System is a module that provides high-level guidance and control over AI agent behavior. The APIs and Tools Provider offers APIs and integration libraries for interacting with tools and services. Multimodal Processing is a set of modules for processing and understanding different data types, such as text, images, audio, and video, using deep learning models to extract meaningful information from different data modalities. The Knowledge Base is a large structured knowledge repository for storing and organizing world information, enabling AI agents to access and reason about a vast amount of knowledge. The Task-specific Modules are a set of modules specifically designed to perform specific tasks, such as sentiment analysis, machine translation, or object detection. By combining these components, the framework provides a comprehensive, flexible, and powerful platform for automating various complex tasks and applications.


# Features

- Large language model support: Support for various types of large language models through extensible interfaces.
- Dialogue terminal: Provides a simple dialogue terminal for direct interaction with large language models.
- Role presets: Provides preset roles for invoking GPT from different perspectives.
- Long conversation mode: Supports long conversation chat and persistence in multiple ways.
- External tools: Integrated external tool capabilities for powerful functions such as web search and executing Python code.
- KEY pool: Provides an API key pool to completely solve the key rate limiting problem.
- Intelligent agent: Integrates advanced agents such as ReAct and self-ask, empowering LLM with external tools.
- Autonomous agent mode: Supports calling official API interfaces, autonomous agents, or using agents provided by Promptulate.
- Chinese optimization: Specifically optimized for the Chinese context, more suitable for Chinese scenarios.
- Data export: Supports dialogue export in formats such as markdown.
- Hooks and lifecycles: Provides Agent, Tool, and LLM lifecycles and hook systems.
- Advanced abstraction: Supports plugin extensions, storage extensions, and large language model extensions.

# Quick Start

- [Quick Start/Official Documentation](https://undertone0809.github.io/promptulate/#/)
- [Current Development Plan](https://undertone0809.github.io/promptulate/#/other/plan)
- [Contribution/Developer's Guide](https://undertone0809.github.io/promptulate/#/other/contribution)
- [FAQ](https://undertone0809.github.io/promptulate/#/other/faq)
- [PyPI Repository](https://pypi.org/project/promptulate/)

To install the framework, open the terminal and run the following command:

```shell script
pip install -U promptulate  
```

Get started with your "HelloWorld" using the simple program below:

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

> Most of the time, we refer to template as pne, where p and e represent the words that start and end template, and n represents 9, which is the abbreviation of the nine words between p and e.

For more detailed information, please refer to the [Quick Start/Official Documentation](https://undertone0809.github.io/promptulate/#/).

# Architecture

Currently, `promptulate` is in the rapid development stage and there are still many aspects that need to be improved and discussed. Your participation and discussions are highly welcome. As a large language model automation and application development framework, `promptulate` mainly consists of the following components:

- `Agent`: More advanced execution units responsible for task scheduling and distribution.
- `llm`: Large language model responsible for generating answers, supporting different types of large language models.
- `Memory`: Responsible for storing conversations, supporting different storage methods and extensions such as file storage and database storage.
- `Framework`: Framework layer that implements different prompt frameworks, including the basic `Conversation` model and models such as `self-ask` and `ReAct`.
- `Tool`: Provides external tool extensions for search engines, calculators, etc.
- `Hook&Lifecycle`: Hook system and lifecycle system that allows developers to customize lifecycle logic control.
- `Role presets`: Provides preset roles for customized conversations.
- `Provider`: Provides more data sources or autonomous operations for the system, such as connecting to databases.

<img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20230704180202.png"/>

# Design Principles

The design principles of the `promptulate` framework include modularity, scalability, interoperability, robustness, maintainability, security, efficiency, and usability.

- Modularity refers to the ability to integrate new components, models, and tools conveniently, using modules as the basic unit.
- Scalability refers to the framework's capability to handle large amounts of data, complex tasks, and high concurrency.
- Interoperability means that the framework is compatible with various external systems, tools, and services, allowing seamless integration and communication.
- Robustness refers to the framework's ability to handle errors, faults, and recovery mechanisms to ensure reliable operation under different conditions.
- Security involves strict security measures to protect the framework, its data, and users from unauthorized access and malicious behavior.
- Efficiency focuses on optimizing the framework's performance, resource utilization, and response time to ensure a smooth and responsive user experience.
- Usability involves providing a user-friendly interface and clear documentation to make the framework easy to use and understand.

By following these principles and incorporating the latest advancements in artificial intelligence technology, `promptulate` aims to provide a powerful and flexible application development framework for creating automated agents.

# Contributions

I am currently exploring more comprehensive abstraction patterns to improve compatibility with the framework and the extended use of external tools. If you have any suggestions, I welcome discussions and exchanges.

If you would like to contribute to this project, please refer to the [current development plan](https://undertone0809.github.io/promptulate/#/other/plan) and [contribution/developer's guide](https://undertone0809.github.io/promptulate/#/other/contribution). I'm excited to see more people getting involved and optimizing it.
