---
name: update-docs
description: Audit docs against type-specific rules, plan fixes, and apply them after approval. Use when the user asks to update, fix, or improve documentation.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
argument-hint: "[optional path to a specific docs/ subdirectory]"
---
Audit documentation files against their type-specific rulesets, produce a fix plan, and apply fixes after user approval.

## Step 1 — Discover Files

1. `Glob("docs/**/*.md")` (or scoped to `$ARGUMENTS`), plus `Glob("**/*.md")` run with each existing records directory of `rules/workflow/records.md` (`docs/decisions/`, `docs/todo/`, `docs/audit/`) as its path.
2. Classify each file by name pattern (`rules/docs/documentation.md` Naming):

| Pattern | Type | Rule file |
|---------|------|-----------|
| `**/concept.md`, `**/concept-*.md` | Concept | `rules/docs/concept.md` |
| `**/model.md`, `**/model-*.md` | Domain model | `rules/docs/model.md` |
| `**/design.md`, `**/design-*.md` | Design | `rules/docs/design.md` |
| `**/spec.md`, `**/spec-*.md` | Algorithm spec | `rules/docs/spec.md` |
| `**/impl.md`, `**/impl-*.md` | Implementation | `rules/docs/impl.md` |
| `docs/todo/**` | Task | `rules/docs/todo.md` |
| `docs/decisions/**`, `docs/audit/**` | Local record | `rules/workflow/records.md` only |
| `**/index.md` | Index | `rules/docs/index.md` |
| `**/glossary.md`, `**/glossary-*.md` | Glossary | `rules/docs/glossary.md` |

Files matching no pattern: report as **unclassified** for user review.

## Step 2 — Audit Each File

Read every file. Load the rule file of its type and `rules/docs/documentation.md`, and audit every requirement in them, including each rule's own exceptions and omission conditions. Record each violation with `[file:line] description`.

## Step 3 — Cross-File Consistency

Check across files within the same docs subdirectory:

1. **Terminology**: the glossary exists at `glossary.path` (project rule file `glossary.md`) when the project has documentation. Every domain term used in a concept, model, design, or spec file (Step 1 patterns) has a glossary entry and is spelled as its heading. No retired name in use. Report an entry that fails `rules/docs/glossary.md` Selection; redundant entries under Selection; and an entry no document uses.
2. **Ownership**: each fact lives in its owning document under `rules/docs/documentation.md` Ownership; another document links it.
3. **Cross-references valid**: every `see [file.md]` link points to an existing file.
4. **index.md sync**: each `index.md` lists its directory's files under `rules/docs/index.md`; no orphan entries.
5. **impl.md sync**: no `impl.md` entry references a removed function, and `design.md` links an external API fact to its `impl.md` entry instead of restating it.
6. **Repositories**, across the main repository and its submodules under `rules/docs/documentation.md` Repositories and `rules/docs/glossary.md` Repositories: every cross-repository link resolves and uses the stated link form; no link or term reference points against the dependency direction; no concept has entries in two glossaries; every imported term exists at its owning entry.

## Step 4 — Plan

Output a structured fix plan.

```text
## Docs Update Plan: <scope>
### Missing Sections
- [file] missing: <section name> — action: <add/restructure>
### Content Violations
- [file:line] <rule type>: <description> — fix: <what to change>
### Cross-File Issues
- <description> — fix: <what to move/rename/update>
### Format Issues
- [file:line] <description> — fix: <what to change>
### Summary
- Files audited: N
- Missing sections: N
- Content violations: N
- Cross-file issues: N
- Format issues: N
- Total fixes planned: N
```

Wait for user approval before proceeding to Step 5.

## Step 5 — Apply Fixes

For each approved item in the plan:

1. Apply the fix. Preserve existing content — restructure, not rewrite.
2. Verify the fix resolves the specific violation.
3. Check cross-file consistency after each change.

One file at a time. If a fix requires changes in another file, apply them together as one logical unit.

## Step 6 — Report

```text
## Docs Update Results: <scope>
### Fixed
- [file:line] <what was fixed>
### Skipped (user declined or needs domain input)
- [file:line] <description> — reason: <why skipped>
### Remaining
- [file:line] <description> — requires: <user input/domain knowledge>
### Summary
- Files updated: N
- Violations fixed: N
- Remaining: N
```

## Rules

- Preserve content. Restructure and move — never delete domain knowledge.
- Missing sections that require domain knowledge: report as "needs user input", do not fabricate content.
- One logical change per file update. Atomic edits.
