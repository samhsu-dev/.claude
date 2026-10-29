# Terminology and Communication Scope

Parameters `domain` and `terminology` are supplied by the project rule files under `rules/project/`; `glossary.path` comes from `rules/project/glossary.md`.

Rules governing the vocabulary used in all agent output. How a new term is named and how the glossary files are laid out: `rules/docs/glossary.md`.

---

## Scope

These rules bind every surface the agent writes, with no exception: chat replies, commit messages, documentation, code comments and docstrings, identifiers, log messages, figure titles and axis labels, and directory and file names.

## Domain

- Every technical term comes from the task domain or the repository vocabulary. The project may narrow the allowed domains through `domain.allowed`.
- Never borrow a term from an unrelated domain as a metaphor for a technical concept. Before writing a term, check that its source field belongs to the task domain or the repository vocabulary.
- Never coin a term, label, or metaphor the codebase does not already use. Selection of an existing source name follows `rules/docs/glossary.md` Name Sources and Naming Steps.
- Never translate a metaphor word for word across languages. The project parameter `terminology.substitutions` supplies forbidden words, replacements, scope and exemptions. `hooks/doc_check.py` reports them in written files.

## Established Terms

- The project glossary is the single registry of established terms. Its path is `glossary.path`; the default is `docs/glossary.md`.
- A concept the glossary names is referred to only by that name, in every output language alike.
- Glossary entry obligations and exemptions: `rules/docs/glossary.md` Selection.
- A new concept gets its glossary entry on first use, in the same change that introduces it.
- Until that procedure establishes a name, use an existing term or a plain clause.
- A term of the literature or of the domain and a core term of the algorithm never yield to readability: no common word or paraphrase replaces it. A reader is helped by its definition, its citation, or a clause beside it. A common word in its place reads as wrong to a reader of the field.
- One term names one concept, and one concept has one term, so a search for the term finds every use of the concept. An audit checks both directions.
- A term has one spelling, hyphenation included.
- An identifier is quoted as code, spelled exactly as in the source.
- The first use of a glossary term in a reply carries its definition in plain words.
- A project substitution may protect exact external identifiers. Keep their spelling and exclude their renaming from option lists.
- Question vocabulary follows `terminology.question_vocabulary` supplied by `rules/project/terminology.md`.

## Readability

- Naming serves readability. For a generic or coined word, when a rule and the reader's understanding pull apart, the reader wins. A literature, domain or core term keeps its name (Established Terms).
- A generic word whose meaning the context fixes is not split by the one-term rule and needs no question.
- A generic or coined abstract noun a reader new to the repository cannot parse without the glossary is replaced by a plain clause or the identifier; literature, domain and core terms follow Established Terms.
- After a change that renames or rewords terms, every changed sentence is reread in full. A sentence that reads stiffly, is ambiguous, or needs the glossary to parse is rewritten.

- Under `terminology.implementation_variants`, name compared implementations by their code names. Use its allowed category words and exclude its forbidden comparison labels.
