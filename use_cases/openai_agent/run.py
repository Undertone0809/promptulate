"""Example runner for the OpenAI Responses API agent."""

from __future__ import annotations

import sys
from pathlib import Path

from pne import build_openai_agent, load_local_skills


def _prompt() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    return "Use the basic-math skill to compute 17 * 23."


def main() -> None:
    skill_root = Path(__file__).with_name("skills") / "basic_math"
    agent = build_openai_agent(skills=load_local_skills([skill_root]))
    print(agent.run(_prompt()))


if __name__ == "__main__":
    main()
