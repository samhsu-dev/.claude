# Git Commit Standards

Guardrails active at all times. Full commit procedure: `/commit` skill.

---

## Commit Message Format

Conventional Commits 1.0.0. `type[(scope)]: description`. Imperative mood, 72-char hard limit.

## Staging

- One concept per commit.

## Cadence

- Commit each completed task before starting the next. Never defer commits until many tasks are done.
- Commit at every point the tree is runnable (compiles, tests pass) and one concept is complete — not at the end of a work session.
- A large refactor commits in stages as each runnable step lands. A working tree holding many completed tasks at once is a deferral defect: the intermediate runnable states no longer exist and cannot be reconstructed without prohibited history rewriting.
- Atomic changes (a move/rename whose halves are not independently runnable) commit as one unit. Stage them the moment that unit is complete, before further edits entangle it.

## Attribution

- No AI names, emails, or references in git author, committer, or trailer fields.
- No `Co-Authored-By`, `Signed-off-by`, or any trailer containing `Claude`, `AI`, or `Anthropic`.

## Procedure

Use `/commit` for the full staging, classification, and commit workflow.
