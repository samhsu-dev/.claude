# Global Agent Rules

## Loading and precedence

Explicit user instructions and higher-priority session instructions take precedence over this profile. Existing user authorization satisfies workflow approval gates within that authorized scope.

Language- and project-independent rules and skills. A language profile adds only language conventions.
Existing project rules remain separate from the shared language profile.

## Skills

Skills are active procedures. Rules are passive guardrails. Both layers enforce the same standards. The human-facing listing of rules and skills: `README.md`. A change to design documents or code follows skill `chain-session` Pipeline.

## Parameter Binding

The project rule files under `rules/project/` supply project values as named parameters. They contain values only; global rules own the procedures.
The native project roots are `<repository>/.claude/rules/project/` for Claude and `<repository>/.codex/rules/project/` for Codex.
Each project value file lists in `paths:` frontmatter the files whose work needs it and loads with a matching file; a consuming rule or skill whose procedure applies reads it from the host project's `.claude/rules/project/`. Before changing algorithm semantics, a core principle or an evaluation, read `decisions.md` there.
Paths in values resolve against the host project unless a field names another base.
A linked parameter uses the value at its owning bullet. Numeric suffixes preserve list order.
Project names, domains, corpora, models, schedules, paths and integration policies live only in project values. Apply domain-specific procedures only when their corresponding parameters are configured. A missing required value is reported as missing evidence; missing optional sections create no requirement and retain only documented domain-independent defaults.
Tools read the fixed headings and formats declared in these project rules. Parsed substitution words/exemptions, bibliography path, evidence aliases and reference runtime fields contain literal values; other parameters may link their owner. No separate parameter file is selected.

| Parameters | Project owner under `rules/project/` | Consuming rule |
|---|---|---|
| `paths`; `algorithm`; `usage_corpus`; `scoring_corpus`; `viewpoints` | `decisions.md` | `rules/workflow/decisions.md`; `rules/workflow/change-policy.md`; `skills/decisions/SKILL.md`; `skills/multi-agent/SKILL.md` |
| `reference`; `evidence` | `evidence.md` | `rules/workflow/decisions.md`; `skills/decisions/SKILL.md` |
| `domain`; `terminology` | `terminology.md` | `rules/communication/terminology.md`; `hooks/doc_check.py` |
| `glossary` | `glossary.md` | `rules/docs/glossary.md`; `rules/communication/terminology.md`; `skills/decisions/SKILL.md`; `skills/update-docs/SKILL.md`; `tools/codex_rules.py` |
| `bibliography` | `bibliography.md` | `rules/docs/bibliography.md`; `hooks/doc_check.py` |
| `readme` | `readme.md` | `rules/docs/readme.md` |
| `integration` | `integration.md` | `skills/multi-agent/SKILL.md` |
| `agent_prompt` | `prompts.md` | `rules/prompt/prompting.md` |
| `completion` | `completion.md` | `skills/chain-session/SKILL.md` |
| `profile` | `profile.md` | Native entry points; installation |
| `execution` | `execution.md` | `skills/multi-agent/SKILL.md`; `skills/decisions/SKILL.md` |
