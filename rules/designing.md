---
paths:
  - "**/design.md"
---

# Python Design Standards

Python-specific design rules. PEP 8 / PEP 20 / PEP 257 / PEP 484 / PEP 544.

---

## Type Selection

- @dataclass for data holders. @dataclass(frozen=True) for immutable data holders.
- BaseModel for validated or schema-generated data (LLM structured output).
- TypedDict for typed dictionary shapes (TOML/JSON config).
- Protocol + @runtime_checkable for structural subtyping without shared state.
- ABC + @abstractmethod for type hierarchies with shared state.
- NewType for zero-overhead type distinctions.

## Visibility

Public = used by consumers of the package. Internal = used only within the package.

| Construct | Public | Internal |
|-----------|--------|----------|
| Module | re-exported in __init__.py | _module.py |
| Class | in __all__ | _ClassName |
| Function | in __all__ | _func_name |
| Method | no prefix | _method |
| Constant | in __all__ | _CONSTANT |

- Public when a consumer needs it or benefits from direct access. Internal when it is an implementation detail.
- __all__ is the single source of truth for a package's public API.
- No __method (name mangling). Use _method for internal.
- Google-style docstrings on all public symbols.
- Public API is discoverable: __all__ + docstrings.

## Module Design

- One __init__.py per package with explicit __all__.
- Internal modules prefixed with _. Public API re-exported from __init__.py.
- Modules grouped by domain. No utils/, helpers/, common/.
- Exceptions in _exceptions.py. Types in _types.py when numerous.
- Resource files (TOML, Jinja2 templates) in _resources/. Jinja2 templates in _resources/templates/.

## TOML Externalization

Externalize to TOML when:
- Data is a table, list, or mapping that would dominate the Python source.
- Data is shared across multiple modules or layers.
- Data changes independently of the logic that consumes it.

Keep as Python constants when:
- Value is a single scalar.
- Value is an enum member or a frozen set of a few items.
- Value is tightly coupled to one function and meaningless elsewhere.

## Exception Design

- Derive from Exception, not BaseException.
- Hierarchy by how callers catch, not where raised.
- Structured context fields (step, reason). No bare strings.
- Third-party exceptions mapped at boundary.
- Misuse errors separate from runtime errors.

## API Design

- No mutable default arguments.
- Explicit parameters. No *args/**kwargs unless proven necessary.
- All branches return a value, or none do.
- Factory functions when construction has configuration or variants.
- Properties for O(1) access. Methods for computation.

## Typing Patterns

- TypeVar(bound=) for generic functions on a type hierarchy.
- @overload when return type depends on input type.
- Literal for finite value sets.

## Resource Management

- Context managers for resource lifecycle. No __del__.
- @functools.cache / @functools.lru_cache for pure-function memoization.
