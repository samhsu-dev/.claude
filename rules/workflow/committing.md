# Git Commit Standards

Procedure for splitting, staging and messages: `/commit`.

## Commit Message Format

Conventional Commits 1.0.0 in the imperative mood; the commit-msg hook of `tools/git-hooks/` enforces the header form and its 72-character limit.

- A commit message states what changed and why in plain words.
- A merge commit takes the same header form: its subject states the change the merged branch delivers, and its body lists the subjects of the merged commits. The commit-msg hook rejects Git's default merge subject (`Merge commit '<sha>' into HEAD`, `Merge branch '<name>'`).

## Staging

- One concept per commit, committed once the tree is runnable (compiles, tests pass) and before the next task starts; a chain session that returns with red work commits it under a `wip:` subject.
- A repository commits what a new developer needs to build, test and understand the product: source, tests, build and quality configuration, reader documentation, product tools and repository metadata. Agent tool configuration and instructions, local working records (`rules/workflow/records.md`) and run artifacts stay out of commits: the global Git ignore file lists them and `hooks/git_guard.py` blocks staging them; an agent configuration repository re-includes its own files through its `.gitignore` whitelist.
- A committed file states its current content on its own: it leaves every name of, link to and dependency on a local record, the change history, decision IDs, commit hashes, dates that only a record needs, and "user decision", "agent decision", "revises" and "keeps every decision" markers to the local records.

## Attribution

- Write the author, committer and trailer fields and every pull request body with no AI attribution. The commit-msg hook blocks attribution trailers and markers in the message; `hooks/git_guard.py` blocks them in pull request bodies; no hook checks the author and committer fields.
- Leave out the `Signed-off-by` trailer.
