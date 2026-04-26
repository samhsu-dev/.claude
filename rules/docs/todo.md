---
paths:
  - "**/todo.md"
---

# Task Management Standards

## Task Format

```
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

- One task = one session of work.
- Action verb + object + detail. No vague titles.
- Acceptance criteria when verifiable.
- Explicit dependencies.
- Reference interfaces from design docs. No new design in TODO files.

## File Organization

- One `todo.md` per phase. Sequential numbering when multiple: `1.todo.md`, `2.todo.md`.
- Group related tasks together.
- Update state immediately after change.

## Templates

Feature:
```
[ ] Implement <feature>
  Acceptance: <criteria>
  - [ ] <subtask>
  - [ ] Quality gate
```

Bug fix:
```
[ ] Fix <description>
  Acceptance: <repro no longer fails>
  - [ ] Reproduce
  - [ ] Root cause
  - [ ] Fix
  - [ ] Regression test
  - [ ] Quality gate
```

Refactor:
```
[ ] Refactor <component>
  Acceptance: <no behavior change, tests pass>
  - [ ] Analyze
  - [ ] Implement
  - [ ] Update tests
  - [ ] Quality gate
```
