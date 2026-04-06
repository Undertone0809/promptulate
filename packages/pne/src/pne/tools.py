"""Built-in tools for the Pne SDK."""

from __future__ import annotations

import ast
import os
import re
import shlex
import subprocess
import time
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
                '"recursive": true for recursive listing.'
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


# =============================================================================
# Advanced Tools (new)
# =============================================================================

class BashSecurityAnalyzer:
    """Lightweight security analyzer for bash commands.

    Detects dangerous operations, destructive commands, and injection patterns.
    Inspired by Claude Code's bash security but kept practical for this SDK.
    """

    # Dangerous command patterns: (regex, description)
    DANGEROUS_PATTERNS: list[tuple[re.Pattern[str], str]] = [
        # Destructive file operations
        (re.compile(r"\brm\s+.*-[rfR]+", re.IGNORECASE), "rm with force/recursive flags"),
        (re.compile(r"\brm\s+.*\b/\b", re.IGNORECASE), "rm targeting root directory"),
        (re.compile(r"\brm\s+.*\b\.\b", re.IGNORECASE), "rm targeting current directory"),
        (re.compile(r"\brmdir\s+.*-[rfR]+", re.IGNORECASE), "rmdir with force flags"),
        (re.compile(r"\bmkfs\b", re.IGNORECASE), "filesystem formatting"),
        (re.compile(r"\bdd\s+.*of=", re.IGNORECASE), "dd write operation"),
        (re.compile(r"\b:\(\)\s*\{\s*:\s*\|:\s*\}&", re.IGNORECASE), "fork bomb"),
        # Destructive git operations
        (re.compile(r"\bgit\s+push\s+.*--force\b", re.IGNORECASE), "git force push"),
        (re.compile(r"\bgit\s+push\s+.*\s+-f\b", re.IGNORECASE), "git force push (-f)"),
        (re.compile(r"\bgit\s+reset\s+.*--hard\b", re.IGNORECASE), "git hard reset"),
        (re.compile(r"\bgit\s+clean\s+.*-[dfx]+", re.IGNORECASE), "git clean with force"),
        (re.compile(r"\bgit\s+filter-branch\b", re.IGNORECASE), "git filter-branch (rewrites history)"),
        # Database destructive operations
        (re.compile(r"\bDROP\s+TABLE\b", re.IGNORECASE), "SQL DROP TABLE"),
        (re.compile(r"\bDROP\s+DATABASE\b", re.IGNORECASE), "SQL DROP DATABASE"),
        (re.compile(r"\bDELETE\s+FROM\b", re.IGNORECASE), "SQL DELETE FROM"),
        (re.compile(r"\bTRUNCATE\s+TABLE\b", re.IGNORECASE), "SQL TRUNCATE"),
        # System modifications
        (re.compile(r"\bsudo\b", re.IGNORECASE), "sudo privilege escalation"),
        (re.compile(r"\bsu\s+-", re.IGNORECASE), "switch user"),
        (re.compile(r"\bchmod\s+.*777\b", re.IGNORECASE), "chmod 777"),
        (re.compile(r"\bchown\s+.*-R\b", re.IGNORECASE), "recursive chown"),
        (re.compile(r"\bkillall\b", re.IGNORECASE), "killall"),
        (re.compile(r"\bpkill\b", re.IGNORECASE), "pkill"),
        (re.compile(r"\bshutdown\b", re.IGNORECASE), "shutdown"),
        (re.compile(r"\breboot\b", re.IGNORECASE), "reboot"),
        (re.compile(r"\binit\s+0\b", re.IGNORECASE), "init 0 (shutdown)"),
        # Network/remote
        (re.compile(r"\bcurl\s+.*\|\s*sh\b", re.IGNORECASE), "curl pipe to shell"),
        (re.compile(r"\bwget\s+.*\|\s*sh\b", re.IGNORECASE), "wget pipe to shell"),
        (re.compile(r"\bcurl\s+.*\|\s*bash\b", re.IGNORECASE), "curl pipe to bash"),
    ]

    # Injection patterns that are always suspicious
    INJECTION_PATTERNS: list[tuple[re.Pattern[str], str]] = [
        (re.compile(r"\$\s*\("), "command substitution $()"),
        (re.compile(r"`[^`]*`"), "backtick command substitution"),
        (re.compile(r"\$\{[^}]*\}"), "parameter expansion ${}"),
        (re.compile(r"\|\s*rm\b", re.IGNORECASE), "pipe to rm"),
        (re.compile(r"\|\s*sh\b", re.IGNORECASE), "pipe to sh"),
        (re.compile(r"\|\s*bash\b", re.IGNORECASE), "pipe to bash"),
        (re.compile(r">\s*/dev/(null|zero|random|urandom)"), "dangerous redirection"),
        (re.compile(r"2>&1\s*>\s*/dev/"), "stderr redirection to device"),
    ]

    def analyze(self, command: str) -> dict[str, Any]:
        """Analyze a command for security concerns.

        Returns a dict with:
        - safe: bool - whether the command passes all checks
        - concerns: list[str] - list of detected concerns
        - needs_confirmation: bool - whether user confirmation is recommended
        """
        concerns: list[str] = []
        cmd_lower = command.lower().strip()

        # Check dangerous patterns
        for pattern, description in self.DANGEROUS_PATTERNS:
            if pattern.search(command):
                concerns.append(f"Dangerous: {description}")

        # Check injection patterns
        for pattern, description in self.INJECTION_PATTERNS:
            if pattern.search(command):
                concerns.append(f"Suspicious: {description}")

        # Check for empty or trivial commands
        if not cmd_lower or cmd_lower in {"true", "false", ":", "echo"}:
            return {"safe": True, "concerns": [], "needs_confirmation": False}

        needs_confirmation = len(concerns) > 0
        return {
            "safe": not needs_confirmation,
            "concerns": concerns,
            "needs_confirmation": needs_confirmation,
        }


