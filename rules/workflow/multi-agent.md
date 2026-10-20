# Multi-Agent Discussion and Design

Codex CLI runs and Claude subagents discuss and design; the main agent alone modifies the repository. Always active; applies when work is delegated. Shared working-tree safety: `workflow/git-safety.md`.

---

## Division of Labor

- A delegated run returns findings, analysis, design, options, recommendations or refutations as text. It never edits a file, writes the target tree, or runs a Git command.
- The main agent performs every repository edit and every commit itself, directly, after the discussion concludes. No patch stack, no applier, no delegated edit.
- Multi-agent runs serve one purpose: designing complex algorithms and discussing, researching and reviewing them. The repository is read-only to every delegated run.
- A change that requires seeing several files at once — deduplication, conflict resolution, a cross-file rename, a corpus-wide edit — the main agent makes directly, never split across agents.
- A single call or a direct edit is the default. A delegated discussion launches only when its parallel viewpoints or breadth exceed one call, and the task's value pays for the added cost.
- The main agent runs the quality gate — doc check and lint — on every file it writes before committing.

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
| Review | Independent critic, security/performance/precision reviewers, chief; new reader last | Candidate design, evidence, the main agent's integrated edits; reader inputs owned by `workflow/development.md` Reader Review | Refutations, verification evidence, chief's corrections and reader findings |

- Full design reviews collect each module owner's provided/required interfaces and handoff defects in one sheet before role reviewers read all sheets; the chief consolidates their replies by root cause.
- Architect review uses `docs/design.md` for maintainability, semantic type boundaries and abstraction, and `communication/terminology.md` for naming; it also checks domain policy stays outside reusable mechanisms.
- A design review returns design/implementation findings as text; algorithm findings enter discussion and code differences follow `docs/design.md` Open Gaps. The main agent makes any resulting edit.
- The main agent applies new-reader corrections itself.

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
- After a user decision, the main agent records and implements it itself, then continues the next independent discussion; recording and implementation are never delegated.
- Decision record placement and document ownership follow `CLAUDE.md`.

## Model Routing

- Each delegated run names the model its discussion needs; the main agent itself holds every file edit and commit.
- Reasoning, research, root-cause analysis, algorithm design, mathematics, question drafting and checking run through background Codex CLI, with explicit model `gpt-6.1-sol` and reasoning effort `max`; no Claude wrapper agent. Divergent mathematics, literature and open-design discussions add such a run as an independent participant.
- Multiple senior architects use Sonnet 5.5 at `xhigh` for synthesis and software-design discussion; one chief architect uses Opus 5.5 at `max` to decide and to state design/implementation corrections for the main agent to write.
- A code review convenes a Sonnet 5.5 reader that critiques the main agent's diff read-only and returns findings, not edits.
- The main thread reads only each run's summary file and requests missing evidence through a follow-up run; it never re-derives returned analyses.
- Tool-dependent research receives exported source material when the run lacks the tool; every proposal passes the same critics.

## Run Isolation

- Run directories live in persistent scratch storage outside temporary directories; each run's working directory and sandbox are its own unique output directory, never the target tree.
- Every Codex run loads the agent rules, which Codex never reads on its own: `tools/codex_rules.py pack` writes its working directory's `AGENTS.md`, listing the always-active rules and the path-scoped rules for the files its topic touches. Its findings count only when its log shows a read of every rule its topic relies on.
- A launch brief carries the ledger entry plus the question and the return format.
- Every run persists its findings before the main agent reads them and returns a summary with evidence, limits and next step.
- Each batch has one waiter that waits for every handle and sends one completion notification with findings and failures; no polling.
- Research artifacts, vetted analogues and citation-audit verdicts feed matching review roles for a second pass; the main agent edits the documents after the discussion concludes.
- Failed or missing findings block dependent discussions; the ledger records the remaining work before a batch closes.