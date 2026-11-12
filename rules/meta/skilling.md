---
paths:
  - "**/.claude/skills/**/*"
  - "**/SKILL.md"
---

# Skill Writing Standards

Field and variable reference: [Extend Claude with skills](https://code.claude.com/docs/en/skills).

---

## File Structure

```text
skill-name/
├── SKILL.md            # Required — frontmatter + prompt
├── scripts/            # Deterministic helpers (shell or scripting language)
└── reference.md        # Large docs Claude reads on demand
```

- One `SKILL.md` per directory. Directory name = skill name when `name:` omitted.
- Reference files via `${CLAUDE_SKILL_DIR}/path`. Claude does not discover unreferenced files.
- `SKILL.md` under 500 lines.

## Frontmatter and Variables

- Every field is optional; give `description`. Field meanings, defaults and substitution variables follow the reference above, not a local copy.
- `disable-model-invocation: true` + `user-invocable: false` = contradictory. Never combine.
- `context: fork` without actionable task = empty output.
- `allowed-tools` pre-approves the listed tools, including `Bash(pattern)` specifiers, for the invoking turn.
- `effort` takes a level the session model supports: `low`, `medium`, `high`, `xhigh` or `max`.

## Shell Preprocessing

- A preprocessing command matches no deny rule and is allowed outside auto mode.
- A preprocessing command exits 0, or 1 for a search or comparison command.

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
- Scripts return structured JSON on success and error. Agent reads and presents.
- Scripts use stdlib only. A script that needs a non-stdlib dependency documents it.
- Scripts handle errors internally. Return error objects, never crash.

## Content Rules

- Imperative mood. "Run the script." Not "You should run the script."
- One task per skill. Multiple tasks = multiple skills.
- A skill states its procedure. A standard it applies is a link to the owning rule file and section, never a restatement (`rules/meta/rulewriting.md` Structure).
- Numbered steps. Each step = one action.
- Tables for mappings. Lists for rules.
- Error handling section when external calls can fail.

## Description Rules

- Under 250 characters.
- Pattern: `{Action} {target}. Use when {trigger}.`
- No vague descriptions ("Useful utility", "Helper for tasks").

---

## Security

### allowed-tools Rules

- Pre-approve only tools the procedure uses, narrowest specifier first (`Bash(git status *)` over bare `Bash`; `WebFetch` only when HTTP fetch is the skill's purpose). Pre-approval skips confirmation; settings permissions remain the boundary.

### Shell Preprocessing Rules

- Never fetch and execute remote scripts (`` !`curl url | bash` ``).
- Never write to shell profiles (`~/.zshrc`, `~/.bashrc`).
- Never access credentials or secrets in preprocessing.
- Use preprocessing only for read-only context injection (`git status`, `node --version`).

### Sensitive Data

- Never store API keys, tokens, or passwords in SKILL.md or scripts.
- Use environment variables (`env` in settings.json) or plugin `userConfig` with `"sensitive": true`.

### Trust Levels

A skill copied from an unknown author stays untrusted until audited, whatever its installation scope.

### Audit Checklist (before installing external skills)

1. Read `SKILL.md` frontmatter. What tools are allowed?
2. Search for `` !` `` and `` ```! ``. What shell commands run?
3. Search for `WebFetch`, `curl`, `wget`. Network access?
4. Check `scripts/` directory. What do executables do?
5. Check `user-invocable: false`. Hidden skills can auto-trigger silently.

---

## Distribution

### Symlink (cross-project)

```bash
ln -s /path/to/skill-name .claude/skills/skill-name
```

### Git submodule (cross-repo)

```bash
git submodule add <url> extern/skill-name
ln -s ../../extern/skill-name .claude/skills/skill-name
```

### Plugin (marketplace distribution)

```text
plugin-name/
├── .claude-plugin/plugin.json
└── skills/skill-name/SKILL.md
```

Invoked as `/plugin-name:skill-name`.

## Verification

- `/name` triggers correctly with `$ARGUMENTS`.
- All referenced files exist at `${CLAUDE_SKILL_DIR}` paths.
