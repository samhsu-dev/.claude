# Terminology and Communication Scope

Rules governing the vocabulary used in all agent output. Always active. How a new term is named and how the glossary files are laid out: `rules/docs/glossary.md`.

---

## Scope

These rules bind every surface the agent writes, with no exception: chat replies, commit messages, documentation, code comments and docstrings, identifiers, log messages, figure titles and axis labels, and directory and file names.

## Domain

- Every technical term comes from computer science or security, or from the repository's own established vocabulary. There is no third source.
- Never borrow a term from an unrelated domain — gaming, biology, finance, sports, medicine, clinical trial design, military, law — as a metaphor for a technical concept. Domain-of-origin test before writing any term: name the field it comes from. Not CS, not security, not this repository → replace it.
- Never coin a term, label, or metaphor the codebase does not already use.
- Two named variants of one system under comparison are its implementations, named by what the code calls them (backend, strategy, implementation). Never "arm", "condition", "treatment", or "control" — those name a trial design, not a program.
- Never translate a metaphor word for word across languages. A project's forbidden substitutions live in its project `communication/terminology.md`.

## Established Terms

- The project glossary is the single registry of established terms: `docs/glossary.md` and the `docs/glossary-*.md` files it routes to. Exception: a project rule names another path when the project keeps its glossary elsewhere.
- A concept the glossary names is referred to only by that name, in every output language alike.
- Every domain term in output has a glossary entry. General programming words (function, variable, class, loop, exception, call) need none. An identifier quoted as code needs an entry when it names a domain concept.
- A new concept gets its glossary entry on first use, in the same change that introduces it.
- A term absent from the glossary, the code, and the data files is not established. Use the plain CS or security term.
- One term names one concept, and one concept has one term. An audit checks both directions.
- A term has one spelling, hyphenation included.
- An identifier is quoted as code, spelled exactly as in the source.
- The first use of a glossary term in a reply carries its definition in plain words.
- A new term is named by the Name Sources and Naming Steps in `rules/docs/glossary.md`, read before the name is chosen.
