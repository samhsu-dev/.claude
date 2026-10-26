# Decisions

Rules for deciding an open design item: who decides it, what a solution conforms to, how it is asked, and how it is recorded. Always active.

---

## Who Decides

- Every open item is triaged first: agent-decidable or user-decidable, with a one-clause reason.
- The user decides an item that touches a core principle of the algorithm: stretch, relax, the states STRETCHED and CONCRETE, the approximation order and its unknown top, the store version query, contexts, the join mechanism, or the division of work among the three phases.
- The user decides an item that exposes a design limitation: a PHP example whose `php` output every available option contradicts.
- The user decides an item that shows a large gap against prior work: a paper or tool that handles a case the design misses.
- The user decides an item whose solution lowers precision or recall on any PHP example, or raises the cost of a phase, against the current design.
- The agent decides every other item that has one clearly better design, including software interface design: public API shape, signatures, field names, result types.
- An agent decision revises a user decision only when the revision is local: it touches no core principle listed above, and a PHP example shows the revised sentence reports a result the `php` output contradicts, or the sentence it narrows is derived text. Its decision log entry names each revised decision with its commit. Every other revision of a user decision goes to the user.
- An item where only one option matches the `php` output on every example is agent-decidable, unless the item touches a core principle.
- A naming item whose options report identical results on every example is agent-decidable.
- A name read off an existing graph type identifier, as function entity off `ENTITY_FUNCTION`, is agent-decidable and applied without a question.
- A user question asks only the core choice in plain words, with one example; the mechanism details that follow from the choice are agent decisions.

## Solution Conformance

Every solution, an agent decision or an option offered to the user, passes each check:

- It is a rule of the three-phase algorithm and of the AST, PDG, ADG and CCG as the docs decide them. Phase 1 is intraprocedural with branch contexts; Phase 2 relaxes context-sensitively over the CCG from file entries; Phase 3 traverses with call and branch contexts.
- It reads data the graphs and the earlier phases already hold before it adds anything: an ADG edge (INHERIT_FROM, REFER_TO, ALIAS_OF, DEFINED_BY, RESOLVE_AS), a Phase 1 or Phase 2 result, a holder path.
- It extends an existing mechanism before it adds a node type, an edge type, a table or a walk. Example: builtin method lookup walks the INHERIT_FROM edges of builtin class entities (BP-1, 010b4423a), not a second walk over parents in the facts layer.
- No parallel structure: no second walk, cache, map or edge that restates a relation a graph already records.
- No side channel: no data passed outside the graphs and the decided algorithm data, such as a global flag, a string-keyed map beside a rule, or a lookup beside the mechanism.
- It fixes the root cause: the problem is traced to the phase rule, graph relation or mechanism that produces it, the design is rethought there, and one change solves every item with that cause. No patch: no special case for one builtin, one PHP construct or one test, and no edge, node or walk added beside the cause to cover one symptom.
- It loses no capability: on each PHP example it states what the analysis reports before and after, which shows precision and recall do not drop, and it states the nodes, edges, walks or run time it adds to each phase.
- A node is never modified after its creation.
- Its result on each PHP example matches PHP 8.5.11 output.
- A solution with a known limitation is preceded by a survey of the literature, tools, other fields and known algorithms for the same problem.
- Code is the lowest-confidence source. A difference between code and a decided doc is a code gap, never evidence against the doc.

## Before Asking

Every question to the user and every option list is preceded by these steps, in order:

1. Read the local decision log entries of every module the question touches (`docs/decisions/`, never committed), then the docs of every module the question touches and of every module whose facts an option reads or writes: `concept*.md`, `model*.md`, `spec*.md`, `design*.md`, and the glossary: `docs/glossary/glossary.md` and the `docs/glossary/glossary-*.md` file holding the entry of each concept the question touches (`grep -n "^### <term>" docs/glossary/glossary*.md`).
2. Search history for each concept the question names: `git log -S '<term>' --oneline -- docs/ <module>/src/` and `git log --grep='<term>' --oneline`.
3. Read the deleted text of every hit: `git show <commit>^:<path>`.
4. A decision found in steps 1-3 is cited with its decision log entry and commit and applied. It is never offered as an open option.
5. A premise taken from a conversation summary or from text marked "derived, not a user decision" is checked against the docs before use. Unchecked, it is no premise.
6. The question opens with a constraint list: every decision found in steps 1-3 that the options touch, each with its commit, and every edge case recorded for the topic, each with its example.
7. The question states which docs and commits were reviewed.
8. Each PHP construct an option treats differently, and each case a known limitation leaves out, is counted in the PHPCVEs corpus (release v2025.03, 258 projects; local copy `/Users/yichao/Projects/CobraPHP-Datasets/datasets/cves`): occurrences and projects. The question states the counts. PHPCVEs is a usage corpus here, never a scoring corpus: FT-1 scores on PHPTarpits only.

## Question Format

- Every question and every option list carries a minimal PHP example with its real `php` output, written out in readable multi-line form, never abbreviated.
- Each option states what the analysis reports on that example under the option, and its effect on precision, recall and the cost of each phase against the current design.
- Each option states either "keeps every decision" or the decision sentence it revises, with its commit.
- An option that revises a decision is recommended only when a PHP example shows the decision reports a result the `php` output contradicts.
- The option list ends with a discussion option and names one recommended option.

## Recording

- The decision log is the local record `docs/decisions/`. An entry holds the decision ID, user or agent, the question, the options, the choice, the reason, the PHP example with its output, the PHPCVEs counts with the counting method, the decisions it revises and every commit that records it. An open item is an entry with no choice yet, and the same entry takes the choice when it is decided.
- A user decision is written in the same turn it is made: its log entry, and the resulting rule into the committed doc of the affected module as current design.
- An agent decision is written into its log entry and its rule into the committed doc, and committed at once. Its log entry states "keeps every decision" or the revised decisions, the existing data or mechanism it reuses, and the rejected alternatives.
- A committed doc and a commit message carry no decision ID, no commit citation, and no "user decision", "agent decision", "revises" or "keeps every decision" marker. A doc states the rule; its reason stays only when a reader needs it to understand the design, as plain prose in the owning concept or model section. A commit message states what changed and why in plain words; the log entry maps the decision to the commit.
- An edge case raised in discussion is written with its PHP example into the Edge Cases section of the affected doc, or into the open decision entry while its rule is open, in the same turn it is raised.
- A new conformance rule triggers a review of every logged agent decision against it. A decision that fails is revised by a new agent decision, or goes to the user when Who Decides assigns it there.
