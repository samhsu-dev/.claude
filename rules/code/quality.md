---
paths:
  - "**/*.kt"
---

# Kotlin Code Quality

Kotlin-specific rules. Extends global `code/quality.md`. kotlinlang.org conventions. detekt defaults.

---

## Naming

- Classes/Objects: PascalCase.
- Functions/Properties/Variables: camelCase.
- Constant naming and placement: `code/constants.md`.
- Backing properties: `private val _elementList` / `val elementList`.
- Type parameters: single capital letter (`T`, `E`, `K`, `V`).
- Acronyms: two-letter uppercase both (`IOStream`). Longer capitalize first only (`XmlHttpRequest`).

## Formatting

- 4-space indentation. Never tabs.
- 120-character line limit.
- K&R braces. `else`/`catch`/`finally` on same line as closing brace.
- Spaces around binary operators except range (`0..i`).
- Trailing commas at declaration sites.
- Chained calls: `.` or `?.` on next line with single indent.
- Lambdas: spaces around braces and arrow. Single lambda outside parentheses.

## Modifier Order

`public`/`protected`/`private`/`internal` → `expect`/`actual` → `final`/`open`/`abstract`/`sealed`/`const` → `external` → `override` → `lateinit` → `tailrec` → `vararg` → `suspend` → `inner` → `enum`/`annotation`/`fun` → `companion` → `inline`/`value` → `infix` → `operator` → `data`.

## Imports

- No wildcard imports. Explicit imports only.
- ASCII sorted.

## Null Safety

- `?.` for safe access, `?:` for a contractually optional value, and `as?` for safe casts. Missing required values follow global `code/quality.md` Error Handling.
- `!!` only when provably non-null through business logic the compiler cannot verify. Never on untrusted external data. Never in public APIs.
- `filterNotNull()` to remove nulls from collections.
- Public functions and properties: explicit Kotlin types for Java interop platform types.

## Idiomatic Kotlin

- `val` over `var`. Immutable collections (`listOf`, `setOf`, `mapOf`) over mutable.
- Default parameter values for optional parameters, over function overloads.
- Expression bodies (`fun foo(): Type = expr`) for single-expression functions.
- String templates (`"$name"`) over concatenation. Multiline strings with `trimIndent()`.
- `if` for binary conditions. `when` for 3+ branches. Both as expressions where applicable.
- `require()` for argument validation. `check()` for state validation. `error()` for illegal states.
- `emptyList()` / `emptySet()` / `emptyMap()` over `listOf()` for empty collections.
- `is` / `!is` for type checks. Smart casts after type check.
- Property syntax for Java getters: `obj.name` not `obj.getName()`.
- Implicit `it` only in short non-nested lambdas. Named parameters in nested/multiline lambdas.

## Scope Functions

| Function | Ref | Returns | Use |
|----------|-----|---------|-----|
| `let` | `it` | Lambda result | Non-null execution (`?.let`), limited-scope variables |
| `run` | `this` | Lambda result | Object config + compute result |
| `with` | `this` | Lambda result | Multiple calls on an object |
| `apply` | `this` | Object | Builder / object configuration |
| `also` | `it` | Object | Side effects (logging, validation) |

- Never nest scope functions. Max depth: 1.

## Extension Functions

- Extensions resolve statically. Member functions take precedence.
- Extensions cannot access `private`/`protected` members.
- Class-related extensions: same file as the class. Client-specific extensions: near the client.
- No extensions on `Any` without strong justification.
- Extension properties: no backing fields, explicit getter required.

## Collections

- `filter`, `map`, `fold` over manual loops.
- `for` over `forEach` unless receiver is nullable or chained.
- `..<` for open-ended ranges.
- `sequence { }` for lazy pipelines on large collections.

## Complexity Thresholds (detekt)

- The detekt default thresholds apply: `buildUponDefaultConfig = true` and `maxIssues: 0` in `config/detekt/detekt.yml`. `./gradlew detekt` enforces them.
- Replaces global `code/quality.md` function length, parameter count and indentation thresholds, and global `code/organization.md` file length, with the detekt thresholds above.

## Code Smells

- Abstract class with no abstract members → concrete class or interface.
- Data class with mutable properties.
- A utility grouping uses the stateless `object` form in `docs/design.md` Type Selection; it has no public constructor.
- A function returning a compile-time constant becomes `const val`. A fixed runtime value becomes `val` under `code/constants.md`.
- Replaces global `code/quality.md` return-type annotations for `Unit`: omit `Unit` unless the Visibility requirements in `rules/code/organization.md` require an explicit return type.
- Redundant `constructor` keyword.
- Object literals implementing single method → lambda.

---

## Quality Workflow

### Before editing
- `./gradlew detekt` — check existing violations.

### After editing
- `./gradlew detekt` — no new violations.
- `./gradlew test` — unit tests pass; run any separate integration suite as part of the all-tests task gate.
- `./gradlew build` — compiles clean.

---

## Toolchain

| Tool | Command | Purpose |
|------|---------|---------|
| detekt | `./gradlew detekt` | Static analysis + style (default rule set) |
| JUnit 5 | `./gradlew test` | Test runner |
| Kover | `./gradlew koverHtmlReport` | Coverage report |
| Gradle | `./gradlew build` | Compile + full verification |
