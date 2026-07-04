---
paths:
  - "**/*.py"
---

# Python File Naming and Organization

Python realization of global `rules/code/organization.md`. PEP 8 naming; src layout per PyPA.

---

## Module and Package Naming

- Module names: lowercase letters, digits, underscores.
- Package (directory) names: lowercase, no underscores. A multi-word package becomes a nested subpackage: `http/client.py`, not `http_client/`.

## Package Layout

- Distributable packages use src layout: `src/<package>/`. Applications never installed as a package keep the package at repo root.
- `tests/` at repo root, outside `src/`. Test layout: `rules/code/testing.md`.

## Visibility

Public = used by consumers of the package. Internal = used only within the package.

| Construct | Public | Internal |
|-----------|--------|----------|
| Module | re-exported in __init__.py | _module.py |
| Class | in __all__ | _ClassName |
| Function | in __all__ | _func_name |
| Method | no prefix | _method |
| Constant | in __all__ | _CONSTANT |

- __all__ is the single source of truth for a package's public API.
- No __method (name mangling). Use _method for internal.

## Module Design

- One __init__.py per package with explicit __all__.
- __init__.py contains re-exports, __all__, and __version__ only. No logic.
- Internal modules prefixed with _. Public API re-exported from __init__.py.
- Exceptions in _exceptions.py. Types in _types.py when numerous.

## Entry Points

- CLI entry: cli.py exposing main(), registered in [project.scripts].
- __main__.py contains the main() call only: `sys.exit(main())`. No __name__ guard.

## Package Data

- Resource files (data files, templates) in _resources/. Templates in _resources/templates/.
- Read package data via importlib.resources. Never via __file__ path arithmetic.
- Build configuration includes _resources/ in the distribution.
