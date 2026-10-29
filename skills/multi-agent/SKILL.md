---
name: multi-agent
description: Coordinate delegated runs as the main agent. Use before dispatching, briefing or resuming a run, choosing a review, merging a branch, after a module's documents are revised, at consolidation, in a credential outage, or after compaction.
---

Coordinate delegated work as the main agent. Hard limits: `rules/workflow/multi-agent.md`. Parameters `integration` and `execution` come from the project rule files `integration.md` and `execution.md` under `rules/project/`, and `algorithm.core_principles` from `decisions.md`.

## Dispatch

1. Before each launch, compare open tasks and questions for shared inputs, write sets and root causes. Merge rows that share a cause into one row, landed on one branch and checked by one review; order a row that needs another's result after it; record the choice with its reason.
2. Parallelize across independent tasks, never across the stages of one task. The stages of one task share context and the implicit decisions in its actions; every handoff between them loses detail.
3. Keep one agent loop. A separate run is justified only by one of:
   1. an independent review or refutation, which needs a fresh context;
   2. a task with fixed inputs whose write set is disjoint from every running task's;
   3. context the main agent must not hold, whose result fits a one-screen summary.
4. Give a change that requires seeing several files at once — deduplication, conflict resolution, a cross-file rename, a corpus-wide edit — to one run, never split across runs.
5. Size each task to finish before its session's first automatic context compaction.
6. Launch a task beside others only when its board row records each check:
   1. Every user-decidable decision it implements is recorded.
   2. Its write set, stated at module level, is disjoint from every running task's write set.
   3. Every contract it consumes is merged into `integration.branch`.
   4. Its result is checkable by the quality gate and an independent review.
7. Hold a task that fails a check, or add it to the chain that owns its files. The number of concurrent chains has no fixed cap: every task that passes the checks of step 6 may run.
   - Whenever a run ends or a branch merges, recheck every held row against the current diffs, not against its recorded hold reason. A shared document whose two edits touch disjoint sections does not block; a hold whose cause is gone is released.
   - While a task waits, its read-only preparation — an inventory, a brief, a site list — runs ahead.
8. Write the brief: the task or question, project root, write set or target files, exclusions, protected files, dependencies, acceptance criteria and return format. The protected files are the files another running task writes, computed at launch.
9. Quote in the brief, with path and line, every decided document sentence the task implements; never paraphrase a rule.
10. Write the run registry row before launch: handle, task, model and effort, branch, progress file, status and next action.
11. Launch the run from the shell as a tracked background command, so its exit notifies the main agent. No worker exists only to wrap another provider's run, and nothing polls; a waiter for several runs starts only after each run's launch record exists.
12. Give a research run that lacks a tool the exported source material.

## Boundary Questions

- Answer a chain session's question in that same session, by resume or message; never stop and relaunch it.
- Widen the write set when no running task writes the files the answer needs; otherwise order the item after that task.
- Take a user-decidable question to the user under skill `decisions`.

## Chains

- A chain is a sequence of tasks that share files, contracts or decisions. Its tasks run in order in one session.
- After a merge, resume the chain session for the chain's next task; its brief carries the integration diff since its last commit.
- A fresh session replaces it after its first automatic context compaction or when the chain moves to another module.

## Review

Pick the check before each review round from what the pending diff changes:

| Pending diff | Check |
|---|---|
| A task's first landing, or a fix that adds or changes a semantic sentence (result selection, order, identity, state or lifetime, serialization, algorithm text) or decides a design question | One independent full review against the decided sentences and program output |
| A fix that changes a mechanism, an invariant, a shared caller, a reference identity or a decoder | A targeted check of the whole cause and its boundary cases with every earlier reproduction, in the earlier reviewer's resumed session |
| A fix that changes only assertions or fixtures of decided behavior, wording or links | The gate and the main agent's diff check, which confirms each reproduction fails on the base and passes on the fix |

- A task whose board row is mechanical and whose diff changes at most 200 lines takes the main agent's diff check and the gate in place of the independent full review; every other first landing keeps the independent full review.
- A review runs at `execution.review.<difficulty>` of its board row. Exception: the first full review of a change to a semantic sentence of an `algorithm.core_principles` entry runs at `execution.background.max_effort`.
- An S1 finding that a later review or run finds and an earlier review of the same module missed raises that module's review effort one entry of `execution.review.levels` for its next tasks, up to the last entry. The ledger records the module's raised level.
- The reviewer brief names the Review Checklist of skill `chain-session`, which defines the severities and real inputs; its acceptance criteria list only the task's real inputs.
- After each FIX-FIRST and before the fix round, record on the board row one line per finding: the task goal it serves and the real output it changes. A finding without that line gets no fix round; it becomes its own row or is dropped.
- A second FIX-FIRST on the same component, or a fix that needs a new dependency, parser or module, stops the chain until the main agent restates the task's scope.
- A branch takes at most two full reviews. After that only an S1 finding the diff introduces, shown by program output or a decided sentence, blocks its merge, and it closes through the targeted check or the diff check.
- A finding whose cause lies outside the branch's write set becomes its own row. When the branch newly exposes it on a program the integration head analyzes, the branch merges after that row.
- The merge report gives the user the phase counts of a change that broke a decided bound of zero added work (`rules/workflow/change-policy.md`).

