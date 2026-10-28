---
paths:
  - "**/*.{py,ts,tsx,js,jsx,go,rs,java,cpp,c,cs,rb,swift,kt,php}"
---

# Code Quality Standards

Language-specific naming, formatting, idioms, and complexity thresholds: see project `.claude/rules/code/quality.md`.

## Control Flow
- Early returns over nested conditionals.
- Guard clauses to minimize nesting. Max 2 levels of indentation in function body.
- `continue` over nested `if` in loops.
- `break` on condition.
- No boolean parameters that switch behavior — split into two functions.
- No flag variables tracking state across a loop — extract to function or use early exit.

## Error Handling
- Specific exception/error types. No broad catches.
- Errors handled at the appropriate abstraction level.
- Original error context preserved across call chains.
- Error messages include context (function, parameters, state).
- Fail fast. Never return empty values, fall back, or degrade. Exception: a sub-tool's documented partial or recoverable output is not application degradation — handle it per `resource-bounds.md`.
- No swallowed exceptions — every catch block re-raises, logs, or transforms.
- No error codes as return values. Raise/throw on failure.

## Code Structure
- Functions under 20 lines.
- Max 3 parameters per function. More → introduce a parameter object.
- Multi-step logic in dedicated functions.
- Meaningful names. No single-letter variables outside comprehensions and loop indices.
- Internal imports follow language convention.
- Call only own methods, parameter methods, locally created objects, direct attributes.
- No duplicate logic blocks. Two identical blocks → extract function.
- No feature envy — a function accessing another object's fields more than its own belongs on that object.
- No data clumps — recurring argument clumps become parameter objects; fields always passed together become a type.

## No Stale Code
- No dead code. No commented-out code.
- No compatibility stubs. Removed API = removed everywhere.
- No historical references in docstrings or comments.
- No redundant indirection.
- No orphan artifacts.

## Code Smells — Detect and Eliminate
- No primitive obsession — raw strings/ints representing domain concepts → wrap in a type.
- No god objects — a class with >7 public methods or >5 fields → split responsibilities.
- No shotgun surgery — one change requires edits in many files → consolidate.
- No speculative generality — abstractions, parameters, or config for hypothetical futures → remove.
- No message chains — `a.b().c().d()` → encapsulate in a method on `a`.
- No middle-man classes that only delegate → remove and call target directly.
- No magic numbers/strings. Named constants or enums.
- No repeated conditional logic on the same discriminant → polymorphism or lookup table.

## Bug Prevention
- Check for string injection.
- For every range, slice, and index operation, apply boundary value analysis from `testing.md`.
- Null/None: never assume a return value is non-null without a type guarantee or check.
- Resource leaks: every opened resource (file, connection, lock) has a guaranteed close path.
- Mutation hazard: never mutate a collection while iterating. Never mutate function arguments.
- String building: use structured formatting. No manual concatenation of user-controlled input.
- Comparison: use value equality for data, identity for singletons only.
- Integer overflow: validate arithmetic on external inputs before use.
- Race condition: shared mutable state requires explicit synchronization or is forbidden.
- Encoding: explicit encoding on every I/O boundary. No implicit platform defaults.

## Resource Management
- Use the language's scoped resource mechanism to satisfy the guaranteed close path in Bug Prevention.
- No object creation inside loops. Move allocation outside.
- Cache check before expensive operations.

## Documentation

### Comments
- English.
- Why, not what.

### Docstrings (Public API)
- Public API only. Private: one-line comment.
- Content: summary; constraints; parameters; return value; exceptions.
- No redundancy, no implementation details, no examples.
- Language-standard convention.

## Type Safety
- Type annotations on all parameters and return values. Project rules may specify language-level omissions.
- Concrete types. No escape types (`Any`, `any`, `Object`, `interface{}`).
- Strict type checking enabled.

## Input Contract & Invariants
- Allowed input set defined per function.
- Single validation point for the allowed input set at the system or trust boundary; a violation raises/throws. Core logic accepts verified data only; never re-validate that data deep inside code.
- Invariants as executable checks, not comments.
- Single access path for optional/variant fields.
- Same violation → same exception type at same layer.

## No Patch-Style Code
- Every change integrates as if written from scratch. No "add a check here" band-aids.
- No inline workarounds with `# HACK`, `# FIXME`, `# TODO`, `# WORKAROUND` left in place.
- No conditional branches added solely to handle one caller's edge case — fix the design.
- No adapter/shim layers around code you control — change the source.
- No defensive copies inside code operating on boundary-verified data; validation placement: Input Contract & Invariants.

## Post-Edit Verification (Mandatory)
After every code modification, review all changed files for:
1. Check Code Structure and Code Smells.
2. Check Bug Prevention.
3. Check No Patch-Style Code.
Fix every finding before considering the change complete. No exceptions.

## API Design
- Exception-driven error handling.
- Data containers hold data. No embedded behavior.
- Application logic as explicit functions.
