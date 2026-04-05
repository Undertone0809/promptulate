"""Example runner for the PNE ReACT agent with Claude Code."""

from __future__ import annotations

import sys

from pne import build_adapter, build_agent


def _read_prompt() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    return sys.stdin.read().strip()


def main() -> None:
    prompt = _read_prompt()
    adapter = build_adapter("claude-code")
    agent = build_agent(adapter=adapter)
    print(agent.run(prompt))


if __name__ == "__main__":
    main()
