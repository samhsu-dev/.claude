---
paths:
  - "**/docs/todo/**"
---

# Task Management Standards

## Task Format

```text
[state] <action verb> <object> <detail>
  Depends on: <task ids>
  Acceptance: <criteria>
  - [ ] <subtask>
  - [ ] Quality gate (see below)
```

States: `[ ]` todo, `[x]` done, `[~]` in progress, `[-]` skipped.

## Quality Gate

Every task ends with this checklist (do not repeat inline — reference this section):

- [ ] Lint and format (project linter)
- [ ] Type check (project type checker)
- [ ] Unit tests for new/changed public API
- [ ] All tests pass

## Scope Rules

- A task delivers one independent behavior and is committed as one concept (`rules/workflow/committing.md` Staging); one chain session carries one or more tasks in order.
- Action verb + object + detail. No vague titles.
- Explicit dependencies.
- Reference interfaces from design docs. No new design in TODO files.

## File Organization

- Record location and file naming: `rules/workflow/records.md`.
- Tasks that share a module or a cause are adjacent in the file.
- A run lists each task-doc item in its report; the main agent writes it to `docs/todo/<module>.md` in the main checkout and updates task state there when it accepts the run.

## Templates

Feature:

```text
[ ] Implement <feature>
  Acceptance: <criteria>
  - [ ] <subtask>
  - [ ] Quality gate
```

Bug fix:

```text
[ ] Fix <description>
  Acceptance: <repro no longer fails>
  - [ ] Reproduction test, failing
  - [ ] Root cause
  - [ ] Fix
  - [ ] Quality gate
```

Refactor:

```text
[ ] Refactor <component>
  Acceptance: <no behavior change, tests pass>
  - [ ] Analyze
  - [ ] Implement
  - [ ] Update tests
  - [ ] Quality gate
```
