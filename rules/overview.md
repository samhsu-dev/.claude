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
| 2 | Key Challenges and Solution Overview | Pair each challenge with its solution | Core-artifact lead → N challenges (each with example + SOTA failure) → strategy closer → N solution blocks (1:1, same order) |
| 3 | Threat Model | Bound the scope | Target class → attacker capabilities → attacker knowledge → covered vulnerability types |

## Opening Sentence

- One sentence declaring the section uses a single example to illustrate both the challenges and the solution overview.

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
- Name each component by the responsibility it owns: rendering, persistence, external settlement. No vague verb ("builds", "handles") that the next paragraph must correct.
- Declare the invariant under test explicitly: "the business-logic invariant we consider is X". Use the term `business-logic invariant`, matching module 1.
- Close the primer on "the application is correct only when this invariant holds", so the walkthrough opens on "this invariant is broken here".

### Walkthrough element
- State why the developer made the mistake, not only the data path. The reader learns the root cause, not just the symptom.
- One causal chain in one paragraph. No clause appended per edge case — that reads as a patch.
- Trace source → tainted use → sink by line number, then the one-line exploit, then the no-signal observation (no crash, no error status, no tainted-sink alarm).

## Code Snippet Conventions

Code lives in `Assets/motivating.php`. The section includes it with `\lstinputlisting[language=myPHP, caption={...}, label={lst:motivating}]{Assets/motivating.php}` and defines `\newcommand{\motivline}[1]{\refline{lst:motivating}{#1}}` for line references.

### Code form
- Under 30 lines. Lines short enough not to wrap in one column.
- Top-level functions, not class methods. Short function names.
- Short variable names (`vid`, `qty`).
- File-origin banner comment marks code from different files: `// ===== Models/Order.php =====`.
- Attacker-controlled input appears as `$_POST[...]` directly, so the source is visible.
- Real code, simplified for illustration. The caption states "slightly simplified".

### Comment form
- A comment supplies only what the code cannot show: a cross-layer guard, a runtime fact, a domain rule.
- No comment restates what the code already expresses.
- Comments occupy their own line above the code they annotate. No trailing inline comments that force wrapping.
- Challenge tags `// C1:`, `// C2:`, `// C3:` mark the code site of each challenge. One axis only. No TP/FP/FN tags in the snippet.

### Invariant line
- The invariant is a mathematical expression over domain logic variables: `// Invariant: amount == SUM(price_i * qty_i)`.
- Logic variables are application-independent. No code symbols in the invariant.

### Challenge sites
- Each challenge marks one code site, mapping 1:1 to introduction module 3.
- C1 (binding): one logic variable with two candidate code locations — the authoritative database value and the client value; binding to the client value is the false negative.
- C2 (coincidence): an equality that holds across every observed run yet encodes no rule.
- C3 (confirmation): a tamper that looks exploitable at one stage but a later-stage runtime guard neutralizes; confirmation needs the full workflow.

## Key Challenges and Solution Overview (2)

Lead with the core artifact the method builds. State why that artifact is decisive for this task.

Challenge narration (one per challenge, same order and vocabulary as introduction module 3):
- Phenomenon — what is hard, in one clause.
- Example — a specific location in the running snippet (line number).
- SOTA failure — name the tool and its exact failure on this example.

Close challenge narration with one sentence stating the method's core strategy.

Solution blocks (`2.2.1`, `2.2.2`, ...), 1:1 with challenges, same order:
- Name the core mechanism, italicized, reusing the introduction module-4 innovation name.
- Trace the mechanism over the running snippet.
- Reference one figure that illustrates the mechanism on the snippet.

Rules:
- Challenge count = solution count. Same order, same names as the introduction.
- Never rename a challenge or innovation introduced in the introduction.
- Each solution block carries one figure walking the mechanism over the snippet.
- Overview develops each challenge to line level; the introduction states it in one sentence.

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
