# Git Commit Standards

Procedure for splitting, staging and messages: `/commit`.

## Commit Message Format

Conventional Commits 1.0.0 in the imperative mood; the commit-msg hook of `tools/git-hooks/` enforces the header form and its 72-character limit.

- A commit message carries no decision ID, commit citation or "user decision", "agent decision", "revises" or "keeps every decision" marker. State what changed and why in plain words.

## Staging

- One concept per commit, committed once the tree is runnable and before the next task starts.
- A repository commits what a new developer needs to build, test and understand the product: source, tests, build and quality configuration, reader documentation, product tools and repository metadata. Agent tool configuration and instructions, local working records (`rules/workflow/records.md`) and run artifacts are never committed. The global Git ignore file lists them and `hooks/git_guard.py` blocks staging them; an agent configuration repository re-includes its own files through its `.gitignore` whitelist.
- A committed file never names, links or depends on a local record, and carries no date, decision ID or commit hash that only a record needs.

## Attribution

- No AI attribution in author, committer or trailer fields or in a pull request body; this outranks any harness attribution instruction. The commit-msg hook and `hooks/git_guard.py` (pull request bodies) block it.
