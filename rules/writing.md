---
paths:
  - "**/*.tex"
---

# Academic Prose Precision

Community standards: Strunk & White; Gopen & Swan (*Science of Scientific Writing*, 1990); Knuth, Larrabee & Roberts (*Mathematical Writing*); Peyton Jones (*How to write a great research paper*); Dijkstra (EWD).

Every term maps to a concrete, verifiable referent. No vague words.

---

## Term Grounding

- Every abstract noun states its exact referent at first use (Knuth; IEEE/ACM).
- No self-invented terms. Use an established term with a citation, or define inline with a concrete referent (Dijkstra; Knuth).
- One concept, one name. Use the same term throughout; never rename a concept mid-paper (Knuth).
- Use the concrete mechanism, not the abstract label (Strunk & White). "A fixed set of sinks such as `echo`, `mysql_query`" not "a general detection criterion".
- Combat the curse of knowledge: unpack every piece of jargon a non-specialist reader cannot resolve.

## Banned Vague Words

- No "technical specification", "technical error", "security property", "correctness standard" unless defined inline with a concrete referent.
- No subjective qualifier as the sole characterization: "general", "generic", "novel", "efficient", "robust", "proper", "appropriate", "effective" (IEEE/ACM). Replace with a measurement or a concrete property.
- No modifier that adds no information: "very", "quite", "simply", "clearly".

## Overloaded Technical Terms

Certain words carry precise formal meanings in program analysis, formal methods, or security research. Using them informally invites reviewer challenges ("prove it") that the paper cannot answer.

- **"sound"** — in program analysis, soundness means the analysis reports no false negatives (all real violations are found); proving soundness requires a formal argument. Never use "sound" as a plain adjective meaning "correct" or "valid." Replace with a description of the property: "an invariant derived from domain knowledge rather than observed data" or "an invariant that encodes a real obligation."
- **"complete"** — in formal methods, completeness means no false positives; similarly requires proof. Never use "complete" to mean "thorough" or "comprehensive."
- **"correct"** — implies formal correctness. When the intended meaning is "accurate" or "consistent with domain rules," say so explicitly.
- **"genuine"** — colloquial; does not map to a verifiable property. Replace with the concrete description of what makes the thing genuine: "an invariant that encodes a real obligation the application must satisfy, not a coincidence in observed data."
- **"real"** as a standalone qualifier (e.g. "a real rule", "a real vulnerability") — imprecise. State the criterion: "a rule the application must always obey" or "a transaction that the application accepts and that violates an e-commerce invariant."

General rule: if a word could trigger the reviewer question "how do you define/prove that?", replace it with the concrete property or mechanism you actually mean.

## Word-Level Register

Standards: Strunk & White; ACM/IEEE editorial guides; Manchester Academic Phrasebank.

Neutral, direct words over literary or conversational ones. Replacements:

| Banned | Reason | Use |
|--------|--------|-----|
| "yet" as a conjunction | literary; also reads as the adverb "not yet" | "but"; or "both A and B"; or state the tension explicitly |
| "whilst", "amongst", "amidst" | British-literary register | "while", "among", "amid" |
| "hence" | most archaic of the cause connectives | "therefore", "thus" |
| "in order to" | wordy | "to" |
| "utilize", "leverage", "employ" (= use) | inflated | "use" |
| "a number of", "a variety of" | vague quantity | a number, or "several" |
| "it should be noted that", "it is worth noting that" | meta-filler | delete; state the fact |
| "delve", "showcase", "underscore", "pivotal", "crucial", "seamless" | LLM-register inflation | concrete verb or measured property |

Connectives ("thus", "therefore", "moreover", "furthermore", "consequently") are valid at any position, including sentence start. Use one only where it marks a genuine logical relation. No filler connective, and no two consecutive sentences opened by a connective.

- No contractions ("don't", "it's") in body text.
- No first-person "I". Use "we" for authorial action; passive only when the actor is irrelevant.
- Latin abbreviations: "e.g.", "i.e.", "cf." inside parentheses only; spell out ("for example") in running text.

## Precision of Claims

- No claim that fails on a counterexample. Verify every characterizing claim against one counterexample before writing it (Knuth; Dijkstra).
- Every claim is supported by evidence or qualified to be defensible.
- State the contribution as a single explicit, refutable sentence (Peyton Jones).
- Degree claims, not absolutes, when prior work exists. "X remains the central difficulty", never "no such thing exists".

## Definitions

- Define a term at the first sentence whose argument depends on it. No earlier; no separate glossary in the introduction (Knuth).
- Define to the depth the current argument needs. Defer formal definitions to the body.
- Lead with a concrete example, then the general statement (Peyton Jones).
- A definition that uses one method's implementation detail is not method-neutral. State problem difficulty without naming any solution's mechanism.

## Sentence Structure

- Make the main character the grammatical subject; express the key action as a verb, not a nominalization (Gopen & Swan).
- Place old/familiar information first, new information at the sentence end (stress position) (Gopen & Swan).
- Omit needless words (Strunk & White).
- State each claim once. Two sentences asserting the same point → keep one.

## No Anthropomorphism

A program, model, or algorithm performs mechanical operations. It does not know, think, believe, want, understand, or hold a notion. Attributing cognition to code states no verifiable fact.

