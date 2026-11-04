# Git Safety — Multi-Agent Environment

Multiple agents work concurrently on the same repository. The working tree is shared state. Preflight and safe alternatives: skill `commit`; branch cleanup and submodule pointers: skill `multi-agent` Branch Lifecycle.

## Prohibited Operations

- `hooks/git_guard.py` blocks the operations that discard work, rewrite history or skip the Git hooks, and names the safe alternative; a block is never worked around.

## Publication

- A push requires explicit user authorization and follows configured project publication constraints. A local commit, passed review or merge does not authorize publication.

## Branches and Conflicts

- Never switch branches without explicit user instruction.
- Delete a branch only on explicit user instruction with `git branch -d`, or under skill `multi-agent` Branch Lifecycle.
- Never silently discard conflicting changes or another writer's uncommitted work.
- Pull or rebase conflicts go to the user. Never auto-resolve, except the submodule pointers skill `multi-agent` Branch Lifecycle permits.
- `git rebase --abort` or `git merge --abort`: requires explicit user approval.
