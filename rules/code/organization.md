---
paths:
  - "**/*.{py,ts,tsx,js,jsx,go,rs,java,cpp,c,cs,rb,swift,kt,php}"
---

# File Naming and Organization

One naming logic for every project, independent of language. Language-specific casing, layout, and packaging: see project `.claude/rules/code/organization.md`.

## File Responsibility

- One responsibility per file. All types and functions in a file serve that responsibility.
- Files under 300 lines. Extract a new file when a second responsibility emerges.
- Splits follow responsibility boundaries, never line count alone. A split that leaves a fragment without a nameable responsibility is wrong.
- A file exceeding the size limit becomes a directory of the same name; the directory's index file re-exports the original names so import paths survive the split.

## File Naming

- The file name states the single responsibility the file owns.
- File names contain lowercase letters, digits, and underscores only. No dashes, dots, spaces, or uppercase.
- File names are domain nouns, never pattern roles. No `utils`, `helpers`, `common`, `shared`, `misc`, `manager`, `handler` as a file name.
- Never name a file after one class it contains when the file owns a broader responsibility. The file names the responsibility; the class names the instance.
- One grammatical number for file and directory names across a codebase. Never singular and plural variants of the same name.

## Directory Organization

- Directories group files by domain feature, not by architectural layer. Exception: framework-mandated layer files inside a feature directory.
- No `utils/`, `helpers/`, `common/`, `misc/` directories. A shared function belongs to the module that owns its theme.

## Entry Points

- Entry-point files contain argument parsing and delegation only. Business logic lives in importable modules.
