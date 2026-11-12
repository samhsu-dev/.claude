---
paths:
  - "**/*.{py,ts,tsx,js,jsx,go,rs,java,cpp,c,cs,rb,swift,kt,php}"
---

# Code Quality Standards

Language-specific naming, formatting, idioms, and complexity thresholds: see project `.claude/rules/code/quality.md`.

## Control Flow

- Use guard clauses and early returns. Maximum two indentation levels in a function body.
- In a loop, a guard condition uses `continue`; no nested `if` around the loop body.
- Use `break` when the loop stopping condition holds.
- A boolean parameter that selects between two behaviors, each with its own callers, becomes two functions.
- No flag variables tracking state across a loop — extract to function or use early exit.

## Error Handling

- Specific exception/error types. No broad catches.
- Handle an error at the layer that can recover or report the operation failure.
- Error context and logging: `code/logging.md` Error Records.
- Detect an error at the earliest point and raise or throw there, including a missing required internal value. Never disguise failure as an empty value, fallback or degradation. No result and failure are distinguishable by type. Documented recoverable sub-tool output follows `resource-bounds.md`.
- Every catch re-raises, reports at its handling boundary, or raises another exception carrying the caught one as its cause.
- No error codes as return values. Exception: a tool protocol that requires structured success/error objects uses that protocol.

## Code Structure

- Functions under 20 lines.
- Max 3 parameters per function. More → introduce a parameter object.
- A statement sequence that the function's doc or a design doc names as one step is its own function named for that step.
- Single-letter names only for loop indices, the parameter of a one-line lambda or comprehension, and type parameters.
- Call only own methods, parameter methods, locally created objects, direct attributes.
- No duplicate logic blocks. Two identical blocks → extract function.
- A function that reads one object's fields more than its own belongs with that concept. For a data-only type, put the function in the module that owns it; API Design governs data holders.
- A group of two or more arguments or fields passed together at two or more call sites becomes a type.

## No Stale Code

- No dead code. No commented-out code.
- No compatibility stubs. Removed API = removed everywhere.
- No historical references in docstrings or comments.
- Remove artifacts with no surviving code, design, build or entry-point consumer.

## Code Smells — Detect and Eliminate

- No primitive obsession — raw strings/ints representing domain concepts → wrap in a type.
- No god objects — a class with >7 public methods or >5 fields → split responsibilities. File splitting follows `code/organization.md`.
- No shotgun surgery — one change requires edits in many files → consolidate.
- No speculative generality — abstractions, parameters, or config for hypothetical futures → remove.
- No middle-man classes that only delegate → remove and call target directly.
- No magic numbers/strings. Named constants or enums.
- No repeated conditional logic on the same discriminant → polymorphism or lookup table. Exception: an exhaustive `when` over a sealed data hierarchy in a pass that owns the behavior.

## Bug Prevention

- No command, query or path is built by concatenating an external string; it is passed as a separate argument or parameter.
- A range, slice or index whose bounds come from a parameter or external input is tested at minimum, minimum−1, maximum and maximum+1 (boundary value analysis, `testing.md`).
- Null/None: never assume a return value is non-null without a type guarantee or check.
- Every opened file, connection or lock has a guaranteed close path through the language's scoped resource mechanism.
- Mutation hazard: never mutate a collection while iterating. Never mutate a function argument, except a parameter whose declared type is a mutable collection and whose name and doc comment state that the function fills it.
- String building: use structured formatting. No manual concatenation of user-controlled input.
- Comparison: use value equality for data, identity for singletons only.
- Integer overflow: validate arithmetic on external inputs before use.
- Race condition: shared mutable state requires explicit synchronization or is forbidden.
- Encoding: explicit encoding on every I/O boundary. No implicit platform defaults.

## Resource Management

- Move object construction before a loop when every iteration can share the object and a measurement shows its allocation cost.
- Consult a mechanism's existing valid cache before expensive work.

## Documentation

### Comments

- English.
- Why, not what.

### Docstrings (Public API)

