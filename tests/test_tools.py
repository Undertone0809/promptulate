from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from pne import build_local_tools, ToolSpec


class TestLocalTools(TestCase):
    def test_build_local_tools_without_write_does_not_expose_danger(self) -> None:
        tools = {tool.name: tool for tool in build_local_tools(base_path=".", allow_write=False, allow_command=False)}
        self.assertIn("read_file", tools)
        self.assertIn("list_dir", tools)
        self.assertIn("search_in_files", tools)
        self.assertIn("calculator", tools)
        self.assertIn("utc_now", tools)
        self.assertNotIn("write_file", tools)
        self.assertNotIn("run_command", tools)

    def test_read_file_and_path_traversal(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "a.txt"
            target.write_text("hello", encoding="utf-8")

            tools = {tool.name: tool for tool in build_local_tools(base_path=tmp, allow_write=False)}
            read_tool: ToolSpec = tools["read_file"]

            got = read_tool.handler({"path": "a.txt"})
            self.assertEqual({"path": str(target), "content": "hello"}, got)

            with self.assertRaises(ValueError):
                read_tool.handler({"path": "../evil.txt"})

    def test_list_dir_supports_recursive(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a").mkdir()
            (root / "a" / "x.txt").write_text("x", encoding="utf-8")
            (root / "b.txt").write_text("b", encoding="utf-8")

            list_tool: ToolSpec = {tool.name: tool for tool in build_local_tools(base_path=tmp)}["list_dir"]
            got = list_tool.handler({"path": ".", "recursive": True})["entries"]
            names = sorted(item["name"] for item in got)
            self.assertIn("a", names)
            self.assertIn("b.txt", names)
            self.assertIn("x.txt", names)

    def test_search_in_files_and_missing_base_path(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.txt").write_text("alpha beta\n", encoding="utf-8")
            (root / "b.md").write_text("nope\n", encoding="utf-8")

            search_tool: ToolSpec = {tool.name: tool for tool in build_local_tools(base_path=tmp)}["search_in_files"]
            matches = search_tool.handler({"base_path": ".", "pattern": "alpha"})
            self.assertEqual(1, len(matches))
            self.assertEqual(str(root / "a.txt"), matches[0]["path"])

            with self.assertRaises(NotADirectoryError):
                search_tool.handler({"base_path": "missing", "pattern": "x"})

    def test_write_file_enabled_only_when_allowed(self) -> None:
        with TemporaryDirectory() as tmp:
            tools = {tool.name: tool for tool in build_local_tools(base_path=tmp, allow_write=True)}
            write_tool: ToolSpec = tools["write_file"]
            payload = {"path": "sub/out.txt", "content": "ok"}
            write_tool.handler(payload)
            self.assertEqual("ok", (Path(tmp) / "sub" / "out.txt").read_text(encoding="utf-8"))

            tools_disabled = {tool.name: tool for tool in build_local_tools(base_path=tmp, allow_write=False)}
            self.assertNotIn("write_file", tools_disabled)

    def test_command_tool_respects_allowlist(self) -> None:
        with TemporaryDirectory() as tmp:
            tools = {tool.name: tool for tool in build_local_tools(base_path=tmp, allow_command=True)}
            command_tool: ToolSpec = tools["run_command"]
            with self.assertRaises(RuntimeError):
                command_tool.handler({"command": "rm -rf /tmp"})
