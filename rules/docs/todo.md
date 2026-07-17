---
paths:
  - "**/todo.md"
---

# TypeScript Task Management

TypeScript-specific task conventions.

---

## Quality Gate

Every task ends with:
- [ ] prettier --write and eslint with zero violations
- [ ] tsc --noEmit passes
- [ ] vitest run -- all pass

## Conventions

- Design docs by relative path: Depends on: path/to/design.md.
- Test tasks name the test file: tests/<component>.test.ts.
- Implementation tasks reference impl.md for library findings.
