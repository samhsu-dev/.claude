---
paths:
  - "**/docs/todo/**"
---

# Kotlin Task Management

Kotlin-specific task conventions. Extends global `docs/todo.md`.

---

## Quality Gate

Project commands for the global quality gate:
- Linter: `./gradlew detekt` — no new violations.
- Test runner: `./gradlew test` — all pass.
- Compilation and build verification: `./gradlew build` — compiles clean; required in every task's quality gate.

## Conventions

- Design docs cited by relative path: `path/to/design.md`.
- Test tasks name the test file: `src/test/kotlin/<package>/<Component>Test.kt`.
- Implementation tasks reference `impl.md` for library findings.
