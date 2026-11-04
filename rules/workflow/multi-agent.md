# Multi-Agent Work

Hard limits of delegated work. Roles, task modes, briefs and acceptance: skill `multi-agent` for the main agent, skill `chain-session` for a chain session and a reviewer.

- A write run edits only its own worktree, branch and run directory, and never merges, pushes or rebases.
- A reviewer, refutation or new-reader run is read-only.
- Running tasks have disjoint write sets.
- The main agent keeps decisions, acceptance, integration and the user conversation; it delegates execution unless briefing costs more than the work.
