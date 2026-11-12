---
paths:
  - "**/*test*"
  - "**/*Test*"
---

# Testing Standards

Language-specific test framework, layout, assertions, and execution: see project `.claude/rules/code/testing.md`.

## 1. Principles

- Concentrate tests on high-risk and high-change areas.

## 2. Test Design

### Black-box (specification-based)

- **Equivalence partitioning**: divide input domain into classes where all values produce equivalent behavior. One test per class.
- **Boundary value analysis**: test at edges of each partition — minimum, minimum−1, maximum, maximum+1.
- **Error cases**: invalid inputs, empty inputs, null/None, out-of-range, wrong type.

### Coverage targets

- **Branch coverage**: every true/false path taken.
- Target: >= 90% branch coverage over each package the change touches. Production source roots named by the project configuration only. Exclude generated code and vendor deps. Report missing lines. Fail CI below threshold.

## 3. Layout

- The test tree mirrors the source tree. The project rule names its root and file-name pattern.
- One test file per component. A test file over the `code/organization.md` size limit splits by the component's responsibilities, one responsibility per file; together those files are the component's test file.
- Shared fixtures per test directory, in the framework's fixture mechanism.

## 4. Types

- Unit: isolated from external systems.
- Integration: cross-module or external.
- Growth: when the project configures `algorithm.phases`, each function that runs one phase to completion (its driver) and each worklist loop inside such a function has a growth test. The test runs the size sweep of `workflow/performance.md` Localization and records, at each size, the work counters and the elapsed time; the counters decide the growth order, and a test whose counters grow faster than the bound its owning `spec.md` Complexity states fails.

## 5. Structure

- Arrange → Act → Assert.
- One behavior per test.
- Name states component, condition, and expected result. The project rule names the pattern.
- Suites/classes only if the framework requires them.

## 5a. File-Level Index Comment

- Every test file starts with a file-level comment listing all test cases and their purpose.
- Format: file description, then one entry per test function with name and one-line verification goal.
- Update the comment when adding, removing, or renaming test functions.

## 6. Fixtures & Data

- Scenario-specific fixtures per test when needed.
- Temporary resources for file/network/process. Auto-clean after test.
- A hand-written input that a test passes to the product as source text is a file in a data directory under the test root, in a directory named after the tested behavior; the file states its expected result. An input a test generates stays in test code.
- No bulk payloads inline in test files. No test data in the source tree.

## 7. Assertions

- Specific assertions (equality, errors, ranges); never boolean checks.
- Negative paths and error conditions asserted explicitly.

## 8. Mocking

- Mock at system boundaries only.
- A test that uses a mock at a system boundary verifies each call to it that the behavior under test requires; a stub that only returns data is not verified.

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
- Before adding a test, search the component's tests and test data for a test of the same behavior. A new input that differs from an existing test's input only by names, by literals the code under test does not branch on, or by a construct the code under test handles on the same branch is added to that test as a named case; no new test is created.
- Two existing tests that meet that condition are merged into one test, each input kept as a named case.
- A test is stale when it covers a function or behavior the current design documents no longer state, tests private methods or internal state instead of a public contract, or repeats another test's input and assertion. A stale test is deleted; a reproduction test follows Reproductions.

## Reproductions

- Before repairing a defect, write a reproduction test that fails on the unfixed implementation.
- Keep reproduction tests permanently. Exception: a reproduction whose contract the owning design document removed is deleted with that contract, and the deletion names the document change.

## Failures

- Assertions come from the documented contract, never from observed behavior.
- A failing test is first checked against the accepted contract in the owning design document. A test that contradicts the contract is a test defect and is corrected to the contract; a test that matches it reports an implementation defect.
