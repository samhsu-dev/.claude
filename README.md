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
| `workflow/multi-agent.md` | always | Role discussion, model routing, task consolidation, run ledger and serial patch integration |
| `workflow/performance.md` | performance and benchmark files | Optimization guardrails |
| `code/quality.md` | code files | Control flow, naming, complexity |
| `code/organization.md` | code files | File naming and layout |
| `code/logging.md` | code files | Logging |
| `code/resource-bounds.md` | code and shell files | Timeouts and input bounds |
| `code/debugging.md` | code and test files | Debugging guardrails |
| `code/testing.md` | test files | Test design, layout, assertions |
| `docs/<type>.md` | the doc type it names | Format of concept, model, spec, design, impl, todo, index, glossary, README, llms, HTML |
| `docs/bibliography.md` | `.bib` files and docs that cite | One bibliography exported from Zotero by Better BibTeX, Pandoc citation keys, pinned tool versions |
| `prompt/prompting.md` | `*.prompty`, `prompts/` | LLM prompt construction |
| `meta/rulewriting.md` | rule files, `CLAUDE.md` | How to write rules |
| `meta/skilling.md` | skill files | How to write skills |

## Hooks

Hooks check what a rule can only ask for. They apply in every repository once registered in `~/.claude/settings.json`; `settings.json` is not tracked, so a new machine adds this block:

```json
"PreToolUse": [{ "matcher": "Bash", "hooks": [{ "type": "command", "if": "Bash(git *)",
  "command": "python3 \"$HOME/.claude/hooks/git_guard.py\"" }] }],
"PostToolUse": [{ "matcher": "Write|Edit|MultiEdit", "hooks": [{ "type": "command",
  "command": "python3 \"$HOME/.claude/hooks/doc_check.py\"" }] }]
```

| Script | Event | Checks |
|--------|-------|--------|
| `hooks/git_guard.py` | before a git command | Blocks the operations `workflow/git-safety.md` prohibits; blocks a commit whose subject breaks Conventional Commits or 72 chars, or that carries an attribution trailer |
| `hooks/doc_check.py` | after a file write | Reports a doc or rule file past its line limit, a forbidden term from the project's `.claude/rules/communication/terminology.md`, a glossary Source path that does not resolve, a URL, path or line number in a glossary citation, a glossary citation field without a key, and a citation key the bibliography does not hold |

Project data comes from the project: `doc_check.py` reads the forbidden terms of the repository it edits, so one script serves every repository.

## License

MIT
