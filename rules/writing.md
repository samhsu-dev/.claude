---
paths:
  - "**/*.tex"
---

# Academic Prose Precision

Community standards: Strunk & White; Williams (*Style*); Pinker (*Sense of Style*); Gopen & Swan (*Science of Scientific Writing*, 1990); Knuth, Larrabee & Roberts (*Mathematical Writing*); Zobel (*Writing for Computer Science*); Peyton Jones (*How to write a great research paper*); Whitesides; Dijkstra (EWD).

Every term maps to a concrete, verifiable referent. No vague words.

---

## Term Grounding

- Every abstract noun states its exact referent at first use (Pinker; Knuth; Zobel; IEEE/ACM).
- No self-invented terms. Use an established term with a citation, or define inline with a concrete referent (Dijkstra; Knuth).
- One concept, one name. Use the same term throughout; never rename a concept mid-paper (Knuth; Zobel).
- Prefer the concrete mechanism over the abstract label (Strunk & White; Pinker; Zobel). "A fixed set of sinks such as `echo`, `mysql_query`" not "a general detection criterion".
- Combat the curse of knowledge: unpack every piece of jargon a non-specialist reader cannot resolve (Pinker).

## Banned Vague Words

- No "technical specification", "technical error", "security property", "correctness standard" unless defined inline with a concrete referent.
- No subjective qualifier as the sole characterization: "general", "generic", "novel", "efficient", "robust", "proper", "appropriate", "effective" (IEEE/ACM; Whitesides). Replace with a measurement or a concrete property.
- No modifier that adds no information: "very", "quite", "simply", "clearly".

## Word-Level Register

Standards: Strunk & White; Zobel; ACM/IEEE editorial guides; Manchester Academic Phrasebank.

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

- No claim that fails on a counterexample. Verify every characterizing claim against one counterexample before writing it (Knuth; Zobel; Dijkstra).
- Every claim is supported by evidence or qualified to be defensible (Zobel; Whitesides).
- State the contribution as a single explicit, refutable sentence (Whitesides; Peyton Jones).
- Degree claims, not absolutes, when prior work exists. "X remains the central difficulty", never "no such thing exists".

## Definitions

- Define a term at the first sentence whose argument depends on it. No earlier; no separate glossary in the introduction (Knuth; Zobel).
- Define to the depth the current argument needs. Defer formal definitions to the body.
- Lead with a concrete example, then the general statement (Peyton Jones).
- A definition that uses one method's implementation detail is not method-neutral. State problem difficulty without naming any solution's mechanism.

## Sentence Structure

- Make the main character the grammatical subject; express the key action as a verb, not a nominalization (Williams; Gopen & Swan).
- Place old/familiar information first, new information at the sentence end (stress position) (Gopen & Swan; Williams).
- Omit needless words (Strunk & White).
- State each claim once. Two sentences asserting the same point → keep one.

## Explanatory Prose

- Explaining a defect or mechanism: state the root cause, not the observable symptom. "The developer trusted the value after it round-tripped through the client", not "the value is attacker-controlled".
- One causal chain per paragraph. A clause appended to cover an edge case is a patch. Rewrite the chain to include the case, or drop it.
- A trailing clause that restates the sentence's point is a patch. Drop it.
- Name a component by the action it performs, not a placeholder verb. "Settles the order through the payment SDK", not "handles payment".

## Metadiscourse

Standards: Williams (*Style*); Hyland (*Metadiscourse*, 2005); Peyton Jones; Manchester Academic Phrasebank.

Writing needs some metadiscourse; too much buries the content (Williams). Keep the kind that carries a logical relation or a pointer the reader needs; cut the kind that only announces structure or narrates the act of writing.

Cut:
- The canned roadmap: "The rest of this paper is organized as follows. Section 2... Section 3..." (Peyton Jones). Replace with inline forward references from the narrative.
- Self-narration: "In this section we discuss", "as we will show", "it is important to note that".
- Content-free structural announcement: "this poses N challenges", "in the same order as the introduction".

Keep:
- Inline forward references woven into a claim: "We prove the type system sound (\autoref{...})" (Peyton Jones).
- Logical transitions that mark a real relation: "but", "thus", "in contrast to X" (Hyland transitions).
- Frame markers that orient the reader through stages: "We first bind each variable; building on it, we then mutate the inputs" (Hyland frame markers).
- Endophoric pointers that aid reuse: "as defined in \autoref{...}".

The line: a sentence that *announces* structure is cut; a sentence that *carries* a logical relation or a needed pointer is kept.

## Post-Edit Reread

- After editing any sentence, reread the entire paragraph before stopping. Local edits accumulate redundancy and patches at sentence seams.
- Verify the paragraph is one causal chain, states each claim once, and carries no meta-commentary. Fix every violation in the same pass.

## Evidence and Attribution

- Cite a third party's metric only when that party's relation to the subject is verifiable. Same vendor or same framework is not a verified relation.
- External links unverifiable: state the subject is a representative instance, defer the magnitude to where it is established.

## BELUGA Term Discipline

- Invariant: a boolean predicate over domain-level semantic variables (e.g., `total = price * quantity`). Semantics are application-independent.
- Oracle: the in-code, runtime check that decides whether an invariant holds in one application.
- The invariant's semantics are application-independent and reusable. Only the binding of semantic variables to concrete code locations is application-specific. Never conflate the two.
- "No scalable oracle" is a degree claim, not an absolute. State it as a difficulty, never as non-existence, since prior work supplies oracles.
