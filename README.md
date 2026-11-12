# .claude

> The user-level Claude Code directory: shared agent rules and skills.

Language-independent agent rules and skills for Claude Code, organized by the artifact they constrain.

## Install

```bash
git clone https://github.com/<profile.repository> ~/.claude
```

The project rule files under `rules/project/` supply `profile.repository` and profile branch identities.

Skill invocation controls: [Skill Writing Standards](rules/meta/skilling.md#frontmatter-and-variables).

## Usage

Skill procedures and usage triggers:

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `/commit` | User asks to commit | Staging, classification, multi-commit workflow, cadence, safe Git alternatives |
| `/update-codes` | User asks to update or fix code quality | Audit, plan fixes, apply after approval |
| `/update-docs` | User asks to update or fix documentation | Audit against type rules, plan fixes, apply after approval |
| `/update-tests` | User asks to add, audit, or update tests | Design-driven coverage audit, add missing, remove stale |
| `/update-prompts` | User asks to update, review, or fix a prompt | Audit, plan fixes, apply after approval, rerun the eval |
| `/render-doc` | User asks to convert a doc to HTML | Render a Markdown source as a self-contained HTML page |
| `/perf` | User asks to optimize or benchmark | Measurement-driven optimization pipeline |
| `/debug` | User reports a bug or test failure | Reproduce-first investigation and fix protocol |
| `/zotero-audit` | User asks to check or clean Zotero items | Read-only metadata audit against Crossref |
| `/multi-agent` | Main agent dispatches, reviews, merges or consolidates delegated runs | Roles, task modes, acceptance, briefs, dispatch, review rounds, branch lifecycle, records, consolidation |
| `/chain-session` | A brief makes the agent a chain session or a reviewer, or a change touches design documents or code | Development pipeline, work loop, boundary questions, self-check, review checklist |
| `/decisions` | A design question is open | Triage and agent authority, evidence preparation, decision runs, solution checks, question format, recording |

## Rules

Loading semantics: [Rule Writing Standards](rules/meta/rulewriting.md#context-loading).

| File | Loads for | Governs |
|------|-----------|---------|
| `communication/terminology.md` | always | Which terms output may use |
| `workflow/change-policy.md` | always | When code and public API may change |
| `workflow/committing.md` | always | Commit message, staging, attribution |
| `workflow/git-safety.md` | always | Prohibited git operations in a shared working tree |
| `workflow/multi-agent.md` | always | Hard limits of delegated work |
| `workflow/decisions.md` | always | Decision authority |
| `workflow/records.md` | decision, task and audit records | Local record layout and entry fields |
| `workflow/performance.md` | performance and benchmark files | Optimization guardrails |
| `code/quality.md` | code files | Control flow, naming, complexity |
| `code/organization.md` | code files | File naming and layout |
| `code/logging.md` | code files | Logging |
| `code/resource-bounds.md` | code and shell files | Timeouts and input bounds |
| `code/testing.md` | test files | Test design, layout, assertions |
| `docs/documentation.md` | Markdown files | Document naming, size limit, fact ownership |
| `docs/<type>.md` | the doc type it names | Format of concept, model, spec, design, impl, task docs, index, glossary, README, llms, HTML |
| `docs/bibliography.md` | `.bib` files and docs that cite | One bibliography exported from Zotero by Better BibTeX, Pandoc citation keys, pinned tool versions |
| `prompt/prompting.md` | `*.prompty`, `prompts/`, `PROMPT*.md` briefs | LLM prompt construction |
| `meta/rulewriting.md` | rule files, `CLAUDE.md` | How to write rules |
| `meta/skilling.md` | skill files | How to write skills |

## Hooks

Hooks check what a rule can only ask for. They apply in every repository once registered in `~/.claude/settings.json`; `settings.json` is not tracked, so a new machine adds this block:

```json
"SessionStart": [{ "matcher": "", "hooks": [{ "type": "command", "command": "python3 \"$HOME/.claude/tools/branch_check.py\" --hook SessionStart", "timeout": 60 }] }],
"PreToolUse": [{ "matcher": "Bash", "hooks": [
  { "type": "command", "if": "Bash(git *)", "command": "python3 \"$HOME/.claude/hooks/git_guard.py\"", "onFailure": "block" },
  { "type": "command", "if": "Bash(gh pr *)", "command": "python3 \"$HOME/.claude/hooks/git_guard.py\"", "onFailure": "block" },
  { "type": "command", "command": "python3 \"$HOME/.claude/hooks/poll_guard.py\"", "onFailure": "block" }] }],
"PostToolUse": [{ "matcher": "Write|Edit|MultiEdit", "hooks": [{ "type": "command",
  "command": "python3 \"$HOME/.claude/hooks/doc_check.py\"", "onFailure": "block" }] },
  { "matcher": "Bash", "hooks": [{ "type": "command", "if": "Bash(git push *)", "command": "python3 \"$HOME/.claude/tools/branch_check.py\" --hook PostToolUse --no-fetch", "timeout": 60 }] }]
```

`"attribution": {"commit": "", "pr": "", "sessionUrl": false}` in the same file stops Claude Code from adding attribution lines.

| Script | Event | Checks |
|--------|-------|--------|
| `hooks/git_guard.py` | before a git or `gh pr` command | Blocks the operations of `workflow/git-safety.md`, Git hook bypasses, staging of never-committed paths and attribution in pull request bodies |
| `hooks/poll_guard.py` | before a shell command | Blocks a polling loop (`until` or `while` with `sleep`) under `workflow/multi-agent.md` |
| `hooks/doc_check.py` | after a file write | Checks the documentation constraints named by `rules/docs/`; reads project markdown values |
| `tools/branch_check.py` | session start and after `git push` | Reports the Branch Lifecycle state of skill `multi-agent`: integration branch ahead of or behind its upstream, landed, overdue and unowned branches, removable and missing worktrees; reads the project `Integration` values |

### Git hooks

`tools/git-hooks/` is a Git hooks directory run by [Lefthook](https://lefthook.dev): `commit-msg` checks the message with commitlint against `commitlint.config.mjs`, and `pre-commit` runs markdownlint-cli2 and CSpell on staged Markdown in a repository that commits `.markdownlint-cli2.jsonc` or `cspell.json`. It needs `lefthook`, `commitlint`, `markdownlint-cli2` and `cspell` on `PATH` (`brew install lefthook`; `npm install -g @commitlint/cli markdownlint-cli2 cspell`). A repository uses it when its Git configuration sets `core.hooksPath`; `~/.gitconfig` scopes that to the agent configuration repositories and each project repository that opts in:

```ini
[includeIf "gitdir:~/.claude/.git/"]
    path = ~/.config/git/agent-hooks
[includeIf "gitdir:~/.codex/.git/"]
    path = ~/.config/git/agent-hooks
[includeIf "gitdir/i:<project repository>/.git/"]
    path = ~/.config/git/agent-hooks
```

`~/.config/git/agent-hooks` holds `[core] hooksPath = <home>/.claude/tools/git-hooks`. A gitdir pattern covers the repository's linked worktrees and submodules, whose Git directories lie under it.

## Tools

| Script | Used by | Does |
|--------|---------|------|
| `tools/codex_rules.py` | run launcher | `pack` writes rule routes, routing native Codex project value files by their `paths:`; `--lean` adds the chain-session skill as a required read; `gate` checks logged always-active paths, with the read inspection required by skill `multi-agent` Run Isolation |
| `tools/evidence.py` | task coordinator | Evidence schema, merge, freshness and brief commands |

See [Parameter Binding](CLAUDE.md#parameter-binding) for native project roots and fixed section formats.

## License

MIT
