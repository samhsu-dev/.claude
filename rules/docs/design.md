---
paths:
  - "**/design.md"
  - "**/design-*.md"
---

# Rust Design Standards

Rust-specific design rules. Rust API Guidelines (C-* references).

---

## Type Selection

- `struct` with private fields for data holders. `pub` fields only on plain-data structs whose every field is independently valid (C-STRUCT-PRIVATE).
- `enum` for finite state and closed variant sets. `#[non_exhaustive]` on public enums and structs that will grow.
- Newtype (`struct Meters(f64);`) for zero-cost type distinctions and validated values (C-NEWTYPE). Validated construction via `TryFrom` or `new(..) -> Result`.
- Trait for behavior with multiple implementations. Generic parameter (`T: Trait`) for static dispatch; `Box<dyn Trait>` for heterogeneous collections and plugin boundaries.
- Builder (`XBuilder` with `build()`) when construction has more than two optional parameters (C-BUILDER).
- Typestate (`Struct<S>` with `PhantomData<S>`) when the design names a state machine whose invalid transitions are compile-time errors.
- `Default` when a zero-argument value is valid; a `new()` with no arguments implies `Default` (clippy `new_without_default`).

## Module Structure

- Visibility, module layout, packaging, package data: `rules/code/organization.md`.
- The design doc records each module's visibility (`pub` or `pub(crate)`) and its crate.

## Value Placement

- Constant vs config struct vs data file: decision order in `rules/code/constants.md`.
- The design doc records the tier of each named value the design introduces.

## Error Design

- One error enum per crate deriving `thiserror::Error` and `Debug`. Variants partition failures by how callers match, not where raised.
- Variant fields are structured (`path: PathBuf`, `line: usize`). No preformatted `String`. Exception: an opaque message from an external system.
- Third-party errors mapped at the boundary into a variant with `#[source]`; `#[from]` only when the mapping is one-to-one and adds no context.
- Misuse errors (caller violated a documented precondition) panic and are listed under `# Panics`. Runtime errors (I/O, parse, external) are `Result`.
- Public error types are `std::error::Error + Send + Sync + 'static` (C-GOOD-ERR).
- The design doc lists each variant, its fields, and the caller decision it enables.

## API Design

- Constructors: `new` for the primary; `with_<param>` for a variant; `From` / `TryFrom` impls for conversions (C-CTOR, C-CONV-TRAITS).
- Accessors: `field()` returns `&T`; `field_mut()` returns `&mut T`. No `get_` prefix (C-GETTER).
- Receivers: `&self` by default; `&mut self` on mutation; `self` on consumption or `into_` conversion.
- Parameters generic over `impl Into<T>` / `impl AsRef<T>` at the public boundary; concrete types in internals.
- No `bool` or `Option<bool>` parameters: an enum (C-CUSTOM-TYPE).
- Standard traits per C-COMMON-TRAITS: `Debug`, `Clone`, `PartialEq`, `Eq`, `Hash`, `Default`; `Display` for user-facing values; `FromStr` for parseable values; `Send + Sync`. The design doc lists derives per type.
- Lazy sequences return `impl Iterator<Item = T>`. `Vec<T>` only when the collection is materialized anyway.
- Side-effect-free functions returning a value are `#[must_use]`.
- Every public item is semver surface: a new variant, field, or trait method without a default is a breaking change unless `#[non_exhaustive]` / a default body applies (`rules/workflow/releasing.md`).

## Typing Patterns

- Trait bounds on `impl` blocks and functions, not on struct definitions (C-STRUCT-BOUNDS).
- Sealed traits for extension-closed traits (C-SEALED): `mod private { pub trait Sealed {} }`.
- `Deref` only for smart pointers. Never for inheritance-style delegation (C-DEREF).
- Associated types for one-to-one type relations; generic parameters for many.
- Lifetimes elided where the rules permit. A named lifetime is documented with what it borrows.
