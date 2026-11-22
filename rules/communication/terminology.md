# Terminology and Communication Scope

How a new term is named and how the glossary files are laid out: `rules/docs/glossary.md`.

---

## Scope

These rules bind every surface the agent writes: chat replies, briefs to agents, agent reports and results, review findings, decision questions and refutations, commit messages, documentation, code comments and docstrings, identifiers, log messages, figure titles and axis labels, and directory and file names.

## Domain

- Take every technical term from a domain `domain.allowed` lists, or, without that value, from computer science (security analysis included) and the repository vocabulary; write the rest of agent text in ordinary words, and spell each established term as its glossary entry spells it.
- Name a technical concept by its technical term or a plain clause; use the words of its own domain, with no metaphor from an unrelated domain.
- Use the terms, labels and metaphors the codebase already uses; select an existing source name under `rules/docs/glossary.md` Name Sources and Naming Steps.
- Translate a term across languages by its meaning. The project parameter `terminology.substitutions` supplies forbidden words, replacements, scope and exemptions. `hooks/doc_check.py` reports each use of a forbidden word outside its exemptions in written files. A substitution marked `check: review` applies only where the text is about its subject; review checks it and the hook skips it.

## Established Terms

- The project glossary is the single registry of established terms. Its path is `glossary.path`; the default is `docs/glossary.md`. A project with documentation has one; its first documentation change creates it. A brief to another agent names that path.
- A concept the glossary names is referred to only by that name, spelled as its entry spells it, in every output language, heading and table alike, in place of any synonym, abbreviation or paraphrase. A concept a dependency repository defines keeps the name its owning glossary gives it (`rules/docs/glossary.md` Repositories).
- A new concept gets its glossary entry in the change that first uses it; which concepts get one follows `rules/docs/glossary.md` Selection.
- Until that procedure establishes a name, use an existing term or a plain clause.
- Keep a term of the literature or of the domain and a core term of the algorithm under its name, and add a definition, a citation or a clause beside it for readability.
- One term names one concept, and one concept has one term, in prose and in domain identifiers alike. An identifier differs from the term only by the casing its language requires; a protected external name keeps its spelling, its glossary entry maps it to the term, and an option list keeps its name. A terminology audit checks both directions: each term names one concept, and each concept has one term.
- A term has one spelling, hyphenation included.
- An identifier is quoted as code, spelled exactly as in the source.
- Under `terminology.implementation_variants`, name compared implementations by their code names. Use its allowed category words and exclude its forbidden comparison labels.
- The first use of a glossary term in each chat reply to the user carries its definition in plain words.
- A question to the user uses only the vocabularies `terminology.question_vocabulary` lists.

## Readability

- For a generic or coined word, when a rule and the reader's understanding pull apart, the reader wins. A literature, domain or core term keeps its name (Established Terms).
- A generic word whose meaning the context fixes is not split by the one-term rule and needs no question.
- A generic or coined abstract noun a reader new to the repository cannot parse without the glossary is replaced by a plain clause or the identifier.
- After a change that renames or rewords terms, the agent rereads every changed sentence in full and rewrites each one that has two readings or that a reader new to the repository cannot parse without the glossary.
