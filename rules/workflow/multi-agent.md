# Multi-Agent Discussion, Design and Implementation

Codex CLI runs and Claude subagents discuss, design, implement and test; on a modular project the main agent plans, dispatches, merges and talks to the user. Always active; applies when work is delegated. Shared working-tree safety: `workflow/git-safety.md`.

---

## Division of Labor

- Scope picks the editor. On a small project, or for a change that cannot be split by module or file, the main agent edits and commits directly. On a project whose modules or files develop independently, the main agent writes no code or document itself; implementation runs under Parallel Dispatch.
- Discussion, research, design and review runs are read-only and return text.
- An implementation run edits only inside its own git worktree and branch. It never merges, pushes, or writes the shared working tree or another run's worktree.
- A change that requires seeing several files at once — deduplication, conflict resolution, a cross-file rename, a corpus-wide edit — goes to one run, never split across runs.
- Whoever writes a file runs the quality gate — tests, lint, doc check — on it before committing.

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

Every role has its own scope and authority.

| Role | Model, effort | Scope | Authority |
|---|---|---|---|
| Main agent | session model | Task board, ledger, merge queue, branch cleanup, user communication | Dispatches runs that pass Parallel Dispatch, fast-forwards finished branches, runs the full gate after each merge; edits nothing on a modular project |
| Implementer | Haiku 5.5 or Sonnet 5.5 `low` for mechanical tasks; Sonnet 5.5 `medium` for moderate tasks; Sonnet 5.5 `high` or Opus 5.5 `high` for algorithmic tasks | One task chain in its own worktree | Reads the cited documents, writes the test first, implements, runs the gate, commits, takes every fix round of its branch (a new agent takes over only when it is gone) |
| Reviewer | Codex `gpt-6.1-sol` `high` | One finished branch | Checks the diff against the decided documents and real program output, writes each edge case as a reproduction the implementer adds as a test, returns MERGE or FIX-FIRST; read-only |
| Analyst | Codex `gpt-6.1-sol` `max` | Reasoning, mathematics, research, algorithm plans, implementation analysis | Precedes an algorithmic task's implementer; read-only |
| Senior architects; chief architect | Sonnet 5.5 `xhigh`; Codex `gpt-6.1-sol` `max` | Interface choices and algorithm questions the analyst and reviewer leave open | Architects discuss; the chief decides and states corrections for the implementer |
| New reader | Sonnet 5.5 `low`; Haiku 5.5 `medium` or `low` | Finished documents | Reports every place it cannot follow; read-only |

- Each worktree and branch is cut from the integration branch head, with every submodule at the commit that head records.
- A file two tasks touch has one owner or a fixed order. Cross-module contracts merge before their consumers start.
- A branch merges after it is rebased onto the integration head and passes its gate and an independent reviewer. The main agent fast-forwards it and runs the full gate. A rebase conflict goes to the user, never auto-resolved. Exception: a conflict confined to submodule pointers, where the task's submodule commits were first rebased onto the commits the integration head records and `git range-diff` shows them patch-identical; the main agent sets each pointer to the rebased submodule commit of the same step.
- The task board lists every task with its write set, dependencies, difficulty, assigned role, branch and the Parallel Dispatch checks. When a run finishes, the main agent dispatches the next task that passes those checks.
- A split or a consolidation moves every acceptance item and dependency to the row that keeps it, and removes each parent or covered row in the same board update.
- Each run writes its details to its output file and returns a summary of at most one screen; the main agent reads only summaries, so its context holds coordination, not work; missing evidence comes from a follow-up run, never from re-deriving the analysis.

## Finding Triage

