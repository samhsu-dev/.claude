---
paths:
  - "introduction.tex"
  - "intro.tex"
---

# Introduction Structure

Standards: Peyton Jones, *How to Write a Great Research Paper*; Gopen & Swan.

---

## Opening Paragraph

- The subject of the first substantive sentence is the paper's central artifact or domain, matching the title's primary noun.
- No technology, language, or tool appears as the grammatical subject of the opening unless the paper's title names it.
- Define the central artifact or domain in the first paragraph before introducing any property, vulnerability class, or detection concept that depends on it.
- A concrete real-world incident appears before the formal definition it motivates, not after.

## Defining a Problem Class

- Define a vulnerability or bug class by its observable symptom (what the application does that it should not), not by reference to a detection abstraction (invariant, oracle, rule) that has not yet been introduced.
- A detection abstraction (invariant, oracle, rule) is a researcher-constructed tool concept. It is not an inherent property of the domain. Never define a vulnerability class as "violating an invariant" before explaining that invariants are a researcher-imposed abstraction for detection.
- The correct order: (1) describe the observable symptom, (2) note that prior work models this symptom as violation of a domain rule, (3) introduce the abstraction with its source made explicit.

## Logical Ordering

- Every term used in a definition appears in running text before the definition that depends on it.
- A challenge or problem statement names only concepts introduced in the preceding paragraph.
- Prior work's framing of a problem is attributed to prior work, not presented as ground truth about the domain.