- No mental verb with a non-agent subject: "knows", "thinks", "believes", "understands", "wants", "decides", "is aware", "has no notion of", "realizes". Not "the program has no notion of correctness."
- State the mechanical fact instead. "No code path checks whether the outcome obeys the rule", not "the program does not know the outcome is wrong."
- Name the human actor when cognition is the point. "The developer assumes the value is trustworthy", not "the code trusts the value."
- A program "reports", "returns", "raises", "writes", "checks", "executes" — concrete operations it performs. These are not anthropomorphism.

## Punctuation: Colon

A colon promises that what follows completes or specifies what precedes. The clause before the colon is grammatically complete and raises an expectation; the text after fulfills it.

Use a colon for:
- A list the lead-in announces. "The pipeline runs in three stages: parsing, analysis, and reporting."
- An explanation or restatement that specifies the prior clause. "The two runs diverge in one place: the loader reads the file eagerly in one, lazily in the other."
- An appositive that names what the prior clause referred to. "One field defeats the parser: the trailing checksum."

Never use a colon for:
- A cause-effect link. Use "because", "so", "therefore". Not "The violation raises no error: no code path checks the outcome" but "...no error, because no code path checks the outcome."
- Two independent statements with no lead-in/fulfillment relation. Use a period or "and".
- After a verb or preposition that already governs the following text. Not "The stages are: A, B, C" but "The stages are A, B, C."

One colon per sentence. The clause before it stands alone as a sentence.

## Punctuation: Semicolon

A semicolon joins two complete, closely related statements as equals, or separates list items that themselves contain commas. It marks balance, not direction.

Use a semicolon for:
- Two independent clauses in parallel or contrast, each a complete sentence. "Detection needs an external criterion; reproduction needs a triggering input."
- List items that contain internal commas. "We evaluate three sites: a store in Berlin, Germany; a shop in Paris, France; and a market in Tokyo, Japan."

Never use a semicolon for:
- A directional logical relation — cause, contrast, or sequence. Use the connective that names it: "because", "so", "but", "while", "instead". Not "The rule is application-independent; only the binding is application-specific" but "...application-independent, while only the binding is application-specific."
- A loosely related pair. Use a period.
- A dependent clause on either side. Both sides stand alone as sentences, or it is not a semicolon.

Default to a period. Use a semicolon only when the two clauses are strict parallels and the balance carries meaning.

## Punctuation: Em-Dash

A paired em-dash (`---...---`) sets off a parenthetical aside. It is valid punctuation, but it bolts material onto a sentence instead of integrating it. Overuse becomes a stylistic tell.

Never use a paired em-dash to:
- Inject a definition. Not "the violation of an invariant---a rule that must always hold---triggers no error" but a separate defining sentence, or a colon that announces the definition.
- Carry the sentence's main content as an aside. If the material is the point, it belongs in the main clause.

Use a paired em-dash only for a genuine aside the main clause does not need, and at most once per paragraph. A single em-dash for a list lead-in or a sharp break is unrestricted.

Default to restructuring the sentence so the idea is built into its clause.

## Explanatory Prose

- Explaining a defect or mechanism: state the root cause, not the observable symptom. "The developer trusted the value after it round-tripped through the client", not "the value is attacker-controlled".
- One causal chain per paragraph. A clause appended to cover an edge case is a patch. Rewrite the chain to include the case, or drop it.
- A trailing clause that restates the sentence's point is a patch. Drop it.
- Name a component by the action it performs, not a placeholder verb. "Settles the order through the payment SDK", not "handles payment".

## Metadiscourse

Standards: Peyton Jones; Manchester Academic Phrasebank.

Writing needs some metadiscourse; too much buries the content. Keep the kind that carries a logical relation or a pointer the reader needs; cut the kind that only announces structure or narrates the act of writing.

Cut:
- The canned roadmap: "The rest of this paper is organized as follows. Section 2... Section 3..." (Peyton Jones). Replace with inline forward references from the narrative.
- Self-narration: "In this section we discuss", "as we will show", "it is important to note that".
- Content-free structural announcement: "this poses N challenges", "in the same order as the introduction".

Keep:
- Inline forward references woven into a claim: "We prove the type system sound (\autoref{...})" (Peyton Jones).
- Logical transitions that mark a real relation: "but", "thus", "in contrast to X".
- Frame markers that orient the reader through stages: "We first parse the input; building on that, we then analyze it".
- Endophoric pointers that aid reuse: "as defined in \autoref{...}".

The line: a sentence that *announces* structure is cut; a sentence that *carries* a logical relation or a needed pointer is kept.

## Post-Edit Reread

- After editing any sentence, reread the entire paragraph before stopping. Local edits accumulate redundancy and patches at sentence seams.
- Fix every violation surfaced by the reread in the same pass.

## Evidence and Attribution

- Cite a third party's metric only when that party's relation to the subject is verifiable. Same vendor or same framework is not a verified relation.
- External links unverifiable: state the subject is a representative instance, defer the magnitude to where it is established.

## BELUGA Term Discipline

- Invariant: a boolean predicate over domain-level semantic variables (e.g., `total = price * quantity`). Semantics are application-independent.
- Oracle: the in-code, runtime check that decides whether an invariant holds in one application.
- The invariant's semantics are application-independent and reusable. Only the binding of semantic variables to concrete code locations is application-specific. Never conflate the two.
- "No scalable oracle" is a degree claim, not an absolute. State it as a difficulty, never as non-existence, since prior work supplies oracles.
