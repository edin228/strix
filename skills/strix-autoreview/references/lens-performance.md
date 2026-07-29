# Performance Lens

Review changed realistic hot paths for concrete query amplification, unbounded
work, resource exhaustion, and avoidable repeated I/O.

## Coverage checklist

- **Multiplicity:** Check lists, serializers, loops, relationship traversal,
  rendering, and fan-out for per-item queries, provider calls, parsing, or
  repeated computation. Trace provider or database batches through their apply
  phase and look for per-item lookups or writes that should share one set-based
  batch context. Multiply realistic outer and inner cardinalities, including
  membership or deduplication against a growing list; use set/map membership
  or one batch lookup when the supported path would otherwise become
  quadratic or repeat the same small lookup for every item.
- **Bounds:** Check requests, workers, exports, searches, realtime paths, and
  payloads for pagination, limits, chunking, streaming, and tenant-data growth.
  Follow every cursor, offset, limit, date range, field selection, and batch
  size through proxies and adapters; a bounded caller is not bounded when an
  intermediate boundary drops its controls. Check query-string, header, and
  request-target growth as well as response size, using a body transport when
  supported identifiers can exceed realistic proxy or server limits.
- **Query shape:** Check predicates, joins, ordering, eager loading, and indexes
  against the actual hot-table access pattern and supported input size. Do not
  infer bounded work from a page limit alone: verify default hydration, nested
  relationships, grouped deduplication, status aggregation, and expensive
  subqueries are restricted to the keys and fields the page actually returns.
  Follow exclusion predicates through the query, relationship loader, entity
  normalization, and serializer: filtering rows only after the ORM loaded
  their nested relationships does not bound database work or memory. Check
  payload entity tables for the same hidden rows. Likewise, a bounded sync
  must not preload an entire tenant history merely to deduplicate its current
  window.
- **Repeated I/O and CPU:** Check whether database/provider calls, parsing,
  sorting, aggregation, serialization, or rendering repeat when one
  current-scope computation preserves behavior. Inspect helper loops for
  growing-list membership tests, repeated scans, and per-item owner lookups
  even when the surrounding caller is nominally batched.
- **Client delivery and rendering:** Check static import reachability across
  mutually exclusive desktop/mobile or editor/viewer variants, and check DOM
  or computation growth for Cartesian and whole-dataset rendering. A runtime
  conditional does not remove an import from the client bundle.
- **Runtime resources:** Check connection-pool and concurrency defaults,
  deployment overrides, nested session needs, memory, file descriptors, and
  payload growth under realistic service load.
- **Failure mode:** Establish whether the cost produces meaningful latency,
  timeout, resource exhaustion, or operational impact rather than only a
  theoretical inefficiency.

Use unchanged schemas, serializers, query plans, relationship definitions, and
call frequency only to establish the actual multiplicative cost.

## Calibration boundaries

Serializing nested relationships from a detail query without eager loading is
a material true-positive pattern when each relationship can lazy-load per
entity. A constant-size settings lookup, bounded detail response, or small
local array pass is not a blocker merely because it could be made microseconds
faster.

## Exclude

- Micro-optimizations without evidence of a hot path, meaningful input size, or
  user/operational impact.
- Indexes, caching, memoization, batching, or pagination added for hypothetical
  future scale.
- Complexity preferences or benchmark requests that do not identify a
  concrete regression introduced or exposed by the change.
- Reliability, migration, security, or UI-polish critique unless it directly
  proves the performance failure.
