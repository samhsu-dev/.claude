# Global Agent Rules

## Loading and precedence

Explicit user instructions and higher-priority session instructions take precedence over this profile. Existing user authorization satisfies workflow approval gates within that authorized scope.
Language- and project-independent rules and skills. A language profile adds only language conventions.
Project values bind through Parameter Binding below.
Existing project rules remain separate from the shared language profile.

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

A product repository document never names an agent rule, skill, or hook, or any path under `.claude/`, `.codex/`, `~/.claude/` or `~/.codex/`. The agent configuration is not part of the product repository; a document states the convention it follows in its own words (`hooks/doc_check.py` reports such a path). The agent configuration's own documentation is exempt.

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
Keep rationale only when readers need it to understand the design, as plain prose in the owning concept or model section.

## Local Records

Records that serve only the developers at work live in three local directories, excluded through `.git/info/exclude` and never committed:

| Record | Directory | Holds |
|--------|-----------|-------|
| Decision log | `docs/decisions/` | One entry per question, open or decided; fields below |
| Task docs | `docs/todo/` | Tasks still to do (`rules/docs/todo.md`) |
| Audit reports | `docs/audit/` | Each audit's findings, each with where it went: a doc fix, a task, or a decision item |

- A record goes to the directory its content belongs to, not the one of the activity that produced it: an audit's open question is a decision item, its follow-up is a task.
- Each directory holds one file per module, named after the module (`catalog-import.md` for `docs/catalog/import/`), split by concern past 200 lines, and an `index.md` listing its files.
- Dates, decision IDs and commit hashes are allowed in local records only.
- A decision entry holds its ID and authority, question, options, viewpoint recommendations, the refutation result when a refutation ran, choice and reason.
- It also holds examples and complete reference outputs, corpus counts and counting method, revised decisions and all recording commits.
- It records reused data or mechanisms, rejected alternatives, and whether earlier decisions are kept or which sentences change.
- An open entry has no choice. Fill that entry when the question is decided.
- Copy evidence needed by the entry into it; a record never depends on a run directory.
- A committed document never names or links a local record, and no committed fact depends on one.

## Skills

Skills are active procedures. Rules are passive guardrails. Both layers enforce the same standards. The human-facing listing of rules and skills: `README.md`.

## Parameter Binding

The project rule files under `rules/project/` supply project values as named parameters. They contain values only; global rules own the procedures.
The native project roots are `<repository>/.claude/rules/project/` for Claude and `<repository>/.codex/rules/project/` for Codex.
Every project markdown file is always active: it has no `paths:` frontmatter. Claude loads these files; `tools/codex_rules.py pack` lists them before any work in each Codex run.
Paths in values resolve against the host project unless a field names another base.
A linked parameter uses the value at its owning bullet. Numeric suffixes preserve list order.
A missing required value is reported as missing evidence; it is never guessed. Missing optional sections retain each consumer's documented default.
Tools read the fixed headings and formats declared in these project rules. Parsed substitution words/exemptions, bibliography path, evidence aliases and reference runtime fields contain literal values; other parameters may link their owner. No separate parameter file is selected.

| Parameters | Project owner under `rules/project/` | Consuming rule |
|---|---|---|
| `project`; `paths`; `algorithm`; `usage_corpus`; `scoring_corpus`; `viewpoints` | `decisions.md` | `rules/workflow/decisions.md` |
| `reference`; `evidence` | `evidence.md` | `rules/workflow/decisions.md`; `rules/workflow/multi-agent.md`; `tools/evidence.py` |
| `domain`; `terminology` | `terminology.md` | `rules/communication/terminology.md`; `hooks/doc_check.py` |
| `glossary` | `glossary.md` | `rules/docs/glossary.md`; `rules/communication/terminology.md` |
| `bibliography` | `bibliography.md` | `rules/docs/bibliography.md`; `hooks/doc_check.py` |
| `readme` | `readme.md` | `rules/docs/readme.md` |
| `integration` | `integration.md` | `rules/workflow/multi-agent.md` |
| `agent_prompt` | `prompts.md` | `rules/prompt/prompting.md` |
| `completion` | `completion.md` | `rules/workflow/development.md` |
| `profile` | `profile.md` | Native entry points; installation |
| `execution` | `execution.md` | `rules/workflow/multi-agent.md`; `rules/workflow/decisions.md` |
