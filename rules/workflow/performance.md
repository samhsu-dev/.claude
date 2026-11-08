---
paths:
  - "**/performance.md"
  - "**/*Performance*"
  - "**/*Benchmark*"
---

# Performance Optimization Guardrails

Full pipeline: `/perf` skill.

---

- One optimization per commit. No combining with refactors.
- Measurement before and after every change. No unmeasured optimizations.
- Estimate measurement variability before claiming an improvement. Use configured project metrics and acceptance thresholds; an unconfigured threshold is not a requirement.
- A regression of an accepted constraint follows `workflow/change-policy.md` Correctness and Verification. A required reversal uses a new commit under `workflow/git-safety.md`.
- Put optimization state in the module task record under `rules/workflow/records.md`.
- Decision authority follows `workflow/decisions.md`; existing user authorization covers candidate selection within the accepted scope.

## Localization

- A candidate needs profile or counter evidence. A code-reading suspicion is a hypothesis until measured.
- Growth order comes from work counters over a size sweep: the target workload fixed, one unrelated dimension grown, the counts recorded. Counters judge the growth order; wall time does not. Cost forecasts of a core change follow `workflow/change-policy.md` Early Cost Checks.
- Hot paths come from a sampling profiler run on a fixed sample.
- The cost is classified as CPU, allocation/GC or waiting (IO, lock, external process) before a fix is chosen.
- The language profile names the tools; the project values name the samples and counters.

## Fix Order

- Algorithm and data structure first, then implementation overhead, then runtime tuning.
- A micro-benchmark compares before and after a change to a located hot spot. It does not find one.

## Logging and Regression Guard

- Logging added for performance is a counter or stage timing that explains a cause. Never log per element in a loop.
- A periodic measurement on a fixed sample is compared with a recorded baseline. Work-count checks may gate merges; wall-time checks run separately because of noise.
