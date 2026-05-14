---
paths:
  - "**/index.md"
---

# Index Document Standards

Developer-facing navigation for documentation directories. Routes agents to the correct file without forcing a full read.

---

## Scope

- One `index.md` per documentation directory that contains 3+ files or any split documents (`idea-*`, `model-*`, `spec-*`, `design-*`, `impl-*`).
- Contains file list with one-line descriptions. No domain content, no concepts, no code.
- Loaded first when an agent enters a documentation directory. All other files loaded on demand.

## Structure

```markdown
# <Module Name> — <one-line role>

| File | Content |
|------|---------|
| idea.md | <what concepts it covers> |
| model-<topic>.md | <what domain semantics it covers> |
| design.md | <what software structure it covers> |
| impl.md | <what external APIs it covers> |
```

- H1: module name + role. One line.
- One table. Columns: File (relative path), Content (one-line description).
- File column: exact filename, no path prefix.
- Content column: under 80 characters. States what the file covers, not what it is.
- Rows ordered: idea → model → spec → design → impl → todo (pipeline order).

## When to Split

- Any document exceeding 200 lines: split into prefixed topic files.
- After splitting: delete the original monolithic file. Update `index.md`.

### Split Logic

Split by domain concept. Never by section heading, file type, or mechanical line count.

- Identify the domain concepts the document covers. Each concept that can be understood independently becomes one file.
- Related content stays together: an entity's definition, its state transitions, and its invariants belong in one file — not three files split by "entities", "states", "invariants".
- Cross-referencing concepts that cannot be understood without each other stay in the same file.
- A split file may contain content from multiple document types if they serve the same domain concept. Domain coherence over document-type purity.
- Test: "Can a reader understand this file without reading the sibling files?" Yes → good split. No → merge back.

## Naming Convention

Split files use the document-type name as prefix, followed by the topic name:

| Prefix | Document type | Example |
|--------|---------------|---------|
| `idea-` | Concept | `idea-dataflow.md` |
| `model-` | Domain model | `model-entities.md`, `model-state.md` |
| `spec-` | Algorithm | `spec-fixpoint.md` |
| `design-` | Design | `design-extensions.md`, `design-pipeline.md` |
| `impl-` | Implementation | `impl-serialization.md` |

- Prefix: document type name + hyphen. Alphabetical sort groups same-type files together.
- Topic name: noun or noun phrase. No verbs, no abbreviations.
- Prefix triggers the corresponding document type rule (`model-*.md` triggers `model.md` rules, `design-*.md` triggers `design.md` rules).

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
