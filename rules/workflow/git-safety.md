# Git Safety — Multi-Agent Environment

Multiple agents work concurrently on the same repository. The working tree is shared state. Preflight and safe alternatives: skill `commit`; branch cleanup and submodule pointers: skill `multi-agent` Branch Lifecycle.

## Prohibited Operations

- Never `git reset`, `checkout --`/`.`/`-f`, `restore`, `clean`, `stash`, `push --force`/`-f`/`--force-with-lease`, `branch -D`, `rebase -i`, `commit --amend`, `add -A`/`.`. `hooks/git_guard.py` blocks each one; a block is never worked around.

## Publication

- A push requires explicit user authorization and follows configured project publication constraints. A local commit, passed review or merge does not authorize publication.

## Branches and Conflicts

- Never switch branches without explicit user instruction.
- Delete a branch only on explicit user instruction with `git branch -d`, or under skill `multi-agent` Branch Lifecycle.
- Never silently discard conflicting changes or another writer's uncommitted work.
- Pull or rebase conflicts go to the user. Never auto-resolve, except the submodule pointers skill `multi-agent` Branch Lifecycle permits.
- `git rebase --abort` or `git merge --abort`: requires explicit user approval.
