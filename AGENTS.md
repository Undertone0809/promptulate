# Repository Guidelines

## Project Structure & Module Organization

This repository is a small monorepo centered on Python packages in `libs/`:

- `libs/pne/`: main framework package (`pne/`) with the most complete tests and CI coverage.
- `libs/client/`: client package (`pne_client/`).
- `libs/experimental/`: experimental package (`pne_experimental/`).
- `docs/`: VitePress documentation site.
- `example_bak/`, `promptulate_bak/`, `tests_bak/`: legacy or reference material; avoid adding new production code there.

Prefer package-local changes and tests. For example, changes to the core framework should usually touch `libs/pne/pne/` and `libs/pne/tests/`.

## Build, Test, and Development Commands

- `make lint`: run root Ruff checks for `libs/`.
- `make format`: format Python code in `libs/`.
- `cd libs/pne && make install`: install core package dependencies.
- `cd libs/pne && make test`: run pytest with coverage for `libs/pne/tests/basic`.
- `cd libs/pne && make lint`: run style checks plus tests for the core package.

More commands see Makefile and confia file.

## Coding Style & Naming Conventions

Target Python `>=3.9`. Use 4-space indentation, double quotes, and a maximum line length of 88. Ruff is the source of truth for formatting and import ordering; run it before submitting changes.

Follow existing naming patterns:

- modules/packages: lowercase with underscores
- test files: `test_*.py`
- keep public package code inside each package directory (`pne/`, `pne_client/`, `pne_experimental/`)

## Testing Guidelines

Pytest is the active test framework. Add tests beside the package you changed, not in root-level placeholder tests unless you are updating root tooling. For core changes, add coverage in `libs/pne/tests/basic/`. Coverage is configured with a `fail_under = 50` threshold, so new work should not reduce it.

## Commit & Pull Request Guidelines

Recent history uses Conventional Commit-style prefixes such as `feat:`, `refactor:`, and `chore:`. Keep commits scoped to one package or concern when possible.

PRs should include:

- a short summary of the change
- the affected package(s) or docs area
- commands you ran (`make lint`, `cd libs/pne && make test`, etc.)
- linked issues when relevant
- screenshots for documentation or UI-facing doc changes

## Security & Configuration Tips

Do not commit secrets or API keys. Keep runtime credentials in environment variables such as `OPENAI_API_KEY` or `TAVILY_API_KEY`, matching the examples in `README.md`.

## Git commit rules

- After completing a feature, small functionality, test change, or bug fix, and after the necessary validation passes, default to running `git commit` and `git push` to the current remote branch.
- Continue using the repository's Conventional Commit format for commit messages (for example `feat:`, `fix:`, `test:`).
- If there are unrelated dirty changes in the working tree, default to committing only the files changed for the current task instead of asking for confirmation.
- Exception: if the user explicitly asks not to commit/push, or the commit scope is ambiguous / conflict risk is high, stop and confirm before committing or pushing.