---
name: review-section
description: Review a LaTeX section or subsection for logic, argumentation rigor, and writing standards. Use when asked to review, audit, or check a section of the paper.
allowed-tools:
  - Read
  - Glob
argument-hint: "<section-file-path> [subsection-name]"
---

Review the academic writing quality of `$ARGUMENTS`.

Parse `$ARGUMENTS` as: first token is the `.tex` file path; optional second token is a subsection name or keyword to scope the review within that file.

Read the target file (and the full rules at `${CLAUDE_SKILL_DIR}/rules.md`) before beginning.

---

## Layering

`check-sentence` is the sentence-level module. It owns every check at the granularity of one sentence or one adjacent-sentence pair: internal validity, sentence-to-sentence coherence, first-read position, and reviewer-rejection risk. This skill composes over it: it runs `check-sentence` across the section, then adds only the checks that span more than two adjacent sentences — paragraph arc, whole-section terminology, whole-section prose sweeps, and structural alignment. Never re-derive a sentence-level check here.

---

## Step 1 — Read

1. Read the target `.tex` file in full.
2. If a subsection is specified, identify its boundaries and focus there; still flag cross-section issues visible from the excerpt.
3. Read `${CLAUDE_SKILL_DIR}/rules.md` for the section-level check list.
4. Read the sentence-level module at `${CLAUDE_SKILL_DIR}/../check-sentence/SKILL.md`.

---

## Step 2 — Sentence Audit (run check-sentence)

Apply the `check-sentence` procedure to each paragraph of the scoped text. It is authoritative for:
- sentence-internal validity (quantifier accuracy, hidden universals, word-referent precision, causal language, comparisons);
- adjacent-pair coherence (logical bridge, scope transfer, hidden premise, referent continuity, first-read position, stress position);
- reviewer-rejection risk (undefendable strong declarations, scope overreach, unqualified firsts, causal overclaim, proof-triggering terms).

Record each finding with its line number, verbatim quote (≤ 120 characters), and `check-sentence` category. Fold them into the report below. Do not restate these checks.

---

## Step 3 — Section-Level Argument Arc

Check what spans more than two adjacent sentences. Record every violation with its line number and a verbatim quote (≤ 120 characters).

- Every claim is backed by a citation, an experiment result, or a logical inference from a stated premise.
- Each paragraph has exactly one main claim, stated in its topic sentence.
- Each paragraph's argument follows from the preceding paragraph; no unexplained jumps.
- Each section ending motivates the opening of the following section.
- Promises made in introductory text (enumerated topics, "we show that…") are fulfilled in the stated order.
- Terms used at different logical levels are not equated (bug ≠ vulnerability; correlation ≠ causation).
- Concepts defined by prior work are attributed to prior work, not presented as domain ground truth.
- Observable phenomenon described before its formal label is introduced anywhere in the section.

---

## Step 4 — Terminology Consistency (section-wide)

Check what only a whole-section view reveals; `check-sentence` sees one passage at a time and cannot catch drift across the section.

- One name per concept throughout the section. Flag any synonym cycling.
- One spelling and capitalization per term. Flag hyphenation or capitalization variants.
- No self-invented terms without an inline definition and a citation or a concrete referent.
- A pronoun ("this", "these", "such") referring to a class introduced several sentences earlier without restatement.

---

## Step 5 — Prose Sweep (section-wide)

### 5a. Banned Words
Flag any appearance of: delve, tapestry, landscape, pivotal, crucial, foster, showcase, testament, navigate, leverage, realm, embark, underscore, multifaceted, nuanced, comprehensive, robust, intricate, cornerstone, paradigm, synergy, holistic, streamline, cutting-edge, groundbreaking.

### 5b. Throat-Clearing
Flag sentence openers: "In the realm of", "It is important to note that", "It is worth mentioning that", "It goes without saying that", "In order to", "It should be noted that", "With that being said", "When it comes to", "This section will discuss", "In this section we".

### 5c. Sentence Rhythm
- Flag five or more consecutive sentences of similar length (within a ±5 word range).

---

## Step 6 — Structural Alignment Audit

- Every figure and table cited in the text before or at its first appearance.
- Caption text matches figure content; spatial descriptions match actual layout.
- A section introduction listing topics addresses them in the stated order.

---

## Step 7 — Report

Output findings in this format. Omit any category with zero issues.

```
## Section Review: <file> [<subsection>]

### Critical — Logic and Argumentation
| # | Line | Issue | Quote |
|---|------|-------|-------|
| 1 | L42  | Claim without support | "…" |

### Warnings — Terminology and Consistency
| # | Line | Issue | Quote |
|---|------|-------|-------|

### Warnings — Prose and Register
| # | Line | Issue | Quote |
|---|------|-------|-------|

### Notes — Structural Alignment
| # | Line | Issue | Quote |
|---|------|-------|-------|

---
**Summary**: <N> critical, <N> warnings, <N> notes.
**Verdict**: Pass / Needs revision / Major revision required.
```

Severity levels:
- **Critical**: affects logical validity or claim accuracy — must fix before submission.
- **Warning**: weakens rigor or violates register — fix before submission.
- **Note**: minor style or structural issue — fix when convenient.

---

## Rules

- Report only verifiable violations with line numbers and quotes. No speculation.
- Do not suggest rewrites in this step. Report findings only.
- If the argument is valid but a term's academic definition is uncertain, flag it as a Warning and suggest `/define-term <term>`.
