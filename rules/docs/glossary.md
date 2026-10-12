---
paths:
  - "**/glossary.md"
  - "**/glossary-*.md"
---

# Glossary Standards

The registry of a project's established terms: how a new term is named and how the registry is laid out. Which terms output may use: `communication/terminology.md`.

---

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

## Files

- `glossary.md` is the routing file. Every other glossary file is `glossary-<concern>.md` in the same directory, one concern per file.
- The routing file holds, in order: the project's naming decisions (its rank 2 and rank 3 name sources, its naming-step parameters, its core terms, its top classes, its layers, each with its commit), the conventions shared by every glossary file (Source path prefix, bibliography path), the routing table, and the retired-names table. It holds no entry. Pinned versions live in the bibliography (`rules/docs/bibliography.md`).
- Routing table columns: File, Concern. Routing table order is reading order. A term is found by its heading: `grep -n "^### <term>" <dir>/glossary*.md`.
- Retired-names table columns: Retired, Successor, Commit. One row per rename or removal.
- A glossary file is at most 200 lines. A file past 200 lines splits by concern and the routing table gains a row.

## Layers

- The glossary files form layers, read from the general to the specific. Default order: architecture (modules, phases); infrastructure (storage, input and output, settings, dispatch); the model of the analyzed language or system; one schema file per data structure (a graph, a model, a table) with its element types and their attributes; the core algorithm; analysis semantics, one file per concern; the procedure of each phase; outputs (facts, reports). The routing file names the project's layers and the commit that fixed them.
- An entry goes to the file of the structure its Is a names. An attribute of an element goes to the schema file of that element's structure. A rule for writing a structure goes to infrastructure. A phase step goes to that phase's procedure file.
- A file holds no entry whose Is a names a structure another file owns.

## Entry

One entry per term: an H3 heading followed by fields in this order.

```markdown
### <Long form> (<ABBREVIATION>)
- **Is a:** <parent entry or element kind>
- **Definition:** <one to three sentences>
- **Example:** `<minimal input>` → <the term's instance in it>
- **Source:** `<path>` `<symbol>`
- **Status:** code | design | gap | withdrawn
- **Reference:** [@<key>] `<symbol>` | [@<key>, "<section>"] — same | similar | clash | none
- **Literature:** [@<key>, sec. <section>] — borrowed | same | similar | method | clash | none
- **Tools:** [@<key>] `<symbol>` | [@<key>, "<page>"] — same | similar | clash | none
- **Decision:** <commit> (<decision ID>) — <one clause>
```

- **Heading:** one term as used in prose, or one identifier in backticks. An abbreviation follows the long form in parentheses. The identifier that implements a prose term is named in Source, never in the heading. A heading never names two terms.
- **Is a:** the parent entry; or, when no entry is the parent, the element kind from the locate step of the naming steps. An element kind is not an entry. Omitted on a top class only.
- **Definition:** one to three sentences of plain prose. The first names the parent and the distinguishing property. Each following sentence gives one case of the term's rule. Status `code`: written from the implementing symbol. Status `design`: written from the doc section. No citation, no history.
- **Example:** a minimal input and the term's instance in it. For a program value, the output the reference implementation prints, verified by running it. For a structural element, the element the analysis yields; for status `design`, the element the doc section specifies. Required when an input yields an instance of the term (a value, a node, an edge, a label, a construct). Omitted on a module, a phase, a component, a principle, and a dataset.
- **Source:** every file and symbol that implements the term, separated by `;`. Status `design`: the doc and its section. Status `gap` or `withdrawn`: the doc section, then the code symbol. Every Source resolves to the named location; `hooks/doc_check.py` reports one that does not.
- **Status:** `code` (implemented); `design` (decided, no code); `gap` (code and decided design differ, the Definition's last sentence states the difference); `withdrawn` (removed from the design, code still present). A design term with partial code is `gap`.
- **Reference:** the rank 2 or rank 3 counterpart, then the relation. Present when the project names ranks 2 and 3.
- **Literature:** one line per source: its bibliography key with the section that defines the word as locator, then the relation. `borrowed` marks the defining source of a borrowed word and is required for one. `method` marks the mechanism behind a core term. `clash` marks the same word for another concept. At most three lines, the defining source first. Further sources go in the module's concept doc.
- **Tools:** one line per tool: its bibliography key, then the symbol or the documentation page title, then the relation. At most two lines.
- Reference, Literature, and Tools cite by bibliography key (`rules/docs/bibliography.md`). Reference and Tools name a symbol, a manual section, or a page title: never a URL, a directory path, or a line number. A file name is added only when the symbol alone is ambiguous. `hooks/doc_check.py` reports a URL, a path, or a line number outside Source and Example, and a citation field without a key.
- **Decision:** one line: every user decision that fixed the name or the definition, newest last, separated by `;`. A commit resolves in the repository. A decision ID resolves in the module's decision record.
- No field carries a date. A commit fixes when a decision, a rename, or a check was made.
- Is a, Definition, Source, and Status are required. Example is required by its rule above. The other fields are present when one exists.

## Order

- A definition uses only terms defined above it in the same file or in a file listed above it. An identifier in backticks refers to its enumeration row and is never a forward reference. Every field after Definition may name any entry.
- Two concerns that define each other's terms move the shared term to the earlier file.
- A class is defined before its members. A member's entry follows its class entry in the same file. Exception: a class whose members exceed one file keeps its entry in the first file; each later file opens with an H2 naming the class and linking its entry, and the routing table lists the later files directly below the first.
- Entries are grouped by H2 section, one per class or per locus. Sections run from the general to the specific.

## Names

- Every heading is unique across all glossary files. An identifier and the prose term it implements share one entry.
- A heading is a term, never the bare element kind of the locate step: no entry named "Node", "Edge", or "Label".
- A rename deletes the old entry and adds a retired-names row with the successor and the commit. A term removed from the design whose code is gone gets a row with successor `none`. A retired name is never reused for another concept.

## Enumerations

- A closed set (every node type or edge type of one graph, every label) is one H2 section: the set's class entry, then one table with columns Member, Definition, Status, Reference, Literature, Tools. A file holds any number of closed sets.
- A counterpart cell holds a citation and its relation in the form of the matching Entry field, or `none`.
- A table row holds one sentence of definition. A member needing more keeps its row and gets an entry headed by its identifier directly below the table.
- A set generated from an external schema has one row per naming pattern, with the generator named in Source.
