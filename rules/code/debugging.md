---
paths:
  - "**/*.py"
  - "**/*test*"
---

# Python Debugging

Python-specific debugging tools and patterns.

---

## Tools

- logging module. Configure at package __init__.py.
- pdb / breakpoint() for interactive debugging. Remove before commit.
- traceback.print_exc() for full chain in catch blocks.
- pytest --tb=short -x -- concise tracebacks, stop on first failure.
- pytest --pdb -- debugger on failure.

## Logging

- One logger per module via getLogger(__name__).

## Common Pitfalls

- assert stripped by python -O. Use if not x: raise in production.
