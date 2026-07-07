# Resource Bounds and Timeouts

Rules governing how cost, runtime, and process liveness are bounded.

---

## Where the Bound Lives

- Bound cost by reducing input — scope, file count, item count, granularity. Never by killing a running computation on a wall-clock deadline.
- A deadline that kills a process producing all-or-nothing output is forbidden on a mandatory step. Its abort yields zero output, which fails the whole operation.
- Aborting a mandatory all-or-nothing step converts slow success into total failure. The bound belongs on the input, not on the wall clock.

## Liveness Backstops

- A hard-kill deadline is a liveness backstop, not a tuning parameter. Never expose it as a per-run configuration knob.
- One liveness backstop per unit of work. Never add an inner deadline that duplicates an outer deadline already bounding the same work.
- When an external or enclosing timeout bounds total runtime, inner steps set no fixed sub-deadline. The outer bound reaps a wedged process.

## Degradation

- Degradation of a mandatory step produces a cheaper-but-complete result. Skipping the step or continuing with empty output is failure, not degradation.
- A mandatory step is one whose output is the sole input to a downstream step; its absence fails the operation. Identify it before adding any bound.

## Sub-Tool Limits

- Use a sub-tool's own per-unit limits (per-file timeout, per-item budget) that skip the slow unit and return partial results. Never wrap the whole sub-tool in an external kill that returns nothing.
- Treat a sub-tool's recoverable per-unit errors (per-file timeout, partial parse) as warnings and keep partial results. Reserve fatal handling for whole-tool failure.
