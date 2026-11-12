---
paths:
  - "**/performance.md"
  - "**/*Performance*"
  - "**/*Benchmark*"
---

# Performance Optimization Guardrails

Full pipeline: `/perf` skill.

---

- Measurement before and after every change. No unmeasured optimizations.
- Estimate measurement variability before claiming an improvement. Use configured project metrics and acceptance thresholds; an unconfigured threshold is not a requirement.
- A regression of an accepted constraint follows `workflow/change-policy.md` Correctness and Verification.- Put optimization state in the module task record under `rules/workflow/records.md`.
- Decision authority follows `workflow/decisions.md`.

## Localization

- A candidate needs profile or counter evidence.- Growth order comes from work counters over a size sweep: the target workload fixed, one unrelated dimension grown, the counts recorded. Counters judge the growth order; wall time does not. Cost forecasts of a core change follow `workflow/change-policy.md` Early Cost Checks.
- Hot paths come from a sampling profiler run on a fixed sample.
- The cost is classified as CPU, allocation/GC or waiting (IO, lock, external process) before a fix is chosen.

## Fix Order

- Algorithm and data structure first, then implementation overhead, then runtime tuning.
- A micro-benchmark only compares before and after a change to a located hot spot.

## Logging and Regression Guard

- Logging added for performance is a counter or stage timing that explains a cause. Never log per element in a loop.
- A periodic measurement on a fixed sample is compared with a recorded baseline. Work-count checks gate merges when the project gate runs them; wall-time checks run outside the merge gate.
