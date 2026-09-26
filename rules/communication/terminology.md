# Project Terminology

Extends global `communication/terminology.md`, which sets the scope and the
domain test. This file names the established vocabulary of this repository:
the second of the two sources a term may come from.

---

## Established Terms

- `docs/glossary.md` is the single table of established terms. Each entry is defined by the code that implements it. Use it exactly.
- A concept the glossary names is referred to only by that name, in English and Chinese output alike.

## Forbidden Substitutions

- The Phase 1 loop iteration cap (`MAX_LOOP_ITERATIONS`) is "iteration cap", never "widening". No widening operator is applied.
- The per-node visit cap (`MAX_NODE_VISITS`) is "liveness bound", never "lattice height".
- The graph in `graphs/pdg/` is "PDG", never "CPG". Exception: the `cpg` field of `TaintGraphs`.
- Comparing behavior with the PHP manual or php-src is "check against", never "adjudicate" or "裁定" (law).
- A phase-end user confirmation is "phase confirmation" or "阶段确认", never "门禁".

## Registration

- A term absent from `docs/glossary.md`, from the code, and from the data files is not established. Use the plain CS term.
- A genuinely new concept is added to `docs/glossary.md` on first use, defined from the code that implements it.
