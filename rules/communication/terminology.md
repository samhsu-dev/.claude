# Terminology and Communication Scope

Rules governing the vocabulary used in all agent output. Always active.

---

## Scope

These rules bind every surface the agent writes, with no exception: chat replies, commit messages, documentation, code comments and docstrings, identifiers, log messages, figure titles and axis labels, and directory and file names.

## Domain

- Every technical term comes from computer science or security, or from the repository's own established vocabulary. There is no third source.
- Never borrow a term from an unrelated domain — gaming, biology, finance, sports, medicine, clinical trial design, military, law — as a metaphor for a technical concept. Domain-of-origin test before writing any term: name the field it comes from. Not CS, not security, not this repository → replace it.
- Never coin a term, label, or metaphor the codebase does not already use.
- A concept the repository already names is referred to only by that name.
- Two named variants of one system under comparison are its implementations, named by what the code calls them (backend, strategy, implementation). Never "arm", "condition", "treatment", or "control" — those name a trial design, not a program.

## Verification Before Use

- Check the project glossary (`.claude/glossary.md` when present) before introducing any term.
- A term absent from code, data files, and glossary is not established; use the plain CS or security term instead.
- Register a genuinely new term in the glossary on first use. Define it from the code that implements it, never from its name.

## Explanation

- Explain every non-obvious term in plain words on first use.
- State the concept directly. A reader never decodes a metaphor to reach the meaning.
- Use the exact identifier from the code over a paraphrase when precision matters.

## Forbidden Substitutions

- Image build provenance is "构建来源", never "血缘" (biology).
- A pseudonym-hardened image is "假名加固镜像", never "换皮镜像" (gaming slang).
- A per-cell isolated environment is the established repo phrase, never an invented image.
