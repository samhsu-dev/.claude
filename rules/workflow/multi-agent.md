# Multi-Agent Work

Hard limits of delegated work. Procedures: skill `multi-agent` for the main agent, skill `chain-session` for a chain session and a reviewer.

| Role | Scope |
|---|---|
| Main agent | Owns progress, scope and dependencies; accepts delegated results and maintains the board, records, merges, branch cleanup and user communication. |
| Resident agent | Holds one standing responsibility in a reused context (simple work, bookkeeping, one module's chain or review) and takes its queued tasks in order. |
| Chain session | Carries related routine or full-process tasks in a reused context and assigned worktree. |
| Reviewer | Checks a finished diff against the decided documents and program output. Read-only. |
| Refutation | Tries to refute a user-decidable draft in a fresh context. Read-only. |
| New reader | Reads a module's revised documents as a reader new to the repository. Read-only. |

- The main agent does a Simple task itself when briefing an agent costs more context than the work. On a project whose modules develop independently, it delegates other code and document work; on a small project, or for a change that cannot be split by module, it edits and commits directly.
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
- Only Full starts the multi-stage pipeline. A Simple or Routine task runs no design stage, refutation or independent review run.
- After each launch or resume, check the run's transcript model; relaunch a run on an older model generation than required.
- Project task and run records hold current state; retain history separately. Apply the project's configured record formats, size limits and existing checks.

## Context Economy

- Keep one resident agent per standing responsibility. Route a task to the resident that already holds its files and contracts; start a new agent only when no resident covers them.
- A brief names paths, the input revision, the write set and the change since that agent's last task. It never restates content the agent can read.
- A result returns outcome, commit, checks and open items. Detail stays in the run directory; another agent receives its path, never its text.
- A resident restarts only when its context runs out or its responsibility ends, leaving a handoff file in its run directory.
