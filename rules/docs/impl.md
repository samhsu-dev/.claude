---
paths:
  - "**/impl.md"
  - "**/impl-*.md"
---

# TypeScript Implementation Documents

TypeScript-specific `impl.md` conventions. Extends global `docs/impl.md`.

---

## Library Entry Format

- `library_name >= version` -- purpose. `pnpm add library_name`, or `npm install library_name` under npm.
- Type coverage stated per library: ships its own types, a `@types/*` package, or untyped (typed wrapper at the boundary).
