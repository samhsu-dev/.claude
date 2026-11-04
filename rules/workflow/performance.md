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
