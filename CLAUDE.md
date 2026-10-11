# Project Rules

Kotlin/Gradle project. Global rules (`~/.claude/rules/`) provide language-agnostic standards. Project rules in `.claude/rules/` add Kotlin-specific guidance.

## Build System

- Gradle with Kotlin DSL (`build.gradle.kts`). Multi-module build declared in `settings.gradle.kts`.
- Build command: `./gradlew build`.
- Test command: `./gradlew test`.

## Workflow

- No summary/README generation after task completion. Update existing files only.
