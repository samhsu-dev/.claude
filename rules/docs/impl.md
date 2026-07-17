---
paths:
  - "**/impl.md"
  - "**/impl-*.md"
---

# TypeScript Implementation Documents

TypeScript-specific `impl.md` conventions.

---

## API Entry Format

**[library]** `import { Thing } from 'library'` -- when/gotcha.

Example:
**[zod]** `schema.safeParse(input)` -- returns { success, data | error }; .parse() throws ZodError.
**[undici]** `fetch(url, { signal: AbortSignal.timeout(10_000) })` -- no default timeout; omitting signal hangs on a dead peer.

## Library Entry Format

- library_name >= version -- purpose. Install via the repo package manager (`npm install library_name` / `pnpm add library_name`).
- Type coverage stated per library: ships own types, @types/* package, or untyped (wrapper required at boundary).
