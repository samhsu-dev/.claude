---
name: update-codes
description: Audit code against quality standards, plan fixes, and apply them after approval. Use when the user asks to update, fix, or improve code quality.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
argument-hint: "[optional file or scope to focus on]"
---

Audit code against quality standards, produce a fix plan, and apply fixes after user approval.

## Step 1 — Identify Scope

Determine scope from `$ARGUMENTS`:

| Input | Scope |
|-------|-------|
| No arguments | All changed files (`git diff --name-only` + `git diff --cached --name-only`) |
| Directory path | All source files under that directory |
| File path | That single file |

List all source files in scope.

## Step 2 — Static Analysis

Run the linter the language profile names.

- Record all violations on scoped files.
- Ignore pre-existing violations on out-of-scope files.

## Step 3 — Code Smell Scan

Read each scoped file. Audit it against every requirement of these rule files, including their exceptions and the active language profile's named replacements, and record each violation under the plan category in parentheses:

- `rules/code/quality.md` Control Flow, Code Structure and `rules/code/organization.md` File Responsibility (Code Smells).
- `rules/code/quality.md` Code Smells, No Stale Code, Documentation, Type Safety, Agent Maintainability and API Design (Code Smells).
- `rules/code/quality.md` Error Handling, Bug Prevention, Resource Management and Input Contract & Invariants (Bug Risks).
- `rules/code/logging.md` (Logging).
- `rules/code/organization.md` File Naming, Directory Organization and Entry Points (Naming & Organization).
- `rules/code/quality.md` No Patch-Style Code and `rules/workflow/change-policy.md` Correctness and Verification (Patch Patterns).

## Step 4 — Plan

Output a structured fix plan.

```text
## Code Update Plan: <scope>

### Linter Violations
- [file:line] <violation> — fix: <what to change>

### Code Smells
- [file:line] <smell type> — fix: <what to change>

### Bug Risks
- [file:line] <risk type> — fix: <what to change>

### Logging
- [file:line] <violation> — fix: <what to change>

### Naming & Organization
- [file or path] <violation> — fix: <what to change>

### Patch Patterns
- [file:line] <pattern> — fix: <what to change>

### Summary
- Files scanned: N
- Linter violations: N
- Code smells: N
- Bug risks: N
- Logging: N
- Naming & organization: N
- Patch patterns: N
- Total fixes planned: N
```

Wait for user approval before proceeding to Step 5.

## Step 5 — Apply Fixes

For each approved item in the plan:

1. Apply the fix.
2. Run linter on the changed file — verify no new violations.
3. Run the tests skill `chain-session` Work Loop step 7 requires.

One cause at a time. A repair outside the task's scope is reported to the user before it is made.

## Step 6 — Verify

1. Run full linter — clean or improved score.
2. Run build — compiles clean.

## Step 7 — Report

```text
## Code Update Results: <scope>

### Fixed
- [file:line] <what was fixed>

### Skipped (user declined or out of scope)
- [file:line] <description>

### Verification
- linter: clean / score
- tests: all pass / N failures
- build: clean / errors
```

## Rules

- One cause per fix, covering every site that shares it (`rules/workflow/change-policy.md` Correctness and Verification).
- Test after every fix. A regression is reverted and reported: revert a committed change with a new revert commit and an uncommitted change by inspecting `git diff` and editing the files back (skill `commit`).
- Linter-only violations: auto-fixable by formatter do not need individual plan items — batch as "Run formatter".
