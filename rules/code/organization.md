---
paths:
  - "**/*.rs"
  - "**/Cargo.toml"
---

# Rust File Naming and Organization

Rust realization of global `rules/code/organization.md`. Cargo package layout; module conventions per the Rust reference and API guidelines.

---

## Crate and Module Naming

- Package name (`[package].name`): lowercase, hyphen-separated. Cargo derives the library target name by replacing `-` with `_`. Never set `[lib] name`.
- Module and file names: `snake_case`. A module is named for its concern: `parser`, not `parser_types`.
- A module file is `foo.rs`; its children live in `foo/bar.rs`. No `mod.rs` (clippy `mod_module_files`).
- No `utils`, `helpers`, `common`, `misc` modules (global rule). Exception: `tests/common/mod.rs` (`rules/code/testing.md`).

## Package Layout

Cargo default layout. Repo root holds `Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`, `clippy.toml`, `README.md`, `LICENSE`.

| Package type | Layout | Scaffold |
|--------------|--------|----------|
| Binary: one executable, no library consumers | `src/main.rs` | `cargo new <name>` |
| Library: consumed by other crates | `src/lib.rs` | `cargo new --lib <name>` |
| Application with tests: executable whose logic is integration-tested | `src/lib.rs` (all logic) + `src/main.rs` (entry only) | `cargo new --lib <name>`, then add `src/main.rs` |
| Additional executables | `src/bin/<name>.rs` | manual |

- `tests/`, `benches/`, `examples/` at the package root beside `src/`. Cargo discovers them; no `[[test]]` / `[[bench]]` / `[[example]]` tables.
- One library target per package. Two libraries are two packages in a workspace.

## Multi-Crate Repository

A repo containing multiple crates is a Cargo workspace.

- Root `Cargo.toml` is a virtual manifest: `[workspace]` with `members = ["crates/*"]` and `resolver = "3"`. No `[package]` at the root. One `Cargo.lock` and one `target/` at the root.
- Members live under `crates/<package-name>/`, each with its own `Cargo.toml` and `src/`. Scaffold with `cargo new --lib crates/<name>`.
- The member directory is named after the package, hyphens included. Overrides the global no-dash file-name rule for package directories only; files inside `src/` stay `snake_case`.
- Shared metadata (`edition`, `rust-version`, `license`, `repository`, `authors`) in `[workspace.package]`; members inherit with `<key>.workspace = true`.
- Shared dependency versions in `[workspace.dependencies]`; members declare `<dep> = { workspace = true }`. No version literal in a member manifest.
- Shared lints in `[workspace.lints]`; members declare `[lints] workspace = true`.
- A sibling dependency is declared once in `[workspace.dependencies]` as `<name> = { path = "crates/<name>", version = "<x.y.z>" }`. `version` is mandatory for a publishable member.
- Per-member commands use `-p <name>`: `cargo test -p <name>`, `cargo build -p <name>`.

## Visibility

Public = used by consumers of the crate. Internal = used within the crate.

| Construct | Public | Internal |
|-----------|--------|----------|
| Module | private `mod` with `pub use` re-export in `lib.rs` | private `mod` |
| Type / trait / function | `pub`, reachable from the crate root | `pub(crate)` or private |
| Struct field | `pub` only on plain-data structs | private, with accessor methods |
| Constant | `pub` in its owner module | `pub(crate)` |

- The public API is the set of items reachable from `lib.rs`. A `pub` item in a private module without re-export is internal.
- `pub(crate)` or private. No `pub(super)`, no `pub(in path)`.
- A trait not meant for external implementation is sealed (C-SEALED).
- Additions to a public struct or enum are semver-major unless it is `#[non_exhaustive]` (`rules/docs/design.md`).

## Module Design

- `lib.rs` contains `//!` crate docs, `mod` declarations, and `pub use` re-exports only. No item definitions.
- Types consumers name are re-exported at the crate root. Module paths are an implementation detail.
- Error types in `error.rs`. CLI argument structs in `cli.rs`.

## Entry Points

- `src/main.rs` holds `fn main() -> anyhow::Result<()>` (or `-> ExitCode`) that builds the config (`rules/code/constants.md`), installs the tracing subscriber (`rules/code/debugging.md`), and calls one library function. No other logic.
- Each `src/bin/<name>.rs` follows the same rule.

## Package Data

- Resource files (data, templates) in `data/` at the package root. Templates in `data/templates/`.
- Embedded at compile time via `include_str!` / `include_bytes!`, path relative to the source file. Never read at runtime relative to the current directory or the executable path.
- When `[package].include` is set, it lists `data/**`. `cargo package --list` shows every data file before publish.
