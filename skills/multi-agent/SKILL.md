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

- Select the mode from the current unit's uncertainty and consequences, by the Applies-when column alone.
- Escalate the part that meets a higher mode's criteria; retain completed work and continue independent items.
- A branch carries one independently deliverable behavior, also when one context carries several branches.
- Only Full runs a separate design, refutation or independent review run; a Simple or Routine task passes the affected Pipeline phases of skill `chain-session` in its own session.

## Main Agent

- Assign code, documents, investigation that one read does not answer, evidence gathering, record edits and worktree cleanup to the roles `execution` assigns, through residents. Keep dispatch, decisions, acceptance disposition, integration and the user conversation. Edit and commit directly only a change that cannot be split by module.
- Accept a result from the resident's report and the evidence the report names (commit, check output, diff stat). Read a diff hunk, file or log excerpt when the report leaves a doubt that changes the acceptance, when the task mode requires a diff check, or to verify launch metadata; read run summaries in place of full transcripts.
- Send a gap in a resident's reported investigation back to that resident as a question.
- Answer boundary questions, decide agent-decidable items and put the user-decidable items, prepared under skill `decisions`, to the user in one batched question on the day they arise: in the reply text while a run can finish before the answer, with the host's question tool otherwise. An item counts as asked once that question is sent.
- Answer a question that a read of the project's own code or documents answers by doing that read.
- List every host that runs delegated or long-running work in `execution.hosts` with its role, output location and status command before work starts on it. Build each status report from the status command of every listed host.
- Report to the user the state of each running task in one line, the decisions waiting for the user, and each risk and each failed check that changes what the user would do.

## Context Economy

- Keep one resident agent per standing responsibility while its context stays useful. Resolve a task's module and role from its board write set and the resident registry `execution.resident` names, and resume that resident; start a new agent when no resident covers them, when the resident cannot be resumed, or when the handoff costs less than the stale context, and record the replacement in that registry.
- A brief states the purpose, the outcome as an independently deliverable result, acceptance checks, the tool and write boundaries, the effort level, dependencies, input revision and the change since that agent's last task. It references readable content by path and section and inlines only the decided sentences and changes needed to interpret the task.
- A result returns outcome, commit, checks and open items. Detail stays in the run directory; another agent receives its path.
- A resident restarts only when its context runs out or its responsibility ends, leaving a handoff file in its run directory.
- A read-only run whose result is an edit of the files it read continues in the same session under a write profile; a new session takes the edit only for independence (review, refutation, new reader), an exhausted context, or parallel write sets one session cannot carry. Reproduce a defect row on the current integration head inside that row's preparation session and record the input and result before the first edit; close the row, or add regression coverage, when it no longer reproduces.
- The implementing session fixes a reviewed diff; the reviewer stays read-only. A read-only audit of documents applies its own findings, continued under a write profile one document area at a time after the running writers of that area; a finding that changes the meaning of a decided sentence goes to the main agent before the edit.

## Dispatch

1. Select Simple, Routine or Full under Task Modes above. Do a Simple task directly when briefing costs more than the work; route other work to the resident that holds its context. Before adding a board row or launching a run, search every open board row and open question for a shared root cause, decided sentence, input or write set, and record that search in the request: each open row that shares one, or that no row does. Attach each symptom test to the row that implements its decided sentence. Merge rows sharing a root cause and acceptance goal into one independently deliverable row, preserving every acceptance item; order a row that needs another's result after it; record the choice with its reason. Open rows are taken in the order `integration.dispatch_order` states when it is configured.
2. Parallelize across independent tasks; run the stages of one task in one session.
3. Keep one agent loop. Start a separate run for one of:
   1. an independent review or refutation, which needs a fresh context;
   2. a task with fixed inputs whose write set is disjoint from every running task's;
   3. context the main agent must not hold, whose result fits a one-screen summary.
