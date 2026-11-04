# Development Workflow

Parameter `completion` is supplied by the project rule files under `rules/project/`, in `completion.md`.

Task modes follow `workflow/multi-agent.md` Task Modes. Simple and Routine reuse existing decisions and perform only affected steps below; Full uses the affected design stages and independent review. Outcome and scope follow `workflow/change-policy.md`. Document content follows `rules/docs/<type>.md`.

---

## Pipeline

| # | Phase | Document | Gate | Skip when |
|---|-------|----------|------|-----------|
| 1 | Concept | `concept.md`; glossary entries for its terms | User confirms scope, terminology, boundaries | Existing scope and concepts remain unchanged |
| 2 | Domain Model | `model.md` | User confirms entities, invariants, state rules | Applicability criteria in `rules/docs/model.md` require no model |
| 3 | Algorithm | `spec.md` | User confirms correctness and termination | Applicability criteria in `rules/docs/spec.md` When Required and When Not Required require no spec |
| 4 | Design | `design.md` | User confirms structure and responsibility allocation | Existing contracts and responsibilities remain unchanged |
| 5 | Research | `impl.md` | None; agent reports findings | No unresolved external API or implementation question |
| 6 | Plan | task doc `docs/todo/<module>.md` | User confirms task breakdown and order | Existing authorization and task order cover the work |
| 7 | Code | source code | None; agent follows the task doc in order | Never |
| 8 | Verify | passing quality gate | Task doc Quality Gate checklist passes; every domain term in the changed docs has a glossary entry | Never |

- Read the earlier owning documents needed by the affected stages; reuse unchanged decisions and verified evidence. A stage that introduces a domain term adds its glossary entry under `communication/terminology.md` Established Terms.
- State stage selection briefly in the task context. A skipped stage creates no document or approval step.
- Research follows `docs/impl.md` for external API verification and recording.

## Existing Codebase Changes

- Read the existing docs in the target directory first.
- Start at the earliest phase the change affects.
- Update documents in place. Never recreate them from scratch.
- A change rewrites the section that owns the fact. It never appends a paragraph or a note beside the text it changes.
- A concept or model change updates the downstream sentences it invalidates before implementing that change.

## Phase Transitions

- An affected stage completes before work that depends on it. Existing user authorization satisfies its approval step within that scope.
- When evidence invalidates an assumption or changes the approach comparison, return to the earliest affected stage and update the owning text before dependent implementation.

## Index

- Index creation and updates after a stage adds or renames a file: `rules/docs/index.md`.

- At task completion, `completion` controls creation of summary and README files. An existing-files-only setting applies to those completion artifacts.
