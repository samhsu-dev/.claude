---
paths:
  - "**/index.md"
---

# Index Document Standards

---

## Scope

- One `index.md` per documentation directory that contains 3+ files or any split documents; the change that adds, renames or removes a documentation file updates `index.md` of its directory.
- Contains file list with one-line descriptions. No code.
- An agent reads a documentation directory's `index.md` before it reads another file of that directory. All other files loaded on demand.

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
- A committed navigation index lists committed docs only; indexes inside local record directories follow `rules/workflow/records.md`.

## Naming Convention

- Topic name: noun or noun phrase. No verbs, no abbreviations.

## Content Rules

- No domain content: a Content cell names the topic, never its definition.
- No redundancy with file content. The description says what topic the file covers; the file itself has the content.
- No hierarchy or nesting. Flat table. No subsections, no grouping headers.
- No external links. Entries target files in this directory or the subdirectory indexes specified in Multi-Level Navigation.

## Multi-Level Navigation

- Top-level `index.md` links to subdirectory `index.md` files, not to individual files within subdirectories.
- Entry format for subdirectories: `<dirname>/index.md` with a one-line description of the subdirectory scope.
- Three levels maximum, counted from the repository's own top-level `docs/index.md`; a submodule counts from its own. No `index.md` chain longer than three, and no cycle.

## Verification

- Every documentation file of the directory and every subdirectory `index.md` appears in the directory's `index.md`.
- Every entry in `index.md` points to an existing file.
