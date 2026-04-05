"""Example runner for the OpenAI Responses API agent."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from pne import build_openai_agent, load_local_skills


def _load_dotenv() -> None:
    if os.getenv("OPENAI_API_KEY"):
        return

    for directory in (Path.cwd(), *Path.cwd().parents):
        dotenv_path = directory / ".env"
        if not dotenv_path.is_file():
            continue
        for line in dotenv_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            key = key.strip()
            if not key or key in os.environ:
                continue
            os.environ[key] = value.strip().strip("'\"")
        if os.getenv("OPENAI_API_KEY"):
            return


def _prompt() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    return "Use the basic-math skill to compute 17 * 23."


def main() -> None:
    _load_dotenv()
    skill_root = Path(__file__).with_name("skills") / "basic_math"
    agent = build_openai_agent(skills=load_local_skills([skill_root]))
    print(agent.run(_prompt()))


if __name__ == "__main__":
    main()
