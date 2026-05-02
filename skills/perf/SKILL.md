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

Run the 8-step performance optimization pipeline. All state tracked in `docs/performance.md`.

## Step 1 — Identify Candidates

Analyze code for optimization opportunities. If `$ARGUMENTS` specifies a target, focus there. Otherwise scan changed files.

Look for:
- Unnecessary allocations (object creation, copies, boxing).
- Inefficient patterns (element-by-element vs bulk, concatenation in loops).
- Redundant operations (dead code, unused intermediates).
- Missing bulk/batch APIs.

Record each candidate:

| Field | Format |
|-------|--------|
| ID | `P<round>-<seq>` (increment from last used round in `docs/performance.md`) |
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

Present the ranked list to the user. Wait for approval before proceeding.

## Step 3 — Baseline

Run the project's benchmark suite. Capture fresh numbers.

- If `docs/performance.md` has a recorded baseline, compare. Differ >5% → update and investigate before proceeding.
- If no baseline exists, record this as the initial baseline.

### Benchmark Reliability

- 3+ independent runs. Report median.
- Warm-up phase: 3-5 iterations discarded.
- < 3% variation is noise. > 5% is meaningful.

## Step 4 — Implement

For each approved candidate, in priority order:

1. One candidate at a time. No combining with refactors or cleanups.
2. Minimal change. Keep revertable.
3. Note exact files touched.

## Step 5 — Measure

Run full benchmark suite after each change.

- Compare **all** metrics against previous state, not just the targeted metric.
- Check for cross-component regressions.

## Step 6 — Decide

| Target metric | Other metrics | Decision |
|--------------|---------------|----------|
| Improved | No regression (< -3%) | **KEEP** |
| Improved | Minor regression (3-10%) non-critical | **KEEP with note** |
| Improved | Regression (> 10%) anywhere | **REVERT** |
| No change | No regression | **KEEP** if bug fix, **SKIP** if pure optimization |
| Degraded | Any | **REVERT** |

Report the decision to the user with numbers.

## Step 7 — Document

Update `docs/performance.md`:

- **KEEP**: Move candidate from Candidates to Completed Optimizations. Update Current Baseline.
- **REVERT**: Move to Evaluated & Rejected. Record result and reason. Revert source files.
- **SKIP**: Move to Evaluated & Rejected with "Not tested" and reason.

After round: update Remaining Bottlenecks and Key Insights.

### `docs/performance.md` Structure

```
## Current Baseline
## Key Improvements
## Completed Optimizations
## Evaluated & Rejected
## Candidates
## Remaining Known Bottlenecks
## Key Insights
```

## Step 8 — Commit

One optimization per commit. Use `/commit` skill or stage manually:

- **KEEP**: `perf(<ID>): <title>` — stage source + `docs/performance.md`.
- **REVERT**: revert source, stage `docs/performance.md`, `perf(<ID>): reject — <reason>`.

## Safety

- Never combine optimization with unrelated changes.
- Never skip measurement.
- Never keep an optimization that causes >10% regression anywhere.
- All decisions require user approval.
