# Promptulate

A new generation agent core.

## ReAct Agent

This repo now includes a minimal OpenAI ReAct agent in `pne/react_agent.py`.

Run it with:

```bash
export OPENAI_API_KEY=your_key
uv run pne-react "What is 17 * 23?"
```

You can register your own tools by importing `ReActAgent` and `ToolSpec` from `pne`.
