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

Audit and update tests for source files. Tests are derived from design documents, never from reading implementation code.

## Core Principle

Tests verify documented contracts. A failing test means a bug in the code, not a test error. Never modify a test to match current code behavior — if the code deviates from the design doc, that is a bug to report.

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

For each module in scope, read the design documentation **before** reading any source or test code:

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

For each source file, check:

### 3a. Test file layout conformance
- Every source file has exactly one corresponding test file (or split group). 1:1 mapping.
- Test file path mirrors source path: `src/a/b/foo.py` → `tests/a/b/test_foo.py`.
- Missing test file → record as **MISSING**.
- Test file exists but at wrong path (does not mirror source) → record as **MISPLACED** with current and expected path.
- Multiple test files covering the same source file without clear responsibility split → record as **FRAGMENTED** with paths to consolidate.
- Test file exceeds 300 lines → record as **OVERSIZED** with recommended split by responsibility.

#### Splitting oversized test files

When a test file exceeds 300 lines, split by responsibility area of the source file:

| Source | Split test files |
|--------|-----------------|
| `src/a/parser.py` | `tests/a/test_parser_tokenize.py`, `tests/a/test_parser_ast.py` |
| `src/a/auth.py` | `tests/a/test_auth_login.py`, `tests/a/test_auth_permissions.py` |

Naming: `test_<source_name>_<responsibility>.<ext>`.

Split rules:
- Each split file tests one responsibility area of the source file.
- Responsibility areas come from classes, logical groups of functions, or design.md sections.
- Shared fixtures extracted to a `conftest.py` (or equivalent) in the same test directory.
- Every split file has its own docstring index.

### 3b. Public function coverage
- Every public function in the source has at least one test.
- Match by function name in test method names.
- Untested public function → record as **UNCOVERED**.

### 3c. Contract coverage per function
For each public function, verify tests cover:

| Category | What to check |
|----------|--------------|
| Happy path | Normal input → expected output per design.md |
| Equivalence classes | One test per input partition |
| Boundary values | min, min-1, max, max+1 for each range |
| Error cases | Invalid input, empty input, null (if nullable), out-of-range, wrong type |
| Exceptions | Each documented exception type triggers correctly |
| Invariants | State invariants from model.md hold after operation |
| Edge cases | Degenerate inputs from spec.md |

Missing category → record as **GAP** with the specific category.

### 3d. Stale test detection
A test is stale when:
- It tests a function that no longer exists in source.
- It tests behavior contradicted by current design docs.
- It tests internal implementation details (private methods, internal state) rather than public contracts.
- It duplicates another test (same input, same assertion, different name).

Stale test → record as **STALE** with reason.

## Step 4 — Plan

Output a structured plan before writing any code:

```
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

For each item in the approved plan:

### Reorganize layout issues (before writing new tests)
1. **MISPLACED**: Move test file to the correct mirror path. Update imports. Run tests to confirm no breakage.
2. **FRAGMENTED**: Merge all test methods for the same source file into one test file at the correct path. Deduplicate fixtures. Update file-level docstring. Delete empty originals.
3. **OVERSIZED**: Split test file by responsibility into `test_<source>_<responsibility>.<ext>` files. Extract shared fixtures to `conftest.py` (or equivalent). Update docstrings in each new file. Delete the original oversized file.
4. Preserve all existing test logic during reorganization. No test deletion or modification beyond import paths and file moves.

### New test files
1. Create test file at the correct mirror path.
2. Add file-level docstring listing all test cases and their purpose.
3. Use project fixture conventions for shared setup.

### New test methods
1. Read design doc for the function's contract (behavior, input, output, errors).
2. Write test assertions based on the documented contract — not current code behavior.
3. One behavior per test. Arrange → Act → Assert.
4. Name per project convention (e.g., `test_<component>_<condition>_<expected>`).
5. Parameterized tests for equivalence partitioning and boundary analysis.
6. Error cases: assert expected exception type for each documented error condition.

### Remove stale tests
1. Delete the test method.
2. Update the file-level docstring.
3. If the test file becomes empty, delete the file.

## Step 6 — Verify

1. Run project test command — all pass.
2. If a new test fails: this is likely a bug in the source code, not a test error. Report it to the user with the design doc reference. Do not modify the test to match current behavior.
3. Run project linter — no new violations.

## Step 7 — Report

```
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

### Failures (potential bugs)
- <TestFile:testMethod> — expected per design.md: X, actual: Y
  Design ref: <doc file and section>

### Verification
- tests: all pass / N failures (reported as potential bugs)
- linter: clean / N violations
```

## Rules

- Read design docs before source code. Always.
- Test assertions come from documented contracts, not observed behavior.
- A failing test is a bug report, not a test error. Never weaken a test to pass.
- One behavior per test. No multi-assertion tests unless verifying one composite behavior.
- Mock at system boundaries only. Real objects for internal collaborators.
- No test inheritance. Plain classes with annotated methods.
- Fresh objects per test. No shared mutable state.
- Parameterized tests for partitioning and boundary analysis.
- Every test file has a docstring index of its test cases.
- 1:1 source-to-test mapping. One source file = one test file at the mirrored path.
- Reorganize before writing. Fix layout issues (misplaced, fragmented) before adding new tests.
- Reorganization preserves all existing test logic. No accidental test deletion during moves.
