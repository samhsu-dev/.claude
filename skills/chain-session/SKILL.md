---
name: chain-session
description: Carry one task chain to merge-ready in its own worktree, or review a finished diff. Use when a brief makes you a chain session or a reviewer, or before an author's self-check.
---

Carry one task chain from reading to merge-ready in its own worktree, or review its finished diff. Hard limits: `rules/workflow/multi-agent.md`.

## Work Loop

1. Read every sentence the brief quotes in its own file, and implement every quoted sentence.
2. Append each finished step to the progress file in the run directory, so a stopped session resumes from its last step.
3. Decide and record each agent-decidable design question under skill `decisions`.
4. Apply `workflow/change-policy.md` Outcome and Scope. For a defect, locate its producing rule, mechanism or data using the reference evidence; run a probe when that cause is not established. A necessary repair outside the write set is a boundary question before editing it.
5. For new or changed behavior, write the relevant test before implementation; a behavioral defect requires a failing reproduction under `code/testing.md`. For documentation, formatting or other reversible changes without changed behavior, use applicable checks without creating implementation-mirroring tests.
6. Implement. A distinct mechanism beside an existing one for the same or a similar problem needs evidence that the problem differs and a rationale in its owning document.
7. Run the affected checks required by the assigned task mode and project gate. Reuse passing evidence for an unchanged revision; required integration checks remain mandatory.
8. Commit before you return, red work under a `wip:` subject. A pointer bump and its dependent consumer change share one commit.
9. Self-check the scoped diff. Routine returns it to the main agent; Full proceeds to independent review under `multi-agent`.
10. Continue related tasks and fixes in the same context; refresh revisions and decisions after compaction or integration.

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
- Apply `rules/docs/design.md` to maintainability, semantic type boundaries and abstraction, and `rules/communication/terminology.md` to naming; domain policy stays outside reusable mechanisms.
- Apply `workflow/change-policy.md` Correctness and Verification to each fix.
- A new engine, index, pass or helper that duplicates an existing relation, phase result, mechanism or sibling idiom is a finding that names what it should reuse.
- New or changed names, signatures, result types, error and outcome shapes follow their sibling interfaces and the glossary; a divergence is a finding that names the sibling.
- Read each changed call site without its declaration and each changed signature against its readers: a literal whose meaning the call hides, a setting every caller must restate, or a parameter no code reads is a finding under `rules/code/quality.md` API Design.
- Report one finding per cause, naming every site of the diff that shares it, and check the author's site list against your own search; a missed site is a finding of that cause.
- Give a reproduction for each blocking behavioral finding. Add regression tests for accepted behavior and introduced failures; apply the development-tool input boundary in Severity above.
- Return MERGE or FIX-FIRST.
