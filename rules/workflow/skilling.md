---
paths:
  - "**/.claude/skills/**/*"
  - "**/SKILL.md"
---

# Skill Writing Standards

A skill is a prompt template injected into conversation when invoked. Not code, not a function.

---

## File Structure

```
skill-name/
├── SKILL.md            # Required — frontmatter + prompt
├── scripts/            # Deterministic helpers (shell or scripting language)
└── reference.md        # Large docs Claude reads on demand
```

- One `SKILL.md` per directory. Directory name = skill name when `name:` omitted.
- Reference files via `${CLAUDE_SKILL_DIR}/path`. Claude does not discover unreferenced files.
- `SKILL.md` under 500 lines.

## Frontmatter

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `name` | string | dir name | `/name` invocation. Lowercase, hyphens, max 64 chars. |
| `description` | string | first paragraph | Auto-trigger judgment. Under 250 chars. |
| `allowed-tools` | string/list | session perms | Pre-approved tools. Names only, no patterns. |
| `argument-hint` | string | none | Autocomplete hint. |
| `disable-model-invocation` | bool | `false` | `true` = user-only, Claude cannot auto-trigger. |
| `user-invocable` | bool | `true` | `false` = Claude-only, hidden from `/` menu. |
| `paths` | string/list | none | Glob filter. Skill loads only for matching files. |
| `model` | string | session | Override model. |
| `effort` | enum | session | `low` / `medium` / `high` / `max`. |
| `context` | string | inline | `fork` = isolated subagent. |
| `agent` | string | general-purpose | Subagent type for `context: fork`. |
| `shell` | enum | `bash` | Shell for preprocessing. |

### Constraints

- `disable-model-invocation: true` + `user-invocable: false` = contradictory. Never combine.
- `context: fork` without actionable task = empty output.
- `allowed-tools` accepts tool names only. `Bash(npm *)` is invalid.

## Variables

| Variable | Value |
|----------|-------|
| `$ARGUMENTS` | All args. Auto-appended if absent. |
| `$ARGUMENTS[N]` / `$N` | Nth arg (0-indexed). |
| `${CLAUDE_SESSION_ID}` | Session UUID. |
| `${CLAUDE_SKILL_DIR}` | Skill directory absolute path. |

## Shell Preprocessing

`` !`command` `` executes before Claude sees content. Output replaces placeholder.

- Runs as the current OS user with full permissions.
- Failed commands produce empty replacement.
- Disabled by policy: `"disableSkillShellExecution": true`.

---

## Script vs Agent Boundary

Deterministic work in scripts. Reasoning in SKILL.md.

| Handled by script | Handled by agent |
|--------------------|-----------------|
| URL construction, HTTP fetch, JSON parse | Interpret results, summarize findings |
| Regex classification, keyword matching | Ambiguous edge cases, judgment calls |
| Arithmetic, hashing, scoring | Compare against user context |
| CSV/JSON read-write, bulk transforms | Format output, answer follow-ups |

- Scripts in `scripts/`. Invoke: `${CLAUDE_SKILL_DIR}/scripts/<name> $ARGUMENTS`.
- Scripts output structured JSON. Agent reads and presents.
- Scripts use stdlib only. Document dependencies if unavoidable.
- Scripts handle errors internally. Return error objects, never crash.

## Content Rules

- Imperative mood. "Run the script." Not "You should run the script."
- One task per skill. Multiple tasks = multiple skills.
- Numbered steps. Each step = one action.
- Tables for mappings. Lists for rules.
- Error handling section when external calls can fail.

## Description Rules

- Under 250 characters.
- Pattern: `{Action} {target}. Use when {trigger}.`
- No vague descriptions ("Useful utility", "Helper for tasks").

---

## Security

### Threat Model

Skills run with the user's full OS permissions. A malicious skill can:
- Read any file (`~/.ssh`, `~/.aws`, `.env`) via `Read` or `Bash(cat)`.
- Exfiltrate data via `WebFetch`, `Bash(curl)`, or MCP tools.
- Modify git history, install packages, create persistence.
- Shell preprocessing (`` !`cmd` ``) runs before Claude sees anything.

### allowed-tools Rules

- List only tools the procedure uses. No extras.
- Never grant bare `Bash` unless the skill requires arbitrary shell. Prefer `Read`/`Write`/`Grep`.
- `WebFetch` = network access. Grant only when HTTP fetch is the skill's purpose.
- Pre-approval bypasses user confirmation. Over-permitting = reduced oversight.
- `allowed-tools` cannot override deny rules in settings.json. Deny always wins.

### Shell Preprocessing Rules

- Never fetch and execute remote scripts (`` !`curl url | bash` ``).
- Never write to shell profiles (`~/.zshrc`, `~/.bashrc`).
- Never access credentials or secrets in preprocessing.
- Use preprocessing only for read-only context injection (`git status`, `node --version`).
- Disable for untrusted skills: `"disableSkillShellExecution": true` in settings.

### Sensitive Data

- Never store API keys, tokens, or passwords in SKILL.md or scripts.
- Use environment variables (`env` in settings.json) or plugin `userConfig` with `"sensitive": true`.
- `userConfig` sensitive values stored in OS keychain.

### Trust Levels

| Scope | Location | Trust | Risk |
|-------|----------|-------|------|
| Personal | `~/.claude/skills/` | High | Applies to all projects |
| Project | `.claude/skills/` | Medium | Anyone with repo access controls |
| Plugin | marketplace install | Low | Unknown author |
| Managed | enterprise policy | Highest | Admin-vetted |

### Audit Checklist (before installing external skills)

1. Read `SKILL.md` frontmatter. What tools are allowed?
2. Search for `` !` `` and `` ```! ``. What shell commands run?
3. Search for `WebFetch`, `curl`, `wget`. Network access?
4. Check `scripts/` directory. What do executables do?
5. Check `user-invocable: false`. Hidden skills can auto-trigger silently.

---

## Distribution

### Symlink (cross-project, recommended)

```bash
ln -s /path/to/skill-name .claude/skills/skill-name
```

### Git submodule (cross-repo)

```bash
git submodule add <url> extern/skill-name
ln -s ../../extern/skill-name .claude/skills/skill-name
```

### Plugin (marketplace distribution)

```
plugin-name/
├── .claude-plugin/plugin.json
└── skills/skill-name/SKILL.md
```

Invoked as `/plugin-name:skill-name`.

## Discovery & Priority

| Scope | Priority |
|-------|----------|
| Enterprise managed | highest |
| Personal `~/.claude/skills/` | high |
| Project `.claude/skills/` | medium |
| Plugin | lowest |

Same-name: higher scope wins, no merging. Live reload on file change.

## Verification

- `/name` triggers correctly with `$ARGUMENTS`.
- All referenced files exist at `${CLAUDE_SKILL_DIR}` paths.
- `allowed-tools` matches actual tool usage. No excess.
- Scripts return valid JSON on success and error.
- Description under 250 chars. SKILL.md under 500 lines.