# Global analyzer instance
_bash_analyzer = BashSecurityAnalyzer()


def _bash_impl(
    args: dict[str, Any],
    *,
    base_path: Path,
) -> dict[str, Any]:
    """Execute a bash command with optional safety analysis."""
    command_text = str(args.get("command", "")).strip()
    if not command_text:
        raise ValueError("command is required")

    timeout = int(args.get("timeout", 120000))
    if timeout <= 0 or timeout > 600000:
        timeout = 120000

    description = str(args.get("description", "")).strip()
    run_in_background = bool(args.get("run_in_background", False))

    # Run the command
    argv = _shell_command_argv(command_text)

    if run_in_background:
        # Start process in background and return immediately
        proc = subprocess.Popen(
            argv,
            cwd=str(base_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return {
            "command": command_text,
            "description": description,
            "return_code": None,
            "stdout": "",
            "stderr": "",
            "interrupted": False,
            "background": True,
            "pid": proc.pid,
        }

    try:
        result = subprocess.run(
            argv,
            cwd=str(base_path),
            text=True,
            capture_output=True,
            timeout=timeout / 1000,
            check=False,
        )
        return {
            "command": command_text,
            "description": description,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "interrupted": False,
            "background": False,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command_text,
            "description": description,
            "return_code": -1,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "interrupted": True,
            "background": False,
        }


def bash_tool(*, base_path: str | Path = ".") -> ToolSpec:
    """Build a bash tool with safety analysis metadata."""
    root = Path(base_path).expanduser().absolute()
    return ToolSpec(
        name="bash",
        description=(
            "Execute shell commands in the user's terminal with safety analysis. "
            "Runs commands through a safety analyzer that detects destructive operations "
            "(rm -rf, git push --force, etc.). Commands run in the user's shell environment "
            "with full access to installed tools."
        ),
        parameters={
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to execute.",
                },
                "timeout": {
                    "type": "integer",
                    "description": "Optional timeout in milliseconds (max 600000, default 120000).",
                    "default": 120000,
                },
                "description": {
                    "type": "string",
                    "description": "Clear, concise description of what this command does in active voice.",
                },
                "run_in_background": {
                    "type": "boolean",
                    "description": "Set to true to run this command in the background.",
                    "default": False,
                },
            },
            "required": ["command"],
            "additionalProperties": False,
        },
        handler=lambda args, _root=root: _bash_impl(args, base_path=_root),
    )


def analyze_bash_command(command: str) -> dict[str, Any]:
    """Public API to analyze a bash command for security concerns."""
    return _bash_analyzer.analyze(command)


# =============================================================================
# File operation tools (advanced)
# =============================================================================

