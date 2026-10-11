# Project Terminology

Project parameters for the global `communication/terminology.md`. The policy — domain test, name-source ranks, naming steps, registration — lives there and is not restated here.

---

## Glossary

- `docs/glossary.md` Naming records the naming decisions cited below with their dates.
- PHP keywords need no glossary entry.

## Name Sources

- Rank 2 is the PHP manual. Rank 3 is php-src (user decision 2026-10-11, `docs/glossary.md` Name Sources).

## Naming Steps

- The head noun is the graph element: an AST, PDG, ADG or CCG node or edge, a label, or a datum of the algorithm (user decision 2026-10-11, 87bd7a879).
- A value is classified by the program point at which PHP obtains it (user decision 2026-10-11, 87bd7a879, `docs/glossary.md` Naming Steps).

## Core Terms

- The core terms are STRETCHED, CONCRETE, UNKNOWN, stretch, and relax (user decision 2026-10-02, `docs/glossary.md` Core Terms).
- The algorithm's own data are named from the core terms: relax memo, relax component (user decision 2026-10-11, TQ18, 129474c19).
- The publication classes are the outer stretch node and the inner stretch node of the COBRA paper (Xu et al., ICSE 2026, §3.2), the top classes of STRETCHED values (user decision 2026-10-11, e16f1f78c).

## Forbidden Substitutions

- The Phase 1 loop iteration cap (`MAX_LOOP_ITERATIONS`) is "iteration cap", never "widening". No widening operator is applied.
- The per-node visit cap (`MAX_NODE_VISITS`) is "liveness bound", never "lattice height".
- The graph in `graphs/pdg/` is "PDG", never "CPG". Exception: the `cpg` field of `TaintGraphs`.
- Comparing behavior with the PHP manual or php-src is "check against", never "adjudicate" or "裁定" (law).
- A phase-end user confirmation is "phase confirmation" or "阶段确认", never "门禁".
- One path out of an `if`, `switch`, `match`, ternary, or `try` is a "branch" ("分支"), never "arm". Exception: an external identifier quoted as code (PHP-Parser `MatchArm`, php-src `match_arm`) and the AST enum entries that copy PHP-Parser names (`STRU_MATCH_ARM`, `ARMS`, `ARM_CONDS`; kept by user decision 2026-10-09, `docs/graphs/ast/design-graph.md`). Never offer to rename them.
