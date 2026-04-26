---
paths:
  - "**/*impl.md"
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

- group:artifact:version — purpose. Add to `build.gradle.kts` dependencies.

## Verification

- Check `impl.md` for existing findings before writing integration code.
- Record all findings immediately. Not in conversation only.
- Verify via DeepWiki, Context7, or minimal test. No guessing.
