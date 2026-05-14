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
- < 3% variation is noise. > 5% is meaningful.
- Regression > 10% anywhere → revert. No exceptions.
- All state tracked in `docs/performance.md`.
- All decisions require user approval.
