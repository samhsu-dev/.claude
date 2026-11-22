---
paths:
  - "**/docs/decisions/**"
  - "**/docs/todo/**"
  - "**/docs/audit/**"
---

# Local Records

Records that serve only the developers at work live in three local directories, listed in the global Git ignore file and kept out of commits (`rules/workflow/committing.md` Staging):

| Record | Directory | Holds |
|--------|-----------|-------|
| Decision log | `docs/decisions/` | One entry per question, open or decided; fields below |
| Task docs | `docs/todo/` | Tasks still to do (`rules/docs/todo.md`) |
| Audit reports | `docs/audit/` | Each audit's findings, each with where it went: a doc fix, a task, or a decision item |

- A record goes to the directory of its content, whatever activity produced it: an audit's open question is a decision item, its follow-up is a task.
- Each directory holds one file per module, named after the module (`catalog-import.md` for `docs/catalog/import/`), and an `index.md` listing its files.
- A project task or run record holds current state; its history goes to that record's archive.
- The run ledger, handoff records and agent memory hold current state, evidence and owner links. A rule, procedure or project value lives at its owner; a memory entry links a project value or tool procedure in one line naming that owner.
- Dates, decision IDs and commit hashes are allowed here; committed files follow `rules/workflow/committing.md` Staging.
- A decision entry holds its ID and authority, question, choice and reason, the rejected alternatives and all recording commits.
- A user-decidable entry also holds the options, viewpoint recommendations, the refutation result, examples with their expected results and supporting evidence, impact measurements with their method when the choice depends on them, the reused data or mechanisms, and whether earlier decisions are kept or which sentences change.
- An open entry has no choice. Fill that entry when the question is decided.
- Copy evidence needed by the entry into the log's `evidence/` directory and name its paths in the entry, so the entry reads without any run directory.
- A decision entry starts with its heading and a fenced `jsonl` header: `id`, `decided_by`, `status` (active, open, unknown, superseded, void), `supersedes`, `superseded_by`, `module`, `landing` and `evidence`. The landing is the committed document that states the rule, as a file path with the heading or line of its sentence; a process directive lands in the rule file that applies it; an active directive whose sentence an open row will change names that row as its landing until the row merges.
- Superseded and void entries live under the log's `archive/`; bulk evidence (test output, discussion text, old sentence versions) lives under its `evidence/` with a manifest of paths and hashes. A lookup reads `archive/` and `evidence/` only for a path an entry names.
- The decision log's `index.md` is written only by `paths.decision_index_command`, one line per entry. A lookup greps the index, then reads one entry.