## Branch Lifecycle

- Cut each worktree and branch from the `integration.branch` head, with every submodule at the commit that head records, outside the repository folder, since an editor opened on the repository indexes the whole folder.
- Name a branch by `integration.task_branch_pattern`; its `branch.<name>.description` holds the task ID, the goal and the session handle.
- After an interruption, commit the run's work in progress on its branch.
- During implementation, submodule commits are pushed only to the task-named branch. At integration, fast-forward each submodule's `integration.submodule_branch` to the commit the superproject records and push it before `integration.branch`; a failed fast-forward goes to the user.
- Rebase a finished branch in place onto `integration.branch`, under its own name. After its gate and review pass, fast-forward `integration.branch` to it and run the full gate. Before each push, fetch and rebase onto `integration.upstream`; never push unresolved conflicts.
- After the full gate, remove the worktree once its tracked, untracked and ignored files and every submodule are clean or disposable build output. A task-named submodule branch goes only after its commits reach `integration.submodule_branch`.
- After every merge, reconcile branches absent from the open board line by line against integration; recover or explain missing content. A rejected implementation's branch stays only while a board row names it as reference.

## Records

- The run ledger holds the verbatim question, numbered user directives, chains, gate order, versioned inputs, dependencies and next steps, one short line per row; full directive text lives in its archive. Proposed, applied, committed and independently verified stay distinct states.
- The board lists every open task with its write set, dependencies, chain, branch, difficulty and the checks. A split or consolidation moves every acceptance item and dependency to the row that keeps it and removes the covered rows in the same update.
- Update the run registry row on every notification.
- After context compaction, reread the run registry, then the ledger, then the board, before acting; they take precedence over the compacted summary.
- Read only run summaries. Missing evidence comes from a follow-up turn of the session that holds the context, never from re-deriving the analysis.
- A script computes, per task, runs launched, resumptions, fix rounds, review rounds, `execution.token_measure` and wall time from git and the run logs.
- A process change alters one thing at a time and is judged against these numbers on comparable tasks.
- A daily retrospective names the largest process problem with its numbers, counts the decisions a later review overturned, and applies at most one change.

## Consolidation

- Daily, without delegating, list the rows that share a cause or a write set, duplicates, rows outside the current step, stale statuses and branches ready to merge. Apply the merges, moves and state changes, merge each ready branch and record the open-row count before and after.
- The same pass splits each row larger than one branch lifetime or holding more than one behavior into independently mergeable parts, each one behavior with its tests; an activation lands its dormant parts first and the switch last, and each acceptance item and dependency moves to the part that owns it.
- For each row more than three open rows wait on, it names what each waiting row consumes, as a contract, file or decided sentence, and the smallest slice or commit that provides it, and replaces a whole-row dependency by that slice when the write sets are disjoint.
- After each merge, the rows that named the merged row are checked again for a shared cause, a met dependency and a narrower dependency.
- A row that implements a decided sentence closes only into a row that implements the same sentence.

## Credential Outage

- A zero-token shell watcher, never a timed model turn, checks run liveness and the model provider's credentials. It wakes the main agent only for a stale run, a sign-in session about to end, or credentials restored after an outage.
- Before the sign-in session ends: no new run on `execution.outage_provider` starts; each running write run on that provider commits its work in progress and every running run on it records its last finished step; the ledger takes a checkpoint entry, and the user is asked to sign in again.
- During an outage, runs on `execution.continuing_provider` continue; nothing requiring a turn on `execution.outage_provider` is retried.
- On restore, a recovery report lists each open row's state and every result landed since the outage start; each stopped run resumes in its own session from its checkpoint, and no finished work restarts.

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
- `tools/codex_rules.py pack` writes the rule-reading instructions into the run directory, including every project markdown rule under `<repository>/.codex/rules/project/`; `--lean` briefs a chain session and adds skill `chain-session` as a required read. Findings count only after the log shows those reads; `gate` checks always-active path mentions, so scoped reads still need inspection.
- Each run persists its result and returns a summary of at most one screen with evidence, limits and next step. A failed or missing result blocks dependent work; the ledger records the remaining work before a batch closes.

## Reader Review

- After every complete revision of a module's documents is committed, a new reader reads them from `index.md`: concept, model, design, impl, in that order, the documents only.
- It reports with file:line every place it cannot follow: an undefined or generic-looking term, a step it cannot trace, a diagram that differs from its text, a missing reason, a term whose meaning drifts, a class or layer that does not match what it groups, a section a maintainer cannot change safely without reading other files.
- Acceptance: accurate semantics and sound abstraction, so the documents are easy to understand and easy to maintain.
- A fix changes the documents, never the algorithm.
