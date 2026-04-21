---
paths:
  - "**/*.tex"
  - "**/*.bib"
  - "**/*.sty"
  - "**/*.cls"
---

# LaTeX Source Quality

Community standards: dspinellis/latex-advice, booktabs, siunitx v3, Kopka & Daly.

---

## Source Formatting

- One clause or phrase per line. Break after logical units. Improves Git diffs (dspinellis/latex-advice).
- No hard wrapping at fixed column width. Let the editor soft-wrap.
- Indent environment bodies consistently (two spaces common). No tabs in `.tex` files.
- Blank line between paragraphs. No `\\` for paragraph breaks in body text.
- Non-breaking space before citations: `text~\cite{Key}`.
- Non-breaking space before references: `Section~\ref{sec:label}`, `Figure~\ref{fig:name}`.

## File Organization

Single-file is the community default for conference/journal papers. Split into per-section files only when:
- Multiple authors edit in parallel.
- Document exceeds ~30 pages.
- `\includeonly` speeds up partial builds.

When splitting:
- `main.tex`: root document. Preamble, `\begin{document}`, `\input` calls, `\end{document}`.
- One `.tex` file per section. Filename matches topic: `introduction.tex`, `evaluation.tex`.
- Use `\input{}` (no page break) for sections. Use `\include{}` (page break) for chapters in long documents.

## Labels and References

- Format: `\label{<type>:<name>}` (dspinellis/latex-advice, latex2e examples).
- Standard prefixes: `sec:`, `fig:`, `tab:`, `eq:`, `lst:`, `app:`.
- Names: lowercase, underscores: `sec:related_works`, `fig:system_overview`.
- `\ref{}`, `\autoref{}`, or `\cref{}` (cleveref). No hardcoded numbers.
- Every `\label` has at least one `\ref`. Every `\ref` has a corresponding `\label`.
- `\label` after `\caption` in floats. Technical requirement: `\caption` calls `\refstepcounter`, so `\label` before `\caption` captures the wrong counter.

## Citations and Bibliography

- BibTeX keys: one common convention is `AuthorYY` (e.g., `Ker08`, `DMG07`). Other schemes (`smith2020`, `smith:2020:topic`) are valid. Pick one, use consistently.
- `.bib` files: one entry per key, sorted alphabetically.
- Multiple `.bib` files for distinct categories (e.g., `references.bib`, `softwares.bib`).
- No orphan citations. Every `\cite` key exists in `.bib`. Every `.bib` entry is cited.
- Title in title case. Protect capitalization with braces: `{C} Programming Language`.
- Use `doi2bib.org` for generating entries. Store DOI without resolution prefix (dspinellis/latex-advice).

## Figures

- Vector (PDF) for diagrams and plots. Raster (PNG) for screenshots. No JPEG for text/diagrams.
- `\includegraphics[width=\columnwidth]{figures/name.pdf}`. Use relative paths.
- Every figure has `\caption{}` and `\label{fig:name}` (label after caption).
- `subcaption` package for multi-panel figures. Conflicts with `subfigure` -- use one.

## Tables

- `booktabs`: `\toprule`, `\midrule`, `\bottomrule`. No `\hline`. No vertical rules (booktabs author recommendation).
- Align `&` separators in source with spaces or tabs for readability (dspinellis/latex-advice).
- Every table has `\caption{}` and `\label{tab:name}`.

## Numbers and Units

- `siunitx` v3: `\num{12345}` for numbers, `\qty{7146}{s}` for number+unit, `\unit{m}` for standalone units.
- `\qty` replaces deprecated `\SI`. `\unit` replaces deprecated `\si`.
- Spell out integers under 10 in prose ("three tools", not "3 tools").

## Commands and Macros

- `\newcommand` for project terms appearing 3+ times.
- After macro invocation, use `{}` or `\ ` to prevent space swallowing: `\sys{} is a tool`. `\xspace` is convenient but has known edge cases where it incorrectly adds or omits spaces.
- `\todo{text}` for unfinished sections. Remove before submission.

## Package Management

- No duplicate `\usepackage`. Check before adding.
- `hyperref` loads near-last. It redefines `\ref`, `\cite`, sectioning, and more.
- `cleveref` loads after `hyperref` (hard requirement).
- Comment: `% purpose` on same line or line above each `\usepackage`.

## Editor Magic Comments

Editor convention (TeXShop, TeXworks, TeXstudio, VS Code LaTeX Workshop), not a LaTeX language feature. Widely supported:
```
% !TeX program = pdflatex
% !TeX root = main.tex
```

In sub-files: `% !TeX root = ../main.tex` for single-file compilation.

---

## Compilation Verification

After every edit:
- Zero compilation errors (`!` lines in log).
- Zero undefined references (`Reference ... undefined`).
- Zero missing citations (`Citation ... undefined`).
- No overfull hboxes exceeding 1pt.
- PDF renders correctly at edited section.

### Common Errors
- `! Undefined control sequence`: typo or missing `\usepackage`.
- `! Missing $ inserted`: math symbol outside `$...$`.
- `! Extra alignment tab`: more `&` than table columns.
- `Reference ... undefined`: missing `\label` or stale `.aux`. Recompile twice.
- `Citation ... undefined`: missing `.bib` entry or `bibtex` not run.
- Stale build: `latexmk -C` then rebuild.

---

## Toolchain

| Tool | Command | Purpose |
|------|---------|---------|
| latexmk | `latexmk -pdf` | Multi-pass compilation (recommended) |
| pdflatex | `pdflatex -interaction=nonstopmode` | Single-pass compilation |
| bibtex | `bibtex <jobname>` | Bibliography processing |
| chktex | `chktex *.tex` | LaTeX linter (also via TexLab/LSP) |

---

## External Tools

- Context7: LaTeX package docs before integration.
- DeepWiki: reference project structure and patterns.

## Workflow

- No summary/README generation after task completion. Update existing files only.
