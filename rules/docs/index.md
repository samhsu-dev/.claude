---
paths:
  - "**/index.md"
---

# Index Document Standards

Developer-facing navigation for documentation directories. Routes agents to the correct file without forcing a full read.

---

## Scope

- One `index.md` per documentation directory that contains 3+ files or any split documents (`concept-*.md`, `model-*.md`, `design-*.md`, `spec-*.md`, `impl-*.md`).
- Contains file list with one-line descriptions. No domain content, no concepts, no code.
- Loaded first when an agent enters a documentation directory. All other files loaded on demand.

## Structure

```markdown
# <Module Name> — <one-line role>

| File | Content |
|------|---------|
| concept.md | <what concepts it covers> |
| model.md | <what domain semantics it covers> |
| design.md | <what software structure it covers> |
| spec.md | <what algorithms it covers> |
| impl.md | <what external APIs it covers> |
| todo.md | <what tasks remain> |
```

- H1: module name + role. One line.
- One table. Columns: File (relative path), Content (one-line description).
- File column: exact filename, no path prefix.
- Content column: under 80 characters. States what the file covers, not what it is.
- Rows ordered: concept → model → design → spec → impl → todo.

## When to Split

- Any doc file exceeding 200 lines: split by concern using prefix naming.
- Split by concept, not by section heading. Each file covers one self-contained topic.
- After splitting: delete the original monolithic file. Update `index.md`.

## Naming Convention

Split files use `<type>-<topic>.md` prefix naming:

| Type | Single | Split |
|------|--------|-------|
| Concept | `concept.md` | `concept-<topic>.md` |
| Model | `model.md` | `model-<topic>.md` |
| Design | `design.md` | `design-<topic>.md` |
| Spec | `spec.md` | `spec-<topic>.md` |
| Implementation | `impl.md` | `impl-<topic>.md` |

- Topic name: noun or noun phrase. No verbs, no abbreviations.
- Prefix matches the document type rule (`model-` triggers `model.md` rules, `design-` triggers `design.md` rules).

## Content Rules

- No domain content. "ADG node types and their semantic roles" not a definition of what ADG node types are.
- No redundancy with file content. The description says what topic the file covers; the file itself has the content.
- No hierarchy or nesting. Flat table. No subsections, no grouping headers.
- No external links. All entries point to files in the same directory.

## Multi-Level Navigation

- Top-level `index.md` links to subdirectory `index.md` files, not to individual files within subdirectories.
- Entry format for subdirectories: `<dirname>/index.md` with a one-line description of the subdirectory scope.
- Two levels maximum. No `index.md` linking to another `index.md` linking to another `index.md`.

## Verification

- Every file in the directory appears in `index.md`.
- Every entry in `index.md` points to an existing file.
- No file exceeds 200 lines. Split and update `index.md` when exceeded.
