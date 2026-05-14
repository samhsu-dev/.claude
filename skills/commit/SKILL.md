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

## Step 2 — Classify Changes

Group files into **one or more logical commits**, each covering one concept:

| Commit order | Content |
|--------------|---------|
| 1 | Types, config, build files |
| 2 | Core logic |
| 3 | Deletions, cleanup, refactoring |
| 4 | Adapters, integrations |
| 5 | Documentation |
| 6 | Tests |

Skip empty groups. If all changes belong to one concept, use one commit.

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
