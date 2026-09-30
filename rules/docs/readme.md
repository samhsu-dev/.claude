---
paths:
  - "**/README.md"
---

# Rust README Badges

Extends global `readme.md`. Badge set, format, and placement for Rust
crates. Overrides the global **Badges** bullet for Rust projects.

---

## Principle

- Every badge reports a live fact a reader acts on in the adopt decision: installable version, API documentation, toolchain compatibility, quality signal, legal terms, citation.
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
| 1 | crates.io version | latest installable version? | `crates/v/<crate>` | `https://crates.io/crates/<crate>` |
| 2 | docs.rs | is the API documented, does it build? | `docsrs/<crate>` | `https://docs.rs/<crate>` |
| 3 | MSRV | compiles on my toolchain? | `crates/msrv/<crate>` | crates.io page |
| 4 | Coverage | test depth? | `endpoint?url=<coverage-badge.json>` | coverage report |
| 5 | CI build | is `main` green? | `github/actions/workflow/status/<org>/<repo>/<wf>.yml` | Actions page |
| 6 | License | may I use it? | `github/license/<org>/<repo>` | `./LICENSE` |

Optional, after License, present only when its question applies:

- DOI — how to cite? — `badge/DOI-<doi>-blue` linking to the Zenodo or publisher record. Present when a released paper or dataset DOI exists.

Excluded as low-information: download counts (`crates/d/<crate>`), code-style/logo badges, "PRs welcome". Each restates no live adopt-decision fact.

## Backing-State Gate

- A badge appears only after its backing service returns real status. A badge rendering `invalid`, `unknown`, or `no status` is forbidden (global: no broken links).
- crates.io, docs.rs, and MSRV badges: present only after the crate is published to crates.io. Absent for a crate carrying `publish = false`. The MSRV badge reads `[package].rust-version`; absent when that field is unset.
- docs.rs badge: present only after the docs.rs build of the published version succeeded.
- Coverage badge: value comes from `cargo llvm-cov --workspace --all-features --json --summary-only` (field `data[0].totals.lines.percent`). A CI workflow on `main` writes a shields `endpoint` JSON from that value and hosts it in-repo. No third-party coverage service.
- Coverage and CI badges: present only after that workflow runs on `main`.
- Pre-publication crate: shows License only. No placeholder badge for a not-yet-live metric.

## Values

- `<crate>` is `[package].name` in the crate's `Cargo.toml`. In a workspace: the user-facing crate the README describes.
- `<org>/<repo>` is the GitHub slug from `git remote get-url origin`.
- `<wf>` is the workflow file name under `.github/workflows/`.

## Format

- `[![<alt>](<shields-url>)](<target-url>)`. Every badge is a link; no bare image.
- `<alt>` names the metric: `crates.io`, `docs.rs`, `MSRV`, `coverage`, `CI`, `License`.
- shields.io is the source. The coverage badge uses shields `endpoint` reading the repo-hosted coverage JSON; no third-party coverage service.
