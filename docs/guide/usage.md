# 运行方式

`pne` 核心 SDK 只做能力拼装，不做运行时启动参数解析，推荐在 `use_cases/` 中保存具体入口。

## 通用调用示例

```python
from pne import build_adapter, build_agent

agent = build_agent(adapter=build_adapter("auto"))
print(agent.run("What is 17 * 23?"))
```

流式事件消费示例：

```python
import asyncio
from pne import build_adapter, build_agent


async def main() -> None:
    agent = build_agent(adapter=build_adapter("auto"))
    async for event in agent.run_stream("What is 17 * 23?"):
        print(f"[{event['type']}] {event.get('content') or event.get('output')}")


asyncio.run(main())
```

## 示例入口

本仓库的使用示例集中在 `use_cases/` 目录下维护，每个入口有独立的 README 与运行脚本。

如需接入新上下文（HTTP、CLI、任务队列），请在对应 `use_case` 模块封装启动逻辑。
