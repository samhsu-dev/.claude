---
paths:
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
- When an external call fails, verify the input matches the API contract (check `implementation.md`).
- No guessing. If the cause is unclear, add a targeted assertion or log to confirm before fixing.
