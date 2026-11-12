---
name: chain-session
description: Carry one task chain to merge-ready, or review a finished diff. Use when a brief makes you a chain session or a reviewer, before changing design documents or code, or before a self-check.
---

Carry one task chain from reading to merge-ready in its own worktree, or review its finished diff. Hard limits: `rules/workflow/multi-agent.md`.

## Pipeline

A change to design documents or code passes the affected phases below in order, whoever implements it. Simple and Routine reuse existing decisions and perform only affected steps; Full uses the affected design stages and independent review (skill `multi-agent` Task Modes). Parameter `completion` comes from the project rule file `completion.md` under `rules/project/`. Document content follows `rules/docs/<type>.md`.

| # | Phase | Document | Approval | Skip when |
|---|-------|----------|----------|-----------|
| 1 | Concept | `concept.md`; glossary entries for its terms | User confirms scope, terminology, boundaries | Existing scope and concepts remain unchanged |
| 2 | Domain Model | `model.md` | User confirms entities, invariants, state rules | Applicability criteria in `rules/docs/model.md` require no model |
| 3 | Algorithm | `spec.md` | User confirms correctness and termination | Applicability criteria in `rules/docs/spec.md` When Required and When Not Required require no spec |
| 4 | Design | `design.md` | User confirms structure and responsibility allocation | Existing contracts and responsibilities remain unchanged |
| 5 | Research | `impl.md` | None; agent reports findings | No unresolved external API or implementation question |
| 6 | Plan | task doc `docs/todo/<module>.md` | User confirms task breakdown and order | Existing authorization and task order cover the work |
| 7 | Code | source code | None; agent follows the task doc in order | Never |
| 8 | Verify | passing quality gate | Task doc Quality Gate checklist passes; every domain term in the changed docs has a glossary entry | Never |

- A skipped stage creates no document or approval step; state stage selection briefly in the task context.
- Read the existing docs in the target directory and the earlier owning documents the affected stages need; reuse unchanged decisions and verified evidence. Start at the earliest phase the change affects, and complete it before work that depends on it.
- A stage that introduces a domain term adds its glossary entry under `communication/terminology.md` Established Terms. Research follows `rules/docs/impl.md`. Index updates after a stage adds or renames a file follow `rules/docs/index.md`.
- Update documents under `rules/docs/documentation.md` Updating, and a concept or model change updates the downstream sentences it invalidates before implementation.
- When evidence invalidates an assumption or changes the approach comparison, return to the earliest affected stage and update the owning text before dependent implementation.
- At task completion, `completion` controls creation of summary and README files; an existing-files-only setting applies to those completion artifacts.

## Work Loop

1. Read each sentence the brief quotes at the path and line the brief gives, in that document, and implement every quoted sentence.
   - Intent comes from the design documents; a chain session reads the decision log (`rules/workflow/records.md`) only while it decides under skill `decisions`.
2. Append each finished step to the progress file in the run directory, so a stopped session resumes from its last step.
3. Decide and record each agent-decidable design question under skill `decisions`.
4. Apply `workflow/change-policy.md` Outcome and Scope and, for a defect, Correctness and Verification, using the reference evidence; run a probe when the cause is not established. A necessary repair outside the write set is a boundary question before editing it.
5. For new or changed behavior, write the relevant test before implementation; a behavioral defect requires a failing reproduction under `code/testing.md`. For documentation, formatting or other reversible changes without changed behavior, use applicable checks without creating implementation-mirroring tests.
6. Implement.
7. Run the checks that `integration.test_tiers`, the assigned task mode (skill `multi-agent` Task Modes) and the project gate require; without `integration.test_tiers`, run the full test suite once per revision. Reuse a passing result of an earlier revision, citing its log and revision, when the diff since that revision touches none of the code it exercises; required integration checks remain mandatory. Every run executes each required check instead of inferring its result: a check that failed to start or only compiled is not a behavioral pass, and the report names each check that could not run; a run adds no verification beyond these checks.
   - Before returning a result as finished, run the full project gate with no test filter once, on the merge result: the current integration head merged into the branch in a detached worktree under the run directory, with its submodules initialized, removed afterwards unless the report names its path and the reason it stays. Compare test failures and static-analysis findings with the integration head's recorded baseline. Only when that gate fails, run it on the branch head as well, to tell whether the failure comes from the branch or from the merge. Fix each failure or finding the baseline lacks in this session, or return it as an open item with its cause. The report gives the merge-result gate's counts, the integration head it merged, and the branch-head counts when that gate ran. While iterating, affected tests and the fast tier run as usual; a filtered run never counts as this check.
