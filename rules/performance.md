---
paths:
  - "**/performance.md"
  - "**/*Performance*"
  - "**/*Benchmark*"
---

# Performance Optimization Pipeline

Measurement-driven, incremental optimization. One candidate at a time. All state tracked in `docs/performance.md`.

## Pipeline

```
Identify → Classify → Baseline → Implement → Measure → Decide → Document → Commit
    ↑                                                                  |
    └──────────────────────────────────────────────────────────────────┘
```

### 1. Identify

Find candidates through code analysis:
- Unnecessary allocations (object creation, copies, boxing).
- Inefficient patterns (element-by-element vs bulk, concatenation in loops).
- Redundant operations (dead code, unused intermediates).
- Missing bulk/batch APIs.

Record each candidate with:
- **ID**: `P<round>-<seq>` (e.g. P5-1), incrementing from last used round.
- **Title**: short description.
- **File(s)**: affected source files.
- **Hypothesis**: what the change does and expected effect.
- **Risk**: low / medium / high.

### 2. Classify

| Priority | Criteria |
|----------|----------|
| Bug fix | Correctness issue. Apply regardless of perf impact. |
| High | Hot path, measurable allocation removal. |
| Medium | Utility functions, constructors, off-hot-path. |
| Low | Structural improvement, no expected throughput impact. |

Sort: bug fixes first, then high → low. Same priority: prefer lower risk, smaller diff.

### 3. Baseline

Capture fresh baseline before each round. If numbers differ >5% from recorded baseline, update and investigate before proceeding.

### 4. Implement

- One candidate at a time. No combining with refactors or cleanups.
- Minimal change. Keep revertable.
- Note exact files touched before editing.

### 5. Measure

Run full benchmark suite after each change. Compare **all** metrics against previous state, not just the targeted metric. Check for cross-component regressions.

### 6. Decide

| Target metric | Other metrics | Decision |
|--------------|---------------|----------|
| Improved | No regression (< -3%) | **KEEP** |
| Improved | Minor regression (3-10%) non-critical | **KEEP with note** |
| Improved | Regression (> 10%) anywhere | **REVERT** |
| No change | No regression | **KEEP** if bug fix, **SKIP** if pure optimization |
| Degraded | — | **REVERT** |

### 7. Document

- **KEEP**: Candidates → Completed. Update baseline.
- **REVERT**: Candidates → Rejected. Record result and reason.
- **SKIP**: Candidates → Rejected with "Not tested" and reason.
- After round: update Current Baseline, Remaining Bottlenecks, Key Insights.

### 8. Commit

One optimization per commit. Commit before starting next candidate.
- **KEEP**: `perf(<ID>): <title>` — stage source + docs/performance.md.
- **REVERT**: revert source, stage docs/performance.md, `perf(<ID>): reject — <reason>`.

## Benchmark Reliability

- **Multiple runs**: 3+ independent process invocations. Report median, not single snapshot.
- **Warm-up**: dedicated phase exercising exact measurement code path. 3-5 iterations discarded.
- **Isolation**: close unnecessary applications. Consistent CPU governor. Discard >20% outliers.
- **Comparability**: same machine, same runtime version. No cross-machine comparisons.
- **Noise threshold**: < 3% is noise. > 5% is meaningful.

## `docs/performance.md` Structure

```
## Current Baseline          ← latest numbers (always up to date)
## Key Improvements          ← table of per-optimization deltas
## Completed Optimizations   ← File, Change, Impact per entry
## Evaluated & Rejected      ← rejected/skipped with reasons
## Candidates                ← current round (empty when idle)
## Remaining Known Bottlenecks
## Key Insights              ← accumulated principles
```

### Section Rules
- **Current Baseline**: overwrite after each kept optimization.
- **Key Improvements**: append-only.
- **Completed Optimizations**: append-only. File, Change, Impact.
- **Evaluated & Rejected**: append-only. Preserves what NOT to try.
- **Candidates**: working area. Empty between rounds.
