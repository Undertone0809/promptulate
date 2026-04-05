"""Example runner for the PNE ReACT agent.

This lives under `use_cases/` so the SDK package stays import-only.
"""

from __future__ import annotations

import argparse
import sys

from pne import build_agent


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the PNE ReACT agent example.")
    parser.add_argument(
        "prompt", nargs="?", help="Prompt to send to the agent. Reads stdin if omitted."
    )
    parser.add_argument("--model", default="gpt-5.1", help="OpenAI model name.")
    parser.add_argument(
        "--reasoning-effort",
        default="low",
        help="Reasoning effort for reasoning models.",
    )
    args = parser.parse_args()

    prompt = args.prompt
    if prompt is None:
        prompt = sys.stdin.read().strip()

    agent = build_agent(model=args.model, reasoning_effort=args.reasoning_effort)
    print(agent.run(prompt))


if __name__ == "__main__":
    main()
