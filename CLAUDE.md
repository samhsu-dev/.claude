# Project Rules

LaTeX academic paper project. Global rules (`~/.claude/rules/`) provide language-agnostic standards. Project rules below add LaTeX-specific guidance.

## Recommended Project Structure

```
paper/
├── main.tex              # Root document
├── references.bib        # Bibliography database
├── Sections/             # One .tex file per section (optional for short papers)
├── figures/              # PDF/PNG figures
├── tables/               # Standalone table .tex files (optional)
├── *.sty / *.cls         # Local style/class files (project root or subdir)
├── .latexmkrc            # Build configuration (optional)
└── .claude/
    ├── CLAUDE.md         # This file
    └── rules/
        ├── codequality.md  # LaTeX source quality (*.tex, *.bib, *.sty)
        ├── committing.md   # Project commit and push rules
        ├── designing.md    # Paper structure and layout (design.md)
        ├── implementing.md # Package/macro conventions (*implementation.md)
        ├── tasking.md      # Task management (todo.md)
        └── idea.md         # Research ideas and argumentation (idea.md)
```

Rules use `paths:` frontmatter to load only when working with matching files.

## Build System

- Engine: `pdflatex`, `xelatex`, or `lualatex`.
- Build tool: `latexmk -pdf` (recommended), or editor-integrated (TeXShop / VS Code LaTeX Workshop).
- Multi-pass sequence: `pdflatex` -> `bibtex` -> `pdflatex` -> `pdflatex`. `latexmk` automates this.
- Output directory: configurable via `-outdir=` flag or `.latexmkrc`. No fixed name.
- Bibliography: `bibtex` with venue `.bst`, or `biblatex` + `biber` for new projects.
