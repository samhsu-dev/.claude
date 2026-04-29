# Project Rules

Kotlin/Gradle project. Global rules (`~/.claude/rules/`) provide language-agnostic standards. Project rules below add Kotlin-specific guidance.

## Structure

```
.claude/
├── CLAUDE.md           # This file
└── rules/
    ├── codequality.md  # Kotlin code quality and idioms (*.kt)
    ├── committing.md   # Project commit, push, and PR rules
    ├── designing.md    # Kotlin design standards (design.md)
    ├── implementing.md # Implementation doc standards (*impl.md)
    ├── tasking.md      # Task management standards (todo.md)
    ├── testing.md      # Kotlin testing standards (test files)
    └── debugging.md    # Kotlin debugging standards (test files)
```

Global rules provide standards for `idea.md`, `model.md`, `spec.md`. No project-level overrides needed — Kotlin-specific guidance lives in `designing.md` and `implementing.md`.

Rules use `paths:` frontmatter to load only when working with matching files.

## Build System

- Gradle with Kotlin DSL (`build.gradle.kts`).
- Build command: `./gradlew build`.
- Test command: `./gradlew test`.
