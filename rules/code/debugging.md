---
paths:
  - "**/*.rs"
  - "**/*test*"
---

# Rust Debugging

Rust-specific debugging tools and patterns.

---

## Tools

- `tracing` macros (`trace!` .. `error!`, `#[instrument]`) for diagnostics that stay in the code.
- `dbg!(expr)` for temporary inspection. Removed before commit (clippy `dbg_macro = "deny"`).
- `RUST_BACKTRACE=1` for panic backtraces; `RUST_BACKTRACE=full` for every frame.
- `cargo test <name> -- --exact --nocapture` -- one test with its output.
- `rust-lldb` / `rust-gdb target/debug/<bin>` -- interactive debugging of a debug build.
- `cargo expand <module>` (cargo-expand) -- macro-expanded source.
- `#[track_caller]` on a function that panics on caller misuse: the panic location names the caller.

## Logging

- Macros record `module_path!()` as the target. No custom `target:`.
- Binary crates install `tracing_subscriber::fmt().with_env_filter(EnvFilter::from_default_env()).init()` once, first thing in `main`. Filter at runtime with `RUST_LOG=<crate>=debug`.
- Library crates never install a subscriber.
- Tests needing log output call `tracing_subscriber::fmt().with_test_writer().try_init()` in a fixture; `-- --nocapture` shows it.

## Common Pitfalls

- `debug_assert!` is stripped in release builds. An invariant that must hold in production uses `assert!` or returns an error.
- Integer overflow panics in debug and wraps in release. Arithmetic that can overflow uses `checked_*`, `wrapping_*`, or `saturating_*` explicitly.
- `let _ = value;` drops immediately. A guard or `TempDir` is bound to a named `_guard` to live until scope end.
- A panic from `unwrap` names no operation; `.context("...")` before `?` does.
- Tests run on parallel threads: a test mutating process state (current directory, environment) races with its neighbours.
- Output of passing tests is captured. `-- --nocapture` reveals it.
