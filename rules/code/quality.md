---
paths:
  - "**/*.rs"
---

# Rust Code Quality

Rust-specific rules and toolchain. Rust API Guidelines (C-* references), Rust Style Guide, edition 2024.

---

## Naming

Rust API Guidelines C-CASE.

| Item | Convention |
|------|------------|
| Crates, modules, functions, methods, locals, macros | `snake_case` |
| Types, traits, enum variants | `UpperCamelCase` |
| Constants, statics | `SCREAMING_SNAKE_CASE` |
| Type parameters | one uppercase letter or `UpperCamelCase` |
| Lifetimes | short lowercase: `'a`, `'de`, `'src` |
| Cargo features | `snake_case`; no `use-` / `with-` prefix |

- An acronym is one word in `UpperCamelCase`: `Uuid`, `HttpClient`. Not `UUID`, `HTTPClient`.
- Conversions (C-CONV): `as_` borrowed to borrowed, free; `to_` borrowed to owned, expensive; `into_` consumes `self`.
- Getters carry no `get_` prefix: `fn name(&self)` (C-GETTER). Exception: `get` / `get_mut` on a keyed collection.
- Iterator methods: `iter`, `iter_mut`, `into_iter`; iterator types named after the method: `Iter`, `IntoIter` (C-ITER, C-ITER-TY).
- Word order matches existing std names: `ParseError`, `parse_json`, `JoinPathsError` (C-WORD-ORDER).

## Formatting

- rustfmt defaults: 100-column width, 4-space indent. No `rustfmt.toml`; rustfmt reads `edition` from `Cargo.toml`.
- `cargo fmt --all` before every commit. Formatting is never hand-adjusted.

## Imports

- Three groups separated by one blank line: `std` / `core` / `alloc`; external crates; `crate` / `super` / `self`. rustfmt sorts within a group.
- `use` declarations before `mod` declarations, both after inner attributes and `//!` docs.
- Types and traits imported by full path; functions called through their parent module: `fs::read_to_string`, not `read_to_string`.
- No glob imports. Exceptions: `use super::*;` in a `#[cfg(test)]` module; a crate's own `prelude` module.
- `pub use` re-exports only in `lib.rs` (`rules/code/organization.md`).

## Error Handling

- Library crate: one enum deriving `thiserror::Error` in `error.rs`, plus `pub type Result<T> = std::result::Result<T, Error>;`. Never `Box<dyn Error>` in a public signature (C-GOOD-ERR).
- Binary crate: `anyhow::Result` in `main` and command handlers. `.context("...")` / `.with_context(|| ...)` at every `?` that crosses a boundary and would otherwise lose the operation name.
- `?` propagates. Never `match` on a `Result` only to return its error.
- Causes stay in the chain via `#[source]` or `#[from]`. Never formatted into the message string.
- `unwrap`, `panic!`, `unreachable!`, `todo!`, `unimplemented!` are forbidden outside tests. `expect("<invariant>")` is permitted when the message states the invariant that makes failure impossible.
- No `std::process::exit` outside `main`. `main` returns `anyhow::Result<()>` or `ExitCode`.

## Idioms

- `Option` / `Result` combinators (`map`, `and_then`, `ok_or`, `unwrap_or_else`) over a `match` with one trivial arm.
- `if let` / `let else` for one pattern. `match` on a crate-local enum has no `_` arm.
- Iterator chains over index loops. `for` over `while` with a counter.
- Parameters: `&str` not `&String`; `&[T]` not `&Vec<T>`; `impl AsRef<Path>` for paths; `impl Into<String>` for owned-string sinks.
- No `bool` parameters: a two-variant enum (C-CUSTOM-TYPE).
- Derives per C-COMMON-TRAITS: `Debug` on every public type; `Clone`, `PartialEq`, `Eq`, `Hash`, `Default` when semantically valid; `Copy` on small plain-data types.
- `#[must_use]` on side-effect-free functions returning a value and on builder methods.
- `#[non_exhaustive]` on public structs and enums that will grow.
- Inline format arguments: `format!("{name}")`. Not `format!("{}", name)`.
- `Arc::clone(&x)` / `Rc::clone(&x)`. Not `x.clone()` on a reference-counted pointer.

