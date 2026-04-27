---
paths:
  - "**/todo.md"
---

# Python Task Management

Python-specific task conventions.

---

## Quality Gate

Every task ends with:
- [ ] uv run black and uv run isort
- [ ] uv run pylint -- 9.0+
- [ ] uv run mypy --strict
- [ ] uv run pytest -- all pass

## Conventions

- Design docs by relative path: Depends on: path/to/design.md.
- Test tasks name the test file: tests/test_<component>.py.
- Implementation tasks reference impl.md for library findings.
