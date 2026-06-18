---
name: check-sentence
description: Check sentences for logical validity and reviewer-rejection risk — premise-conclusion soundness, sentence-to-sentence coherence, causal chain integrity, unsupported strong claims, and patterns that invite reviewer challenge. Use when a sentence or passage feels logically off, or before submitting a section.
allowed-tools:
  - Read
argument-hint: "<quoted sentence, L42-L48, or paragraph> [file.tex]"
---

Check the logical validity and reviewer-rejection risk of `$ARGUMENTS`.

Parse `$ARGUMENTS` as: a quoted sentence, a line range (e.g. `L42-L48`), or a paragraph marker, and an optional file path. If a file and line range are given, read those lines first.

---

## Step 1 — Internal sentence validity

Check each sentence in isolation.

**Quantifier accuracy**
- "every", "all", "always", "never" hold without exception? If not, scope them: "in all tested cases", "across our 100-repo corpus."
- "must", "requires", "is necessary" assert logical necessity. Flag unless the necessity is proven in this paper, not just observed.

**Causal language**
- "because", "therefore", "leads to", "causes", "results in" assert a causal link. Flag if the paper establishes only correlation. Replace with "we observe that X coincides with Y" or "X is associated with Y."

**Universal negatives**
- "X does not Y" fails on one counterexample. Scope it or qualify it.

**Comparisons**
- "X outperforms Y", "X is better than Y" require a named metric and a named scope. Unqualified comparisons are undefendable.

**Existence vs. universal**
- "there exists an application where…" and "all applications…" are not interchangeable. Flag conflation.

---

## Step 2 — Sentence-to-sentence coherence

Check every pair of adjacent sentences in the passage.

**Logical bridge**
- Does sentence B follow from sentence A, or is there an implicit leap? Name what is missing.
- A transition word ("therefore", "thus", "however") that does not reflect a real logical relation is a false bridge. Flag it.

**Scope transfer**
- If A makes a claim about a subset and B extends it to a superset, flag the generalization. State the missing warrant.

**Hidden premise**
- If A→B requires an unstated premise C, name C explicitly. Readers should not supply premises the paper omits.

**Referent continuity**
- Does the subject of sentence B match the topic introduced in sentence A? An abrupt subject change without a bridge breaks coherence.

**Stress position**
- The new information at the end of sentence A should be the topic of sentence B. If it is not, the chain loses momentum (Gopen & Swan).

---

## Step 3 — Reviewer rejection risk

Think as a skeptical reviewer. Flag patterns that invite challenge, rejection, or a negative impression.

**Undefendable strong declarations**

| Pattern | Reviewer reaction | Fix |
|---------|-------------------|-----|
| "X must be Y" | "Prove the necessity." | "X is Y in our setting" or "X is typically Y" |
| "the only way to" | "Here is another way." | "one natural way to" or "the approach we take" |
| "X always Y" | "Give a counterexample." | "X consistently Y across our corpus" |
| "requires X" (unproven) | "Prove X is necessary, not just sufficient." | "X is the natural means to" |
| "trivially", "obviously", "clearly" | "Not obvious to me." | Delete; state the fact directly |
| "simply" (before a non-trivial step) | Condescending; reader may not find it simple | Delete |

**Scope overreach**
- Conclusions drawn from N experiments stated as universal truths. Scope every empirical claim: "across our 100-repo corpus", "in our evaluation", "for the PHP e-commerce applications we tested."

**Unqualified firsts**
- "the first approach to X" invites the reviewer to recall prior work. Either cite a survey confirming the claim, or qualify: "the first approach to X that also Y."

**Dismissive prior work**
- "naive approach", "simplistic", "merely" applied to prior work creates a negative impression without adding information. Replace with a concrete limitation statement.

**Causal overclaim**
- "X causes Y" without a causal study. Reviewers with methods training will flag this immediately. Use "X is associated with Y" or "our results are consistent with X contributing to Y."

**Proof-triggering terms used informally**
- "sound", "complete", "correct", "optimal", "provably" without a proof. Each invites "prove it." Use only with a formal argument, or replace with the specific property you mean.

**Unsubstantiated motivation**
- "X is important because…" where the "because" clause is an assertion, not evidence. Either cite data or remove the motivation claim.

---

## Output format

For each issue found:

```
[CATEGORY] Line N — <issue type>
  Sentence: "…" (≤120 chars)
  Problem:  <one sentence stating the flaw or risk>
  Fix:      <one sentence stating the minimal change>
```

Categories and severity:
- **INVALID** — logically false or self-contradicting. Must fix before submission.
- **UNSUPPORTED** — claim may be true but is not established in the paper. Add evidence or qualify.
- **REVIEWER-RISK** — logically defensible but likely to trigger reviewer challenge or negative impression. Fix before submission.
- **COHERENCE** — adjacent sentences do not flow; logical bridge missing. Fix before submission.
- **AMBIGUOUS** — two valid readings exist. Disambiguate.

If no issues are found: `No issues found in the provided passage.`

---

## Rules

- Report only verifiable flaws or specific reviewer-risk patterns, not style preferences.
- Do not rewrite sentences. State the flaw and the minimal fix direction.
- Do not flag correctly hedged claims ("we believe", "this suggests", "in our evaluation") as risks — hedging is correct epistemic practice.
- Do not flag claims that are defended elsewhere in the paper unless the passage presents them as self-evident without a forward reference.
- When flagging reviewer risk, name the specific reviewer objection, not just "this is risky."
