---
name: multi-agent
description: Coordinate delegated runs as the main agent. Use before dispatching, briefing or resuming a run, choosing a review, merging a branch, after a module's documents are revised, at consolidation, or after compaction.
---

Coordinate delegated work as the main agent. Hard limits: `rules/workflow/multi-agent.md`. Parameters `integration` and `execution` come from the project rule files `integration.md` and `execution.md` under `rules/project/`, and `algorithm.core_principles` from `decisions.md`; read those three files before the first dispatch.

## Roles

| Role | Scope |
|---|---|
| Main agent | Manages: sets outcomes and priorities, dispatches, decides, accepts results, integrates and talks with the user. Delegates execution and record upkeep. |
| Resident agent | Holds one standing responsibility in a reused context (simple work, bookkeeping, one module's chain or review) and takes its queued tasks in order. |
| Chain session | Carries related routine or full-process tasks in a reused context and assigned worktree. |
| Reviewer | Checks a finished diff against the decided documents and program output. Read-only. |
| Refutation | Tries to refute a user-decidable draft in a fresh context. Read-only. |
| New reader | Reads a module's revised documents as a reader new to the repository. Read-only. |

## Task Modes

| Mode | Applies when | Required work |
|---|---|---|
| Simple | Inputs and expected result are explicit; no design choice or shared behavior changes | Resident agent executes, checks the result and reports briefly |
| Routine | Established contracts or bounded local design determine the result; no complex core change | Reuse the owning chain context; implement, run affected checks and let the main agent inspect the diff |
| Full | Complex work changes core semantics, architecture, termination or security contracts, or resolves a substantive conflict in those contracts | Affected design stages, implementation and independent review; refutation only for unresolved user-decidable core choices |

- Select the mode from the current unit's uncertainty and consequences. File count, first landing and a parent chain's difficulty do not trigger Full.
- Escalate only the part that meets a higher mode's criteria; retain completed work and continue independent items.
- A branch carries one independently deliverable behavior; context reuse does not combine unrelated changes.
- Only Full starts the multi-stage pipeline. A Simple or Routine task runs no design stage, refutation or independent review run.
- After each launch or resume, check the run's transcript model; relaunch a run on an older model generation than required.
- Project task and run records hold current state; retain history separately. Apply the project's configured record formats, size limits and existing checks.

## Main Agent

- The main agent keeps decisions and delegates execution. Code, documents, investigation, evidence gathering, record edits and worktree cleanup go to residents. Exceptions: it does a Simple task itself when briefing an agent costs more context than the work, and it edits and commits directly on a small project or for a change that cannot be split by module.
- It accepts a result from the resident's report and the evidence the report names (commit, check output, diff stat). It reads a diff hunk, file or log excerpt when the report leaves a material doubt, when the task mode requires a diff check, or to verify launch metadata; it never re-reads a full transcript.
- It never repeats an investigation a resident reported; a gap goes back to that resident as a question.
- It answers boundary questions, decides agent-decidable items and batches user-decidable items into one question to the user.
- It reports to the user the state of each running task in one line, the decisions waiting for the user, and each risk or failed check that changes what the user would do.

## Context Economy

- Keep one resident agent per standing responsibility while its context stays useful. Route a task to the resident that already holds its files and contracts; start a new agent only when no resident covers them or the handoff costs less than the stale context.
- A brief states the purpose, the outcome as an independently deliverable result, acceptance checks, the tool and write boundaries, the effort level, dependencies, input revision and the change since that agent's last task. It references readable content by path and section and inlines only the decided sentences and changes needed to interpret the task.
- A result returns outcome, commit, checks and open items. Detail stays in the run directory; another agent receives its path, never its text.
- A resident restarts only when its context runs out or its responsibility ends, leaving a handoff file in its run directory.

## Dispatch

1. Select Simple, Routine or Full under Task Modes above. Do a Simple task directly when briefing costs more than the work; route other work to the resident that holds its context. Before a new launch, compare open tasks and questions for shared inputs, write sets and root causes. Merge rows sharing a root cause and acceptance goal into one independently deliverable row, preserving every acceptance item; order a row that needs another's result after it; record the choice with its reason.
2. Parallelize across independent tasks, never across the stages of one task. The stages of one task share context and the implicit decisions in its actions; every handoff between them loses detail.
3. Keep one agent loop. A separate run is justified only by one of:
   1. an independent review or refutation, which needs a fresh context;
   2. a task with fixed inputs whose write set is disjoint from every running task's;
   3. context the main agent must not hold, whose result fits a one-screen summary.
4. Give a change that requires seeing several files at once — deduplication, conflict resolution, a cross-file rename, a corpus-wide edit — to one run, never split across runs.
5. Size tasks as independently checkable results. Reuse established context and evidence; context compaction alone creates no new task or agent.
6. Launch a task beside others only when its board row records each check:
   1. Every user-decidable decision it implements is recorded.
   2. Its write set, stated at module level, is disjoint from every running task's write set.
   3. Every contract it consumes is merged into `integration.branch`.
   4. Its result is checkable by the checks required for its task mode.
7. Hold a task that fails a check, or add it to the chain that owns its files. Launch a task that passes the checks of step 6 when its expected speed or quality gain exceeds its coordination cost and the configured concurrency, token, compute and spending limits admit it; otherwise queue it.
   - Whenever a run ends or a branch merges, recheck every held row against the current diffs, not against its recorded hold reason. A shared document whose two edits touch disjoint sections does not block; a hold whose cause is gone is released.
   - While a task waits, its read-only preparation — an inventory, a brief, a site list — runs ahead.
8. Apply `workflow/change-policy.md` Outcome and Scope before dispatch. A Simple request supplies inputs, allowed edits and a completion check in a short message. For Routine or Full, write the brief under Context Economy above, adding the project root, the glossary path (`communication/terminology.md` Established Terms), exclusions, protected files and return format. The protected files are the files another running task writes, computed at launch.
9. Quote in the brief, with path and line, every decided document sentence the task implements; never paraphrase a rule.
   - Name a related decision only by its ID and landing path:line; never copy decision-log content into a brief. The decision log is read only to trace why a rule holds or to prepare a new decision, by the main agent or under skill `decisions`.
   - Check the implemented decisions against entries governing the same affected contract. Reuse established evidence; contradictory requirements for one input go to the user before dependent work starts.
   - Update owning text when its meaning changes. Independent specification review applies to Full; an unchanged approved specification is reused.
10. Write the run registry row before launch: handle, task, model and effort, branch, progress file, status and next action.
11. Launch through the host's agent tool or a tracked background command. Retain its handle for follow-up and completion notifications. No worker exists only to wrap another run, and no model turn polls for unchanged status.
12. Give a research run that lacks a tool the exported source material.

## Boundary Questions

- Answer a chain session's question in that same session, by resume or message; never stop and relaunch it.
- Widen the write set only for a prerequisite of the accepted result, within existing authorization and with no concurrent writer; otherwise keep the item separate or order it after its dependency.
- Take a user-decidable question to the user under skill `decisions`.

## Chains

- Keep the residents of Context Economy above: one for simple work and bookkeeping, one chain per related set of files, contracts or mechanisms, one reviewer per module under review. Queue tasks within each resident sequentially; every request names its current input revision and permitted write set.
- After a merge, resume the chain session for the chain's next task; its brief carries the integration diff since its last commit.
- Before compaction or a context replacement, a session writes to its progress record the current revision, task, constraints, decisions, affected contracts, completed checks, open failures and next action; afterwards it reloads that record and verifies it against the repository before continuing. A resident's context is replaced only under Context Economy above.

## Review

Pick the check before each review round from what the pending diff changes:

Task Modes determines review depth. A configured project review trigger may specialize checks within Full; required correctness and integration checks still apply.

| Task mode | Check |
|---|---|
| Simple | Resident verifies the requested result; main agent checks the returned evidence |
| Routine | Implementer checks affected behavior; main agent inspects the diff and evidence; an unresolved correctness or security risk escalates that part to Full |
| Full | One independent review against accepted contracts and behavioral evidence; fixes within unchanged contracts take reproduction, applicable gate and main-agent diff checks |

- Every mode retains required repository and integration checks. Reuse checks for the same revision; rerun affected checks after changes or new failures.
- A review runs at `execution.review.<difficulty>` of its board row. Exception: the first full review of a change to a semantic sentence of an `algorithm.core_principles` entry runs at `execution.background.max_effort`.
- An S1 finding that a later review or run finds and an earlier review of the same module missed raises that module's review effort one entry of `execution.review.levels` for its next tasks, up to the last entry. The ledger records the module's raised level.
- The reviewer brief names the Review Checklist of skill `chain-session`, which defines the severities and real inputs; its acceptance criteria list only the task's real inputs.
- After each FIX-FIRST and before the fix round, record on the board row one line per finding: the task goal it serves and the real output it changes. A finding without that line gets no fix round; it becomes its own row or is dropped.
- A second FIX-FIRST on the same component, or a fix that needs a new dependency, parser or module, stops the chain until the main agent restates the task's scope.
- A branch takes at most two full reviews. After that only an S1 finding the diff introduces, shown by program output or a decided sentence, blocks its merge, and it closes through the main agent's reproduction, gate and diff checks.
- A second introduced S1 after the full reviews stops the branch: the item goes to the user with its evidence instead of another fix round.
- A finding outside the write set follows the deferred-finding classification below. A demonstrated regression of the accepted result remains blocking until a scoped repair or independently correct split removes it.
- Route deferred findings by the project's acceptance criteria. A finding that shares an open task's cause joins that task; an unrelated improvement does not block the accepted result.

## Branch Lifecycle

- Cut each worktree and branch from the `integration.branch` head, with every submodule at the commit that head records, outside the repository folder, since an editor opened on the repository indexes the whole folder.
- A finished part whose gate and review pass merges that day; a part that waits on a decision or another row splits into its own row and never holds the finished part.
- When `integration.branch_lifetime` is configured, size tasks to fit it. Branch age counts from creation, waiting included. A branch that reaches the limit consolidates at once: its independently correct finished work merges after the required checks, the rest splits into bounded rows, or the ledger records why no safe finished slice exists. A split row is ordered after the merge of the branch's finished part, never as its prerequisite, unless that part alone adds a defect no row owns.
- A replacement of one implementation by another lands in the integration branch in steps behind one switch whose default keeps the old implementation (branch by abstraction); no task branch holds the switch or the replacement's fixes past `integration.branch_lifetime`. The default flips in its own change once the comparison below shows no difference, or the user decides each remaining one; the next row removes the old implementation.
- While both implementations exist, the full gate runs both on the project's evaluation inputs and compares their outputs (parallel run). Each difference is owned by an open row; a difference no row owns stops integration until a row owns it.
- The project's record check reports each unmerged task branch past `integration.branch_lifetime`; every status pass consolidates the reported branches.
- Name a branch by `integration.task_branch_pattern`; its `branch.<name>.description` holds the task ID, the goal and the session handle.
- After an interruption, commit the run's work in progress on its branch.
- Only the main agent publishes, under `workflow/git-safety.md` Publication and configured project policy. When publication is authorized, publish task submodule commits to the configured task branch; at integration, fast-forward each configured submodule branch and publish it before its superproject. A failed fast-forward goes to the user.
- The main agent integrates a finished branch using the configured project integration policy and Git safety rules. After its gate and review pass, run the required integration checks. A finished-result report without the full-gate comparison of skill `chain-session` Work Loop step 7 goes back to the same session before review or merge. The integration branch moves only to a merge result whose full gate adds no failure or finding to the integration head's; a failure found after the move goes back to the session that holds the branch context. Publication follows `workflow/git-safety.md`; never resolve conflicts or publish without the required authorization.
- After the full gate, remove the worktree once its tracked, untracked and ignored files and every submodule are clean or disposable build output, then delete the task branch with `git branch -d` from the integration checkout. A task-named submodule branch goes only after its commits reach `integration.submodule_branch`.
- Rebased submodule pointers for the same implementation step may be set without the user when those commits were rebased onto the integration head's recorded commits and `git range-diff` proves the patches identical.
- After every merge, reconcile branches absent from the open board line by line against integration; recover or explain missing content. A rejected implementation's branch stays only while a board row names it as reference.

## Records

- The run ledger holds the verbatim question, numbered user directives, chains, gate order, versioned inputs, dependencies and next steps, one short line per row; full directive text lives in its archive. Proposed, applied, committed and independently verified stay distinct states.
- The board lists every open task with its write set, dependencies, chain, branch, difficulty and the checks. A split or consolidation moves every acceptance item and dependency to the row that keeps it and removes the covered rows in the same update.
- A run result that changes rows is applied per item: each verdict lands as a board edit in one update, or as a row that names the items still to apply. The run registry records the result as applied only when no item remains; a result file never holds a board change the board lacks.
- Update the run registry row on every notification.
- A board dependency names the file or contract the row consumes from that row; an entry with neither is dropped.
- Record edits that follow a fixed procedure (post-merge archiving, status cells, ledger lines) go to one resident bookkeeper run on `execution.implementer.mechanical`, one request per batch; the main agent keeps the decisions and reads only its reply.
- After context compaction, reread the run registry, then the ledger, then the board, before acting; they take precedence over the compacted summary.
- Read only run summaries. Missing evidence comes from a follow-up turn of the session that holds the context, never from re-deriving the analysis.
- A script computes per task, from git and the run logs: runs launched, resumptions, fix and review rounds, model and effort, `execution.token_measure` split into uncached input, cached input, output and reasoning without double counting, billed cost, wall time and the accepted outcome.
- A process change alters one thing at a time and is judged against these numbers on comparable tasks.
- When `integration.progress_snapshot` is configured, the bookkeeper appends its row on that schedule and records the close date on each row it archives as done; a completion-date estimate reads those rows, not the archive alone.
- When the user requests a retrospective or a configured project schedule calls for one, use the recorded evidence to identify a process problem and evaluate a scoped change. No default recurring task is created.

## Consolidation

- Consolidate when requested or required by a configured project schedule or integration step. List rows that share a cause or write set, duplicates, stale statuses and ready branches; apply only authorized merges and record state changes.
- When consolidation is required, split a row that combines independently deliverable behavior; a branch past its lifetime follows Branch Lifecycle. Preserve each acceptance item and dependency with the part that owns it.
- For a blocking row, identify the contract, file or decided sentence each dependent consumes and the smallest independently correct delivery that provides it. Replace whole-row waits with that delivery when write sets are disjoint; remove an edge only after its contract is delivered.
- After a task completes or a result integrates, lightly recheck affected rows for a shared cause, satisfied dependency, smaller delivery and newly available disjoint work. The periodic pass covers the whole board.
- A row that implements a decided sentence closes only into a row that implements the same sentence.

## Model Routing

| Run | Model and effort |
|---|---|
| Main agent | Session model |
| Chain session | `execution.implementer.<difficulty>` of the chain's hardest task |
| Reviewer | Review above |
| Research, analysis | `execution.background` at `max_effort` |
| Refutation, count run, new reader | `execution.background` at `high_effort` |

## Run Isolation

- Run directories live in persistent scratch storage outside temporary directories. Each board task has one working directory there, named by its task ID, with one subdirectory per run; it moves to the run storage archive when the row closes.
- A read-only run's working directory and sandbox are its own run directory, never the target tree. A write run works in its own worktree.
- `tools/codex_rules.py pack` writes the rule-reading instructions into the run directory, routing each project value file under `<repository>/.codex/rules/project/` by its `paths:` frontmatter, and the project glossary path; `--lean` briefs a chain session and adds skill `chain-session` as a required read. Findings count only after the log shows those reads; `gate` checks always-active path mentions, so scoped reads still need inspection.
- Each run persists its result and returns a summary of at most one screen with evidence, limits and next step. A failed or missing result blocks dependent work; the ledger records the remaining work before a batch closes.

## Reader Review

- For a Full task with a substantial document revision, or an explicitly requested reader review, a fresh reader starts at `index.md` and follows the affected owning documents. Routine wording edits use the main agent's diff check.
- It reports with file:line every place it cannot follow: an undefined or generic-looking term, a step it cannot trace, a diagram that differs from its text, a missing reason, a term whose meaning drifts, a class or layer that does not match what it groups, a section a maintainer cannot change safely without reading other files.
- Acceptance: accurate semantics and sound abstraction, so the documents are easy to understand and easy to maintain.
- A fix changes the documents, never the algorithm.
