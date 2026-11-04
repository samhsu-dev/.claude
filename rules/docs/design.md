---
paths:
  - "**/design.md"
  - "**/design-*.md"
---

# Python Design Standards

Python-specific design rules. Extends global `docs/design.md`. PEP 8 / PEP 20 / PEP 257 / PEP 484 / PEP 544.

---

## Type Selection

- `@dataclass` for data holders. `@dataclass(frozen=True)` for immutable data holders.
- `BaseModel` for data requiring runtime validation or schema generation.
- `TypedDict` for typed dictionary shapes (TOML/JSON config).
- `Enum` for a closed set of domain values. `Literal` only for values an external interface fixes or an `@overload` selects.
- `Protocol` + `@runtime_checkable` for structural subtyping without shared state.
- `ABC` + `@abstractmethod` for type hierarchies with shared state.
- `NewType` for zero-overhead type distinctions.

## Module Structure

- Visibility, module layout, packaging, package data: `rules/code/organization.md`.
- The design doc records each module's visibility (public or internal) and its package.

## Value Placement

- Constant vs config object vs data file: decision order in `rules/code/constants.md`.
- The design doc records the tier of each named value the design introduces.

## Exception Design

- Exception hierarchy, context and misuse errors: `rules/code/quality.md` Error Handling.

## API Design

- All branches return a value, or none do.
- Factory functions when construction has configuration or variants.
- Properties for O(1) access without side effects. Methods for computation.

## Typing Patterns

- `TypeVar(bound=)` for generic functions on a type hierarchy.
- `@overload` when return type depends on input type.
