---
paths:
  - "**/design.md"
  - "**/design-*.md"
---

# TypeScript Design Standards

TypeScript-specific design rules. Extends global `docs/design.md`. Google TypeScript Style Guide / TypeScript handbook / typescript-eslint `strictTypeChecked`.

---

## Type Selection

- `interface` for data holders. `readonly` on every field not mutated after construction.
- zod schema with `z.infer` for data requiring runtime validation: values crossing a runtime boundary (HTTP, file, env, queue). The schema is the type's source of truth.
- A closed set of domain values is an `as const` object with a same-named derived union: `const Status = { ACTIVE: "active", CLOSED: "closed" } as const; type Status = (typeof Status)[keyof typeof Status];`. Validated at a boundary by `z.enum(Status)`. Never `enum`: `erasableSyntaxOnly` rejects it.
- A bare literal union only for values an external interface fixes or an overload selects.
- `interface` as capability contract for structural subtyping without shared state. Implementations need no `implements` clause to conform.
- `abstract class` for type hierarchies with shared state.
- Branded type for zero-overhead type distinctions: `type UserId = string & { readonly __brand: "UserId" }`.

## Module Structure

- Visibility, module layout, packaging, package data: `rules/code/organization.md`.
- The design doc records each module's visibility (public or internal) and its package.

## Value Placement

- Constant vs config object vs data file: decision order in `rules/code/constants.md`.
- The design doc records the tier of each named value the design introduces.

## Exception Design

- Derive from `Error`. Set `name` to the class name.
- Hierarchy by how callers catch, not where thrown.
- Structured context fields (step, reason). No bare message strings.
- Third-party errors mapped to domain errors at the boundary.
- Misuse errors separate from runtime errors: caller misuse of the package's API throws a builtin (`TypeError` for a wrong type or shape, `RangeError` for a value outside the allowed range, `Error` for a call in the wrong state); runtime failures throw domain errors. No caller catches a misuse error.

## API Design

- All branches return a value, or none do.
- Factory functions when construction has configuration or variants.
- Getters for O(1) access without side effects. Methods for computation.
- Async is part of the contract: a function returns `Promise<T>` on every path or on none.

## Typing Patterns

- Generic functions constrain with `extends` when the body relies on structure. No type parameter used only once: `@typescript-eslint/no-unnecessary-type-parameters` in `strictTypeChecked` checks it.
- Overloads when the return type depends on the input type, ordered specific to general.
- Template literal type for a structured finite string space.
