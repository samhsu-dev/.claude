---
name: review-code
description: Run quality review on current code changes — detekt, tests, build, code smell scan. Use when the user asks to review or verify code.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
argument-hint: "[optional file or scope to focus on]"
---

Review all pending changes in the current session for quality, correctness, and safety.

## Step 1 — Identify Changed Files

Run in parallel:

1. `git diff --name-only` — unstaged changes.
2. `git diff --cached --name-only` — staged changes.
3. `git diff HEAD --name-only` — all changes vs last commit.

Merge into a deduplicated list. If `$ARGUMENTS` specifies a scope, filter to matching files.

## Step 2 — Static Analysis

Run `./gradlew detekt` (or the project's configured linter).

- Record all violations on changed files.
- Ignore pre-existing violations on unchanged files.

## Step 3 — Tests

Run `./gradlew test` (or the project's configured test command).

- All tests pass. Any failure is a blocking finding.

## Step 4 — Build

Run `./gradlew build` (or the project's configured build command).

- Clean compilation. Any error is a blocking finding.

## Step 5 — Code Smell Scan

Read each changed file. For each, check:

### Structure
- Functions under 20 lines (60 for Kotlin per detekt).
- Max 3 parameters (5 for Kotlin, 6 for constructors).
- One responsibility per file. Files under 300 lines (600 for Kotlin).
- Max 2 levels of indentation in function body (4 for Kotlin).

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

## Step 6 — Report

Output a structured report:

```
## Review Results

### Blocking
- [file:line] description

### Warnings
- [file:line] description

### Passed
- detekt: clean / N violations
- tests: all pass / N failures
- build: clean / errors
- smell scan: clean / N findings
```

If blocking findings exist, list fixes. Do not auto-fix without user approval.
