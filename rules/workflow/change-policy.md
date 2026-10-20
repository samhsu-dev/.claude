---
---

# Change Policy

Rules governing when and how the agent modifies code and public API.

---

- No guessing. Verify via documentation, source code, or test. If unverifiable, ask.
- A fix starts at the root cause: the fault is traced to the rule, mechanism or data that produces it, the design is reworked there, and one change solves every item that shares the cause. A check, branch, structure or special case added beside the cause to hide one symptom is rejected.
- A change keeps every capability: before it lands, it states its effect on correctness, precision, recall and cost, with the example, test or measurement that shows it. A change that lowers correctness, precision or recall, or raises cost, goes to the user with that evidence.
- Before changing or removing a component, read the code that implements it to establish the actual division of labor. Never infer responsibility from names, docstrings, or an adjacent doc sentence.
- Search for existing libraries before implementing.
- No backward-compatibility requirements.
- No changes to return types, signatures, or behavior without explicit user request.
- No additions, removals, or renames of public API without explicit instruction.
- A project decision rule may assign software interface design to the agent.
