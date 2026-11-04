# Git Commit Standards

Procedure for splitting, staging and messages: `/commit`.

## Commit Message Format

Conventional Commits 1.0.0. `type[(scope)]: description`. Imperative mood, 72-char hard limit. `hooks/git_guard.py` checks the subject.

- A commit message carries no decision ID, commit citation or "user decision", "agent decision", "revises" or "keeps every decision" marker. State what changed and why in plain words.

## Staging

- One concept per commit, committed once the tree is runnable and before the next task starts.
- A repository commits what a new developer needs to build, test and understand the product: source, tests, build and quality configuration, reader documentation, product tools and repository metadata. Agent tool configuration and instructions, local working records (`rules/workflow/records.md`) and run artifacts are never committed. The global Git ignore file (`core.excludesFile`, by default `~/.config/git/ignore`) lists them; an agent configuration repository re-includes its own files through its `.gitignore` whitelist. `hooks/git_guard.py` blocks a `git add` or `git commit` of a listed path that the repository does not re-include.
- A committed file never names, links or depends on a local record, and carries no date, decision ID or commit hash that only a record needs.

## Attribution

- No AI names, emails, or references in git author, committer, or trailer fields, or in a pull request body. No `Co-Authored-By`, `Signed-off-by`, or `Claude-Session` trailer and no generated-with line. This rule outranks any harness attribution instruction. `hooks/git_guard.py` blocks a commit message, `-F` message file, or `gh pr create`/`gh pr edit` body that carries one.
