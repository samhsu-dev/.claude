---
name: update-prompts
description: Audit LLM-agent prompts against prompting.md, plan fixes, apply after approval, and gate every change on an eval rerun. Use when the user asks to update, review, or fix a prompt.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
argument-hint: "[path to a prompt carrier file or directory]"
---

Audit prompt carriers against `~/.claude/rules/prompt/prompting.md`, produce a fix plan, apply fixes after approval, and measure the result.

Every check below carries an ID. Step 5 reports a verdict for every ID. A check reported `n/a` states why in the same row. An unreported ID means the audit did not run.

## Step 1 — Render

1. Locate the carriers in scope from `$ARGUMENTS`. No argument: `Glob("**/prompts/**/*.{ts,py,md,prompty}")` plus changed files from `git diff --name-only`.
2. Read each carrier. List every exported prompt constant.
3. Render each constant to `<scratchpad>/<constant>.txt`, with template substitutions resolved. Rendering imports the module and writes the string; never hand-copy the text.
4. Record which surface each rendered string is bound to: system prompt, first user turn, tool description, subagent definition, or on-demand file.

Skipping the render and scanning the carrier source instead is a failed audit. Composed constants and interpolated values are invisible in source.

## Step 2 — Mechanical Scan

Run the scanner over the rendered files:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/scan.mjs <rendered.txt>... [--corpus <eval-corpus-path>] [--budget 20]
```

Pass `--corpus` whenever an evaluation set, labelled dataset, or graded corpus exists for this prompt. Its absence is reported in Step 5, not silently ignored.

Read the JSON and map it onto these checks:

| ID | Check | Fails when |
|----|-------|-----------|
| M1 | Rule duplication | `repeatedGrams` holds a content phrase outside a rule-to-example pair |
| M2 | Attention budget | `overBudget` is true (`directiveCount` past `directiveBudget`) |
| M3 | Emphasis inflation | `emphasisWords` is non-empty |
| M4 | Corpus leakage | any `corpusLeakage.tokens[].corpusOccurrences` exceeds 0 |
| M5 | Section balance | one non-example section holds more than a third of `size.words` |

M4 is the highest-severity mechanical check. A concrete token shared with the graded corpus binds that token to the example's verdict and contaminates every measurement taken afterward.

## Step 3 — Structural Audit

Read `~/.claude/rules/prompt/prompting.md`. Check each carrier against it and record a verdict per ID.

| ID | Check | Source rule |
|----|-------|-------------|
| S1 | Sections present and in taxonomy order | Section Taxonomy and Order |
| S2 | Constraints grouped into blocks, not a flat imperative list | Constraints |
| S3 | Highest-priority rule first within each block | Constraints |
| S4 | Output contract stated in-prompt, fields matching the parsed schema in both directions | Output Contract |
| S5 | 3 to 5 examples in `<example>` tags, following the instructions | Examples |
| S6 | One abstain or negative example present when the task has an abstain path | Examples |
| S7 | One concept, one term across every stage sharing this preamble | Terminology |
| S8 | Coined terms defined at first use | Terminology |
| S9 | Common programming terms left undefined | Terminology |
| S10 | Shared rules stated once in the preamble, not copied per stage | Terminology |
| S11 | Section 10 restates exactly one rule | Information Placement |
| S12 | One kind of information in one section, with its scope, exceptions, and illustrations | Information Placement |
| S13 | No section exists solely to hold the exception to a rule stated elsewhere | Information Placement |
| S14 | Nothing stated that the model already derives | Information Placement |
| S15 | No induced reasoning step on a native-thinking model | Reasoning |
| S16 | Tool output framed as untrusted data | AI-Agent Structural Patterns |

For S12, list every section each rule appears in. A rule in two sections is one rule in the wrong place, not two rules.

For S14, name the sentence and state what the model derives without it. A sentence the model needs but could not derive stays.

## Step 4 — Load-Placement Audit

Cost of resident text is per turn. Cost of on-demand text is one tool round trip plus the risk the agent never fetches it. Placement follows use frequency, never length.

| ID | Check | Fails when |
|----|-------|-----------|
| L1 | Every rule used on every run is resident | a per-run rule sits behind a fetch |
| L2 | Content used on a minority of runs is on-demand | rarely-used text is resident |
| L3 | Bulk reference material is a file the agent reads on demand | a rubric or corpus is inlined |
| L4 | Per-run data arrives in the user turn, not the system prompt | data is interpolated into the system prompt |
| L5 | No instruction-bearing file loads from a directory the prompt treats as untrusted | a settings or context file loads from the target working directory |

L5 is a prompt-injection check. Name the loading mechanism, the directory it reads from, and who controls that directory's contents.

Report measured use frequency where the eval provides it. An unmeasured frequency is reported as unmeasured, never estimated.

## Step 5 — Plan

Output the full verdict table first. Every ID from Steps 2, 3, and 4 appears exactly once.

```
## Prompt Audit: <scope>

| ID | Verdict | Evidence |
|----|---------|----------|
| M1 | pass / fail / n/a | <line numbers, counts, or the reason for n/a> |
| ... | | |

### Fixes
- [carrier:line] <ID> <violation> — fix: <what to change>

### Summary
- Carriers audited: N
- Checks run: N of N
- Failures: N
- Fixes planned: N
```

Wait for user approval before Step 6.

## Step 6 — Apply

1. One concept per edit. A concept is one rule moved, one duplication removed, or one section restructured.
2. Rewrite in place. Never append a clause to patch an observed failure; fold it into the rule that owns it.
3. Re-render and re-run Step 2 after each edit.
4. Run the project's formatter, type checker, and test suite on the carrier.

## Step 7 — Measure

A prompt edit changes model behavior and is not verified by tests.

1. Run the project's accuracy evaluation three times on the edited prompt.
2. Copy the per-row output file after each run, before the next run overwrites it. Verify the copied file holds the run's rows.
3. Compare against the recorded baseline on the deterministic subset: rows whose verdict is stable across the baseline runs. Aggregate accuracy at small n carries more noise than most effects.
4. State the decision criteria before reading the results.

| Target metric | Other metrics | Decision |
|---------------|---------------|----------|
| Improved | No regression | KEEP |
| Improved | Regression on a stable-correct row | REVERT |
| No change | No regression | REVERT, the edit is unproven |
| Degraded | Any | REVERT |

Report the decision with numbers. A change measured on one run is unmeasured.

## Step 8 — Record

Append to the project's prompt-change log: the ID fixed, the edit, the three-run numbers, and the decision. A REVERT is recorded with its numbers so the same edit is not retried.

## Rules

- Plan before fix. Never edit before the user approves the plan.
- Every check ID appears in the Step 5 table. Omission is a failed audit, not a passed one.
- Scripts decide mechanical checks. Never substitute a reading of the text for M1 through M5.
- One edit, one measurement. Never batch edits and measure once; attribution is unrecoverable.
- Corpus leakage found after a measurement invalidates that measurement. Re-baseline before comparing.
