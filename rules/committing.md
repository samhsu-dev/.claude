# Project Commit Rules

Extends global `committing.md`. No duplication -- project-specific additions only.

## Pre-Push

- Rebase onto main before every push.
- Resolve all conflicts before pushing. Never push with unresolved conflicts.
- Never force-push without explicit user approval.

## LaTeX-Specific

- Never commit build artifacts: `.aux`, `.log`, `.bbl`, `.blg`, `.out`, `.toc`, `.fls`, `.fdb_latexmk`, `.synctex.gz`.
- Never commit build output directories.
- Never commit the output PDF unless explicitly requested (e.g., camera-ready submission).
- Use the `github/gitignore` TeX.gitignore template as baseline.
- Commit `.bib` files alongside `.tex` files that cite them.
- Commit figure source files (`.drawio`, `.svg`) alongside exported PDFs.
- Binary figures (PDF, PNG): one figure per commit when adding multiple. Keeps diffs reviewable.
