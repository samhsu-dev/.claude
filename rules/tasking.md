---
paths:
  - "**/todo.md"
---

# LaTeX Task Management

Paper-specific task conventions.

---

## Quality Gate

Every task ends with:
- [ ] `latexmk -pdf main.tex` -- zero errors
- [ ] Zero undefined references in log
- [ ] Zero missing citations in log
- [ ] PDF visually correct at edited section

## Conventions

- Design docs by relative path: `Depends on: path/to/design.md`.
- Section tasks name the section file: `Sections/<topic>.tex` or `<topic>.tex`.
- Figure tasks name the asset: `figures/<name>.pdf`.
- Table tasks name the asset: `tables/<name>.tex`.
- Implementation tasks reference `implementation.md` for package findings.
