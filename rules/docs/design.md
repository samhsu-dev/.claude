---
paths:
  - "**/design.md"
  - "**/design-*.md"
---

# Kotlin Design Standards

Kotlin-specific design rules. Extends global `docs/design.md`. kotlinlang.org conventions.

---

## Type Selection

- `data class` for value holders (equality by properties, `copy()`, destructuring).
- `sealed class` / `sealed interface` for closed type hierarchies (exhaustive `when`).
- `enum class` for finite fixed sets of constants.
- `interface` for contracts and structural abstraction. Over abstract class when no shared state.
- `abstract class` for type hierarchies with shared state or template methods.
- `value class` (`@JvmInline`) for zero-overhead type wrappers around a single property.
- `object` for singletons and stateless utility groupings.
- `typealias` for long generic types or functional types used repeatedly.

## Module Structure

- Visibility, module layout, packaging, resources: `rules/code/organization.md`.
- The design doc records each type's visibility (public or internal) and its module.

## Value Placement

- Constant vs config object vs data file: decision order in `rules/code/constants.md`.
- The design doc records the tier of each named value the design introduces.

## Class Design

- Primary constructor for required dependencies.
- Use `init` with `require()` or `check()` when construction is the single validation boundary. Global `code/quality.md` owns validation placement.
- `companion object` for factory methods and constants associated with a class.
- Delegation (`by`) over inheritance for composing behavior.
- `open` only when subclassing is intended. Classes final by default.

## Interface Design

- Default implementations for methods with obvious common behavior.
- Properties in interfaces for contract-level state.
- `fun interface` (SAM) for single-method interfaces consumed as lambdas.

## Sealed Hierarchies

- Subclasses in same file (sealed class) or same package (sealed interface).
- Exhaustive `when` — no `else` branch. Compiler enforces completeness.

## Exception Design

- Inherit from `Exception`, not `Throwable` or `Error`.
- Hierarchy by how callers catch, not where raised.
- Structured context: named properties on exception classes, not bare message strings.
- Third-party exceptions mapped at boundary.
- Misuse errors separate from runtime errors: caller misuse raises through `require()` / `check()` (`IllegalArgumentException` / `IllegalStateException`); unexpected runtime failures raise domain exceptions. Expected runtime failures follow API Design. No caller catches a misuse error.

## API Design

- Default-parameter contracts: `rules/code/quality.md` Idiomatic Kotlin.
- Extension functions for operations that do not need private access.
- Properties for O(1) access without side effects. Functions for computation.
- Builder DSL (`apply` / typed receivers) for complex object construction.
- Replaces global `code/quality.md` failure signaling for expected runtime failures: use `Result<T>` or a sealed result. Unexpected failures use exceptions. Misuse errors follow Exception Design.

## Generics

- `out` (covariant) for producers. `in` (contravariant) for consumers.
- Declaration-site variance when possible. Use-site variance only when declaration-site is not feasible.
- Reified type parameters (`inline fun <reified T>`) to preserve type info at runtime.
- Star projection (`*`) when the type parameter is irrelevant.

## Coroutines

- Structured concurrency: parent waits for all children. Canceling parent cancels children.
- `launch` for fire-and-forget. `async`/`await` for concurrent computation needing a result.
- `Dispatchers.Default` for CPU. `Dispatchers.IO` for I/O. Specify explicitly.
- `suspend` functions: no "suspend" in the name.
- `CoroutineScope` as receiver on functions that launch coroutines, not as a parameter.

## Resource Management

- `use` extension for `Closeable`/`AutoCloseable` resources.
- `withContext` for dispatcher switching within coroutines.
