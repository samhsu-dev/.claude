---
name: decisions
description: Prepare, decide, ask and record an open design question. Use when a design question is open, before drafting a user question or a refutation run, or when recording a decision.
---

Prepare, decide, ask and record an open design question. Authority: `rules/workflow/decisions.md`. Parameters `paths`, `algorithm`, `usage_corpus`, `scoring_corpus` and `viewpoints` come from the project rule file `decisions.md` under `rules/project/`; `reference` and `evidence` from `evidence.md`; `glossary.path` from `glossary.md`; `execution` from `execution.md`. Read those four files before step 1.

## Authority

The user-authority conditions are `rules/workflow/decisions.md` Authority.

- Triage each item as agent-decidable or user-decidable. Give a one-clause reason.
- For an item no user-authority condition covers, public API shape, signatures, field names and result types included, the agent chooses one option and records the chosen option, the evidence deciding it and the rejected alternative.
- A unique option matching every reference example is agent-decidable unless a user-authority condition applies.
- Behavior-equivalent naming choices follow the glossary at `glossary.path` and `rules/docs/glossary.md` Naming Steps. A name derived from an existing type identifier needs no user question.
- The agent revises a user decision outside the core principles when reference output refutes the decided sentence or when an agent derived that sentence from another decided sentence that still holds; the user decides every other revision.
- Keep mechanism details with the agent when they follow from a core choice. Ask the user only that core choice, in plain words, with one example.

## Evidence Preparation

1. Apply `workflow/change-policy.md` Outcome and Scope. Read the owning documents and decision entries for the affected contracts, including a producer or consumer whose contract an option changes.
2. Read the glossary entry for each concept through `glossary.path`.
3. Search history when the owning documents and decision entries of step 1 leave an authority or behavior premise unresolved. Use scoped `git log -S` or `git log --grep`; paths come from `paths`.
4. Read the changes needed to resolve that premise. A history match alone creates no investigation obligation.
5. Apply recorded decisions as fixed premises of the option list.
6. Check summary-derived or explicitly derived premises against owning documents before using them.
7. When a decision depends on usage frequency, measure the affected cases in a configured usage corpus and record the counting method. Measure usage frequency outside the configured scoring corpus.
8. Gather missing facts once: a chain session in its own context and decision entry, a user-decidable item into its evidence file under Evidence Files below.

## Decision Runs

- The chain session of a task decides each agent-decidable item inside that task, in its own context, with a short rationale: the chosen option, the evidence deciding it and the rejected alternative. It verifies the choice against Solution Checks in that task, with no viewpoints and no refutation run.
- Draft an open choice in its owning resident or chain context. A Simple or Routine choice that requires user authority goes directly to the user with relevant options and evidence; it creates no separate design or refutation run.
- Record each open core question in the decision log when it is found, and queue its evidence gathering or draft at once under skill `multi-agent` Dispatch.
- Route an unresolved user-decidable core choice in Full through the design and refutation procedure below. Its drafter weighs the affected viewpoints. `viewpoints` supplies the selected roles and their exact project focuses. Each viewpoint is a section that ends with its own option and recommendation.
- The drafter then lists the disagreements and the evidence deciding each, followed by the decision draft and its record draft.
- A Full core-choice draft takes one refutation run on `execution.background` at `high_effort` in a fresh context. Its only substantive inputs are the question, the evidence file and the candidate rule; it receives no design reasoning.
- The refutation tries to refute the rule through counterexamples, invariants and cost counts, including security and precision consequences. It cites reference input and complete output, a decided sentence, or a code line.
- The drafter and the refutation apply Solution Checks.
- Return a refutation that holds to the drafter once. Then present the item to the user in Question Format with each supported position: the refutation that still holds and each viewpoint that still disagrees.
- A brief for a run that compares designs or investigates a choice states three requirements. The run reports what it finds, independent of the preference of the main agent or the user, and a result that contradicts every listed candidate is valid. The run adds to the listed candidates each other design it finds in the literature, industrial tools or the code's existing mechanisms, with its source. The result gives the evidence against its own recommendation in a separate section.
- A fact the drafter or refutation lacks becomes a follow-up question from the main agent to the session that holds that context; a choice depending on it waits for the answer.

