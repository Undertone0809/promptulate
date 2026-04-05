# Promptulate

A new generation agent core.

## SDK

`pne` is a small SDK for building ReACT agents across OpenAI, Anthropic, and local command-based backends.

Provider SDKs are optional extras:

```bash
uv add "pne[openai]"
uv add "pne[anthropic]"
```

If you do not install any provider extra, the runtime can still use local command-based adapters when available on `PATH`.

Example usage lives in [use_cases/react_agent/README.md](use_cases/react_agent/README.md).
An OpenAI Responses API example with a local skill bundle lives in [use_cases/openai_agent/README.md](use_cases/openai_agent/README.md).

Client-side usage:

```python
from pne import build_adapter, build_agent

agent = build_agent(adapter=build_adapter("auto"))
answer = agent.run("What is 17 * 23?")
print(answer)
```

You can register your own tools by importing `ReActAgent` and `ToolSpec` from `pne`.
