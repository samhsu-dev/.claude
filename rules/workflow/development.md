# Development Workflow

Phase pipeline for feature development. Always active. The content rules of each document live in `rules/docs/<type>.md`.

---

## Pipeline

| # | Phase | Document | Gate | Skip when |
|---|-------|----------|------|-----------|
| 1 | Concept | `concept.md` | User confirms scope, terminology, boundaries | Never |
| 2 | Domain Model | `model.md` | User confirms entities, invariants, state rules | Pure infrastructure (adapters, I/O, CLI) or trivial domain semantics |
| 3 | Algorithm | `spec.md` | User confirms correctness and termination | No worklist, fixpoint, graph traversal, or recursive structure |
| 4 | Design | `design.md` | User confirms structure and responsibility allocation | Never |
| 5 | Research | `impl.md` | None; agent reports findings | Never |
| 6 | Plan | `todo.md` | User confirms task breakdown and order | Never |
| 7 | Code | source code | None; agent follows `todo.md` in order | Never |
| 8 | Verify | passing quality gate | `todo.md` Quality Gate checklist passes | Never |

- Each phase reads the documents of the earlier phases as input.
- A skipped phase states its skip reason in the next document.
- Research verifies every external API via documentation, DeepWiki, Context7, or a minimal test, and records each finding in `impl.md` at once.
- Code commits each `todo.md` task the moment it lands runnable, before the next task starts.

## Existing Codebase Changes

- Read the existing docs in the target directory first.
- Start at the earliest phase the change affects.
- Update documents in place. Never recreate them from scratch.
- A concept or model change revises every downstream document before code changes.

## Phase Transitions

- Forward only. Exception: Research findings that invalidate a design assumption return to Design, and `design.md` is revised before work continues.
- A backward step states its reason.
- Each phase completes before the next begins.

## Index

- A directory with 3+ documentation files has an `index.md`, updated after any phase that adds or renames a file.