4. Give a change that requires seeing several files at once (deduplication, conflict resolution, a cross-file rename, a corpus-wide edit) to one run.
5. Size tasks as independently checkable results. Reuse established context and evidence; keep the task and agent across a context compaction.
6. Launch a task beside others only when its board row records each check:
   1. Every user-decidable decision it implements is recorded.
   2. Its write set is prepared and approved before the session edits, and disjoint from every running task's write set, compared by file and, for a shared document, by section; the comparison is repeated before the write set widens.
   3. Every contract it consumes is merged into `integration.branch`.
   4. Its result is checkable by the checks required for its task mode.
7. Hold a task that fails a check, or add it to the chain that owns its files. Launch a task that passes the checks of step 6 when its expected speed or quality gain exceeds its coordination cost and `integration.write_concurrency` and the configured token, compute and spending limits admit it; otherwise queue it.
   - Whenever a run ends or a branch merges, recheck each held row whose write set, dependency or hold cause that run or merge touches, against the current diffs, for a shared cause, a satisfied dependency, a smaller delivery and newly available disjoint work. A shared document whose two edits touch disjoint sections does not block; a hold whose cause is gone is released.
   - While a task waits, its read-only preparation (an inventory, a brief, a site list) runs ahead, or as `execution.prep` states when it is configured.
8. Apply `workflow/change-policy.md` Outcome and Scope before dispatch. A Simple request supplies inputs, allowed edits and a completion check in a short message. For Routine or Full, write the brief under Context Economy above with the task inputs, the project root, the glossary path (`communication/terminology.md` Established Terms), the write set, the protected files (the files another running task writes, computed at launch), the rules by owner path and the return fields. Route a required command the run's sandbox or allowlist refuses to the executor authorized to run it. For each function, type or property whose signature or behavior the task changes, search its callers, implementers and overrides; put each file found in the brief's write set, or state in the brief the reason that file needs no edit.
9. Quote in the brief, with path and line, every decided document sentence the task implements, and cite each rule by its owner path.
   - Name a related decision by its ID and landing path:line. Read the decision log only to trace why a rule holds or to prepare a new decision, by the main agent or under skill `decisions`.
   - Check the implemented decisions against entries governing the same affected contract. Reuse established evidence; contradictory requirements for one input go to the user before dependent work starts.
   - Update owning text when its meaning changes. Independent specification review applies to Full; an unchanged approved specification is reused.
10. Write the run registry row before launch: handle, task, model and effort, branch, progress file, status and next action. A gate the main agent launches and awaits itself gets its row once, when it ends, with its result.
11. Launch through the host's agent tool or a tracked background command, and keep its handle for follow-up and completion notifications. Launch each run directly; wait for its completion notification.
12. Give a research run that lacks a tool the exported source material.

## Dispatch Order

Dispatch open rows by layer, then by the configured precondition or chain order within a layer, then by the number of open rows a row blocks, then by cost from greatest to least, then by row ID. `execution.dispatch` supplies the project's preconditions and mechanism chains in order; without that value only the layer definitions apply.

1. Precondition: a defect that keeps results from being trusted or measured, such as an analysis that does not end on a project input or an unstable gate.
2. Mechanism chain: a step of a core mechanism replacement in progress. Each chain keeps one write run until the chain ends. A chain has file priority: a row that writes a file the chain's next step writes starts after that step merges.
3. Symptom: a crash, a missed finding or a false finding. Its reproduction test merges at once under Branch Lifecycle. Its fix is dispatched only when no chain is expected to remove or change the symptom and the code it changes is not code a chain deletes; otherwise the row waits and is rechecked when that chain step merges.
4. Cleanup, API work and later planned steps.

- A cost row belongs to the layer of the result its cost blocks.
- Record every blocker of a row as a dependency of that row.
- Merge a mechanism step under `integration.merge_bar` when it is configured, otherwise when every existing test passes and the parallel run of Branch Lifecycle shows each difference owned by an open row.
- A dispatch that departs from this order records its reason on the board row.

## Boundary Questions

- Answer a chain session's question in that same session, by resume or message.
- Widen the write set only for a prerequisite of the accepted result, within existing authorization and with no concurrent writer; otherwise keep the item separate or order it after its dependency.

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

