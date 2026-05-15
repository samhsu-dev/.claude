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

Run the project's configured linter (e.g., `uv run pylint`, `./gradlew detekt`).

- Record all violations on scoped files.
- Ignore pre-existing violations on out-of-scope files.

## Step 3 — Code Smell Scan

Read each scoped file. Check against:

### Structure
- Functions under 20 lines.
- Max 3 parameters per function.
- One responsibility per file. Files under 300 lines.
- Max 2 levels of indentation in function body.

### Smells
- Primitive obsession — raw strings/ints representing domain concepts.
- God objects — class with >7 public methods or >5 fields.
- Feature envy — function accessing another object's fields more than its own.
- Data clumps — fields always passed together not grouped into a type.
- Duplicate logic blocks — two identical blocks not extracted.
- Magic numbers/strings — unnamed constants.
- Middle-man classes that only delegate.
- Speculative generality — abstractions for hypothetical futures.
- Message chains — `a.b().c().d()`.

### Bugs
- Off-by-one in range/slice/index operations.
- Null safety — unchecked nullable returns.
- Resource leaks — opened resources without guaranteed close.
- Mutation during iteration.
- String concatenation with user-controlled input.
- Shared mutable state without synchronization.

### Patch Patterns (reject)
- Band-aid fixes with `HACK`/`FIXME`/`TODO`/`WORKAROUND` comments.
- Shim/adapter layers around code we control.
- Caller-specific branches.
- Redundant deep validation already done at boundary.

## Step 4 — Plan

Output a structured fix plan. Do NOT apply any fix before approval.

```
## Code Update Plan: <scope>

### Linter Violations
- [file:line] <violation> — fix: <what to change>

### Code Smells
- [file:line] <smell type> — fix: <what to change>

### Bug Risks
- [file:line] <risk type> — fix: <what to change>

### Patch Patterns
- [file:line] <pattern> — fix: <what to change>

### Summary
- Files scanned: N
- Linter violations: N
- Code smells: N
- Bug risks: N
- Patch patterns: N
- Total fixes planned: N
```

Wait for user approval before proceeding to Step 5.

## Step 5 — Apply Fixes

For each approved item in the plan:

1. Apply the fix.
2. Run linter on the changed file — verify no new violations.
3. Run tests — verify no regressions.

One logical change at a time. If a fix cascades into other files, report scope expansion before proceeding.

## Step 6 — Verify

1. Run full linter — clean or improved score.
2. Run full test suite — all pass.
3. Run build — compiles clean.

## Step 7 — Report

```
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

- Plan before fix. Never auto-fix without user approval of the plan.
- One smell/violation per fix. Atomic changes.
- Test after every fix. Regression = revert and report.
- Fix root cause. No band-aids.
- Linter-only violations: auto-fixable by formatter do not need individual plan items — batch as "Run formatter".
