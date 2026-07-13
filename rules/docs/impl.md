---
paths:
  - "**/impl.md"
  - "**/impl-*.md"
---

# Kotlin Implementation Documents

Kotlin-specific `impl.md` conventions. Extends global `docs/impl.md`.

---

## API Entry Format

**[library]** `import library.Thing` — when/gotcha.

Example:
**[kotlinx-serialization]** `@Serializable data class Foo(...)` — requires compiler plugin; no-arg constructor generated.
**[kotlinx-coroutines]** `withContext(Dispatchers.IO) { }` — switches dispatcher; does not launch new coroutine.

## Dependency Entry Format

- group:artifact:version — purpose. Version catalog alias in `gradle/libs.versions.toml`, referenced from `build.gradle.kts`.
