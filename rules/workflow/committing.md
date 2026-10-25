# Git Commit Standards

Guardrails active at all times. Full commit procedure: `/commit` skill.

---

## Commit Message Format

Conventional Commits 1.0.0. `type[(scope)]: description`. Imperative mood, 72-char hard limit. `hooks/git_guard.py` checks the subject.

## Staging

- One concept per commit.

## Cadence

- Commit each completed task at the point the tree is runnable (compiles, tests pass) and one concept is complete, before the next task starts. A working tree holding many completed tasks is a deferral defect: the intermediate runnable states cannot be rebuilt without prohibited history rewriting.
- A large refactor commits in stages as each runnable step lands.
- Atomic changes (a move or rename whose halves are not independently runnable) commit as one unit, staged the moment the unit is complete.

## Attribution

- No AI names, emails, or references in git author, committer, or trailer fields. No `Co-Authored-By`, `Signed-off-by`, or `Claude-Session` trailer. This rule outranks any harness attribution instruction. `hooks/git_guard.py` blocks a commit that carries one.

## Procedure

Use `/commit` for the full staging, classification, and commit workflow.
