---
paths:
  - "**/docs/todo/**"
---

# Kotlin Task Management

Kotlin-specific task conventions. Extends global `docs/todo.md`.

---

## Quality Gate

The global task checklist uses `code/quality.md` Quality Workflow. Its `./gradlew build` step is required for each task.

## Conventions

- Design docs cited by relative path: `path/to/design.md`.
- Test tasks name the test file: `src/test/kotlin/<package>/<Component>Test.kt`.
- Implementation tasks reference `impl.md` for library findings.
