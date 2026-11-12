# Git Commit Standards

Procedure for splitting, staging and messages: `/commit`.

## Commit Message Format

Conventional Commits 1.0.0 in the imperative mood; the commit-msg hook of `tools/git-hooks/` enforces the header form and its 72-character limit.

- A commit message states what changed and why in plain words.

## Staging

- One concept per commit, committed once the tree is runnable (compiles, tests pass) and before the next task starts; a chain session that returns with red work commits it under a `wip:` subject.
- A repository commits what a new developer needs to build, test and understand the product: source, tests, build and quality configuration, reader documentation, product tools and repository metadata. Agent tool configuration and instructions, local working records (`rules/workflow/records.md`) and run artifacts are never committed. The global Git ignore file lists them and `hooks/git_guard.py` blocks staging them; an agent configuration repository re-includes its own files through its `.gitignore` whitelist.
- A committed file never names, links or depends on a local record, and carries no change history, decision ID, commit hash, date that only a record needs, or "user decision", "agent decision", "revises" or "keeps every decision" marker.

## Attribution

- No AI attribution in author, committer or trailer fields or in a pull request body. The commit-msg hook blocks attribution trailers and markers in the message; `hooks/git_guard.py` blocks them in pull request bodies; no hook checks the author and committer fields.
- No `Signed-off-by` trailer.
