---
paths:
  - "**/implementation.tex"
  - "**/implementations.tex"
---

# Implementation Structure

A short section reporting engineering facts the approach left out. One opening sentence on scale and availability, then one labeled paragraph per implementation concern. Every claim carries a concrete number or a named artifact. No restatement of the approach's algorithm.

---

## Section Order

| # | Block | Function |
|---|-------|----------|
| 1 | Opening | Implementation language, code size, public repository |
| 2 | Concern paragraphs | One `\paragraph{}` per engineering concern, each a named decision with its number or reason |

## Opening Sentence

- One sentence: the tool name, the implementation language, the line count, and a `\url{}` to the open-source repository.
- State size as a measured line count, not "large" or "small".
- No algorithm recap. The approach section owns the method.

## Concern Paragraphs

Each concern is one `\paragraph{Name:}` block. The label names the concern; the body states the decision and the evidence for it.

Concerns appear only when the implementation made a non-obvious choice. Each block:

- Opens by naming the concern.
- States the decision as a fact, not a goal.
- Backs every quantitative claim with a number, and every reused component with a `\cite`.
- Defers exhaustive lists to the repository documentation, with a pointer.

Recurring concern types:

| Concern | Content |
|---------|---------|
| Coverage | Fraction of target-language features supported, as "X of Y", per version. Name the hard cases handled. Point to the documented full list. |
| Reused component | The external library adopted and the one concrete reason it was chosen, cited. |
| Multi-backend artifact | Two implementations of one core structure, the trade-off each makes, and the measured threshold that selects between them. |
| Performance | The optimization applied, named to a specific stage, and the mechanism that keeps it correct. |

## Quantification

- Coverage: "X of Y built-in functions and constructs", one figure per supported version.
- Threshold: state the exact switch point, with its unit (e.g., lines of code).
- No bare adjective where a number exists. "112 of 122" not "most".

## Invariants

- Every paragraph reports a decision the approach section did not specify.
- Every quantitative claim has a number; every reused component has a citation.
- No method step, no algorithm, no result. Engineering facts only.
- Exhaustive enumerations live in the repository documentation, reached by a pointer.
