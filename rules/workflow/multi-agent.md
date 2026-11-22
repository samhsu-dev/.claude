# Multi-Agent Work

Hard limits of delegated work. Roles, task modes, briefs and acceptance: skill `multi-agent` for the main agent, skill `chain-session` for a chain session and a reviewer.

- A write run edits only its own worktree, branch and run directory and moves only its own branch, with no push and no rebase; the main agent publishes. Its merges are the merge-result check of skill `chain-session` Work Loop, in a detached worktree under its run directory, and, when that check meets a conflict, the merge of `integration.branch` into its own branch that resolves the conflict under `workflow/git-safety.md`.
- A reviewer, refutation or new-reader run is read-only outside its run directory.
- Running tasks have disjoint write sets, compared under skill `multi-agent` Dispatch.
- The main agent keeps dispatch, decisions, acceptance disposition, integration and the user conversation, and assigns execution and record writes to the roles the project `execution` values set, unless briefing costs more than the work.
- Every agent leaves unchanged the processes, directories, branches and worktrees `execution.foreign_work` lists.
- A run waits on a command by running it in the foreground or as a tracked background run whose completion notifies the waiter; `hooks/poll_guard.py` blocks an `until` or `while` loop that sleeps. A wait starts only the awaited command, with no `tail -f`, `tail -F` or second waiting command. Before a claim about run state, a pause record or a handoff record, the main agent checks the agent list and live processes of each host `execution.hosts` lists, by its status command.
