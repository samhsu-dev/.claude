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

## Granularity

The unit of work — request, job, task, consumed message — is the anchor for log granularity, not the function or the line.

- Every unit of work emits one summary record at completion carrying its identifiers, outcome, and duration.
- The summary record is emitted on every exit path: success, handled failure, abort.
- Every call to an external system (network, database, subprocess) is recorded with target, duration, and result — as its own record or as fields on the unit-of-work summary.
- Records report completed outcomes. A start record whose only field is the operation name is TRACE. Exception: an operation that can hang or crash mid-work logs start at INFO, so the absence of its completion record is diagnosable.

## Error Records

- A failure is logged exactly once, at the layer that handles it. A layer that propagates an error never logs it.
- Propagation sites attach context (operation, parameters, entity IDs) to the error object; context reaches the handling boundary inside the error, not as log records.
- Every ERROR record carries the exception type and stack trace, the operation attempted, and the inputs and state needed to reproduce the failure.
- Every ERROR record carries the identifiers of the affected unit of work and entities.
- A failed unit's summary record carries the error identifier, linking summary to failure detail.

## Correlation

- Every record emitted within a unit of work carries that unit's correlation ID.
- The system boundary accepts an inbound correlation ID and generates one when absent.
- The correlation ID propagates across every boundary the work crosses: outbound calls, queue messages, background jobs, spawned processes.
- When tracing is active, the trace ID is the correlation ID; records carry trace and span IDs.

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
- Every record is interpretable alone: event type, affected entities, and outcome, without reading adjacent records.
- An operation that can fail or block carries outcome and duration on its record.
- High-cardinality identifiers — request ID, user ID, entity IDs — are record fields. Cardinality is never a reason to omit an identifier.
- Context established at the unit-of-work boundary is bound once and carried on every record within that unit. Call sites add only event-specific fields.
- One canonical field name per concept. The same identifier never appears under two keys.
- No secrets, credentials, tokens, or PII in any record.
