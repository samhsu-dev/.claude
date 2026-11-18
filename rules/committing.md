# Project Commit Rules

Extends global `committing.md`.

## Pre-Push

- Rebase onto `main` before every push.
- Resolve every conflict before pushing.

## LaTeX-Specific

- Never commit build artifacts (`.aux`, `.log`, `.bbl`, `.blg`, `.out`, `.toc`, `.fls`, `.fdb_latexmk`, `.synctex.gz`) or build output directories.
- Never commit the output PDF unless the user requests it.
- `.gitignore` extends the `github/gitignore` TeX.gitignore template.
- Commit a `.bib` file in the same commit as the `.tex` files that cite its new entries.
- Commit a figure's source file (`.drawio`, `.svg`) in the same commit as its exported PDF.
- When adding several binary figures (PDF, PNG), commit one figure per commit.
