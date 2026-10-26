---
paths:
  - "**/docs/todo/**"
---

# Python Task Management

Python-specific task conventions. Extends global `docs/todo.md`.

---

## Quality Gate

Project commands for the global quality gate:
- Lint and format: `uv run ruff format`, then `uv run ruff check` -- zero violations.
- Type check: `uv run mypy --strict` -- zero errors.
- Tests: `uv run pytest` -- all pass.

## Conventions

- Design docs cited by relative path: `path/to/design.md`.
- Test tasks name the test file: `tests/<sub>/test_<module>.py`.
- Implementation tasks reference `impl.md` for library findings.
