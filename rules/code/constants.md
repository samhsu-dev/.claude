---
paths:
  - "**/*.rs"
---

# Value Placement

Every named value has exactly one home: constant in code, typed config struct, or external data file. Placement follows who changes the value, not its size or type.

---

## Decision Order

Apply in order. First match wins.

1. An operator changes it per run without editing code → run-setting → typed config struct.
2. Bulk data that grows or shrinks independently of the consuming logic → data file.
3. Fixed by the algorithm, protocol, or domain with one correct value → constant in code.

## Constants

- Invariants — thresholds, buffer sizes, header names, magic byte lengths, fixed domain sets — are `const` items in `SCREAMING_SNAKE_CASE` in the module that owns the consuming logic.
- `static` instead of `const` only when the value needs one address or is computed once (`LazyLock`). Never `static mut`.
- Every constant carries a `///` or `//` comment stating what fixes its value.
- A constant used by multiple modules has one owner module, declared `pub(crate)`. Consumers import it.
- Never move an invariant into a config struct, TOML, or JSON. A runtime-read invariant loses type checking, grep discoverability, and same-diff locality with its logic, and turns a fixed value into a misconfiguration surface.

## Run-Settings

- Run-settings — time budgets, concurrency, targets, verbosity, endpoints — live in one `Config` struct per binary target.
- The struct is built once in `main` from CLI arguments (`clap` derive; `#[arg(long, env = "...")]` for environment fallback) or a TOML file deserialized with `serde` and `#[serde(deny_unknown_fields)]`, then passed as `&Config` through the call chain.
- Core logic never reads `std::env::args`, `std::env::var`, or config files. It receives the config struct.
- No `static` globals, no `OnceLock` singletons, and no `HashMap<String, String>` bags for run-settings.
- A liveness backstop deadline is never a run-setting (`resource-bounds.md`).

## Data Files

- Bulk payloads — word lists, lookup tables, fixture-like data — live in external TOML/JSON files, never as literals in Rust source. File location: `rules/code/organization.md` Package Data.
- A data file is embedded with `include_str!` / `include_bytes!` and parsed at one boundary into typed structs. Core logic receives typed data, never raw text.

## Promotion

- "An operator might tune it later" does not make a value a run-setting. A value is a run-setting when a concrete run requires a different value without a code change.
- Promotion keeps the constant as the default: `#[arg(default_value_t = CONSTANT)]` or `#[serde(default = "...")]` returning the constant.
- A config field no run overrides returns to a constant.