## Evidence Files

- A user-decidable question keeps each established fact with its source and relevant input or version in the question's evidence file under the decision log's `evidence/` directory (`rules/workflow/records.md`). Use a configured evidence schema and validator when present.
- Read that file before gathering more facts. Consolidate contributions by source, retaining conflicts explicitly.
- A row is stale when its quoted text, with each whitespace run read as one space, no longer appears in its source file, or its program file or interpreter version changed. A stage that relies on it reads the source again and writes a new row.
- Later stages cite fresh rows and add only missing facts.
- `tools/evidence.py merge <task-dir>` merges the run rows; `tools/evidence.py brief <task-dir>` prints the brief lines.

## Solution Checks

- Check the candidate against each decided contract Evidence Preparation step 1 read and each configured `algorithm` constraint.
- Reuse and representation checks follow `rules/docs/design.md` Design principles. Inspect `algorithm.reuse_candidates` before adding data or a mechanism; apply `algorithm.reuse_example` to its named operation, relation and owners.
- Before listing options, apply `rules/workflow/change-policy.md` Correctness and Verification to the failure: state the fact or rule the design lacks and every site where that lack changes a result, each with an input and its reference output. List only options that change the owner of that fact, one of them correcting it for all listed sites; leave a guard, a special case or a second mechanism beside the existing one at the failing site off the list.
- A root-cause option is weighed like every other: state the result quality it gains or loses and the dimension its work grows with, with the bound that stops it. When the complete correction does not scale, offer the same correction at the owner with a stated bound, and name what the bound leaves open.
- A run asked to check a question receives the question and the evidence before any candidate list, and proposes its own options first.
- When `algorithm.allowed_data` is configured, route data only through those structures.
- Keep each entity listed in `algorithm.immutable_entities` unchanged after creation.
- Check each example by running `reference.command` and record the version `reference.version_command` prints in the example's evidence; without a reference runtime, check it against the accepted contract. Record the input, expected result and verification evidence.
- Treat a mismatch as a limitation under Authority above, and mark each failing option as failing.
- Before offering a known limitation, the drafter cites for each of literature, industrial tools, other fields, closed-form mathematics and known algorithms either an alternative with its remaining limit or the search that found none.
- Check all affected items and boundary cases against research, repository conventions and recorded decisions.
- A code/doc difference is a code gap unless independent reference output shows a semantic defect.

## Question Format

- Send or list a question only after recording its authority (Authority above), the searches of the decided documents, the directives and the transcripts with their results, and the question with its evidence.
- Open with every affected recorded constraint with its decision entry and recording commit, then every recorded edge case with its example.
- Name the documents and commits reviewed.
- Every question and option list includes a minimal example, its expected result and supporting evidence; include complete reference output when a reference run supplies that evidence.
- Each option states its observable result and effects on required quality and resource constraints against the current design, using configured metrics and phases.
- The recommendation states the tradeoff between result quality and growth that selects it.
- Each option states that it keeps earlier decisions or quotes each sentence it changes with its commit.
- Recommend a revision of an earlier sentence when reference output refutes it or when an agent derived it from another decided sentence that still holds (Authority above); otherwise recommend an option that keeps it.
- End with a discussion option and name one recommended option.

## Recording

- In the turn the user decides, the main agent records the decision and resumes the drafting session, which writes the decided sentence into its owning design text.
- The chain session that decides an agent decision writes its rule into the owning document and commits it at once. It writes the decision entry into its progress file; the main agent moves the entry into the decision log.
- After a user decision is recorded, the main agent resumes the drafting session to implement it and continues the next independent work.
- Write a new edge case in the same turn: its example goes beside the rule that decides it in the owning document, or into the open decision entry while the rule is undecided.
- The session that writes a decided sentence searches the project's documents and code comments for each sentence that states a different result for the same input, and corrects each in the same commit; a sentence in a file outside that session's write set is added to the board as an open row that quotes it with path and line.
- When a rule is added, the main agent checks each logged agent decision that governs a contract the rule governs, and revises a failing one under Authority above or takes it to the user.
- A decision result names the corrections for the session that implements it.
