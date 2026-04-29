# Kotlin Quality Gate

Verification steps before and after code changes. Runs per editing session; `workflow/committing.md` covers pre-push.

## Before Editing

- `./gradlew detekt` — check existing warnings.

## After Editing

- `./gradlew detekt` — no new violations.
- `./gradlew test` — all pass.
- `./gradlew build` — compiles clean.

## External Tools

- Context7: library docs before integration.
- DeepWiki: repository structure and patterns.

## Agent Behavior

- No summary/README generation after task completion. Update existing files only.
