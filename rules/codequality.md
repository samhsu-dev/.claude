---
paths:
  - "**/*.tex"
  - "**/*.bib"
  - "**/*.sty"
  - "**/*.cls"
---

# LaTeX Source Quality

Community standards: dspinellis/latex-advice, booktabs, Kopka & Daly.

---

## Source Formatting

- A complete sentence occupies one source line. Never split a sentence across multiple lines.
- Break only at sentence boundaries or at the boundary between two independent clauses joined by a coordinating conjunction.
- A bulleted or enumerated prose list whose items are short noun phrases may place each item on its own line. Running prose that contains a list stays on one line.
- No hard wrapping at fixed column width. Let the editor soft-wrap.
- Indent environment bodies consistently (two spaces). No tabs in `.tex` files.
- Blank line between paragraphs. No `\\` for paragraph breaks in body text.
- Non-breaking space before citations: `text~\cite{Key}`.
- Non-breaking space before references: `Section~\ref{sec:label}`, `Figure~\ref{fig:name}`.
- Sub-files carry `% !TeX root = ../main.tex` as the first line.

## File Organization

- `main.tex`: root document. Preamble, `\begin{document}`, `\input` calls, `\end{document}`.
- One `.tex` file per section. Filename matches topic: `introduction.tex`, `evaluation.tex`.
- Use `\input{}` (no page break) for sections. Use `\include{}` (page break) for chapters only.

## Labels and References

- Format: `\label{<type>:<name>}`. Standard prefixes: `sec:`, `fig:`, `tab:`, `eq:`, `lst:`, `app:`.
- Names: lowercase with underscores: `sec:related_works`, `fig:system_overview`.
- Use `\autoref{}` or `\cref{}`. No hardcoded numbers.
- Every `\label` has at least one `\ref`. Every `\ref` has a corresponding `\label`.
- `\label` after `\caption` in floats: `\caption` calls `\refstepcounter`, so `\label` before it captures the wrong counter.

## Citations and Bibliography

- No orphan citations. Every `\cite` key exists in `.bib`. Every `.bib` entry is cited.
- Title in title case. Protect capitalization with braces: `{C} Programming Language`.
- Store DOI without resolution prefix (dspinellis/latex-advice).

## Figures

- Vector (PDF) for diagrams and plots. Raster (PNG) for screenshots. No JPEG for text/diagrams.
- Every figure has `\caption{}` and `\label{fig:name}` (label after caption).
- `subcaption` for multi-panel figures. Do not load both `subcaption` and `subfigure`.

## Tables

- `booktabs`: `\toprule`, `\midrule`, `\bottomrule`. No `\hline`. No vertical rules.
- Every table has `\caption{}` and `\label{tab:name}`.

## Numbers and Units

- This project does not load `siunitx`. Write numbers bare: `26 million`, `20\%`, `\$20,000`. No `\num{}`/`\qty{}`/`\unit{}`.
- Non-breaking space between a number and its unit: `7146~s`, `4~years`.
- Spell out integers under 10 in prose ("three tools", not "3 tools").

## Commands and Macros

- `\newcommand` for project terms appearing 3+ times.
- After macro invocation, use `{}` to prevent space swallowing: `\sys{} is a tool`.
- `\todo{text}` for unfinished sections. Remove before submission.

## Package Management

- No duplicate `\usepackage`. Check before adding.
- `hyperref` loads near-last. `cleveref` loads after `hyperref`.
- Comment each `\usepackage` with its purpose on the same line.

## Compilation Verification

After every edit:
- Zero compilation errors (`!` lines in log).
- Zero undefined references and citations.
- No overfull hboxes exceeding 1pt.

Build command: `latexmk -pdf`. Clean: `latexmk -C`.
