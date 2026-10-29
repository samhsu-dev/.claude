---
---

# Change Policy

Rules governing when and how the agent modifies code and public API.

---

- No guessing. Verify via documentation, source code, or test. If unverifiable, ask.
- A fix starts at the root cause: the fault is traced to the rule, mechanism or data that produces it, the design is reworked there, and one change solves every item that shares the cause. A check, branch, structure or special case added beside the cause to hide one symptom is rejected.
- Before a diff goes to review, each invariant the diff introduces or a finding names is checked at every site it governs: a search of the diff and its callers lists the sites, each site obeys the invariant or the diff changes it, and each kind of site has a test. The site list goes to the reviewer with the diff.
- A change keeps every capability of the branch it merges into: before it lands, it states its effect on correctness, precision, recall and cost against that branch, with the example, test or measurement that shows it. A change that lowers any of them goes to the user with that evidence; removing what the same branch added lowers none of them. Exception: a decided bound of zero added work never stops a chain session: it picks a representation that adds no work when one exists, and otherwise implements with the phase counts below, which reach the user after the merge.
- For configured algorithm phases, count added nodes, edges, walks or runtime in each phase and report the result on every reference example.

- Before changing or removing a component, read the code that implements it to establish the actual division of labor. Never infer responsibility from names, docstrings, or an adjacent doc sentence.
- Search for an existing library or standard command before implementing, and build no tool for what a standard command already does.
- A tool that serves only development, such as a document generator or a script, handles only the inputs the repository holds and stops with an error on any other input.
- No backward-compatibility requirements.
- Return types, signatures, behavior and public API change only within user authorization or the agent authority assigned by `workflow/decisions.md`.
