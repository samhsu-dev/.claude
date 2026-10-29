# Multi-Agent Work

Hard limits of delegated work. Procedures: skill `multi-agent` for the main agent, skill `chain-session` for a chain session and a reviewer.

| Role | Scope |
|---|---|
| Main agent | Owns the board, records, merges, branch cleanup and user communication. |
| Chain session | Takes one task chain to merge-ready in its own worktree. |
| Reviewer | Checks a finished diff against the decided documents and program output. Read-only. |
| Refutation | Tries to refute a user-decidable draft in a fresh context. Read-only. |
| New reader | Reads a module's revised documents as a reader new to the repository. Read-only. |

- On a project whose modules develop independently, the main agent writes no code or document. On a small project, or for a change that cannot be split by module, it edits and commits directly.
- A write run edits only its own worktree, branch and run directory, and never merges, pushes or rebases.
- A branch carries one task.
- Running tasks have disjoint write sets.
- After each launch or resume, check the run's transcript model; relaunch a run on an older model generation than required.
- The ledger, the run registry and the board hold the current state only, each within the byte budget a zero-token check enforces; history moves to its archive when it is written.
