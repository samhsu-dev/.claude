# Global Agent Rules

Language-independent rules and skills. Project rules in `<project>/.claude/` supply the project parameters.

## Documentation Naming

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

Single doc file: 200 lines max (`hooks/doc_check.py` reports an overrun). Exceeds limit → split by concern using prefix naming above. When a single concern still exceeds the limit, append numeric index: `concept-{concern}-{index}.md` (e.g., `design-auth-1.md`, `design-auth-2.md`).

A repository document never names an agent rule, skill, or hook, or any path under `.claude/` or `~/.claude/`. The agent configuration is not part of the repository; a document states the convention it follows in its own words (`hooks/doc_check.py` reports such a path).

## Documentation Ownership

Each fact has one owning document; every other document links it and never restates it.

| Fact | Owner |
|------|-------|
| What a term means | its glossary entry |
| Why a module needs a concept, how concepts relate | `concept.md` |
| Rules a concept obeys: relations, states, invariants | `model.md` |
| Algorithm steps | `spec.md` |
| Types, functions, open gaps between code and decided design | `design.md` |
| External APIs | `impl.md` |

A committed document states the current design. No dates, no change history, no dated or "verified" sections, no decision IDs, no commit citations, no "user decision", "agent decision", "revises" or "keeps every decision" markers. Decision records follow Local Records; a commit records when a fact changed.

## Local Records

Records that serve only the developers at work live in three local directories, excluded through `.git/info/exclude` and never committed:

| Record | Directory | Holds |
|--------|-----------|-------|
| Decision log | `docs/decisions/` | Each decision item, open or decided: question, options, examples, choice, reason, evidence, commits |
| Task docs | `docs/todo/` | Tasks still to do (`rules/docs/todo.md`) |
| Audit reports | `docs/audit/` | Each audit's findings, each with where it went: a doc fix, a task, or a decision item |

- A record goes to the directory its content belongs to, not the one of the activity that produced it: an audit's open question is a decision item, its follow-up is a task.
- Each directory holds one file per module, named after the module (`catalog-import.md` for `docs/catalog/import/`), split by concern past 200 lines, and an `index.md` listing its files.
- Dates, decision IDs and commit hashes are allowed in local records only.
- A committed document never names or links a local record, and no committed fact depends on one.

## Skills

Skills are active procedures. Rules are passive guardrails. Both layers enforce the same standards. The human-facing listing of rules and skills: `README.md`.
