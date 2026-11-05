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

- Existing user authorization satisfies an approval within its scope. A skipped stage creates no document or approval step; state stage selection briefly in the task context.
- Read the existing docs in the target directory and the earlier owning documents the affected stages need; reuse unchanged decisions and verified evidence. Start at the earliest phase the change affects, and complete it before work that depends on it.
- A stage that introduces a domain term adds its glossary entry under `communication/terminology.md` Established Terms. Research follows `docs/impl.md`. Index updates after a stage adds or renames a file follow `rules/docs/index.md`.
- Update documents in place, never recreated from scratch. A change rewrites the section that owns the fact, never a note beside it, and a concept or model change updates the downstream sentences it invalidates before implementation.
- When evidence invalidates an assumption or changes the approach comparison, return to the earliest affected stage and update the owning text before dependent implementation.
- At task completion, `completion` controls creation of summary and README files; an existing-files-only setting applies to those completion artifacts.

## Work Loop

1. Read every sentence the brief quotes in its own file, and implement every quoted sentence.
   - Intent comes from the design documents; a chain session never reads the decision log (`rules/workflow/records.md`).
2. Append each finished step to the progress file in the run directory, so a stopped session resumes from its last step.
3. Decide and record each agent-decidable design question under skill `decisions`.
4. Apply `workflow/change-policy.md` Outcome and Scope. For a defect, locate its producing rule, mechanism or data using the reference evidence; run a probe when that cause is not established. A necessary repair outside the write set is a boundary question before editing it.
5. For new or changed behavior, write the relevant test before implementation; a behavioral defect requires a failing reproduction under `code/testing.md`. For documentation, formatting or other reversible changes without changed behavior, use applicable checks without creating implementation-mirroring tests.
6. Implement. A distinct mechanism beside an existing one for the same or a similar problem needs evidence that the problem differs and a rationale in its owning document.
7. Run the affected checks required by the assigned task mode (skill `multi-agent` Task Modes) and project gate. Reuse passing evidence for an unchanged revision; required integration checks remain mandatory. A Sonnet or Haiku run executes each required check instead of inferring its result: a check that failed to start or only compiled is not a behavioral pass, and the report names each check that could not run. An Opus run adds no verification beyond these checks.
   - Before returning a result as finished, run the full project gate with no test filter twice: on the branch head, and on the branch merged with the current integration head in a detached worktree under the run directory, removed afterwards. Compare test failures and static-analysis findings with the integration head's gate. Fix each failure or finding the integration head lacks in this session, or return it as an open item with its cause. The report gives the failure and finding counts of all three gates. A filtered run serves iteration only and never counts as this check.
8. Commit before you return, red work under a `wip:` subject. A pointer bump and its dependent consumer change share one commit.
9. Self-check the scoped diff. Routine returns it to the main agent; Full proceeds to independent review under `multi-agent`.
10. Continue related tasks and fixes in the same context. Around compaction, write and reload the progress record under skill `multi-agent` Chains; after integration, refresh revisions and decisions.

## Boundary Questions

- Record a user-decidable question, or an edit the task needs outside its write set, in the progress file with its evidence. Never record it as an open gap of the code.
- Continue the unblocked items. Return with the open questions when none remains; the main agent answers by resuming this session.

## Self-Check

1. Apply the Review Checklist to your own diff and fix each finding.
2. Send the site list `rules/workflow/change-policy.md` requires with the diff to review.

## Review Checklist

- Report the problems the diff introduces and the violations of the decided sentences its task implements. A pre-existing problem, a case outside the product's valid inputs, or a request for behavior beyond those sentences goes to an appendix, never decides the verdict, and becomes a row of its module's task doc.
- A decided sentence is read at the integration base, never at the branch head. A diff that changes or removes a sentence stating a user decision, without a user directive the brief quotes, is S1.
- Severity: S1 a result the reference output contradicts, a contradiction of a decided document, a crash or a gate failure; S2 a missing test of decided behavior, or a rule violation the diff introduces; S3 wording or style. S1 and S2 need a real input: a file in the repository, a decided sentence, or a valid input of the product's public API. A problem that only a constructed input triggers in a tool that serves only development is S3 and never blocks the merge.
- Apply `rules/docs/design.md` to maintainability, semantic type boundaries and abstraction, and `rules/communication/terminology.md` to naming; domain policy stays outside reusable mechanisms. A term in the diff, a document or a report that is neither a glossary term nor a general programming word is a finding.
- Apply `workflow/change-policy.md` Correctness and Verification to each fix.
- A new engine, index, pass or helper that duplicates an existing relation, phase result, mechanism or sibling idiom is a finding that names what it should reuse.
- New or changed names, signatures, result types, error and outcome shapes follow their sibling interfaces and the glossary; a divergence is a finding that names the sibling.
- Read each changed call site without its declaration and each changed signature against its readers: a literal whose meaning the call hides, a setting every caller must restate, or a parameter no code reads is a finding under `rules/code/quality.md` API Design.
- Report one finding per cause, naming every site of the diff that shares it, and check the author's site list against your own search; a missed site is a finding of that cause.
- Give a reproduction for each blocking behavioral finding. Add regression tests for accepted behavior and introduced failures; apply the development-tool input boundary in Severity above.
- Return MERGE or FIX-FIRST.
