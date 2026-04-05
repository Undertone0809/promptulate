"""Built-in tools for the Pne SDK."""

from __future__ import annotations

import ast
import os
import shlex
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from .types import ToolSpec


def _safe_calculate(expression: str) -> int | float:
    """Evaluate a simple arithmetic expression safely."""

    allowed_binops: dict[type[ast.AST], Any] = {
        ast.Add: lambda a, b: a + b,
        ast.Sub: lambda a, b: a - b,
        ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: a / b,
        ast.FloorDiv: lambda a, b: a // b,
        ast.Mod: lambda a, b: a % b,
        ast.Pow: lambda a, b: a**b,
    }
    allowed_unaryops: dict[type[ast.AST], Any] = {
        ast.UAdd: lambda a: a,
        ast.USub: lambda a: -a,
    }

    def evaluate(node: ast.AST) -> Any:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp):
            operator = allowed_binops.get(type(node.op))
            if operator is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            return operator(evaluate(node.left), evaluate(node.right))
        if isinstance(node, ast.UnaryOp):
            operator = allowed_unaryops.get(type(node.op))
            if operator is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            return operator(evaluate(node.operand))
        raise ValueError(f"Unsupported expression: {type(node).__name__}")

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree)


def calculator_tool() -> ToolSpec:
    return ToolSpec(
        name="calculator",
        description="Evaluate a simple arithmetic expression using +, -, *, /, //, %, and ** with parentheses.",
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Arithmetic expression to evaluate.",
                }
            },
            "required": ["expression"],
            "additionalProperties": False,
        },
        handler=lambda args: {"result": _safe_calculate(args["expression"])},
    )


def utc_now_tool() -> ToolSpec:
    return ToolSpec(
        name="utc_now",
        description="Return the current UTC time in ISO 8601 format.",
        parameters={
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        handler=lambda args: {"utc_now": datetime.now(timezone.utc).isoformat()},
    )


def shell_tool(*, base_path: str | Path = ".") -> ToolSpec:
    root = Path(base_path).expanduser().absolute()
    return ToolSpec(
        name="shell",
        description=(
            "Run a shell command string through /bin/sh (or cmd.exe on Windows). "
            "Use this for pipes, redirects, globbing, and other shell features."
        ),
        parameters={
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Shell command string to execute.",
                }
            },
            "required": ["command"],
            "additionalProperties": False,
        },
        handler=lambda args, _root=root: _shell_command_impl(args, base_path=_root),
    )


def _safe_path(base_path: Path, candidate: str | Path) -> Path:
    root = Path(os.path.abspath(str(base_path)))
    path = Path(candidate).expanduser()
    resolved_candidate = (
        Path(os.path.abspath(str(path)))
        if path.is_absolute()
        else Path(os.path.abspath(str(root / path)))
    )
    resolved = resolved_candidate
    if os.name == "nt":
        resolved = Path(os.path.normcase(str(resolved)))
        root = Path(os.path.normcase(str(root)))
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("Path traversal detected.") from exc
    return resolved


def _read_file_impl(args: dict[str, Any], *, base_path: Path) -> dict[str, str]:
    path = _safe_path(base_path, args["path"])
    if not path.exists():
        raise FileNotFoundError(f"File not found: {args['path']}")
    if path.is_dir():
        raise IsADirectoryError(f"Path is a directory: {args['path']}")

    content = path.read_text(encoding="utf-8", errors="replace")
    return {"path": str(path), "content": content}


def _list_dir_impl(
    args: dict[str, Any],
    *,
    base_path: Path,
) -> dict[str, Any]:
    path = _safe_path(base_path, args["path"])
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {args['path']}")
    if not path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {args['path']}")
    recursive = bool(args.get("recursive", False))
    entries: list[dict[str, str | bool | int]] = []
    iterator = path.rglob("*") if recursive else path.iterdir()
    for item in sorted(iterator, key=lambda p: p.name.lower()):
        if item.is_dir():
            item_type = "dir"
            size = 0
        else:
            item_type = "file"
            size = item.stat().st_size
        entries.append(
            {
                "name": item.name,
                "path": str(item),
                "type": item_type,
                "size": size,
            }
        )
    return {"path": str(path), "entries": entries}


def _search_in_files_impl(
    args: dict[str, Any],
    *,
    base_path: Path,
) -> list[dict[str, Any]]:
    search_base = _safe_path(base_path, args["base_path"])
    if not search_base.exists() or not search_base.is_dir():
        raise NotADirectoryError(f"Search base directory not found: {args['base_path']}")

    pattern = args.get("pattern", "")
    if not pattern:
        raise ValueError("pattern is required")

    include = str(args.get("include", "**/*"))
    results: list[dict[str, Any]] = []
    for candidate in sorted(
        search_base.glob(include),
        key=lambda p: str(p).lower(),
    ):
        if not candidate.is_file():
            continue
        try:
            text = candidate.read_text(encoding="utf-8", errors="replace")
        except UnicodeDecodeError:
            continue
        if pattern in text:
            lines = [
                {"line": index + 1, "text": line}
                for index, line in enumerate(text.splitlines())
                if pattern in line
            ]
            results.append(
                {
                    "path": str(candidate),
                    "matches": lines,
                }
            )
    return results


