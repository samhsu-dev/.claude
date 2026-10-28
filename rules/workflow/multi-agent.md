# Multi-Agent Work

Parameters `integration`, `evidence` and `execution` are supplied by the project rule files under `rules/project/`, in `integration.md`, `evidence.md` and `execution.md`; `reference` is owned by `evidence.md`.

How the main agent runs delegated work. Always active; applies when work is delegated. Shared working-tree safety: `workflow/git-safety.md`.

---

## Principle

- Parallelize across independent tasks, never across the stages of one task. The stages of one task share context and the implicit decisions in its actions; every handoff between them loses detail.
- One agent loop is the default. A separate run is justified only by one of:
  1. an independent review or refutation, which needs a fresh context;
  2. a task with fixed inputs whose write set is disjoint from every running task's;
  3. context the main agent must not hold, whose result fits a one-screen summary.
- A change that requires seeing several files at once — deduplication, conflict resolution, a cross-file rename, a corpus-wide edit — goes to one run, never split across runs.
- Work follows the phase gates of `workflow/development.md`; no run skips or reorders them.

## Roles

| Role | Scope and authority |
|---|---|
| Main agent | Owns the board, ledger, merge queue, branch cleanup and user communication. Dispatches tasks that pass Parallel Dispatch, fast-forwards finished branches and runs the full gate after each merge. |
| Chain session | Owns one task chain from reading to merge-ready in its own worktree: reads the cited documents, decides the chain's agent-decidable design questions, writes the test first, implements, runs the gate, commits and takes every fix round. |
| Reviewer | Checks a finished diff against the decided documents and real output. Returns MERGE or FIX-FIRST and writes each edge case as a reproduction the chain session adds as a test. Read-only. |
| Drafter and refutation | Only for a user-decidable question: `workflow/decisions.md` Decision Runs. |
| New reader | `workflow/development.md` Reader Review. Read-only. |

- Scope picks the editor. On a small project, or for a change that cannot be split by module or file, the main agent edits and commits directly. On a project whose modules or files develop independently, the main agent writes no code or document itself.
- A read-only run returns text. A write run edits only inside its own git worktree and branch and its run directory; it never merges, pushes, rebases, or writes the shared working tree or another run's worktree.
- Whoever writes a file runs the task quality gate, including tests, lint and the documentation check for the written files, before committing.

## Chain Session

- A chain is a sequence of tasks that share files, contracts or decisions. Its tasks run in order in one session.
- The session is long-lived: after a merge it resumes for the chain's next task, and its brief carries the integration diff since its last commit. A fresh session replaces it after its first automatic context compaction or when the chain moves to another module.
- It appends each finished step to a progress file in its run directory, so a stopped session resumes from its last step.
- It decides an agent-decidable design question itself under `workflow/decisions.md` Decision Runs and writes the decision entry into its progress file; the main agent moves the entry into the decision log. A user-decidable question stops that item with the question and its evidence.
- Every fix follows `workflow/change-policy.md` and `code/quality.md` No Patch-Style Code: existing mechanisms first; a distinct mechanism needs evidence that the problem differs and a rationale in its owning document.
- A sentence it cannot implement inside its write set stops that item with a report; it is never recorded as an open gap of the code.

## Parallel Dispatch

- A task runs beside others only when its board row records each check:
  1. Every user-decidable decision it implements is recorded.
  2. Its write set is disjoint from every running task's write set.
  3. Every contract it consumes is merged into the integration branch.
  4. Its result is checkable by the quality gate and an independent review.
- A task that fails a check waits, or joins the chain that owns its files. At most three chains run at once; filling that cap is never a goal.
- A brief quotes, with path and line, every decided document sentence the task implements; it never paraphrases a rule. The chain session reads the cited documents itself and implements every quoted sentence.
- The board lists every open task with its write set, dependencies, chain, branch and the checks. A split or consolidation moves every acceptance item and dependency to the row that keeps it and removes the covered rows in the same update.

## Review

- A reviewer reports the problems the diff introduces and the violations of the decided sentences its task implements. A pre-existing problem, a case outside the valid inputs, or a request for behavior beyond those sentences goes to an appendix, never decides the verdict, and becomes a row of its module's task doc.
- Severity: S1 a result the reference output contradicts, a contradiction of a decided document, a crash or a gate failure; S2 a missing test of decided behavior, or a rule violation the diff introduces; S3 wording or style.
- A review applies `rules/docs/design.md` to maintainability, semantic type boundaries and abstraction, and `rules/communication/terminology.md` to naming; domain policy stays outside reusable mechanisms.
- Before each review round, the main agent picks the check from what the pending diff changes:
  1. A task's first landing, or a fix that adds or changes a semantic sentence (result selection, order, identity, state or lifetime, serialization, algorithm text) or decides a design question: one independent full review against the decided sentences and program output.
  2. A fix that changes a mechanism, an invariant, a shared caller, a reference identity or a decoder: a targeted check of the whole cause and its boundary cases with every earlier reproduction, in the earlier reviewer's resumed session.
  3. A fix that changes only assertions or fixtures of decided behavior, wording or links: the gate and the main agent's diff check, which confirms each reproduction fails on the base and passes on the fix.
- A branch takes at most two full reviews. After that only an S1 finding the diff introduces, shown by program output or a decided sentence, blocks its merge, and it closes through check 2 or 3.
- A finding whose cause lies outside the branch's write set becomes its own row. When the branch newly exposes it on a program the integration head analyzes, the branch merges after that row.

## Branch Lifecycle

