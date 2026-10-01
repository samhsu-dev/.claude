---
paths:
  - "**/Cargo.toml"
  - "Cargo.lock"
  - ".github/workflows/*.yml"
---

# Rust Release Rules

Release standards by crate type. Project-specific release facts — crate names, artifact inventories, tag names, credential mechanism, identity policy — live in the project's `docs/releasing.md`, never here.

---

## Crate Types

| Type | Contents | Artifacts |
|------|----------|-----------|
| Library crate | `src/lib.rs`, consumed as a `Cargo.toml` dependency | `.crate` on crates.io; docs on docs.rs |
| Binary crate | executable installed by end users | `.crate` on crates.io (`cargo install --locked <crate>`) + per-target archives and installers on the GitHub Release |
| Multi-crate workspace | several publishable crates from one workspace | union of each member's artifacts |

## All Crates

- `edition = "2024"` and `rust-version = "<MSRV>"` in every `[package]` (inherited from `[workspace.package]` in a workspace). The MSRV raises only on explicit user instruction; a raise is a minor bump.
- `cargo hack check --rust-version --workspace --all-targets --ignore-private` passes before every release. CI builds on the MSRV toolchain as well as stable.
- `Cargo.lock` is committed for every crate type. CI runs every cargo command with `--locked`.
- A version published to crates.io is permanent. Never re-upload the same version; a broken release is yanked (`cargo yank --version <v>`) and superseded by a new version.
- Quality gate green before the version-bump commit: formatter, linter, tests, doc build (`rules/docs/todo.md`).
- `cargo semver-checks` passes against the last published version before the bump. A reported breaking change forces a major bump (the `y` position while the version is `0.y.z`).
- Version bump, `Cargo.lock` update (`cargo update -w`), and sibling-pin updates land in one commit.
- `[package]` metadata: `description`, `license` (SPDX expression), `repository`, `readme`, `keywords`, `categories`. `documentation` only when the docs are not on docs.rs.
- `[package.metadata.docs.rs]` names the features docs.rs builds (`all-features = true` when no features are mutually exclusive), plus `rustdoc-args = ["--cfg", "docsrs"]` when feature-gated items use `#[cfg_attr(docsrs, doc(cfg(...)))]`.
- `cargo publish --dry-run` and `cargo package --list` reviewed before every publish: the file list holds no test data, CI config, or secrets. `include` / `exclude` trims it.

## Library Crates

- Version stream follows the code: bump on every released change.
- Dependency requirements are caret ranges (`"1.2"`). Never `=x.y.z`: an exact pin in a library blocks version unification in consumers. Exception: a proc-macro companion (below).
- No `Cargo.lock`-dependent behavior: the crate builds with any consumer lockfile satisfying its requirements.

## Binary Crates

- Install path documented as `cargo install --locked <crate>`.
- `--version` prints `CARGO_PKG_VERSION` (clap `#[command(version)]`).
- Per-target archives, installers, and the release workflow come from `dist`: `dist init` writes `dist-workspace.toml` and generates `.github/workflows/release.yml`. The generated workflow is never hand-edited; configuration changes go through `dist init` again.

## Multi-Crate Workspaces

- A new crate is created only when content is (a) a proc-macro (a proc-macro crate exports nothing else), (b) an optional dependency set too heavy for a Cargo feature, or (c) an independent product. Other growth goes into the existing crate behind a feature.
- Internal-only members carry `publish = false`. A published crate never depends on a `publish = false` crate: crates.io rejects a dependency on code outside crates.io (dev-dependencies excepted).
- A proc-macro companion is named `<main>-derive` or `<main>-macros`, re-exported from the main crate, exact-pinned (`=x.y.z`) by it, and versioned in lockstep with it.
- All other version streams are decoupled: each member bumps only on its own changes. The sibling pin changes in the same commit as the sibling's version.
- `cargo publish --workspace` (Rust 1.90+) publishes members in dependency order. On an older toolchain, `cargo publish -p <crate>` per member in dependency order.

## Release Procedure

Releases run through CI (see Tag-Driven CI). The local steps end at the tag push.

1. Quality gate green; `cargo semver-checks` clean; `cargo hack check --rust-version` clean.
2. Bump versions per the type rules; update sibling pins; run `cargo update -w`; commit.
3. Tag the release commit `v<version>` (single crate) or `<crate>-v<version>` (workspace); one tag per crate being released.
4. Push the commit and tag. CI verifies, packages, publishes to crates.io, builds binary artifacts, and creates the GitHub Release after approval.

Manual fallback (CI unavailable): `cargo publish --dry-run`; review `cargo package --list`; `cargo publish --locked -p <crate>` in dependency order.

## Tag-Driven CI

- One tag releases one crate. The workflow parses the tag and fails when the tag version differs from that crate's `[package].version`.
- Gate job before publish: `cargo fmt --all -- --check`, `cargo clippy --all-targets --all-features -- -D warnings`, `cargo test --workspace --all-features`, `RUSTDOCFLAGS="-D warnings" cargo doc --no-deps`, `cargo hack check --rust-version`, `cargo semver-checks`.
- Publish credentials are CI environment secrets. The credential mechanism (registry API token or crates.io trusted publishing) is a project decision recorded in the project's `docs/releasing.md`.
- Trusted publishing on GitHub Actions: the job declares `permissions: id-token: write`, runs `rust-lang/crates-io-auth-action@v1`, and passes its short-lived token as `CARGO_REGISTRY_TOKEN`; no long-lived registry token in repository secrets.
- The publish job runs in a GitHub environment with required reviewers; the final publish waits for manual approval.
- First publish of a new crate name uses a user token: a trusted publisher is configured on crates.io only for an existing crate (repository owner, repository name, workflow file name, environment name).
- Binary crates: the `dist`-generated `release.yml` builds per-target archives on the tag and attaches them to the GitHub Release.
