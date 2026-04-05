from __future__ import annotations

import tempfile
from pathlib import Path
from unittest import TestCase

from pne.skills import LocalSkill, load_local_skill, load_local_skills, skill_context


class TestSkills(TestCase):
    def test_skill_loading_and_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "math"
            root.mkdir()
            (root / "SKILL.md").write_text(
                """
---
name: basic-math
description: Basic arithmetic helper
---
Use this skill for arithmetic.
""".lstrip(),
                encoding="utf-8",
            )

            skill = load_local_skill(root)
            self.assertIsInstance(skill, LocalSkill)
            self.assertEqual("basic-math", skill.name)
            self.assertEqual("Basic arithmetic helper", skill.description)
            self.assertIn("Use this skill for arithmetic.", skill.instructions)

            context = skill_context([skill])
            self.assertTrue(context.startswith("Available local skills:"))
            self.assertIn("- basic-math: Basic arithmetic helper", context)
            self.assertIn("(path:", context)

            loaded = load_local_skills([root, str(root)])
            self.assertEqual(2, len(loaded))
            self.assertEqual("basic-math", loaded[0].name)

    def test_load_local_skill_accepts_manifest_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "SKILL.md"
            manifest.write_text("name: manifest\n", encoding="utf-8")
            skill = load_local_skill(manifest)
            self.assertEqual(root.resolve(), skill.root)
            self.assertEqual(manifest.resolve(), skill.manifest_path)

    def test_load_local_skill_invalid_path_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            text_file = Path(tmp) / "README.md"
            text_file.write_text("hello", encoding="utf-8")
            with self.assertRaises(FileNotFoundError):
                load_local_skill(Path(tmp) / "MISSING")

            with self.assertRaises(FileNotFoundError):
                load_local_skill(text_file)

    def test_skill_context_with_empty_skills(self) -> None:
        self.assertEqual("", skill_context([]))
