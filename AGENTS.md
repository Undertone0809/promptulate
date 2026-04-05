# Repository Guidelines

## Documentation

- Use `README.md` for the project overview.
- For use cases, keep one folder per use case, put a `README.md` in each folder, and leave `use_cases/README.md` empty for now.

## Git commit rules

- After completing a feature, small functionality, test change, or bug fix, and after the necessary validation passes, default to running `git commit` and `git push` to the current remote branch.
- Continue using the repository's Conventional Commit format for commit messages (for example `feat:`, `fix:`, `test:`).
- If there are unrelated dirty changes in the working tree, default to committing only the files changed for the current task instead of asking for confirmation.
- Exception: if the user explicitly asks not to commit/push, or the commit scope is ambiguous / conflict risk is high, stop and confirm before committing or pushing.
