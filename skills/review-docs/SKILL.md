---
name: review-docs
description: Audit docs/ files against their type-specific rules (idea, model, design, spec, impl, todo, index). Use when the user asks to review or verify documentation.
allowed-tools:
  - Read
  - Grep
  - Glob
argument-hint: "[optional path to a specific docs/ subdirectory]"
---

Audit every documentation file under `docs/` (or `$ARGUMENTS` if a subdirectory is specified) against its type-specific ruleset. Report violations.

## Step 1 — Discover Files

1. `Glob("docs/**/*.md")` (or scoped to `$ARGUMENTS`).
2. Classify each file by suffix/name:

| Pattern | Type | Ruleset |
|---------|------|---------|
| `**/idea.md` | Concept | concept rules |
| `**/*model.md` | Domain model | model rules |
| `**/*design.md`, `**/*design-*.md` | Design | design rules |
| `**/spec.md` | Algorithm spec | spec rules |
| `**/*impl.md` | Implementation | impl rules |
| `**/todo.md`, `**/*.todo.md` | Task | todo rules |
| `**/index.md` | Index | index rules |

Files matching no pattern: report as **unclassified** for user review.

## Step 2 — Audit Each File

Read every file. Check against the rules below for its type. Record each violation with `[file:line] description`.

---

### idea.md (Concept)

**Required sections** (in order):
1. Context: Problem Statement, System Role, Data Flow (Inputs/Outputs/Connections), Scope Boundaries (Owned/Not Owned)
2. Concepts: Conceptual Diagram, Core Concepts (each: Name, Definition, Scope, Relationships)
3. Contracts & Flow: Data Contracts, Internal Processing Flow
4. Scenarios: Typical, Boundary, Interaction (minimum one each)

**Content rules:**
- Concepts and terminology only. No implementation details, APIs, commands, or code.
- Concept definitions: name + one-sentence definition + scope + relationships.
- No formal semantics (state transitions, invariants, edge direction rules) — those go in `model.md`.
- Technical specifications link to `design.md`. Domain semantics link to `model.md`.

**Format rules:**
- Paragraphs: 2-4 sentences.
- One diagram per interaction boundary.
- Consistent terminology across sections.

---

### *model.md (Domain Model)

**Required sections** (in order, include only if content exists):
1. Entities — name, semantic role, existence conditions per entity kind
2. Relations — direction, label requirements, cardinality, meaning (table format)
3. State Model — states, transitions, guards, terminal conditions
4. Invariants — structural constraints, one per line, falsifiable
5. Cross-Structure Contracts — semantic mappings between domain structures

**Content rules:**
- Define what each entity/relation **means**, not how implemented.
- State transitions: source state, trigger, guard, target state.
- Invariants: precise and falsifiable. "Every X has at least one Y" not "X should have Y."
- No language-specific types, class names, or method signatures. Domain vocabulary only.
- Reference `idea.md` for rationale. Reference `design.md` for implementation mapping.

---

### *design.md (Design)

**Required sections** (in order):
1. Design Overview — types/classes, relationships (one-way only), abstract types, exceptions, dependency roles
2. Class / Type Specifications — per type: Responsibility, state/fields, methods (Behavior/Input/Output/errors)
3. Function Specifications — per function: name(signature), Responsibility, Behavior, Input, Output, errors
4. Exception / Error Types — each type and when raised

**Overview format check:**
- Classes listed
- Relationships one-way (no A↔B)
- Abstract types with implementors
- Dependency roles: data holders, orchestrators, helpers

**Content rules:**
- No domain entity semantics, state transition rules, or structural invariants — those go in `model.md`.
- No algorithm steps, pseudocode, or complexity analysis — those go in `spec.md`.
- Dependencies one-way: A uses B → B must not use A.
- Data holders: only primitives, enums, or other data holders.

---

### spec.md (Algorithm Specification)

**Required sections** per algorithm:
1. Problem — input, output, correctness condition (one paragraph)
2. Steps — numbered pseudocode, language-independent
3. Invariants — loop invariants, maintained properties, one per line
4. Termination — why the algorithm halts, variant function or bound
5. Complexity — time and space, Big-O with variables defined

**Content rules:**
- Pseudocode uses domain vocabulary from `model.md`, not implementation names.
- No language-specific syntax.
- Edge cases and degenerate inputs documented after main steps.

---

### *impl.md (Implementation)

**Required sections** (in order, include only if content exists):
1. APIs — `**[Lib]** snippet` — one-line when/gotcha
2. Libraries — name, version if fixed, purpose (one line each)
3. Developer instructions — workflow, command, pattern, constraint (one fact per line)
4. Design-specific — invariants, non-obvious behavior, integration notes

**Content rules:**
- One to two lines per API entry: canonical import + when/gotcha.
- No design duplication. No long examples or tutorials.
- Developer instructions: concrete only. Remove when workflow changes.

---

### todo.md (Task Management)

**Task format:**
```
[state] <action verb> <object> <detail>
  Depends on: <task ids or paths>
  Acceptance: <criteria>
  - [ ] <subtask>
  - [ ] Quality gate
```

**States:** `[ ]` todo, `[x]` done, `[~]` in progress, `[-]` skipped.

**Rules:**
- Action verb + object + detail. No vague titles.
- Acceptance criteria when verifiable.
- Explicit dependencies.
- No new design in TODO files — reference design docs.
- Quality gate present on every task.

---

### index.md (Index/Navigation)

**Structure:**
- H1: module name + role (one line)
- One table: File | Content columns
- File column: exact filename, no path prefix
- Content column: under 80 characters, states what the file covers

**Rules:**
- Every file in the directory appears in `index.md`.
- Every entry in `index.md` points to an existing file.
- Rows ordered: idea → model → design → impl → todo.
- No domain content. Descriptions say what topic, not definitions.
- No hierarchy or nesting. Flat table.
- No file exceeds 200 lines. Split and update `index.md` when exceeded.

---

## Step 3 — Cross-File Consistency

Check across files within the same docs subdirectory:

1. **Terminology**: concepts defined in `idea.md` match names used in `model.md`, `design.md`, `spec.md`.
2. **No content in wrong file**: implementation details not in `idea.md`/`model.md`; domain semantics not in `design.md`; algorithms not in `design.md`.
3. **Cross-references valid**: every `see [file.md]` link points to an existing file.
4. **index.md sync**: if `index.md` exists, all sibling files listed; no orphan entries.
5. **impl.md sync**: API entries match what `design.md` specifies; no stale references to removed functions.

## Step 4 — Report

Output a structured report:

```
## Docs Review: <scope>

### Violations
- [file:line] <rule type>: <description>

### Warnings
- [file:line] <description>

### Cross-File Issues
- <description>

### Summary
- Files audited: N
- Violations: N (blocking)
- Warnings: N
- Clean files: list
```

Violations are rule breaches. Warnings are style issues or borderline cases.

Do not auto-fix. List violations for user review.
