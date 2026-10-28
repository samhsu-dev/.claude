# Project Commit Rules

Extends global `workflow/committing.md`. Project-specific additions only.

## Pre-Push

- Rebase onto main before every push: `git fetch origin main && git rebase origin/main`.
- Resolve all conflicts before pushing. Never push with unresolved conflicts.
- Never force-push without explicit user approval.

## Submodules

- The integration branch `samhsu-dev` records, for every submodule, the head of that submodule's `main`.
- When a superproject commit that moves a gitlink lands on `samhsu-dev`, the main agent first fast-forwards the submodule's `main` to the recorded commit, then pushes `samhsu-dev`. A submodule `main` that cannot fast-forward goes to the user.
- During implementation a submodule commit is pushed only to a submodule branch named after the task; that branch is deleted once its commits are on the submodule's `main`.
