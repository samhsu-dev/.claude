---
paths:
  - "**/idea.md"
---

# IDEA Standards (Concepts & Terminology)

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
- **Name:** [identifier]
- **Definition:** [what it is and why it matters]
- **Scope:** [includes/excludes]
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
- Concepts and terminology only. No implementation details, APIs, commands, or code.
- Technical specifications link to `design.md`.
- Consistent terminology across modules.

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
