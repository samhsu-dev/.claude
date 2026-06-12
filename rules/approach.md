---
paths:
  - "**/approach.tex"
  - "**/approaches.tex"
---

# Approach Structure

One core artifact carries the whole section. The artifact is built once, then every phase reads and enriches it. One running example, introduced in the overview's motivating snippet, is reused for every phase. The reader holds one data structure and one example across the whole section.

---

## Section Order

| # | Block | Function |
|---|-------|----------|
| 1 | Opening | Name the approach, point to the architecture figure, trace the pipeline as one preprocessing step plus N phases |
| 2 | Core Artifact | Define the one data structure every phase reads and writes |
| 3 | Phase I..N | One subsection per phase, in execution order |

## Opening Block

- One sentence: the approach name and a pointer to the architecture figure (`\autoref{fig:architecture}`).
- One preprocessing step that turns raw input into the structural representation every phase consumes. Name the representation.
- One sentence listing the N phases by name, in execution order, stating that each adds nodes and edges to the core artifact.
- Architecture figure spans `\linewidth`, has `\caption`, `\label{fig:architecture}`, and `\Description`.
- No phase detail in the opening. The opening is a map.

## Core Artifact Block

- One subsection defining the artifact every phase reads and enriches.
- State what the artifact extends or builds on, and the one responsibility it owns across all phases.
- List the artifact's internal structures as an enumerated set, each named by the role it plays.
- State which phase introduces each later mechanism, with a forward `Section~\ref` to that phase. No mechanism detail here.

## Phase Subsections

One subsection per phase, in execution order. Each phase:

- Carries a `\label{subsec:approach_phase_N}` referenced by earlier forward pointers.
- Opens on its goal in one sentence: what this phase produces for the next phase.
- Names every new node type and edge type it adds to the core artifact, each introduced with the italic term macro.
- Traces each new element over the running example by line number (`\motivline{...}`).
- Closes by stating what the next phase consumes from this phase's output.

Rules:
- Phase count in the body equals the phase count named in the opening. Same names, same order.
- A node or edge type is introduced in exactly one phase. Later phases reference it, never redefine it.
- Each new element is shown on the running example at the point of introduction.

## Formal Definitions

- A phase that defines a formal object states the definition before its algorithm.
- Definition order: base sets first, then the composed object built from them.
- State each set by the program elements it models. One symbol per set.
- After the formal definition, instantiate it once on the running example, mapping each symbol to a concrete line or value.
- Formal objects with fixed structure go in a table with `\caption` and `\label`. The prose references the table.

## Subsubsection Order

A phase splits into subsubsections when it has separable steps. Within a phase:

- Definitional subsubsection first: name and define the objects the phase operates on.
- Algorithmic subsubsections next, in execution order.
- Each subsubsection states its goal in the first sentence.
- A subsubsection that introduces an edge type defines the edge, then shows it on the running example.

## Invariants

- One core artifact named in the opening and built before Phase I. Every phase reads and writes it.
- One running example, the same snippet the overview introduced. Every phase refers to it by line number.
- Each phase's output is the next phase's input. State the handoff explicitly at each phase boundary.
- Phase names, node names, and edge names are identical across the opening, the figure, and the body.
- Forward references point to the phase that introduces a mechanism. Every forward reference resolves to a `\label`.
