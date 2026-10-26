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

Shared bibliography storage and citation syntax. Glossary field relations: `rules/docs/glossary.md` Entry.

---

## File

- One bibliography per repository: `docs/references.bib`, in BibLaTeX syntax. The glossary routing file names it and the Zotero collection it is exported from.
- The bibliography is a Better BibTeX auto-export (Better BibLaTeX translator) of the project's Zotero collection. It is never edited by hand: a source is added or changed as a Zotero item in that collection.
- One item per source. A source cited twice is one item cited twice.
- A paper item holds authors, title, venue, year, pages, and DOI, checked against the DOI registry.
- A tool, a reference implementation, a manual, or a documentation site is a Computer Program or Document item. Its Version field holds the pinned repository commit or the documentation version; a Document item, which has no Version field, holds it as a `tex.version:` line in Extra, which Better BibTeX exports as `version`. Its URL holds the repository or the site. The pin lives only here.
- A tool or reference implementation hosted as a GitHub repository has the repository's `owner/repo` full name, as GitHub spells it today, as its Title: `<owner>/<repo>`. The Zotero Title wraps the name in `<span class="nocase">…</span>`, so Better BibTeX exports it as typed instead of title-casing it (`<ExactRepositoryName>`). Its URL is that repository. A documentation site or a specification keeps the document's own title.
- No `urldate`, `abstract`, or other access date in the export. A commit of the bibliography fixes when a pin was checked.
- The auto-export is registered through the Better BibTeX JSON-RPC method `autoexport.add`, and a one-off export runs through `item.export`; neither needs the Zotero window.
- Paper key: the key Better BibTeX generates with the formula `auth.lower + "_" + shorttitle(1, 0).lower.condense("_") + "_" + year`: `author_title_2026`. A generated key holding a character a Pandoc citation key does not allow (anything but letters, digits, `_` and the internal punctuation `:.#$%&-+?<>~/`) is set in the item's native Citation Key field with that character removed, before the key is first committed: `a^2agent` becomes `a2agent`. Software and manual key: the project's own name in lowercase, set in the item's native Citation Key field (Better BibTeX 9 ignores an Extra `Citation Key:` line): `tool`, `runtime`, `manual`.
- A key is never renamed. A source replaced by another gets a new key.

## Citation

- Pandoc syntax: `[@key]`; a locator after a comma: `[@key, sec. 3.2]`, `[@key, p. 37]`, `[@key, def. 3]`; several sources: `[@a; @b]`.
- A code symbol follows the key of its software entry: `` [@tool] `process` ``. A manual section or a documentation page title is the quoted suffix: `[@manual, "Configuration"]`.
- A citing document never writes a source in prose beside its key: no authors, title, venue, version, URL, directory path, or line number.
- Every key resolves in the bibliography. `hooks/doc_check.py` reports a key that does not; `pandoc --citeproc` reports it as `citation <key> not found`.
