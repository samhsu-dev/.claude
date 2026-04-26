---
paths:
  - "**/spec.md"
---

# Algorithm Specification Standards

IEEE 1016 Algorithm viewpoint. Formalizes computation logic between domain model (model.md) and coding notes (impl.md).

---

## Scope

- One `spec.md` per module with non-trivial algorithms.
- Same directory as paired `design.md`.
- Contains algorithm steps, invariants, termination arguments, complexity.
- No domain entity definitions -- stays in `model.md`.
- No class structure or method signatures -- stays in `design.md`.
- No library API notes -- stays in `impl.md`.

## Required Sections

Per algorithm:

| Section | Content |
|---------|---------|
| **Problem** | Input, output, correctness condition. One paragraph. |
| **Steps** | Numbered pseudocode. Language-independent. |
| **Invariants** | Loop invariants, maintained properties. One per line. |
| **Termination** | Why the algorithm halts. Variant function or bound. |
| **Complexity** | Time and space. Big-O with variables defined. |

## Content Rules

- Pseudocode uses domain vocabulary from `model.md`, not implementation names.
- One algorithm per heading. Multiple algorithms grouped by concern.
- No language-specific syntax. Pseudocode: unambiguous but language-neutral.
- Edge cases and degenerate inputs documented after main steps.
- Reference `model.md` for entity/state definitions used in steps.

## When Required

- Module implements iterative/recursive algorithms (worklist, fixpoint, graph traversal).
- Correctness depends on invariants not obvious from code.
- Algorithm choice is a design decision (why worklist, not chaotic iteration).

## When Not Required

- Logic is straightforward dispatch or delegation.
- Algorithm is a standard library call (sort, search).
