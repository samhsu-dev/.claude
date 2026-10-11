# Project Terminology

Forbidden substitutions of CobraPHP for the global `communication/terminology.md`. The project's naming decisions (name sources, naming steps, core terms, publication classes) live in `docs/glossary.md` Naming.

---

## Forbidden Substitutions

- The Phase 1 loop iteration cap (`MAX_LOOP_ITERATIONS`) is "iteration cap", never "widening". No widening operator is applied.
- The per-node visit cap (`MAX_NODE_VISITS`) is "liveness bound", never "lattice height".
- The graph in `graphs/pdg/` is "PDG", never "CPG". Exception: the `cpg` field of `TaintGraphs`.
- Comparing behavior with the PHP manual or php-src is "check against", never "adjudicate" or "裁定" (law).
- A phase-end user confirmation is "phase confirmation" or "阶段确认", never "门禁".
- One path out of an `if`, `switch`, `match`, ternary, or `try` is a "branch" ("分支"), never "arm". Exception: an external identifier quoted as code (PHP-Parser `MatchArm`, php-src `match_arm`) and the AST enum entries that copy PHP-Parser names (`STRU_MATCH_ARM`, `ARMS`, `ARM_CONDS`; kept by user decision 2026-10-09, `docs/graphs/ast/design-graph.md`). Never offer to rename them.