def _run_command_impl(
    args: dict[str, Any],
    *,
    base_path: Path,
    allow_command: bool,
    command_allowlist: tuple[str, ...],
) -> dict[str, Any]:
    if not allow_command:
        raise RuntimeError("Command execution is disabled for this agent instance.")

    command_text = str(args.get("command", "")).strip()
    if not command_text:
        raise ValueError("command is required")

    argv = shlex.split(command_text)
    binary = argv[0]
    if binary not in command_allowlist:
        raise RuntimeError(f"Command '{binary}' is not in the allowed list.")

    result = subprocess.run(
        argv,
        cwd=str(base_path),
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "command": command_text,
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def _shell_command_argv(command_text: str) -> list[str]:
    if os.name == "nt":
        return ["cmd.exe", "/c", command_text]
    return ["/bin/sh", "-c", command_text]


def _shell_command_impl(
    args: dict[str, Any],
    *,
    base_path: Path,
) -> dict[str, Any]:
    command_text = str(args.get("command", "")).strip()
    if not command_text:
        raise ValueError("command is required")

    argv = _shell_command_argv(command_text)
    result = subprocess.run(
        argv,
        cwd=str(base_path),
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "command": command_text,
        "shell": argv[0],
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def _write_file_impl(args: dict[str, Any], *, base_path: Path) -> dict[str, Any]:
    path = _safe_path(base_path, args["path"])
    content = str(args.get("content", ""))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return {"path": str(path), "bytes": len(content.encode("utf-8"))}


@dataclass(frozen=True)
class ToolPreset:
    base_path: str = "."
    allow_write: bool = False
    allow_command: bool = False
    allow_shell: bool = False
    command_allowlist: tuple[str, ...] = (
        "ls",
        "find",
        "rg",
        "git",
        "pwd",
        "echo",
    )


def build_local_tools(
    *,
    base_path: str = ".",
    include_builtins: bool = True,
    allow_write: bool = False,
    allow_command: bool = False,
    allow_shell: bool = False,
    command_allowlist: Sequence[str] = (
        "ls",
        "find",
        "rg",
        "git",
        "pwd",
        "echo",
    ),
) -> list[ToolSpec]:
    """Build a local default toolset for local agents."""

    root = Path(base_path).expanduser().absolute()
    allowlist = tuple(command_allowlist)

    tools: list[ToolSpec] = [
        ToolSpec(
            name="read_file",
            description=(
                "Read a text file and return its UTF-8 content. "
                "For binary files, best-effort decode with replacement."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path under base_path to read.",
                    }
                },
                "required": ["path"],
                "additionalProperties": False,
            },
            handler=lambda args, _root=root: _read_file_impl(args, base_path=_root),
        ),
        ToolSpec(
            name="list_dir",
            description=(
                "List a directory from base_path. "
                'Use "recursive": true for recursive listing.'
            ),
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path to list relative to base_path.",
                    },
                    "recursive": {
                        "type": "boolean",
                        "description": "Whether to recursively list nested files.",
                        "default": False,
                    },
                },
                "required": ["path"],
                "additionalProperties": False,
            },
            handler=lambda args, _root=root: _list_dir_impl(args, base_path=_root),
        ),
        ToolSpec(
            name="search_in_files",
            description=(
                "Search for a plain-text pattern in files under base_path."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "base_path": {
                        "type": "string",
                        "description": "Directory to search in (relative to base_path).",
                    },
                    "pattern": {
                        "type": "string",
                        "description": "Literal substring to match.",
                    },
                    "include": {
                        "type": "string",
                        "description": "Glob pattern for files, defaults to **/*.",
                        "default": "**/*",
                    },
                },
                "required": ["base_path", "pattern"],
                "additionalProperties": False,
            },
            handler=lambda args, _root=root: _search_in_files_impl(args, base_path=_root),
        ),
    ]

    if allow_command:
        tools.append(
            ToolSpec(
                name="run_command",
                description=(
                    "Run a shell command with strict allowlist checking. "
                    "Returns stdout/stderr/return_code."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The command string to execute.",
                        }
                    },
                    "required": ["command"],
                    "additionalProperties": False,
                },
                handler=lambda args, _root=root: _run_command_impl(
                    args,
                    base_path=_root,
                    allow_command=True,
                    command_allowlist=allowlist,
                ),
            )
        )

    if allow_shell:
        tools.append(shell_tool(base_path=root))

    if allow_write:
        tools.append(
            ToolSpec(
                name="write_file",
                description=(
                    "Write textual content to a file under base_path. "
                    "If the file exists, it will be overwritten."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Relative path under base_path to write.",
                        },
                        "content": {
                            "type": "string",
                            "description": "Text to write.",
                        },
                    },
                    "required": ["path", "content"],
                    "additionalProperties": False,
                },
                handler=lambda args, _root=root: _write_file_impl(args, base_path=_root),
            )
        )

    if include_builtins:
        tools.extend([calculator_tool(), utc_now_tool()])

    return tools
