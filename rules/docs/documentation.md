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

Each split file follows the same rules as its single-file counterpart. One concern per file.

A companion file holds one kind of supporting content for one owning file and omits the type's required sections; its first line links the owner. Companions: `spec-{concern}-examples*.md` (complete inputs, context and expected results of the owning spec), `design-structure*.md` (diagrams of the owning design), `design-gaps*.md` (Open Gaps of the owning design). A companion defines no rule, algorithm step or API of its own; the owner keeps the complete contract, and a reader reaches the companion's owner in one link. Glossary layout: `rules/docs/glossary.md`.

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

## Writing

- Each document follows the rules of its type file under `rules/docs/`.
- An engineer writes for a software engineer who implements, reviews or maintains the design. A document states what a component does, its inputs, outputs and invariants, and the reason for each rule. It only transfers information and design: no persuasion, narrative, restated summary, process note or commentary about the document.
- Each sentence has one reading. It names the exact data, program point, context and condition; a quantity or bound is stated, not implied. A vague word ("handles", "appropriately", "some", "etc.") gives way to the list or condition it stands for.
- No two sentences contradict each other, within a document or across documents.
- Structure is plain: short sections and paragraphs, at most two heading levels below the title where the type's required structure allows, bullets nested at most one level, a table only for rows-by-columns data, no decorative callout, no chain of cross-references a reader follows to understand one rule.
- Terms follow `communication/terminology.md`: computer-science terms and glossary terms only, algorithm terms spelled as the glossary spells them.

## Updating

- A change starts at the owning statement, the sentence that first defines the concept. Revise it there, rewrite the section that holds it so the whole section states the new design as if written fresh, then align every dependent sentence in this and other documents.
- Never append a correcting sentence, an exception, an override note or a change history beside unchanged old text. Wording such as "now also", "in addition to the above", "previously", "changed to", or an exception paragraph after the rule it amends, marks a patch.
- A section the change does not affect keeps its text; no document is recreated from scratch.

## Repositories

These rules apply when a product spans several repositories: a main repository and the submodules it records, which may depend on each other.

- The repository that defines a concept owns its design text. Ownership above applies within each repository; another repository links the owner and never restates it.
- Links and term references point only along the dependency direction: from the main repository to a submodule, and from a submodule to a repository it depends on; never back. A library's documents read standalone.
- The main repository links into a submodule by relative path.
- A submodule links to a repository it depends on by the absolute URL of the target file at the release tag of the dependency version its build declares.
