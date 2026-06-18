# Review-Section: Complete Rule Reference

Condensed from `.claude/rules/writing.md` and `.claude/rules/introduction.md`.
This file is read by the review-section skill at runtime.

---

## Logic and Argumentation

- Every claim backed by citation, experiment, or stated inference.
- No claim that fails on a counterexample.
- Degree claims when prior work exists; never absolutes unless provable.
- "requires X" only when logically necessary, not merely conventional.
- One main claim per paragraph, stated in the topic sentence.
- Each paragraph's argument follows from the preceding paragraph.
- Section ending motivates the following section's opening.
- Promises in introductory text fulfilled in stated order; no unfulfilled enumeration.
- Concepts at different logical levels never equated (bug ≠ vulnerability; correlation ≠ causation).
- Prior work's abstractions attributed to prior work, not presented as domain ground truth.
- Observable phenomenon described before its formal label.
- Every term in running text before the sentence that depends on it.

---

## Terminology and Consistency

- One name per concept. No synonym cycling.
- One spelling and capitalization per term throughout.
- No self-invented term without inline definition + citation or concrete referent.
- "sound", "complete", "correct", "valid", "genuine", "real" only with their formal meaning.
- Pronouns ("this", "these", "such") have an unambiguous antecedent in the immediately preceding sentence.

---

## Prose and Register

**Banned vague qualifiers**: general, generic, novel, efficient, robust, proper, appropriate, effective (as sole characterization).

**Banned AI-register terms**: delve, tapestry, landscape, pivotal, crucial, foster, showcase, testament, navigate, leverage, realm, embark, underscore, multifaceted, nuanced, comprehensive, intricate, cornerstone, paradigm, synergy, holistic, streamline, cutting-edge, groundbreaking.

**Banned throat-clearing openers**: "In the realm of", "It is important to note that", "It is worth mentioning that", "It goes without saying that", "In order to", "It should be noted that", "With that being said", "When it comes to", "This section will discuss", "In this section we".

**Sentence rules**:
- One sentence, one meaning.
- No absolute quantifiers unless provable: every, all, never, always.
- No anthropomorphism: programs do not know, think, believe, or understand.
- No paired em-dashes to inject a definition or carry main content.
- Vary sentence length; flag 5+ consecutive sentences within ±5 words of each other.

**Register**:
- No "yet" as conjunction → "but".
- No "utilize", "leverage", "employ" meaning "use" → "use".
- No "in order to" → "to".
- No connective ("thus", "therefore", "moreover") without a genuine logical relation.
- No two consecutive sentences opened by a connective.

---

## Structural Alignment

- Every figure and table cited in text before or at first appearance.
- Caption matches figure; spatial descriptions match actual layout.
- Section introduction enumerating topics addresses them in stated order.
