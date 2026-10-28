---
paths:
  - "**/*.{py,ts,tsx,js,jsx,go,rs,java,cpp,c,cs,rb,swift,kt,php}"
---

# Code Quality Standards

Language-specific naming, formatting, idioms, and complexity thresholds: see project `.claude/rules/code/quality.md`.

## Control Flow
- Use guard clauses and early returns. Maximum two indentation levels in a function body.
- `continue` over nested `if` in loops.
- Use `break` when the loop stopping condition holds.
- No boolean parameters that switch behavior — split into two functions.
- No flag variables tracking state across a loop — extract to function or use early exit.

## Error Handling
- Specific exception/error types. No broad catches.
- Handle an error at the layer that can recover or report the operation failure.
- Error context and logging: `code/logging.md` Error Records.
- Detect and report errors at the earliest point. Raise or throw on failure, including a missing required internal value. Never disguise failure as an empty value, fallback or degradation. Documented recoverable sub-tool output follows `resource-bounds.md`.
- Every catch re-raises, reports at its handling boundary, or transforms the error. Logging follows `code/logging.md`.
- No error codes as return values. Exception: a tool protocol that requires structured success/error objects uses that protocol.

## Code Structure
- Functions under 20 lines.
- Max 3 parameters per function. More → introduce a parameter object.
- Put each multi-step operation in a function named for that operation.
- Names state the domain concept or responsibility. Single-letter variables are limited to comprehensions, loop indices and language-profile type parameters.
- Internal imports follow language convention.
- Call only own methods, parameter methods, locally created objects, direct attributes.
- No duplicate logic blocks. Two identical blocks → extract function.
- A function that reads one object's fields more than its own belongs with that concept. For a data-only type, put the function in the module that owns it; API Design governs data holders.
- Repeated groups of arguments or fields passed together become a type. The parameter-count limit above still applies.

## No Stale Code

- No redundant indirection.
- No dead code. No commented-out code.
- No compatibility stubs. Removed API = removed everywhere.
- No historical references in docstrings or comments.
- Indirection follows Code Smells and API Design.
- Remove artifacts with no surviving code, design, build or entry-point consumer.

## Code Smells — Detect and Eliminate
- No primitive obsession — raw strings/ints representing domain concepts → wrap in a type.
- No god objects — a class with >7 public methods or >5 fields → split responsibilities. File splitting follows `code/organization.md`.
- No shotgun surgery — one change requires edits in many files → consolidate. Duplicate facts retain one owner.
- No speculative generality — abstractions, parameters, or config for hypothetical futures → remove.
- No message chains — `a.b().c().d()` → encapsulate in a method on `a`.
- No middle-man classes that only delegate → remove and call target directly.
- No magic numbers/strings. Named constants or enums.
- No repeated conditional logic on the same discriminant → polymorphism or lookup table.

## Bug Prevention
- Check for string injection.
- For every range, slice, and index operation, apply boundary value analysis from `testing.md`.
- Null/None: never assume a return value is non-null without a type guarantee or check.
- Every opened file, connection or lock has a guaranteed close path through the language's scoped resource mechanism.
- Mutation hazard: never mutate a collection while iterating. Never mutate function arguments.
- String building: use structured formatting. No manual concatenation of user-controlled input.
- Comparison: use value equality for data, identity for singletons only.
- Integer overflow: validate arithmetic on external inputs before use.
- Race condition: shared mutable state requires explicit synchronization or is forbidden.
- Encoding: explicit encoding on every I/O boundary. No implicit platform defaults.

## Resource Management
- Scoped resource use: Bug Prevention.
- No object construction in loop bodies. Move construction before the loop.
- Consult a mechanism's existing valid cache before expensive work. Representation ownership follows `docs/design.md` Design principles.

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
- Controlled-code adapters: API Design.
- No defensive copies inside code operating on boundary-verified data; validation placement: Input Contract & Invariants.

## Post-Edit Verification (Mandatory)
After every code modification, review all changed files for:
1. Check Code Structure and Code Smells.
2. Check Bug Prevention.
3. Check No Patch-Style Code.
Fix every finding before considering the change complete. No exceptions.

## API Design
- Error signaling: Error Handling.
- Data containers hold data. No embedded behavior.
- Application logic as explicit functions.

- Call core module APIs directly. No wrapping layers around controlled code.
- Keep infrastructure dependencies outside core API contracts; boundaries own infrastructure adapters.
