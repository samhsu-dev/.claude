---
paths:
  - "**/overview.tex"
  - "**/overall.tex"
---

# Overview Structure

Three subsections driven by one running example. The example is introduced once and reused for every challenge and every solution. The reader understands one code snippet and follows the whole section.

---

## Subsections

| # | Subsection | Function | Internal order |
|---|------------|----------|----------------|
| 1 | Motivating Example | Establish one concrete carrier for all later argument | Anchor case → domain scale → high-level consequence → mechanism primer → line-level walkthrough |
| 2 | Solution Overview | Lead with the key insight, then show each mechanism on the snippet | Key insight + core artifact + strategy → N self-contained blocks, each: difficulty on the snippet → one-line why naive/prior fails → mechanism traced on the same lines |
| 3 | Threat Model | Bound the scope | Target class → attacker capabilities → attacker knowledge → covered vulnerability types |

## Opening Sentence

- One sentence declaring the section uses a single example to illustrate the solution.

## Motivating Example (1)

Five elements in fixed order:

| # | Element | Content |
|---|---------|---------|
| 1 | Anchor | Source repositories + the real cases the snippet splices + how each was confirmed |
| 2 | Scale | The case is production-grade: maintained, real deployment. Defer the magnitude numbers to module 1 |
| 3 | Consequence | One sentence on what the vulnerability lets an attacker do |
| 4 | Primer | The components the walkthrough crosses, each named by its concrete responsibility, plus the invariant under test |
| 5 | Walkthrough | The root-cause developer error as one causal chain, naming concrete variables and line numbers |

Rules:
- One snippet. Every challenge and solution refers back to it by line number.
- Cases are real and traceable to a source repository. No hypothetical code.
- A spliced snippet states every source repository it draws from, by repository name only.
- State how each case was confirmed: manual validation, a tool's false negative, or a tool's false positive.
- The primer explains only the mechanism the walkthrough depends on.

### Scale element
- State the case is maintained and in real deployment. No invented magnitude numbers.
- Cite a third party's scale only when that party's relation to the case is verifiable. An unverified link (same vendor, same framework) is not scale evidence — drop it.
- Module 1 carries the domain magnitude. The motivating case need only be a representative instance of it.

### Primer element
- Name each component by the responsibility it owns. No vague verb ("builds", "handles") that the next paragraph must correct.
- Declare the correctness property under test explicitly, using the term defined in introduction module 1.
- Close the primer on the state where the property holds, so the walkthrough opens on the state where it is broken.

### Walkthrough element
- State why the developer made the mistake, not only the data path. The reader learns the root cause, not just the symptom.
- One causal chain in one paragraph. No clause appended per edge case — that reads as a patch.
- Trace source → tainted use → sink by line number, then the one-line exploit, then the no-signal observation (no crash, no error status, no tainted-sink alarm).

## Code Snippet Conventions

Code lives in a standalone asset file, included with `\lstinputlisting[language=..., caption={...}, label={lst:motivating}]{...}`. Define a line-reference macro bound to that label for use throughout the section.

### Code form
- Under 30 lines. Lines short enough not to wrap in one column.
- Top-level functions, not class methods. Short function names.
- Short variable names (`vid`, `qty`).
- File-origin banner comment marks code spliced from different files.
- Attacker-controlled input appears as the language's request-parameter access directly, so the source is visible.
- Real code, simplified for illustration. The caption states "slightly simplified".

### Comment form
- A comment supplies only what the code cannot show: a cross-layer guard, a runtime fact, a domain rule.
- No comment restates what the code already expresses.
- Comments occupy their own line above the code they annotate. No trailing inline comments that force wrapping.
- Challenge tags `// C1:`, `// C2:`, ... mark the code site of each challenge, one per challenge. One axis only. No TP/FP/FN tags in the snippet.

### Property line
- The correctness property is a mathematical expression over domain-level variables, written as a comment: `// Property: <expression>`.
- Domain variables are application-independent. No code symbols in the expression.

### Challenge sites
- Each challenge marks one code site, mapping 1:1 to introduction module 3.
- One tag per challenge, in the introduction's order. Each tag sits at the line where that challenge is concretely visible.
- A tag marks where the challenge manifests, not how the method solves it.

## Solution Overview (2)

Structure is insight-driven, not challenge-driven: the section is organized by the method's mechanisms, and the difficulty each mechanism overcomes is stated inside that mechanism's block. Use this structure when the work has no dense same-direction prior work to compare against line by line.

Opening paragraph (one, before the solution blocks):
- State the key insight in one or two sentences: the observation that makes the problem solvable, and the core artifact it leads to. Define the core artifact inline with a concrete referent.
- Point to where each step's difficulty appears in the running snippet, one clause per step, by line number. No detail here — this paragraph is a map.
- Close with one sentence stating the method's core strategy (build the artifact, then use it).

Solution blocks (`2.2.1`, `2.2.2`, ...), 1:1 with mechanisms, in the order the artifact is built then used. Each block is self-contained: difficulty on the snippet, then mechanism, so each example appears once in the whole section.
- Name the mechanism, italicized, reusing the introduction module-4 innovation name.
- Open on the difficulty as it appears on the running snippet. The first sentence names a line or value in the snippet.
- State why a naive or prior approach does not overcome it — one clause, at the class level (no line-by-line targeting of a tool that does not operate on this snippet).
- Trace the mechanism over the same lines; the mechanism emerges from the concrete trace.
- Reference one figure that illustrates the mechanism on the snippet.

Term discipline:
- Overview gives intuition in plain words. Self-coined formal terms (e.g. invariant semantics, semantic variable, concrete variable) and pipeline-internal component names debut in the approach section, not here.
- A named, inline-defined core artifact (the oracle) is allowed; an undefined formal term is not.

Rules:
- Mechanism count = challenge count = solution count. Same order maps to the introduction's challenges.
- Never rename a challenge or innovation introduced in the introduction.
- Each example (line or value) is developed in one block only. No difficulty detail is repeated in the opening paragraph.
- Each solution block carries one figure walking the mechanism over the snippet.
- The overview and the introduction are complementary: the introduction states each mechanism as a one-sentence idea; the overview shows it on the snippet at line level.
- No sentence restates the introduction's abstract description of a mechanism. Carry the idea forward by demonstrating it on the snippet, not by repeating it.

## Threat Model (3)

| # | Element | Content |
|---|---------|---------|
| 1 | Target class | The one vulnerability class this work detects |
| 2 | Capabilities | The input channels the attacker controls |
| 3 | Knowledge | What the attacker knows and the access denied |
| 4 | Covered types | List of vulnerability types, each with a CWE number and one real CVE |

## Invariants

- One running example carries the entire section.
- Challenge and solution lists map 1:1 and reuse the introduction's terms and order.
- Criticize prior work by tool name and specific failure on the running example. Never by generic claim.
- Each solution block references one figure.

## Cross-Section Consistency

- Challenge names: identical to introduction module 3.
- Innovation names: identical to introduction module 4.
- Core artifact: the same artifact named in introduction module 4 mechanism overview.
