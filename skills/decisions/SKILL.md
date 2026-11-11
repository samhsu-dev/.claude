---
name: decisions
description: Prepare, decide, ask and record an open design question. Use when a design question is open, before drafting a user question or a refutation run, or when recording a decision.
---

Prepare, decide, ask and record an open design question. Authority: `rules/workflow/decisions.md`. Parameters `paths`, `algorithm`, `usage_corpus`, `scoring_corpus` and `viewpoints` come from the project rule file `decisions.md` under `rules/project/`; `reference` and `evidence` from `evidence.md`; `glossary.path` from `glossary.md`; `execution` from `execution.md`. Read those four files before step 1.

## Authority

The user-authority conditions are `rules/workflow/decisions.md` Authority.

- Triage each item as agent-decidable or user-decidable. Give a one-clause reason.
- The agent decides other items with one evidence-supported better design, including public API shape, signatures, field names and result types.
- A unique option matching every reference example is agent-decidable unless a user-authority condition applies.
- Behavior-equivalent naming choices follow `docs/glossary.md`. A name derived from an existing type identifier needs no user question.
- The agent may revise a user decision only outside the core principles, when reference output refutes the old sentence or the narrowed sentence is derived text.
- Keep mechanism details with the agent when they follow from a core choice. Ask the user only that core choice, in plain words, with one example.

## Evidence Preparation

1. Apply `workflow/change-policy.md` Outcome and Scope. Read the owning documents and decision entries for the affected contracts, including a producer or consumer whose contract an option changes.
2. Read the glossary entry for each concept through `glossary.path`.
3. Search history when current owners and records leave an authority or behavior premise unresolved. Use scoped `git log -S` or `git log --grep`; paths come from `paths`.
4. Read the changes needed to resolve that premise. A history match alone creates no investigation obligation.
5. Apply recorded decisions; never offer them again as open choices. Cite the decision entry and recording commit in the question.
6. Check summary-derived or explicitly derived premises against owning documents before using them.
7. When a decision depends on usage frequency, measure the affected cases in a configured usage corpus and record the counting method. A scoring corpus, when configured, retains its separate evaluation role.
8. Gather missing facts once: a chain session in its own context and decision entry, a user-decidable item into its evidence file under Evidence Files below.

## Decision Runs

- The chain session of a task decides each agent-decidable item inside that task, in its own context, with a short rationale: the chosen option, the evidence deciding it and the rejected alternative. No viewpoints and no refutation run; the task mode's verification checks the decision against Solution Checks.
- Draft an open choice in its owning resident or chain context. A Simple or Routine choice that requires user authority goes directly to the user with relevant options and evidence; it creates no separate design or refutation run.
- Only an unresolved user-decidable core choice in Full uses the design and refutation procedure below. Its drafter weighs the affected viewpoints. `viewpoints` supplies the selected roles and their exact project focuses. Each viewpoint is a section that ends with its own option and recommendation.
- It then lists the disagreements and the evidence deciding each, followed by the decision draft and its record draft.
- A Full core-choice draft takes one refutation run on `execution.background` at `high_effort` in a fresh context. Its only substantive inputs are the question, the evidence file and the candidate rule; it receives no design reasoning.
- The refutation tries to refute the rule through counterexamples, invariants and cost counts, including security and precision consequences. It cites reference input and complete output, a decided sentence, or a code line.
- The drafter and the refutation apply Solution Checks.
- A refutation that holds returns to the drafter once. The item then reaches the user in Question Format; a refutation that still holds, or viewpoints that still disagree, are shown with both positions. No rebuttal round.
- A missing fact becomes a follow-up question. A choice depending on it waits for the answer.

## Evidence Files

- A user-decidable question keeps each established fact with its source and relevant input or version in the task's evidence record. Use a configured evidence schema and validator when present.
- Read that record before gathering more facts. Consolidate contributions by source, retaining conflicts explicitly. This procedure requires no project-specific script or new evidence tool.
- A row is stale when its quoted text no longer appears in its source file, or its program file or interpreter version changed. A stage that relies on it reads the source again and writes a new row.
- The first stage gathers the needed facts once; later stages cite fresh rows and add only missing facts.

## Solution Checks

- Check the candidate against every decided contract and configured `algorithm` constraint.
- Reuse and representation checks follow `rules/docs/design.md` Design principles. Inspect `algorithm.reuse_candidates` before adding data or a mechanism; apply `algorithm.reuse_example` to its named operation, relation and owners.
- Root-cause and capability checks follow `rules/workflow/change-policy.md`.
- Before listing options, state the fact or rule the design lacks that produces the failure, and search for every other site where the same lack changes a result; each site gets an input and its reference output. The option list includes one option that corrects the owner of that fact for all listed sites. An option that only changes the site where the failure was seen (a guard, a special case, a second mechanism beside the existing one) is a patch and is rejected, not offered. Options are never limited to the site where the failure was first seen.
- A root-cause option is weighed like every other: state the result quality it gains or loses and the dimension its work grows with, with the bound that stops it. When the complete correction does not scale, offer the same correction at the owner with a stated bound, never a site patch, and name what the bound leaves open.
- A run asked to check a question receives the question and the evidence before any candidate list, and proposes its own options first.
- When `algorithm.allowed_data` is configured, data flows only through those structures; no additional representation bypasses that constraint.
- Entities listed in `algorithm.immutable_entities` are never modified after creation.
- Check examples against the configured reference command and version, or against the accepted contract when no reference runtime exists. Record the input, expected result and verification evidence.
- A mismatch is a limitation under Authority above; no failing option is silently treated as conforming.
- Before offering a known limitation, survey literature, industrial tools, other fields, closed-form mathematics and known algorithms. Cite alternatives and remaining limits.
- Check all affected items and boundary cases against research, repository conventions and recorded decisions.
- Code has the lowest confidence for intended semantics. A code/doc difference is a code gap; independent reference output can establish a semantic defect.

## Question Format

- Open with every affected recorded constraint and its commit, then every recorded edge case with its example.
- Name the documents and commits reviewed.
- Every question and option list includes a minimal example, its expected result and supporting evidence; include complete reference output when a reference run supplies that evidence.
- Each option states its observable result and effects on required quality and resource constraints against the current design, using configured metrics and phases.
- State the lacking fact or rule and the list of affected sites before the options (Solution Checks). The recommendation states the tradeoff between result quality and growth that selects it.
- Each option states that it keeps earlier decisions or quotes the sentence it changes with its commit.
- Recommend a revision only when a reference example contradicts the earlier sentence.
- Include the impact measurements the decision relies on.
- End with a discussion option and name one recommended option.

## Recording

- Record a user decision and update its owning design text in the same turn.
- The chain session that decides an agent decision writes its rule into the owning document and commits it at once. It writes the decision entry into its progress file; the main agent moves the entry into the decision log, which is never committed.
- After a user decision is recorded, the main agent resumes the drafting session to implement it and continues the next independent work.
- Write a new edge case in the same turn. Put its example in the owning document's Edge Cases section when its rule is decided; otherwise use the open decision entry.
- A new conformance rule reviews every logged agent decision. Revise a failing decision under Authority above or take it to the user.
- A decision result names the corrections for the session that implements it.