8. Commit before you return, red work under a `wip:` subject. A pointer bump and its dependent consumer change share one commit.
9. Before the full-gate run of step 7, the chain session applies Self-Check to its scoped diff and fixes each finding, so the gate runs once on the revision it returns. The chain session returns the self-checked diff with its site list to the main agent; for Routine the main agent inspects the diff, and for Full it launches one independent review under skill `multi-agent` Review.
10. When the main agent resumes the session with the chain's next task, the session takes it in the same context, from the input revision and write set the request names. Around compaction, write and reload the progress file under skill `multi-agent` Chains. After the main agent integrates the session's branch, the session starts its next task on a new branch cut from the `integration.branch` head, reads the integration diff its brief carries, and records the new input revision in its progress file.

## Boundary Questions

- Record a user-decidable question, or an edit the task needs outside its write set, in the progress file with its evidence. The main agent writes the point into the owning `design.md` Open Gaps when the question is recorded in the decision log.
- Continue the unblocked items. Return with the open questions when none remains; the main agent answers by resuming this session.

## Self-Check

1. Apply the Review Checklist to your own diff and fix each finding.
2. Send the site list `rules/workflow/change-policy.md` requires with the diff to review.

## Review Checklist

- Report the problems the diff introduces and the violations of the decided sentences its task implements. The reviewer lists a pre-existing problem, a case outside the product's valid inputs, or a request for behavior beyond those sentences in an appendix that never decides the verdict; the main agent adds each appendix item that shares no open task's cause as a row of `docs/todo/<module>.md`, and joins each other item to the open task that shares its cause.
- The reviewer reads each decided sentence at the current `integration.branch` head, never at the branch head. A diff that changes or removes a sentence stating a user decision, without a user directive the brief quotes, is S1.
- Severity: S1 a result the reference output contradicts, a contradiction of a decided document, a crash or a gate failure; S2 a missing test of decided behavior, or a rule violation the diff introduces; S3 wording or style. S1 and S2 need a real input: a file in the repository, a decided sentence, or a valid input of the product's public API. A problem that only a constructed input triggers in a tool that serves only development is S3 and never blocks the merge.
- A finding that occurs only in an implementation an open board row replaces or removes is superseded when the reviewer shows, on the same input, that the replacing implementation gives the correct result. A superseded finding blocks no merge and gets no fix round, unless the diff introduces it; the report marks it superseded and names the replacing row, and the main agent records it there as an acceptance item (the open-gap text to delete, the test that must pass). Without that evidence it keeps its severity.
- Apply `rules/docs/design.md` to maintainability, semantic type boundaries and abstraction, and `rules/communication/terminology.md` to naming. A term in the diff, a document or a report that is neither a glossary term nor a general programming word is a finding.
- Apply `rules/docs/documentation.md` Writing and Updating to each changed document: an ambiguous or contradicting sentence, or text that amends old text beside it instead of rewriting its owning section, is a finding.
- Apply `workflow/change-policy.md` Correctness and Verification to each fix.
- Apply `rules/code/quality.md` API Design: a new engine, index, pass or helper that duplicates an existing relation, phase result, mechanism or sibling idiom is a finding that names the existing one it duplicates, and a new or changed name, signature, result type, error or outcome shape that differs from its sibling interfaces or the glossary is a finding that names the sibling.
- Read each changed call site without its declaration and each changed signature against its readers: a literal whose meaning the call hides, a setting every caller must restate, or a parameter no code reads is a finding under `rules/code/quality.md` API Design.
- An operation that runs inside a loop and traverses a whole collection which that loop does not consume has the bound on how often it runs stated in a code comment of the diff or in its owning `spec.md` Complexity; the reviewer reports each such operation without a stated bound as a finding.
- For each test the diff adds, name the behavior it checks that no existing test checks; a test without one is a finding under `rules/code/testing.md` Maintenance and names the existing test it repeats.
- Report one finding per cause, naming every site of the diff that shares it, and check the author's site list against your own search; a missed site is a finding of that cause.
- The review report ends with reading notes: each file and line range read with the conclusion drawn there, the call chain and reproduction command behind each finding, and each suspicion ruled out with its reason. A fix run reads these notes before opening any other file.
- Give a reproduction for each blocking behavioral finding, and name the regression test each accepted behavior and introduced failure needs; apply the development-tool input boundary in Severity above.
- The reviewer returns FIX-FIRST when the report holds an S1 or S2 finding that is neither superseded nor in the appendix, and MERGE otherwise.
