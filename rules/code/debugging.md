---
paths:
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*test*"
---

# TypeScript Debugging

TypeScript-specific debugging tools and patterns.

---

## Tools

- node --inspect-brk + debugger statement for interactive debugging. Remove debugger before commit.
- error.cause chain read in full: for (let e = err; e; e = e.cause) before changing code.
- vitest run --bail=1 -- stop on first failure.
- vitest run --reporter=verbose -- per-test output.
- vitest --inspect-brk --no-file-parallelism -- debugger on tests.

## Logging

- One structured logger per process, injected or imported from a single logging module. No scattered console.log.

## Common Pitfalls

- A floating promise swallows its rejection. Await or return every promise; --unhandled-rejections=strict surfaces the rest.
- JSON.stringify(error) yields {}. Log error.message, error.stack, error.cause explicitly or via the logger's error serializer.
- node:assert is not stripped in production. Guard clauses with typed throws replace assert in library code.
- try/catch around await catches rejections. try/catch around an unawaited call does not.
