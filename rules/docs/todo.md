---
paths:
  - "**/todo.md"
---

# Kotlin Task Management

Kotlin-specific task conventions. Extends global `docs/todo.md`.

---

## Quality Gate

Every task ends with:
- [ ] `./gradlew build` — compiles clean
- [ ] `./gradlew test` — all pass

## Conventions

- Design docs by relative path: `Depends on: path/to/design.md`.
- Test tasks name the test file: `src/test/kotlin/<package>/<Component>Test.kt`.
- Implementation tasks reference `impl.md` for library findings.
