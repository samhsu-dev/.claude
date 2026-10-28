---
paths:
  - "docs/glossary/*.md"
---

# Project Glossary Parameters

CobraPHP glossary parameters. Each naming parameter cites the commit that recorded it.

---

## Name Sources

- Rank 2 is the PHP manual and rank 3 is php-src (d4e77cbcd).
- An entry also names, when one exists, a paper from 2015 or later and an industrial tool that use the same concept (817d50841).
- A paper published after the COBRA paper is never a name source; an entry cites it as similar at most (TQ5b, 67043c2d6).
- An entry's Tools lines check Joern's CPG schema, php2cpg and dataflowengineoss for the same or a similar concept: `ENTITY_FILE` is similar to the php2cpg `<global>` method (9f4643959).

## Naming Steps

Parameters for the ordered Locate, Classify and Name steps in the global glossary rule:

- The head noun is the graph element: an AST, PDG, ADG or CCG node or edge, a label, or a datum of the algorithm (87bd7a879).
- A value is classified by the program point at which PHP obtains it: the result of an operation at an AST expression, or a value where several definitions meet, at a branch merge, a loop header, a weak-update write, a function entry or a call site (87bd7a879).

## Core Terms

- The core terms are the states STRETCHED and CONCRETE, and stretch and relax (9f324846a; UNKNOWN left State by user decision U5-1, 868bdbfa1, and is the adjective "unknown" by U5-3, 6fdee1389).
- The algorithm's own data are named from them, as relax memo and relax component (129474c19).
- The literature terms the algorithm borrows, held to the same rule as core terms: abstract value, approximation order, store version, join, label, backward slice.

## Top Classes

- The two classes of the COBRA paper (Xu et al., ICSE 2026, §3.2), the outer and the inner stretch node, are the top classes of STRETCHED values (e16f1f78c).
- A value at a function entry or a call site is an outer stretch node; every other STRETCHED value is an inner stretch node.

## Layers

- The glossary files form eight layers, read in this order: architecture; infrastructure, that is graph storage, export, settings and dispatch; the PHP language model; one schema file per graph with its node types, edge types and attributes; the core algorithm; analysis semantics by concern; the procedure of each phase; facts and taint (e6de435be).

## Entry

- Operation headings: Fork, Collapse, Relax, Freeze (N6 A, 190b2683c). PHP property heading: Early-bound (TQ2, e4eaac226).