- Doc comments document public declarations; a private or `internal` declaration has no doc comment or a one-line comment.
- Content: summary; constraints; parameters; return value; exceptions.
- No redundancy, no implementation details, no examples.
- Language-standard convention.

## Type Safety

- Type annotations on all parameters and return values.
- Concrete types. No escape types (`Any`, `any`, `Object`, `interface{}`).
- Strict type checking enabled.

## Input Contract & Invariants

- Each public function's allowed input set is stated in its design-doc Function Specification Input and checked at entry; caller misuse raises.
- Single validation point for the allowed input set at the system or trust boundary; a violation raises/throws. Core logic accepts verified data only; never re-validate that data deep inside code.
- Invariants as executable checks, not comments.
- Single access path for optional/variant fields.
- Same violation → same exception type at same layer.

## No Patch-Style Code

- Every change integrates as if written from scratch, within the existing ownership, types and callers; fault location: `workflow/change-policy.md` Correctness and Verification.
- No inline workarounds with `# HACK`, `# FIXME`, `# TODO`, `# WORKAROUND` left in place.
- A conditional branch expresses an input distinction the contract defines.
- No defensive copies inside code operating on boundary-verified data; validation placement: Input Contract & Invariants.

## Agent Maintainability

- Among implementations that satisfy accepted behavior, security and resource constraints, choose the one a reader new to the repository changes correctly from its owning documents and identifiers alone.
- Every concept a change adds or changes links to its owning document section, its identifier, its mechanism and a behavioral test. The site list sent with the diff names those four links per concept; a missing link is a finding.
- A reviewer resolves each link from the repository alone. A link that needs the author's conversation to resolve is a finding.

## Tool Enforcement

- A rule that an established analyzer, formatter, linter, type checker or architecture test can check is enforced by that tool in the build or gate. The tool runs at zero new findings over a recorded baseline. Review and agent checks cover only what no configured tool checks.
- Before adding a review item or an agent check step, look for an established tool rule that covers it, starting with the language's standard analyzer rule sets. The run that proposes a tool rule runs it on the codebase and enables it in the same change when every finding is fixed or recorded in the baseline file in that change.
- When a review finds a defect class that a tool rule could catch, enabling that rule goes into the same change or into a recorded follow-up.
- A passing tool result is evidence: neither review nor an agent rereads code to recheck what a passing configured tool already checked.

## Post-Edit Verification

- The self-check of skill `chain-session` applies Code Structure, Code Smells, Bug Prevention, No Patch-Style Code and Agent Maintainability to the diff.

## API Design

- Sibling service interfaces are reviewed together.
- A call reads without its declaration. A literal whose meaning the call does not show (a bare `true`, `false`, `null` or number) is passed by name, or its parameter becomes an enum or an options type.
- A setting has a default that serves the common case, so a caller it does not concern never names it.
- A signature names what its function's job needs. A parameter, field or setting enters an interface in the change that adds its first reader; a value threaded through signatures that nothing reads is speculative generality.
- One concern has one mechanism. Before adding a parameter style, options type, dispatch, registry, result or error shape, find how sibling code handles the same concern and reuse it; a genuine difference is named in the design document.
- One service has one interface. A function or algorithm is reached through one entry; a second entry offering the same service merges into the owner the design names, and its callers move to that owner. An old and a new implementation coexist only during a recorded migration whose task removes the old one.
- Components of one kind share one interface shape: construction, entry verbs, parameter order, input and result conventions, synchronous or asynchronous invocation, completion and cancellation ownership, and glossary vocabulary. Name and justify a component-specific difference in the design document.
- Data holders hold data. No embedded behavior.
- Application logic lives in named functions; no logic in initializers, property getters with side effects or reflection.

- Call core module APIs directly. No wrapping layers around controlled code.
- Keep infrastructure dependencies outside core API contracts; boundaries own infrastructure adapters.
- Core API contracts expose domain operations and results; implementation data structures and intermediate steps are exposed only when a documented caller scenario requires them.
