---
paths:
  - "**/README.md"
---

# TypeScript README Badges

Extends global `readme.md`. Badge set, format, and placement for npm
packages. Overrides the global **Badges** bullet for TypeScript projects.

---

## Principle

- Every badge reports a live fact a reader acts on in the adopt decision: installable version, runtime compatibility, quality signal, legal terms, citation.
- A badge value is pulled from a backing service and reflects current state. A hand-set or decorative badge (static version, tech logo, "PRs welcome", "made with") is forbidden.
- Value test before adding a badge: name the reader question it answers and the action its value changes. No question, no badge.

## Placement

- Badges occupy one row immediately below the title, before the description. Overrides the global "after description, before install" placement.
- One blank line above and below the row.
- One row only. A second row is a badge wall, forbidden by global `readme.md`.

## Badge Set

Order left to right. A badge is present only when its Backing-State gate holds.

| # | Badge | Reader question | shields.io source | Link target |
|---|-------|-----------------|-------------------|-------------|
| 1 | npm version | latest installable version? | `npm/v/<pkg>` | `https://www.npmjs.com/package/<pkg>` |
| 2 | Node versions | runs on my runtime? | `node/v/<pkg>` | npm package page |
| 3 | Coverage | test depth? | `endpoint?url=<coverage-badge.json>` | coverage report |
| 4 | CI build | is `main` green? | `github/actions/workflow/status/<org>/<repo>/<wf>.yml` | Actions page |
| 5 | License | may I use it? | `github/license/<org>/<repo>` | `./LICENSE` |

Optional, after License, present only when its question applies:

- DOI — how to cite? — `badge/DOI-<doi>-blue` linking to the Zenodo or publisher record. Present when a released paper or dataset DOI exists.

Excluded as low-information: download counts, bundle-size, code-style/logo badges, "PRs welcome". Each restates no live adopt-decision fact.

## Backing-State Gate

- A badge appears only after its backing service returns real status. A badge rendering `invalid`, `unknown`, or `no status` is forbidden (global: no broken links).
- npm and Node-versions badges: present only after the package is published to npm. Absent for a package marked `"private": true`.
- Node-versions badge additionally requires `engines.node` in the published package.json; shields reads it from the registry.
- Coverage badge: value comes from the CI coverage run (`vitest run --coverage`, json-summary reporter, field `total.branches.pct`). A CI workflow on `main` writes a shields `endpoint` JSON from that value and hosts it in-repo. No third-party coverage service.
- Coverage and CI badges: present only after that workflow runs on `main`.
- Pre-publication package: shows License only. No placeholder badge for a not-yet-live metric.

## Values

- `<pkg>` is `"name"` in package.json. Scoped names URL-encode the slash: `@scope%2Fname`.
- `<org>/<repo>` is the GitHub slug from `git remote get-url origin`.
- `<wf>` is the workflow file name under `.github/workflows/`.

## Format

- `[![<alt>](<shields-url>)](<target-url>)`. Every badge is a link; no bare image.
- `<alt>` names the metric: `npm`, `node`, `coverage`, `CI`, `License`.
- shields.io is the source. The coverage badge uses shields `endpoint` reading the repo-hosted coverage JSON; no third-party coverage service.
