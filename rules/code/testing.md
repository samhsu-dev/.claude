---
paths:
  - "**/*test*"
---

# Testing Standards

Language-specific test framework, layout, assertions, and execution: see project `.claude/rules/code/testing.md`.

## 1. Principles

- Tests prove the presence of defects, not their absence.
- Exhaustive testing is impossible.
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
- Target: >= 90% branch coverage on changed modules. Production source roots named by the project configuration only. Exclude generated code and vendor deps. Report missing lines. Fail CI below threshold.

## 3. Layout
- The test tree mirrors the source tree. The project rule names its root and file-name pattern.
- One test file per component. Split by responsibility past 300 lines.
- Shared fixtures per test directory, in the framework's fixture mechanism.

## 4. Types
- Unit: isolated from external systems. One unit per test file.
- Integration: cross-module or external. Run separately from unit.

## 5. Structure
- Arrange → Act → Assert.
- One behavior per test.
- Name states component, condition, and expected result. The project rule names the pattern.
- Suites/classes only if the framework requires them.

## 5a. File-Level Index Comment
- Every test file starts with a file-level comment listing all test cases and their purpose.
- Format: file description, then one entry per test function with name and one-line verification goal.
- Update the comment when adding, removing, or renaming test functions. The comment is the index — code is the implementation.

## 6. Fixtures & Data
- Reusable setup in fixtures/factories.
- Scenario-specific fixtures per test when needed.
- Temporary resources for file/network/process. Auto-clean after test.
- Test data files in a data directory under the test root. No bulk payloads inline in test files. No test data in the source tree.

## 7. Assertions
- One assertion per test. Multiple only when verifying one behavior.
- Specific assertions (equality, errors, ranges) over boolean checks.
- Negative paths and error conditions asserted explicitly.

## 8. Mocking
- Mock at system boundaries only.
- Dependency injection enables mocking.
- Verified interactions on test doubles.
- No over-mocking. Real behavior for internal collaborators.

## 9. Configuration
- Framework, discovery, markers, strict/fail-fast in repo config.
- Deterministic environment: fixed seeds, stable paths, isolated temp dirs.

## 10. Execution
- Default command: unit tests only. Separate command for integration.
- Parallel execution when supported.
- Concise tracebacks. Stop on first failure for debugging.

## 11. Maintenance
- Tests alongside new/changed code in the same change set.
- Independent tests. No shared mutable state.
- Deduplicate via helpers, fixtures, factories.
