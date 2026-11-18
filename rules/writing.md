---
paths:
  - "**/*.tex"
---

# Academic Prose

## Governing Principle

- Each term, claim, and transition is verifiable from the text before it. No sentence depends on a later section.
- The target reader is a computer-science expert who has not read this paper.
- Never define a field-standard CS term (data flow, static analysis, precision, recall, NP-hardness).
- Define every paper-specific term, system name, and non-standard use of a common word at its first use.

## Term Grounding

- Use an established term and cite its source. Introduce a new term only when no established term names the concept, and define it at first use by a concrete referent.
- One concept has one name in the whole paper.
- Name the concrete mechanism instead of an abstract label: "a fixed set of calls such as `read()` and `write()`", not "a general detection criterion".
- Never use a term whose meaning in an adjacent field (payments, security, programming languages, networking) differs from the intended sense. Example: "settlement" means bank-side fund clearing, not checkout completion.

## Word Choice Precision

- Never characterize a result or a system only by "general", "generic", "novel", "efficient", "robust", "proper", "appropriate", or "effective". Replace the word with a measurement or a concrete property.
- Delete a modifier when the claim is equally specific without it: "very", "quite", "clearly", "direct", and a modifier true of every member of its class ("custom implementation").
- Never write "technical specification", "technical error", "security property", or "correctness standard" without an inline definition.
- **Overloaded terms.** Write "sound" only for no false negatives, "complete" only for no false positives, and "correct" only for a formal proof. Never use "genuine" or "real" as a property; state the criterion.
- **Near-synonym precision.** "Accuracy", "precision", "recall", "F1", "correctness", "soundness", and "completeness" are distinct. Write the one the paper computes or proves.
- Before using a term whose field-standard meaning is unconfirmed, confirm it with `/define-term`.
- State a quantitative comparison with a noun phrase and a relational verb: "the measured latency was lower than the baseline", not "the latency fell far short of the baseline".

## Word-Level Register

| Banned | Use |
|--------|-----|
| "yet" as a conjunction | "but" |
| "whilst", "amongst", "amidst" | "while", "among", "amid" |
| "hence" | "therefore", "thus" |
| "in order to" | "to" |
| "utilize", "leverage", "employ" (meaning use) | "use" |
| "a number of", "a variety of" | a number, or "several" |
| "it should be noted that" | delete; state the fact |
| "delve", "showcase", "underscore", "pivotal", "crucial", "seamless" | a concrete verb or a measured property |
| "translate to" (causal) | "result in", "lead to", "cause" |
| "by hand" | "manually" |
| "call it", "call X Y" | "refer to it as", "refer to X as Y" |
| "spans" with an abstract subject | "accounts for", "is distributed across", "covers" |

- Never open two consecutive sentences with a connective.
- No contractions.
- No "I". Write "we" for an action of the authors.
- Write "e.g.", "i.e.", and "cf." only inside parentheses. In running text, write "for example", "that is", "compare".

## Sentence Structure

- The actor is the grammatical subject and the action is the main verb: "COBRA resolves the call", not "the resolution of the call is performed by COBRA".
- Never write "emerges", "reveals", "suggests", or "captures" with a non-agent subject. Write a literal verb.
- A participial phrase has the same subject as its main clause.
- Known information opens a sentence; new information ends it.
- The subject of sentence N+1 is the concept at the end of sentence N. Otherwise sentence N+1 opens with a clause that names its relation to sentence N.
- Delete each word whose removal loses no fact, number, or relation.
- One sentence states one of: a definition, a causal claim, an example.
- Within a paragraph, no five consecutive sentences have lengths within 5 words of each other. Add a sentence under 10 words or merge two sentences.
- A term that appears in sentence A only as a modifier or inside a prepositional phrase is not the referent of "this X" or "that X" in sentence B. Make the term the subject or the final phrase of sentence A, or repeat the full noun phrase in sentence B.

## Grammatical Agreement

### Articles

- Every singular count noun has a determiner: "a", "an", "the", "this", "each", or a possessive.
- Write "a" or "an" at the first mention of a count noun and for an arbitrary instance: "a violation", "an invariant".
- Write "the" for a count noun already introduced or made unique by a restrictive phrase: "the invariant defined above".
- A claim about a whole class takes the bare plural: "e-commerce websites accept orders". Never "the" plus a singular noun for a class.
- A mass or abstract noun used generically has no article: "static analysis", "data flow", "prior work".
- Choose "a" or "an" by the sound of the next word: "an ELV", "a unique state", "an honest user".

### Coordination

- One verb governs coordinated objects only when it fits each object: "receives the source and the flow, and uses the backend", not "receives the source, the flow, and the backend".

### Number

- The verb agrees with its grammatical subject, not with a noun inside an intervening prepositional phrase.
- "Each", "every", "a", and "one" plus a singular noun take a singular verb and "it". Never "they" or "them" for a singular antecedent.
- A claim about a class takes the bare plural and a plural verb: "violations occur".
- "Prior work" and "the literature" are singular. Write "prior works" or "studies" only when counting distinct works.

## Tense

