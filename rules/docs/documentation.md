---
paths:
  - "**/*.md"
---

# Documentation Standards

## Naming

Documents split by responsibility use prefix naming:

| Type | Single file | Split by concern |
|------|-------------|------------------|
| Concept | `concept.md` | `concept-{concern}.md` |
| Domain Model | `model.md` | `model-{concern}.md` |
| Design | `design.md` | `design-{concern}.md` |
| Spec | `spec.md` | `spec-{concern}.md` |
| Implementation | `impl.md` | `impl-{concern}.md` |
| Glossary | `glossary.md` | `glossary-{concern}.md` |

Each split file follows the same rules as its single-file counterpart. One concern per file. Glossary layout: `rules/docs/glossary.md`.

Every Markdown file in a repository: 200 lines max; `SKILL.md` follows `rules/meta/skilling.md` (`hooks/doc_check.py` reports an overrun of either). A document that exceeds the limit → split by concern using prefix naming above. A single concern that still exceeds the limit splits into its sub-concerns, each file named `<type>-{concern}-{sub-concern}.md`.

After splitting, delete the original monolithic file and update the directory's `index.md` (`rules/docs/index.md`).

Split within a document type by domain concept, not by section heading or mechanical line count.

- Identify the domain concepts the document covers. Each concept that can be understood independently becomes one file.
- Related content stays together: an entity's definition, its state transitions, and its invariants belong in one file — not three files split by "entities", "states", "invariants".
- Cross-referencing concepts that cannot be understood without each other stay in the same file.
- Keep each fact in the document type that owns it under Ownership. Link other types.
- A file explains its own concern. Follow links for adjacent concerns; merge fragments that need sibling text to define their own concern.

No committed file of a product repository (document, code comment, build file) names an agent rule, skill or hook, or any path under `.claude/`, `.codex/`, `~/.claude/` or `~/.codex/`. The agent configuration is not part of the product repository (`rules/workflow/committing.md` Staging); a document states the convention it follows in its own words. The agent configuration's own documentation is exempt, and so is a local record (`rules/workflow/records.md`); `hooks/doc_check.py` reports a named configuration path in every other Markdown file of a Git work tree.

## Ownership

Each fact has one owning document; every other document links it and never restates it.

| Fact | Owner |
|------|-------|
| What a term means | its glossary entry |
| Why a module needs a concept, how concepts relate | `concept.md` |
| Rules a concept obeys: relations, states, invariants | `model.md` |
| Algorithm steps | `spec.md` |
| Types, functions, open gaps between code and decided design, performance risks of a mechanism | `design.md` |
| External APIs | `impl.md` |

A committed document states the current design (`rules/workflow/committing.md` Staging); it has no dated or "verified" section. Decision records follow `rules/workflow/records.md`; a commit records when a fact changed.
Rationale lives in `concept.md` Rationale and Rejected Alternatives.

## Repositories

These rules apply when a product spans several repositories: a main repository and the submodules it records, which may depend on each other.

- The repository that defines a concept owns its design text. Ownership above applies within each repository; another repository links the owner and never restates it.
- Links and term references point only along the dependency direction: from the main repository to a submodule, and from a submodule to a repository it depends on; never back. A library's documents read standalone.
- The main repository links into a submodule by relative path.
- A submodule links to a repository it depends on by the absolute URL of the target file at the release tag of the dependency version its build declares.
