---
paths:
  - "**/*.py"
---

# Python File Naming and Organization

Python realization of global `rules/code/organization.md`. PEP 8 naming; layout per `uv init` defaults.

---

## Module and Package Naming

- Module names: lowercase letters, digits, underscores.
- Package (directory) names: lowercase, no underscores. A multi-word package becomes a nested subpackage: `http/client.py`, not `http_client/`.

## Package Layout

A single-project repo follows the `uv init` default layout for its project type. Repo root holds `pyproject.toml`, `.python-version`, `README.md`, `uv.lock`.

| Project type | Layout | Scaffold |
|--------------|--------|----------|
| Script-style application: run in place, never installed | Flat: `main.py` at repo root | `uv init` |
| Installable application: console script in `[project.scripts]` | src layout: `src/<import_name>/` | `uv init --package` |
| Library: imported by other projects | src layout: `src/<import_name>/` + `py.typed` | `uv init --lib` |

- `tests/` at repo root, outside `src/`. Test layout: `rules/code/testing.md`.

## Multi-Project Repository

A repo containing multiple Python projects is a uv workspace.

- Root `pyproject.toml` declares `[tool.uv.workspace]` with `members` globs. One `uv.lock` and one `.venv` at repo root.
- Members live under `packages/`. Each member follows the uv default layout: `packages/<dist-name>/` holding its own `pyproject.toml` and `src/<import_name>/`. Scaffold with `uv init --lib packages/<dist-name>`.
- A member depends on another member via `[tool.uv.sources]` with `<dist-name> = { workspace = true }`.
- Per-member commands use `--package`: `uv run --package <dist-name>`, `uv sync --package <dist-name>`.
- A workspace is one shared resolution. Members requiring conflicting dependency versions or disjoint `requires-python`: independent projects with `{ path = "..." }` sources, no `[tool.uv.workspace]` table.

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
