# Promptulate

A new generation agent core.

## SDK

`pne` is a small SDK for building agents across OpenAI, Anthropic, and local command-based backends.

Provider SDKs are optional extras:

```bash
uv add "pne[openai]"
uv add "pne[anthropic]"
```

If you do not install any provider extra, the runtime can still use local command-based adapters when available on `PATH`.

Example usage lives in [use_cases/react_agent/README.md](use_cases/react_agent/README.md).
An alternative unified-agent example with local skills lives in [use_cases/openai_agent/README.md](use_cases/openai_agent/README.md).
You can also inspect [use_cases/claude_code/README.md](use_cases/claude_code/README.md) and [use_cases/codex/README.md](use_cases/codex/README.md).
Example runners may load a repository-local `.env`, but the SDK itself does not.

Client-side usage:

```python
from pne import build_adapter, build_agent

agent = build_agent(adapter=build_adapter("auto"))
answer = agent.run("What is 17 * 23?")
print(answer)
```

`build_agent` now constructs the normal production agent.
`ReActAgent` is kept as an experimental variant and can be built explicitly.

You can register your own tools by importing `ToolSpec` from `pne`, and optionally
try `ReActAgent` for the experimental ReAct style.

## Docs

This repository includes a VitePress documentation site in `docs/`.

```bash
cd docs
npm install
npm run docs:dev
```

Deploy to Vercel is configured via `vercel.json`:

- Install command: `cd docs && npm install`
- Build command: `cd docs && npm run docs:build`
- Output directory: `docs/.vitepress/dist`
