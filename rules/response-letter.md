---
paths:
  - "**/response.tex"
---

# Response Letter

Applies to `Sections/response.tex`. Extends `writing.md`.

## Answer First

- Write the first sentence of each response as the takeaway. Answer the request's verb and object in the request's own terms and state the key number. "Distinguish A from B": state the verdict on A versus B. "Provide evidence": state the claim and the headline figure.
- Reject a first sentence that states only a number or a partial result.
- Group the remaining text by request point under bold lead-ins, in the order the request lists the points.
- End with the paper changes: the sections that contain the answer.

## Necessity

- Apply the deletion test to every sentence and clause. Delete it unless its removal loses a fact, a number, or a stated relation (contrast, consequence, condition).
- Apply the duplicate-claim test. Delete a sentence that repeats a claim made earlier in the response.
- Delete roadmap, announcement, and linking-only sentences ("We answer the points in turn", "Below we document ...").
- Delete an ordinal label ("The first is", "First,") when the following words name the dimension. Write "In checking X, ...".
- Keep a connective only when it names a relation the reader cannot see without it.
- Include a number, table, or URL only when it supports the stated answer.
- Delete implementation details the request does not ask for.
- Delete a second figure that repeats what the first shows.
- Merge a sentence that patches an earlier sentence into that sentence.
- Write prose that cites the table or list it carries; place no table or list beside prose that does not use it.

## Scope

- Answer only what the request asks. Omit limitations, caveats, failure counts, and weaknesses the request does not raise.
- State a limit the request does raise as scope and design rationale: what the system targets, why, what it detects within that scope ("detects 62 of the y"), and where the paper discusses extensions. Do not write "cannot", "misses", or "establishes nothing" about the system.
- Report a result the request asks about in full, with the interpretation that answers the request.
- Write for experts. Do not explain field-standard terms or arithmetic.
- State each claim directly. Do not set up a claim with "not X but Y" or a counterexample.
- Attribute a difference to a cause only when a controlled setup excludes the other causes. Otherwise state the comparison ("differs", "is lower").

## Terms

- Use the paper's canonical names: Convergent Semantic Binding, Monitor-Guided Fuzzing, invariant monitor, false-detection rate (FDR).
- Name each system by its own name (BELUGA, STRIX, STRIX-Control, PromFuzz-PHP, GPTScan-PHP), also in plural statements ("STRIX and STRIX-Control").
- Use a group noun or generic word ("both", "the two tools", "configuration") only when the same or the preceding sentence lists its members and the count equals the number of members.
- Use one name per entity in the letter and the paper.
- Report the metric the paper reports. Do not switch between precision and FDR for one result.
- Write the reviewer's term at first mention, then the paper's term.
- Do not write reviewer shorthand ("checkout context") or coined phrases ("application domain"). Quote the reviewer only inside the request block.

## Wording

- Choose a verb that fits every object it governs. Split a coordination whose objects need different verbs.
- Use a pronoun only when its antecedent is the nearest preceding noun phrase.
- Verify each number against the result tables and `Packages/local.tex`, and each system claim against its repository or prompt, before writing. Mark an unverified claim with `\todo` or omit it.

## Flow

- Begin each paragraph with the step it takes: a result, the next difference, or the next comparison.
- Order each group: setup, result, interpretation.

## Sync With the Paper

- Apply a change to a description, number, or term in the letter to every place in the paper that states it, in the same change: section text, `\begin{revised}` blocks, captions, tables, `Packages/local.tex` macros, abstract, conclusion.
- Apply a change in the paper to the letter's quotes and answers.
- Before editing, search the whole source for the system name, the number, and the key phrase. Report the places changed.

## Revising an Item

- When one sentence of an item is flagged, reread the whole item against the request and rewrite it as a whole. Do not patch the flagged span.
- Before rewriting, list the request's points and fix the grouping: group by the compared entity the request names (one group per tool), and keep method claims apart from domain evidence. A wrong grouping cannot be repaired by local edits.
- Mention a mechanism only where it is the difference the comparison shows.

## Check Before Delivering

Run these steps on each response item. Do not report the item done before every step passes.

1. Read the first sentence alone. It answers the request in the request's terms and states the key number. Test it against the request text.
2. Run the deletion test and the duplicate-claim test on every sentence. List each deleted sentence in the report.
3. Match every number to the result tables and `Packages/local.tex`, and every system claim to its repository or prompt.
4. Search the item for "both", "the two", "two of", "them", "this", "configuration", "variant". Check that each has a listed referent and a correct count. Check that no limitation the request did not raise appears, and that no "cannot", "misses", "nothing", or "only" frames the system as weak.
5. Pass the `writing.md` Post-Edit Reread list.
6. Update every place that states the same fact (Sync With the Paper).
7. Build with exit 0 and no undefined references.
