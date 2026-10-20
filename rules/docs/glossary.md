---
paths:
  - "**/glossary.md"
  - "**/glossary-*.md"
---

# Glossary Standards

The registry of a project's established terms: which terms it holds, how a new term is named, and how the registry is laid out. Which terms output may use: `communication/terminology.md`. Basis: ANSI/NISO Z39.19-2005 (R2010) §5.3.5 term selection by warrant, §8.3 hierarchical relations; W3C SKOS Reference, documentation and mapping properties.

---

## Selection

- An entry exists for a term whose meaning a reader of the repository needs and cannot take from general CS or security usage: a concept the project defines, or a concept of the literature, the analyzed system's manual, or its reference implementation that the documents use with that source's meaning.
- No entry for a general programming word `communication/terminology.md` exempts, nor for a CS or security term used with its textbook meaning: Interface Segregation Principle.
- No entry for a keyword of the analyzed language.
- No entry for an identifier that names no concept of the domain: a helper class, an index, a monitor, an internal variable, field, counter or ID format, a module or package name. Its owner is the design doc.
- No entry for a compound whose meaning follows from its words in general usage: builtin entity, caller label, initial stack.
- No entry for a named external artifact: a paper, a tool, a dataset. Its owner is the bibliography.
- No entry for a shorthand one document uses in its own prose.
- An entry stays only when removing it leaves a sentence of some document ambiguous or unexplained.
- A coined term whose meaning its parts, an existing name, or a plain clause state as well gets no entry and is not used. A new noun bundling several existing things is the typical case. Selection runs before Name Sources.
- Removing an entry never removes the term from the prose: a textbook or literature term stays in the text with its textbook meaning, and only its entry goes.

## Name Sources

Except for the core terms governed by Naming Steps, a concept takes the name the highest-ranked source gives that same concept:

1. A name widely accepted in the literature.
2. The reference manual or standard of the language or system the project analyzes or implements.
3. The reference implementation of that language or system.
4. A name several tools in the field use.
5. The repository's own name.
6. A name only one tool uses.

- Ranks 2 and 3 apply when the project analyzes or implements a language or system. The project rule names them.
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
- Core terms keep their names ahead of Name Sources; their project declarations follow Files. A literature name for the same mechanism is cited in the entry as its method or as a similar concept, never used as the name. A literature name for what a value stands for serves as the role noun.
- A class named in the project's own publication stays a class in the glossary. It never becomes the name of one implementation element.

## Files

- `glossary.md` is the routing file. Every other glossary file is `glossary-<concern>.md` in the same directory, one concern per file.
- The project's naming decisions (its rank 2 and rank 3 name sources, its naming-step parameters, its core terms, its top classes, its layers, each with its commit) are agent instructions. They live in the project rule `.claude/rules/docs/glossary.md`, never in a repository document.
- The routing file holds only what a reader of the glossary needs, in order: what the glossary is, the conventions for reading an entry (Source path prefix, bibliography path), the routing table, and the retired-names table. It holds no entry and no instruction for writing one. Pinned versions live in the bibliography (`rules/docs/bibliography.md`).
- Routing table columns: File, Concern. Routing table order is reading order. A term is found by its heading: `grep -n "^### <term>" <dir>/glossary*.md`.
- Retired-names table columns: Retired, Successor. One row per rename or removal; provenance follows `CLAUDE.md` Local Records.
- After a glossary file splits, add its new files to the routing table.

## Layers

- The glossary files form layers, read from the general to the specific. Default order: architecture (modules, phases); infrastructure (storage, input and output, settings, dispatch); the model of the analyzed language or system; one schema file per data structure (a graph, a model, a table) with its element types and their attributes; the core algorithm; analysis semantics, one file per concern; the procedure of each phase; outputs (facts, reports). The project rule names the project's layers and the commit that fixed them.
- An element type of a structure, or an attribute of one, goes to that structure's schema file. A rule for writing a structure goes to infrastructure. A step of one phase goes to that phase's procedure file.
- Any other entry goes to the file of the concern its Definition states, whatever structure its Is a names. A semantic term whose Is a is an AST node type, such as a read of a variable, stays with its concern, not in the AST schema file.

## Entry

