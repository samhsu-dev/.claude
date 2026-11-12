---
paths:
  - "**/.claude/rules/**/*.md"
  - "**/CLAUDE.md"
---

# Rule Writing Standards

## Platform Constraints

- `paths:` YAML frontmatter → loaded when Claude reads matching files. No `paths:` → always active.
- One topic per file.
- A rule a script, a linter, or a hook can check is enforced there. The rule file keeps one line stating the rule and naming the check; reasons and examples go.
- CLAUDE.md holds no directory tree; a file is listed only in the Parameter Binding table.

## Context Loading

- An agent performing one task loads the minimum number of rule files that covers every requirement of that task.
- Rules that always co-apply to one task type live in one file. Rules for unrelated task types live in separate files.
- `paths:` globs match exactly the files whose editing requires the rule. No broader, no narrower.
- A file states its own rules completely. A cross-reference names an owning file and section for another concern; load that owner before applying its rule.
- Always-active status (no `paths:`) is reserved for rules governing every task. A rule needed by one task type gets `paths:`. Value-only project files under `rules/project/` follow the same rule: `paths:` names the files their consumers govern.
- File-count test before adding or splitting a rule file: for each task type, count the rule files it forces into context. A change that raises the count without adding a requirement is wrong.

## Repository Layout

| Directory | Contains | File named after |
|-----------|----------|------------------|
| `rules/code/` | Rules constraining code artifacts | The concern: `quality.md`, `logging.md`, `organization.md` |
| `rules/docs/` | Rules constraining one documentation artifact each | The artifact it governs: `design.md` governs design.md files |
| `rules/workflow/` | Rules constraining operational processes | The process: `committing.md`, `git-safety.md` |
| `rules/communication/` | Rules constraining the wording of agent output | The concern: `terminology.md` |
| `rules/prompt/` | Rules constraining LLM prompt files | The artifact: `prompting.md` |
| `rules/meta/` | Rules for authoring `.claude` assets | The asset type: `rulewriting.md`, `skilling.md` |

- A rule file lives in the directory of the artifact it constrains, not the activity that produces it.
- File names are nouns or gerunds. No bare verbs.
- Always-active status comes from missing `paths:` frontmatter, not from location. A paths-less file stays in its domain directory.

## Audience

- Rule files address the agent. Every sentence is a rule (an observable condition and the required action), a command or an order; a rule file holds no rationale, history, introduction, summary, or definition that no rule of the file uses.

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
- Use H1 for the title, H2 for sections and H3 for subsections. No deeper heading.
- The rule most often violated comes first in its section.
- Tables for structured data. Lists for rules. Code blocks for patterns.
- No redundancy within or across files. Each rule has one authoritative location. Before adding a sentence, search for one that already states the fact and extend it.
- A change to a rule fact updates, in the same change, every skill, hook and project value of the Claude and the Codex configuration repositories and of both native project roots (`.claude/rules/project/`, `.codex/rules/project/`) that cites or implements it, together with the rule's counterpart in the other host, found by searching them for the rule's file name, section heading and parameter names.

## Content

- Every rule states an observable condition and a required action that can be verified; a rule without them is removed.
- Every rule is necessary. Removing it changes nothing → remove.
- No tautologies. "Use meaningful names" adds no information.
- No examples of what not to do unless the wrong pattern is non-obvious.

## Conflict Resolution

- Rules within one file or across files: no contradictions.
- Global rules are language- and project-independent. Language profiles hold only language conventions. Project parameters hold only project values.
- Instruction precedence and existing authorization follow the global entry point's Loading and precedence. A language or project rule names the global setting it overrides.
- A project rule that sets another value for a metric a global rule sets names the replaced global rule in the same bullet: "Replaces global `code/quality.md`: functions under 20 lines."
- Edge cases: one rule states the priority. "X. Exception: Y when Z."
