---
---

# Change Policy

Rules governing when and how the agent modifies code and public API.

---

- No guessing. Verify via documentation, source code, or test. If unverifiable, ask.
- Before changing or removing a component, read the code that implements it to establish the actual division of labor. Never infer responsibility from names, docstrings, or an adjacent doc sentence.
- Search for existing libraries before implementing.
- No backward-compatibility requirements.
- No changes to return types, signatures, or behavior without explicit user request.
- No additions, removals, or renames of public API without explicit instruction.
