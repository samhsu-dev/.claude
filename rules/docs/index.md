---
paths:
  - "**/index.md"
---

# Index Document Standards

Developer-facing navigation for documentation directories. Routes agents to the correct file without forcing a full read.

---

## Scope

- One `index.md` per documentation directory that contains 3+ files or any split documents (`*-model.md`, `*-design.md`).
- Contains file list with one-line descriptions. No domain content, no concepts, no code.
- Loaded first when an agent enters a documentation directory. All other files loaded on demand.

## Structure

```markdown
# <Module Name> — <one-line role>

| File | Content |
|------|---------|
| idea.md | <what concepts it covers> |
| <topic>-model.md | <what domain semantics it covers> |
| design.md | <what software structure it covers> |
| impl.md | <what external APIs it covers> |
```

- H1: module name + role. One line.
- One table. Columns: File (relative path), Content (one-line description).
- File column: exact filename, no path prefix.
- Content column: under 80 characters. States what the file covers, not what it is.
- Rows ordered: idea → model files → design files → impl → todo.

## When to Split

- Any `model.md` or `design.md` exceeding 200 lines: split into `<topic>-model.md` or `<topic>-design.md`.
- Split by concept, not by section heading. Each file covers one self-contained topic.
- After splitting: delete the original monolithic file. Update `index.md`.

## Naming Convention

- Concept files: `<topic>-model.md` (e.g., `entities-model.md`, `state-model.md`).
- Design files: `<topic>-design.md` (e.g., `extensions-design.md`).
- Topic name: noun or noun phrase. No verbs, no abbreviations.
- Suffix matches the document type rule (`-model.md` triggers `modeling.md` rules, `-design.md` triggers `designing.md` rules).

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
