# Development Workflow

Phase pipeline for feature development. Always active.

---

## Pipeline

```
Concept → Model → Algorithm → Design → Research → Plan → Code → Verify
            ↑         ↑
        conditional conditional
```

Each phase produces one document. Later phases read earlier documents as input. No phase skipped without explicit justification.

## Phases

### 1. Concept (`concept.md`)

- **Input:** user request or problem statement.
- **Output:** `concept.md` — problem, scope, terminology, data flow, scenarios.
- **Gate:** user confirms scope, terminology, and boundaries before proceeding.
- **Rules:** concepts and vocabulary only. No domain semantics, no software structure, no code.

### 2. Domain Model (`model.md`) — conditional

- **Input:** `concept.md`.
- **Output:** `model.md` — entities, relations, state model, invariants, cross-structure contracts.
- **Gate:** user confirms entities, invariants, and state rules before proceeding.
- **Skip when:** module is pure infrastructure (adapters, I/O, CLI) or domain semantics are trivial. State skip reason explicitly.
- **Rules:** domain vocabulary only. No class names, no method signatures, no algorithms.

### 3. Algorithm (`spec.md`) — conditional

- **Input:** `model.md` (or `concept.md` if model skipped).
- **Output:** `spec.md` — problem, steps, invariants, termination, complexity.
- **Gate:** user confirms correctness and termination before proceeding.
- **Skip when:** no non-trivial algorithms (no worklists, fixpoints, graph traversals, recursive structures). State skip reason explicitly.
- **Rules:** pseudocode in domain vocabulary. No language-specific syntax, no class structure.

### 4. Design (`design.md`)

- **Input:** `concept.md`, `model.md`, `spec.md` (whichever exist).
- **Output:** `design.md` — types, relationships, responsibilities, method specifications.
- **Gate:** user confirms structure and responsibility allocation before proceeding.
- **Rules:** software structure only. No domain semantics (stays in `model.md`), no algorithm steps (stays in `spec.md`), no library APIs.

### 5. Research (`impl.md`)

- **Input:** `design.md`.
- **Output:** `impl.md` — library findings, API snippets, developer instructions.
- **Gate:** none. Agent proceeds, reports findings.
- **Rules:** verify every API via documentation, DeepWiki, Context7, or minimal test. Record all findings immediately. If findings invalidate design assumptions, return to Phase 4 and revise `design.md` before continuing.

### 6. Plan (`todo.md`)

- **Input:** `design.md`, `impl.md`.
- **Output:** `todo.md` — ordered tasks with dependencies, acceptance criteria, subtasks.
- **Gate:** user confirms task breakdown and order before proceeding.
- **Rules:** reference interfaces from `design.md`. Reference libraries from `impl.md`. One task = one session of work. No new design in task files.

### 7. Code

- **Input:** `todo.md`, `impl.md`, `model.md`, `design.md`.
- **Output:** source code implementing tasks in order.
- **Gate:** none. Agent proceeds per task list.
- **Rules:** follow `code/quality.md` and `code/testing.md`. Check `impl.md` before using external libraries. Each task committed separately per `workflow/committing.md`.

### 8. Verify

- **Input:** completed code.
- **Output:** all quality gate checks pass.
- **Rules:** run project quality gate (`workflow/quality-gate.md`). Fix failures before reporting completion.

## Existing Codebase Changes

- Read existing docs in the target directory first.
- Start at the earliest phase affected by the change.
- Update documents — do not recreate from scratch.
- Concept or model changes cascade: revise all downstream docs before writing code.

## Phase Transitions

- Forward only, except: Research (Phase 5) may trigger Design (Phase 4) revision.
- Revision reason stated explicitly. No silent backtracking.
- Each phase completes fully before the next begins. No interleaving.

## Index (`index.md`)

- Create or update `index.md` when a directory contains 3+ documentation files.
- Update after any phase that adds or renames a file.
