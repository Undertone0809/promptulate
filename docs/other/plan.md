# 开发计划

如果你有更好的建议，欢迎一起讨论，你可以通过[issue](https://github.com/Undertone0809/promptulate/issues)
，email，以及[交流群](README.md#交流群)进行交流。


## v1.4.0 发展计划
- [v1.4.0开发计划]()

## 其他发展计划

### Tool
- image_generate

### Other
- ~~添加角色预设~~
- 为预设角色提供LLM的参数配置
- ~~提供prompt模板与prompt结构化~~
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
- 尝试接入[https://github.com/zilliztech/GPTCache](https://github.com/zilliztech/GPTCache)构建LLMCache，提高响应能力
- 尝试兼容langchain组件
- 兼容接入langsmith
- 用ChatOpenAI+text context memory构建chain
