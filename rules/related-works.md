---
paths:
  - "**/related_works.tex"
  - "**/related-works.tex"
  - "**/relatedwork.tex"
---

# Related Works Structure

## Section Order

| # | Block | Content |
|---|-------|---------|
| 1 | Opening | The axes or categories that partition prior work, in body order |
| 2 | Category I..N | One paragraph per methodological category |
| 3 | Other works | One final paragraph for cited work that fits no category |

## Opening Block

- The opening names the axes or categories with `\sys{}` as subject or as the work being placed: "\sys{} relates to prior work along two axes: ...".
- The categories it names equal the category paragraphs in name and order.
- No citation and no self-narration ("we discuss") in the opening.

## Category Paragraphs

- Each paragraph starts with an italic title `\emph{Title.}`.
- The first sentence defines the category's method.
- Cited works appear oldest first.
- Each work is introduced by author surname, then `~\cite{key}`, then its contribution in one clause. A named system the work introduced is named.
- A cited work appears in exactly one category.
- The last sentence contrasts the category with `\sys{}` on one stated axis: execution model, analysis target, deployment cost, or scope. The contrast names the `\sys{}` mechanism that differs and states no quality judgment.
- Category and mechanism names match the introduction and the overview verbatim.

## Citation Conventions

- Author citation: `Felmetsger et al.~\cite{key}`. `\citeauthor` is unavailable under `bibtex` with IEEEtran.
- One author: the surname. Two authors: both surnames. Three or more: the first surname and "et al.".
- A named system is introduced once, then referred to by its macro or name.
- Chronology is marked by "Early research", "Later on", "More recently".
- A number about a cited work comes from that work. Otherwise delete the number.
