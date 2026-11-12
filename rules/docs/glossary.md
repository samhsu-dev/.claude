---
paths:
  - "**/glossary.md"
  - "**/glossary-*.md"
---

# Glossary Standards

Which terms output may use: `communication/terminology.md`.

---

## Selection

- Every domain term in output has a glossary entry. General programming words (function, variable, class, loop, exception, call) need none. An identifier quoted as code needs an entry when it names a domain concept.
- No entry for an identifier that names no concept of the domain: a helper class, an index, a monitor, an internal variable, field, counter or ID format, a module or package name. Its owner is the design doc.
- No entry for a named external artifact: a paper, a tool, a dataset. Its owner is the bibliography.
- A coined term whose meaning its parts, an existing name, or a plain clause state as well gets no entry and is not used. Two entries whose definitions overlap, or one that is a special case the other states with a plain clause, are redundant: one stays and the other folds into it or is removed. Selection runs before Name Sources.
- Removing an exempt entry never removes the term from prose.

## Name Sources

A concept takes the name the highest-ranked source gives that same concept:

1. A name widely accepted in the literature.
2. The reference manual or standard of the language or system the project analyzes or implements.
3. The reference implementation of that language or system.
4. A name several tools in the field use.
5. The repository's own name.
6. A name only one tool uses.

- Ranks 2 and 3 apply when the project analyzes or implements a language or system. Their values are `glossary.name_sources`.
- A source counts only where its word names the same concept. The same word for another concept is a clash, never a name source.
- A candidate name that already names another glossary concept is recorded with both entries as a user question in the finding run's progress file; the main agent asks the user.
- A borrowed word with no literature source in its glossary entry is a coined term.
- A rename question cites the rank and the source of every candidate name.
- A literature name source is a paper of `glossary.literature_min_year` or later; a paper later than `glossary.naming_cutoff_work` is similar at most, never a name source.
- The Tools field checks each counterpart of `glossary.tools`.

## Naming Steps

An existing source name is selected in three steps, in order:

1. **Locate.** The structure the term belongs to — the structure and the element kind within it — gives the head noun.
2. **Classify.** Identify the domain context that distinguishes the concept, such as its lifecycle stage or role in a process.
3. **Name.** The name is the locus plus one role noun taken by Name Sources.

- Terms of one locus that play the same role take one role noun; terms of one locus with different roles take different role nouns.
- A state or attribute recorded on the element stays out of the element's name.
- An umbrella term names only a class with a behavior of its own.
- Core terms keep their names ahead of Name Sources; their project declarations follow Files. A literature name for the same mechanism is cited in the entry as its method or as a similar concept, never used as the name. A literature name for what a value stands for serves as the role noun.
- A class named in the project's own publication stays a class in the glossary. It never becomes the name of one implementation element.

## Files

- `glossary.md` is the routing file. Every other glossary file is `glossary-<concern>.md` in the same directory, one concern per file.
- The routing file holds only what a reader of the glossary needs, in order: what the glossary is, the conventions for reading an entry (Source path prefix, bibliography path and `bibliography.collection` when set), the routing table, the imported-terms table (Repositories), and the retired-names table. It holds no entry and no instruction for writing one.- Routing table columns: File, Concern. Routing table order is reading order. A term is found by its heading or its enumeration row: `grep -n "^### <term>\|^| <term> |" <dir>/glossary*.md`.
- Retired-names table columns: Retired, Successor. One row per rename or removal; provenance follows `rules/workflow/records.md`.
- After a glossary file splits, add its new files to the routing table.

## Layers

- Read glossary concerns in configured `glossary.layers` order. Without that value, follow the documentation's dependency order.
- An element type or attribute belongs to its structure's schema; a process step belongs to its process concern.
- Other entries belong to the concern their Definition states, independently of the structure named by Is a.

## Entry

One entry per term: an H3 heading followed by fields in this order.

```markdown
### <Long form> (<ABBREVIATION>)
- **Is a:** <parent entry>
- **Definition:** <definition>
- **Example:** `<minimal input>` → <the term's instance in it>
- **Source:** `<path>` `<symbol>`
- **Reference:** [@<key>] `<symbol>` | [@<key>, "<section>"] — same | similar | clash | none
- **Literature:** [@<key>, sec. <section>] — borrowed | same | similar | method | clash | none
- **Tools:** [@<key>] `<symbol>` | [@<key>, "<page>"] — same | similar | clash | none
```

