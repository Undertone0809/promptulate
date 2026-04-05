# Repository Guidelines

## Documentation

- Use `README.md` for the project overview.
- For use cases, keep one folder per use case, put a `README.md` in each folder, and leave `use_cases/README.md` empty for now.

## SDK Boundaries

- Keep `pne/` import-only and side-effect free.
- Do not make SDK code discover repository files, load `.env`, mutate process environment, or infer runtime configuration from the current working directory.
- Keep environment loading, CLI parsing, and other app bootstrap logic in `use_cases/` or in the caller.
- When a behavior depends on local machine state, make it explicit in the example or entrypoint so the SDK surface stays predictable and embeddable.
- Why: SDKs are reused in notebooks, services, tests, and other host applications, so hidden bootstrap logic makes behavior depend on cwd, checkout layout, or local files instead of explicit caller input.
- Why: implicit file loading and env mutation blur the boundary between library and application, which makes debugging, composition, and security review harder.
- Why: examples can be opinionated and convenience-driven, but the package API itself should stay deterministic, portable, and easy to embed in larger systems.

## Testing policy

- All public SDK behaviors must have mock unit tests in this repository.
- For adapter/provider behavior, always use mocks for:
  - `openai` / `anthropic` imports,
  - shell command execution,
  - backend detection (`importlib` and `shutil.which`).
- Tests must not touch the network and should avoid real command execution.
- Preferred command:

```bash
python -m unittest
```

## Git commit rules

- After completing a feature, small functionality, test change, or bug fix, and after the necessary validation passes, default to running `git commit` and `git push` to the current remote branch.
- Continue using the repository's Conventional Commit format for commit messages (for example `feat:`, `fix:`, `test:`).
- If there are unrelated dirty changes in the working tree, default to committing only the files changed for the current task instead of asking for confirmation.
- Exception: if the user explicitly asks not to commit/push, or the commit scope is ambiguous / conflict risk is high, stop and confirm before committing or pushing.