- A reviewer reports the problems the branch's diff introduces and the violations of the decided sentences its task implements. A pre-existing problem, a case outside the valid inputs, or a request for behavior beyond those sentences goes to an appendix and never decides the verdict or widens the branch's acceptance.
- Each finding carries a severity: S1 a result the reference output contradicts, a contradiction of a decided document, a crash or a gate failure; S2 a missing test of decided behavior, or a rule violation the diff introduces; S3 wording or style.
- Each finding carries a difficulty: mechanical, local or algorithmic.
- Each finding carries an urgency: U0 blocks a merge or the gate; U1 lies on the critical path of the current program step; U2 is an in-scope leaf; U3 lies outside the current step's scope and goes to its module's task doc, never to the board.
- Before each review round, the main agent records what the pending diff changes and picks the check from it:
  1. A task's first landing, or a fix that adds or changes a semantic sentence (result selection, order, identity, state or lifetime, serialization, algorithm text): one independent review of the whole task against its decided sentences and program output. A plan, chief or choice check never replaces it.
  2. A fix that changes a mechanism, an invariant, a shared caller, a reference identity or a decoder: a targeted independent check of the whole cause and its boundary cases, with every reproduction of the earlier rounds.
  3. A fix that changes only assertions or fixtures of decided behavior, wording or links, and adds no semantic sentence, helper algorithm, source path or caller: the gate and the main agent's diff check, which confirms each reproduction fails on the base and passes on the fix. No new review.
- A branch takes at most two full reviews. After that only an S1 finding the diff introduces, shown by a program output or a decided sentence, blocks its merge, and it closes through check 2 or 3; every other finding goes to a task doc or a board row.
- A finding whose cause lies outside the branch's write set becomes its own row with that write set. When the branch's diff newly exposes it on a program the integration head analyzes, the branch merges after that row.

## Branch Lifecycle

- A branch is named `wt/<task-id>` and carries one task. From creation its `branch.<name>.description` holds the task ID, the goal and the agent handle.
- Every run commits before it ends, red work under a `wip:` subject. After an interruption the main agent commits the run's work in progress on its branch.
- A pointer bump and the consumer change that needs it share one commit. The main agent pushes each submodule commit to a submodule branch named after the task, and when the superproject commit lands, to the submodule branch the project rules name for the integration branch, before the superproject push.
- A branch is rebased in place under its own name; a task never re-cuts its work onto a new branch name.
- Right after a branch's fast-forward and full gate, the main agent removes its worktree and deletes the branch with `git branch -d`, run from a checkout whose HEAD is the integration branch.
- A worktree is removed only after its tracked, untracked and ignored files and every submodule are clean or disposable build output.
- After every merge, the branches not merged into the integration branch match the board's open rows. An extra branch is compared line by line against the integration branch; content absent there is recovered or explained before the user deletes the branch with `-D`.
- A rejected implementation's branch stays only while a board row names it as reference.

## Measurement

- The ledger records per task: review rounds, rework commits, wall time and Claude tokens. A chief or other decision run is also measured from its transcript: tool calls by kind, repeated calls, and the minute of its first result write.
- A process change alters one thing at a time and is judged against these numbers on comparable tasks.
- A daily retrospective reads these numbers, the run registry and the board growth, names the largest process problem with its numbers, and applies at most one change.

## Run Ledger

- The main agent owns user communication and a persistent run ledger; a complex discussion forms a hierarchy of main agent, track leads and independent checkers.
- The ledger holds the verbatim question, numbered user directives, hierarchy, roles, inputs and their versions, dependencies and next steps.
- Before launch, a ledger entry fixes task ID, parent, role, model, effort, inputs, output directory, dependencies and the question to answer; the handle is added when assigned.
- Every finding, failure and decision updates the ledger with evidence, status and next step; proposed, agreed and independently verified remain distinct states.
- A run registry holds one row per delegated run: handle, task, model and effort, branch, output file, status, last progress and next action. The row is written before launch and updated on every notification.
- The ledger keeps the current state in one short file and the history in an archive; the board lists open rows only, and a closed row moves to the board archive.
- After context compaction, the main agent rereads the run registry, then the current ledger, before acting; both take precedence over the compacted summary.

## Credential Outage

- A zero-token shell watcher, never a timed model turn, checks run liveness and the model provider's credentials. It wakes the main agent only for a stale run, a sign-in session about to end, or credentials restored after an outage.
- A run appends each finished step to its output file as it goes, so a stopped run resumes from its last step.
- Before the sign-in session ends: no new Claude run starts, each running Claude run commits its work in progress and records its last finished step, the ledger takes a checkpoint entry, and the user is asked to sign in again.
- During an outage Codex runs continue; nothing that needs a Claude turn is retried.
- On restore: a recovery report lists each open row's state and every result landed since the outage start; each stopped Claude run resumes with SendMessage from its checkpoint, landed results are consumed, and no finished work restarts.

