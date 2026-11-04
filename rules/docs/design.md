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
- `value class` (`@JvmInline`) for a type wrapper around a single property; boxing: `rules/code/quality.md` Types and Errors.
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

## Types and Errors

- Sealed hierarchies, exception design, failure signaling and coroutine scopes: `rules/code/quality.md` Types and Errors and Coroutines.

## API Design

- Default-parameter contracts: `rules/code/quality.md` Idiomatic Kotlin.
- Extension functions for operations that do not need private access.
- Properties for O(1) access without side effects. Functions for computation.
- Builder DSL (`apply` / typed receivers) for complex object construction.

## Generics

- `out` (covariant) for producers. `in` (contravariant) for consumers.
- Declaration-site variance when possible. Use-site variance only when declaration-site is not feasible.
- Reified type parameters (`inline fun <reified T>`) to preserve type info at runtime.
- Star projection (`*`) when the type parameter is irrelevant.

## Resource Management

- `use` extension for `Closeable`/`AutoCloseable` resources.
- `withContext` for dispatcher switching within coroutines.
