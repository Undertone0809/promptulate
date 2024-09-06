# Memory

> 文档完善中...

在正常使用 Agent 和 Prompt Framework 的时候，信息默认是无状态的，即交互产生的消息是不会被持久化的。然而在某些应用中，如聊天机器人，其需要利用读取上一次对话的历史数据，这个时候就需要用到消息持久化。`promptulate`
为 Agent 和 Framework 模块提供了 Memory 模块，用于进行数据的持久化。

**Memory 模块可以提供：**
- 用户与LLM交互产生的对话记录
- 存储Agent相关的配置信息 (计划中)
- 对话信息持久化
- 支持存储在不同类型的存储介质中

**当前 Memory 支持的存储方式**
- buffer临时缓存
- file文件存储
- 关系型数据库存储 (计划中)

## 在Framework中使用memory

参考文档[framework-Conversation](modules/framework?id=%e7%bb%a7%e7%bb%ad%e4%b8%8a%e4%b8%80%e6%ac%a1%e8%bf%90%e8%a1%8c%e7%9a%84%e5%af%b9%e8%af%9d)