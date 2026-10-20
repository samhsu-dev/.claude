# Multi-Agent Orchestration

How the main agent runs work across Codex CLI runs and Claude subagents. Always active; applies when work is delegated. Shared working-tree safety: `workflow/git-safety.md`.

---

## Run Ledger

- The main agent owns user communication and a persistent run ledger; large tasks form a hierarchy of main agent, track leads, workers and independent checkers.
- The ledger holds the verbatim task and numbered user directives, hierarchy, gate order, dependencies, protected files and next steps.
- Before launch, a ledger entry fixes task ID, parent, role, model, effort, inputs and their versions, output directory, target files, protected files, dependencies and acceptance criteria; the handle is added when assigned.
- Every result, failure, gate and decision updates the ledger with evidence, status and next step; proposed, applied, committed and independently verified remain distinct states.
- After context compaction, the main agent rereads the ledger before acting; the ledger takes precedence over the compacted summary.

## Task Consolidation

- Before every launch and after every analysis, the main agent compares tasks for shared inputs, target files and root causes, and records merge, order or parallel execution with reasons in the ledger.
- Tasks sharing a cause merge when one deliverable and acceptance gate cover them; tasks that need another task's output are ordered.
- Workers return consolidation findings after each analysis; the main agent reconciles them before the next launch.
- Independent tasks run in parallel only when their inputs are complete and fixed and their write sets are disjoint; no task consumes an input still being produced.
- Tasks targeting the same files run in order or return patches; patch reconciliation follows Run Isolation and Integration.

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
| Recording | Recorder, affected module owners, chief | Resolved decision, owning sections, approved research and audit findings | Patches for owning documents and downstream work |
| Review | Independent critic, security/performance/precision reviewers, chief; new reader last | Candidate solution, evidence, integrated changes; reader inputs owned by `workflow/development.md` Reader Review | Refutations, verification evidence, chief's corrections and reader findings |

- Full design reviews collect each module owner's provided/required interfaces and handoff defects in one sheet before role reviewers read all sheets; the chief consolidates their replies by root cause.
- Architect review uses `docs/design.md` for maintainability, semantic type boundaries and abstraction, and `communication/terminology.md` for naming; it also checks domain policy stays outside reusable mechanisms.
- A design-only review returns design/implementation-document patches; algorithm findings enter discussion and code differences follow `docs/design.md` Open Gaps, with no algorithm or code edits in that review.
- The chief routes new-reader corrections through the applier.

## No Ad Hoc Solutions

- Before any fix, the root-cause gate applies the root-cause and capability rules of `workflow/change-policy.md`: it validates the consolidation groups and asks whether one mechanism solves each group, checking existing mechanisms first.
- The gate rejects per-item special cases under `code/quality.md` No Patch-Style Code; a distinct mechanism requires evidence that the problem differs and a design rationale in its owning document.
- Before proposing a solution with a known limitation, researchers survey literature, industrial tools, cross-domain methods, closed-form mathematics and known algorithms, and return cited alternatives and remaining limits.
- Analysis covers every affected item and boundary case against research, repository conventions and recorded decisions before options leave the panel.
- An independent adversarial verifier attempts to refute every solution with counterexamples and invariant, security, precision and cost checks; unresolved refutations return to analysis.

## Decisions Before the User

- Decision authority and question format come from the project decision rule.
- A user-decided item reaches the user only after panel discussion, a check against recorded decisions, and panel agreement on the options, recommended option and worked example.
- The chief decides agent-decidable items without asking and sends the outcome for recording; the ledger links the project's decision record.
- After a user decision, the main agent delegates recording and implementation in background tasks and continues the next independent decision discussion.
- Decision record placement and document ownership follow `CLAUDE.md`; recording batches contain one or two items and return patches to the applier.

## Model Routing

- Before launch, the main agent records whether Codex can execute the task; Claude workers handle code or tasks requiring tools Codex lacks.
- Reasoning, research, root-cause analysis, algorithm design, mathematics, question drafting and checking run directly through background Codex CLI, with explicit model `gpt-6.1-sol` and reasoning effort `max`; no Claude wrapper agent. Divergent mathematics, literature and open-design discussions add such a run as an independent participant.
- Multiple senior architects use Sonnet 5.5 at `xhigh` for synthesis and software-design discussion; one chief architect uses Opus 5.5 at `max` to decide, produce design/implementation-document corrections and review them.
- Code workers use Sonnet 5.5 at `medium` or `high`; recording uses Codex or an inherited-model worker.
- The main thread reads only worker summary files and requests missing evidence through follow-up tasks; it never re-derives returned analyses.
- Tool-dependent research receives exported source material when the worker lacks the tool; GPT proposals pass the same critics as other proposals.

## Run Isolation and Integration

- Run directories live in persistent scratch storage outside temporary directories; each worker's working directory and write sandbox are its own unique output directory.
- Every Codex run loads the agent rules, which Codex never reads on its own: `tools/codex_rules.py pack` writes its working directory's `AGENTS.md`, listing the always-active rules it reads before any work and the path-scoped rules and skills it reads before touching a matching file. Its result counts only when `tools/codex_rules.py gate` finds in its log a read of every rule its patched files need.
- A launch brief carries the Run Ledger entry plus exclusions and return format; workers never write the target tree or Git metadata.
- Every worker persists its result before the main agent reads it and returns patches plus a summary containing evidence, limits, verification and next step; no-change results return an empty patch set.
- Each batch has one waiter that waits for every handle and sends one completion notification with results and failures; no polling by the main agent or wrapper workers.
- Research artifacts, vetted analogues, citation-audit verdicts and approved source additions feed matching design-review/audit roles for a second pass and the update plan; all research finishes before document-update patches are applied.
- Only one applier writes the target tree and Git metadata; concurrent patches use the same fixed base. The applier takes a stack only from a run that passed the rules gate, checks patch bases, reconciles overlaps, applies, runs `tools/codex_rules.py doccheck` on every written file and rejects a new finding, lints and commits serially through the project's quality gate.
- The applier skips protected files and records them as unresolved; staging by name and Git-write checks belong to `workflow/git-safety.md`, commit procedure and cadence to `workflow/committing.md`.
- Failed or missing outputs block dependent tasks; independent verification follows integration, and the ledger records the remaining work before a batch closes.
