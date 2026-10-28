# Multi-Agent Discussion, Design and Implementation

Parameters `integration` and `evidence` are supplied by the project rule files under `rules/project/`, in `integration.md` and `evidence.md`; `reference` is owned by `evidence.md`.

Worker runs discuss, design, implement and test. `execution` is supplied by `rules/project/execution.md`. The main agent coordinates delegated work. Always active; applies when work is delegated. Shared working-tree safety: `workflow/git-safety.md`.

---

## Division of Labor

- Scope picks the applier. On a small project or an indivisible change, the main agent applies directly. On a modular project, implementation workers return patches under Parallel Dispatch to the single applier.
- Workers never write the target tree or Git metadata; their unique output directory is their write sandbox. Discussion, research and analysis return text; implementation, recording and design-only review return patches plus summaries.
- Only one applier writes the target tree and Git metadata. Concurrent patches use the same fixed base; the applier checks patch bases, reconciles overlaps and integrates serially.
- A change that requires seeing several files at once — deduplication, conflict resolution, a cross-file rename, a corpus-wide edit — goes to one run, never split across runs.
- Whoever writes a file runs the task quality gate, including tests, lint and the documentation check for the written files, before committing.

## When to Split

- One agent loop is the default: the main agent works directly, or one implementer owns a whole task chain — plan, tests, code and fix rounds — in one context.
- A separate run is justified only by one of: context the main loop must not hold, whose result fits a one-screen summary; parallel work whose context is disposable once it lands; independent verification (review, adversarial check); an isolated write set or permission. The task's value pays for the added cost.
- Work splits by context, never by role or problem type. Tasks that share files, contracts or decisions stay in one run, in order.
- Every handoff loses detail, so a task keeps the shortest chain: decided documents, implementer, independent reviewer, implementer. A task whose design the decided documents already state gets no intermediate plan document; an analyst plan precedes only an algorithmic task.

## Parallel Dispatch

- A task runs as an asynchronous parallel run only when it is established fit for it, and its board row records each check:
  1. Every decision it implements is recorded.
  2. Its write set is disjoint from every running task's write set.
  3. Every contract it consumes is merged into the integration branch.
  4. Its result is checkable by the quality gate and an independent review.
- A task that fails a check waits, or joins the run that owns its chain, in order. Filling a concurrency cap is never a goal.
- At most three implementation chains run at once.
- A brief quotes, with path and line, every decided document sentence the task implements; it never paraphrases a rule. The implementer reads the cited documents itself.
- The implementer implements every sentence its brief quotes. A sentence it cannot implement inside its write set stops the run with a report; it is never recorded as an open gap of the code.

## Implementation Organization

Model and effort routing belongs to Model Routing. Decision-run authority belongs to `workflow/decisions.md`.

| Role | Scope and authority |
|---|---|
| Main agent | Owns the board, ledger, merge queue and user communication. Dispatches ready work and assigns the single applier under Division of Labor. |
| Applier | Accepts patches only from a run that passed the rules gate; checks bases, reconciles overlaps, applies, runs the documentation check on every written file and rejects a new finding, lints and commits serially through the task gate. Owns branch integration and cleanup. |
| Implementer | Owns one patch task chain and every fix round in its output directory. Reads cited documents, follows `code/testing.md`, returns patches, verification and a summary. A replacement takes over only when the original run is gone. |
| Reviewer | Independently checks the finished diff against decided documents and real output. Returns MERGE or FIX-FIRST. Each edge case is a reproduction for the implementer. Read-only. |
| Analyst | Owns research, mathematics, implementation analysis and the algorithm steps of a task whose design is decided. Precedes algorithmic implementation; read-only. A design question goes to the design run. |
| Decision roles | Handle every design question: an interface choice, an algorithm, or a mechanism the decided documents do not name. Authority follows `workflow/decisions.md` Decision Runs. |
| New reader | `workflow/development.md` Reader Review. Read-only. |

