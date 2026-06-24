---
paths:
  - "**/*.tex"
---

# Academic Prose Precision

Community standards: Strunk & White (*Elements of Style*); Gopen & Swan (*Science of Scientific Writing*, Am. Scientist 1990); Knuth et al. (*Mathematical Writing*, Stanford 1989); Peyton Jones (*How to Write a Great Research Paper*, MSR 2014); Levin & Redell (*How to Write a Good Systems Paper*, SIGOPS 1983); Shaw (*Writing Good SE Research Papers*, ICSE 2003); Shewchuk (*Three Sins*, CMU 1997); McDaniel (*How to Write a Security Paper*, Penn State); Dijkstra (EWD).

## Governing Principle

Every sentence is read by a reviewer seeing the paper for the first time. Each term, claim, and transition is verifiable from the text already read, never from knowledge of a later section. Every rule below serves this test: a term maps to a concrete, verifiable referent; a claim survives one counterexample; a transition supplies every step the reader needs.

The target reader is a computer-science expert with no prior knowledge of this paper. This baseline calibrates term choice in both directions: assume field-standard CS terms (data flow, static analysis, precision, recall, NP-hardness) are known and do not explain them; define every paper-specific term, system name, and non-standard use of a common word at first use. Over-explaining a standard term wastes the expert's attention; leaving a paper-specific term ungrounded breaks the first-read test.

---

## Term Grounding

- Every abstract noun states its exact referent at first use (Knuth; IEEE/ACM).
- No self-invented terms. Use an established term with a citation, or define inline with a concrete referent (Dijkstra; Knuth).
- One concept, one name. Never rename a concept mid-paper (Knuth).
- Use the concrete mechanism, not the abstract label. "A fixed set of calls such as `read()`, `write()`" not "a general detection criterion".

## Word Choice Precision

- No subjective qualifier as the sole characterization: "general", "generic", "novel", "efficient", "robust", "proper", "appropriate", "effective". Replace with a measurement or a concrete property.
- No modifier that adds no information: "very", "quite", "clearly", "direct".
- No contentless modifier: a modifier that applies to every member of the class it modifies is contentless. Test: remove it; if the claim is no less specific, delete it (e.g., "custom" before "implementation" — all implementations are developed by someone).
- No "technical specification", "technical error", "security property", "correctness standard" unless defined inline.
- **Overloaded terms** — use only with their formal meaning; each invites "prove it" if used informally: "sound" (no false negatives), "complete" (no false positives), "correct" (formal proof), "genuine" / "real" (no verifiable criterion). Replace with the concrete property you mean.
- **Near-synonym precision** — measurement and theory terms are distinct and non-interchangeable: "accuracy", "precision", "recall", "F1", "correctness", "soundness", "completeness". Name the one the paper actually computes or proves; never substitute one for another.
- Use the exact established term for a concept, not an approximate near-synonym. Confirm an unfamiliar or ambiguous term's field-standard meaning before committing it (`/define-term`).
- Express quantitative or comparative relations with noun phrases and a relational verb: "the measured latency was lower than the baseline", not "the latency fell far short of the baseline".

## Word-Level Register

Neutral, direct words. Replacements:

| Banned | Use |
|--------|-----|
| "yet" as a conjunction | "but" |
| "whilst", "amongst", "amidst" | "while", "among", "amid" |
| "hence" | "therefore", "thus" |
| "in order to" | "to" |
| "utilize", "leverage", "employ" (= use) | "use" |
| "a number of", "a variety of" | a number, or "several" |
| "it should be noted that" | delete; state the fact |
| "delve", "showcase", "underscore", "pivotal", "crucial", "seamless" | concrete verb or measured property |
| "translate to" (causal) | "result in", "lead to", "cause" |
| "by hand" | "manually" |


- Connectives ("thus", "therefore", "moreover") mark genuine logical relations only. No filler connective. No two consecutive sentences opened by a connective.
- No contractions in body text.
- No first-person "I". Use "we" for authorial action.
- Latin abbreviations: "e.g.", "i.e.", "cf." inside parentheses only; spell out in running text.

## Sentence Structure

