---
paths:
  - "**/*.prompty"
  - "**/prompts/**"
---

# Prompt Construction Standards

Rules for authoring LLM-agent prompts. Sources: Anthropic prompt-engineering docs, OpenAI GPT-4.1 prompting guide, and structural patterns from autonomous agents (Strix, PentAGI, CAI, PentestGPT, XBOW, Big Sleep).

---

## Section Taxonomy and Order

One prompt = these sections, in this order. Omit a section only when it has no content.

| # | Section | Content | Excluded content |
|---|---------|---------|------------------|
| 1 | Role / Objective | Persona + one-line goal | Rules, data, examples |
| 2 | Task | Stage goal in one sentence | Constraints, output shape |
| 3 | Constraints | High-priority rules, grouped | Examples, output schema, data |
| 4 | Exclusions | What to reject, stated positively as "treat X as Y" | Selection rules |
| 5 | Priority / Tie-break | Ranking and disambiguation order | Hard constraints |
| 6 | Reasoning | Induced planning step — non-reasoning models only | Any content on native-thinking models |
| 7 | Output Format | Response contract: fields, value domains, abstain path | Task restatement |
| 8 | Examples | 3–5 few-shot demonstrations in XML tags | Novel rules not stated above |
| 9 | Context / Data | Long input data, wrapped in XML tags | Instructions |
| 10 | Final | Restate single most important rule; anchor query last | New rules |

- Data block placement: long input data goes in section 9, above the anchored query, never before the instructions.
- For prompts over 20k tokens: mirror the highest-priority constraint at both top and bottom.

## Constraints

- Constraints sit in section 3, adjacent to the task, before examples and output format.
- Group constraints into few hierarchical blocks. Never a flat list of many imperative lines.
- Maximum attention degrades past ~20 instructions. Split excess rules across pipeline stages, not into one prompt.
- No per-line emphasis inflation ("CRITICAL", "MUST", "ALWAYS"). Emphatic inflation lowers adherence.
- Highest-priority rules first within each block. Middle-of-prompt rules receive least attention.

## Output Contract

- State the output shape inside the prompt. Never rely solely on an out-of-band parsed schema.
- Every field the parsed schema reads is described in the Output Format section. Every field the prompt promises is read by the schema. No field on one side only.
- Strict structured output uses Structured Outputs or tool-calling with an enum. No assistant prefill (deprecated Claude 4.6+).
- Phrase the contract positively: state the target shape, not forbidden shapes.

## Reasoning

- Induce a brief planning step only when the model is non-reasoning.
- No hand-scripted reasoning steps and no forced reasoning field on native-thinking models.
- "think" is a sensitive trigger token on recent Opus. No emphatic reasoning directives.

## Examples

- Few-shot examples follow the instructions, never precede them.
- 3–5 examples, diverse, each wrapped in `<example>` tags; group under `<examples>`.
- Include one abstain / negative example when the task has an abstain path.
- Concrete tokens in examples are illustrative. No merchant-specific or caller-specific token baked into a constraint as if it were a general rule.

## Multi-Stage Consistency

- All stages share one identical system preamble: role, scope, XML tag taxonomy, output conventions.
- All stages use the same section order and the same section labels. One concept = one label across every stage.
- Stage N tags its output; stage N+1 consumes those tags verbatim. Tag names are identical across stages.
- Recall stage: wide net, bounded top-k, "include anything plausibly relevant, do not filter." A candidate dropped here is unrecoverable.
- Precision stage: verify strictly, abstain on doubt. Emit `{decision, confidence, abstain_reason}`.
- Confidence is a ranking signal, not a calibrated probability. Threshold it on a held-out set. Route abstain to review, never to a forced decision.
- A stage's prompt states only that stage's job. No precision/ranking bias in a recall prompt. No value-selection a downstream solver owns.

## Terminology

- One concept, one term, across all stage prompts. No synonym drift (no `EXCLUDE` in one stage and `out_of_scope` in another for the same act).
- A coined or domain-specific term gets a one-clause definition at first use.
- Common programming terms (array access, property access, DB query) receive no definition.
- A domain rule appearing in two stages is stated once in the shared preamble, not copied per stage.

## Anti-Patterns

- Instruction stacking: many flat imperative lines diluting attention. Group or split.
- Taxonomy drift: same concept under different labels across stages.
- Schema decoupling: prompt and parsed schema describe different fields.
- Rule duplication: one rule hard-coded in multiple stage files. Source it once.
- Hidden prompt: an LLM call whose prompt is an inline code string, not a prompt carrier file. Every LLM call's prompt lives in a carrier.
- Hollow contract: a documented output field the prompt never requests and the schema never parses.

## AI-Agent Structural Patterns

- Forced-action loop: every agent turn carries exactly one tool call (Strix, PentAGI).
- Explore-then-validate: a separate verifier or PoC gate confirms a finding before it surfaces. The strongest false-positive defense is architectural, not prompt wording (XBOW, Big Sleep).
- Report-gated output: findings exist only via a structured report tool requiring evidence fields.
- Tool output is untrusted data, not authority. Re-validate it; never act on it as ground truth (CAI).
