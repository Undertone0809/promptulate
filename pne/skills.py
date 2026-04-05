"""Local skill loading helpers for the PNE SDK."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


def _parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text.strip()

    metadata: dict[str, str] = {}
    body_start = 1
    for index in range(1, len(lines)):
        line = lines[index].strip()
        if line == "---":
            body_start = index + 1
            break
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip().lower()] = value.strip().strip("'\"")

    body = "\n".join(lines[body_start:]).strip()
    return metadata, body


def _find_skill_manifest(path: Path) -> Path:
    if path.is_file():
        if path.name.lower() != "skill.md":
            raise FileNotFoundError(f"Skill file must be named SKILL.md: {path}")
        return path

    if not path.exists():
        raise FileNotFoundError(f"Skill path does not exist: {path}")

    candidates = sorted(
        candidate
        for candidate in path.iterdir()
        if candidate.is_file() and candidate.suffix.lower() == ".md" and candidate.name.lower() == "skill.md"
    )
    if not candidates:
        raise FileNotFoundError(f"No SKILL.md file found under: {path}")
    return candidates[0]


@dataclass(frozen=True)
class LocalSkill:
    """A local skill bundle rooted at a directory or SKILL.md file."""

    name: str
    description: str
    root: Path
    manifest_path: Path
    instructions: str

    @property
    def path(self) -> Path:
        return self.root


def load_local_skill(path: str | Path) -> LocalSkill:
    manifest_path = _find_skill_manifest(Path(path).expanduser().resolve())
    metadata, body = _parse_front_matter(manifest_path.read_text(encoding="utf-8"))
    root = manifest_path.parent
    return LocalSkill(
        name=metadata.get("name") or root.name,
        description=metadata.get("description") or "",
        root=root,
        manifest_path=manifest_path,
        instructions=body,
    )


def load_local_skills(paths: Sequence[str | Path]) -> list[LocalSkill]:
    return [load_local_skill(path) for path in paths]


def skill_context(skills: Sequence[LocalSkill]) -> str:
    if not skills:
        return ""

    lines = ["Available local skills:"]
    for skill in skills:
        lines.append(
            f"- {skill.name}: {skill.description or 'No description provided'} (path: {skill.manifest_path})"
        )
    lines.append("If a skill matches the task, read its SKILL.md at the listed path before acting.")
    return "\n".join(lines)
