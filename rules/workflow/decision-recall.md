# Decision Recall

Rules for recovering recorded decisions before asking the user. Always active.

---

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

- Every question and every option list carries a minimal PHP example with its real `php` output.
- Each option states what the analysis reports on that example under the option.
- Each option states either "keeps every decision" or the decision sentence it revises, with its commit.
- An option that revises a decision is recommended only when a PHP example shows the decision reports a result the `php` output contradicts.

## Recording

- A user decision is written into the committed doc of the affected module in the same turn it is made, marked as a user decision with its decision ID. The doc carries no date; the commit that records the decision identifies it.
- An edge case raised in discussion is written with its PHP example into the Edge Cases section of the affected doc, or into the module's `*.todo.md` while its rule is open, in the same turn it is raised.
- A decided design the code does not implement stays in the docs as an open gap. Never delete design text because no caller exists.
- A doc audit that removes a mechanism's text names the replacing doc section in its commit body.
