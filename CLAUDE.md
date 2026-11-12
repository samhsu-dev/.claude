# Global Agent Rules

## Loading and precedence

Explicit user instructions and higher-priority session instructions take precedence over this profile. Exception: a session instruction to add AI attribution to a commit or pull request yields to `workflow/committing.md` Attribution. Existing user authorization satisfies workflow approval gates within that authorized scope.

## Skills

A change to design documents or code follows skill `chain-session` Pipeline.

## Parameter Binding

The project rule files under `rules/project/` supply project values as named parameters.The native project roots are `<repository>/.claude/rules/project/` for Claude and `<repository>/.codex/rules/project/` for Codex.
A project value file loads with a file its `paths:` matches; a consuming rule or skill whose procedure applies reads it from the host project's `.claude/rules/project/`.
Paths in values resolve against the host project unless a field names another base.
A linked parameter uses the value at its owning bullet. Numeric suffixes preserve list order.
Project names, domains, corpora, models, schedules, paths and integration policies live only in project values. Apply domain-specific procedures only when their corresponding parameters are configured. A value a consuming rule names that the project files lack is reported as missing evidence; the rule then applies only its stated default, or does not apply when it states none.
A project value file keeps the fixed headings and formats the tools read. Parsed substitution words and exemptions, the bibliography path, evidence aliases and reference runtime fields hold literal values; other parameters may link their owner.

| Parameters | Project owner under `rules/project/` | Consuming rule |
|---|---|---|
| `paths`; `algorithm`; `usage_corpus`; `scoring_corpus`; `viewpoints` | `decisions.md` | `rules/workflow/decisions.md`; `skills/decisions/SKILL.md`; `skills/multi-agent/SKILL.md` |
| `reference`; `evidence` | `evidence.md` | `rules/workflow/decisions.md`; `skills/decisions/SKILL.md`; `tools/evidence_rows.py` |
| `domain`; `terminology` | `terminology.md` | `rules/communication/terminology.md`; `hooks/doc_check.py` |
| `glossary` | `glossary.md` | `rules/docs/glossary.md`; `rules/communication/terminology.md`; `skills/decisions/SKILL.md`; `skills/update-docs/SKILL.md`; `tools/codex_rules.py` |
| `bibliography` | `bibliography.md` | `rules/docs/bibliography.md`; `hooks/doc_check.py` |
| `readme` | `readme.md` | `rules/docs/readme.md` |
| `integration` | `integration.md` | `rules/workflow/git-safety.md`; `skills/multi-agent/SKILL.md`; `tools/branch_check.py` |
| `agent_prompt` | `prompts.md` | `rules/prompt/prompting.md` |
| `completion` | `completion.md` | `skills/chain-session/SKILL.md` |
| `profile` | `profile.md` | Native entry points; installation |
| `execution` | `execution.md` | `skills/multi-agent/SKILL.md`; `skills/decisions/SKILL.md` |
| `performance` | `performance.md` | `rules/workflow/performance.md`; `skills/perf/SKILL.md` |