- Each worktree and branch is cut from the integration branch head, with every submodule at the commit that head records.
- Shared-file ordering and contract readiness follow Parallel Dispatch.
- Rebase a finished branch onto `integration.branch` and pass its gate and required independent review. The applier fast-forwards it and runs the full gate. Conflict handling belongs to `workflow/git-safety.md`.
- The task board lists every task with its write set, dependencies, difficulty, assigned role, branch and the Parallel Dispatch checks. When a run finishes, the main agent dispatches the next task that passes those checks.
- A split or a consolidation moves every acceptance item and dependency to the row that keeps it, and removes each parent or covered row in the same board update.
- Each run writes its details to its output file and returns a summary of at most one screen; the main agent reads only summaries, so its context holds coordination, not work; missing evidence comes from a follow-up run, never from re-deriving the analysis.

## Finding Triage

- A reviewer reports the problems the branch's diff introduces and the violations of the decided sentences its task implements. A pre-existing problem, a case outside the valid inputs, or a request for behavior beyond those sentences goes to an appendix and never decides the verdict or widens the branch's acceptance.
- Each finding carries a severity: S1 a result the reference output contradicts, a contradiction of a decided document, a crash or a gate failure; S2 a missing test of decided behavior, or a rule violation the diff introduces; S3 wording or style.
- Each finding carries a difficulty: mechanical, local or algorithmic.
- Each finding carries an urgency: U0 blocks a merge or the gate; U1 lies on the critical path of the current program step; U2 is an in-scope leaf; U3 lies outside the current step's scope and goes to its module's task doc, never to the board.
- Before each review round, the main agent records what the pending diff changes and picks the check from it:
  1. A task's first landing, or a fix that adds or changes a semantic sentence (result selection, order, identity, state or lifetime, serialization, algorithm text): one independent review of the whole task against its decided sentences and program output. A plan, chief or refutation never replaces it.
  2. A fix that changes a mechanism, an invariant, a shared caller, a reference identity or a decoder: a targeted independent check of the whole cause and its boundary cases, with every reproduction of the earlier rounds.
  3. A fix that changes only assertions or fixtures of decided behavior, wording or links, and adds no semantic sentence, helper algorithm, source path or caller: the gate and the main agent's diff check, which confirms each reproduction fails on the base and passes on the fix. No new review.
- A branch takes at most two full reviews. After that only an S1 finding the diff introduces, shown by a program output or a decided sentence, blocks its merge, and it closes through check 2 or 3; every other finding goes to a task doc or a board row.
- A finding whose cause lies outside the branch's write set becomes its own row with that write set. When the branch's diff newly exposes it on a program the integration head analyzes, the branch merges after that row.

## Branch Lifecycle

- A branch uses `integration.task_branch_pattern` and carries one task. From creation its `branch.<name>.description` holds the task ID, the goal and the agent handle.
- The applier commits implementation work before the task ends, using `wip:` for failing work; after interruption it commits pending implementation work on that branch. Workers checkpoint their output and never commit.
- A pointer bump and its dependent consumer change share one commit.
- During implementation, the applier pushes submodule commits only to the task-named branch.
- At integration, the superproject records each submodule's `integration.submodule_branch` head. Fast-forward that branch to the recorded commit and push it before pushing `integration.branch`. A failed fast-forward goes to the user.
- Delete a task-named submodule branch only after its commits reach that branch and deletion is authorized under `workflow/git-safety.md`.
- Before each push, fetch and rebase onto `integration.upstream`. Never push unresolved conflicts.
- A branch is rebased in place under its own name; a task never re-cuts its work onto a new branch name.
- After fast-forward and the full gate, remove the worktree when Branch Lifecycle cleanup conditions hold. Branch deletion follows `workflow/git-safety.md`; run it from the integration checkout when authorized.
- A worktree is removed only after its tracked, untracked and ignored files and every submodule are clean or disposable build output.
- After every merge, reconcile branches absent from the open board line by line against integration. Recover or explain missing content. Deletion remains subject to `workflow/git-safety.md`; the agent never uses a prohibited command.
- A rejected implementation's branch stays only while a board row names it as reference.

## Measurement

- The ledger records review rounds, rework commits, wall time, the `execution.token_measure`, decision-run counts and later overturns. Decision transcripts also supply tool calls by kind, repeated calls and time to first result write.
- A process change alters one thing at a time and is judged against these numbers on comparable tasks.
- A daily retrospective reads these numbers, the run registry and the board growth, names the largest process problem with its numbers, and applies at most one change.

