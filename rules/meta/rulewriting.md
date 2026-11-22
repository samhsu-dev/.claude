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
- `paths:` globs match exactly the files whose editing requires the rule.
- A file states its own rules completely. A cross-reference names an owning file and section for another concern; load that owner before applying its rule.
- Always-active status (no `paths:`) is reserved for rules governing every task. A rule that some task type does not need gets `paths:`. Value-only project files under `rules/project/` follow the same rule: `paths:` names the files their consumers govern.
- File-count test before adding or splitting a rule file: for each task type, count the rule files it forces into context. A change that raises a task type's count without adding a requirement of that task type is wrong.

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
- File names are nouns or gerunds.
- Always-active status comes from missing `paths:` frontmatter, not from location. A paths-less file stays in its domain directory.

## Audience

- Rule files address the agent. Write each rule as one command: who acts, the action, the condition it applies on, and the check that applies it when one exists. Put rationale, history, dates, incident references, introductions, summaries and definitions no rule of the file uses in the decision log or an archive.

## Language

- Order style: state who does what, on which condition. Write the action that replaces a prohibited one, and keep in that action the boundary the prohibition protected.
- One rule per line. One concept per bullet.
- Replace each modifier ("properly", "appropriately", "effectively", "ideally", "simply"), softener ("prefer", "avoid", "consider", "try to") and hedge ("when possible", "if applicable", "as needed", "where appropriate") with the exact action and condition it stands for.
- State each condition explicitly: "X when Y".

## Structure

- Title states the domain.
- Sections group related rules. One topic per section.
- Use H1 for the title, H2 for sections and H3 for subsections, and stop at H3.
- The rule most often violated comes first in its section.
- Tables for structured data. Lists for rules. Code blocks for patterns.
- Give each rule one authoritative location. Before adding a sentence, search for one that already states the fact and extend it.
- A change to a rule rewrites its owning command with all its conditions. The check of each condition runs at the action it governs; when a program cannot decide the condition, that action prints the command.
- A change to a rule fact updates, in the same change, every skill, hook and project value of the Claude and the Codex configuration repositories and of both native project roots (`.claude/rules/project/`, `.codex/rules/project/`) that cites or implements it, together with the rule's counterpart in the other host, found by searching them for the rule's file name, section heading and parameter names.

## Content

- Every rule states an observable condition and a required action that can be verified; remove a rule without them.
- Remove a rule whose removal changes nothing, a tautology ("Use meaningful names") included.
- Give an example of a wrong pattern only when the wrong pattern is non-obvious.

## Conflict Resolution

- Resolve each contradiction between rules, within one file or across files, at the owner in the change that finds it.
- Global rules are language- and project-independent. Language profiles hold only language conventions. Project parameters hold only project values.
- Instruction precedence and existing authorization follow the global entry point's Loading and precedence. A language or project rule names the global setting it overrides.
- A project rule that sets another value for a metric a global rule sets names the replaced global rule in the same bullet: "Replaces global `code/quality.md`: functions under 20 lines."
- When two rules apply to one case, the owning rule states which applies, as a condition of that rule.
