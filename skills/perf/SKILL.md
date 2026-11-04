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

Read `rules/workflow/performance.md` before applying this workflow. Follow `workflow/change-policy.md` Outcome and Scope. Resolve the affected module's task record under `rules/workflow/records.md` once and use that path for every record read/write in this procedure.

## Step 1 — Identify Candidates

Analyze code for optimization opportunities. If the user supplies a target, focus there. Otherwise scan changed files.

Look for:

- Unnecessary allocations (object creation, copies, boxing).
- Inefficient patterns (element-by-element vs bulk, concatenation in loops).
- Redundant operations (dead code, unused intermediates).
- Missing bulk/batch APIs.

Record each candidate:

| Field | Format |
|-------|--------|
| ID | `P<round>-<seq>` (increment from last used round in the resolved module task record) |
| Title | Short description |
| File(s) | Affected source files |
| Hypothesis | What the change does and expected effect |
| Risk | low / medium / high |

## Step 2 — Classify and Prioritize

| Priority | Criteria |
|----------|----------|
| Bug fix | Correctness issue. Apply regardless of perf impact. |
| High | Hot path, measurable allocation removal. |
| Medium | Utility functions, constructors, off-hot-path. |
| Low | Structural improvement, no expected throughput impact. |

Sort: bug fixes first, then high to low. Same priority: lower risk first, smaller diff first.

Present the ranked list. Existing authorization covers candidates within the accepted scope; an expanded scope or an unauthorized constraint tradeoff goes to the user under `workflow/decisions.md`.

## Step 3 — Baseline

Run the project's benchmark suite. Capture fresh numbers.

- Compare an existing baseline with fresh measurements. Investigate a difference that exceeds measured variability and affects the conclusion.
- If no baseline exists, record this as the initial baseline.

### Benchmark Reliability

- 3+ independent runs. Report median.
- Warm-up phase: 3-5 iterations discarded.
- Assess variability and improvement under `rules/workflow/performance.md`; apply configured acceptance thresholds.

## Step 4 — Implement

For each approved candidate, in priority order:

1. One candidate at a time, under `rules/workflow/performance.md`.
2. Minimal change. Keep revertable.
3. Note exact files touched.

## Step 5 — Measure

Run the required benchmark suite and affected checks after each coherent change; retain any project-mandated full suite.

- Compare the target metric and accepted quality and resource constraints against the baseline.
- Check for cross-component regressions.

## Step 6 — Decide

| Target metric | Other metrics | Decision |
|--------------|---------------|----------|
| Improved | Accepted constraints hold | **KEEP** |
| Improved | An accepted constraint regresses | Ask the user unless an existing decision authorizes the tradeoff; otherwise reject |
| No change | No regression | **KEEP** if bug fix, **SKIP** if pure optimization |
| Degraded | Any | **REVERT** |

Report the decision to the user with numbers.

## Step 7 — Document

Update the resolved module task record:

- **KEEP**: Move candidate from Candidates to Completed Optimizations. Update Current Baseline.
- **REVERT**: Move to Evaluated & Rejected. Record result and reason. Revert source files.
- **SKIP**: Move to Evaluated & Rejected with the measured result and reason.
- A candidate dropped before any measurement moves to Evaluated & Rejected with "Not tested" and reason.

After round: update Remaining Bottlenecks and Key Insights.

### Module task record structure

```text
## Current Baseline
## Key Improvements
## Completed Optimizations
## Evaluated & Rejected
## Candidates
## Remaining Known Bottlenecks
## Key Insights
```

## Step 8 — Commit

Commit under `rules/workflow/performance.md`. Use `/commit` skill or stage manually:

- **KEEP**: `perf(<ID>): <title>` — stage source only; keep the module task record uncommitted.
- **REVERT**: revert through a new commit under `workflow/git-safety.md`; record the result in the uncommitted module task record.
