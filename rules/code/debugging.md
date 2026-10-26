---
paths:
  - "**/*.py"
---

# Python Debugging

Python-specific debugging tools and patterns. Extends global `code/debugging.md`.

---

## Tools

- `breakpoint()`, `print()` and `traceback.print_exc()` traces stay local. Remove before commit.
- `uv run pytest --pdb` -- debugger on failure.

## Logging

- One logger per module: `logger = logging.getLogger(__name__)`.
- Handlers and levels are configured once, in the entry point's `main()`, through `logging.config.dictConfig`. Library modules add no handlers.

## Common Pitfalls

- `assert` is stripped by `python -O`. Production checks use `if not x: raise`.
