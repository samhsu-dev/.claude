---
paths:
  - "**/*.bib"
  - "**/glossary.md"
  - "**/glossary-*.md"
  - "**/concept.md"
  - "**/concept-*.md"
  - "**/model.md"
  - "**/model-*.md"
  - "**/spec.md"
  - "**/spec-*.md"
  - "**/design.md"
  - "**/design-*.md"
  - "**/impl.md"
  - "**/impl-*.md"
---

# Bibliography Standards

Every paper, manual, reference implementation, and tool a document cites is one entry of the repository's bibliography, cited by key in Pandoc citation syntax, the syntax Pandoc citeproc, MyST, and Quarto share. How a glossary entry uses citations: `rules/docs/glossary.md` Entry.

---

## File

- One bibliography per repository: `docs/references.bib`, in BibLaTeX syntax. The glossary routing file names it.
- One entry per source. A source cited twice is one entry cited twice.
- A paper entry holds authors, title, venue, year, pages, and DOI, checked against the DOI registry.
- A tool, a reference implementation, a manual, or a documentation site is a `@software` or `@manual` entry. `version` holds the pinned repository commit or the documentation version; `url` holds the repository or the site. The pin lives only here.
- No `urldate` and no other access date. A commit of the bibliography fixes when a pin was checked.
- Paper key: first author's family name, year, first title word that is not an article, lowercase ASCII: `xu2026cobra`, `horwitz1990interprocedural`. Software and manual key: the project's own name in lowercase: `joern`, `php-src`, `php-manual`.
- A key is never renamed. A source replaced by another gets a new key.
- Entries are sorted by key.

## Citation

- Pandoc syntax: `[@key]`; a locator after a comma: `[@key, sec. 3.2]`, `[@key, p. 37]`, `[@key, def. 3]`; several sources: `[@a; @b]`.
- A code symbol follows the key of its software entry: `` [@joern] `CfgCreator.run` ``. A manual section or a documentation page title is the quoted suffix: `[@php-manual, "Variable scope"]`.
- A citing document never writes a source in prose beside its key: no authors, title, venue, version, URL, directory path, or line number.
- Every key resolves in the bibliography. `hooks/doc_check.py` reports a key that does not; `pandoc --citeproc` reports it as `citation <key> not found`.
