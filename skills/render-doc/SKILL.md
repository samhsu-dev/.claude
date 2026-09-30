---
name: render-doc
description: Render a Markdown document as a self-contained editorial HTML page. Use when the user asks to convert a doc to HTML, produce a readable or printable version, or reduce the LLM-generated look of a written page.
allowed-tools: Read, Write, Edit, Glob, Bash
argument-hint: [path/to/doc.md]
---

Render `$1` as a self-contained HTML page in the editorial design system below. The Markdown stays authoritative. The HTML is a derived rendering and is regenerated, never edited in place as the source of truth.

## Step 1 — Read the source

1. Read the full Markdown file. No excerpt, no search shortcut. Structure decisions in Step 3 depend on the whole document.
2. Record the document's own repeated shapes: a claim-and-citation pair, a verdict line, a metrics table, a step sequence. These become semantic blocks, not styled paragraphs.
3. Resolve the output path: same directory, same basename, `.html` extension, unless the user names one.

## Step 2 — Fix the shell

Write one file with `<!doctype html>`, a `<title>` matching the document title, `<meta charset>` and `<meta name="viewport">`, and one `<style>` element holding the whole stylesheet.

Inline `${CLAUDE_SKILL_DIR}/assets/document.css` into that `<style>` element. Read it and paste it. The page fetches nothing: no font CDN, no stylesheet link, no script, no remote image. Embed any image as a `data:` URI.

Wrap the body content in `<article class="page">`.

## Step 3 — Map Markdown onto semantic blocks

The page reads as a technical report, in the register of institutional reference documentation: plain declarative sentences, imperative mood for anything the reader must do, numbered sections, and admonition boxes for what must not be missed.

| Source shape | Rendered as |
|---|---|
| `#` title | `.masthead`: `.org` mark and lab name, `.doctype` label, plain `h1` |
| Provenance, scope, inputs, method | `dl.meta`, a definition-list table of labelled facts |
| What the reader must know before reading | `.admonition` titled `Read this first`, directly under the meta table |
| Section list | `nav.toc` with numbered entries. Floats left of the text column above 1280px, sits inline below it |
| `##` section | `h2` with `<span class="n">` section number |
| `###` subsection carrying an identifier | `h3` with `<span class="n">` number and a trailing `.code-tag` for the identifier and row count |
| A quoted source set against a quoted response | `figure.exhibit`, numbered `Exhibit N` in the `figcaption` beside the row identifier, one `.voice` block per speaker |
| A verdict, judgment, or check on a preceding claim | `.admonition` with `result-confirmed`, `result-refuted`, or `result-narrowed`, the outcome named in the title |
| Table | `.table-block` with a numbered `.caption`, `table` inside `.scroll`, numeric cells `.num`, key column `.k` |
| Closing caveat | `p.closing` |

Cross-references in prose use section numbers, never "above" or "below". Every table and exhibit carries a number and is referenced by it.

Every block in the table above already exists in the stylesheet. Adding a new visual treatment means adding a rule, and a new rule is justified only by a shape the document repeats at least twice.

## Step 3a — Source links and syntax highlighting

1. A repository path in the source becomes `<a class="src" href="vscode://file/<absolute-path>">` so the reader opens it in the editor. Link only paths that exist on disk. A path into an ephemeral checkout stays plain text, and the meta table states why.
2. Tag inline and block code with `class="language-js|ts|py|sh"` where the language is known.
3. After writing the page, run `node ${CLAUDE_SKILL_DIR}/scripts/highlight.mjs <output.html>`. It rewrites tagged code into `.tok-*` spans at render time, so the page ships no script. It is idempotent and reports the block count.

## Step 4 — Strip the generated-text tells

The rendering is the moment to remove templated prose. Rewrite, never delete content.

| Tell | Replacement |
|---|---|
| `Example is X. Their side: ... Our side: ...` | The `figure.exhibit` block, with the row identifier as the caption and each side labelled |
| A paragraph opening with a fixed word such as `Double-check.` or `Note.` | The `.check` block, with the label carried by `.verdict` |
| A heading that restates the section it sits in | The distinguishing half only |
| Bold runs used to mark importance | Position and heading level |
| Emoji, icons, decorative dividers | Removed |

Preserve every quotation verbatim. Preserve every number, identifier, file path, and cross-reference exactly. Rewriting applies to connective prose only.

## Step 5 — Verify

1. Read `~/.claude/rules/docs/html.md` and check the output against every constraint and every prohibition it lists. It carries the typographic constants, the contrast floor, and the machine-generated-design prohibitions.
2. `grep -c 'https\?://' <output>` counts only in-document links. Any font, script, or stylesheet host is a failure.
3. Read the file end to end against the source. Every heading, table row, quotation, and link is present.
4. Confirm the palette, the two families, and the measure are the stylesheet's own. A per-document override means Step 2 was not followed.

## Design system

Palette and typefaces come from the Johns Hopkins visual identity, in its post-2025 open-source form. The stylesheet in `assets/` already encodes them, along with the constants the rule file requires.

| Role | Value |
|---|---|
| Structure, headings, links | Heritage Blue `#002d72` |
| Body text | Sable-toned ink `#1c1a17` |
| Labelled states | Spirit Blue `#68ace5`, Homewood Green `#008767`, Dark Red `#a6192e`, Sand `#cba052` |
| Prose and headings | Source Serif 4, falling back to Charter then Georgia |
| Labels, eyebrows, table text | Work Sans, falling back to system-ui |

The typographic constants trace to Butterick's Practical Typography and the GOV.UK Design System. The table convention is booktabs.

## Rules

- One source file, one output file. Never split a rendering across pages.
- The Markdown is authoritative. A content correction is made in the Markdown and the page re-rendered.
- Never invent content to fill a layout. A block with no source material is removed, not padded.
- Never edit `assets/document.css` to accommodate one document. Per-document deviation means the design system is wrong or the document is.
