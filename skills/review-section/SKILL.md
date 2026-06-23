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

---

## Layering

`check-sentence` owns every sentence-level and adjacent-pair check; it sees one passage at a time and a reader who has read only up to the current sentence. This skill runs `check-sentence` across the section (Step 2), then adds only what spans more than two adjacent sentences or more than one passage: the cross-section first-read state (Step 3) and the section-wide checks named in `writing.md` (Steps 4–7). `writing.md` is the single authority for the rules; the steps name which of its sections apply at section scope. Never re-derive a sentence-level check here.

---

## Step 1 — Read and establish reading order

1. Read the target `.tex` file in full.
2. If a subsection is specified, identify its boundaries and focus there; still flag cross-section issues visible from the excerpt.
3. Read `main.tex` and record the `\input`/`\include` order. The target section's position in that order defines "prior sections" — every section input before it.
4. Read every prior section in document order. Build a knowledge ledger of what a reviewer holds on entering the target section: defined terms and notation, established claims, prior-work concepts and their attribution, and stated assumptions. Carry only what the prior text actually establishes, not background knowledge.
5. Read `.claude/rules/writing.md`, the authoritative writing rules. Steps 3–7 name the sections that apply at section scope.
6. Read the sentence-level module at `${CLAUDE_SKILL_DIR}/../check-sentence/SKILL.md`.

---

## Step 2 — Sentence Audit (run check-sentence)

Apply the `check-sentence` procedure to each paragraph of the scoped text. It is authoritative for:
- sentence-internal validity (quantifier accuracy, hidden universals, word-referent precision, technical-term accuracy, causal language, comparisons, article and number agreement, tense);
- adjacent-pair coherence (logical bridge, scope transfer, hidden premise, referent continuity, first-read position, stress position);
- reviewer-rejection risk (undefendable strong declarations, scope overreach, unqualified firsts, causal overclaim, proof-triggering terms).

Run `check-sentence` on every paragraph in reading order; do not sample. Tag each finding with its `check-sentence` category and fold it into the report below, and do not restate these checks. Category-to-report mapping: INVALID/UNSUPPORTED/COHERENCE/AMBIGUOUS → Logic and Argumentation; GRAMMAR → Prose and Register; VAGUE and technical-term accuracy → Terminology and Consistency; REVIEWER-RISK → its matching report row.

---

## Step 3 — First-Read Knowledge-State Audit (cross-section)

This step operationalizes the `writing.md` Governing Principle (every sentence verifiable from text already read) across section boundaries.

Advance the knowledge ledger from Step 1 sentence by sentence through the target section, so it always reflects what a reviewer has read up to the current line. Add a term to the ledger only when the text defines it, cites it, or grounds it in a concrete referent. Flag every paper-specific term, symbol, prior-work concept, claim treated as known, and assumption the text relies on that is not yet in the ledger; never flag standard field background a target reviewer holds. Sort each violation into one report category:

- **Forward dependency** — established only in a later section, with no explicit forward reference (`Section N`) at the point of use.
- **Unestablished assumption** — never established anywhere in prior text.
- **Intra-section forward use** — defined later in this same section.

---

## Step 4 — Section-Level Argument Arc

Apply the `writing.md` **Precision of Claims**, **Argument Continuity**, and **Definitions** checks to what spans more than two adjacent sentences: paragraph topic claims, paragraph-to-paragraph flow, section-to-section motivation, fulfilled promises, logical-level conflation, prior-work attribution, and observable-phenomenon-before-label.

---

## Step 5 — Terminology Consistency (section-wide)

Apply the `writing.md` **Terminology Consistency** checks across the whole section — the drift `check-sentence` cannot see from a single passage: naming, spelling, term invention, subject consistency, and the canonical form of multi-word technical terms (spacing, hyphenation, capitalization). Also flag a measurement or concept term used inconsistently across the section (`writing.md` **Word Choice Precision** Near-synonym precision).

---

## Step 6 — Prose Sweep (section-wide)

Scan the whole section for the `writing.md` **Word Choice Precision** vague qualifiers, **Word-Level Register** banned terms, **Metadiscourse** throat-clearing openers, the **Sentence Structure** rhythm rule (5+ consecutive sentences within ±5 words), and **Tense** drift across the section (consistent tense per narrative frame). Sentence-internal register and per-sentence tense are run by `check-sentence` (Step 2); here run only the section-wide scan.

---

## Step 7 — Structural Alignment Audit

Apply the `writing.md` **Structural Alignment** checks: figure and table citation order, caption-to-figure match, and topic-enumeration order.

---

## Step 8 — Report

Output findings in this format. Omit any category with zero issues.

```
## Section Review: <file> [<subsection>]

### Critical — First-Read Knowledge State
| # | Line | Category | Issue | Quote |
|---|------|----------|-------|-------|
| 1 | L42  | Forward dependency / Unestablished assumption / Intra-section forward use | <what the reader cannot resolve here> | "…" |

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
**Summary**: <N> first-read, <N> critical, <N> warnings, <N> notes.
**Verdict**: Pass / Needs revision / Major revision required.
```

Severity levels:
- **First-read (Critical)**: a reviewer cannot resolve the term, symbol, claim, or assumption from text read so far — must fix before submission.
- **Critical**: affects logical validity or claim accuracy — must fix before submission.
- **Warning**: weakens rigor or violates register — fix before submission.
- **Note**: minor style or structural issue — fix when convenient.

---

## Rules

- Record every finding with its line number and a verbatim quote (≤ 120 characters). No speculation.
- Do not suggest rewrites in this step. Report findings only.
- If the argument is valid but a term's academic definition is uncertain, flag it as a Warning and suggest `/define-term <term>`.