One entry per term: an H3 heading followed by fields in this order.

```markdown
### <Long form> (<ABBREVIATION>)
- **Is a:** <parent entry>
- **Definition:** <one to three sentences>
- **Example:** `<minimal input>` → <the term's instance in it>
- **Source:** `<path>` `<symbol>`
- **Reference:** [@<key>] `<symbol>` | [@<key>, "<section>"] — same | similar | clash | none
- **Literature:** [@<key>, sec. <section>] — borrowed | same | similar | method | clash | none
- **Tools:** [@<key>] `<symbol>` | [@<key>, "<page>"] — same | similar | clash | none
```

- **Heading:** one term as used in prose, or one identifier in backticks. An abbreviation follows the long form in parentheses. The identifier that implements a prose term is named in Source, never in the heading. A heading never names two terms.
- **Is a:** the parent entry, or the enumeration member in backticks, such that "<heading> is a <parent>" holds and both name the same kind of concept: two operations, two data, two rules. Omitted when no entry is the parent. A part never names its whole here; the Definition states the whole.
- **Definition:** one sentence of plain prose: the genus and the distinguishing property. The genus is the Is a entry, or a plain CS word (operation, graph, rule) when Is a is omitted. Written from the design doc section that decides the term; from the implementing symbol when no doc section decides it. No citation, no history.
- **Example:** a minimal input and the term's instance in it. For a program value, the output the reference implementation prints, verified by running it. For a structural element, the element the analysis yields; for a term with no code, the element the doc section specifies. Required when an input yields an instance of the term (a value, a node, an edge, a label, a construct); omitted otherwise.
- **Source:** every file and symbol that implements the term, separated by `;`. A term with no code: the doc and its section. A term whose code differs from the decided design, or whose code the design removed: the doc section, then the code symbol; the Open Gaps section of that design doc states the difference. Every Source resolves to the named location; `hooks/doc_check.py` reports one that does not.
- **Reference:** the rank 2 or rank 3 counterpart, then the relation. Present when the project names ranks 2 and 3.
- **Literature:** one line per source: its bibliography key with the section that defines the word as locator, then the relation. `borrowed` marks the defining source of a borrowed word and is required for one. `method` marks the mechanism behind a core term. `clash` marks the same word for another concept. At most three lines, the defining source first. Further sources go in the module's concept doc.
- **Tools:** one line per tool: its bibliography key, then the symbol or the documentation page title, then the relation. At most two lines.
- Shared citation syntax: `rules/docs/bibliography.md`. Glossary locators name a symbol, manual section, or page title; a file name is added only when the symbol alone is ambiguous. No URL, path, or line number outside Source and Example, and no citation field without a key; `hooks/doc_check.py` reports these violations.
- Definition and Source are required. Fields without a presence condition above are present when a source exists.

## Order

- A definition uses only terms defined above it in the same file or in a file listed above it. An identifier in backticks refers to its enumeration row and is never a forward reference. Every field after Definition may name any entry.
- Two concerns that define each other's terms move the shared term to the earlier file.
- A class is defined before its members. A member's entry follows its class entry in the same file. Exception: a class whose members exceed one file keeps its entry in the first file; each later file opens with an H2 naming the class and linking its entry, and the routing table lists the later files directly below the first.
- Entries are grouped by H2 section, one per class or per locus. Sections run from the general to the specific.

## Names

- Every heading is unique across all glossary files.
- A heading is a term, never the bare element kind of the locate step: no entry named "Node", "Edge", or "Label".
- A rename deletes the old entry and adds a retired-names row with the successor. A term removed from the design whose code is gone gets a row with successor `none`. A retired name is never reused for another concept.

## Enumerations

- A closed set (every node type or edge type of one graph, every label) is one H2 section: the set's class entry, then one table with columns Member, Definition, Reference, Literature, Tools. A file holds any number of closed sets.
- A counterpart cell holds a citation and its relation in the form of the matching Entry field, or `none` with an optional parenthetical reason. A `|` inside a cell is escaped as `\|`.
- A table row holds one sentence of definition. A member needing more keeps its row and gets an entry headed by its identifier directly below the table.
- A set generated from an external schema has one row per naming pattern, with the generator named in Source.
