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

Each split file follows the same rules as its single-file counterpart. One concern per file. Exception: the glossary's single file is its routing file and holds no entry (`rules/docs/glossary.md`).

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

A document states the current design. No dates, no change history, no dated or "verified" sections, no decision IDs, no commit citations, no "user decision" or "agent decision" markers. A decision's question, options, choice, evidence and commits live in the project's local decision log, which is never committed; a commit records when a fact changed.

## Skills

Skills are active procedures. Rules are passive guardrails. Both layers enforce the same standards. The human-facing listing of rules and skills: `README.md`.