## Consolidation

- Before every launch and after every analysis, the main agent compares open questions for shared inputs and root causes, and records merge or order with reasons in the ledger.
- Questions sharing a cause merge into one discussion; a question that needs another's answer is ordered after it.
- Independent discussions run in parallel only when their inputs are complete and fixed; no discussion consumes an answer still being produced.
- Each run returns consolidation findings after its analysis; the main agent reconciles them before the next launch.
- A consolidation pass runs every six hours: an independent read-only run lists the rows that share a cause or a write set, duplicates, rows outside the current step, stale statuses and branches whose checks passed. The main agent applies the merges, moves and state changes, merges each ready branch, and records the open-row count before and after. A row that implements a decided sentence closes only into a row that implements the same sentence.

## Roles per Stage

- The main agent selects roles with distinct viewpoints for the stage's questions and records the selection; no fixed full panel.
- Discussion depth follows difficulty. A design question (an algorithm, a core principle, or a mechanism or interface the decided documents do not name) takes one design run and one independent refutation. A local change takes the implementer and one review. A mechanical change takes a low-cost implementer, the gate and the main agent's diff check.
- The design run reads the evidence file and writes one section per selected viewpoint, each ending in its own option and recommendation; then the claims on which the sections disagree, each settled by an evidence row; then the decision, or the question text, and the decision entry. One model holding several viewpoints in one context matches a multi-agent discussion at a fraction of its runs, and rebuttal rounds add little beyond independent answers.
- The refutation runs in a fresh context with the question, the evidence file and the candidate rule, not the design run's reasoning, and tries to refute the rule with counterexamples, invariant and cost checks. A refutation returns to the design run once. One that still stands, or a design run whose viewpoints disagree on the option, escalates: independent proposals, one per viewpoint, then one chief; no rebuttal round.
- The evidence a topic's decision needs (decision records, document lines, history hits, program outputs, corpus counts) is gathered once, by the first stage that drafts options, into the task's evidence file (Working Files). Every later stage cites its rows and adds a row only for a fact the file lacks; no stage repeats a search a row records.
- The chief decides from the role results and the evidence file within the time box its brief sets. It runs no search or program of its own; a fact it lacks becomes a follow-up question in its result, and the choice that needs the fact waits for the answer.
- One Codex run checks a chief's result: it tries to refute each choice and answers the follow-up questions together, since both read the same inputs.
- Stage discussions overlay the phase gates owned by `workflow/development.md`; they grant no permission to skip or reorder those gates.

| Stage | Roles selected for the question | Reads | Outputs |
|---|---|---|---|
| Research | Researcher, security expert, cross-domain researcher | Question, recorded decisions, literature, tools, reference implementations | Cited findings, analogous mechanisms, limits and counterexamples |
| Analysis | Algorithm designer, security expert, performance/precision reviewer, affected module owners | Complete affected-item inventory, research, current contracts | Cause groups, all-member and boundary checks, cost/precision/security tradeoffs |
| Design | Module owners, architect, algorithm designer, engineer | All module interface sheets, analysis and research | Contract corrections and abstraction assessment |
| Decision | Relevant reviewers and chief | Discussed proposals, adversarial results, recorded decisions | Agreed options, recommendation and worked example; disposition under the project decision rule |
| Review | Independent critic, security/performance/precision reviewers, chief; new reader last | Candidate design, evidence, the integrated edits; reader inputs owned by `workflow/development.md` Reader Review | Refutations, verification evidence, chief's corrections and reader findings |

- Full design reviews collect each module owner's provided/required interfaces and handoff defects in one sheet before role reviewers read all sheets; the chief consolidates their replies by root cause.
- Architect review uses `docs/design.md` for maintainability, semantic type boundaries and abstraction, and `communication/terminology.md` for naming; it also checks domain policy stays outside reusable mechanisms.
- A design review returns design/implementation findings as text; algorithm findings enter discussion and code differences follow `docs/design.md` Open Gaps. The owner of the file makes any resulting edit.
- New-reader corrections go to the owner of the document.

