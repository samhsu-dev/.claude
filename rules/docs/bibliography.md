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

Glossary field relations: `rules/docs/glossary.md` Entry.

---

Zotero, Better BibTeX and collection-specific procedures apply only when that bibliography workflow is configured. Otherwise use the repository's existing bibliography workflow; a missing collection creates no export or library-setup task.

## File

- One bibliography per repository, in BibLaTeX syntax. `bibliography.path` defaults to `docs/references.bib`.
- Use Better BibTeX auto-export with the Better BibLaTeX translator for `bibliography.collection` in its configured library. Edit sources in Zotero, never in the export.
- One item per source. A source cited twice is one item cited twice.
- A paper item holds authors, title, venue, year, pages, and DOI, checked against the DOI registry.
- A tool, a reference implementation, a manual, or a documentation site is a Computer Program or Document item. Its Version field holds the pinned repository commit or the documentation version; a Document item, which has no Version field, holds it as a `tex.version:` line in Extra, which Better BibTeX exports as `version`. Its URL holds the repository or the site. The pin lives only here.
- A tool or reference implementation hosted as a GitHub repository has the repository's `owner/repo` full name, as GitHub spells it today, as its Title: `<owner>/<repo>`. The Zotero Title wraps the name in `<span class="nocase">…</span>`. Its URL is that repository. A documentation site or a specification keeps the document's own title.
- No `urldate`, `abstract`, or other access date in the export.
- The auto-export is registered through the Better BibTeX JSON-RPC method `autoexport.add`, and a one-off export runs through `item.export`.
- Paper key: the key Better BibTeX generates with the formula `auth.lower + "_" + shorttitle(1, 0).lower.condense("_") + "_" + year`: `author_title_year`. Software and manual key: the project's own name in lowercase, pinned in the item's native Citation Key field, never a `Citation Key:` line in Extra.
- A key is never renamed. A source replaced by another gets a new key.

## Citation

- Pandoc syntax: `[@key]`; a locator after a comma: `[@key, sec. 3.2]`, `[@key, p. 37]`, `[@key, def. 3]`; several sources: `[@a; @b]`.
- A code symbol follows the key of its software entry: `` [@tool] `process` ``. A manual section or a documentation page title is the quoted suffix: `[@manual, "Configuration"]`.
- A citing document never writes a source in prose beside its key: no authors, title, venue, version, URL, directory path, or line number.
- Every key resolves in the bibliography. `hooks/doc_check.py` reports a key that does not; `pandoc --citeproc` reports it as `citation <key> not found`.
