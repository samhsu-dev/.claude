---
name: define-term
description: Look up the accurate academic definition of a term in a specific field, using Wikipedia REST API and Semantic Scholar. Use when the user asks to define a technical or academic term.
allowed-tools:
  - WebFetch
  - Bash
argument-hint: "<term> [field]"
---

Look up the accurate academic definition of `$ARGUMENTS`.

Parse `$ARGUMENTS` as: first word(s) are the term, last word (if prefixed with `in:` or after a comma) is the field. If no field is given, infer from context or default to Computer Science.

## Step 1 — Wikipedia REST API

Fetch the Wikipedia summary for the term:

```
https://en.wikipedia.org/api/rest_v1/page/summary/<term-url-encoded>
```

Extract: `title`, `description`, `extract` (first 2-3 sentences). Note the `content_urls.desktop.page` link.

## Step 2 — Semantic Scholar

Search for the term in academic papers to find how it is formally defined in the literature:

```
https://api.semanticscholar.org/graph/v1/paper/search?query=<term+field>&fields=title,abstract,year,authors&limit=3
```

From the top results, extract the abstract sentences that directly define the term (look for patterns like "X is defined as", "X refers to", "we define X as", "X is a method/framework/algorithm that").

## Step 3 — Domain-specific source (when field is known)

| Field | Source |
|-------|--------|
| Security / Cryptography | `https://csrc.nist.gov/glossary/term/<term>` |
| Machine Learning | Check arXiv abstract via Semantic Scholar |
| General CS | Wikipedia + Semantic Scholar sufficient |

## Step 4 — Synthesize and Report

Output in this format:

**Term:** `<term>`
**Field:** `<field>`

**Definition:**
> One concise paragraph synthesizing the most accurate, consensus definition from sources above. Prioritize formal/academic phrasing over layman descriptions.

**Key distinctions:**
- Bullet points for any important nuances, edge cases, or common misconceptions.

**Sources:**
- Wikipedia: `<url>`
- Semantic Scholar: top paper title + year
- (NIST if applicable)

If sources conflict, note the conflict and explain which definition is more widely accepted and why.
