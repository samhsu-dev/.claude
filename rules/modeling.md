---
paths:
  - "**/*model.md"
---

# Domain Model Documentation Standards

IEEE 1016 Information viewpoint + State dynamics viewpoint. Formalizes domain semantics between concept definition (idea.md) and software structure (design.md).

---

## Scope

- One `model.md` per module with non-trivial domain semantics.
- Same directory as paired `idea.md` and `design.md`.
- Contains domain entity semantics, state models, invariants, relation semantics.
- No software structure (classes, methods, fields) -- stays in `design.md`.
- No problem context or scenarios -- stays in `idea.md`.
- No algorithm steps or pseudocode -- goes in `spec.md`.
- No library APIs or coding notes -- stays in `impl.md`.

## Required Sections

Sections in order; include only if they have content:

| Section | Content |
|---------|---------|
| **Entities** | Each domain entity: name, semantic role, existence conditions. One entry per entity kind. |
| **Relations** | Each semantic relation: direction, label requirements, cardinality, meaning. Table format. |
| **State Model** | States, transitions, guards, terminal conditions. State diagram or table. |
| **Invariants** | Structural constraints that hold at all times. One per line, falsifiable. |
| **Cross-Structure Contracts** | Semantic mappings between domain structures (e.g., AST-to-ADG mapping rules). |

## Content Rules

- Define what each entity/relation **means**, not how it is implemented.
- State transitions: source state, trigger, guard, target state. Table or list.
- Invariants: precise and falsifiable. "Every X has at least one Y" not "X should have Y."
- No language-specific types, class names, or method signatures. Domain vocabulary only.
- Reference `idea.md` for rationale. Reference `design.md` for implementation mapping.

## When Required

- Module has domain-specific data structures with semantic constraints.
- Module has state transitions with non-obvious rules.
- Module has structural invariants beyond basic type safety.

## When Not Required

- Module is pure software infrastructure (adapters, I/O, CLI).
- Domain semantics are trivial or fully captured by type signatures in `design.md`.
