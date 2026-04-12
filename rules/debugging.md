---
paths:
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
- debug for flow. info for state transitions. error for failures.
- Context in every log.

## Common Pitfalls

- except Exception swallows too much. Catch domain exceptions.
- Missing from exc loses the original traceback.
- assert stripped by python -O. Use if not x: raise in production.
- Mutable default arguments cause cross-test contamination.
