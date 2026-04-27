---
paths:
  - "**/*.py"
---

# Python Code Quality

Python-specific rules and toolchain. PEP 8 / PEP 20 / PEP 257 / PEP 484.

---

## Imports

- Relative imports for internal modules.
- isort for sorting. Groups: stdlib, third-party, local -- blank line between each.
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
- uv run pylint <target> -- check score and warnings.

### After editing
- uv run black <target> and uv run isort <target>.
- uv run pylint <target> -- 9.0+.
- uv run mypy --strict <target>.
- uv run pytest -- all pass.

---

## Toolchain

| Tool | Command | Purpose |
|------|---------|---------|
| black | uv run black | Formatter |
| isort | uv run isort | Import sorter |
| pylint | uv run pylint | Linter (9.0+) |
| mypy | uv run mypy --strict | Type checker |
| pytest | uv run pytest | Test runner |
| uv | uv run, uv add, uv sync | Package manager |
