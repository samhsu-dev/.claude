# Design Decisions

Parameters `algorithm` and `reference` are supplied by the project rule files under `rules/project/`, in `decisions.md` and `evidence.md`.

Authority over an open design question. Procedure: skill `decisions`.

## Authority

- Triage each item as agent-decidable or user-decidable. Give a one-clause reason.
- The user decides changes to `algorithm.core_principles`.
- The user decides a known limitation when every available option contradicts a complete reference output.
- The user decides a gap where a paper or tool handles a case the design misses.
- Correctness, precision, recall and cost regressions follow `workflow/change-policy.md`.
- The agent decides other items with one evidence-supported better design, including public API shape, signatures, field names and result types.
- A unique option matching every reference example is agent-decidable unless a user-authority condition above applies.
- Behavior-equivalent naming choices follow `docs/glossary.md`. A name derived from an existing type identifier needs no user question.
- The agent may revise a user decision only outside the core principles, when reference output refutes the old sentence or the narrowed sentence is derived text.
- All other revisions of user decisions go to the user.
- Keep mechanism details with the agent when they follow from a core choice. Ask the user only that core choice, in plain words, with one example.
