---
paths:
  - "**/README.md"
---

# README Standards

Audience: developers evaluating or using the product. Not maintainers, not contributors.

---

## Principle

---

## Required Sections

Sections in this order:

| # | Section | Content |
|---|---------|---------|
| 1 | **Title** | Project name, spelled as the build's root project name. |
| 2 | **Badges** | Badge lines directly under the title, above the Name line, no heading. Show build or coverage, language and runtime version, release, last commit, package (JitPack), repository size and license. Versions match the repository's current release. A README that has badges keeps them; a rewrite never removes them. |
| 3 | **Name** | One-line blockquote (`>`) with name etymology or metaphor. |
| 4 | **Description** | One line, under 120 characters. Core functionality and idea — not how. |
| 5 | **Install** | Code block. Copy-paste-run. List every prerequisite the install command needs. |
| 6 | **Usage** | Minimal working example in a code block. Simplest case first. |
| 7 | **API** | Exported functions/classes, signatures, parameters, return types. Link to the full API docs when they exist. |
| 8 | **Citation** | When `readme.citation_required` is true; format below. |
| 9 | **License** | License section below. Always last. |

### Optional Sections

Optional sections follow the last required section before License, in table order. Include each section below only under the condition it states:

- **Background** — Motivation and context. When the project name or its problem is not stated in the Description section.
- **Contributing** — Link to `CONTRIBUTING.md` or one-line statement.
- **Documentation** — Links to `concept.md` (concepts) and `design.md` (architecture) when they exist. One link per doc, one-line description of what the reader finds there.
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

## License

- License section states `readme.license`, the repository's SPDX identifier, and links to its `LICENSE` file.

## Citation

- When `readme.citation_required` is true, the section holds the associated work's BibTeX in a fenced `bibtex` block and `readme.citation_request`.
- When `readme.work_status` is not `published`, the BibTeX is `readme.citation_placeholder`; on publication its fields are replaced.

## Rules

- One usage example visible without scrolling.
- Detailed docs, tutorials, and guides in separate files or docs site. README is a landing page, not a manual.
- No decorative images (banner images, animated GIFs). Status badges are not decorative.
- No vague descriptions ("A utility library", "A tool for developers").
- Blockquote (`>`) only for the Name line. No blockquote elsewhere.
- No generic section names ("Miscellaneous", "Extra", "Other").

- When citation is required, include `readme.citation_request`.
