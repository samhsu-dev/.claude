# Git Safety — Multi-Agent Environment

Multiple agents work concurrently on the same repository. The working tree is shared state.

---

## Prohibited Operations

Never run these commands. They destroy commits, discard changes, or rewrite history other agents depend on.

- `git reset` — any form (`--hard`, `--soft`, `--mixed`). Moves HEAD, losing commits other agents reference.
- `git checkout -- <path>` / `git checkout .` — discards uncommitted changes other agents made.
- `git checkout -f` — force-switches branch, discarding local changes.
- `git restore` — discards working tree or staged changes.
- `git clean` — deletes untracked files another agent may have created.
- `git stash` — hides changes from other agents. Stash is per-repo, not per-agent.
- `git push --force` / `git push -f` / `git push --force-with-lease` — rewrites remote history.
- `git branch -D` — force-deletes branch with unmerged commits.
- `git rebase -i` / `git rebase --interactive` — can drop or squash commits silently.
- `git commit --amend` — rewrites the last commit another agent may already reference.

## Safe Alternatives

| Destructive | Safe alternative |
|-------------|-----------------|
| `git reset --hard` | Create a new revert commit |
| `git checkout -- file` | `git diff file` to inspect, then edit manually |
| `git commit --amend` | Create a new fixup commit |
| `git push --force` | `git push` (fail = investigate, never force) |
| `git branch -D` | `git branch -d` (refuses if unmerged) |
| `git stash` | Commit WIP to a temporary branch |
| `git clean` | Remove known files by name with `rm` |

## Before Any Git Write Operation

1. `git status` — verify working tree state.
2. Stage specific files by name. Never `git add -A` or `git add .`.
3. Verify no other agent has uncommitted changes in the same files.

## Branch Operations

- Never switch branches without explicit user instruction.
- Never delete branches without explicit user instruction.
- `git branch -d` (lowercase) is acceptable — it refuses to delete unmerged branches.

## Conflict Resolution

- Never silently discard conflicting changes.
- `git pull` or `git rebase` conflicts: report to user. No auto-resolve.
- `git rebase --abort` or `git merge --abort`: requires explicit user approval.