- Main character as grammatical subject; key action as a verb, not a nominalization (Gopen & Swan).
- No figurative or implied constructions ("emerges", "reveals", "suggests"). State the subject and its action directly.
- Old/familiar information first, new information at sentence end (stress position) (Gopen & Swan).
- The concept at the stress position (sentence end) of sentence N becomes the topic position (sentence start) of sentence N+1. A sentence whose subject has no referent in the preceding sentence's stress position requires an explicit logical bridge ("Specifically,", "Three routes illustrate this.").
- Omit needless words (Strunk & White).
- State each claim once.
- One sentence, one meaning. Never merge a definition, a causal claim, and an example into one sentence.
- Vary sentence length within each paragraph. Five or more consecutive sentences of similar length signal monotony; insert a short sentence (under ten words) or combine two.
- A term introduced only as a modifier or object of a prepositional phrase in sentence A cannot serve as the definite referent ("this X", "that X") in sentence B. If sentence B needs to take that concept as its subject, restructure sentence A so the concept stands as the main subject or appears at the stress position, or replace the pronoun chain with a self-sufficient noun phrase in sentence B (Gopen & Swan).

## Grammatical Agreement

### Articles

- Every singular count noun takes a determiner: "a", "an", "the", "this", "each", or a possessive. A bare singular count noun is an error.
- "a"/"an" for a count noun at first mention or for any instance of its class: "a violation", "an invariant".
- "the" for a count noun already introduced, or fixed as unique by the context or a following restrictive phrase: "the invariant defined above", "the attacker in this example".
- No article for a generic claim about a whole class: use the bare plural ("e-commerce websites accept orders"). Never "the" + singular for the class.
- No article for a mass or abstract noun used generically: "static analysis", "data flow", "prior work".
- "a" before a consonant sound, "an" before a vowel sound; decide by sound, not spelling: "an ELV", "a unique state", "an honest user".

### Number

- The verb agrees with its grammatical subject, not with an intervening noun in a prepositional phrase.
- "each", "every", "a", "one" + singular noun take a singular verb and a singular pronoun ("it"). Never bind "they"/"them" to a singular antecedent.
- A generic statement uses the bare plural with a plural verb ("violations occur"), not a singular count noun ("a violation occurs") when the claim is about the class.
- A collective abstract noun is singular: "prior work shows", "the literature reports". Use "prior works"/"studies" only when counting distinct works.

## Tense

- Present tense for general truths, established facts, prior-work claims that still hold, and what the paper or system does: "the oracle evaluates the rule", "prior work detects ELVs".
- Past tense for completed actions of this work: experiments run, corpus collected, results obtained: "we evaluated", "the tool flagged 42 cases".
- Present perfect for prior work's contribution to the current state: "prior work has shown". Past for a specific completed study action: "Felmetsger et al. inferred invariants dynamically".
- One tense per narrative frame. No tense shift within a paragraph when describing the same event or fact.

## Terminology Consistency

- One spelling and capitalization per term throughout the paper. Never alternate hyphenated and unhyphenated forms, or capitalized and lowercase variants, for the same concept.
- A multi-word technical term has one canonical form (spacing, hyphenation, capitalization) used at every occurrence: fix "data flow" / "data-flow" / "dataflow" to a single field-standard form. Confirm the standard form via `/define-term`.
- One term per concept per section. Do not cycle synonyms to avoid repetition; repetition of the correct term aids clarity.
- The grammatical subject for the target system must remain consistent within a paragraph. Establish the precise term at first introduction (e.g., "web application"), then use it or its pronoun ("the application") for all subsequent references in the same passage. Do not shift between "site", "application", "system", and "software" within the same argument.

## Precision of Claims

- No claim that fails on a counterexample (Knuth; Dijkstra).
- Every claim is supported by evidence or qualified to be defensible.
- Degree claims, not absolutes, when prior work exists. "X remains the central difficulty", never "no such thing exists."
- No absolute quantifiers unless strictly provable: "every", "always", "all", "never". Replace with "each", "typically", or a qualified scope.
- No "requires X" for a necessity claim that is not proven. Use "X is the natural way to…" or "X is needed to…" when the necessity is contextual, not logical.
- Never equate concepts at different logical levels. A bug is a code defect; a vulnerability is an exploitable weakness. Use the term that matches the claim's level of abstraction.

## Definitions

- Define a term at the first sentence whose argument depends on it.
- Define to the depth the current argument needs. Defer formal definitions to the body.
- Lead with observable phenomenon first, then the formal definition. Never introduce a label before the reader has seen what it refers to.
- A definition that uses one method's implementation detail is not method-neutral.
- Never define a domain phenomenon using a researcher-constructed abstraction as if that abstraction is an inherent property of the domain. State the observable phenomenon first; attribute the abstraction to the research community that introduced it.
- When introducing a problem class, follow this order: (1) observable symptom, (2) prior work's model of that symptom, (3) the abstraction with its source made explicit.

## No Anthropomorphism

A program performs mechanical operations. It does not know, think, believe, or understand.

- No mental verb with a non-agent subject: "knows", "thinks", "believes", "understands", "decides", "realizes."
- State the mechanical fact: "No code path checks whether the outcome obeys the rule", not "the program does not know the outcome is wrong."
- A program "reports", "returns", "raises", "writes", "checks", "executes."

