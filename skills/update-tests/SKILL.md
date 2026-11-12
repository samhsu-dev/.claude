---
name: update-tests
description: Audit test coverage against design docs, add missing tests, remove stale tests. Use when the user asks to update, add, or audit tests.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
argument-hint: "[path to source dir/file, or blank for all]"
---
Audit and update tests for source files.

## Core Principle

Read the design docs before any source or test code. Assertions and the classification of a failing test: `rules/code/testing.md` Failures.

## Step 1 — Identify Scope

Determine scope from `$ARGUMENTS`:

| Input | Scope |
|-------|-------|
| No arguments | All source files in the project |
| Directory path | All source files under that directory |
| File path | That single file |
| Module name | Resolve to matching source directory |

Then for the resolved scope:

1. List all source files in scope.
2. List all existing test files: map each source path to its test mirror per project layout.
3. List all design docs: find `docs/**/design.md` for the matching module. If the scope is a subdirectory of a module, walk up to find the nearest `docs/` with design files.

## Step 2 — Read Design Docs First

For each module in scope, read the design documentation before reading any source or test code:

1. `design.md` — class/type specs, function specs, exception types.
2. `model.md` — domain invariants, state transitions, relation semantics.
3. `spec.md` — algorithm steps, loop invariants, edge cases.
4. `impl.md` — API gotchas, library constraints.

Extract a contract list per public function/class:

- Expected behavior (from design.md function specs)
- Input constraints and error conditions
- State transitions and invariants (from model.md)
- Algorithm edge cases (from spec.md)
- API-specific gotchas (from impl.md)

## Step 3 — Coverage Audit

Audit each source file in scope against `rules/code/testing.md`, the project testing rule and the contract list from Step 2. Record each finding with its label:

| Label | Finding | Standard |
|-------|---------|----------|
| **MISSING** | Source file without a test file | `rules/code/testing.md` Layout |
| **MISPLACED** | Test file outside the mirrored path; record current and expected path | `rules/code/testing.md` Layout; project testing rule |
| **FRAGMENTED** | Several test files for one source file not split by responsibility; record the paths to consolidate | `rules/code/testing.md` Layout |
| **OVERSIZED** | Test file over the size limit; record the recommended split by responsibility | `rules/code/testing.md` Layout; `rules/code/organization.md` File Responsibility |
| **UNCOVERED** | Public function or class of the contract list without a test | Step 2 contract list |
| **GAP** | Contract without a test for one category: documented behavior, equivalence class, boundary value, error case, documented exception, `model.md` invariant, `spec.md` edge case | `rules/code/testing.md` Test Design; Step 2 contract list |
| **STALE** | Stale test; record the reason | `rules/code/testing.md` Maintenance and Reproductions |

## Step 4 — Plan

Output a structured plan:

```text
## Test Update Plan: <scope>
### Layout Issues
- MISPLACED: <CurrentPath> → move to <ExpectedPath>
- FRAGMENTED: <Path1>, <Path2> → consolidate into <TargetPath>
- OVERSIZED: <TestFile> (N lines) → split into <File1>, <File2>, ...
### Missing Test Files
- <SourceFile> → create <TestFile>
### Uncovered Public Functions
- <SourceFile:function> → add tests in <TestFile>
### Coverage Gaps
- <TestFile:function> — missing: <categories>
### Stale Tests
- <TestFile:testMethod> — reason: <why stale>
### Summary
- Source files: N
- Test files: N existing, N to create, N to move, N to consolidate
- Public functions: N total, N covered, N uncovered
- Gaps: N
- Stale: N to remove
```

Wait for user approval before proceeding to Step 5.

## Step 5 — Reorganize and Write Tests

Apply the approved plan. Fix layout issues before writing new tests; reorganization moves test files, test methods and fixtures and updates import paths and index comments; it never changes an assertion or the input a test builds.

### Reorganize layout issues

1. **MISPLACED**: Move the test file to the mirrored path. Update imports. Run the moved test class by `integration.test_tiers`.
2. **FRAGMENTED**: Merge the test methods for one source file into the test file at the mirrored path. Deduplicate fixtures. Update the index comment. Delete the empty originals.
3. **OVERSIZED**: Split the test file by responsibility under `rules/code/testing.md` Layout, named by the project testing rule. Move shared fixtures into the framework's fixture mechanism. Write each new file's index comment. Delete the original file.

### New test files and methods

1. Create each new test file at the mirrored path with its index comment (`rules/code/testing.md` File-Level Index Comment).
2. Write each assertion from the function's documented contract, under `rules/code/testing.md` Test Design, Structure, Assertions and Mocking and the project testing rule.

### Remove stale tests

1. Delete the test method. A reproduction test is deleted only under `rules/code/testing.md` Reproductions.
2. Update the index comment.
3. Delete a test file left empty.

## Step 6 — Verify

1. Run the tests skill `chain-session` Work Loop step 7 requires.
2. Classify each failing test under `rules/code/testing.md` Failures. A delegated run reports an implementation defect with the design doc reference to the main agent in its result; the main agent takes it to the user.
3. Run the project linter — no new violations.

## Step 7 — Report

```text
## Test Update Results: <scope>
### Reorganized
- MOVED: <OldPath> → <NewPath>
- CONSOLIDATED: <Path1>, <Path2> → <TargetPath>
- SPLIT: <OversizedFile> → <File1>, <File2>, ...
### Created
- <TestFile> — N tests for <SourceFile>
### Added
- <TestFile:testMethod> — covers <function> <category>
### Removed (stale)
- <TestFile:testMethod> — reason
### Failures (implementation defects)
- <TestFile:testMethod> — expected per design.md: X, actual: Y
  Design ref: <doc file and section>
### Verification
- tests: all pass / N failures (reported as implementation defects)
- linter: clean / N violations
```
