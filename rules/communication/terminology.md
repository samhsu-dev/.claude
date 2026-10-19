# Terminology and Communication Scope

Rules governing the vocabulary used in all agent output. Always active. How a new term is named and how the glossary files are laid out: `rules/docs/glossary.md`.

---

## Scope

These rules bind every surface the agent writes, with no exception: chat replies, commit messages, documentation, code comments and docstrings, identifiers, log messages, figure titles and axis labels, and directory and file names.

## Domain

- Every technical term comes from computer science or security, or from the repository's own established vocabulary. There is no third source.
- Never borrow a term from an unrelated domain — gaming, biology, finance, sports, medicine, clinical trial design, military, law — as a metaphor for a technical concept. Domain-of-origin test before writing any term: name the field it comes from. Not CS, not security, not this repository → replace it.
- Never coin a term, label, or metaphor the codebase does not already use.
- A term exists to ease communication. Before a term is introduced or kept, ask what a reader loses when it is replaced by the elements it is made of, an existing name, or a plain clause. Nothing → no term. A new noun bundling several existing things is the typical failure. Necessity is checked before a name is sourced.
- A shorthand written to shorten a sentence never becomes a term.
- A concept the literature names keeps that name. A coined word for it is replaced by the literature term, with its source.
- Two named variants of one system under comparison are its implementations, named by what the code calls them (backend, strategy, implementation). Never "arm", "condition", "treatment", or "control" — those name a trial design, not a program.
- Never translate a metaphor word for word across languages. A project's forbidden substitutions live in the Forbidden Substitutions section of its project `communication/terminology.md`, one bullet each, the forbidden words quoted after "never". `hooks/doc_check.py` reports them in written files.

## Established Terms

- The project glossary is the single registry of established terms: `docs/glossary.md` and the `docs/glossary-*.md` files it routes to. Exception: a project rule names another path when the project keeps its glossary elsewhere.
- A concept the glossary names is referred to only by that name, in every output language alike.
- Every domain term in output has a glossary entry. General programming words (function, variable, class, loop, exception, call) need none. An identifier quoted as code needs an entry when it names a domain concept.
- A new concept gets its glossary entry on first use, in the same change that introduces it.
- A term absent from the glossary, the code, and the data files is not established. Use the plain CS or security term.
- A term of the literature or of the domain (abstract interpretation, lattice, strong update, taint, sanitizer, slice, context sensitivity) and a core term of the algorithm never yield to readability: no common word or paraphrase replaces it. A reader is helped by its definition, its citation, or a clause beside it. A common word in its place reads as wrong to a reader of the field.
- One term names one concept, and one concept has one term, so a search for the term finds every use of the concept. An audit checks both directions.
- A term has one spelling, hyphenation included.
- An identifier is quoted as code, spelled exactly as in the source.
- The first use of a glossary term in a reply carries its definition in plain words.
- A new term is named by the Name Sources and Naming Steps in `rules/docs/glossary.md`, read before the name is chosen.

## Readability

- Every naming rule serves readability; one term per concept is a means to it. For a generic or coined word, when a rule and the reader's understanding pull apart, the reader wins. A literature, domain or core term keeps its name (Established Terms).
- A generic word whose meaning the context fixes is not split by the one-term rule and needs no question.
- An abstract noun a reader new to the repository cannot parse without the glossary ("containment") is replaced by a plain clause or the identifier.
- After a change that renames or rewords terms, every changed sentence is reread in full. A sentence that reads stiffly, is ambiguous, or needs the glossary to parse is rewritten.
