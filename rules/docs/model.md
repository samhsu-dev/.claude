---
paths:
  - "**/model.md"
  - "**/model-*.md"
---

# Domain Model Documentation Standards

IEEE 1016 Information viewpoint + State dynamics viewpoint. Formalizes domain semantics between concept definition (concept.md) and software structure (design.md).

---

## Scope

- One `model.md` per module meeting When Required; apply When Not Required as the exception.
- Same directory as paired `concept.md` and `design.md`.
- Content boundaries and links follow `CLAUDE.md` Documentation Ownership.

## Required Sections

Sections in order; include only if they have content:

| Section | Content |
|---------|---------|
| **Entities** | Each domain entity: name, semantic role, existence conditions. One entry per entity kind. |
| **Relations** | Each semantic relation: direction, label requirements, cardinality, meaning. Table format. |
| **State Model** | States, transitions, guards, terminal conditions. State diagram or table. |
| **Invariants** | Structural constraints that hold at all times. One per line, falsifiable. |
| **Cross-Structure Contracts** | Semantic mappings between domain structures (e.g., AST-to-IR mapping rules). |

## Content Rules

- An entity is named by its glossary heading and linked to its entry.
- Define what each relation **means**, not how it is implemented.
- State transitions: source state, trigger, guard, target state. Table or list.
- No language-specific types, class names, or method signatures. Domain vocabulary only.
- Reference `concept.md` for rationale. Reference `design.md` for implementation mapping.

## When Required

- Module has domain-specific data structures with semantic constraints.
- Module has state transitions with non-obvious rules.
- Module has structural invariants beyond basic type safety.

## When Not Required

- Module is pure software infrastructure (adapters, I/O, CLI).
- Domain semantics are trivial or fully captured by type signatures in `design.md`.
