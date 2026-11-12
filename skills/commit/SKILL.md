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

Commit the current task's pending changes.

## Step 1 — Gather Context

Run these three commands in parallel:

1. `git status` — list all modified, staged, and untracked files.
2. `git diff` and `git diff --cached` — see staged + unstaged changes.
3. `git log --oneline -10` — recent commit messages for style reference.

### Scope self-check

- Count the distinct concepts the changes serve, not the files: changes across 3 or more unrelated modules, one file mixing edits of different features or fixes, or a change set several times larger than recent single-task commits in `git log` each indicate more than one concept.
- When the tree spans more than one unrelated concept, tell the user how many concepts you detect and that `workflow/committing.md` Staging commits each task once its tree is runnable, then commit the best grouping available.
- A concept touching more than 15 files, or several times the size of recent `git log` commits, is split into the Step 2 role-ordered commits, each leaving the tree runnable; it stays one commit only when atomic (Step 2), and you then tell the user why it could not be split.

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

Skip empty groups. A single concept splits into multiple role-ordered commits when each layer lands the tree runnable; collapse to one commit only when the change is atomic — a move/rename or interlocking edit whose halves are not independently runnable.

### When concepts are entangled in shared files

When `git add -p` cannot cleanly separate them (interdependent hunks, or splitting would leave a non-runnable intermediate commit):

- Commit the smallest cohesive unit that still leaves the codebase runnable (compiles, tests pass) — not the finest conceptual split.
- Name it for the dominant concept; list the merged concepts in the body.
- Tell the user when this fallback is used.

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
- Body: `workflow/committing.md` Commit Message Format; never how.

### Footers (when applicable)

- One blank line after body.
- `BREAKING CHANGE: description` for breaking changes.
- `Refs #123`, `Closes #456` for issue references.

## Step 4 — Stage and Commit

For each logical commit, in order:

1. Stage specific files by name.
2. Create the commit using a HEREDOC:

```text
git commit -m "$(cat <<'EOF'
type(scope): description

Optional body.

Optional-Footer: value
EOF
)"
```

1. Run `git status` after each commit to verify.

## Step 5 — Verify

After all commits:

1. `git log --oneline -N` (where N = number of new commits) — verify subjects.
2. Confirm each commit leaves the codebase in a consistent state.

## Safety Rules (multi-agent environment)

- Prohibited git operations: `hooks/git_guard.py` blocks them and names the safe alternative (`workflow/git-safety.md`). The commit-msg hook of `tools/git-hooks/` checks the message.
- No push. A push follows `workflow/git-safety.md` Publication.
- Stage and commit only files that belong to the current task.
- Before staging, run `git status`; a file holding another agent's uncommitted changes is skipped and reported to the user.
- Attribution: `workflow/committing.md` Attribution.
