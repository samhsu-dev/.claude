---
paths:
  - "**/*.{py,ts,tsx,js,jsx,go,rs,java,cpp,c,cs,rb,swift,kt,php}"
---

# Logging Standards

Language-specific logger APIs and configuration: see project `.claude/rules/`.

## Severity Levels

Assign level by actionability, not by code location. Levels follow OpenTelemetry / Syslog (RFC 5424) ordering.

| Level | Emit when |
|-------|-----------|
| FATAL | Process cannot continue; crash imminent. |
| ERROR | Operation failed; needs human intervention. |
| WARN | Anomaly that does not stop the operation; the signal a search or scan exists to surface. |
| INFO | State transition a reader follows in normal operation: start, end, resource loaded, milestone reached. |
| DEBUG | Diagnostic detail for one decision, still human-readable in volume. |
| TRACE | Full execution flow; off by default. Per-iteration success records belong here, never DEBUG. |

- Test before emit: a record whose loss hides no problem is one level too high.
- Expected-success outcomes are not WARN or ERROR.

## Output Control

- Code emits events. Routing, files, rotation, and retention are environment and handler config, not code.
- Never raise a third-party logger's level from inside application code.
- Every file sink has a size or rotation bound. No unbounded log file.

## High-Frequency Paths

- Log state transitions, not iterations. A loop logs when a value flips, not every pass.
- Aggregate at loop exit; never emit one record per iteration.
- Rate-limit or sample any record that can fire more than once per second.
- A record's frequency is set by its caller, not its wording. A per-call summary line ("N passed, M failed") is high-frequency when the function runs in a hot loop. Level it by call frequency, not by whether it reads like a summary.

## Record Content

- Structured key-value records. No string concatenation of fields.
- One event per record. No multi-line narrative.
- No secrets, credentials, tokens, or PII in any record.
