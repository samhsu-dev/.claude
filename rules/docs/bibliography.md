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

- One bibliography per repository: `docs/references.bib`, in BibLaTeX syntax. The glossary routing file names it and the Zotero collection it is exported from.
- The bibliography is a Better BibTeX auto-export (Better BibLaTeX translator) of the project's Zotero collection. It is never edited by hand: a source is added or changed as a Zotero item in that collection.
- One item per source. A source cited twice is one item cited twice.
- A paper item holds authors, title, venue, year, pages, and DOI, checked against the DOI registry.
- A tool, a reference implementation, a manual, or a documentation site is a Computer Program or Document item. Its Version field holds the pinned repository commit or the documentation version; its URL holds the repository or the site. The pin lives only here.
- No `urldate`, `abstract`, or other access date in the export. A commit of the bibliography fixes when a pin was checked.
- The auto-export is registered through the Better BibTeX JSON-RPC method `autoexport.add`, and a one-off export runs through `item.export`; neither needs the Zotero window.
- Paper key: the key Better BibTeX generates with the formula `auth.lower + "_" + shorttitle(1, 0).lower.condense("_") + "_" + year`: `horwitz_interprocedural_1990`. Software and manual key: the project's own name in lowercase, pinned by a `Citation Key:` line in the item's Extra field: `joern`, `php-src`, `php-manual`.
- A key is never renamed. A source replaced by another gets a new key.

## Citation

- Pandoc syntax: `[@key]`; a locator after a comma: `[@key, sec. 3.2]`, `[@key, p. 37]`, `[@key, def. 3]`; several sources: `[@a; @b]`.
- A code symbol follows the key of its software entry: `` [@joern] `CfgCreator.run` ``. A manual section or a documentation page title is the quoted suffix: `[@php-manual, "Variable scope"]`.
- A citing document never writes a source in prose beside its key: no authors, title, venue, version, URL, directory path, or line number.
- Every key resolves in the bibliography. `hooks/doc_check.py` reports a key that does not; `pandoc --citeproc` reports it as `citation <key> not found`.
