---
paths:
  - "**/*.{py,ts,tsx,js,jsx,go,rs,java,cpp,c,cs,rb,swift,kt,php}"
---

# Code Quality Standards

## Control Flow
- Early returns over nested conditionals.
- Guard clauses to minimize nesting. Max 2 levels of indentation in function body.
- `continue` over nested `if` in loops.
- `break` on condition.
- Flat logic. No deep nesting.
- No boolean parameters that switch behavior — split into two functions.
- No flag variables tracking state across a loop — extract to function or use early exit.

## Error Handling
- Specific exception/error types. No broad catches.
- Errors handled at the appropriate abstraction level.
- Original error context preserved across call chains.
- Error messages include context (function, parameters, state).
- Fail fast. Never return empty values, fall back, or degrade.
- No swallowed exceptions — every catch block re-raises, logs, or transforms.
- No error codes as return values. Raise/throw on failure.

## File Responsibility
- One responsibility per file. All types and functions in a file serve that responsibility.
- Files under 300 lines. Extract a new file when a second responsibility emerges.
- File name reflects the single responsibility it owns.

## Code Structure
- Functions under 20 lines.
- Max 3 parameters per function. More → introduce a parameter object.
- Multi-step logic in dedicated functions.
- Meaningful names. No single-letter variables outside comprehensions and loop indices.
- Internal imports follow language convention.
- Law of Demeter: call own methods, parameters, locally created objects, direct attributes only.
- No duplicate logic blocks. Two identical blocks → extract function.
- No feature envy — a function accessing another object's fields more than its own belongs on that object.
- No data clumps — fields always passed together → group into a type.

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
- Off-by-one: boundary values tested for every range/slice/index operation.
- Null/None: never assume a return value is non-null without a type guarantee or check.
- Resource leaks: every opened resource (file, connection, lock) has a guaranteed close path.
- Mutation hazard: never mutate a collection while iterating. Never mutate function arguments.
- String building: use structured formatting. No manual concatenation of user-controlled input.
- Comparison: use value equality for data, identity for singletons only.
- Integer overflow: validate arithmetic on external inputs before use.
- Race condition: shared mutable state requires explicit synchronization or is forbidden.
- Encoding: explicit encoding on every I/O boundary. No implicit platform defaults.

## Performance
- Context managers / RAII / try-with-resources for resources.
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
- Type annotations on all parameters and return values.
- Concrete types. No escape types (`Any`, `any`, `Object`, `interface{}`).
- Strict type checking enabled.

## Input Contract & Invariants
- Allowed input set defined per function.
- Validated at entry. Violation = raise/throw.
- Invariants as executable checks, not comments.
- Single validation point at boundary. Core logic accepts verified data only.
- Single access path for optional/variant fields.
- Same violation → same exception type at same layer.

## No Patch-Style Code
- Every change integrates as if written from scratch. No "add a check here" band-aids.
- No inline workarounds with `# HACK`, `# FIXME`, `# TODO`, `# WORKAROUND` left in place.
- No conditional branches added solely to handle one caller's edge case — fix the design.
- No adapter/shim layers around code you control — change the source.
- No defensive copies or re-validation deep inside code that already validated at the boundary.

## Post-Edit Verification (Mandatory)
After every code modification, review all changed files for:
1. **Smell scan**: code smells listed above — primitive obsession, duplication, feature envy, data clumps, god objects, magic values, middle-man, speculative generality.
2. **Bug scan**: off-by-one, null safety, resource leaks, mutation hazards, race conditions, encoding assumptions, integer overflow, string injection.
3. **Patch scan**: band-aid fixes, workaround comments, shim layers, redundant validation, caller-specific branches.
Fix every finding before considering the change complete. No exceptions.

## API Design
- Call core module APIs directly. No wrapping layers.
- No infrastructure dependencies.
- Exception-driven error handling.
- Data containers hold data. No embedded behavior.
- Application logic as explicit functions.
