# Git Safety — Multi-Agent Environment

Multiple agents work concurrently on the same repository. The working tree is shared state.

---

## Prohibited Operations

- Never `git reset`, `checkout --`/`.`/`-f`, `restore`, `clean`, `stash`, `push --force`/`-f`/`--force-with-lease`, `branch -D`, `rebase -i`, `commit --amend`, `add -A`/`.`. `hooks/git_guard.py` blocks each one; a block is never worked around.

## Safe Alternatives

| Destructive | Safe alternative |
|-------------|-----------------|
| `git reset --hard` | Create a new revert commit |
| `git checkout -- file` | `git diff file` to inspect, then edit manually |
| `git commit --amend` | Create a new fixup commit |
| `git push --force` | `git push` (fail = investigate, never force) |
| `git branch -D` | See Branch Operations for deletion permission |
| `git stash` | Commit WIP to a temporary branch |
| `git clean` | Remove known files by name with `rm` |

## Before Any Git Write Operation

1. `git status` — verify working tree state.
2. Verify no other agent has uncommitted changes in the same files.
3. For staging, add specific files by name. Other Git writes do not stage files.

## Branch Operations

- Never switch branches without explicit user instruction.
- Delete a branch only on explicit user instruction, using `git branch -d`; it refuses to delete unmerged branches. Exception: right after a task branch's fast-forward and full gate, the main agent removes its worktree and deletes the branch with `git branch -d` from the integration checkout, only when tracked, untracked and ignored files and every submodule are clean or disposable build output.

## Conflict Resolution

- Never silently discard conflicting changes.
- Pull or rebase conflicts go to the user. Never auto-resolve.
- Exception: the main agent may set rebased submodule pointers for the same implementation step when those commits were rebased onto the integration head's recorded commits and `git range-diff` proves the patches identical.
- `git rebase --abort` or `git merge --abort`: requires explicit user approval.
