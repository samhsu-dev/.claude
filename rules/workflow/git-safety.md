# Git Safety — Multi-Agent Environment

Preflight and safe alternatives: skill `commit`; branch cleanup and submodule pointers: skill `multi-agent` Branch Lifecycle.

## Prohibited Operations

- `hooks/git_guard.py` blocks the git operations that discard, hide or rewrite work, stage files not named one by one, or skip the Git hooks, and names the safe alternative.

## Publication

- Push only with explicit user authorization or within the scope an `integration.publication` value states; these two are the only authorization of a push.

## Branches and Conflicts

- Name each agent-created task branch by `integration.task_branch_pattern` when it is configured, and every other agent-created branch with the prefix `samhsu/`.
- Create, rename and publish branches outside the `codex/` namespace.
- Switch the branch of a checkout only on explicit user instruction; a run's merge-result check uses a new detached worktree under its run directory.
- Delete a branch only on explicit user instruction with `git branch -d`, or under skill `multi-agent` Branch Lifecycle; `git branch -D` deletes only a branch that Branch Lifecycle archived.
- Keep conflicting changes and another writer's uncommitted work: the main agent reads and archives such work under skill `multi-agent` Branch Lifecycle before it removes the worktree.
- A conflict from merging the integration head into a task branch is resolved by that task's run from the decided documents and measured test output, with each side checked; the main agent checks the resolution diff before integration. A conflict whose sides implement contradictory decided sentences goes to the user.
- Send other pull or rebase conflicts to the user for resolution; an agent resolves only the submodule pointers skill `multi-agent` Branch Lifecycle permits.
- Run `git rebase --abort` or `git merge --abort` only with explicit user approval.