def _file_read_impl(args: dict[str, Any], *, base_path: Path) -> dict[str, Any]:
    path = _safe_path(base_path, args["path"])
    if not path.exists():
        raise FileNotFoundError(f"File not found: {args['path']}")
    if path.is_dir():
        raise IsADirectoryError(f"Path is a directory: {args['path']}")

    content = path.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()

    offset = int(args.get("offset", 1))
    limit = args.get("limit")

    if offset < 1:
        offset = 1

    start_idx = offset - 1
    if limit is not None:
        limit = int(limit)
        end_idx = start_idx + limit
        selected_lines = lines[start_idx:end_idx]
    else:
        selected_lines = lines[start_idx:]

    selected_content = "\n".join(selected_lines)

    return {
        "path": str(path),
        "content": selected_content,
        "total_lines": len(lines),
        "offset": offset,
        "limit": limit,
    }


def _file_edit_impl(args: dict[str, Any], *, base_path: Path) -> dict[str, Any]:
    path = _safe_path(base_path, args["path"])
    if not path.exists():
        raise FileNotFoundError(f"File not found: {args['path']}")
    if path.is_dir():
        raise IsADirectoryError(f"Path is a directory: {args['path']}")

    old_string = str(args.get("old_string", ""))
    new_string = str(args.get("new_string", ""))

    content = path.read_text(encoding="utf-8")

    if old_string not in content:
        raise ValueError(f"old_string not found in file: {args['path']}")

    new_content = content.replace(old_string, new_string, 1)
    path.write_text(new_content, encoding="utf-8")

    return {
        "path": str(path),
        "replaced": True,
        "old_bytes": len(content.encode("utf-8")),
        "new_bytes": len(new_content.encode("utf-8")),
    }


def _file_write_impl(args: dict[str, Any], *, base_path: Path) -> dict[str, Any]:
    path = _safe_path(base_path, args["path"])
    content = str(args.get("content", ""))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return {"path": str(path), "bytes": len(content.encode("utf-8"))}


def _glob_impl(args: dict[str, Any], *, base_path: Path) -> dict[str, Any]:
    search_path = _safe_path(base_path, args.get("path", "."))
    pattern = str(args.get("pattern", "*"))

    if not search_path.exists():
        raise FileNotFoundError(f"Path not found: {args.get('path', '.')}")

    matches = sorted(search_path.glob(pattern), key=lambda p: str(p).lower())
    results: list[dict[str, Any]] = []
    for match in matches:
        results.append({
            "path": str(match),
            "name": match.name,
            "type": "dir" if match.is_dir() else "file",
        })

    return {
        "pattern": pattern,
        "base_path": str(search_path),
        "matches": results,
    }


def _grep_impl(args: dict[str, Any], *, base_path: Path) -> dict[str, Any]:
    search_path = _safe_path(base_path, args.get("path", "."))
    pattern_str = str(args.get("pattern", ""))
    output_mode = str(args.get("output_mode", "content"))

    if not pattern_str:
        raise ValueError("pattern is required")

    try:
        regex = re.compile(pattern_str)
    except re.error as exc:
        raise ValueError(f"Invalid regex pattern: {exc}") from exc

    if not search_path.exists():
        raise FileNotFoundError(f"Path not found: {args.get('path', '.')}")

    results: list[dict[str, Any]] = []
    file_matches: list[str] = []

    if search_path.is_file():
        files_to_search = [search_path]
    else:
        files_to_search = sorted(search_path.rglob("*"), key=lambda p: str(p).lower())

    for candidate in files_to_search:
        if not candidate.is_file():
            continue
        try:
            text = candidate.read_text(encoding="utf-8", errors="replace")
        except (UnicodeDecodeError, OSError):
            continue

        file_has_match = False
        file_results: list[dict[str, Any]] = []

        for idx, line in enumerate(text.splitlines(), start=1):
            if regex.search(line):
                file_has_match = True
                file_results.append({"line": idx, "text": line})

        if file_has_match:
            file_matches.append(str(candidate))
            if output_mode == "content":
                results.append({
                    "path": str(candidate),
                    "matches": file_results,
                })

    if output_mode == "files_with_matches":
        return {
            "pattern": pattern_str,
            "matches": [{"path": p} for p in file_matches],
        }

    return {
        "pattern": pattern_str,
        "matches": results,
    }