- Present tense: general facts, prior-work claims that still hold, and what the paper or the system does.
- Past tense: completed actions of this work, such as experiments run and results obtained.
- Present perfect for the state prior work has established ("prior work has shown"); past tense for one completed study ("Felmetsger et al. inferred invariants").
- One tense per described event within a paragraph.

## Terminology Consistency

- Name each compared system, tool, variant, and dataset by its own name. Write a group noun ("the two systems", "the variants", "the baselines") only when the same or the preceding sentence lists its members. Never write a generic word ("configuration") for a named entity (STRIX-Control).
- A count word ("two", "both", "all three") equals the number of listed members, including `\sys{}` when it is compared. One count word per set.
- Write a pronoun ("it", "them", "this step") only when its antecedent is the nearest preceding noun phrase. Otherwise repeat the noun.
- One spelling, hyphenation, and capitalization per term in the whole paper: one of "data flow", "data-flow", "dataflow". Confirm the field-standard form with `/define-term`.
- Repeat the same term for the same concept. Never alternate synonyms.
- Within a passage, refer to the target system by the term introduced first ("web application", then "the application"). Never switch among "site", "application", "system", and "software".

## Precision of Claims

- A claim holds for every case in its stated scope. Test it against one counterexample before writing it.
- Support each claim with a citation, a table, a figure, or a stated derivation.
- Write a universal quantifier ("every", "all", "always", "never", "no") only when each member of the stated set is verified. Otherwise state the scope: "in 62 of the 100 repositories", "in our evaluation".
- When prior work exists, state the degree: "X remains the central difficulty", not "no solution exists".
- Write "requires X" only for a proven necessity. Otherwise write "X is needed to ... in this setting".
- Use the term at the level of the claim: a bug is a code defect; a vulnerability is an exploitable weakness.
- A derived clause ("as a result", "this means", "so that") asserts only what its premises entail. It adds no actor, need, capability, or effect absent from the premises.
- Between a weaker statement that follows from the premises and a stronger one that needs an unstated assumption, write the weaker one.

## Definitions

- Define a term in the sentence of its first use.
- In the abstract and the introduction, define a term informally. Give the formal definition in the approach section.
- Describe the observable phenomenon before naming it.
- A definition of a problem class names no detail of one method.
- Introduce a problem class in this order: (1) the observable symptom, (2) prior work's model of the symptom, (3) the abstraction, attributed to the work that introduced it.

## No Anthropomorphism

- Never write "knows", "thinks", "believes", "understands", "decides", or "realizes" with a program or a component as the subject.
- Write the mechanical fact: "no code path checks the order total", not "the program does not know the total is wrong".
- Verbs for a program: "reports", "returns", "raises", "writes", "checks", "executes".

## Explanatory Prose

- The topic sentence of a paragraph states its one main claim.
- State the cause, not the symptom.
- One causal chain per paragraph. When an edge case needs a clause, rewrite the chain to include it instead of appending the clause.
- Delete a trailing clause that restates its sentence.
- Delete a sentence that restates, announces, or explains what an expert reads from the numbers.
- State a claim directly. Never set it up with a counterexample or a "not X but Y" contrast.
- Write a connective only when it names a contrast, consequence, or condition that the sentences do not show without it.
- Name a component by its action: "writes each record to the database through the storage API", not "handles storage".

## Argument Continuity

- The last sentence of a paragraph states the fact or gap that the next paragraph's topic sentence takes up. The last paragraph of a section does the same for the next section.
- When an introductory paragraph lists topics, the body covers each topic in the listed order.
- Adjacent paragraphs are linked by a stated relation. "Next" or "Then" alone states no relation.

## Metadiscourse

- Delete roadmap sentences ("The rest of this paper is organized as follows") and self-narration ("In this section we discuss").
- Delete these openers: "In the realm of", "It is important to note that", "It is worth mentioning that", "It goes without saying that", "It should be noted that", "With that being said", "When it comes to".
- Keep a forward reference inside a claim: "the binding feedback loop (Section III-C) rejects ...".

## Post-Edit Reread

- After editing a sentence, reread its whole paragraph and fix every violation of this file in the same edit.
- After changing a description, number, or term, search all `.tex` sources for its other occurrences and change them in the same edit.
- Check each edited paragraph: (1) no sentence is deletable under Explanatory Prose; (2) every term is canonical and defined at first use; (3) each verb fits all its objects; (4) each causal verb rests on a controlled comparison; (5) each number and system behavior matches its source; (6) the topic sentence takes up the last sentence of the previous paragraph.

## Structural Alignment

- Cite every figure and table in the text at or before its first appearance.
- A caption describes what the figure shows. A spatial word in a caption ("left column", "top row") matches the layout.

- Every measured number appears first in the evaluation section, in its text, a table, or a figure. The abstract, introduction, discussion, threats to validity, and conclusion repeat only numbers the evaluation section reports.

## Evidence and Attribution

- Cite a third party's number only when the third party's relation to the measured subject is verifiable.
- When a linked external subject cannot be verified, present it as a representative instance, not as a measured fact.
