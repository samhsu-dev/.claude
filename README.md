# .claude

> The user-level Claude Code directory: rules and skills that load in every project.

Language-independent agent rules and skills for Claude Code, organized by the artifact they constrain.

## Install

```bash
git clone https://github.com/samhsu-dev/.claude ~/.claude
```

Claude Code reads `~/.claude/CLAUDE.md`, `~/.claude/rules/`, and `~/.claude/skills/` at session start. A project adds its own parameters in `<project>/.claude/`.

## Usage

Rules apply by themselves. Skills run on request:

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `/commit` | User asks to commit | Staging, classification, multi-commit workflow |
| `/update-codes` | User asks to update or fix code quality | Audit, plan fixes, apply after approval |
| `/update-docs` | User asks to update or fix documentation | Audit against type rules, plan fixes, apply after approval |
| `/update-tests` | User asks to add, audit, or update tests | Design-driven coverage audit, add missing, remove stale |
| `/update-prompts` | User asks to update, review, or fix a prompt | Audit, plan fixes, apply after approval, rerun the eval |
| `/render-doc` | User asks to convert a doc to HTML | Render a Markdown source as a self-contained HTML page |
| `/perf` | User asks to optimize or benchmark | Measurement-driven optimization pipeline |
| `/debug` | User reports a bug or test failure | Reproduce-first investigation and fix protocol |
| `/zotero-audit` | User asks to check or clean Zotero items | Read-only metadata audit against Crossref |

## Rules

A rule without `paths:` frontmatter is always active. A rule with `paths:` loads when Claude reads a matching file.

| File | Loads for | Governs |
|------|-----------|---------|
| `communication/terminology.md` | always | Which terms output may use |
| `workflow/development.md` | always | Concept → Model → Algorithm → Design → Research → Plan → Code → Verify |
| `workflow/change-policy.md` | always | When code and public API may change |
| `workflow/committing.md` | always | Commit message, staging, cadence, attribution |
| `workflow/git-safety.md` | always | Prohibited git operations in a shared working tree |
| `workflow/performance.md` | performance and benchmark files | Optimization guardrails |
| `code/quality.md` | code files | Control flow, naming, complexity |
| `code/organization.md` | code files | File naming and layout |
| `code/logging.md` | code files | Logging |
| `code/resource-bounds.md` | code and shell files | Timeouts and input bounds |
| `code/debugging.md` | code and test files | Debugging guardrails |
| `code/testing.md` | test files | Test design, layout, assertions |
| `docs/<type>.md` | the doc type it names | Format of concept, model, spec, design, impl, todo, index, glossary, README, llms, HTML |
| `prompt/prompting.md` | `*.prompty`, `prompts/` | LLM prompt construction |
| `meta/rulewriting.md` | rule files, `CLAUDE.md` | How to write rules |
| `meta/skilling.md` | skill files | How to write skills |

## License

MIT
