---
paths:
  - "**/package.json"
  - "package-lock.json"
  - "pnpm-lock.yaml"
  - "pnpm-workspace.yaml"
  - ".github/workflows/*.yml"
---

# TypeScript Release Rules

Release standards by distribution type. Project-specific release facts — package names, artifact inventories, tag names, credential mechanism, identity policy — live in the project's `docs/releasing.md`, never here.

---

## Distribution Types

| Type | Module format | Consumers |
|------|---------------|-----------|
| ESM-only | `"type": "module"`, no `require` condition | Node >= 20.19, bundlers, evergreen runtimes |
| Dual ESM+CJS | separate `.mjs`/`.cjs` builds behind conditional exports | legacy Node or entrenched CJS user base |
| Workspace multi-package | several packages from one pnpm workspace | union of each member's consumers |

New packages are ESM-only. Dual format only on explicit user instruction naming the legacy consumer.

## All Distributions

- `"engines.node": ">=20"` in every package. tsconfig target and lib match this floor. The floor raises only on explicit user instruction.
- A version published to npm is burned. Never unpublish and re-upload under the same version; bump instead.
- Quality gate green before the version-bump commit: formatter, linter, type checker, tests.
- Version bump, lockfile update, and dependent-pin updates land in one commit.
- Package contents via `files: ["dist"]` allowlist. Never `.npmignore`.
- Before publish, every package passes: `npm pack --dry-run` content inspection, `publint`, `attw --pack .` (profile `esm-only` for ESM-only packages).
- `prepublishOnly` runs build, publint, and attw. A publish from an unbuilt tree fails.

## ESM-only Packages

- `exports` map per entry: `"types"` first, `"default"` last. No `"require"` condition.
- `"./package.json": "./package.json"` exported for tooling.
- Build: tsc for unbundled packages; tsdown for bundled ones. Declarations (`.d.ts`) always shipped.

## Dual ESM+CJS Packages

- Conditional exports per entry: `"types"`, `"import"` (`.mjs`), `"require"` (`.cjs`), `"default"` last. Order is most-specific first; Node matches object order.
- One build produces both formats plus declarations (tsdown `--format esm,cjs --dts`).
- attw clean under node16 resolution in both modes. No masquerading verdicts.
- Dual-package hazard: no module-level singleton state; a consumer may load both instances.

## Workspace Multi-Package

- A new package is created only when content is (a) optional for the main package, (b) a separate product, or (c) format- or platform-separate. Growth of the main product goes into the existing package.
- Versioning through changesets: every user-visible change adds a changeset file; `changeset version` bumps packages and internal-dependency ranges; `changeset publish` publishes changed packages and tags.
- Version streams are decoupled: each member bumps only on its own changes.
- `workspace:*` dependencies are rewritten to real versions at publish. No workspace protocol reaches the registry.

## Release Procedure

Releases run through CI (see Tag-Driven CI). The local steps end at the tag push.

1. Quality gate green.
2. Bump versions (changesets in a workspace; manual bump in a single package); update lockfile; commit.
3. Tag the release commit `v<version>`; in a workspace, `<package>@<version>` per released package.
4. Push the commit and tag. CI builds, validates (publint, attw, pack inspection), publishes with provenance, and finishes after approval.

Manual fallback (CI unavailable): build, run publint and attw on the packed tarball, inspect `npm pack --dry-run`, publish with `npm publish --provenance` from a granular token.

## Tag-Driven CI

- One tag releases one package. The workflow parses the tag and fails when the tag version differs from that package's package.json version.
- Lockfile checked in CI: `pnpm install --frozen-lockfile` / `npm ci`.
- Publish authentication: npm trusted publishing (OIDC) with `permissions: id-token: write`. Provenance is automatic under trusted publishing. No long-lived npm tokens in CI secrets.
- The publish job runs in a CI environment with required reviewers; the final publish waits for manual approval.
- First publish of a name unregistered on the registry is a manual bootstrap; trusted publishing is configured on the package page immediately after.
- Post-publish package settings: require 2FA and disallow tokens.
