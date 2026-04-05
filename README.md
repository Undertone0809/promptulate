# Promptulate

A new generation agent core.

## SDK

`pne` is a small SDK for building OpenAI-based ReACT agents.

Example usage lives in [use_cases/react_agent/README.md](use_cases/react_agent/README.md).

Client-side usage:

```python
from pne import build_agent

agent = build_agent()
answer = agent.run("What is 17 * 23?")
print(answer)
```

You can register your own tools by importing `ReActAgent` and `ToolSpec` from `pne`.