## Run Ledger

- The main agent owns user communication and a persistent run ledger; a complex discussion forms a hierarchy of main agent, runs and independent checkers.
- The ledger holds the verbatim question, numbered user directives, hierarchy, roles, gate order, protected files, versioned inputs, dependencies and next steps.
- Before launch, the ledger fixes task ID, parent, role, model, effort, versioned inputs, output directory, target files, dependencies, question and acceptance criteria. Add the handle when assigned.
- Every finding, result, failure, gate and decision updates the ledger with evidence, status and next step. Keep proposed, agreed, applied, committed and independently verified distinct.
- A run registry holds one row per delegated run: handle, task, model and effort, branch, output file, status, last progress and next action. The row is written before launch and updated on every notification.
- The ledger keeps the current state in one short file and the history in an archive; the board lists open rows only, and a closed row moves to the board archive.
- After context compaction, the main agent rereads the run registry, then the current ledger, before acting; both take precedence over the compacted summary.

## Credential Outage

- A zero-token shell watcher, never a timed model turn, checks run liveness and the model provider's credentials. It wakes the main agent only for a stale run, a sign-in session about to end, or credentials restored after an outage.
- A run appends each finished step to its output file as it goes, so a stopped run resumes from its last step.
- Before the sign-in session ends: no new run on `execution.outage_provider` starts; the applier commits pending implementation work, every worker checkpoints its last finished step in its output, the ledger takes a checkpoint entry, and the user is asked to sign in again.
- During an outage, runs on `execution.continuing_provider` continue; nothing requiring a turn on `execution.outage_provider` is retried.
- On restore: a recovery report lists each open row's state and every result landed since the outage start; each stopped run on `execution.outage_provider` resumes with the native message tool from its checkpoint, landed results are consumed, and no finished work restarts.

## Consolidation

- Before every launch and after every analysis, the main agent compares open questions for shared inputs and root causes, and records merge or order with reasons in the ledger.
- Questions sharing a cause merge into one discussion; a question that needs another's answer is ordered after it.
- Independent discussions run in parallel only when their inputs are complete and fixed; no discussion consumes an answer still being produced.
- Each run returns consolidation findings after its analysis; the main agent reconciles them before the next launch.
- A consolidation pass runs every six hours: an independent read-only run lists the rows that share a cause or a write set, duplicates, rows outside the current step, stale statuses and branches whose checks passed. The main agent applies the merges, moves and state changes, merges each ready branch, and records the open-row count before and after. A row that implements a decided sentence closes only into a row that implements the same sentence.

## Roles per Stage

- The main agent selects the viewpoints the stage's questions need and records the selection; no fixed full panel. In a design run each viewpoint is a section, not a separate run. The decision-run sequence belongs to `workflow/decisions.md`.
- A local change takes the implementer and one independent review. A mechanical change takes a low-cost implementer, the gate and the main agent's diff check.
- Stage discussions follow the phase gates in `workflow/development.md`.

| Stage | Viewpoints selected for the question | Reads | Outputs |
|---|---|---|---|
| Research | Researcher, security expert, cross-domain researcher | Question, recorded decisions, literature, tools, reference implementations | Cited findings, analogous mechanisms, limits and counterexamples |
| Analysis | Algorithm designer, security expert, performance/precision reviewer, affected module owners | Complete affected-item inventory, research, current contracts | Cause groups, all-member and boundary checks, cost/precision/security tradeoffs |
| Design | Module owners, architect, algorithm designer, engineer | Every module owner's interface section, analysis and research | Contract corrections and abstraction assessment |
| Decision | `workflow/decisions.md` | Question and evidence | Decision or user question |
| Review | Independent critic, security/performance/precision reviewers, chief on escalation only; new reader last | Candidate design, evidence, the integrated edits; reader inputs owned by `workflow/development.md` Reader Review | Refutations, verification evidence, the chief's corrections on escalation, and reader findings |

