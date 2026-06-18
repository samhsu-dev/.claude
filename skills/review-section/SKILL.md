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

## Step 1 — Read

1. Read the target `.tex` file in full.
2. If a subsection is specified, identify its boundaries and focus there; still flag cross-section issues visible from the excerpt.
3. Read `${CLAUDE_SKILL_DIR}/rules.md` for the complete check list.

---

## Step 2 — Logic and Argumentation Audit

Check each of the following. Record every violation with its line number and a verbatim quote (≤ 120 characters).

### 2a. Claim Support
- Every claim is backed by a citation, an experiment result, or a logical inference from a stated premise.
- No claim that fails on a counterexample.
- Degree claims used when prior work exists; no absolutes ("never", "always", "every") unless provable.
- "requires X" used only when the necessity is logically necessary, not merely conventional.

### 2b. Argument Structure
- Each paragraph has exactly one main claim, stated in its topic sentence.
- The argument in each paragraph follows from the preceding paragraph; no unexplained jumps.
- Within each paragraph, each sentence follows from the one before it. Flag any adjacent sentence pair where the logical connection is missing or supplied by an implicit premise not stated in the passage.
- A transition word ("therefore", "thus", "however") must reflect a real logical relation. Flag false bridges where the connective does not match the actual relation.
- Each section ending motivates the opening of the following section.
- Promises made in introductory text (enumerated topics, "we show that…") are fulfilled in the stated order.

### 2c. Logical Equivalences
- Terms used at different logical levels are not equated (e.g., bug ≠ vulnerability; correlation ≠ causation).
- Concepts defined by prior work are attributed to prior work, not presented as domain ground truth.

### 2d. Definition Ordering
- Observable phenomenon described before its formal label is introduced.
- Every term appears in running text before the sentence that depends on it as a given.

---

## Step 3 — Terminology and Consistency Audit

### 3a. Term Discipline
- One name per concept throughout the section. Flag any synonym cycling.
- One spelling and capitalization per term. Flag hyphenation or capitalization variants.
- No self-invented terms without an inline definition and a citation or a concrete referent.
- Banned overloaded terms used only with their precise formal meaning: "sound", "complete", "correct", "valid", "genuine", "real".

### 3b. Pronoun and Reference Precision
- "this", "these", "such", "the above" have an unambiguous antecedent in the immediately preceding sentence.
- No pronoun refers to a class of objects introduced several sentences earlier without restatement.

---

## Step 4 — Prose and Register Audit

### 4a. Banned Words
Flag any appearance of: delve, tapestry, landscape, pivotal, crucial, foster, showcase, testament, navigate, leverage, realm, embark, underscore, multifaceted, nuanced, comprehensive, robust, intricate, cornerstone, paradigm, synergy, holistic, streamline, cutting-edge, groundbreaking.

### 4b. Throat-Clearing
Flag sentence openers: "In the realm of", "It is important to note that", "It is worth mentioning that", "It goes without saying that", "In order to", "It should be noted that", "With that being said", "When it comes to", "This section will discuss", "In this section we".

### 4c. Sentence Structure
- Each sentence has one meaning. Definitions, causal claims, and examples are in separate sentences.
- No absolute quantifiers unless proven: "every", "all", "never", "always".
- No anthropomorphism: programs do not "know", "think", "believe", or "understand".
- No paired em-dashes used to inject a definition or carry the sentence's main content.

### 4d. Sentence Rhythm
- Flag five or more consecutive sentences of similar length (within a ±5 word range).

---

## Step 5 — Structural Alignment Audit

- Every figure and table cited in the text before or at its first appearance.
- Caption text matches figure content; spatial descriptions match actual layout.
- A section introduction listing topics addresses them in the stated order.

---

## Step 6 — Report

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
