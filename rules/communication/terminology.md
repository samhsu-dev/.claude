# Terminology and Communication Scope

Rules governing the vocabulary used in all agent output. Always active. The layout of the glossary files: `rules/docs/glossary.md`.

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

## Name Sources

A concept takes the name the highest-ranked source gives that same concept:

1. A name widely accepted in the literature.
2. The reference manual or standard of the language or system the project analyzes or implements.
3. The reference implementation of that language or system.
4. A name several tools in the field use.
5. The repository's own name.
6. A name only one tool uses.

- Ranks 2 and 3 apply when the project analyzes or implements a language or system. The glossary routing file names them.
- A source counts only where its word names the same concept. The same word for another concept is a clash, never a name source.
- A candidate name that already names another glossary concept is reported to the user with both entries.
- A borrowed word with no literature source in its glossary entry is a coined term.
- A rename question cites the rank and the source of every candidate name.

## Naming Steps

A new term is named in three steps, in order:

1. **Locate.** The structure the term belongs to — the model, graph, or table, and the element kind within it — gives the head noun.
2. **Classify.** The semantics of the analyzed system fixes the term's locus: for a value in program analysis, the program point at which the language produces it.
3. **Name.** The name is the locus plus one role noun taken by Name Sources.

- The terms of one locus share one role noun.
- A state or attribute recorded on the element stays out of the element's name.
- An umbrella term names only a class with a behavior of its own.
- A project with a central algorithm declares its core terms in the glossary routing file: the names of the algorithm and its states. Core terms keep their names. A literature name for the same mechanism is cited in the entry as its method or as a similar concept, never used as the name. A literature name for what a value stands for serves as the role noun.
- A class named in the project's own publication stays a class in the glossary. It never becomes the name of one implementation element.
