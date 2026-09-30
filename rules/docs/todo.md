---
paths:
  - "**/todo.md"
---

# Rust Task Management

Rust-specific task conventions.

---

## Quality Gate

Every task ends with:
- [ ] cargo fmt --all -- --check
- [ ] cargo clippy --all-targets --all-features -- -D warnings
- [ ] cargo test --workspace --all-features -- all pass
- [ ] RUSTDOCFLAGS="-D warnings" cargo doc --no-deps --all-features

## Conventions

- Design docs by relative path: Depends on: path/to/design.md.
- Test tasks name the test file: tests/<component>.rs for integration tests; the source file holding the `#[cfg(test)]` module for unit tests.
- Implementation tasks reference impl.md for crate findings and required features.