- Every mode retains required repository and integration checks. Rerun affected checks after changes or new failures.
- Run a review at `execution.review.<difficulty>` of its board row, and the first full review of a change to a semantic sentence of an `algorithm.core_principles` entry at the last entry of `execution.review.levels`.
- When a later review or run finds an S1 finding that an earlier review of the same module missed, raise that module's review effort one entry of `execution.review.levels` for its next tasks, up to the last entry, and record the raised level in the ledger.
- Use the Review Checklist of skill `chain-session` for findings and `integration.merge_bar` for the acceptance verdict; without that value the verdict follows the merge criterion below. The reviewer brief names both and lists only the task's real inputs as acceptance criteria.
- Accept a review or acceptance verdict only from the completed run's result for the candidate revision and the gate evidence that result cites.
- After each FIX-FIRST and before the fix round, record on the board row one line per finding: the task goal it serves and the real output it changes. Give a fix round only to the findings with that line; make each other finding its own row or drop it.
- The fix round resumes the implementing session and hands it the review report's path. The re-check resumes the same review session over the fix diff only; a new review session starts only when that session cannot be resumed. A question of the fixer about a finding goes to the review session that holds it.
- Block a merge by `integration.merge_bar` when it is configured; otherwise block it for a regression against the integration head or for a failure of the branch to implement on ordinary inputs the decided sentence it claims, until a scoped repair or an independently correct split removes the cause.
- Merge an uncovered input whose result is no worse than the integration head's with the branch as one disabled test that reproduces and names the fault and one Open Gaps line in the owning design document. Enable a reproduction that passes and give it no gap line. Correct a wrong document or comment sentence in the branch with no further review round.
- After two returns on the same result, classify each open item by the merge criterion above and skill `decisions` Authority, run one closing round on the blocking items the agent owns, and send only user-decidable questions to the user. Split or stop the remaining result when an agent-owned blocking item survives the closing round; return a fix that needs a new dependency or module to the main agent as a scope question under Boundary Questions.
- Route a finding outside the write set and each finding the merge criterion does not block by `integration.scope_control` when it is configured, otherwise by the project's acceptance criteria: join a finding that shares an open task's cause to that task as an acceptance item with its reproducing input as a test of that task, and record an unrelated improvement as its own row.

## Branch Lifecycle

