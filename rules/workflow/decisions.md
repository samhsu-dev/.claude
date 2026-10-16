# Decisions

Rules for deciding an open design item: who decides it, what a solution conforms to, how it is asked, and how it is recorded. Always active.

---

## Who Decides

- Every open item is triaged first: agent-decidable or user-decidable, with a one-clause reason.
- The user decides an item that touches a core principle of the algorithm: stretch, relax, the states STRETCHED, CONCRETE and UNKNOWN, the store version query, contexts, the join mechanism, or the division of work among the three phases.
- The user decides an item that exposes a design limitation: a PHP example whose `php` output every available option contradicts.
- The user decides an item that shows a large gap against prior work: a paper or tool that handles a case the design misses.
- The agent decides every other item that has one clearly better design, including software interface design: public API shape, signatures, field names, result types.
- An agent decision never revises a user decision. An item whose answer revises one goes to the user.

## Solution Conformance

Every solution, an agent decision or an option offered to the user, passes each check:

- It is a rule of the three-phase algorithm and of the AST, PDG, ADG and CCG as the docs decide them. Phase 1 is intraprocedural with branch contexts; Phase 2 relaxes context-sensitively over the CCG from file entries; Phase 3 traverses with call and branch contexts.
- It reads data the graphs and the earlier phases already hold before it adds anything: an ADG edge (INHERIT_FROM, REFER_TO, ALIAS_OF, DEFINED_BY, RESOLVE_AS), a Phase 1 or Phase 2 result, a holder path.
- It extends an existing mechanism before it adds a node type, an edge type, a table or a walk. Example: builtin method lookup walks the INHERIT_FROM edges of builtin class entities (BP-1, 010b4423a), not a second walk over parents in the facts layer.
- No parallel structure: no second walk, cache, map or edge that restates a relation a graph already records.
- No side channel: no data passed outside the graphs and the decided algorithm data, such as a global flag, a string-keyed map beside a rule, or a lookup beside the mechanism.
- No patch: no special case for one builtin, one PHP construct or one test; one mechanism per class of problem.
- A node is never modified after its creation.
- Its result on each PHP example matches PHP 8.5.11 output.
- A solution with a known limitation is preceded by a survey of the literature, tools, other fields and known algorithms for the same problem.
- Code is the lowest-confidence source. A difference between code and a decided doc is a code gap, never evidence against the doc.

## Before Asking

Every question to the user and every option list is preceded by these steps, in order:

1. Read the docs of every module the question touches and of every module whose facts an option reads or writes: `concept*.md`, `model*.md`, `spec*.md`, `design*.md`, and the glossary: `docs/glossary/glossary.md` and the `docs/glossary/glossary-*.md` file holding the entry of each concept the question touches (`grep -n "^### <term>" docs/glossary/glossary*.md`).
2. Search history for each concept the question names: `git log -S '<term>' --oneline -- docs/ <module>/src/` and `git log --grep='<term>' --oneline`.
3. Read the deleted text of every hit: `git show <commit>^:<path>`.
4. A decision found in steps 1-3 is cited with its file or commit and applied. It is never offered as an open option.
5. A premise taken from a conversation summary or from text marked "derived, not a user decision" is checked against the docs before use. Unchecked, it is no premise.
6. The question opens with a constraint list: every decision found in steps 1-3 that the options touch, each with its commit, and every edge case recorded for the topic, each with its example.
7. The question states which docs and commits were reviewed.

## Question Format

- Every question and every option list carries a minimal PHP example with its real `php` output, written out in readable multi-line form, never abbreviated.
- Each option states what the analysis reports on that example under the option.
- Each option states either "keeps every decision" or the decision sentence it revises, with its commit.
- An option that revises a decision is recommended only when a PHP example shows the decision reports a result the `php` output contradicts.
- The option list ends with a discussion option and names one recommended option.
- A question uses only CS terms and glossary terms.

## Recording

- A user decision is written into the committed doc of the affected module in the same turn it is made, marked as a user decision with its decision ID. The doc carries no date; the commit that records the decision identifies it.
- An agent decision is written into the committed doc of the affected module with its decision ID and committed at once. Its commit body marks it "agent decision", states "keeps every decision", names the existing data or mechanism it reuses, and lists the rejected alternatives.
- An edge case raised in discussion is written with its PHP example into the Edge Cases section of the affected doc, or into the module's `*.todo.md` while its rule is open, in the same turn it is raised.
- A decided design the code does not implement stays in the docs as an open gap. Never delete design text because no caller exists.
- A doc audit that removes a mechanism's text names the replacing doc section in its commit body.
- A new conformance rule triggers a review of every recorded agent decision against it. A decision that fails is revised by a new agent decision, or goes to the user when Who Decides assigns it there.
