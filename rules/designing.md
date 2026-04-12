---
paths:
  - "**/design.md"
---

# Design Documentation Standards

## 1. Required structure

Sections in this order:

| Section | Content |
|--------|--------|
| **Design Overview** | Types/classes; relationships (one-way only); abstract types; exceptions/errors; dependency roles. |
| **Class / Type Specifications** | Per type: Responsibility, state/fields, methods (Behavior / Input / Output / errors). |
| **Function Specifications** | Per function: **name(signature)** — Responsibility; Behavior; Input; Output; errors. Omit if none. |
| **Exception / Error Types** | Each type and when raised. |
| **Validation Rules** | Per component. |

**Overview format**:
- **Classes**: `ClassA`, `ClassB`, `ClassC`
- **Relationships**: `ClassA` extends `ClassB`, `ClassA` contains `ClassC` (one-way; no A↔B)
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
- **KISS** — Simplest design that satisfies the requirement.
- **YAGNI** — Implement only what is needed now.
- **DRY** — One authoritative representation per piece of knowledge.
- **Separation of Concerns** — One concern per module. No overlap.
- **Law of Demeter** — Call only own methods, parameter methods, locally created objects, direct attributes.
- **Composition over Inheritance** — Contain and delegate. Inherit only for true is-a with shared state.
- **Fail-fast** — Detect and report errors at the earliest point.

---

## 3. Architectural constraints

- Dependencies are one-way: A uses B → B must not use A.
- Data holders contain only primitives, enums, or other data holders.
- One orchestrator per workflow. Helpers are stateless and receive inputs by argument.
- Files with shared concern grouped into one directory as an internal submodule. One public entry point per directory.
- No guessing. Verify via documentation, source code, or test. If unverifiable, ask.
- Search for existing libraries before implementing.
- Verify external library API via DeepWiki/Context7 or minimal test before use. Record findings in `implementation.md`.

---

## 4. Change policy

- No backward-compatibility requirements.
- No changes to return types, signatures, or behavior without explicit user request.
- No additions, removals, or renames of public API without explicit instruction.
