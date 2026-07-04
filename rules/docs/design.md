---
paths:
  - "**/design.md"
  - "**/design-*.md"
---

# Python Design Standards

Python-specific design rules. PEP 8 / PEP 20 / PEP 257 / PEP 484 / PEP 544.

---

## Type Selection

- @dataclass for data holders. @dataclass(frozen=True) for immutable data holders.
- BaseModel for validated or schema-generated data (LLM structured output).
- TypedDict for typed dictionary shapes (TOML/JSON config).
- Protocol + @runtime_checkable for structural subtyping without shared state.
- ABC + @abstractmethod for type hierarchies with shared state.
- NewType for zero-overhead type distinctions.

## Module Structure

- Visibility, module layout, packaging, package data: `rules/code/organization.md`.
- The design doc records each module's visibility (public or internal) and its package.

## Value Placement

- Constant vs config object vs data file: decision order in `rules/code/constants.md`.
- The design doc records the tier of each named value the design introduces.

## Exception Design

- Derive from Exception, not BaseException.
- Hierarchy by how callers catch, not where raised.
- Structured context fields (step, reason). No bare strings.
- Third-party exceptions mapped at boundary.
- Misuse errors separate from runtime errors.

## API Design

- All branches return a value, or none do.
- Factory functions when construction has configuration or variants.
- Properties for O(1) access. Methods for computation.

## Typing Patterns

- TypeVar(bound=) for generic functions on a type hierarchy.
- @overload when return type depends on input type.
- Literal for finite value sets.
