---
paths:
  - "**/design.md"
---

# LaTeX Paper Structure

Document architecture for academic papers.

---

## Document Layout

- Single `main.tex` root. All content via `\input` or `\include`.
- For multi-file projects: one `.tex` file per section, named by topic (`introduction.tex`, `evaluation.tex`).
- Section files: body text only. `\section` headings can live in `main.tex` or a dispatcher file.

## Standard Sections (SE/CS Conference)

| Order | Section | Purpose |
|-------|---------|---------|
| 1 | Abstract | Problem, method, result, contribution |
| 2 | Introduction | Motivation, gap, thesis, contributions |
| 3 | Background / Overview | Running example, definitions, threat model |
| 4 | Approach | Design, algorithms, formal definitions |
| 5 | Implementation | Engineering details, tools |
| 6 | Evaluation | RQs, methodology, results |
| 7 | Discussion | Threats to validity, limitations |
| 8 | Related Work | Prior work comparison |
| 9 | Conclusion | Summary, future work |

Adapt order and section names to venue requirements.

## Float Placement

- `\begin{figure}[t]` or `\begin{figure*}[t]` for top placement. Avoid `[h]` and `[H]`.
- Tables near first reference. Figures near discussion.
- Full-width: `figure*` / `table*` in two-column layouts.

## Cross-Reference Design

- Label immediately after the element: `\section{Intro}\label{sec:intro}`.
- In floats: `\label` after `\caption` (technical requirement).
- Forward references require two compilation passes.