- Each worktree and branch is cut from the integration branch head, with every submodule at the commit that head records, and lives outside the repository folder, since an editor opened on the repository indexes the whole folder.
- A branch uses `integration.task_branch_pattern` and carries one task; its `branch.<name>.description` holds the task ID, the goal and the session handle. It is rebased in place under its own name.
- Every write run commits before it ends, red work under a `wip:` subject; after an interruption the main agent commits the run's work in progress on its branch. A pointer bump and its dependent consumer change share one commit.
- During implementation, submodule commits are pushed only to the task-named branch. At integration, each submodule's `integration.submodule_branch` is fast-forwarded to the commit the superproject records and pushed before `integration.branch`; a failed fast-forward goes to the user.
- A finished branch is rebased onto `integration.branch` and passes its gate and review; the main agent fast-forwards it and runs the full gate. Before each push, fetch and rebase onto `integration.upstream`; never push unresolved conflicts. Conflict handling belongs to `workflow/git-safety.md`.
- After the full gate, the worktree is removed once its tracked, untracked and ignored files and every submodule are clean or disposable build output. Branch deletion follows `workflow/git-safety.md`; a task-named submodule branch goes only after its commits reach `integration.submodule_branch`.
- After every merge, branches absent from the open board are reconciled line by line against integration; missing content is recovered or explained. A rejected implementation's branch stays only while a board row names it as reference.

## Records

- The main agent keeps a run ledger: the verbatim question, numbered user directives, chains, gate order, protected files, versioned inputs, dependencies and next steps. The current state stays in one short file and the history in an archive; the board lists open rows only. Proposed, applied, committed and independently verified stay distinct states.
- A run registry holds one row per delegated run: handle, task, model and effort, branch, progress file, status and next action. The row is written before launch and updated on every notification.
- After context compaction, the main agent rereads the run registry, then the ledger, then the board, before acting; they take precedence over the compacted summary.
- The main agent reads only run summaries. Missing evidence comes from a follow-up turn of the session that holds the context, never from re-deriving the analysis.
- Per task, the ledger records runs launched, resumptions, review rounds, `execution.token_measure`, wall time and later overturns. A process change alters one thing at a time and is judged against these numbers on comparable tasks. A daily retrospective names the largest process problem with its numbers and applies at most one change.

## Consolidation

- Before every launch, the main agent compares open tasks and questions for shared inputs, write sets and root causes. Those sharing a cause merge into one chain; one that needs another's result is ordered after it; the choice is recorded with its reason.
- Every six hours the main agent itself lists the rows that share a cause or a write set, duplicates, rows outside the current step, stale statuses and branches ready to merge. It applies the merges, moves and state changes, merges each ready branch and records the open-row count before and after. A row that implements a decided sentence closes only into a row that implements the same sentence.

## Credential Outage

- A zero-token shell watcher, never a timed model turn, checks run liveness and the model provider's credentials. It wakes the main agent only for a stale run, a sign-in session about to end, or credentials restored after an outage.
- Before the sign-in session ends: no new run on `execution.outage_provider` starts; each running write run on that provider commits its work in progress and every running run on it records its last finished step; the ledger takes a checkpoint entry, and the user is asked to sign in again.
- During an outage, runs on `execution.continuing_provider` continue; nothing requiring a turn on `execution.outage_provider` is retried.
- On restore, a recovery report lists each open row's state and every result landed since the outage start; each stopped run resumes in its own session from its checkpoint, and no finished work restarts.

## Model Routing

| Run | Model and effort |
|---|---|
| Main agent | session model |
| Chain session | `execution.implementer.mechanical`, `execution.implementer.moderate` or `execution.implementer.algorithmic`, by the chain's hardest task |
| Drafter without a chain, research, analysis | `execution.background` at its maximum effort |
| Review, refutation, count run, new reader | `execution.background` at its high effort |

- After each launch or resume, check the transcript model; stop and relaunch a run on an older generation than required.
- A run launches from the shell as a tracked background command, so its exit notifies the main agent; no worker exists only to wrap another provider's run, and nothing polls. A waiter for several runs starts only after each run's launch record exists.
- A research run that lacks a tool receives exported source material.

## Run Isolation

- Run directories live in persistent scratch storage outside temporary directories. Each board task has one working directory there, named by its task ID, with one subdirectory per run; it moves to the run storage archive when the row closes.
- A read-only run's working directory and sandbox are its own run directory, never the target tree. A write run works in its own worktree.
- `tools/codex_rules.py pack` writes the rule-reading instructions into the run directory, including every project markdown rule under `<repository>/.codex/rules/project/`; `--lean` leaves out the coordination rules for a chain session. Findings count only after the log shows those reads; `gate` checks always-active path mentions, so scoped reads still need inspection.
- A launch brief carries the task or question, project root, write set or target files, exclusions, protected files, dependencies, acceptance criteria and return format. A run never edits a protected file; a needed protected edit is reported as unresolved.
- Each run persists its result and returns a summary of at most one screen with evidence, limits and next step. A failed or missing result blocks dependent work; the ledger records the remaining work before a batch closes.

## Evidence Files

- A user-decidable question keeps its facts in an evidence file in its task's working directory. Row fields, generic kinds and validation belong to `tools/evidence.py`; `evidence` binds the project meanings and reference runtime. One row holds one established fact.
- A run reads the evidence file before it searches and writes new rows only in its own run directory. The main agent merges them with `tools/evidence.py merge`, which keeps one current row per kind and source and marks a row whose value disagrees with the kept one as a conflict; no model edits the merged file.
- A row is stale when its quoted text no longer appears in its source file, or its program file or interpreter version changed. A stage that relies on it reads the source again and writes a new row.
- The first stage gathers the needed facts once; later stages cite fresh rows and add only missing facts. Durable evidence placement follows `CLAUDE.md` Local Records.
