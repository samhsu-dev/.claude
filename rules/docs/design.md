---
paths:
  - "**/design.md"
  - "**/design-*.md"
---

# TypeScript Design Standards

TypeScript-specific design rules. Google TypeScript Style Guide / TS handbook / typescript-eslint strict.

---

## Type Selection

- interface for object shapes and data holders. readonly on every field not mutated after construction.
- zod schema + z.infer for data crossing a runtime boundary (HTTP, file, env, queue). The schema is the type's source of truth.
- type alias for unions, intersections, tuples, mapped and conditional types.
- as const object or array with a derived literal union for finite value sets. enum permitted; const enum never.
- interface as capability contract for structural subtyping without shared state. Implementations need no implements clause to conform.
- abstract class for type hierarchies with shared state or shared behavior.
- Branded type for zero-overhead distinctions: type UserId = string & { readonly __brand: 'UserId' }.

## Module Structure

- Visibility, module layout, packaging, package data: `rules/code/organization.md`.
- The design doc records each module's visibility (public or internal) and its package.

## Value Placement

- Constant vs config object vs data file: decision order in `rules/code/constants.md`.
- The design doc records the tier of each named value the design introduces.

## Error Design

- Derive from Error. Set name to the class name; pass cause through the constructor.
- Hierarchy by how callers catch, not where thrown.
- Structured context fields (step, reason). No bare message strings.
- Third-party errors mapped to domain errors at the boundary.
- Misuse errors (caller bug) separate from runtime errors (environment failure).
- Expected, recoverable failure modes return a discriminated union result. throw is for contract violations and environment failures.

## API Design

- All branches return a value, or none do.
- Factory functions when construction has configuration or variants.
- Getters for O(1) access. Methods for computation.
- Async is part of the contract: a function returns Promise<T> or T, never sometimes-either.
- One options object parameter beyond two positional parameters.

## Typing Patterns

- Generic functions constrain with extends when the body relies on structure. No unused type parameters.
- Overloads ordered specific to general. A union parameter replaces overloads differing in one position.
- Callback parameters required, callback return void when the result is ignored.
- Literal union or template literal type for finite string spaces.
- satisfies for typed constants that must keep their literal type.
