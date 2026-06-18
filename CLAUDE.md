# Project Rules

LaTeX academic paper project (BELUGA). This file is the project interface: structure, rule index, skills, and build system.

## Project Structure

```
paper/
├── main.tex                  # Root document
├── references.bib            # Hand-maintained bibliography
├── zotero-references.bib     # Zotero-exported bibliography
├── Sections/                 # One .tex file per section
├── Packages/
│   ├── local.tex             # Project macros, constants, terminology
│   ├── packages.tex          # Package loader (inputs all Packages/*.tex)
│   ├── codes.tex             # Code listing configuration
│   ├── formats.tex           # Page and float formatting
│   └── revision.tex          # Revision markup commands
├── Assets/                   # Figures and tables
├── Templates/                # Venue templates
├── Revisions/                # Reviewer-response material
└── .claude/
    ├── CLAUDE.md             # This file
    ├── rules/                # Rule files (see Rules below)
    └── skills/               # Project-specific skills (see Skills below)
```

## Rules

`.claude/rules/` holds the project rules. `paths:` frontmatter scopes a rule to matching files; no `paths:` means always active.

| Rule | Scope | Purpose |
|------|-------|---------|
| `writing.md` | `**/*.tex` | Academic prose: opening, structure, contributions, claims, register, punctuation |
| `codequality.md` | `**/*.tex`, `**/*.bib`, `**/*.sty`, `**/*.cls` | LaTeX source quality: formatting, labels, citations, figures, tables |
| `approach.md` | `**/approach.tex`, `**/approaches.tex` | Approach section structure |
| `committing.md` | always active | Project-specific commit and push rules (extends global) |

Global rules in `~/.claude/rules/` provide language-agnostic defaults. Project rules add LaTeX-specific guidance and override globals where both set a concrete value.

## Macros (`Packages/local.tex`)

All project-wide constants and terminology live in `local.tex`, organized into sections:

| Section | Contents |
|---------|----------|
| System names | `\sys`, `\datasetRepo`, `\strix`, `\cobra` |
| Argument structure | `\chalOne`, `\chalTwo`, `\approachName` — challenge and approach names; change once, propagates everywhere |
| Background data | `\phpEcomShare` — PHP market share with derivation comments |
| Evaluation data | Corpus, detection pool, coverage, precision, headline results |
| Linked terminology | `\ecomInvariant`, `\invOracle`, `\semanticVar`, `\invSemantics` — each has a `\termDef{}` hook for the definition anchor |

To rename a challenge or the overall approach, edit only the corresponding macro in Section 3 of `local.tex`.

## Skills

Project-specific skills in `.claude/skills/`. Invoke with `/skill-name [arguments]`.

| Skill | Command | Purpose |
|-------|---------|---------|
| `define-term` | `/define-term <term> [in:<field>]` | Look up the accurate academic definition of a CS/academic term |
| `zotero-research` | `/zotero-research <topic>` | Survey, curate, and enrich the Zotero library for a research topic |
| `review-section` | `/review-section <file.tex> [subsection]` | Review a LaTeX section for logic, argumentation rigor, and writing standards |
| `check-sentence` | `/check-sentence <"sentence" or L42-L48> [file.tex]` | Check sentences for logical validity, sentence-to-sentence coherence, and reviewer-rejection risk (strong declarations, scope overreach, causal overclaims) |

**Examples:**
```
/define-term invariant in:program verification
/zotero-research e-commerce logic vulnerability detection
/review-section Sections/introduction.tex
/review-section Sections/overall.tex motivation
```

## Build System

- Engine: `pdflatex`, `xelatex`, or `lualatex`.
- Build tool: `latexmk -pdf` (recommended).
- Multi-pass sequence: `pdflatex` → `bibtex` → `pdflatex` → `pdflatex`. `latexmk` automates this.
- Bibliography: `bibtex` with venue `.bst`.
- Clean: `latexmk -C`.
