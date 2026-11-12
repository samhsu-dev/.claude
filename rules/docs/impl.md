---
paths:
  - "**/impl.md"
  - "**/impl-*.md"
---

# Implementation Document Standards

## 1. Scope

- One `impl.md` per design whose work needs implementation research or retained external API findings, beside the paired `design.md`.
- Content boundaries and links follow `rules/docs/documentation.md` Ownership.
- Read the paired `impl.md` when it exists and contains findings relevant to the task.
- Format: headings + lists + inline code. One line per fact. No prose.

## 2. Structure

Sections in order; include only if they have content:

| Section | Content |
|--------|--------|
| **APIs** | `**[Lib]**` `snippet` — one-line when/gotcha. |
| **Libraries** | Name; version if fixed; purpose. One line each. |
| **Developer instructions** | Workflow, command, pattern, constraint. One fact per line. |
| **Design-specific** | Links to model invariants; non-obvious behaviour, integration. Subheadings by design filename if multiple. |

## 3. When to write

- API needed → **APIs**. Library needed → **Libraries**. Developer instruction → **Developer instructions**.
- Before first use of an API of a declared dependency (version catalog entry), verify it through documentation, DeepWiki, Context7 or a minimal test. Record API behavior, gotchas and version constraints in `impl.md` immediately.
- No long examples or tutorials.

## 4. Rules

- One to two lines per API: canonical import + when/gotcha. Remove when design no longer uses it.
- Developer instructions: concrete only. Update/remove when workflow changes.
- On user correction: update immediately, deduplicate and remove obsolete findings.
