---
name: chain-session
description: Carry one task chain to merge-ready in its own worktree, or review a finished diff. Use when a brief makes you a chain session or a reviewer, or before an author's self-check.
---

Carry one task chain from reading to merge-ready in its own worktree, or review its finished diff. Hard limits: `rules/workflow/multi-agent.md`.

## Work Loop

1. Read every sentence the brief quotes in its own file, and implement every quoted sentence.
2. Append each finished step to the progress file in the run directory, so a stopped session resumes from its last step.
3. Decide and record each agent-decidable design question under skill `decisions`.
4. Write the test first.
5. Implement. A distinct mechanism beside an existing one for the same or a similar problem needs evidence that the problem differs and a rationale in its owning document.
6. Before each commit, run the task quality gate on the written files: tests, lint and the documentation check.
7. Commit before you return, red work under a `wip:` subject. A pointer bump and its dependent consumer change share one commit.
8. Before review, run the Self-Check.
9. Take every fix round in the same session.

## Boundary Questions

- Record a user-decidable question, or an edit the task needs outside its write set, in the progress file with its evidence. Never record it as an open gap of the code.
- Continue the unblocked items. Return with the open questions when none remains; the main agent answers by resuming this session.

## Self-Check

1. Apply the Review Checklist to your own diff and fix each finding.
2. Send the site list `rules/workflow/change-policy.md` requires with the diff to review.

## Review Checklist

- Report the problems the diff introduces and the violations of the decided sentences its task implements. A pre-existing problem, a case outside the valid inputs, or a request for behavior beyond those sentences goes to an appendix, never decides the verdict, and becomes a row of its module's task doc.
- Severity: S1 a result the reference output contradicts, a contradiction of a decided document, a crash or a gate failure; S2 a missing test of decided behavior, or a rule violation the diff introduces; S3 wording or style.
- Apply `rules/docs/design.md` to maintainability, semantic type boundaries and abstraction, and `rules/communication/terminology.md` to naming; domain policy stays outside reusable mechanisms.
- Report one finding per cause, naming every site of the diff that shares it, and check the author's site list against your own search; a missed site is a finding of that cause.
- Write each edge case as a reproduction the chain session adds as a test.
- Return MERGE or FIX-FIRST.
