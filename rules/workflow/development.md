# Development Workflow

Phase pipeline for feature development. Always active. The content rules of each document live in `rules/docs/<type>.md`.

---

## Pipeline

| # | Phase | Document | Gate | Skip when |
|---|-------|----------|------|-----------|
| 1 | Concept | `concept.md` | User confirms scope, terminology, boundaries | Never |
| 2 | Domain Model | `model.md` | User confirms entities, invariants, state rules | Applicability criteria in `rules/docs/model.md` require no model |
| 3 | Algorithm | `spec.md` | User confirms correctness and termination | Applicability criteria in `rules/docs/spec.md` When Required and When Not Required require no spec |
| 4 | Design | `design.md` | User confirms structure and responsibility allocation | Never |
| 5 | Research | `impl.md` | None; agent reports findings | Never |
| 6 | Plan | task doc `docs/todo/<module>.md` | User confirms task breakdown and order | Never |
| 7 | Code | source code | None; agent follows the task doc in order | Never |
| 8 | Verify | passing quality gate | Task doc Quality Gate checklist passes | Never |

- Each phase reads the documents of the earlier phases as input.
- A skipped phase states its skip reason in the next document.
- Research verifies every external API via documentation, DeepWiki, Context7, or a minimal test, and records each finding in `impl.md` at once.
- Code commits each task the moment it lands runnable, before the next task starts.

## Existing Codebase Changes

- Read the existing docs in the target directory first.
- Start at the earliest phase the change affects.
- Update documents in place. Never recreate them from scratch.
- A change rewrites the section that owns the fact. It never appends a paragraph or a note beside the text it changes.
- A concept or model change revises every downstream document before code changes.

## Phase Transitions

- Forward only. Exception: Research findings that invalidate a design assumption return to Design, and `design.md` is revised before work continues.
- A backward step states its reason.
- Each phase completes before the next begins.

## Reader Review

- After every complete revision of a module's documents is committed, a reader new to the repository reads them from `index.md`: concept, model, design, impl, in that order, the documents only.
- It reports with file:line every place it cannot follow: an undefined or generic-looking term, a step it cannot trace, a diagram that differs from its text, a missing reason, a term whose meaning drifts, a class or layer that does not match what it groups, a section a maintainer cannot change safely without reading other files.
- Acceptance: accurate semantics and sound abstraction, so the documents are easy to understand and easy to maintain.
- A fix changes the documents, never the algorithm.

## Index

- Index creation and updates after a stage adds or renames a file: `rules/docs/index.md`.
