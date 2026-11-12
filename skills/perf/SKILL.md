---
name: perf
description: Run the measurement-driven performance optimization pipeline. Use when the user asks to optimize, benchmark, or profile.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
argument-hint: "[optional target file, function, or optimization ID]"
---

Read `rules/workflow/performance.md` before applying this workflow. Follow `workflow/change-policy.md` Outcome and Scope. Resolve the affected module's task doc `docs/todo/<module>.md` once and use that path for every record read and write in this procedure.

## Step 1 — Localize Candidates

If the user supplies a target, localize there. Otherwise use the project's profiling samples and counters (project value `performance`). Run, under `rules/workflow/performance.md` Localization and with the tools the language profile names:

1. Growth order: a work-counter size sweep with the target workload fixed.
2. Hot paths: a sampling profile of a fixed sample.
3. Cost class: CPU, allocation/GC or waiting.

Record each candidate that has profile or counter evidence:

| Field | Format |
|-------|--------|
| ID | `P<round>-<seq>` (increment from last used round in the resolved module task doc) |
| Title | Short description |
| Evidence | Counter sweep or profile result, with the cost class |
| File(s) | Affected source files |
| Hypothesis | What the change does and expected effect |
| Risk | high when the change alters a contract or a shared mechanism, medium when it changes behavior inside one component, low otherwise |

## Step 2 — Classify and Prioritize

| Priority | Criteria |
|----------|----------|
| Bug fix | Correctness issue. Apply regardless of perf impact. |
| High | A candidate on a profiled hot path or with a measured growth order, of any kind. |
| Medium | A utility function or constructor off the hot path. |
| Low | Structural improvement, no expected throughput impact. |

Sort: bug fixes first, then high to low. Same priority: algorithm and data structure before implementation overhead before runtime tuning (`rules/workflow/performance.md` Fix Order), then lower risk, then smaller diff.

Present the ranked list. An expanded scope or an unauthorized constraint tradeoff goes to the user under `workflow/decisions.md`.

## Step 3 — Baseline

Run the project's benchmark suite and the Step 1 counters. Capture fresh numbers.

- Compare an existing baseline with fresh measurements. Investigate a difference that exceeds measured variability and affects the conclusion.
- If no baseline exists, record this as the initial baseline.

### Benchmark Reliability

- 3+ independent runs. Report median.
- Warm-up phase: 3-5 iterations discarded.
- Assess variability and improvement under `rules/workflow/performance.md`; apply configured acceptance thresholds.

## Step 4 — Implement

For each approved candidate, in priority order:

1. One candidate at a time, under `rules/workflow/performance.md`.
2. Edit only the files the candidate's File(s) field names, and commit the candidate as its own commit.
3. Note exact files touched.

## Step 5 — Measure

Run the required benchmark suite and affected checks after each candidate's change; retain any project-mandated full suite.

- Compare the target metric and accepted quality and resource constraints against the baseline.
- Run the tests and benchmarks of each component that calls the changed code and compare them with the baseline; a worse result is a regression in Step 6.

## Step 6 — Decide

| Target metric | Other metrics | Decision |
|--------------|---------------|----------|
| Improved | Accepted constraints hold | **KEEP** |
| Improved | An accepted constraint regresses | **KEEP** when an existing decision authorizes the tradeoff; otherwise ask the user |
| No change | No regression | **KEEP** if bug fix, **SKIP** if pure optimization |
| Degraded | Any | **REVERT** |

Revert a committed change with a new revert commit and an uncommitted change by inspecting `git diff` and editing the files back (skill `commit`).

Report the decision to the user with numbers.

## Step 7 — Document

Update the resolved module task doc:

- **KEEP**: delete the candidate from Candidates and update Current Baseline.
- **REVERT**, **SKIP**, or dropped before measurement: delete the candidate and add its measured result (or "Not tested") and reason to Key Insights.

After each round, update Remaining Known Bottlenecks and Key Insights.

### Module task record structure

```text
## Current Baseline
## Candidates
## Remaining Known Bottlenecks
## Key Insights
```

## Step 8 — Commit

Commit under `rules/workflow/performance.md`. Use `/commit` skill or stage manually:

- **KEEP**: `perf(<ID>): <title>` — stage source only; keep the module task doc uncommitted.
- **REVERT**: revert through a new commit; record the result in the uncommitted module task doc.
