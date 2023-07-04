# 开发计划

如果你有更好的建议，欢迎一起讨论，你可以通过[issue](https://github.com/Undertone0809/promptulate/issues)
，email，以及[交流群](README.md#交流群)进行交流。


## v1.3.0 发展计划(当前开发中)
> 该版本为本人自行开发，旨在为promptulate构建更加完善的架构体系

- 提供完善的agent,提供Agent进行复杂任务调度
  - 构建ToolAgent
- 提供ReAct, self-ask的framework支持
- 优化message的消息存储结构
- 优化Memory架构



## v1.4.0 发展计划(v1.3.0版本发布之后该部分会发布在issue中)
该issue为`promptulate` v1.4.0的发展计划，**开发中**的计划表示已经有相关的进展，正在开发中，而**计划开发**表示该版本计划完成的功能，但是还没有开始开发，如果你对某个点感兴趣，可以创建一个issue就该内容提一个简单的proposal，描述一下大体的实现思路，然后就可以开始你的开发了！

需要注意的是：

1. 如果你想要开发某一个功能，我十分推荐你开启一个新的issue提及该内容，避免重复开发，另一方面，issue为开发者提供了一起交流的渠道。
2. 如果计划开发中的某一条内容有人提出issue开发，我会将其转移至**开发中**
3. 官方文档中还有一些[其他开发计划](https://undertone0809.github.io/promptulate/#/other/plan)暂未列入当前版本的发展计划中，如果你看到了你想做的功能，我们十分乐意把其加入这个版本的开发计划中！

如果你想到更多有趣的功能，十分欢迎你提出相关建议、issue 和 pr！

**开发中**
- ...

**计划开发**
- 参考构建tool的API式扩展，并无缝衔接可以与现有工具一起调用
  - 参考
    - [连接海量API的大模型：Gorilla](https://mp.weixin.qq.com/s/ZxZAXKVdc1YsxBRpncWTNg)
    - [https://arxiv.org/pdf/2305.15334.pdf](https://arxiv.org/pdf/2305.15334.pdf)
- 更多的LLM适配，如当前各种开源模型的适配
  - ChatGLM
  - ChatGLM2-6B
- 提供Data Source外部数据接入解决方案
  - 提供外部数据接入，文档、url
- 构建更多类型tool
  - 数据库 SqlToolKit的构建 
    - 参考：[SqlDatabaseTookKit](https://github.com/hwchase17/langchain/blob/master/langchain/agents/agent_toolkits/sql/base.py#L14)
  - 接入更多类型的 search API，如google
- BaseFramework的role以及preset的功能是否需要去除，或者有更好的替代方案？
- Memory存储Agent相关的配置信息
- Memory兼容关系型数据库存储
- 完善文档，新增板块，提供LLM、prompt technique相关的知识扫盲
- Tree of Thoughts的嵌入方式作为mixin引入？需要进一步的讨论。
- 开发基于gradio的简易功能演示服务器
- 构建多Agent调度模型


## 其他发展计划
- ~~添加角色预设~~
- 为预设角色提供LLM的参数配置
- 提供prompt模板与prompt结构化
- 提供外部工具扩展
  - ~~外部搜索：Google,Bing等~~
  - 可以执行shell脚本
  - ~~提供Python REPL~~
  - 文件读写工具
  - ~~arxiv论文工具箱，总结，润色~~
  - arxiv上传论文、QA，提供答案索引，提供参考文献
  - 本地文件总结
  - 关系型数据库检索
  - 图数据库检索
- 对话存储
  - 提供向量数据库存储
  - 提供mysql, redis等数据库存储
- 自建知识库建立专家决策系统
- 接入self-ask, prompt-loop, tree of thoughts架构
- 提供多种导出方式
- 提供显示当前token（单词量）的功能
- ~~可以导出历史消息为markdown格式~~
- ~~使用环境变量配置key~~
- ~~添加错误处理机制，如网络异常、服务器异常等，保证程序的可靠性~~
- ~~提供完善的代理模式~~
- 提供gradio快速演示服务器
- ~~提供简易对话终端~~
- ~~封装消息体，完善消息体中的信息~~
- ~~长对话自动/手动总结~~
- ~~提供全局配置的缓存开关~~
- ~~提供限速等问题的错误提示~~
- ~~Conversation传入convesation_id继续上次对话~~
- ~~拷贝Conversation的持久化数据，开启一段新的历史对话~~
- 提供修改local_cache默认位置的方法
- 构建回调系统，在LLM执行的生命周期进行回调触发（使用[broadcast-service](https://github.com/Undertone0809/broadcast-service)构建）
- ~~提供基于LRU算法的API池，解决key限速的问题~~
- 为Key提供更多参数管理，如token管理等
- 提供代理池，收集市面上所有可用的免费代理进行轮询
- 构建结果正确率判别器
- 为工作空间提供定制化粒度
- 构建CacheManager（单例模式），对不同类型的数据与缓存进行调度管理
- 为Tool的LLM提供定制化的参数，提高结果的有效性
- 复现论文[https://arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)


