# Git Safety — Multi-Agent Environment

Preflight and safe alternatives: skill `commit`; branch cleanup and submodule pointers: skill `multi-agent` Branch Lifecycle.

## Prohibited Operations

- `hooks/git_guard.py` blocks the git operations that discard, hide or rewrite work, stage files not named one by one, or skip the Git hooks, and names the safe alternative; a block is never worked around.

## Publication

- A push requires explicit user authorization; an `integration.publication` value is that authorization within the scope it states. A local commit, passed review or merge does not authorize publication.

## Branches and Conflicts

- No agent switches the branch of any checkout without explicit user instruction; a run's merge-result check uses a new detached worktree under its run directory.
- Delete a branch only on explicit user instruction with `git branch -d`, or under skill `multi-agent` Branch Lifecycle; `git branch -D` deletes only a branch that Branch Lifecycle archived.
- Never discard conflicting changes or another writer's uncommitted work; the main agent archives such work under skill `multi-agent` Branch Lifecycle before it removes the worktree.
- A conflict from merging the integration head into a task branch is resolved by that task's run from the decided documents and measured test output, never by taking one side unchecked; the main agent checks the resolution diff before integration. A conflict whose sides implement contradictory decided sentences goes to the user.
- Other pull or rebase conflicts go to the user. Never auto-resolve them, except the submodule pointers skill `multi-agent` Branch Lifecycle permits.
- `git rebase --abort` or `git merge --abort`: requires explicit user approval.
