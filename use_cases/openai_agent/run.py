"""Example runner for the unified agent with local skills."""

from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv
from pne import build_agent, build_adapter, load_local_skills


def _prompt() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    return "Use the basic-math skill to compute 17 * 23."


def main() -> None:
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    skill_root = Path(__file__).with_name("skills") / "basic_math"
    agent = build_agent(
        adapter=build_adapter("auto"),
        skills=load_local_skills([skill_root]),
    )
    print(agent.run(_prompt(), verbose=True))


if __name__ == "__main__":
    main()
