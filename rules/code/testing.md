---
paths:
  - "**/*test*"
---

# Testing Standards

Language-specific test framework, layout, assertions, and execution: see project `.claude/rules/code/testing.md`.

## 1. Principles

- Tests prove the presence of defects, not their absence.
- Exhaustive testing is impossible. Select inputs via equivalence partitioning and boundary analysis.
- Defects cluster. Concentrate tests on high-risk and high-change areas.
- Same tests stop finding new defects over time (pesticide paradox). Update tests as code evolves.

## 2. Test Design

### Black-box (specification-based)
- **Equivalence partitioning**: divide input domain into classes where all values produce equivalent behavior. One test per class.
- **Boundary value analysis**: test at edges of each partition — minimum, minimum−1, maximum, maximum+1. Boundaries are the most common fault locations.
- **Error cases**: invalid inputs, empty inputs, null/None, out-of-range, wrong type.

### Coverage targets
- **Statement coverage**: every line executed.
- **Branch coverage**: every true/false path taken.
- Target: >= 90% branch coverage on changed modules. `src` only. Exclude generated code and vendor deps. Report missing lines. Fail CI below threshold.

## 3. Layout
- One layout profile repo-wide.
- Profile A: `tests/` root; `<component>.test.<ext>`
- Profile B: `tests/` root; `test_<component>.<ext>`
- Profile C: co-located near source; `*_test.<ext>`
- Profile D: `src/test/<lang>/`; mirror packages
- Profile E: inline unit in source; integration in `tests/`

## 4. Types
- Unit: isolated from external systems. One unit per test file.
- Integration: cross-module or external. Run separately from unit.

## 5. Structure
- Arrange → Act → Assert.
- One behavior per test.
- Name: `test_<component>_<condition>_<expected>`.
- Suites/classes only if the framework requires them.

## 5a. File-Level Docstring
- Every test file starts with a module docstring listing all test cases and their purpose.
- Format: file description, then one entry per test function with name and one-line verification goal.
- Update the docstring when adding, removing, or renaming test functions. Docstring is the index — code is the implementation.

## 6. Naming & Location
- Mirror source layout under the selected profile.
- `test_<component>.<ext>` | `<component>.test.<ext>` | `*_test.<ext>`.

## 7. Fixtures & Data
- Reusable setup in fixtures/factories.
- Scenario-specific fixtures per test when needed.
- Temporary resources for file/network/process. Auto-clean after test.

## 8. Assertions
- One assertion per test. Multiple only when verifying one behavior.
- Specific assertions (equality, errors, ranges) over boolean checks.
- Negative paths and error conditions asserted explicitly.

## 9. Mocking
- Mock at system boundaries only.
- Dependency injection enables mocking.
- Verified interactions on test doubles.
- No over-mocking. Real behavior for internal collaborators.

## 10. Configuration
- Framework, discovery, markers, strict/fail-fast in repo config.
- Deterministic environment: fixed seeds, stable paths, isolated temp dirs.

## 11. Execution
- Default command: unit tests only. Separate command for integration.
- Parallel execution when supported.
- Concise tracebacks. Stop on first failure for debugging.

## 12. Maintenance
- Tests alongside new/changed code in the same change set.
- Independent tests. No shared mutable state.
- Deduplicate via helpers, fixtures, factories.
