---
name: commit
description: Stage and commit current changes following Conventional Commits and multi-agent git safety rules. Use when the user asks to commit.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
argument-hint: "[optional scope or message hint]"
---

Commit all pending changes in the current session, following every rule below exactly.

## Step 1 — Gather Context

Run these three commands in parallel:

1. `git status` — list all modified, staged, and untracked files.
2. `git diff` and `git diff --cached` — see staged + unstaged changes.
3. `git log --oneline -10` — recent commit messages for style reference.

### Scope self-check (timing signal)

Before classifying, assess whether the working tree holds one task or many:

- Count the distinct concepts the changes serve, not the files. Signals of multiple concepts: changes span 3+ unrelated subdirectories/modules; the same file mixes edits belonging to different features/fixes; the change set is far larger than recent single-task commits in `git log`.
- File count is a diagnostic signal, not a rule. A cohesive refactor may touch many files (one concept); three unrelated fixes may touch three files (three concepts). High file count triggers reflection — "is this really one concept?" — never a forced split.
- When the tree clearly spans multiple unrelated concepts, warn the user before committing: state how many concepts you detect and that a large multi-concept tree usually means commits were deferred too long, so clean per-concept separation may no longer be possible. Recommend committing per task in future. Then proceed with the best grouping available.

## Step 2 — Classify Changes

Group files into **one or more logical commits** by **concept first, role second**:

1. Partition changes into concepts — one feature, fix, or refactor per concept. Use `git log`, task context, and functional clustering, not file type alone.
2. Within each concept, order commits by role:

| Order | Content |
|-------|---------|
| 1 | Types, config, build files |
| 2 | Core logic |
| 3 | Deletions, cleanup, refactoring |
| 4 | Adapters, integrations |
| 5 | Documentation |
| 6 | Tests |

Skip empty groups. If all changes belong to one concept, use one commit.

### When concepts are entangled in shared files

A single file may carry edits from multiple concepts, and `git` stages whole files. When `git add -p` cannot cleanly separate them (interdependent hunks, or splitting would leave a non-runnable intermediate commit):

- Commit the smallest cohesive unit that still leaves the codebase runnable (compiles, tests pass) — not the finest conceptual split.
- Name it for the dominant concept; list the merged concepts in the body.
- This is a fallback for an already-entangled tree. The real fix is timing: commit after each task completes, before the next task's edits touch the same files. Note this to the user when the fallback is used.

## Step 3 — Draft Each Commit

For each commit, compose a message following Conventional Commits 1.0.0:

### Subject line

Format: `type[(scope)]: description`

- Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`, `perf`, `build`, `style`.
- Scope: noun in parentheses — `fix(parser):`, `feat(auth):`.
- Imperative mood, lowercase after colon, no trailing period.
- 50 characters target. 72 characters hard limit.
- Test: "If applied, this commit will ___."
- Breaking changes: append `!` after type/scope.
- Match the repository's existing commit naming conventions when a project convention exists.

### Body (when subject alone is insufficient)

- One blank line between subject and body.
- Wrap at 72 characters.
- Explain what changed and why. Never how.
- Omit for trivial changes.

### Footers (when applicable)

- One blank line after body.
- `BREAKING CHANGE: description` for breaking changes.
- `Refs #123`, `Closes #456` for issue references.

## Step 4 — Stage and Commit

For each logical commit, in order:

1. Stage specific files by name. Never `git add -A` or `git add .`.
2. Create the commit using a HEREDOC:

```
git commit -m "$(cat <<'EOF'
type(scope): description

Optional body.

Optional-Footer: value
EOF
)"
```

3. Run `git status` after each commit to verify.

## Step 5 — Verify

After all commits:

1. `git log --oneline -N` (where N = number of new commits) — verify subjects.
2. Confirm each commit leaves the codebase in a consistent state.

## Safety Rules (multi-agent environment)

These are absolute prohibitions. No exceptions.

- Never `git add -A` or `git add .`.
- Never `git reset` (any form).
- Never `git commit --amend`.
- Never `git checkout -- <path>` or `git restore`.
- Never `git stash`.
- Never `git clean`.
- Never `git push --force` or `git push -f`.
- Never `git rebase -i`.
- Stage and commit only files that belong to the current task.
- If a file has changes from another agent's work, skip it and report to the user.

## Attribution

- No AI names, emails, or references in author, committer, or trailer fields.
- No `Co-Authored-By`, `Signed-off-by`, or any trailer containing `Claude`, `AI`, or `Anthropic`.
