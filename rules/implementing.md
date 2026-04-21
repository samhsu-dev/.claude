---
paths:
  - "**/*implementation.md"
---

# LaTeX Implementation Documents

Package and macro integration conventions.

---

## Package Entry Format

**[package]** `\usepackage[options]{package}` -- when/gotcha.

Example:
**[booktabs]** `\usepackage{booktabs}` -- `\toprule`, `\midrule`, `\bottomrule`. No vertical rules.
**[siunitx]** `\usepackage{siunitx}` -- `\qty{value}{unit}` (v3). Replaces deprecated `\SI`.
**[subcaption]** `\usepackage{subcaption}` -- conflicts with `subfigure`. Use one.
**[hyperref]** `\usepackage{hyperref}` -- load near-last. `cleveref` loads after.

## Macro Entry Format

- `\newcommand{\name}{expansion}` -- purpose. File where defined.

## Load Order Rules

1. Most packages (order-independent).
2. `hyperref` (near-last, redefines many internals).
3. `cleveref` (after `hyperref`, hard requirement).

## Verification

- Check `implementation.md` for existing findings before adding `\usepackage`.
- Record all package conflicts, load-order requirements, and option gotchas immediately.
- Verify via Context7, package documentation (`texdoc <package>`), or minimal test document. No guessing.
- Test new packages in a minimal `.tex` file before integrating.