- Cut each worktree and branch from the `integration.branch` head, with every submodule at the commit that head records, outside the repository folder.
- A finished part whose gate and review pass merges that day; a part that waits on a decision or another row splits into its own row, and the finished part merges without it.
- When `integration.branch_lifetime` is configured, size tasks to fit it. Branch age counts from creation, waiting included. A branch that reaches the limit consolidates at once: its independently correct finished work merges after the required checks, the rest splits into bounded rows, or the ledger records why no safe finished slice exists. A split row is ordered after the merge of the branch's finished part; it becomes that part's prerequisite only when that part alone adds a defect no row owns.
- A replacement of one implementation by another lands in the integration branch in steps behind one switch whose default keeps the old implementation (branch by abstraction); each task branch that holds the switch or the replacement's fixes merges within `integration.branch_lifetime`. The default flips in its own change once the comparison below shows no difference, or the user decides each remaining one; the next row removes the old implementation.
- While both implementations exist, the gate `integration.test_tiers` selects runs both on the project's evaluation inputs and compares their outputs (parallel run); record each difference on an open row before integration, and judge the difference by `integration.merge_bar` when it is configured.
- `tools/branch_check.py` reads `integration.branch`, `integration.upstream` and `integration.branch_lifetime` and reports, at session start and after each push, the commits of `integration.branch` not yet pushed to or pulled from `integration.upstream`, and each landed, overdue or unowned task branch and removable worktree; every status pass resolves each reported item.
- A defect's reproduction test merges into the integration branch as soon as it reproduces, disabled with the defect named, and the defect is stated as an open gap; a fix that stops leaves its evidence there, not only on its branch.
- A fix that waits on another row stops: its branch is archived and removed, and the row names the archived commits to re-apply. When the dependency merges, the row cuts a new branch from the `integration.branch` head instead of updating the old one.
- A branch ends with its row: when a row closes, splits or is superseded, or its prototype stops, the same records update archives and removes the branch unless an open row names it as reference. Each status pass runs `integration.record_check`, which reports each task branch that no open row names.
- To archive a branch, commit its uncommitted work on it, write its commits beyond `integration.branch` into a bundle under `integration.branch_archive`, verify the bundle and record its path in `branch.<name>.archive`. `hooks/git_guard.py` permits `git branch -D` only for an archived branch.
- Name a task branch by `integration.task_branch_pattern` and every other agent-created branch under `workflow/git-safety.md` Branches and Conflicts; its `branch.<name>.description` holds the task ID, the goal and the session handle.
- After an interruption, commit the run's work in progress on its branch.
- The main agent publishes the targets `integration.publication` names, under `workflow/git-safety.md` Publication. At integration, fast-forward each configured submodule branch and publish it before the superproject commit that records it. Send a failed fast-forward to the user.
- The main agent integrates a finished branch under `integration.merge_bar` and `workflow/git-safety.md`, after its gate and review pass and the required integration checks run. Return a finished-result report that lacks the gate comparison of skill `chain-session` Work Loop step 7 to the same session before review or merge. Move the integration branch only to a merge result that passes `integration.merge_bar`, or, without that value, whose gate adds no failure or finding to the integration head's; send a failure found after the move to the session that holds the branch context. Resolve conflicts under `workflow/git-safety.md`.
- After the merge-result gate, remove the worktree once its tracked, untracked and ignored files and every submodule are clean or disposable build output, then delete the task branch with `git branch -d` from the integration checkout. A task-named submodule branch goes only after its commits reach `integration.submodule_branch`.
- Every status pass reconciles worktrees as well as branches. A worktree that no open run or row names, or whose branch is merged, is judged by what it holds beyond `integration.branch`: commits whose change that branch lacks, uncommitted and untracked files, and submodule heads no ref keeps. With nothing beyond it, the worktree is removed. Commit or port content an open row needs to that row's branch; read and archive the rest, uncommitted work included, then remove the worktree.
- Rebased submodule pointers for the same implementation step may be set without the user when those commits were rebased onto the integration head's recorded commits and `git range-diff` proves the patches identical.
- After every merge, reconcile branches absent from the open board line by line against integration; recover or explain missing content. A rejected implementation's branch stays only while a board row names it as reference; then it is archived and removed.

## Records

- The board, the ledger, the run registry and the directives are the files `integration.records` names; without them the task docs of `rules/workflow/records.md` hold the rows.
- Keep each fact in its one record: task status on the board, run execution and scheduler handles in the run registry, the user's verbatim orders in the directives, measurements in `integration.records.metrics_script` output and the measurement record, and the current state with owner links in the ledger. Keep proposed, applied, committed and independently verified as distinct states.
- The board lists every open task with its write set, dependencies, chain, branch, difficulty and the checks; a defect row also lists the case number of `workflow/change-policy.md` Correctness and Verification that holds for it and, under case 2, the ID of the row whose task implements the sentence. A split or consolidation moves every acceptance item and dependency to the row that keeps it and removes the covered rows in the same update.
- A run result that changes rows is applied per item: each verdict lands as a board edit in one update, or as a row that names the items still to apply. The run registry records the result as applied only when no item remains; the board holds every board change a result file records.
- Update the run registry row on every notification. Record each launch, finished or failed run, added or removed host in the same turn as the event; record each user message and its directive disposition in the directives before acting on it.
- Compute the status of a batch of runs with the status command of each host of `execution.hosts` and the committed run receipts.
- A board dependency names the file or contract the row consumes from that row, under `integration.dependency_evidence` when it is configured; drop an entry that names neither.
- Record edits that follow a fixed procedure (post-merge archiving, status cells, ledger lines) go to one resident bookkeeper run on `execution.bookkeeper`, one request per batch, whose brief states that it edits run-storage records and works in no worktree; the main agent keeps the decisions and reads only its reply.
- After context compaction, reread the run registry, then the ledger, then the board, and the directives against the messages since the last recorded one; reconcile them against the committed receipts and each host's status command before acting or reporting. Act on the reconciled records over the compacted summary, and correct a record that disagrees with those artifacts before any status report.
- Read run summaries. Get missing evidence from a follow-up turn of the session that holds the context.
- `integration.records.metrics_script` computes per task, from git and the run logs: runs launched, resumptions, fix and review rounds, model and effort, `execution.token_measure` split into uncached input, cached input, output and reasoning without double counting, billed cost, wall time and the accepted outcome.
- A process change alters one thing at a time and is judged against these numbers on comparable tasks.
- When `integration.progress_snapshot` is configured, the bookkeeper appends its row on that schedule and records the close date on each row it archives as done; a completion-date estimate reads those rows.
- Run a retrospective when the user requests one or `execution.schedule` names one: identify a process problem from the recorded evidence and evaluate one scoped change. Create a recurring job only from `execution.schedule`, and record its handle in the run registry.

