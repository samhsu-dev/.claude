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

Investigate and fix a bug. Never guess. Never patch symptoms.

## Step 1 — Understand the Failure

Gather information from `$ARGUMENTS` and conversation context:

1. Read the full exception chain / error output. Identify the origin, not just the surface message.
2. Check the exception type and its fields, not just the message string.
3. If a test fails, read the test first — verify the test is correct before suspecting the implementation.

## Step 2 — Reproduce

Write a minimal failing test that triggers the reported behavior.

- Locate the correct test file (mirror source layout).
- Name: `` `should <expected behavior> when <condition>` `` or `test_<component>_<condition>_<expected>`.
- One assertion targeting the exact failure.

Run the test. Confirm it fails.

- If the test passes, the bug does not exist as described. Report back to the user. Stop.

## Step 3 — Narrow Scope

Isolate whether the fault is in input, logic, or external dependency:

1. Check inputs at the function boundary — are they what the code expects?
2. Check assumptions with assertions or targeted logging at boundaries, not in the middle.
3. If an external call fails, verify the input matches the API contract (check `impl.md` if it exists).
4. No guessing. If the cause is unclear, add a targeted assertion or log to confirm before changing code.

### Common Pitfalls (Kotlin)

Check these first when applicable:
- Empty `catch` blocks swallowing exceptions.
- Missing `cause` parameter: `throw DomainException("msg", cause = e)`.
- `lateinit` access before initialization.
- Platform type nullability: Java methods returning null assigned to non-null Kotlin types.
- `!!` on untrusted data.
- Coroutine cancellation swallowed by `catch (e: Exception)`.

## Step 4 — Fix

1. Fix the root cause. One change addressing one fault.
2. Run the reproduction test. Confirm it passes.
3. Run the full test suite. Confirm no regressions.

If the fix requires changes beyond the immediate fault:
- Report the scope to the user before proceeding.

## Step 5 — Verify

1. Run `./gradlew test` (or project test command) — all pass.
2. Run `./gradlew detekt` (or project linter) — no new violations.
3. Run `./gradlew build` (or project build command) — compiles clean.

## Step 6 — Preserve the Test

The reproduction test is a permanent regression guard. Never delete it after the fix.

- Ensure it follows project test conventions (layout, naming, assertions).
- Add a file-level docstring entry if the test file uses them.

## Report

Output a summary:

```
## Bug Fix

**Symptom**: <what was observed>
**Root cause**: <what was wrong and why>
**Fix**: <what changed>
**Test**: <test name and file>
**Verification**: tests pass / detekt clean / build clean
```

## Rules

- Never change implementation code before having a failing reproduction test.
- Never delete a bug-reproduction test after the fix.
- Never patch symptoms. Fix root cause.
- No silent fallbacks. Internal `map[key] ?: default` masks bugs — throw on missing key.
- No guessing. Every hypothesis verified before acting.
