# Project Rules

Kotlin/Gradle project. Global rules (`~/.claude/rules/`) provide language-agnostic standards. Project rules below add Kotlin-specific guidance.

## Structure

```
.claude/
├── CLAUDE.md               # This file
└── rules/
    ├── code/               # Writing code
    │   ├── quality.md      # Kotlin code quality and toolchain (*.kt)
    │   ├── constants.md    # Value placement: constant vs config vs data file (*.kt)
    │   ├── organization.md # Kotlin file naming, module layout, visibility, resources (*.kt, *.kts)
    │   ├── testing.md      # Kotlin/JUnit 5 conventions (test files)
    │   └── debugging.md    # Kotlin debugging tools (*.kt, test files)
    │
    ├── docs/               # Writing documentation
    │   ├── design.md       # Kotlin design standards (design.md, design-*.md)
    │   ├── impl.md         # Kotlin impl.md conventions (impl.md, impl-*.md)
    │   └── todo.md         # Kotlin task conventions (todo.md)
    │
    └── workflow/           # Operational processes
        └── committing.md   # Project commit and push rules
```

Rules use `paths:` frontmatter to load only when working with matching files.

## Build System

- Gradle with Kotlin DSL (`build.gradle.kts`). Multi-module build declared in `settings.gradle.kts`.
- Build command: `./gradlew build`.
- Test command: `./gradlew test`.

## Workflow

- No summary/README generation after task completion. Update existing files only.
