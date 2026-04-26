---
paths:
  - "**/*impl.md"
---

# Implementation Document Standards

## 1. Scope

- One `impl.md` per design. Same directory as the paired `design.md`. Create if missing.
- Contains APIs, libraries, and developer notes for the design. No types or responsibilities (those stay in design).
- On task start: read the paired `impl.md`.
- Before writing code that uses an external library: check `impl.md` for existing findings.
- Format: headings + lists + inline code. One line per fact. No prose.

## 2. Structure

Sections in order; include only if they have content:

| Section | Content |
|--------|--------|
| **APIs** | `**[Lib]**` `snippet` — one-line when/gotcha. |
| **Libraries** | Name; version if fixed; purpose. One line each. |
| **Developer instructions** | Workflow, command, pattern, constraint. One fact per line. |
| **Design-specific** | Invariants, non-obvious behaviour, integration. Subheadings by design filename if multiple. |

## 3. When to write

- API needed → **APIs**. Library needed → **Libraries**. Developer instruction → **Developer instructions**. User correction → update immediately.
- All investigation findings (API behavior, gotchas, version constraints) go into `impl.md` immediately. Not in conversation only.
- No design duplication. No long examples or tutorials.

## 4. Rules

- One to two lines per API: canonical import + when/gotcha. Remove when design no longer uses it.
- Developer instructions: concrete only. Update/remove when workflow changes.
- On user correction: update, deduplicate, remove obsolete. Design stays in design file.
