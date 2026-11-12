---
paths:
  - "**/*.{py,ts,tsx,js,jsx,go,rs,java,cpp,c,cs,rb,swift,kt,php}"
---

# File Naming and Organization

Language-specific casing, layout, and packaging: see project `.claude/rules/code/organization.md`.

## File Responsibility

- One responsibility per file. All types and functions in a file serve that responsibility.
- Files under 300 lines. Extract a new file when a second responsibility emerges. Exception: a standalone tool script — a single-invocation script outside the shipped package (e.g. under `tools/`) — stays one file regardless of length.
- Splits follow responsibility boundaries, never line count alone. A split that leaves a fragment without a nameable responsibility is wrong.
- A file exceeding the size limit becomes a directory of the same name; the directory's index file re-exports the original names so import paths survive the split.

## File Naming

- The file name states the single responsibility the file owns.
- Filename stems use lowercase letters, digits and underscores; extensions are excluded.
- A file name is a domain noun, never a pattern role such as `utils`, `helpers`, `common`, `shared`, `misc`, `manager` or `handler`, alone or as a suffix.
- Never name a file after one class it contains when the file owns a broader responsibility.
- File and directory names use the grammatical number of their existing sibling names. Never singular and plural variants of the same name.

## Directory Organization

- Directories group files by domain feature, not by architectural layer. Exception: framework-mandated layer files inside a feature directory.
- No `utils/`, `helpers/`, `common/`, `misc/` directories. A shared function belongs to the module that owns its theme.
- A directory names the domain concept its files serve, never a language mechanism or pattern role (`extension/`, `impl/`, `workers/`).
- A directory whose files serve several nameable domain concepts splits into one subdirectory per concept.
- Files that share a concern form one directory with one public entry point.

## Dependencies

- Package and module dependencies form an acyclic graph. A lower layer never imports a higher one; a type both need moves down to the layer that owns its concept.
- Domain-independent machinery carries no domain policy and lives in the lowest package or library that can own it. A domain rule reaches it as a parameter.

## Entry Points

- Entry-point files contain argument parsing and delegation only. Business logic lives in importable modules. Exception: a standalone tool script holds its own logic.