def _notebook_edit_impl(args: dict[str, Any], *, base_path: Path) -> dict[str, Any]:
    try:
        import nbformat
    except ImportError as exc:
        raise RuntimeError(
            "nbformat is required for NotebookEdit. Install with: pip install 'pne[notebook]'"
        ) from exc

    notebook_path = _safe_path(base_path, args["notebook_path"])
    if not notebook_path.exists():
        raise FileNotFoundError(f"Notebook not found: {args['notebook_path']}")

    cell_number = int(args.get("cell_number", 0))
    new_source = str(args.get("new_source", ""))
    edit_mode = str(args.get("edit_mode", "replace"))

    notebook = nbformat.read(str(notebook_path), as_version=4)

    if cell_number < 0 or cell_number >= len(notebook.cells):
        raise ValueError(
            f"Invalid cell_number {cell_number}. Notebook has {len(notebook.cells)} cells."
        )

    if edit_mode == "replace":
        notebook.cells[cell_number].source = new_source
    elif edit_mode == "insert":
        new_cell = nbformat.v4.new_code_cell(new_source)
        notebook.cells.insert(cell_number, new_cell)
    elif edit_mode == "delete":
        del notebook.cells[cell_number]
    else:
        raise ValueError(f"Invalid edit_mode: {edit_mode}. Use replace, insert, or delete.")

    nbformat.write(notebook, str(notebook_path))

    return {
        "notebook_path": str(notebook_path),
        "cell_number": cell_number,
        "edit_mode": edit_mode,
        "total_cells": len(notebook.cells),
    }


def _repl_impl(args: dict[str, Any]) -> dict[str, Any]:
    code = str(args.get("code", "")).strip()
    if not code:
        raise ValueError("code is required")

    # Safe evaluation using AST
    try:
        tree = ast.parse(code, mode="exec")
    except SyntaxError as exc:
        return {"error": f"Syntax error: {exc}"}

    # Only allow simple expressions and assignments
    allowed_nodes = (
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, ast.Name,
        ast.Load, ast.Store, ast.Assign, ast.Expr, ast.Add, ast.Sub,
        ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow, ast.USub,
        ast.UAdd, ast.Call, ast.Attribute, ast.Subscript, ast.Index,
        ast.Tuple, ast.List, ast.Dict, ast.Str, ast.Num, ast.keyword,
        ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
        ast.IfExp, ast.BoolOp, ast.And, ast.Or, ast.Not, ast.In, ast.Is,
        ast.JoinedStr, ast.FormattedValue, ast.ListComp, ast.DictComp,
        ast.GeneratorExp, ast.comprehension, ast.If, ast.For, ast.While,
        ast.Break, ast.Continue, ast.Pass, ast.With, ast.withitem,
        ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Return,
        ast.Yield, ast.YieldFrom, ast.Await, ast.Raise, ast.Try,
        ast.ExceptHandler, ast.Assert, ast.Delete, ast.Global, ast.Nonlocal,
        ast.Lambda, ast.arguments, ast.arg, ast.Import, ast.ImportFrom,
        ast.alias, ast.Module, ast.Interactive, ast.Expression,
    )

    for node in ast.walk(tree):
        if not isinstance(node, allowed_nodes):
            return {"error": f"Unsupported Python construct: {type(node).__name__}"}

    # Execute in restricted namespace
    namespace: dict[str, Any] = {
        "__builtins__": {
            "abs": abs, "all": all, "any": any, "bin": bin, "bool": bool,
            "chr": chr, "dict": dict, "divmod": divmod, "enumerate": enumerate,
            "filter": filter, "float": float, "format": format, "frozenset": frozenset,
            "hasattr": hasattr, "hex": hex, "int": int, "isinstance": isinstance,
            "issubclass": issubclass, "iter": iter, "len": len, "list": list,
            "map": map, "max": max, "min": min, "next": next, "oct": oct,
            "ord": ord, "pow": pow, "print": print, "range": range,
            "repr": repr, "reversed": reversed, "round": round, "set": set,
            "slice": slice, "sorted": sorted, "str": str, "sum": sum,
            "tuple": tuple, "type": type, "zip": zip,
        },
    }

    stdout_capture: list[str] = []
    original_stdout_write = None

    class MockStdout:
        def write(self, text: str) -> int:
            stdout_capture.append(text)
            return len(text)
        def flush(self) -> None:
            pass

    import sys as _sys
    old_stdout = _sys.stdout
    try:
        _sys.stdout = MockStdout()
        exec(compile(tree, filename="<repl>", mode="exec"), namespace)
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}
    finally:
        _sys.stdout = old_stdout

    # Get the last expression value if any
    last_value = None
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        try:
            last_value = eval(compile(ast.Expression(tree.body[-1].value), filename="<repl>", mode="eval"), namespace)
        except Exception:
            pass

    result: dict[str, Any] = {
        "stdout": "".join(stdout_capture),
    }

    if last_value is not None:
        result["result"] = repr(last_value)

    return result


