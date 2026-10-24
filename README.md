# .claude

> The user-level Claude Code directory: shared agent rules and skills.

Language-independent agent rules and skills for Claude Code, organized by the artifact they constrain.

## Install

```bash
git clone https://github.com/samhsu-dev/.claude ~/.claude
```

Skill invocation controls: [Skill Writing Standards](rules/meta/skilling.md#frontmatter).

## Usage

Skill procedures and usage triggers:

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

Loading semantics: [Rule Writing Standards](rules/meta/rulewriting.md#context-loading).

| File | Loads for | Governs |
|------|-----------|---------|
| `communication/terminology.md` | always | Which terms output may use |
| `workflow/development.md` | always | Concept → Model → Algorithm → Design → Research → Plan → Code → Verify |
| `workflow/change-policy.md` | always | When code and public API may change |
| `workflow/committing.md` | always | Commit message, staging, cadence, attribution |
| `workflow/git-safety.md` | always | Prohibited git operations in a shared working tree |
| `workflow/multi-agent.md` | always | Delegated discussion, design and implementation; one agent loop by default, split only by context, parallel dispatch only for tasks passing four checks; role table with model and effort, branch lifecycle, run ledger, per-task rework measurement |
| `workflow/performance.md` | performance and benchmark files | Optimization guardrails |
| `code/quality.md` | code files | Control flow, naming, complexity |
| `code/organization.md` | code files | File naming and layout |
| `code/logging.md` | code files | Logging |
| `code/resource-bounds.md` | code and shell files | Timeouts and input bounds |
| `code/debugging.md` | code and test files | Debugging guardrails |
| `code/testing.md` | test files | Test design, layout, assertions |
| `docs/<type>.md` | the doc type it names | Format of concept, model, spec, design, impl, task docs, index, glossary, README, llms, HTML |
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

## Tools

| Script | Used by | Does |
|--------|---------|------|
| `tools/codex_rules.py` | the main agent launching a Codex run | `pack` writes the run's `AGENTS.md` and `rules.json` pointing Codex to the rules and skills; `gate` confirms the run's log shows it read every always-active rule |

Project data comes from the project: `doc_check.py` reads the forbidden terms of the repository it edits, so one script serves every repository.

## License

MIT
