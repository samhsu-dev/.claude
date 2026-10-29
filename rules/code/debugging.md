---
paths:
  - "**/*.ts"
  - "**/*.tsx"
---

# TypeScript Debugging

TypeScript-specific debugging tools and patterns. Extends global `code/debugging.md`.

---

## Tools

- `debugger`, `console.log()` and `console.trace()` traces stay local. Remove before commit.
- `node --inspect-brk --enable-source-maps dist/<entry>.js` -- debugger on the build output, mapped to the TypeScript source.
- `npx vitest --inspect-brk --no-file-parallelism <file>` -- debugger on tests.
- `npx vitest run --bail=1` -- stop on first failure.

## Logging

- One pino root logger, created once in the entry point's `main()` with level, `redact` paths and transport. Modules receive it and derive `logger.child({ module: "<name>" })`.
- Library modules create no logger and no transport. They take a logger from the caller.
- An error is logged under the `err` key: `logger.error({ err }, "<message>")`. The `err` serializer keeps `type`, `message` and `stack`.

## Common Pitfalls

- `JSON.stringify(error)` yields `{}`. Log the error object under `err`, never its serialized string.
- `try`/`catch` catches a rejection only of an awaited promise.
- `node:assert` is not stripped. Production checks use `if (!x) throw`.
