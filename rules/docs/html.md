---
paths:
  - "**/*.html"
---

# HTML Document Standards

Constraints on a standalone HTML page whose purpose is to be read. Rendering procedure: `render-doc` skill.

## Self-Containment

- One file. All CSS in one `<style>` element.
- No external fetch. No font CDN, no stylesheet link, no remote script, no remote image.
- Images embed as `data:` URIs.
- A typeface the reader may not have is named first in a stack ending in a system face.

## Typography

| Property | Value |
|---|---|
| Body size | 19px. Never below 16px |
| Line spacing | 1.5 to 1.6 unitless at that size |
| Measure | 45 to 90 characters. 66 to 72 is the target |
| Families | Two. One serif for prose, one sans for labels |
| Capitalised labels | 10 to 14 percent letterspacing, under one line |

- Bold and italic mark one word or phrase. Never combined.
- Emphasis comes from position and heading level, not from bold runs in body text.

## Colour

- One primary colour carries structure, headings, and links.
- Accent colours distinguish a labelled state. They hold under a fifth of total colour.
- Body and heading text clear WCAG 2.1 AA: 4.5:1 for normal text, 3:1 for large text, in every colour scheme the page declares.
- A page declaring dark mode overrides both `prefers-color-scheme: dark` and `:root[data-theme]` in both directions.

## Tables

- Rule above the header, rule below the header, rule at the foot.
- No vertical rules. No cell fill. No zebra striping.
- Numeric columns right-aligned with tabular figures.
- Every table sits inside an `overflow-x: auto` container. The page body never scrolls horizontally.

## Prohibitions

These are the recognised markers of machine-generated design.

- No purple or violet gradient. No cyan-on-dark. No gradient text.
- No grid of uniform rounded cards. No coloured left border on a card. No icon-heading-blurb triple.
- No oversized hero. No centred badge above the title. No stat banner.
- No emoji. No icon font. No decorative SVG.
- No third typeface for accent. No serif italic as a decorative device.
- No animation, scroll effect, or hover transform.
- No `Conclusion`, `Summary`, `Key Takeaways`, or `Getting Started` section absent from the source.

## Derived Pages

- A page rendered from a Markdown source is derived. The Markdown is authoritative.
- A content correction is made in the source and the page re-rendered. Never edited in the page alone.
- Quotations, numbers, identifiers, and paths carry over verbatim. Rewriting applies to connective prose only.
