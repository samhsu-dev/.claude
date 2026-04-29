# Project Rules

Kotlin/Gradle project. Global rules (`~/.claude/rules/`) provide language-agnostic standards. Project rules below add Kotlin-specific guidance.

## Structure

```
.claude/
├── CLAUDE.md                   # This file
└── rules/
    ├── code/
    │   ├── quality.md          # Kotlin code quality and idioms (*.kt)
    │   ├── testing.md          # Kotlin/JUnit 5 conventions (test files)
    │   └── debugging.md        # Kotlin debugging tools (*.kt + test files)
    ├── docs/
    │   ├── design.md           # Kotlin design standards (*design.md)
    │   ├── impl.md             # Kotlin impl.md conventions (*impl.md)
    │   └── todo.md             # Kotlin task conventions (todo.md)
    └── workflow/
        ├── committing.md       # Project commit and push rules
        └── quality-gate.md     # Gradle verification steps
```

Rules with `paths:` frontmatter load only when working with matching files. Rules without `paths:` are always active.

## Build System

- Gradle with Kotlin DSL (`build.gradle.kts`).
- Build command: `./gradlew build`.
- Test command: `./gradlew test`.