## No Ad Hoc Solutions

- Before any fix, the root-cause gate applies the root-cause and capability rules of `workflow/change-policy.md`: it validates the consolidation groups and asks whether one mechanism solves each group, checking existing mechanisms first.
- The gate rejects per-item special cases under `code/quality.md` No Patch-Style Code; a distinct mechanism requires evidence that the problem differs and a design rationale in its owning document.
- Before proposing a solution with a known limitation, researchers survey literature, industrial tools, cross-domain methods, closed-form mathematics and known algorithms, and return cited alternatives and remaining limits.
- Analysis covers every affected item and boundary case against research, repository conventions and recorded decisions before options leave the design run.
- An independent adversarial verifier attempts to refute every solution with counterexamples and invariant, security, precision and cost checks; unresolved refutations return to analysis.

## Decisions Before the User

- Decision authority and question format come from the project decision rule.
- A user-decided item reaches the user only after its design run and refutation, a check against recorded decisions, and agreement on the options, recommended option and worked example.
- The chief decides agent-decidable items without asking and records the outcome; the ledger links the project's decision record.
- After a user decision, the main agent records it in the same turn and dispatches its implementation, then continues the next independent discussion.
- Decision record placement and document ownership follow `CLAUDE.md`.

## Model Routing

- Each delegated run names its model and effort by task difficulty, per the Implementation Organization table.
- After each launch or resume, the main agent checks the model the run's transcript records. A run on an older model generation than the table names is stopped and relaunched.
- Reasoning, research, root-cause analysis, algorithm design, mathematics, discussion, question drafting and the chief run through background Codex CLI, with explicit model `gpt-6.1-sol` and reasoning effort `max`; review, choice checks and count runs use the same model at `high`. A Codex run launches from Bash by the main agent or by the implementer that needs it; no Claude agent exists only to wrap one. Divergent mathematics, literature and open-design discussions add such a run as an independent participant.
- Tool-dependent research receives exported source material when the run lacks the tool; every proposal passes the same critics.

## Run Isolation

- Run directories live in persistent scratch storage outside temporary directories; each discussion run's working directory and sandbox are its own unique output directory, never the target tree. An implementation run's working directory is its own worktree.
- A worktree lives outside the repository folder: an editor or language server opened on the repository walks the whole folder and would index every worktree's sources.
- Every Codex run loads the agent rules, which Codex never reads on its own: `tools/codex_rules.py pack` writes its working directory's `AGENTS.md`, listing the always-active rules and the path-scoped rules for the files its topic touches. Its findings count only when its log shows a read of every rule its topic relies on.
- A launch brief carries the ledger entry plus the question and the return format.
- A run's summary carries evidence, limits and next step.
- A Codex run launches as a tracked background command, so its exit notifies the main agent. A waiter for several runs starts only after each run's launch record exists, and sends one completion notification with findings and failures; no polling.
- Research artifacts, vetted analogues and citation-audit verdicts feed matching review roles for a second pass; the owning implementer edits the documents after the discussion concludes.
- Failed or missing findings block dependent discussions; the ledger records the remaining work before a batch closes.

## Working Files

- Each board task has one working directory in the run storage, named by its task ID, with one subdirectory per run and the task's evidence file. It lives while the task's row is open and moves to the run storage archive when the row closes.
- The evidence file holds one row per established fact: kind, spelled as `tools/evidence.py` checks it (`decision` record, `doc` line, `code` line, `history` hit, `php` program output, `corpus` count), the claim in one sentence, its source (path and line, commit, or command), the exact quoted text or complete output, and the run that read it.
- A run reads the evidence file before it searches, and writes new rows only in its own run directory. After the run ends, the main agent merges them into the task's file with `tools/evidence.py merge`, which keeps one row per kind and source and marks a row whose value disagrees with the kept one as a conflict; no model edits the merged file.
- A row is stale when its quoted text no longer appears in its source file, or its program file or interpreter version changed. The merge marks it, and a stage that relies on it reads the source again and writes a new row.
- A fact a decision record needs (its example, the output, the counts) is copied into that record when the decision is recorded; no record or document depends on a working directory.
