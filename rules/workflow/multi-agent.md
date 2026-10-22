# Multi-Agent Discussion, Design and Implementation

Codex CLI runs and Claude subagents discuss, design, implement and test; on a modular project the main agent plans, dispatches, merges and talks to the user. Always active; applies when work is delegated. Shared working-tree safety: `workflow/git-safety.md`.

---

## Division of Labor

- Scope picks the editor. On a small project, or for a change that cannot be split by module or file, the main agent edits and commits directly. On a project whose modules or files develop independently, implementation runs in parallel under Implementation Organization, and the main agent writes no code or document itself.
- Discussion, research, design and review runs are read-only and return text.
- An implementation run edits only inside its own git worktree and branch. It never merges, pushes, or writes the shared working tree or another run's worktree.
- A change that requires seeing several files at once — deduplication, conflict resolution, a cross-file rename, a corpus-wide edit — goes to one run, never split across runs.
- A single call or a direct edit is the default for small work. A delegated run launches only when its parallel viewpoints, breadth or independent write set exceed one call, and the task's value pays for the added cost.
- Whoever writes a file runs the quality gate — tests, lint, doc check — on it before committing.

## Implementation Organization

Every module has one lead, and every role has its own scope and authority.

| Role | Model, effort | Scope | Authority |
|---|---|---|---|
| Main agent | session model | Task board, schedule, merge queue, user communication | Dispatches runs, fast-forwards finished branches, runs the full gate after each merge; edits nothing |
| Project lead | Sonnet 5.5 `xhigh` | All modules | Checks that every task is done and that code matches the decided algorithm and documents; reports each gap to the main agent; read-only |
| Module lead | Sonnet 5.5 `high` | One module's tasks and worktree | Splits tasks by difficulty, assigns engineers, reviews their diffs against the code and rule standards, fixes bugs the tests find |
| Engineer | Sonnet 5.5 `medium` or `low`; Haiku 5.5 `medium` or `low` | One task's write set in its module's worktree | Writes the test first, implements, runs the gate, commits |
| Test engineer | Codex `gpt-6.1-sol` `max` | A module once its tasks land | Writes edge-case tests from the design documents; failures go to the module lead |
| Senior architects; chief architect | Sonnet 5.5 `xhigh`; Opus 5.5 `max` | Interface choices and algorithm questions | Architects discuss; the chief decides and states corrections for the owning lead |
| New reader | Sonnet 5.5 `low`; Haiku 5.5 `medium` or `low` | Finished documents | Reports every place it cannot follow; read-only |
| Analyst | Codex `gpt-6.1-sol` `max` | Reasoning, mathematics, research, implementation analysis | Read-only |

- Model and effort follow task difficulty: a mechanical task goes to Haiku 5.5 or Sonnet 5.5 `low`, a moderate task to Sonnet 5.5 `medium`, an algorithmic task to an analyst run first and then a Sonnet 5.5 `high` or Opus 5.5 `high` implementer.
- Each worktree and branch is cut from the integration branch head, with every submodule at the commit that head records.
- Running implementers hold pairwise disjoint write sets. A file two tasks touch has one owner or a fixed order. Cross-module contracts are frozen before their consumers start.
- A branch merges after it is rebased onto the integration head and passes its gate, its module lead's review and an independent read-only reviewer. The main agent fast-forwards it and runs the full gate. A rebase conflict goes to the user, never auto-resolved.
- The task board lists every task with its write set, dependencies, difficulty and assigned role. Whenever a run finishes, the main agent dispatches the next ready task and keeps the concurrency cap filled; the cap follows the machine's build capacity.
- Each run writes its details to its output file and returns a summary of at most one screen; the main agent reads only summaries, so its context holds coordination, not work.

## Run Ledger

- The main agent owns user communication and a persistent run ledger; a complex discussion forms a hierarchy of main agent, track leads and independent checkers.
- The ledger holds the verbatim question, numbered user directives, hierarchy, roles, inputs and their versions, dependencies and next steps.
- Before launch, a ledger entry fixes task ID, parent, role, model, effort, inputs, output directory, dependencies and the question to answer; the handle is added when assigned.
- Every finding, failure and decision updates the ledger with evidence, status and next step; proposed, agreed and independently verified remain distinct states.
- After context compaction, the main agent rereads the ledger before acting; the ledger takes precedence over the compacted summary.

## Consolidation

- Before every launch and after every analysis, the main agent compares open questions for shared inputs and root causes, and records merge or order with reasons in the ledger.
- Questions sharing a cause merge into one discussion; a question that needs another's answer is ordered after it.
- Independent discussions run in parallel only when their inputs are complete and fixed; no discussion consumes an answer still being produced.
- Each run returns consolidation findings after its analysis; the main agent reconciles them before the next launch.

## Roles per Stage

- The main agent selects roles with distinct viewpoints for the stage's questions and records the selection; no fixed full panel.
- Every discussion starts with independent proposals, then each role reads the other positions and answers their claims with evidence; one chief resolves disagreements and records the disposition.
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
- Analysis covers every affected item and boundary case against research, repository conventions and recorded decisions before options leave the panel.
- An independent adversarial verifier attempts to refute every solution with counterexamples and invariant, security, precision and cost checks; unresolved refutations return to analysis.

## Decisions Before the User

- Decision authority and question format come from the project decision rule.
- A user-decided item reaches the user only after panel discussion, a check against recorded decisions, and panel agreement on the options, recommended option and worked example.
- The chief decides agent-decidable items without asking and records the outcome; the ledger links the project's decision record.
- After a user decision, the main agent records it in the same turn and dispatches its implementation, then continues the next independent discussion.
- Decision record placement and document ownership follow `CLAUDE.md`.

## Model Routing

- Each delegated run names its model and effort by task difficulty, per the Implementation Organization table.
- Reasoning, research, root-cause analysis, algorithm design, mathematics, question drafting and checking run through background Codex CLI, with explicit model `gpt-6.1-sol` and reasoning effort `max`. A Codex run launches from Bash by the main agent or by the lead that needs it; no Claude agent exists only to wrap one. Divergent mathematics, literature and open-design discussions add such a run as an independent participant.
- A code review convenes a Sonnet 5.5 reader that critiques a branch's diff read-only and returns findings, not edits.
- The main thread reads only each run's summary file and requests missing evidence through a follow-up run; it never re-derives returned analyses.
- Tool-dependent research receives exported source material when the run lacks the tool; every proposal passes the same critics.

## Run Isolation

- Run directories live in persistent scratch storage outside temporary directories; each discussion run's working directory and sandbox are its own unique output directory, never the target tree. An implementation run's working directory is its own worktree.
- Every Codex run loads the agent rules, which Codex never reads on its own: `tools/codex_rules.py pack` writes its working directory's `AGENTS.md`, listing the always-active rules and the path-scoped rules for the files its topic touches. Its findings count only when its log shows a read of every rule its topic relies on.
- A launch brief carries the ledger entry plus the question and the return format.
- Every run persists its findings before the main agent reads them and returns a summary with evidence, limits and next step.
- Each batch has one waiter that waits for every handle and sends one completion notification with findings and failures; no polling.
- Research artifacts, vetted analogues and citation-audit verdicts feed matching review roles for a second pass; the owning lead edits the documents after the discussion concludes.
- Failed or missing findings block dependent discussions; the ledger records the remaining work before a batch closes.
