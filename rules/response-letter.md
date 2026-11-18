---
paths:
  - "**/response.tex"
---

# Response Letter

Extends `writing.md`.

## Answer First

- The first sentence of each response is its takeaway: it answers the request's verb and object and states the key number. "Distinguish A from B": the verdict on A versus B. "Provide evidence": the claim and the headline number.
- A first sentence that states only a number or a partial result is rewritten.
- The remaining text is grouped by request point under bold lead-ins, in the order the request lists the points.
- The response ends with the paper sections that contain the answer.

## Necessity

- Delete every sentence and clause whose removal loses no fact, number, or stated relation (contrast, consequence, condition).
- Delete a sentence that repeats a claim made earlier in the response.
- Delete roadmap, announcement, and linking-only sentences ("We answer the points in turn", "Below we document ...").
- Delete an ordinal label ("The first is", "First,") and write the dimension instead: "In checking X, ...".
- A number, table, or URL appears only when it supports the stated answer.
- Delete an implementation detail the request does not ask for.
- Delete a figure that shows what another figure in the response shows.
- A sentence that corrects an earlier sentence is merged into that sentence.
- Each embedded table or list is cited by the prose beside it.

## Scope

- Answer only what the request asks. No limitation, caveat, failure count, or weakness the request does not raise.
- A limit the request raises is stated as scope and design rationale: what the system targets, why, what it detects within that scope ("detects 62 of the y"), and where the paper discusses extensions. Never write "cannot", "misses", or "establishes nothing" about the system.
- A result the request asks about is reported in full, with the interpretation that answers the request.
- Never explain arithmetic.

## Terms

- Canonical names: Convergent Semantic Binding, Monitor-Guided Fuzzing, invariant monitor, false-detection rate (FDR).
- System names: BELUGA, STRIX, STRIX-Control, PromFuzz-PHP, GPTScan-PHP. Plural statements list the names ("STRIX and STRIX-Control").
- Each entity has the same name in the letter and in the paper.
- Each result is reported in the metric the paper reports for it. Never switch between precision and FDR for one result.
- Entities and concepts are named by the paper's terms, never by the reviewer's shorthand ("checkout context") or a coined phrase ("application domain").
- Reviewer text is quoted only inside the request block.

## Evidence

- Before writing, check each number against the result tables and `Packages/local.tex`, and each system claim against the system's repository or prompt. An unchecked claim is marked `\todo` or deleted.

## Flow

- Each paragraph begins with the step it takes: a result, the next difference, or the next comparison.
- Each group runs setup, result, interpretation.

## Sync With the Paper

- A change to a description, number, or term in the letter is applied in the same edit to every place in the paper that states it: section text, `\begin{revised}` blocks, captions, tables, `Packages/local.tex` macros, abstract, conclusion.
- A change in the paper is applied in the same edit to the letter's quotes and answers.
- Before editing, search the whole source for the system name, the number, and the key phrase. Report the places changed.

## Revising an Item

- When one sentence of an item is flagged, reread the whole item against the request and rewrite the whole item.
- Before rewriting, list the request's points and set the grouping: one group per compared entity the request names, with method claims and domain evidence in separate groups.
- A mechanism is mentioned only where it is the difference the comparison shows.

## Check Before Delivering

Run each step on each response item. The item is done only when every step passes.

1. Read the first sentence alone. It answers the request's verb and object and states the key number.
2. Apply the Necessity deletions to every sentence. List each deleted sentence in the report.
3. Match every number to the result tables and `Packages/local.tex`, and every system claim to its repository or prompt.
4. Search the item for "both", "the two", "two of", "them", "this", "configuration", "variant": each has a listed referent and a correct count. Search for "cannot", "misses", "nothing", "only": none describes the system as weak. No limitation the request does not raise appears.
5. Pass the `writing.md` Post-Edit Reread checks.
6. Apply Sync With the Paper.
7. Build: exit 0, no undefined reference.
