---
---

# Rule File Standards

Rules are read by agents. Code and documentation produced from rules are read by humans.

---

## Claude Code Platform Specification

Source: https://code.claude.com/docs/en/memory

### How rules load
- Rules are context injected as user messages, not system prompt. Not enforced configuration.
- More specific and concise → more consistent adherence. Vague or conflicting → arbitrary behavior.
- Contradicting rules across files: Claude picks one arbitrarily.

### Priority (highest → lowest)
1. Managed policy (`/Library/Application Support/ClaudeCode/CLAUDE.md`). Cannot be excluded.
2. Project rules (`.claude/CLAUDE.md`, `.claude/rules/*.md`).
3. User rules (`~/.claude/CLAUDE.md`, `~/.claude/rules/*.md`). Loaded first, lowest priority.

### File limits
- Under 200 lines per file. Longer files reduce adherence.
- CLAUDE.md loaded in full. `MEMORY.md` limited to 200 lines / 25KB.
- Split large files via `@path/to/import` (max 5 hops) or `.claude/rules/`.

### Path scoping
- `paths:` YAML frontmatter → loaded when Claude reads matching files.
- No `paths:` → loaded unconditionally at session start.
- Glob patterns: `**/*.py`, `src/**/*`, `*.md`, `src/**/*.{ts,tsx}`.

### Rules file requirements
- One topic per file. Descriptive filename (`testing.md`, `api-design.md`).
- Discovered recursively in `.claude/rules/`.
- Symlinks supported. Circular symlinks detected.

### HTML comments
- `<!-- comments -->` stripped before injection. Use for human-only notes without consuming tokens.
- Comments inside code blocks preserved.

### Verification
- `/memory` lists all loaded files. If a file is not listed, Claude cannot see it.
- `InstructionsLoaded` hook logs which files load, when, and why.
- CLAUDE.md survives `/compact`. Rules given only in conversation do not.

---

## Audience

- **Rule files** → agent. Optimize for parsing: short, unambiguous, no narrative.
- **Generated code** → human developers. Readable, idiomatic, documented.
- **Generated docs** → human readers. Clear prose, logical flow, appropriate detail.

## Language

- Assert-style. State what is, not what should be.
- One rule per line. One concept per bullet.
- No modifiers: no "properly", "appropriately", "effectively", "ideally", "simply".
- No softeners: no "prefer", "avoid", "consider", "try to".
- No hedging: no "when possible", "if applicable", "as needed", "where appropriate".
- Prohibitions: "No" or "Never". Not "avoid" or "do not use unless".
- Conditions explicit: "X when Y". Not "X if appropriate".

## Structure

- Title states the domain.
- Sections group related rules. One topic per section.
- Two heading levels maximum (## and ###).
- Tables for structured data. Lists for rules. Code blocks for patterns.
- No redundancy within one file.
- No redundancy across files. Each rule has one authoritative location.
- Under 200 lines per file (Claude official recommendation).

## Content

- Every rule is actionable. Cannot be verified or applied → remove.
- Every rule is concrete. "Functions under 20 lines" not "keep functions short".
- Every rule is necessary. Removing it changes nothing → remove.
- No tautologies. "Use meaningful names" adds no information.
- No examples of what not to do unless the wrong pattern is non-obvious.
- Standards referenced inline: "(PEP 8)" not a separate references section.

## Conflict Resolution

- Rules within one file: no contradictions.
- Project rules and global rules: no contradictions. Project rules narrow scope, not override.
- Edge cases: one rule states the priority. "X. Exception: Y when Z."
- Contradicting rules → Claude picks arbitrarily (official behavior). Prevent this.
