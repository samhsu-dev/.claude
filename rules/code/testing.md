---
paths:
  - "**/*test*"
  - "**/tests/**"
---

# Rust Testing

Rust / `cargo test` conventions with `rstest`.

---

## Test Design (Rust)

rstest implementation of black-box test design:

### Equivalence partitioning + boundary analysis via `#[case]`
```rust
#[rstest]
#[case(0, false)]  // below minimum
#[case(1, true)]   // minimum boundary
#[case(6, true)]   // nominal (one per valid partition)
#[case(12, true)]  // maximum boundary
#[case(13, false)] // above maximum
fn validate_month_boundaries(#[case] month: u8, #[case] valid: bool) {
    assert_eq!(validate_month(month).is_ok(), valid, "month {month}");
}
```

---

## Layout

| Kind | Location | Sees |
|------|----------|------|
| Unit | `#[cfg(test)] mod tests { use super::*; }` at the bottom of the source file | private items |
| Integration | `tests/<component>.rs`, one crate per file | public API only |
| Doc | `# Examples` blocks in `///` docs | public API only |
| Shared helpers | `tests/common/mod.rs`, declared with `mod common;` in each test file | -- |
| Test data | `tests/data/`, path built with `concat!(env!("CARGO_MANIFEST_DIR"), "/tests/data/<file>")` | -- |

- Test file names carry no `test_` prefix: `tests/parser.rs`. Overrides the global `test_<component>` name; Cargo names the test binary after the file.
- `tests/` is flat: Cargo compiles only top-level `tests/*.rs` as test crates; a subdirectory is a module, not a test. Overrides the global source-mirroring layout.
- Unit tests cover private functions and edge cases. Integration tests exercise the public API as a consumer.
- A binary-only package has no integration-testable surface: logic lives in `src/lib.rs` (`rules/code/organization.md`).

## Naming

- Test functions: `<condition>_<expected_outcome>` in `snake_case`, no `test_` prefix: `empty_input_returns_none`, `month_zero_is_error`. Overrides the global `test_<component>_<condition>_<expected>` name; the `tests` module path and `cargo test` output already carry the component and the test marker.
- Test functions live inside the `tests` module (unit) or at the top level of a `tests/` file (integration). No test classes; a `mod` groups one behavior family.

## Assertions

- `assert_eq!(actual, expected)` / `assert_ne!`. Both operands implement `Debug`.
- `assert!(matches!(value, Pattern { .. }))` for enum variants; `assert_eq!` on the whole value when it implements `PartialEq`.
- Error path: `let err = f().unwrap_err(); assert!(matches!(err, Error::Kind { .. }));`. Never `assert!(f().is_err())` alone.
- A test returning `Result<(), E>` uses `?` for setup only. The assertion under test is an `assert!` macro.
- `#[should_panic(expected = "<substring>")]` only for a documented `# Panics` contract.
- Floats: `assert!((actual - expected).abs() < EPSILON)`. No `assert_eq!` on floats.
- `unwrap` / `expect` are permitted in test code (`clippy.toml` `allow-unwrap-in-tests`, `rules/code/quality.md`).

## Fixtures

- `#[fixture]` functions (`rstest`) for shared setup, injected by parameter name.
- `tempfile::tempdir()` for filesystem tests. The `TempDir` is bound with `let dir = ...` for the test's lifetime; dropping it removes the directory. Never `let _ = tempdir()`.
- No `static` shared mutable state between tests: tests run on parallel threads.
- Never set environment variables in tests: `std::env::set_var` is `unsafe` in edition 2024 and races across threads. Pass values explicitly (`rules/code/constants.md`).
- Mocks: a trait at the boundary the design doc marks as external, mocked with `mockall` `#[automock]`. No mocking of crate-internal types.
- Fixtures return fresh values. No shared mutable state.

## Parametrize

- `#[rstest]` + `#[case(...)]` for data-driven tests.
- `#[values(...)]` for cartesian products.
- `#[ignore = "<reason>"]` for tests needing an external resource; run with `cargo test -- --ignored`.

## Execution

- `cargo test --workspace --all-features` -- all tests.
- `cargo test --no-fail-fast` -- keep running after a failing test binary.
- `cargo test -p <crate>` -- one crate. `cargo test --lib` / `--doc` / `--test <name>` -- one target.
- `cargo test <substring>` -- name match. `cargo test <name> -- --exact` -- one test.
- `cargo test -- --nocapture` -- show output of passing tests.
- `cargo test -- --test-threads=1` -- diagnose test interference only. Never in CI.
- `cargo llvm-cov --workspace --all-features` -- line coverage.

## Configuration

- `[dev-dependencies]`: `rstest`, `tempfile` in every crate with tests; `mockall` when a mocked boundary exists. Added with `cargo add --dev <crate>`.
- No `[[test]]` tables. No custom test harness.
