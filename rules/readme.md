---
paths:
  - "**/README.md"
---

# README Standards

Audience: developers evaluating or using this library. Not maintainers, not contributors.

---

## Principle

Cognitive funnel: broadest to most specific. Each section is an exit point — readers stop when their question is answered. The developer decision flow: name → description → example → install → API → adopt.

A developer understands what the repo does within 10 seconds: title, one-line description, usage example.

---

## Required Sections

Sections in this order:

| # | Section | Content |
|---|---------|---------|
| 1 | **Title** | Project name. Matches package name. |
| 2 | **Name** | One-line blockquote (`>`) with name etymology or metaphor. |
| 3 | **Description** | One line, under 120 characters. Core functionality and idea — not how. |
| 4 | **Install** | Code block. Copy-paste-run. Include prerequisites when non-obvious. |
| 5 | **Usage** | Minimal working example in a code block. Simplest case first. |
| 6 | **API** | Exported functions/classes, signatures, parameters, return types. Link to full docs when extensive. |
| 7 | **License** | SPDX identifier. Always last. |

### Optional Sections

Insert between Usage and License. Include only when the README lacks context without them:

- **Background** — Motivation and context. When the problem or naming is non-obvious.
- **Contributing** — Link to `CONTRIBUTING.md` or one-line statement.
- **Badges** — Build status, version, coverage. No heading. After description, before install.
- **Documentation** — Links to `idea.md` (concepts) and `design.md` (architecture) when they exist. One link per doc, one-line description of what the reader finds there.
- **For Agents** — Link to `docs/llms.txt`. One line: "Agent-consumable documentation index at `docs/llms.txt` (llmstxt.org format)." Present when `docs/llms.txt` exists.
- **Experiments** — One sentence per experiment: what was tested and the outcome. No methodology, no analysis — link to the full write-up.

No table of contents.

---

## Format

- Code blocks for all commands, examples, and output. No prose descriptions of code.
- Two heading levels maximum (`#` and `##`).
- Hyperlink specialized terms, related projects, and external concepts.
- Code examples pass the project's own linter.
- No broken links.

---

## Rules

- Lead with the problem solved, not the implementation.
- One usage example visible without scrolling.
- Detailed docs, tutorials, and guides in separate files or docs site. README is a landing page, not a manual.
- No decorative content (banner images, animated GIFs, badge walls).
- No vague descriptions ("A utility library", "A tool for developers").
- Blockquote (`>`) only for the Name line. No blockquote elsewhere.
- No generic section names ("Miscellaneous", "Extra", "Other").
- Install section present even when trivial (single command).
