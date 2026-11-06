---
paths:
  - "**/related_works.tex"
  - "**/related-works.tex"
  - "**/relatedwork.tex"
---

# Related Works Structure

The section partitions prior work by methodology, not by chronology. Each category is one paragraph that moves from foundational work to recent work, then closes by contrasting the category against our approach. The reader sees where every cited work sits in the methodological landscape and how our work differs from each category.

---

## Section Order

| # | Block | Function |
|---|-------|----------|
| 1 | Opening | One sentence naming the categories the section covers, in body order |
| 2 | Category I..N | One paragraph per methodological category |
| 3 | Other works | Trailing paragraph for cited work that fits no category |

## Opening Block

- One sentence: "we discuss the related work in the field of X, Y, and Z for <domain>."
- The categories named here equal the category paragraphs in the body, same names, same order.
- No citations in the opening. The opening is a map.

## Category Paragraphs

One paragraph per category, headed by an italic title macro (`\emph{Title.}`). Each paragraph:

- Opens on a one-sentence definition of the category's methodology, binding the category's acronym (PIA, MDA, AIH) used elsewhere in the paper.
- Orders cited works oldest to newest. Foundational work first, recent work last.
- Introduces each work by author surname inline, then `~\cite{key}`, then states the work's contribution in one clause.
- Names the system or tool the cited work introduced when it has a name.
- Closes by stating the category's shared limitation and contrasting it against the named \sys{} innovation that resolves it.

Rules:
- Category count in the body equals the category count named in the opening.
- A cited work appears in exactly one category.
- Each category ends on the contrast: what the category does versus the named \sys{} innovation that resolves its limitation.
- The contrast states a methodological difference, not a quality judgment.
- Category acronyms (PIA, MDA, AIH) and innovation names match the introduction and overview verbatim.

## Citation Conventions

- Author surnames written inline, citation bound with a non-breaking space: `Felmetsger et al.~\cite{key}`. The project uses plain `bibtex` + IEEEtran, so `\citeauthor` is unavailable.
- One author: surname. Two authors: both surnames. Three or more: first surname plus "et al.".
- A named system is introduced once, then referred to by its macro or name.
- Transition adverbs mark chronology: "Early research", "Later on", "More recently", "A major advancement".
- Numeric claims about a cited work (counts, percentages) are backed by that work or removed.

## Contrast Discipline

- Every category paragraph ends by distinguishing our approach from that category.
- The contrast names the concrete axis of difference: execution model, analysis target, deployment cost, or scope.
- Phrasing states a difference in aim or method: "a substantially different approach", "differs from our goal of X".
- No claim of superiority without a stated, verifiable axis.

## Revision Markup

- New text added during reviewer response is wrapped in `\begin{revisionenv}...\end{revisionenv}`.
- Commented-out author notes use `%` and are removed before submission.

## Invariants

- Categories named in the opening match category paragraphs in body, in order.
- Each cited work appears in exactly one category.
- Each category paragraph orders works oldest to newest.
- Each category paragraph closes on a methodological contrast with our approach.
- Author-name citations use `\citeauthor{key}~\cite{key}` on first mention.
