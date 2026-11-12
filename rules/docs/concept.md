---
paths:
  - "**/concept.md"
  - "**/concept-*.md"
---

# Concept Standards

## Required Sections

### 1. Context

**Problem Statement** — Core problem in 2–3 sentences.

**System Role** — One sentence: module's position in the architecture.

**Data Flow**

- **Inputs:** [concept names from upstream modules]
- **Outputs:** [concept names to downstream modules]
- **Connections:** [upstream] → [this module] → [downstream]

**Scope Boundaries**

- **Owned:** [responsibilities this module manages]
- **Not Owned:** [explicitly out of scope]

### 2. Concepts

**Conceptual Diagram**

```text
[Module interactions]
```

**Core Concepts** — One entry per concept:

- **Name:** [term, linked to its glossary entry]
- **Role:** [why this module needs the concept, one sentence]
- **Scope:** [includes/excludes within this module]
- **Relationships:** [connections to other concepts]

### 3. Contracts & Flow

**Data Contracts**

- **With [Module A]:** [data exchanged, shared terminology]

**Internal Processing Flow** — Link the algorithm owner under `rules/docs/documentation.md` Ownership; describe only module interactions here.

### 4. Scenarios

At least one of each:

- **Typical:** [normal operation]
- **Boundary:** [edge case]
- **Interaction:** [collaboration with other modules]

### 5. Rationale and Rejected Alternatives

Optional. One entry per design choice the module rests on:

- **Choice:** [why this concept or mechanism, one or two sentences]
- **Rejected:** [each alternative and why it was rejected]

No open question lives here; an undecided point goes to the Open Gaps section of `design.md`.

---

## Generation Rules

### Content

- Concepts only. No implementation details, APIs, commands, or code.
- Content boundaries and links follow `rules/docs/documentation.md` Ownership.

### Format

- Headings, bullet points, bold text, diagrams for structure.
- Paragraphs: 2–4 sentences.
- No modifiers such as "properly", "easily", "simply", "just"; no redundancy.
- Audience: researchers and developers.

### Diagrams

- Module relationships and data flow.
- One diagram per interaction boundary.
