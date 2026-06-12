# Project Rules

LaTeX academic paper project (BELUGA). This file is the project interface: structure, rule index, and build system.

## Project Structure

```
paper/
├── main.tex              # Root document
├── references.bib        # Bibliography database
├── zotero-references.bib # Zotero-exported bibliography
├── Sections/             # One .tex file per section (introduction, overall, ...)
├── Packages/             # Local style and preamble (myart.sty, packages.tex, ...)
├── Assets/               # Figures and other binary assets
├── Templates/            # Venue templates
├── Revisions/            # Reviewer-response material
└── .claude/
    ├── CLAUDE.md         # This file
    └── rules/            # Project rules (see Rules below)
```

## Rules

`.claude/rules/` holds the project rules. Each uses `paths:` frontmatter to load only when a matching file is open; a rule with no `paths:` is always active.

| Rule | Scope (`paths:`) | Purpose |
|------|------------------|---------|
| `codequality.md` | `*.tex`, `*.bib`, `*.sty`, `*.cls` | LaTeX source quality |
| `writing.md` | `*.tex` | Academic prose precision; no vague terms |
| `writing-references.md` | always active | Bibliographic backing for `writing.md` authorities |
| `introduction.md` | `introduction.tex`, `intro.tex` | Introduction structure |
| `overall.md` | `overall.tex`, `overview.tex` | Overview structure |
| `approach.md` | `approach.tex`, `approaches.tex` | Approach structure |
| `committing.md` | always active | Project commit and push rules |

Global rules (`~/.claude/rules/`) provide language-agnostic defaults. These project rules add LaTeX-specific guidance and override the global defaults where both set a concrete value.

## Build System

- Engine: `pdflatex`, `xelatex`, or `lualatex`.
- Build tool: `latexmk -pdf` (recommended), or editor-integrated (TeXShop / VS Code LaTeX Workshop).
- Multi-pass sequence: `pdflatex` -> `bibtex` -> `pdflatex` -> `pdflatex`. `latexmk` automates this.
- Output directory: configurable via `-outdir=` flag or `.latexmkrc`. No fixed name.
- Bibliography: `bibtex` with venue `.bst`, or `biblatex` + `biber` for new projects.
