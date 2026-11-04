# Design Decisions

Configured `algorithm` and `reference` parameters come from project files under `rules/project/`. Their absence implies no particular algorithm or reference runtime.

Triage, the agent's authority and recording: skill `decisions`.

## Authority

- The user decides changes to `algorithm.core_principles`.
- The user decides a known limitation when every available option contradicts a complete reference output.
- The user decides a gap where a paper or tool handles a case the design misses.
- The user decides a revision of a user decision, except the narrow revisions skill `decisions` Authority lists.
- Regressions of accepted behavior, quality or resource constraints follow `workflow/change-policy.md`.
