# Git Commit Standards

Conventional Commits 1.0.0. Community best practices (cbea.ms/git-commit).

## Attribution

Commits and PRs appear under the human author. AI executes operations; AI identity never appears in output.

- No AI names, emails, or references in git author, committer, or trailer fields.
- No `Co-Authored-By`, `Signed-off-by`, or any trailer containing `Claude`, `AI`, or `Anthropic`.
- Verify before push: `git log -1 --format='%an <%ae>'` shows a human identity.

## Subject Line

Format: `type[(scope)]: description` (Conventional Commits 1.0.0).

- Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`, `perf`, `build`, `style`.
- Scope: noun in parentheses — `fix(parser):`, `feat(auth):`.
- Description: imperative mood, lowercase after colon, no trailing period.
- 50 characters target. 72 characters hard limit.
- Test: "If applied, this commit will ___."
- Breaking changes: append `!` after type/scope — `feat!:`, `fix(api)!:`.
- Match the repository's existing commit naming conventions when a project convention exists.

## Body

- One blank line between subject and body.
- Wrap at 72 characters.
- Explain what changed and why. Never explain how — code shows how.
- Required when the subject alone is insufficient. Omit for trivial changes.

## Footers

- One blank line after body.
- Format: `Token-Name: value` or `Token-Name #value`.
- `BREAKING CHANGE: description` (uppercase) for breaking changes.
- `Refs #123`, `Closes #456` for issue references.

## Granularity

- One concept per commit.
- Separate concerns: types/config, core logic, deletions/cleanup, adapters, docs, tests.
- No unrelated changes in a single commit.

## Ordering

- Foundational changes first (types, config), then consumers (core logic, adapters), then cleanup, then docs.
- Each commit leaves the codebase in a consistent state.

## Staging

- Stage specific files by name. Never `git add -A` or `git add .`.
- No dead code, temporary files, or generated artifacts in commits.

## Pull Requests

- Create only after explicit user approval.
- Title: concise summary, under 70 characters.
- Body: natural language, summarize what changed and why in 1-5 bullets.
- No repeated information between title and body.
- No AI names or attribution in title, body, comments, or metadata.
- No auto-generated boilerplate.
