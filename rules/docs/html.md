---
paths:
  - "**/*.html"
---

# HTML Document Standards

Rendering procedure: `render-doc` skill.

## Self-Containment

- One file. All CSS in one `<style>` element.
- The page loads every resource from the file itself: fonts, styles, scripts and images are inline, with no font CDN, stylesheet link, remote script or remote image.
- Images embed as `data:` URIs.
- A typeface the reader may not have is named first in a stack ending in a system face.

## Typography

| Property | Value |
|---|---|
| Body size | 19px; 16 to 19px at viewport widths up to 640px; 16px minimum |
| Line spacing | 1.5 to 1.6 unitless at that size |
| Measure | 45 to 90 characters. 66 to 72 is the target |
| Families | Two. One serif for prose, one sans for labels |
| Capitalised labels | 10 to 14 percent letterspacing, under one line |

- Bold and italic each mark one word or phrase, and a phrase carries at most one of them.
- Emphasis comes from position and heading level, not from bold runs in body text.

## Colour

- One primary colour carries structure, headings, and links.
- Accent colours distinguish a labelled state. They hold under a fifth of total colour.
- Body and heading text clear WCAG 2.1 AA: 4.5:1 for normal text, 3:1 for large text, in every colour scheme the page declares.
- A page declaring dark mode defines its colors for `:root[data-theme="dark"]` and `:root[data-theme="light"]`, and the `data-theme` value wins over `prefers-color-scheme`.

## Tables

- Horizontal rules only: above the header, below the header and at the foot; cells keep the page background.
- Numeric columns right-aligned with tabular figures.
- Every table sits inside an `overflow-x: auto` container. The page body never scrolls horizontally.

## Decoration

- Fill text and backgrounds with flat colours from Colour above; leave out purple or violet gradients, cyan text on dark backgrounds and gradient text.
- Lay out content as prose, headings, lists and tables; leave out grids of uniform rounded cards, coloured left borders on cards and icon-heading-blurb triples.
- Start the page with its title and then the source text; leave out oversized heroes, centred badges above the title and stat banners.
- Mark meaning with text; leave out emoji, icon fonts and decorative SVG.
- Set all text in the two families of Typography; leave out a third accent typeface and serif italic used as decoration.
- Keep the page static: leave out animation, scroll effects and hover transforms.
- Render the sections the source holds and only those, so a `Conclusion`, `Summary`, `Key Takeaways` or `Getting Started` section appears only when the source has it.

## Derived Pages

- A page rendered from a Markdown source is derived. The Markdown is authoritative.
- Make a content correction in the source and re-render the page from it.
- Quotations, numbers, identifiers, and paths carry over verbatim. Rewriting applies to connective prose only.
