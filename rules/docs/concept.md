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
```
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

**Internal Processing Flow**
1. [Step name] — [what happens]
2. ...

### 4. Scenarios
- **Typical:** [normal operation]
- **Boundary:** [edge case]
- **Interaction:** [collaboration with other modules]

---

## Generation Rules

### Content
- Concepts only. No implementation details, APIs, commands, or code.
- No formal semantics (state transitions, invariants, edge direction rules) -- those go in `model.md`.
- Technical specifications link to `design.md`. Domain semantics link to `model.md`.

### Format
- Headings, bullet points, bold text, diagrams for structure.
- Paragraphs: 2–4 sentences.
- No modifiers, no redundancy.
- Audience: researchers and developers.

### Diagrams
- Module relationships and data flow.
- One diagram per interaction boundary.

### Scenarios
- One typical, one boundary, one interaction case minimum.
- Consistent terminology with Section 2.