def _ask_user_question_impl(args: dict[str, Any]) -> dict[str, Any]:
    question = str(args.get("question", "")).strip()
    if not question:
        raise ValueError("question is required")

    print(f"\n[Agent asks] {question}")
    answer = input("Your answer: ").strip()
    return {"question": question, "answer": answer}


def _sleep_impl(args: dict[str, Any]) -> dict[str, Any]:
    duration = int(args.get("duration", 0))
    if duration < 0:
        duration = 0
    if duration > 300000:
        duration = 300000  # max 5 minutes

    time.sleep(duration / 1000)
    return {"duration": duration, "status": "slept"}


# =============================================================================
# Tool factory functions
# =============================================================================

def file_read_tool(*, base_path: str | Path = ".") -> ToolSpec:
    root = Path(base_path).expanduser().absolute()
    return ToolSpec(
        name="FileRead",
        description=(
            "Read a text file and return its UTF-8 content. "
            "Supports offset (1-based line number) and limit for partial reads."
        ),
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path under base_path to read.",
                },
                "offset": {
                    "type": "integer",
                    "description": "1-based starting line number. Default is 1.",
                    "default": 1,
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of lines to read. Omit for all.",
                },
            },
            "required": ["path"],
            "additionalProperties": False,
        },
        handler=lambda args, _root=root: _file_read_impl(args, base_path=_root),
    )


def file_edit_tool(*, base_path: str | Path = ".") -> ToolSpec:
    root = Path(base_path).expanduser().absolute()
    return ToolSpec(
        name="FileEdit",
        description=(
            "Edit a file by replacing a string with another string. "
            "The old_string must exist exactly in the file."
        ),
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path under base_path to edit.",
                },
                "old_string": {
                    "type": "string",
                    "description": "Exact text to replace.",
                },
                "new_string": {
                    "type": "string",
                    "description": "Text to insert in place of old_string.",
                },
            },
            "required": ["path", "old_string", "new_string"],
            "additionalProperties": False,
        },
        handler=lambda args, _root=root: _file_edit_impl(args, base_path=_root),
    )


def file_write_tool(*, base_path: str | Path = ".") -> ToolSpec:
    root = Path(base_path).expanduser().absolute()
    return ToolSpec(
        name="FileWrite",
        description=(
            "Write textual content to a file under base_path. "
            "If the file exists, it will be overwritten. Parent directories are created as needed."
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
        handler=lambda args, _root=root: _file_write_impl(args, base_path=_root),
    )


def glob_tool(*, base_path: str | Path = ".") -> ToolSpec:
    root = Path(base_path).expanduser().absolute()
    return ToolSpec(
        name="Glob",
        description=(
            "Find files matching a glob pattern under base_path. "
            "Supports ** for recursive matching."
        ),
        parameters={
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Glob pattern to match (e.g., '**/*.py').",
                },
                "path": {
                    "type": "string",
                    "description": "Directory to search in (relative to base_path). Defaults to base_path.",
                },
            },
            "required": ["pattern"],
            "additionalProperties": False,
        },
        handler=lambda args, _root=root: _glob_impl(args, base_path=_root),
    )


def grep_tool(*, base_path: str | Path = ".") -> ToolSpec:
    root = Path(base_path).expanduser().absolute()
    return ToolSpec(
        name="Grep",
        description=(
            "Search for a regex pattern in files under base_path. "
            "Returns matching lines with line numbers."
        ),
        parameters={
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Regex pattern to search for.",
                },
                "path": {
                    "type": "string",
                    "description": "File or directory to search in (relative to base_path). Defaults to base_path.",
                },
                "output_mode": {
                    "type": "string",
                    "description": "Output format: 'content' (with line numbers) or 'files_with_matches' (just file paths).",
                    "enum": ["content", "files_with_matches"],
                    "default": "content",
                },
            },
            "required": ["pattern"],
            "additionalProperties": False,
        },
        handler=lambda args, _root=root: _grep_impl(args, base_path=_root),
    )


