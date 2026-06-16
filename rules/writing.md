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
- One concept, one name. Never rename a concept mid-paper (Knuth).
- Use the concrete mechanism, not the abstract label. "A fixed set of sinks such as `echo`, `mysql_query`" not "a general detection criterion".

## Banned Vague Words

- No subjective qualifier as the sole characterization: "general", "generic", "novel", "efficient", "robust", "proper", "appropriate", "effective". Replace with a measurement or a concrete property.
- No modifier that adds no information: "very", "quite", "simply", "clearly", "direct".
- No "technical specification", "technical error", "security property", "correctness standard" unless defined inline.

## Overloaded Technical Terms

These words carry precise formal meanings. Using them informally invites reviewer challenges ("prove it") the paper cannot answer.

- **"sound"** — proves no false negatives; requires a formal argument. Replace with a description of the specific property: "derived from domain knowledge rather than observed data."
- **"complete"** — proves no false positives; requires proof. Replace with a concrete coverage description.
- **"correct"** — implies formal correctness. Use "accurate" or state the specific property.
- **"genuine"** — colloquial; does not map to a verifiable property. Replace with the concrete criterion: "encodes an obligation the system must satisfy, not a coincidence in observed data."
- **"real"** as a standalone qualifier — imprecise. State the criterion explicitly.

If a word could trigger "how do you define/prove that?", replace it with the concrete property you mean.

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

- Connectives ("thus", "therefore", "moreover") mark genuine logical relations only. No filler connective. No two consecutive sentences opened by a connective.
- No contractions in body text.
- No first-person "I". Use "we" for authorial action.
- Latin abbreviations: "e.g.", "i.e.", "cf." inside parentheses only; spell out in running text.

## Sentence Structure

- Main character as grammatical subject; key action as a verb, not a nominalization (Gopen & Swan).
- Old/familiar information first, new information at sentence end (stress position) (Gopen & Swan).
- Omit needless words (Strunk & White).
- State each claim once.

## Precision of Claims

- No claim that fails on a counterexample (Knuth; Dijkstra).
- Every claim is supported by evidence or qualified to be defensible.
- State the contribution as a single explicit, refutable sentence (Peyton Jones).
- Degree claims, not absolutes, when prior work exists. "X remains the central difficulty", never "no such thing exists."

## Definitions

- Define a term at the first sentence whose argument depends on it.
- Define to the depth the current argument needs. Defer formal definitions to the body.
- Lead with a concrete example, then the general statement (Peyton Jones).
- A definition that uses one method's implementation detail is not method-neutral.

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

- State the root cause, not the observable symptom.
- One causal chain per paragraph. A clause appended to cover an edge case is a patch — rewrite the chain.
- A trailing clause that restates the sentence's point is a patch — drop it.
- Name a component by the action it performs: "Settles the order through the payment SDK", not "handles payment."

## Metadiscourse

Cut: canned roadmap ("The rest of this paper is organized as follows…"); self-narration ("In this section we discuss"); content-free structural announcement.

Keep: inline forward references woven into a claim; logical transitions marking a real relation; frame markers orienting the reader through stages.

## Post-Edit Reread

After editing any sentence, reread the entire paragraph. Fix every violation in the same pass.

## Evidence and Attribution

- Cite a third party's metric only when that party's relation to the subject is verifiable.
- External links unverifiable: state the subject is a representative instance.