- In a full design review, the design run gives each affected module owner one section with its provided and required interfaces and its handoff defects; every other viewpoint reads all of those sections, and the refutation groups its findings by root cause.
- Architect review applies `rules/docs/design.md` to maintainability, semantic type boundaries and abstraction, and `rules/communication/terminology.md` to naming. Keep domain policy outside reusable mechanisms.
- A design-only review returns design/implementation-document patches. Algorithm findings enter discussion and code differences follow `rules/docs/design.md` Open Gaps, with no algorithm or code edits in that review. The single applier integrates patches.
- New-reader corrections go through the single applier.

## Solution Review

- Apply `workflow/change-policy.md` to every fix and `code/quality.md` No Patch-Style Code to its implementation.
- Validate cause groups before repair. A distinct mechanism needs evidence that the problem differs and a rationale in its owning document.
- Open design items, independent refutations and their return/escalation sequence, decision authority, questions and recording follow `workflow/decisions.md`.
- The design run or analyst performs the known-limitation survey required by `workflow/decisions.md` Solution Checks.
- The ledger links the decision record placed under `CLAUDE.md` Local Records.

## Model Routing

| Task | Model and effort |
|---|---|
| Main agent | session model |
| Code workers | `execution.code_workers` |
| Recording | `execution.recording` |
| Reasoning, research, analysis, mathematics, algorithm plans and question drafting | `execution.background` at its maximum effort |
| Review, refutations and count runs | `execution.background` at its high effort |
| Decision contexts | `workflow/decisions.md` Decision Runs |
| New reader | `execution.background` at its high effort |

- Record task difficulty and model before launch. Record whether `execution.background.agent` can execute it; use `execution.code_agent` for required tools it lacks or for code work under the table.
- After launch or resume, check the transcript model. Stop and relaunch a run using an older generation than required.
- The main agent launches needed background work directly through the shell. No worker exists only to wrap another provider's run.
- Export source material to research runs that lack a tool. Every proposal passes the same refutation.

## Run Isolation

- Run directories live in persistent scratch storage outside temporary directories. Every worker's working directory and sandbox are its unique output directory, never the target tree. Only the applier edits the integration worktree.
- A worktree lives outside the repository folder: an editor or language server opened on the repository walks the whole folder and would index every worktree's sources.
- `tools/codex_rules.py pack` writes the rule-reading instructions, including every project markdown rule under `<repository>/.codex/rules/project/`, into the run directory. Read always-active rules and every scoped rule the topic needs. Findings count only after the log shows those reads; `gate` checks always-active path mentions, so scoped reads and actual read commands still need inspection.
- A launch brief carries the ledger entry, question, project root, target files, exclusions, protected files, dependencies, acceptance criteria and return format.
- Persist the result before returning patches plus a summary containing evidence, limits, verification and next step. A no-change result returns an empty patch set.
- A background run launches as a tracked background command, so its exit notifies the main agent. A waiter for several runs starts only after each run's launch record exists, and sends one completion notification with findings and failures; no polling.
- Research artifacts, vetted analogues and citation-audit verdicts become rows of the task's evidence file, which the matching refutation or review reads; all research finishes before the applier integrates document patches.
- Failed or missing findings block dependent discussions; the ledger records the remaining work before a batch closes.

## Working Files

- Each board task has one working directory in the run storage, named by its task ID, with one subdirectory per run and the task's evidence file. It lives while the task's row is open and moves to the run storage archive when the row closes.
- Evidence row fields, generic kinds and validation belong to `tools/evidence.py`. `evidence` binds the project meanings and reference runtime. One row holds one established fact.
- A run reads the evidence file before it searches, and writes new rows only in its own run directory. After the run ends, the main agent merges them into the task's file with `tools/evidence.py merge`, which keeps one current row per kind and source and marks a row whose value disagrees with the kept one as a conflict; no model edits the merged file.
- A row is stale when its quoted text no longer appears in its source file, or its program file or interpreter version changed. The merge marks it, and a stage that relies on it reads the source again and writes a new row.
- Durable evidence placement follows `CLAUDE.md` Local Records.

- The first stage drafting options gathers needed facts once. Later stages cite fresh rows and add only missing facts; never repeat a search a fresh row records.

- Never edit protected files named by a brief. Report a needed protected edit as unresolved.