## Punctuation: Colon

Use for: a list the lead-in announces; an explanation that specifies the prior clause; an appositive naming what the prior clause referred to.

Never use for: a cause-effect link (use "because"); two independent statements with no fulfillment relation; after a verb or preposition that governs the following text.

One colon per sentence. The clause before it stands alone as a sentence.

## Punctuation: Semicolon

Use for: two independent clauses in parallel or contrast; list items that contain internal commas.

Never use for: a directional logical relation (use "because", "but", "while"); a loosely related pair (use a period).

Default to a period.

## Punctuation: Em-Dash

A paired em-dash sets off a parenthetical aside. At most once per paragraph.

Never use to: inject a definition; carry the sentence's main content as an aside.

Default to restructuring the sentence so the idea is built into its clause.

## Explanatory Prose

- One main claim per paragraph, stated in its topic sentence.
- State the root cause, not the observable symptom.
- One causal chain per paragraph. A clause appended to cover an edge case is a patch — rewrite the chain.
- A trailing clause that restates the sentence's point is a patch — drop it.
- Name a component by the action it performs: "Writes each record to the database through the storage API", not "handles storage."

## Argument Continuity

- Each paragraph ends by motivating the next; each section ending sets up the opening of the following section.
- Every promise made in an introductory paragraph must be fulfilled in the body, in the stated order. An unfulfilled promise is a structural gap.
- Logical bridge required between adjacent paragraphs. A transition that marks only sequence ("Next, …", "Then, …") is not a logical bridge.

## Metadiscourse

Cut: canned roadmap ("The rest of this paper is organized as follows…"); self-narration ("In this section we discuss"); content-free structural announcement.

Delete these throat-clearing openers: "In the realm of", "It is important to note that", "It is worth mentioning that", "It goes without saying that", "In order to", "It should be noted that", "With that being said", "When it comes to".

Keep: inline forward references woven into a claim; logical transitions marking a real relation; frame markers orienting the reader through stages.

## Post-Edit Reread

After editing any sentence, reread the entire paragraph. Fix every violation in the same pass.

## Structural Alignment

- Every figure and table must have an explicit in-text citation before or at its first appearance. No orphaned floats.
- A section introduction that enumerates topics ("we cover X, Y, and Z") must address them in the stated order with no omissions.
- Caption text must match figure content. A spatial description in the caption ("left column", "top row") must correspond to the actual layout.

## Opening

- The subject of the first substantive sentence is the paper's central artifact or domain, matching the title's primary noun (Gopen & Swan).
- No technology, language, or implementation detail appears as the grammatical subject of the opening unless the paper's title names it.
- Do not open by explaining to experts why their field is important. Open with the paper's specific purpose (Shewchuk).

## Paper Structure

- Abstract: four sentences — (1) the problem, (2) why it is hard, (3) the approach, (4) the result (Peyton Jones).
- Introduction: problem description and contribution list only. No background, no related work, no methodology. One page.
- Related work follows the core idea, not precedes it. Readers cannot evaluate related work before understanding the contribution (Peyton Jones).
- State the contribution at four levels of detail: title (~10 words), abstract (~100 words), introduction (~1000 words), body (~10,000 words). Each level is independently coherent and consistent with the others (Levin & Redell).

## Contributions

- Write the contribution list before drafting the body. The body provides evidence for the contributions, not the other way around (Peyton Jones).
- Each contribution is a single refutable sentence. "We describe X" is not a contribution. "We prove X satisfies property Y (Section N)" is (Peyton Jones).
- Forward-reference the evidence for each contribution at the point of the claim in the introduction.
- Signal explicitly whether the work is novel (new scientific observation) or incremental (improvement over prior work). Do not leave the reader to infer which (McDaniel).

## Evaluation

- State upfront whether the system is implemented and deployed, unimplemented, or purely theoretical. Readers have a right to know this before investing in the paper (Levin & Redell).
- Report failures, limitations, and trade-offs alongside successes. An evaluation that measures only what the system does well invites reviewer skepticism (Levin & Redell).
- Every paper must answer three questions: (1) What is the contribution? (2) What is the new result and how does it differ from prior work? (3) Why should the reader believe the result? (Shaw).

## Conclusions

- Conclusions must add new information: implications, conjectures, open problems, perspective gained after reading the full paper (Shewchuk).
- Do not summarize the paper in the conclusions. The reader has just read it. A conclusion the reader could understand before reading the paper adds nothing.

## Evidence and Attribution

- Cite a third party's metric only when that party's relation to the subject is verifiable.
- External links unverifiable: state the subject is a representative instance.

