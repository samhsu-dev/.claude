---
paths:
  - "**/index.md"
---

# Index Document Standards

Developer-facing navigation for documentation directories. Routes agents to the correct file without forcing a full read.

---

## Scope

- One `index.md` per documentation directory that contains 3+ files or any split documents; update it after any development stage that adds or renames a file.
- Contains file list with one-line descriptions. No code.
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
```

- H1: module name + role. One line.
- One table. Columns: File (relative path), Content (one-line description).
- File column: a filename in this directory, or a subdirectory index path as specified in Multi-Level Navigation.
- Content column: under 80 characters.
- Rows ordered: concept → model → design → spec → impl.
- A committed navigation index lists committed docs only; indexes inside local record directories follow `CLAUDE.md` Local Records.

## When to Split

- Shared size limits and prefix naming: `CLAUDE.md` Documentation Naming.
- After splitting: delete the original monolithic file. Update `index.md`.

### Split Logic

Split within a document type by domain concept, not by section heading or mechanical line count.

- Identify the domain concepts the document covers. Each concept that can be understood independently becomes one file.
- Related content stays together: an entity's definition, its state transitions, and its invariants belong in one file — not three files split by "entities", "states", "invariants".
- Cross-referencing concepts that cannot be understood without each other stay in the same file.
- Keep each fact in the document type that owns it under `CLAUDE.md` Documentation Ownership. Link other types.
- A file explains its own concern. Follow links for adjacent concerns; merge fragments that need sibling text to define their own concern.

## Naming Convention

- Topic name: noun or noun phrase. No verbs, no abbreviations.

## Content Rules

- No domain content. "Graph node types and their semantic roles" not a definition of what the node types are.
- No redundancy with file content. The description says what topic the file covers; the file itself has the content.
- No hierarchy or nesting. Flat table. No subsections, no grouping headers.
- No external links. Entries target files in this directory or the subdirectory indexes specified in Multi-Level Navigation.

## Multi-Level Navigation

- Top-level `index.md` links to subdirectory `index.md` files, not to individual files within subdirectories.
- Entry format for subdirectories: `<dirname>/index.md` with a one-line description of the subdirectory scope.
- Two levels maximum. No `index.md` linking to another `index.md` linking to another `index.md`.

## Verification

- Every documentation file covered by the applicable index scope appears in `index.md`.
- Every entry in `index.md` points to an existing file.
