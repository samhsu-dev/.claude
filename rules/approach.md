---
paths:
  - "**/approach.tex"
  - "**/approaches.tex"
---

# Approach Structure

## Section Order

| # | Block | Content |
|---|-------|---------|
| 1 | Opening | The approach name, the architecture figure, the stages in execution order |
| 2 | Core Artifact | The one data structure every stage reads or writes |
| 3 | Stage I..N | One subsection per stage, in execution order |

## Opening Block

- The first sentence names the approach and cites `\autoref{fig:architecture}`.
- The opening names the inputs and the representation the first stage consumes.
- One sentence lists the stages by name in execution order.
- The opening holds no stage detail.
- The architecture figure has width `\linewidth` and carries `\caption`, `\label{fig:architecture}`, and `\Description`.

## Core Artifact Block

- One subsection defines the core artifact: what it extends, and the one responsibility it has in every stage.
- It lists the parts of the artifact as an enumerated list, each named by its role.
- For each mechanism a later stage introduces, it gives a forward `\autoref` to that stage and no mechanism detail.

## Stage Subsections

- Title `Stage N: Name`, with a `\label` of the form `subsec:approach_<name>`.
- The first sentence states what the stage produces for the next stage.
- Each new element type the stage adds is introduced with `\emph{}` in exactly one stage. Later stages refer to it and never redefine it.
- Each new element is traced on the running example by line, with `\motivline{N}`, where it is introduced.
- The last sentence states what the next stage consumes from this stage's output.
- The stage names, their order, and the element names are identical in the opening, the architecture figure, and the subsections.

## Running Example

- One running example: the listing of the overview section (`lst:motivating`). Every stage refers to it by line number.

## Formal Definitions

- A formal definition precedes the algorithm that uses it.
- Base sets come before the object composed of them. One symbol per set; each set is stated by the program elements it models.
- After a formal definition, one instantiation on the running example maps each symbol to a line or a value.
- A formal object with a fixed structure is given in a table with `\caption` and `\label`, cited in the text.

## Subsubsections

- A stage with separable steps splits into subsubsections: the definitional subsubsection first, then the algorithmic ones in execution order.
- The first sentence of a subsubsection states its goal.
