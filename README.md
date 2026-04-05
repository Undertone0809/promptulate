# Promptulate

A new generation agent core plus local interactive CLI.

Official site: https://pne.zeeland.studio

## Workspace layout

This repo adopts a small workspace:

- `packages/pne` → pure SDK package, import `pne`
- `packages/pne-cli` → terminal UI package, command `pne`

`pne` remains side-effect free and import-friendly. CLI-specific behavior (stdin/stdout, confirmation prompts, session control) lives in `pne_cli`.

## SDK Quick Start

```python
from pne import build_adapter, build_agent

agent = build_agent(adapter=build_adapter("auto"))
print(agent.run("What is 17 * 23?"))
```

Build local tools:

```python
from pne import build_local_tools, build_agent

agent = build_agent(
    adapter=build_adapter("auto"),
    tools=build_local_tools(
        base_path=".",
        allow_write=False,  # optional
        allow_command=False,  # enable run_command explicitly
        allow_shell=False,  # enable shell explicitly when you need pipes/redirects
    ),
)
```

Async stream API:

```python
import asyncio
from pne import build_adapter, build_agent


async def main() -> None:
    agent = build_agent(adapter=build_adapter("auto"))
    async for event in agent.run_stream("What is 17 * 23?"):
        print(event["type"], "=>", event.get("content") or event.get("output"))


    asyncio.run(main())
```

## CLI quick start

```bash
cd promptulate
uv sync
uv run pne ask "What is 17 * 23?"
uv run pne chat
```

- `pne chat`: interactive multi-turn REPL, supports `/reset`, `/quit`.
- `pne ask`: one-shot ask.
- Use `--approve-commands` to expose `run_command` and `--allow-write` to expose `write_file`.
- Use `--allow-shell` to expose a full shell tool when the agent needs pipes, redirects, or shell expansion.
- Use `--trace-json` to keep raw event logs for replay.

Examples and reference entry points are still in:

- `use_cases/react_agent/README.md`
- `use_cases/openai_agent/README.md`
- `use_cases/claude_code/README.md`
- `use_cases/codex/README.md`

Provider SDKs are optional extras:

```bash
uv add "pne[openai]"
uv add "pne[anthropic]"
```

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
