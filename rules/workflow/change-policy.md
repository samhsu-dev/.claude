# Change Policy

## Outcome and Scope

- Define the observable result, required constraints and completion checks before choosing an implementation. Reuse the task's existing statement; no separate planning artifact is required.
- Derive necessary work backward from that result. An added dependency, abstraction, tool, investigation or check names the current requirement, demonstrated failure or concrete safety risk it addresses. Future usefulness alone establishes no requirement.
- Compare materially different feasible approaches by their remaining implementation, verification, runtime and maintenance costs. Include direct use or modification of existing code and data; choose the least complex approach that satisfies the result and constraints.
- Reconsider the approach when a new dependency, repeated repair or cost growth changes that comparison. Prior effort and agent-authored plans do not justify further work or expand user authorization.
- Verify every claim used to justify the result. Investigation covers the task's requirements and affected contracts; it does not enumerate unrelated possibilities.
- Complete the task when its result and required checks pass. Additional investigation or repeated checks need a new change, failure or unresolved concrete risk.

## Correctness and Verification

- No guessing. Verify via documentation, source code, or test. If unverifiable, ask.
- Trace a fault to the rule, mechanism or data that produces it and correct that cause within the accepted scope. Check all affected callers and contracts. A local correction is valid when it restores the contract; masking the failure or creating inconsistent parallel behavior is rejected.
- Before review, identify the sites governed by changed invariants across the diff and its affected callers. Verify every identified site and cover distinct affected behaviors with tests. Send the site list with the diff.
- Compare behavior and required quality and resource constraints with the integration base using tests or measurements. A regression of an accepted constraint goes to the user unless an existing decision authorizes the tradeoff. Removing what the same branch added creates no loss against that base.
- Use project-defined metrics and phases when assessing a resource-sensitive change. Report the evidence supporting the claimed impact.

## Implementation

- Before changing or removing a component, read the code that implements it to establish the actual division of labor. Never infer responsibility from names, docstrings, or an adjacent doc sentence.
- Choose tools and automation under Outcome and Scope. An auxiliary tool supports the accepted inputs; expanding its input domain is a separate scope decision.
- No backward-compatibility requirements.
- Return types, signatures, behavior and public API change only within user authorization or the agent authority assigned by `workflow/decisions.md`.
