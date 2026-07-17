---
paths:
  - "**/*.ts"
  - "**/*.tsx"
---

# TypeScript File Naming and Organization

TypeScript realization of global `rules/code/organization.md`. ESM-first; layout per current npm ecosystem defaults.

---

## File and Directory Naming

- File names: kebab-case -- schema-utils.ts, scope-check.ts. One primary export per file, file named after it.
- Directory names: kebab-case, plural for collections of peers (agents/, handlers/).
- Test files: `rules/code/testing.md`.

## Package Layout

A single-project repo keeps source in `src/`, build output in `dist/`. Repo root holds `package.json`, `tsconfig.json`, the lockfile, `README.md`.

| Project type | Entry | Distribution |
|--------------|-------|--------------|
| Application: run in place, never published | src/index.ts bootstraps | "private": true; no exports map |
| CLI: installed executable | src/cli.ts exposing main(), registered in "bin" | files: ["dist"] |
| Library: imported by other projects | src/index.ts re-exports public API | files: ["dist"] + exports map + shipped .d.ts |

- `"type": "module"` in every new package. ESM-only by default; dual ESM+CJS only per `rules/workflow/releasing.md`.
- `tests/` at repo root, outside `src/`. Test layout: `rules/code/testing.md`.
- `dist/` is generated: gitignored, never edited, never imported from source.

## Multi-Project Repository

A repo containing multiple packages is a pnpm workspace.

- Root `package.json` is `"private": true`. `pnpm-workspace.yaml` declares `packages: ["packages/*"]`. One `pnpm-lock.yaml` at repo root. Never per-package lockfiles.
- Members live under `packages/`. Each member holds its own `package.json`, `tsconfig.json` extending the root config, and `src/`.
- A member depends on another member via the workspace protocol: `"sibling": "workspace:*"`. pnpm rewrites it to a real version on publish.
- Per-member commands use `--filter`: `pnpm --filter <name> run build`.

## Visibility

Public = reachable by consumers. Internal = used only within the package.

| Construct | Public | Internal |
|-----------|--------|----------|
| Module | re-exported from src/index.ts | under src/internal/, never re-exported |
| Symbol | exported and re-exported at entry | exported only for same-package imports |
| Subpath | listed in "exports" map | absent from "exports" -- unresolvable by consumers |

- The `exports` map is the single source of truth for a published package's public surface. Unlisted subpaths throw on import.
- For applications, src/index.ts and the modules it wires are the surface; everything else is internal.
- No underscore prefix for internal symbols. Internality comes from not being exported at the entry point.

## Module Design

- src/index.ts contains re-exports only. No logic.
- One module, one responsibility. A module needing "and" in its description splits.
- Errors in errors.ts. Shared types in types.ts when numerous; otherwise types live beside their logic.
- No circular imports. A cycle is fixed at module structure level, not with lazy import.

## Entry Points

- CLI entry: src/cli.ts exposing main(). "bin" maps the command name to dist/cli.js.
- The bin file body is the main() call: `void main();` behind the `#!/usr/bin/env node` shebang. No logic.
- Server entry: src/index.ts constructs config, wires modules, starts the listener.

## Package Data

- Resource files (data files, templates) in src/resources/. Copied to dist by the build.
- Resolve package data via import.meta.dirname (or fileURLToPath(import.meta.url)). Never via cwd-relative paths, never via __dirname in ESM.
- files field includes dist/ only; resources ship inside it.