- **Heading:** one term as used in prose, or one identifier in backticks. An abbreviation follows the long form in parentheses. The identifier that implements a prose term is named in Source, never in the heading. A heading never names two terms.
- **Is a:** the parent entry, or the enumeration member in backticks, such that `<heading> is a <parent>` holds and both name the same kind of concept: two operations, two data, two rules. Omitted when no entry is the parent. A part never names its whole here; the Definition states the whole.
- **Definition:** one plain sentence with the genus and distinguishing property. The genus is the Is a entry or a plain domain word. Use the owning document section under `rules/docs/documentation.md` Ownership, or the implementing symbol when no document decides it. No citation. Provenance stays in Local Records.
- **Example:** a minimal input and the term's instance in it. For a program value, the output the reference implementation prints, verified by running it. For a structural element, the element the analysis yields; for a term with no code, the element the doc section specifies. Required when an input yields an instance of the term; omitted otherwise.
- **Source:** every file and symbol that implements the term, separated by `;`. A term with no code: the doc and its section. A term whose code differs from the decided design, or whose code the design removed: the doc section, then the code symbol; the Open Gaps section of that design doc states the difference. Every Source resolves to the named location; `hooks/doc_check.py` reports a Source file path that does not resolve.
- **Reference:** the rank 2 or rank 3 counterpart, then the relation. Present when those sources are configured.
- **Literature:** one line per source: its bibliography key with the section that defines the word as locator, then the relation. `borrowed` marks the defining source of a borrowed word and is required for one. `method` marks the mechanism behind a core term. `clash` marks the same word for another concept. At most three lines, the defining source first. Further sources go in the module's concept doc.
- **Tools:** one line per tool: its bibliography key, then the symbol or the documentation page title, then the relation. At most two lines.
- Shared citation syntax: `rules/docs/bibliography.md`. Glossary locators name a symbol, manual section, or page title; a file name is added only when the symbol alone is ambiguous. No URL, path, or line number outside Source and Example, and no citation field without a key; `hooks/doc_check.py` reports these violations.
- Definition and Source are required. Literature and Tools are written after searching `glossary.tools` and the bibliography; a field with no source found is omitted.

## Order

- A definition uses only terms defined above it in the same file or in a file listed above it. An identifier in backticks refers to its enumeration row and is never a forward reference. Every field after Definition may name any entry.
- Two concerns that define each other's terms move the shared term to the earlier file.
- A class is defined before its members. A member's entry follows its class entry in the same file. Exception: a class whose members exceed one file keeps its entry in the first file; each later file opens with an H2 naming the class and linking its entry, and the routing table lists the later files directly below the first.
- Entries are grouped by H2 section, one per class or per locus. Sections run from the general to the specific.

## Names

- Every heading is unique across all glossary files.
- A heading is a term, never the bare element kind of the locate step.
- A rename deletes the old entry and adds a retired-names row with the successor. A term removed from the design whose code is gone gets a row with successor `none`. A retired name is never reused for another concept.

## Enumerations

- A closed set is one H2 section: the set's class entry, then one table with columns Member, Definition, Reference, Literature, Tools. A file holds any number of closed sets.
- A counterpart cell holds a citation and its relation in the form of the matching Entry field, or `none` with an optional parenthetical reason. A `|` inside a cell is escaped as `\|`.
- A table row holds one sentence of definition. A member needing more keeps its row and gets an entry headed by its identifier directly below the table.
- A set generated from an external schema has one row per naming pattern, with the generator named in Source.

## Repositories

- Each repository with documentation has its own glossary. The repository that defines a concept owns its entry; no concept has entries in two glossaries.
- A consumer refers to a dependency's term by its exact name and links its owning entry. It never redefines or renames the term.
- The consumer's routing file holds an imported-terms table with columns Term and Owning entry: one row per dependency term its documents use, no definition. That row and the owner's entry meet the Selection obligation.
- Locate takes the head noun from `glossary.head_kinds`; Classify takes the role from `glossary.loci`; `glossary.top_classes` assigns each locus its top class.
- A heading, word form or spelling that a `glossary` value states is used exactly as stated: `glossary.core_terms`, `glossary.protected_borrowed_terms`, `glossary.algorithm_data_names`, `glossary.operation_headings`, `glossary.property_heading`, `glossary.unknown`.
- Link direction and link form follow `rules/docs/documentation.md` Repositories.