## Consolidation

- Consolidate when requested or required by a configured project schedule or integration step. List rows that share a cause or write set, duplicates, stale statuses and ready branches; apply only authorized merges and record state changes.
- When consolidation is required, split a row that combines independently deliverable behavior; a branch past its lifetime follows Branch Lifecycle. Preserve each acceptance item and dependency with the part that owns it.
- For a blocking row, identify the contract, file or decided sentence each dependent consumes and the smallest independently correct delivery that provides it. Replace whole-row waits with that delivery when write sets are disjoint; the delivery merges first and the rest of the row follows; remove an edge only after its contract is delivered.
- Once per `execution.consolidation_interval`, recheck the whole board.
- A row that implements a decided sentence closes only into a row that implements the same sentence.

## Model Routing

| Run | Model and effort |
|---|---|
| Main agent | Session model |
| Chain session | `execution.implementer.<difficulty>` of the chain's hardest task |
| Reviewer | Review above |
| Research, analysis | `execution.background` at `max_effort` when `execution.background.agent` names the run kind; otherwise `execution.code_agent` |
| Refutation, count run, new reader | `execution.background` at `high_effort` when `execution.background.agent` names the run kind; otherwise `execution.code_agent` |
| Design question | `execution.design.algorithmic` for an algorithm design question; `execution.design.software` for an interface or module design question |

- After each launch or resume, compare the run's transcript model with the routed value; relaunch a run whose model differs.

## Run Isolation

- Run directories live in `integration.run_storage`. Each board task has one working directory there, named by its task ID, with one subdirectory per run; it moves to `integration.run_archive` when the row closes.
- A read-only run's working directory and sandbox are its own run directory. A write run works in its own worktree.
- `tools/codex_rules.py pack`, given the target project checkout, writes the rule-reading instructions into the run directory, routing each project value file under `<repository>/.codex/rules/project/` by its `paths:` frontmatter, and the project glossary path; `--lean` briefs a chain session and adds skill `chain-session` as a required read. Verify the configured glossary path before the run starts. Count findings after the log shows those reads; inspect the scoped reads, since `gate` checks only always-active path mentions.
- Each run persists its result and returns a summary of at most one screen with evidence, limits and next step. Hold dependent work on a failed or missing result; record the remaining work on the board before a batch closes.

## Reader Review

- For a Full task with a revision of a document's design content, or an explicitly requested reader review, a fresh reader starts at `index.md` and follows the affected owning documents. Routine wording edits use the main agent's diff check.
- The fresh reader reports with file:line every place it cannot follow: an undefined or generic-looking term, a step it cannot trace, a diagram that differs from its text, a missing reason, a term whose meaning drifts, a class or layer that does not match what it groups, a section a maintainer cannot change safely without reading other files.
- Acceptance: accurate semantics and sound abstraction, so the documents are easy to understand and easy to maintain.
- Fix a fresh reader's finding in the documents and keep the algorithm.
