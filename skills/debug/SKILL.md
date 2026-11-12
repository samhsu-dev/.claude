---
name: debug
description: Investigate and fix a bug using the reproduce-first protocol. Use when the user reports a bug, test failure, or unexpected behavior.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
argument-hint: "[error message, test name, or symptom description]"
---

Investigate and fix a bug under `rules/workflow/change-policy.md` Correctness and Verification.

## Step 1 — Understand the Failure

Gather information from `$ARGUMENTS` and conversation context:

1. Read the full exception chain / error output. Identify the origin, not just the surface message.
2. Check the exception type and its fields, not just the message string.
3. If a test fails, read the test first and classify the failure under `rules/code/testing.md` Failures before suspecting the implementation.

## Step 2 — Reproduce

Write a minimal failing test that triggers the reported behavior.

- Place and name it under `rules/code/testing.md` §3 Layout and §5 Structure and the project testing rule.
- One assertion targeting the exact failure.

Run the test. Confirm it fails.

- If the test passes, the bug does not exist as described. A delegated run reports this to the main agent in its result and stops; the main agent takes it to the user.

## Step 3 — Narrow Scope

Isolate whether the fault is in input, logic, or external dependency:

1. Check inputs at the function boundary — are they what the code expects?
2. Check assumptions with assertions or targeted logging at boundaries, not in the middle.
3. If an external call fails, verify the input matches the API contract (check `impl.md` if it exists).
4. If the cause is unclear, confirm it with a targeted assertion or log before changing code.

### Common Pitfalls

Check these first:

- Empty catch/except blocks swallowing exceptions.
- Missing error chaining (original cause lost when re-raising).
- Uninitialized state accessed before setup completes.
- Null/None returned from external calls assigned to non-nullable variables.
- Unchecked assertions on untrusted data.
- Concurrency errors swallowed by broad exception handlers.

## Step 4 — Fix

1. Fix the root cause. One change addressing one fault and its other instances (`rules/workflow/change-policy.md` Correctness and Verification).
2. Run the reproduction test. Confirm it passes.
3. Run the tests skill `chain-session` Work Loop step 7 requires.

A repair outside the task's scope is reported to the user before it is made.

## Step 5 — Verify

1. Run project linter — no new violations.
2. Run project build — compiles clean.

## Step 6 — Preserve the Test

Keep the reproduction test under `rules/code/testing.md` Reproductions, in the layout, naming and index comment of `rules/code/testing.md` and the project testing rule.

## Step 7 — Commit

Commit the fix and its reproduction test together, before returning to other work.

- One `fix(scope):` commit carrying the root-cause change plus the regression test — they are one concept.
- Commit now, under `rules/workflow/committing.md` Staging.
- Stage and commit under skill `commit`.

## Report

Output a summary:

```text
## Bug Fix

**Symptom**: <what was observed>
**Root cause**: <what was wrong and why>
**Fix**: <what changed>
**Test**: <test name and file>
**Verification**: tests pass / linter clean / build clean
```

## Rules

- Failure handling and missing required values: `rules/code/quality.md` Error Handling.
