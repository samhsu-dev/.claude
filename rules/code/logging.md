---
paths:
  - "**/*.{py,ts,tsx,js,jsx,go,rs,java,cpp,c,cs,rb,swift,kt,php}"
---

# Logging Standards

Language-specific logger APIs and configuration: see project `.claude/rules/`.

## Severity Levels

Assign level by actionability, not by code location.

| Level | Emit when |
|-------|-----------|
| FATAL | Process cannot continue; crash imminent. |
| ERROR | Operation failed; needs human intervention. |
| WARN | Anomaly that does not stop the operation. |
| INFO | State transition a reader follows in normal operation: start, end, resource loaded, milestone reached. |
| DEBUG | Diagnostic detail for one decision, still human-readable in volume. |
| TRACE | Full execution flow; off by default. Frequency limits follow High-Frequency Paths. |

- Test before emit: a WARN or ERROR record whose loss hides no problem is lowered one level.
- Expected-success outcomes are not WARN or ERROR.

## Granularity

A unit of work is a request, job, task or consumed message.

- Every unit of work emits one summary record at completion carrying its identifiers, outcome, and duration on every exit path: success, handled failure, abort.
- Every call to an external system (network, database, subprocess) is recorded with target, duration, and result — as its own record or as fields on the unit-of-work summary.
- Records report completed outcomes. A start record whose only field is the operation name is TRACE. Exception: an operation that calls an external process or network, or runs under a resource bound of `code/resource-bounds.md`, logs its start at INFO, so the absence of its completion record is diagnosable.

## Error Records

- A failure is logged exactly once, at the layer that handles it. A layer that propagates an error never logs it.
- Propagation sites attach context (operation, parameters, entity IDs) to the error object; context reaches the handling boundary inside the error, not as log records.
- Every ERROR record carries exception type, stack trace, operation, parameters, and reproducible inputs and state.
- A failed unit's summary record carries the error identifier, linking summary to failure detail.

## Correlation

- Every record emitted within a unit of work carries that unit's correlation ID.
- The system boundary accepts an inbound correlation ID and generates one when absent.
- The correlation ID propagates across every boundary the work crosses: outbound calls, queue messages, background jobs, spawned processes.
- When tracing is active, the trace ID is the correlation ID; records carry trace and span IDs.

## Output Control

- Routing, files, rotation and retention live in environment and handler configuration, never in code.
- Application code never sets a third-party logger's level; levels live in environment and handler configuration.
- Every file sink has a size or rotation bound. No unbounded log file.

## High-Frequency Paths

- Outside the TRACE exception below, log state transitions, not iterations; a record emitted once per call of a function that a loop calls is a per-iteration record.
- Aggregate at loop exit. Exception: per-iteration diagnostics use TRACE with the frequency bound below, never DEBUG.
- Rate-limit or sample repeatable diagnostics above one record per second. Required unit summaries and failure outcomes remain complete.

## Record Content

- Structured key-value records. No string concatenation of fields.
- One event per record. No multi-line narrative.
- Every record is interpretable alone: event type, affected entities, and outcome, without reading adjacent records.
- An operation that can fail or block carries outcome and duration on its record.
- High-cardinality identifiers — request ID, user ID, entity IDs — are record fields. Cardinality is never a reason to omit an identifier.
- Context established at the unit-of-work boundary is bound once and carried on every record within that unit. Call sites add only event-specific fields.
- One canonical field name per concept. The same identifier never appears under two keys.
- No secrets, credentials, tokens, or PII in any record.
