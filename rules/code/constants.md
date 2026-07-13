---
paths:
  - "**/*.kt"
---

# Value Placement

Every named value has exactly one home: constant in code, typed config object, or external data file. Placement follows who changes the value, not its size or type.

---

## Decision Order

Apply in order. First match wins.

1. An operator changes it per run without editing code → run-setting → typed config object.
2. Bulk data that grows or shrinks independently of the consuming logic → data file.
3. Fixed by the algorithm, protocol, or domain with one correct value → constant in code.

## Constants

- Invariants — thresholds, buffer sizes, header names, magic byte lengths, fixed domain sets — are UPPER_SNAKE_CASE constants (`const val` for compile-time values, top-level or companion-object `val` otherwise) in the file that owns the consuming logic.
- Every constant carries a comment stating what fixes its value.
- A constant used by multiple classes has one owner file. Consumers import it.
- Never move an invariant into a config object, properties file, or JSON. A runtime-read invariant loses compile-time type checking, grep discoverability, and same-diff locality with its logic, and turns a fixed value into a misconfiguration surface.

## Run-Settings

- Run-settings — time budgets, concurrency, targets, verbosity, endpoints — live in one immutable `data class` (all properties `val`) per entry point.
- The config object is constructed once at the entry point from CLI arguments, environment, or config file, then passed explicitly through the call chain.
- Core logic never reads args, environment variables, or config files. It receives the config object.
- No mutable `object` state and no loose maps for run-settings.
- A liveness backstop deadline is never a run-setting (`resource-bounds.md`).

## Data Files

- Bulk payloads — word lists, lookup tables, fixture-like data — live in external JSON/TOML/properties resource files, never in Kotlin source. File location: `rules/code/organization.md` Resources.
- A data file is loaded at one boundary and validated into typed structures. Core logic receives typed data, never raw parse output.

## Promotion

- "An operator might tune it later" does not make a value a run-setting. A value is a run-setting when a concrete run requires a different value without a code change.
- Promotion keeps the constant as the default: the config field defaults to the in-code constant.
- A config field no run overrides returns to a constant.
