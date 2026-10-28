---
paths:
  - "**/design.md"
  - "**/design-*.md"
---

# Design Documentation Standards

## 1. Required structure

IEEE 1016 Logical viewpoint + Interface viewpoint. Software structure only.

Sections in this order:

| Section | Content |
|--------|--------|
| **Design Overview** | Types/classes; relationships; abstract types; exceptions/errors; dependency roles. |
| **Class / Type Specifications** | Per type: Responsibility, state/fields, methods (Behavior / Input / Output / errors). |
| **Function Specifications** | Per function: **name(signature)** — Responsibility; Behavior; Input; Output; errors. Omit if none. |
| **Exception / Error Types** | Each type and when raised. |
| **Open Gaps** | Undecided points, each stated as an open question; and decided behaviors the code lacks or contradicts, each with the behavior, code symbol and deciding model or spec section. Omit if none. |

Never delete decided design text because no caller exists.

Content boundaries and links follow `CLAUDE.md` Documentation Ownership.

**Overview format**:
- **Classes**: `ClassA`, `ClassB`, `ClassC`
- **Relationships**: `ClassA` extends `ClassB`, `ClassA` contains `ClassC`
- **Abstract**: `ClassE` (implemented by `ClassF`, `ClassG`)
- **Exceptions**: `ExceptionH` extends `ExceptionI`, raised by `ClassA`
- **Dependency roles**: Data holders: `ClassC`. Orchestrator: `ClassA`. Helpers: `ClassB`.

---

## 2. Design principles

### SOLID
- **S** — One reason to change per type.
- **O** — Open for extension, closed for modification.
- **L** — Subtypes fulfill the supertype contract without caller awareness.
- **I** — No client depends on methods it does not use.
- **D** — Depend on abstractions, not concretes.

### Foundational
- **KISS** — Select the design with the fewest mechanisms that satisfies the same requirement and capability constraints.
- Scope of abstractions and configuration: `code/quality.md` Code Smells.
- **DRY** — One authoritative representation per piece of knowledge. Reuse existing data and mechanisms before adding a representation, walk, cache, map or edge.
- **Separation of Concerns** — One concern per module. No overlap.
- Method access contracts: `code/quality.md` Code Structure.
- **Composition over Inheritance** — Contain and delegate. Inherit only for true is-a with shared state.
- Failure signaling: `code/quality.md` Error Handling.

### Naturalness and maintainability

The maintainer reloads context each session and trusts types over execution. Design for that reader.

- Domain wrappers and argument grouping: `code/quality.md`. A closed-value scalar uses an enum.
- **Type boundaries match concept boundaries** — One type, one concept. A type whose fields split by name prefix (`input_`, `output_`) is two concepts.
- **One unit, one abstraction level** — A body mixing collection logic, object construction, and error handling is a split point. Extract the business rule out of the orchestration.
- Granularity follows `code/organization.md` File Responsibility and `code/quality.md` Code Smells.
- **Contract lives in types** — Named fields over optional positional args. Return types exhaust result meaning; type safety contracts: `code/quality.md`.
- **Absence is not failure** — "No result" and "failed" are distinguishable by type, never a shared empty or `None`.

---

## 3. Architectural constraints

- Dependencies are one-way: A uses B → B must not use A.
- Data holders contain only primitives, enums, or other data holders.
- One orchestrator per workflow. Helpers are stateless and receive inputs by argument.
- Files with shared concern grouped into one directory as an internal submodule. One public entry point per directory.
- External API verification and recording: `docs/impl.md`.

