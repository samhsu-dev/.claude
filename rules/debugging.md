---
paths:
  - "**/*test*"
  - "**/*Test*"
---

# Kotlin Debugging

Kotlin-specific debugging tools and patterns.

---

## Tools

- `println` / `System.err.println` for quick traces. Remove before commit.
- SLF4J + Logback for structured logging.
- `./gradlew test --info` -- verbose test output.
- `./gradlew test --tests "*.FailingTest" --stacktrace` -- full stack traces.
- `--debug` flag on Gradle for build-level diagnostics.

## Logging

```kotlin
private val logger = LoggerFactory.getLogger(MyClass::class.java)
```

- One logger per class via `LoggerFactory.getLogger`.
- `debug` for flow tracing. `info` for state transitions. `error` for failures.
- Include structured context: `logger.error("Failed to process node={}, reason={}", nodeId, reason)`.
- No sensitive data in logs.

## Common Pitfalls

- Swallowing exceptions with empty `catch` blocks. Always log or rethrow.
- Missing `cause` parameter: `throw DomainException("msg", cause = e)`.
- `lateinit` access before initialization -- `UninitializedPropertyAccessException`.
- Platform type nullability: Java methods returning null assigned to non-null Kotlin types.
- Coroutine cancellation swallowed by `catch (e: Exception)` -- use `catch (e: Exception) { if (e is CancellationException) throw e; ... }` or `ensureActive()`.
- `runBlocking` in production code blocking the caller thread.

## Null Debugging

- Check `!!` usages -- each is a potential NPE.
- Java interop: verify platform types with explicit null checks at boundary.
- `lateinit` properties: use `::prop.isInitialized` to check before access.
