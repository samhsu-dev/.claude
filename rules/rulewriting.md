---
---

# Rule Writing Standards

Rules are read by agents. Code and documentation produced from rules are read by humans.

---

## Platform Constraints

- Under 200 lines per file. Longer files reduce adherence.
- `paths:` YAML frontmatter → loaded when Claude reads matching files. No `paths:` → always active.
- One topic per file. Descriptive filename.
- Discovered recursively in `.claude/rules/`. Subdirectories supported.
- Contradicting rules across files → Claude picks one arbitrarily. Prevent this.

## Audience

- **Rule files** → agent. Short, unambiguous, no narrative.
- **Generated code** → human developers. Readable, idiomatic.
- **Generated docs** → human readers. Clear prose, logical flow.

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

## Content

- Every rule is actionable. Cannot be verified or applied → remove.
- Every rule is concrete. "Functions under 20 lines" not "keep functions short".
- Every rule is necessary. Removing it changes nothing → remove.
- No tautologies. "Use meaningful names" adds no information.
- No examples of what not to do unless the wrong pattern is non-obvious.

## Conflict Resolution

- Rules within one file: no contradictions.
- Global rules are language-agnostic defaults. Project rules specify language/community conventions.
- Project rules override global rules when both set concrete values for the same metric.
- Edge cases: one rule states the priority. "X. Exception: Y when Z."
