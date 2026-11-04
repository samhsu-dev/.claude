# Multi-Agent Work

Hard limits of delegated work. Procedures: skill `multi-agent` for the main agent, skill `chain-session` for a chain session and a reviewer.

| Role | Scope |
|---|---|
| Main agent | Owns progress, scope and dependencies; accepts delegated results and maintains the board, records, merges, branch cleanup and user communication. |
| Resident agent | Handles queued simple tasks sequentially in a reused context. |
| Chain session | Carries related routine or full-process tasks in a reused context and assigned worktree. |
| Reviewer | Checks a finished diff against the decided documents and program output. Read-only. |
| Refutation | Tries to refute a user-decidable draft in a fresh context. Read-only. |
| New reader | Reads a module's revised documents as a reader new to the repository. Read-only. |

- On a project whose modules develop independently, the main agent writes no code or document. On a small project, or for a change that cannot be split by module, it edits and commits directly.
- A write run edits only its own worktree, branch and run directory, and never merges, pushes or rebases.

## Task Modes

| Mode | Applies when | Required work |
|---|---|---|
| Simple | Inputs and expected result are explicit; no design choice or shared behavior changes | Resident agent executes, checks the result and reports briefly |
| Routine | Established contracts or bounded local design determine the result; no complex core change | Reuse the owning chain context; implement, run affected checks and let the main agent inspect the diff |
| Full | Complex work changes core semantics, architecture, termination or security contracts, or resolves a substantive conflict in those contracts | Affected design stages, implementation and independent review; refutation only for unresolved user-decidable core choices |

- Select the mode from the current unit's uncertainty and consequences. File count, first landing and a parent chain's difficulty do not trigger Full.
- Escalate only the part that meets a higher mode's criteria; retain completed work and continue independent items.
- A branch carries one independently deliverable behavior; context reuse does not combine unrelated changes.
- Running tasks have disjoint write sets.
- After each launch or resume, check the run's transcript model; relaunch a run on an older model generation than required.
- The ledger, the run registry and the board hold the current state only, each within the byte budget a zero-token check enforces; history moves to its archive when it is written.
