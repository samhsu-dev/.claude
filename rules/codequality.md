---
paths:
  - "**/*.kt"
---

# Kotlin Code Quality

Kotlin-specific rules. kotlinlang.org coding conventions. detekt defaults.

---

## Naming

- Packages: all lowercase, no underscores.
- Classes/Objects: PascalCase.
- Functions/Properties/Variables: camelCase.
- Constants (`const val`, top-level/object `val` with no custom getter): UPPER_SNAKE_CASE.
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

`public`/`protected`/`private`/`internal` -> `expect`/`actual` -> `final`/`open`/`abstract`/`sealed`/`const` -> `external` -> `override` -> `lateinit` -> `tailrec` -> `vararg` -> `suspend` -> `inner` -> `enum`/`annotation`/`fun` -> `companion` -> `inline`/`value` -> `infix` -> `operator` -> `data`.

## Imports

- No wildcard imports. Explicit imports only.
- ASCII sorted.

## Null Safety

- `?.` for safe access. `?:` for defaults. `as?` for safe casts.
- `!!` only when provably non-null through business logic the compiler cannot verify. Never on untrusted external data. Never in public APIs.
- `?.let { }` for non-null execution blocks.
- `filterNotNull()` to remove nulls from collections.
- Public functions and properties: always declare explicit Kotlin types for Java interop platform types.

## Idiomatic Kotlin

- `val` over `var`. Immutable collections (`listOf`, `setOf`, `mapOf`) over mutable.
- Default parameter values over function overloads.
- Expression bodies (`fun foo() = expr`) for single-expression functions.
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

| Metric | Limit |
|--------|-------|
| Method length | 60 lines |
| Class length | 600 lines |
| Cyclomatic complexity / method | 14 |
| Cognitive complexity / method | 15 |
| Function parameters | 5 (6 for constructors) |
| Nesting depth | 4 levels |
| Return statements / function | 2 |

## Code Smells

- Abstract class with no abstract members -> use concrete class or interface.
- Data class with mutable properties or non-conversion functions.
- `protected` members in final (non-`open`) classes.
- Utility class with public constructor -> private constructor.
- Magic numbers -> named constants.
- Functions returning only a constant -> `const val`.
- Explicit `Unit` return type -> omit.
- Redundant `constructor` keyword.
- Object literals implementing single method -> lambda.

---

## Quality Workflow

### Before editing
- `./gradlew detekt` -- check warnings.

### After editing
- `./gradlew detekt` -- no new violations.
- `./gradlew test` -- all pass.
- `./gradlew build` -- compiles clean.

---

## External Tools

- Context7: library docs before integration.
- DeepWiki: repository structure and patterns.

## Workflow

- No summary/README generation after task completion. Update existing files only.
