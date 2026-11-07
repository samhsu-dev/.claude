---
paths:
  - "**/*.kt"
  - "**/*.java"
---

# JVM Performance (Kotlin and Java)

JVM engineering cost: allocation, garbage collection, boxing, retention, locking and JIT behavior. This cost is separate from algorithm cost. Growth dimensions and retained-state bounds belong to the algorithm and follow global `workflow/change-policy.md` Early Cost Checks and `code/resource-bounds.md`.

---

## Responsibility

- The implementer applies Structural Choices below in every Kotlin or Java edit, and a reviewer checks them in the diff. Both judge the code as an experienced JVM engineer would.
- Profiling-driven tuning is its own task, scheduled after the algorithm it measures is complete. An algorithm task does no tuning beyond Structural Choices and adds no complexity for speed without a measurement.

## Structural Choices

These choices are expensive to change later, so they are made when the code is written.

- Hot paths: in a loop over graph entities, labels or IDs, avoid boxed `Int`/`Long` keys and a wrapper object per element when a primitive array or an existing primitive-keyed structure fits. Elsewhere the clearest form wins.
- Allocation: a per-entity inner loop builds no intermediate collection per step. A collection is never copied (`toList()`, `toSet()`) only to iterate it. A sequence or stream replaces a multi-step collection chain only under `code/quality.md` Collections, which requires a measurement. Size a collection up front when its size is known.
- Retention: every cache, memo or index has a stated bound or an owner whose end releases it. A listener is removed when its owner closes. Analysis data lives in no `object`, `companion object` or top-level mutable state, and a `ThreadLocal` is removed after use.
- Locks and resources: release them on every exit path, through `withLock`, `use` or `finally` (Java: try-with-resources or `finally`), including `StackOverflowError` and `OutOfMemoryError` unwinding. Never hold a lock across a call whose depth grows with the input.
- Recursion: a traversal whose depth grows with the input uses an explicit stack or `DeepRecursiveFunction`, because the JVM thread stack is fixed.
- Hash keys: a key is immutable and has a cheap, stable `hashCode`. `mutableMapOf()` and `mutableSetOf()` are insertion-ordered (`LinkedHashMap`, `LinkedHashSet`); code that needs no order uses `HashMap()` or `HashSet()`, and output whose order is observable has a defined order.
- Logging: a log message is built only when its level is enabled (a lambda or a guarded call).

## Measurement

- A performance claim names its JVM measurement: JFR or async-profiler for CPU, allocation and lock contention; JMH, with warm-up, forks and every result consumed (returned or passed to `Blackhole`), for a micro-benchmark of a profiled hotspot. A safepoint-biased sampler and a single cold run are not measurements.
- Heap is reported as the peak live heap after GC (JFR or `-Xlog:gc`), never as `Runtime.totalMemory`.
- A merge of a core change compares wall time and peak heap with the integration base on a fixed workload (global `workflow/change-policy.md` Correctness and Verification). Both sides run on the same JDK, flags and `-Xmx`, with several runs per side and their spread reported. That comparison guards against regressions; it is not tuning.
