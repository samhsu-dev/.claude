# Local Records

Records that serve only the developers at work live in three local directories, excluded through `.git/info/exclude` and never committed:

| Record | Directory | Holds |
|--------|-----------|-------|
| Decision log | `docs/decisions/` | One entry per question, open or decided; fields below |
| Task docs | `docs/todo/` | Tasks still to do (`rules/docs/todo.md`) |
| Audit reports | `docs/audit/` | Each audit's findings, each with where it went: a doc fix, a task, or a decision item |

- A record goes to the directory its content belongs to, not the one of the activity that produced it: an audit's open question is a decision item, its follow-up is a task.
- Each directory holds one file per module, named after the module (`catalog-import.md` for `docs/catalog/import/`), split by concern past 200 lines, and an `index.md` listing its files.
- Dates, decision IDs and commit hashes are allowed in local records only.
- A decision entry holds its ID and authority, question, choice and reason, the rejected alternatives and all recording commits.
- A user-decidable entry also holds the options, viewpoint recommendations, the refutation result, examples with their expected results and supporting evidence, impact measurements with their method when the choice depends on them, the reused data or mechanisms, and whether earlier decisions are kept or which sentences change.
- An open entry has no choice. Fill that entry when the question is decided.
- Copy evidence needed by the entry into it; a record never depends on a run directory.
- A committed document never names or links a local record, and no committed fact depends on one.
