---
paths:
  - "**/*.py"
---

# Python Code Quality

Python-specific rules and toolchain. PEP 8 / PEP 20 / PEP 257 / PEP 484.

---

## Imports

- Relative imports for internal modules.
- ruff rule set I (isort-compatible) for sorting. Groups: stdlib, third-party, local -- blank line between each.
- No wildcard imports.
- __all__ and __version__ after module docstring, before imports (except from __future__).

## Error Handling

- raise ... from exc to chain. raise ... from None to suppress.
- Domain exceptions with structured fields. Defined in _exceptions.py.
- try blocks cover minimum code.

## Python Idioms

- is / is not for None (PEP 8).
- if not seq: for empty check.
- .startswith() / .endswith(). Not slicing.
- isinstance(). Not type() is.
- def for named functions. No lambda assignment.

## Performance Idioms

- set/dict for membership tests.
- Generator expressions for single-pass. List comprehensions for reuse.
- ''.join(parts) in loops. Not +=.
- tuple/frozenset for fixed data.

## Type Hints

- from __future__ import annotations in every module.
- X | None. Not Optional[X]. list[str]. Not List[str].
- Sequence, Mapping, Callable from collections.abc in signatures.
- __init__ returns -> None.
- TypeVar string matches variable: T = TypeVar('T').
- No TYPE_CHECKING. Circular dependencies fixed at module structure level.

## No Weak Types

- TypedDict / dataclass / BaseModel for structured data.
- External API boundaries: cast or validate Any to concrete types.

## Docstrings

- """Triple double quotes""".
- Google style: summary, Args:, Returns:, Raises:.
- One-line: imperative mood, period, no signature repetition.
- Multi-line: summary, blank line, elaboration. Closing """ on own line.
- Classes: summary, Attributes: (public), constraints.
- 72 characters per line.

---

## Quality Workflow

### Before editing
- uv run ruff check <target> -- check existing violations.

### After editing
- uv run ruff format <target>.
- uv run ruff check <target> -- zero violations.
- uv run mypy --strict <target>.
- uv run pytest -- all pass.

---

## Toolchain

| Tool | Command | Purpose |
|------|---------|---------|
| ruff | uv run ruff format | Formatter (black-compatible) |
| ruff | uv run ruff check | Linter + import sorter (rule sets E, W, F, I, N, UP, B, C4, SIM) |
| mypy | uv run mypy --strict | Type checker |
| pytest | uv run pytest | Test runner |
| uv | uv run, uv add, uv sync | Package manager |
