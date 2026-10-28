# Design Decisions

Parameters `project`, `paths`, `algorithm`, `usage_corpus`, `scoring_corpus` and `viewpoints` are supplied by the project rule files under `rules/project/`, in `decisions.md`; `reference` comes from `evidence.md` and `glossary.path` from `glossary.md`.

Apply this rule to an open design question. Project values bind through `CLAUDE.md` Parameter Binding.
Development phase gates remain owned by `workflow/development.md`.

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

## Evidence Preparation

1. Read affected local decision entries and every affected module's documents, including modules whose data an option reads or writes.
2. Read the glossary entry for each concept through `glossary.path`.
3. Search history for each concept. Use `git log -S '<term>' --oneline -- <documentation-paths> <source-paths>` and `git log --grep='<term>' --oneline`. Paths come from `paths`.
4. Read deleted text for every history hit with `git show <commit>^:<path>`. For a root commit, inspect its diff against the empty tree.
5. Apply recorded decisions; never offer them again as open choices. Cite the decision entry and recording commit in the question.
6. Check summary-derived or explicitly derived premises against owning documents before using them.
7. When an option changes how a construct is treated, count each such construct and each omitted limitation case in `usage_corpus`. Record occurrences, projects and method. Keep its role distinct from `scoring_corpus`.
8. Gather missing facts once: a chain session in its own context and decision entry, a user-decidable item into its evidence file under `workflow/multi-agent.md` Evidence Files.

## Decision Runs

- The chain session of a task decides each agent-decidable item inside that task, in its own context. A user-decidable item is drafted the same way by the chain session that meets it. A question no chain owns, or one several tasks implement, takes one design run, launched as the chain session of the first of those tasks on the model `workflow/multi-agent.md` Model Routing gives that chain; its session then implements that task.
- The drafter weighs three viewpoints, fewer only when the item touches fewer. `viewpoints` supplies the selected roles and their exact project focuses. Each viewpoint is a section that ends with its own option and recommendation.
- It then lists the disagreements and the evidence deciding each, followed by the decision draft and its record draft.
- An agent-decidable decision is recorded under Recording. The task's next full review checks it against Solution Checks; no separate refutation runs.
- A user-decidable draft takes one refutation run at `execution.background` high effort in a fresh context. Its only substantive inputs are the question, the evidence file and the candidate rule; it receives no design reasoning.
- The refutation tries to refute the rule through counterexamples, invariants and cost counts, including security and precision consequences. It cites reference input and complete output, a decided sentence, or a code line.
- The drafter and the refutation apply Solution Checks.
- A refutation that holds returns to the drafter once. The item then reaches the user in Question Format; a refutation that still holds, or viewpoints that still disagree, are shown with both positions. No chief and no rebuttal round.
- A missing fact becomes a follow-up question. A choice depending on it waits for the answer.
- After the user decides, the drafting session implements the decision.
- Count launched runs and resumptions per decision, wall time from evidence preparation through the recorded decision, and decisions a later review overturns. The run ledger keeps them under `workflow/multi-agent.md` Records.

## Solution Checks

- Check the candidate against every decided contract and configured `algorithm` constraint.
- Reuse and representation checks follow `docs/design.md` Design principles. Inspect `algorithm.reuse_candidates` before adding data or a mechanism; apply `algorithm.reuse_example` to its named operation, relation and owners.
- Root-cause and capability checks follow `workflow/change-policy.md`.
- Data flows only through `algorithm.allowed_data`. No unlisted flag, map or lookup bypasses it.
- Entities listed in `algorithm.immutable_entities` are never modified after creation.
- Compare examples with `reference.command` on `reference.version`. Record the complete output and version.
- A mismatch is a limitation under Authority; no failing option is silently treated as conforming.
- Before offering a known limitation, survey literature, industrial tools, other fields, closed-form mathematics and known algorithms. Cite alternatives and remaining limits.
- Check all affected items and boundary cases against research, repository conventions and recorded decisions.
- Code has the lowest confidence for intended semantics. A code/doc difference is a code gap; independent reference output can establish a semantic defect.

## Question Format

- Open with every affected recorded constraint and its commit, then every recorded edge case with its example.
- Name the documents and commits reviewed.
- Every question and option list includes a minimal example and complete real reference output in readable multi-line form.
- Each option states its reported result, precision, recall and cost per configured phase against the current design.
- Each option states that it keeps earlier decisions or quotes the sentence it changes with its commit.
- Recommend a revision only when a reference example contradicts the earlier sentence.
- State the usage counts from Evidence Preparation.
- End with a discussion option and name one recommended option.

## Recording

- Record fields and placement follow `CLAUDE.md` Local Records. Current design and provenance follow Documentation Ownership.
- Record a user decision and update its owning design text in the same turn.
- The chain session that decides an agent decision writes its rule into the owning document and commits it at once under `workflow/committing.md`. It writes the decision entry into its progress file; the main agent moves the entry into the decision log, which is never committed.
- After a user decision is recorded, the main agent resumes the drafting session to implement it and continues the next independent work.
- Write a new edge case in the same turn. Put its example in the owning document's Edge Cases section when its rule is decided; otherwise use the open decision entry.
- A new conformance rule reviews every logged agent decision. Revise a failing decision under Authority or take it to the user.

- A decision result names the corrections for the session that implements it.