def notebook_edit_tool(*, base_path: str | Path = ".") -> ToolSpec:
    root = Path(base_path).expanduser().absolute()
    return ToolSpec(
        name="NotebookEdit",
        description=(
            "Edit a Jupyter notebook (.ipynb) by replacing, inserting, or deleting a cell. "
            "Requires nbformat to be installed (pip install 'pne[notebook]')."
        ),
        parameters={
            "type": "object",
            "properties": {
                "notebook_path": {
                    "type": "string",
                    "description": "Path to the .ipynb file (relative to base_path).",
                },
                "cell_number": {
                    "type": "integer",
                    "description": "0-based index of the cell to edit.",
                },
                "new_source": {
                    "type": "string",
                    "description": "New source code/text for the cell.",
                },
                "edit_mode": {
                    "type": "string",
                    "description": "Operation to perform: 'replace', 'insert', or 'delete'.",
                    "enum": ["replace", "insert", "delete"],
                    "default": "replace",
                },
            },
            "required": ["notebook_path", "cell_number"],
            "additionalProperties": False,
        },
        handler=lambda args, _root=root: _notebook_edit_impl(args, base_path=_root),
    )


def repl_tool() -> ToolSpec:
    return ToolSpec(
        name="repl",
        description=(
            "Execute Python code in a restricted REPL environment. "
            "Supports basic arithmetic, data structures, and standard library functions. "
            "Returns stdout output and the result of the last expression."
        ),
        parameters={
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python code to execute.",
                },
            },
            "required": ["code"],
            "additionalProperties": False,
        },
        handler=_repl_impl,
    )


def ask_user_question_tool() -> ToolSpec:
    return ToolSpec(
        name="AskUserQuestion",
        description=(
            "Prompt the user for input or confirmation. "
            "Use this when you need clarification, additional information, or explicit user approval."
        ),
        parameters={
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The question to ask the user.",
                },
            },
            "required": ["question"],
            "additionalProperties": False,
        },
        handler=_ask_user_question_impl,
    )


def sleep_tool() -> ToolSpec:
    return ToolSpec(
        name="Sleep",
        description=(
            "Pause execution for a specified duration in milliseconds. "
            "Used for rate limiting, waiting for external processes, or pacing multi-step operations."
        ),
        parameters={
            "type": "object",
            "properties": {
                "duration": {
                    "type": "integer",
                    "description": "Duration to sleep in milliseconds (max 300000 = 5 minutes).",
                },
            },
            "required": ["duration"],
            "additionalProperties": False,
        },
        handler=_sleep_impl,
    )


# =============================================================================
# build_advanced_tools factory
# =============================================================================

def build_advanced_tools(
    *,
    base_path: str = ".",
    include_builtins: bool = True,
    allow_write: bool = False,
    allow_bash: bool = False,
    allow_repl: bool = False,
    allow_ask: bool = False,
    allow_notebook: bool = False,
) -> list[ToolSpec]:
    """Build an advanced toolset with all new tools."""

    root = Path(base_path).expanduser().absolute()

    tools: list[ToolSpec] = [
        # File operations (advanced naming)
        file_read_tool(base_path=root),
        file_edit_tool(base_path=root),
        file_write_tool(base_path=root),
        glob_tool(base_path=root),
        grep_tool(base_path=root),
        # Legacy file operations (for backward compat in same toolset)
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
                '"recursive": true for recursive listing.'
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
            description=("Search for a plain-text pattern in files under base_path."),
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

    if allow_bash:
        tools.append(bash_tool(base_path=root))

    if allow_repl:
        tools.append(repl_tool())

    if allow_ask:
        tools.append(ask_user_question_tool())

    if allow_notebook:
        tools.append(notebook_edit_tool(base_path=root))

    tools.append(sleep_tool())

    if include_builtins:
        tools.extend([calculator_tool(), utc_now_tool()])

    return tools