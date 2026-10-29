---
paths:
  - "**/*.ts"
  - "**/*.tsx"
---

# TypeScript File Naming and Organization

TypeScript realization of global `code/organization.md`. ESM packages; layout per npm and Node.js module defaults.

---

## File Naming

- Replaces global `code/organization.md` File Naming stem convention: file and directory names are kebab-case: `scope-check.ts`, `http-client/`.

## Package Layout

A single-project repo keeps source in `src/` and build output in `dist/`. Repo root holds `package.json`, `tsconfig.json`, the lockfile, `README.md`.

| Project type | Entry | `package.json` |
|--------------|-------|----------------|
| Application: run in place, never published | `src/main.ts` | `"private": true`, no `exports` |
| CLI: installed executable | `src/bin.ts` | `"bin"` maps the command to `dist/bin.js`; `"files": ["dist"]` |
| Library: imported by other projects | `src/index.ts` | `"exports"` map, `"files": ["dist"]`, shipped `.d.ts` |

- `"type": "module"` in every package. Module format per `rules/workflow/releasing.md` Distribution Types.
- `dist/` is generated: gitignored, never edited, never imported from source.
- Test tree: `rules/code/testing.md` Layout.

## Multi-Project Repository

A repo containing multiple packages is a pnpm workspace.

- Root `package.json` is `"private": true`. `pnpm-workspace.yaml` declares `packages: ["packages/*"]`. One `pnpm-lock.yaml` at repo root. No per-package lockfiles.
- Members live under `packages/<name>/`. Each member holds its own `package.json`, a `tsconfig.json` extending the root config, `src/` and `tests/`.
- A member depends on another member through the workspace protocol: `"<name>": "workspace:*"`.
- Per-member commands use `--filter`: `pnpm --filter <name> run build`.

## Visibility

Public = reachable by consumers of the package. Internal = used only within the package.

- A symbol is internal until a consumer outside the package exists. Public only for the package's intended API.

| Construct | Public | Internal |
|-----------|--------|----------|
| Module | re-exported from `src/index.ts` | not re-exported |
| Symbol | re-exported from `src/index.ts` | `export` only for same-package imports, or not exported |
| Subpath | listed in the `exports` map | absent from `exports`; Node.js refuses the import |

- The `exports` map is the single source of truth for a published package's public API.
- No `_` prefix for internal symbols. Visibility comes from the entry re-export.

## Module Design

- One `index.ts` per directory that a consumer imports, re-exporting that directory's public symbols. No logic.
- Errors in `errors.ts`. Types in `types.ts` when numerous; otherwise beside their logic.
- The dependency direction between directories is a dependency-cruiser `forbidden` rule in `.dependency-cruiser.js`.

## Entry Points

- CLI entry: `src/cli.ts` exporting `main(argv: readonly string[]): Promise<number>`.
- The executable file `src/bin.ts` holds the `#!/usr/bin/env node` line and the `main()` call only: `process.exitCode = await main(process.argv.slice(2));`. No logic.
- Application entry: `src/main.ts` builds the config object, the logger and the module graph, then starts the work.

## Package Data

- Resource files (data files, templates) in `src/resources/`. The build copies them into `dist/resources/`.
- Resolve package data relative to the module: `new URL("./resources/words.json", import.meta.url)`. Never via `process.cwd()` or `__dirname`.
- `"files": ["dist"]` ships the resources inside `dist/`.
