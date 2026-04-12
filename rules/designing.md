---
paths:
  - "**/design.md"
---

# Kotlin Design Standards

Kotlin-specific design rules. kotlinlang.org conventions and idioms.

---

## Type Selection

- `data class` for value holders (equality by properties, `copy()`, destructuring). Properties immutable (`val`) by default.
- `sealed class` / `sealed interface` for closed type hierarchies (exhaustive `when`).
- `enum class` for finite fixed sets of constants.
- `interface` for contracts and structural abstraction. Prefer over abstract class when no shared state.
- `abstract class` for type hierarchies with shared state or template methods.
- `value class` (`@JvmInline`) for zero-overhead type wrappers around a single property.
- `object` for singletons and stateless utility groupings.
- `typealias` for long generic types or functional types used repeatedly.

## Visibility

| Modifier | Scope |
|----------|-------|
| `public` (default) | Visible everywhere. Omit keyword unless in explicit API mode. |
| `internal` | Visible within the module. Use for implementation details shared across files. |
| `private` | Visible within the file (top-level) or class. |
| `protected` | Visible in class and subclasses. Only on `open`/`abstract` members. |

- Public when consumers need it. `internal` for module implementation details. `private` for file/class-local.
- No `protected` on final classes.

## Class Design

- Primary constructor for required dependencies. Default values for optional parameters.
- `init` blocks for validation. `require()` / `check()` inside `init`.
- `companion object` for factory methods and constants associated with a class.
- Delegation (`by`) over inheritance for composing behavior.
- `open` only when subclassing is intended. Classes final by default.

## Interface Design

- Small, focused interfaces. One responsibility per interface.
- Default implementations for methods with obvious common behavior.
- Properties in interfaces for contract-level state.
- `fun interface` (SAM) for single-method interfaces consumed as lambdas.

## Sealed Hierarchies

- `sealed` when all subtypes are known at compile time.
- Subclasses in same file (sealed class) or same package (sealed interface).
- Exhaustive `when` -- no `else` branch. Compiler enforces completeness.

## Exception Design

- Inherit from `Exception`, not `Throwable` or `Error`.
- Hierarchy by how callers catch, not where raised.
- Structured context: named properties on exception classes, not bare message strings.
- Third-party exceptions mapped at boundary. Internal code raises domain exceptions only.

## API Design

- Default parameter values over overloads.
- Extension functions for operations that do not need private access.
- Properties for O(1) access without side effects. Functions for computation.
- Builder DSL (`apply` / typed receivers) for complex object construction.
- `Result<T>` or sealed class for expected failures. Exceptions for unexpected failures.

## Generics

- `out` (covariant) for producers. `in` (contravariant) for consumers.
- Declaration-site variance on the class when possible. Use-site variance (`out`/`in` at call site) only when declaration-site is not feasible.
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
