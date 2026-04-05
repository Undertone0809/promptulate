# 运行方式

`pne` 核心 SDK 负责能力拼装，不直接承担运行参数解析；本仓库为 workspace 结构，`pne_cli` 负责交互式入口。

## SDK 示例

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

本地工具示例：

```python
from pne import build_adapter, build_agent, build_local_tools

agent = build_agent(
    adapter=build_adapter("auto"),
    tools=build_local_tools(base_path=".", allow_write=False, allow_command=False),
)
```

## CLI 使用

```bash
uv run pne ask "列一个 3x3 表格"
uv run pne chat
```

`pne chat` 逐步输出：

- `step_start`
- `model_turn`
- `tool_call`
- `tool_output`
- `final`

会话内置命令：

- `/quit`：退出
- `/reset`：清空历史
- `/help`：显示帮助
