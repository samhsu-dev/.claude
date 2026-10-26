# Project Terminology

Forbidden substitutions of CobraPHP for the global `communication/terminology.md`. The project glossary is `docs/glossary/glossary.md` and the `docs/glossary/glossary-*.md` files it routes to. The project's naming decisions (name sources, naming steps, core terms, top classes, layers) live in `.claude/rules/docs/glossary.md`. Bibliography parameters live in `.claude/rules/docs/bibliography.md`.

---

## Forbidden Substitutions

- The Phase 1 loop iteration cap (`MAX_LOOP_ITERATIONS`) is "iteration cap", never "widening". Exception: "widening operator" names the operator of [@cousot] that the design does not apply; a doc may state that no widening operator is applied.
- The per-node visit cap (`MAX_NODE_VISITS`) is "liveness bound", never "lattice height".
- The graph in `graphs/pdg/` is "PDG", never "CPG".
- Comparing behavior with the PHP manual or php-src is "check against", never "adjudicate" or "裁定" (law).
- A phase-end user confirmation is "phase confirmation" or "阶段确认", never "门禁".
- One path out of an `if`, `switch`, `match`, ternary, or `try` is a "branch" ("分支"), never "arm". Exception: an external identifier quoted as code (PHP-Parser `MatchArm`, php-src `match_arm`) and the AST enum entries that copy PHP-Parser names (`STRU_MATCH_ARM`, `ARMS`, `ARM_CONDS`; kept by user decision 951342447, `docs/graphs/ast/design-graph.md`). Never offer to rename them.
- A list of tasks is a task doc in `docs/todo/`, never "backlog".
- What Phase 2 does to a STRETCHED value is "relax", never "settle". Exception: "| settle | Relax" (retired-names row).
- The relation a `CCG_FUNC_CONTAIN` or `CONTAIN_*` edge records is a plain clause, a function's body holds its call sites, or the identifier, never "containment". Exception: "| containment, for a" (retired-names row).

## Domain

- Every technical term comes from computer science or security, or from the repository's own established vocabulary. There is no third source.
- Two named variants of one system under comparison are its implementations, named by what the code calls them (backend, strategy, implementation). Never "arm", "condition", "treatment", or "control" — those name a trial design, not a program.

## Decision Questions

- A question uses only CS terms and glossary terms.
