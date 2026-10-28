---
paths:
  - "**/*.{py,ts,tsx,js,jsx,go,rs,java,cpp,c,cs,rb,swift,kt,php,sh}"
---

# Resource Bounds and Timeouts

Rules governing how cost, runtime, and process liveness are bounded.

---

## Where the Bound Lives

- Bound cost through input scope, file count, item count or granularity. Never use a wall-clock kill to tune cost; Liveness Backstops governs a wedged process.
- A deadline that kills a process producing all-or-nothing output is forbidden on a mandatory step. Its abort yields zero output, which fails the whole operation.

## Liveness Backstops

- A hard-kill deadline is a liveness backstop, not a tuning parameter. Never expose it as a per-run configuration knob.
- One liveness backstop per unit of work. When an external or enclosing timeout bounds total runtime, inner steps set no fixed sub-deadline; the outer bound reaps a wedged process.

## Degradation

- Degradation of a mandatory step produces a cheaper-but-complete result. Skipping the step or continuing with empty output is failure, not degradation.
- A step is mandatory when the operation cannot finish without its output. Identify mandatory steps before adding a bound.

## Sub-Tool Limits

- Use a sub-tool's own per-unit limits (per-file timeout, per-item budget) that skip the slow unit and return partial results. Never wrap the whole sub-tool in an external kill that returns nothing.
- Keep partial output and report recoverable per-unit errors as warnings. Whole-tool failure is fatal. A mandatory operation still has to meet Degradation.
