---
paths:
  - "docs/glossary/*.md"
  - "docs/references.bib"
---

# Project Glossary Parameters

CobraPHP's parameters to the global `rules/docs/glossary.md` and `rules/docs/bibliography.md`. Each parameter cites the commit that recorded it. The glossary files in `docs/` state none of this and never cite this file.

---

## Location

- The glossary lives in `docs/glossary/`: the routing file `docs/glossary/glossary.md` and the entry files `docs/glossary/glossary-<concern>.md` (9781dd7c0).

## Name Sources

- Rank 2 is the PHP manual and rank 3 is php-src (d4e77cbcd).
- An entry also names, when one exists, a paper from 2015 or later and an industrial tool that use the same concept (817d50841).
- A paper published after the COBRA paper is never a name source; an entry cites it as similar at most (TQ5b, 67043c2d6).
- PHP keywords need no entry (1ef0b5641).

## Naming Steps

- The head noun is the graph element: an AST, PDG, ADG or CCG node or edge, a label, or a datum of the algorithm (87bd7a879).
- A value is classified by the program point at which PHP obtains it: the result of an operation at an AST expression, or a value where several definitions meet, at a branch merge, a loop header, a weak-update write, a function entry or a call site (87bd7a879).

## Core Terms

- The core terms are the states STRETCHED, CONCRETE and UNKNOWN, and stretch and relax (9f324846a).
- The algorithm's own data are named from them, as relax memo and relax component (129474c19).
- A literature name for what a value stands for, such as actual-out, serves as its role noun.

## Top Classes

- The two classes of the COBRA paper (Xu et al., ICSE 2026, §3.2), the outer and the inner stretch node, are the top classes of STRETCHED values (e16f1f78c).
- A value at a function entry or a call site is an outer stretch node; every other STRETCHED value is an inner stretch node.

## Layers

- The glossary files form eight layers, read in this order: architecture; infrastructure, that is graph storage, export, settings and dispatch; the PHP language model; one schema file per graph with its node types, edge types and attributes; the core algorithm; analysis semantics by concern; the procedure of each phase; facts and taint (e6de435be).
- A node type, an edge type or an attribute goes to its graph's schema file, a rule for writing graph edges to infrastructure, a step of one phase to that phase's procedure file. Any other entry goes to the file of the concern its Definition states, whatever graph element its Is a names (be325acce).

## Bibliography

- `docs/references.bib` is the Better BibLaTeX auto-export of the Zotero collection CobraPHP Docs in the group library jhu-seclab-cobra (groupID 4886325, local libraryID 3) and is never edited by hand (30f5ba1f0).
- A paper key is the key Better BibTeX generates, as `horwitz_interprocedural_1990`. A tool key is the project name pinned in the item's Extra field, as `php-src` (30f5ba1f0).
