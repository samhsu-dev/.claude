---
paths:
  - "**/*.tex"
  - "**/*.bib"
  - "**/*.sty"
  - "**/*.cls"
---

# LaTeX Source Quality

## Source Formatting

- One sentence per source line. Never split a sentence across lines; never put two sentences on one line.
- A list whose items are short noun phrases may put each `\item` on its own line.
- No hard wrapping at a fixed column.
- Indent environment bodies by two spaces. No tabs in `.tex` files.
- A blank line separates paragraphs. No `\\` for a paragraph break.
- Non-breaking space before a citation and a reference: `text~\cite{key}`, `Section~\ref{sec:label}`.
- The first line of a section file is `% !TeX root = ../main.tex`.

## File Organization

- `main.tex` holds the preamble, `\begin{document}`, the `\input` calls, and `\end{document}`.
- One `.tex` file per section, named by its topic: `introduction.tex`, `evaluation.tex`.
- Sections are loaded with `\input{}`, never `\include{}`.

## Labels and References

- A label is `<prefix>:<name>` with prefix `sec:`, `subsec:`, `fig:`, `tab:`, `eq:`, `lst:`, or `app:`, and a lowercase name whose parts are joined by `_` or `:` (`sec:related_works`, `subsec:eval:setup`).
- Reference with `\autoref{}` or `\cref{}`. No hard-coded section, figure, or table numbers.
- Every `\label` has at least one reference, and every reference has its `\label`.
- In a float, `\label` follows `\caption`.

## Citations and Bibliography

- Every `\cite` key exists in a `.bib` file. Every entry of `references.bib` is cited.
- A title is in title case, with capitals that must survive protected by braces: `{C} Programming Language`.
- A DOI is stored without the `https://doi.org/` prefix.

## Figures

- Diagrams and plots are vector PDF; screenshots are PNG. No JPEG.
- Every figure has `\caption{}` and then `\label{fig:name}`.
- A multi-panel figure uses `subcaption`. Never load `subcaption` and `subfigure` together.

## Tables

- Rules are `\toprule`, `\midrule`, and `\bottomrule` from `booktabs`. No `\hline`, no vertical rules.
- Every table has `\caption{}` and `\label{tab:name}`.

## Numbers and Units

- No `siunitx`. Write numbers bare: `26 million`, `20\%`, `\$20,000`.
- Non-breaking space between a number and its unit: `7146~s`, `4~years`.
- Spell out an integer under 10 in prose ("three tools"). Exception: write digits for a count beside a rate or in the same list as a number of 10 or more ("2 bind 14--16, 14 bind 10--13").

## Commands and Macros

- A project term used three or more times is a `\newcommand` in `Packages/local.tex`.
- A macro followed by a space is written with `{}`: `\sys{} is`.
- `\todo{text}` marks unfinished text. No `\todo` remains at submission.

## Revision Markup

`Packages/revision.tex` defines the markup of the revised version.

- `\revision{old}{new}` wraps only the changed words; the common prefix and suffix stay outside. A whole-sentence `\revision` is only for a rewritten sentence.
- A new passage of several sentences goes in `revisionenv`.
- A grammar, hyphenation, spacing, or macro-brace edit (`previously-unknown` to `previously unknown`, `\sys` to `\sys{}`) carries no markup.
- A number not yet measured is `\revisiondata{tag}`, or `\revisionvalue{old}{tag}` inside a macro. Never write an estimate in its place.
- A change proposed for the author's review is `\changedBy{new}{old}` until the author approves it; then it becomes `\revision{old}{new}`.
- After narrowing a `\revision`, the old view and the new view each read unchanged.

## Package Management

- No duplicate `\usepackage`.
- `hyperref` loads after every package except `cleveref`, which loads after `hyperref`.
- Each `\usepackage` carries a comment stating its purpose on the same line.

## Compilation Verification

- After every edit, `latexmk -pdf` finishes with no `!` error, no undefined reference or citation, and no overfull box over 1pt.
- Clean with `latexmk -C`.
