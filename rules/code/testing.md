---
paths:
  - "**/*test*"
---

# Python Testing

Python/pytest conventions.

---

## Test Design (Python)

Pytest implementations of black-box test design:

### Equivalence partitioning + boundary analysis via parametrize
@pytest.mark.parametrize("month,valid", [
    (0, False),   # below minimum
    (1, True),    # minimum boundary
    (6, True),    # nominal (one per valid partition)
    (12, True),   # maximum boundary
    (13, False),  # above maximum
])
def test_validate_month(month: int, valid: bool) -> None:
    if valid:
        assert validate_month(month) == month
    else:
        with pytest.raises(ValueError):
            validate_month(month)

---

## Layout

- Shared fixtures in tests/conftest.py. Subdirectory fixtures in tests/<subdir>/conftest.py.

## Discovery

- Files: test_*.py or *_test.py.
- Functions prefixed with test_.
- No unittest.TestCase. Plain functions with fixtures.

## Fixtures

### Scope
- function (default): per test.
- module: per file. For setup shared across one file.
- session: per run. For read-only resources.
- No class scope. No test classes.

### Patterns
- Yield fixtures for teardown.
- tmp_path: unique Path per test.
- monkeypatch: env vars and attribute patching. Auto-reverted.
- capsys: stdout/stderr capture.
- Fixtures return fresh objects. No shared mutable state.

### conftest.py
- Auto-discovered. No import needed.
- One per directory. Scoped to that directory and below.

## Assertions

- assert x == y -- pytest rewrites for detailed output.
- pytest.raises(Type) with field check.
- pytest.approx() for floats.
- No unittest assertions. Plain assert.

## Parametrize

- @pytest.mark.parametrize for data-driven tests.
- @pytest.fixture(params=[...]) for fixture variants.

## Execution

- uv run pytest -- all tests.
- uv run pytest -x --tb=short -- stop on first failure.
- uv run pytest tests/<subdir>/ -- one directory.
- uv run pytest -k "test_keyword" -- keyword match.

## Configuration

[tool.pytest.ini_options]
testpaths = ["tests"]
