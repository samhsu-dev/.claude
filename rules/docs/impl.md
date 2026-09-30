---
paths:
  - "**/impl.md"
  - "**/impl-*.md"
---

# Rust Implementation Documents

Rust-specific `impl.md` conventions.

---

## API Entry Format

**[crate]** `use crate_name::Thing` -- when/gotcha.

Example:
**[reqwest]** `Client::builder().timeout(Duration::from_secs(10)).build()?` -- no default timeout; omitting it hangs forever.
**[serde]** `#[serde(deny_unknown_fields)]` on config structs -- the default silently ignores misspelled keys.

## Crate Entry Format

- crate_name >= version -- purpose. `cargo add crate_name`. `cargo add --dev` for test-only crates.

## Feature Flags

- Every entry names the Cargo features it requires: `cargo add tokio --features rt-multi-thread,macros`. A feature omitted from `impl.md` is a compile error found late.
