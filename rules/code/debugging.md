---
paths:
  - "**/*.{py,ts,tsx,js,jsx,go,rs,java,cpp,c,cs,rb,swift,kt,php}"
  - "**/*test*"
---

# Debugging Standards

## Investigation Method

1. Reproduce the failure with a minimal case.
2. Read the full exception chain (`raise ... from exc`) to identify the origin.
3. Narrow scope: isolate whether the fault is in input, logic, or external dependency.
4. Verify assumptions with assertions or print/log at the boundary, not in the middle.
5. Fix the root cause. Never patch symptoms.

## Logging

- Log at module boundaries (entry/exit of public functions), not inside inner loops.
- Log levels: `debug` for flow tracing, `info` for state transitions, `warning` for recoverable issues, `error` for failures.
- Include structured context (function name, key parameters, IDs). No bare messages.
- No sensitive data in logs (credentials, tokens, PII).
- Debug logging is internal. Not exposed in public API.

## Error Diagnosis

- Read the full traceback before changing code.
- Check the exception type and its fields, not just the message string.
- When a test fails, verify the test is correct before changing the implementation.
- When an external call fails, verify the input matches the API contract (check `impl.md`).
- No guessing. If the cause is unclear, add a targeted assertion or log to confirm before fixing.
- No silent fallbacks. `map[key] ?: default` on internal mappings masks bugs — throw on missing key.

## Bug Fix Protocol

- Write a minimal failing test that reproduces the suspected bug before changing any source code.
- Run the test to confirm it fails. A passing test means the bug does not exist — do not fix what is not broken.
- Fix the source code. Run the test again to confirm it passes.
- Keep the test as a permanent regression guard. Never delete a bug-reproduction test after the fix.
