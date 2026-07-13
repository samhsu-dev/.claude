---
paths:
  - "**/*.kt"
  - "**/*.kts"
---

# Kotlin File Naming and Organization

Kotlin realization of global `rules/code/organization.md`. kotlinlang.org naming; layout per Gradle defaults.

---

## Package Naming

- Package names: lowercase letters and digits, no underscores. A multi-word segment becomes a nested package: `http.client`, not `http_client`.

## File Naming

- Kotlin source files: PascalCase with `.kt` extension. Overrides the global lowercase-underscore rule — Kotlin community convention.
- A file holding one primary class is named after the class: `Parser.kt`.
- A file holding multiple related declarations is named after the responsibility it owns, not after any one class.

## Module Layout

Gradle default source sets per module:

| Path | Contents |
|------|----------|
| `src/main/kotlin/` | Production sources, packages mirror directory structure |
| `src/main/resources/` | Bundled resource files |
| `src/test/kotlin/` | Tests, mirroring main packages |
| `src/test/resources/` | Test data files |

- Repo root holds `settings.gradle.kts`, `gradle.properties`, `gradle/libs.versions.toml`, and the Gradle wrapper.

## Multi-Module Repository

- A repo containing multiple Kotlin modules is one Gradle build: root `settings.gradle.kts` declares each module with `include("<module>")`.
- One version catalog: `gradle/libs.versions.toml`. Build scripts reference `libs.<alias>`. No literal dependency versions in `build.gradle.kts`.
- A module depends on a sibling via `implementation(project(":<module>"))`. `api(...)` only when the dependency's types appear in the module's own public API.
- A vendored external repo is a composite build: `includeBuild` in `settings.gradle.kts`, with `dependencySubstitution` mapping its published coordinates to the local project.

## Visibility

Public = used by other modules or by consumers of a published module. Internal = used only within one module.

- Declarations are `internal` until a consumer outside the module exists. Public (no modifier) only for the module's intended API.
- `private` for declarations used only within one file (top-level) or one class (member).
- No `protected` members in final (non-`open`) classes.
- Published library modules enable `explicitApi()`: every public declaration carries an explicit visibility modifier and return type.

## Entry Points

- The CLI module applies the `application` plugin; the entry class is set via `application { mainClass }` in `build.gradle.kts`.
- `fun main` contains argument parsing and delegation only. Business logic lives in library modules.

## Resources

- Resource files in `src/main/resources/`, namespaced by package path.
- Read resources via the classloader: `javaClass.getResourceAsStream(...)`. Never via `File` path arithmetic against the working directory.
