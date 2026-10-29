---
name: decisions
description: Prepare, decide, ask and record an open design question. Use when a design question is open, before drafting a user question or a refutation run, or when recording a decision.
---

Prepare, decide, ask and record an open design question. Authority: `rules/workflow/decisions.md`. Parameters `paths`, `algorithm`, `usage_corpus`, `scoring_corpus` and `viewpoints` come from the project rule file `decisions.md` under `rules/project/`; `reference` and `evidence` from `evidence.md`; `glossary.path` from `glossary.md`; `execution` from `execution.md`.

## Evidence Preparation

1. Read affected local decision entries and every affected module's documents, including modules whose data an option reads or writes.
2. Read the glossary entry for each concept through `glossary.path`.
3. Search history for each concept. Use `git log -S '<term>' --oneline -- <documentation-paths> <source-paths>` and `git log --grep='<term>' --oneline`. Paths come from `paths`.
4. Read deleted text for every history hit with `git show <commit>^:<path>`. For a root commit, inspect its diff against the empty tree.
5. Apply recorded decisions; never offer them again as open choices. Cite the decision entry and recording commit in the question.
6. Check summary-derived or explicitly derived premises against owning documents before using them.
7. When an option changes how a construct is treated, count each such construct and each omitted limitation case in `usage_corpus`. Record occurrences, projects and method. Keep its role distinct from `scoring_corpus`.
8. Gather missing facts once: a chain session in its own context and decision entry, a user-decidable item into its evidence file under Evidence Files below.

## Decision Runs

- The chain session of a task decides each agent-decidable item inside that task, in its own context, with a short rationale: the chosen option, the evidence deciding it and the rejected alternative. No viewpoints and no refutation run; the task's next full review checks the decision against Solution Checks.
- A user-decidable item is drafted by the chain session that meets it. A question no chain owns, or one several tasks implement, takes one design run, launched as the chain session of the first of those tasks on the model skill `multi-agent` Model Routing gives that chain; its session then implements that task.
- The drafter of a user-decidable item weighs three viewpoints, fewer only when the item touches fewer. `viewpoints` supplies the selected roles and their exact project focuses. Each viewpoint is a section that ends with its own option and recommendation.
- It then lists the disagreements and the evidence deciding each, followed by the decision draft and its record draft.
- A user-decidable draft takes one refutation run on `execution.background` at `high_effort` in a fresh context. Its only substantive inputs are the question, the evidence file and the candidate rule; it receives no design reasoning.
- The refutation tries to refute the rule through counterexamples, invariants and cost counts, including security and precision consequences. It cites reference input and complete output, a decided sentence, or a code line.
- The drafter and the refutation apply Solution Checks.
- A refutation that holds returns to the drafter once. The item then reaches the user in Question Format; a refutation that still holds, or viewpoints that still disagree, are shown with both positions. No chief and no rebuttal round.
- A missing fact becomes a follow-up question. A choice depending on it waits for the answer.

## Evidence Files

- A user-decidable question keeps its facts in an evidence file in its task's working directory. Row fields, generic kinds and validation belong to `tools/evidence.py`; `evidence` binds the project meanings and reference runtime. One row holds one established fact.
- A run reads the evidence file before it searches and writes new rows only in its own run directory. The main agent merges them with `tools/evidence.py merge`, which keeps one current row per kind and source and marks a row whose value disagrees with the kept one as a conflict; no model edits the merged file.
- A row is stale when its quoted text no longer appears in its source file, or its program file or interpreter version changed. A stage that relies on it reads the source again and writes a new row.
- The first stage gathers the needed facts once; later stages cite fresh rows and add only missing facts.

## Solution Checks

- Check the candidate against every decided contract and configured `algorithm` constraint.
- Reuse and representation checks follow `rules/docs/design.md` Design principles. Inspect `algorithm.reuse_candidates` before adding data or a mechanism; apply `algorithm.reuse_example` to its named operation, relation and owners.
- Root-cause and capability checks follow `rules/workflow/change-policy.md`.
- Data flows only through `algorithm.allowed_data`. No unlisted flag, map or lookup bypasses it.
- Entities listed in `algorithm.immutable_entities` are never modified after creation.
- Compare examples with `reference.command` on `reference.version`. Record the complete output and version.
- A mismatch is a limitation under `rules/workflow/decisions.md` Authority; no failing option is silently treated as conforming.
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

- Record a user decision and update its owning design text in the same turn.
- The chain session that decides an agent decision writes its rule into the owning document and commits it at once. It writes the decision entry into its progress file; the main agent moves the entry into the decision log, which is never committed.
- After a user decision is recorded, the main agent resumes the drafting session to implement it and continues the next independent work.
- Write a new edge case in the same turn. Put its example in the owning document's Edge Cases section when its rule is decided; otherwise use the open decision entry.
- A new conformance rule reviews every logged agent decision. Revise a failing decision under `rules/workflow/decisions.md` Authority or take it to the user.
- A decision result names the corrections for the session that implements it.