## Ownership and Resources

- Resource lifetime by ownership and `Drop`. A `close(self) -> Result` method exists only to surface teardown errors; correctness never depends on the caller invoking it.
- Borrow over clone. A `.clone()` in a hot path carries a comment stating why the borrow is impossible.
- `Arc<Mutex<T>>` / `RwLock` only at concurrency boundaries. Core logic takes `&T` / `&mut T`.
- `unsafe_code = "forbid"`. Exception: an FFI crate, where every `unsafe` block carries a `// SAFETY:` comment (clippy `undocumented_unsafe_blocks`).

## Documentation

- `//!` crate docs in `lib.rs`: one-paragraph purpose and one runnable example (C-CRATE-DOC, C-EXAMPLE).
- `///` on every public item. First line: one sentence, third person, period, no signature repetition.
- Sections in order: `# Examples`; `# Errors` on every `Result`-returning fn; `# Panics` on every fn that can panic; `# Safety` on every `unsafe fn` (C-FAILURE). No `# Arguments` / `# Returns` sections.
- Doctests propagate with `?` inside a hidden `# fn main() -> Result<(), Box<dyn std::error::Error>>` wrapper. Never `unwrap` in a doctest (C-QUESTION-MARK).
- Every referenced item is an intra-doc link: [`Type`], [`module::function`]. Other code names in backticks.
- `#[doc(hidden)]` only on items public for macro expansion. Never to hide API.

## Lints

Declared in `Cargo.toml` (`[workspace.lints]` plus `[lints] workspace = true` per member in a workspace). Never as `#![...]` crate attributes.

```toml
[lints.rust]
unsafe_code = "forbid"
missing_docs = "warn"

[lints.clippy]
all = { level = "warn", priority = -1 }
pedantic = { level = "warn", priority = -1 }
unwrap_used = "deny"
expect_used = "warn"
dbg_macro = "deny"
todo = "deny"
unimplemented = "deny"
undocumented_unsafe_blocks = "deny"
mod_module_files = "deny"
allow_attributes = "deny"
allow_attributes_without_reason = "deny"

[lints.rustdoc]
broken_intra_doc_links = "deny"
missing_crate_level_docs = "warn"
```

- `clippy.toml` at the repo root: `allow-unwrap-in-tests = true`, `allow-expect-in-tests = true`, `allow-panic-in-tests = true`. No `msrv` key: Clippy reads `rust-version` from `Cargo.toml`.
- A lint exception is `#[expect(<lint>, reason = "...")]` on the narrowest item. Never `#[allow]`; never crate-wide `#![allow]`. An `expect` that stops firing is itself a warning, so the exception expires with its cause.
- Restriction-group lints are enabled one by one, as above. Never `restriction = "warn"`.

---

## Quality Workflow

### Before editing
- `cargo clippy --all-targets --all-features` -- check existing violations.

### After editing
- `cargo fmt --all`.
- `cargo clippy --all-targets --all-features -- -D warnings` -- zero warnings.
- `cargo test --workspace --all-features` -- all pass.
- `RUSTDOCFLAGS="-D warnings" cargo doc --no-deps --all-features` -- doc build clean.

---

## Toolchain

`rust-toolchain.toml` at the repo root pins `[toolchain] channel` and `components = ["rustfmt", "clippy"]`.

| Tool | Command | Purpose |
|------|---------|---------|
| rustfmt | `cargo fmt --all` | Formatter |
| clippy | `cargo clippy --all-targets --all-features -- -D warnings` | Linter |
| rustdoc | `cargo doc --no-deps --all-features` | API docs and doc lints |
| cargo test | `cargo test --workspace --all-features` | Unit, integration, and doc tests |
| cargo-llvm-cov | `cargo llvm-cov --workspace --all-features` | Coverage |
| cargo-semver-checks | `cargo semver-checks` | Public API compatibility against the last published version |
| cargo-hack | `cargo hack check --rust-version --workspace --all-targets` | MSRV verification |
| cargo | `cargo add`, `cargo update`, `cargo build` | Package manager |
