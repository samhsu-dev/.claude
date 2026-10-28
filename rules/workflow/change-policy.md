---
---

# Change Policy

Rules governing when and how the agent modifies code and public API.

---

- No guessing. Verify via documentation, source code, or test. If unverifiable, ask.
- A fix starts at the root cause: the fault is traced to the rule, mechanism or data that produces it, the design is reworked there, and one change solves every item that shares the cause. A check, branch, structure or special case added beside the cause to hide one symptom is rejected.
- Before a diff goes to review, each invariant the diff introduces or a finding names is checked at every site it governs: a search of the diff and its callers lists the sites, each site obeys the invariant or the diff changes it, and each kind of site has a test. The site list goes to the reviewer with the diff.
- A change keeps every capability: before it lands, it states its effect on correctness, precision, recall and cost, with the example, test or measurement that shows it. A change that lowers any of them goes to the user with that evidence.
- For configured algorithm phases, count added nodes, edges, walks or runtime in each phase and report the result on every reference example.

- Before changing or removing a component, read the code that implements it to establish the actual division of labor. Never infer responsibility from names, docstrings, or an adjacent doc sentence.
- Search for existing libraries before implementing.
- No backward-compatibility requirements.
- Return types, signatures, behavior and public API change only within user authorization or the agent authority assigned by `workflow/decisions.md`.
