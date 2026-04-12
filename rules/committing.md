# Project Commit Rules

Extends global `committing.md`. No duplication -- project-specific additions only.

## Pre-Push

- Rebase onto main before every push: `git fetch origin main && git rebase origin/main`.
- Resolve all conflicts before pushing. Never push with unresolved conflicts.
- Never force-push without explicit user approval.
