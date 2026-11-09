# Multi-Agent Work

Hard limits of delegated work. Roles, task modes, briefs and acceptance: skill `multi-agent` for the main agent, skill `chain-session` for a chain session and a reviewer.

- A write run edits only its own worktree, branch and run directory, and never pushes, rebases or moves another branch. Its only merge is the merge-result check of skill `chain-session` Work Loop, in a detached worktree under its run directory.
- A reviewer, refutation or new-reader run is read-only.
- Running tasks have disjoint write sets.
- The main agent keeps decisions, acceptance, integration and the user conversation; it delegates execution unless briefing costs more than the work.
- A run waits on a command by running it in the foreground or as a tracked background run whose completion notifies the waiter, never by a polling loop; `hooks/poll_guard.py` blocks an `until` or `while` loop that sleeps. Before a claim about run state, a pause record or a handoff record, the main agent checks the host's agent list and the live processes.
