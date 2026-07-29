# Data Integrity and Reliability Lens

Review changed state transitions and side effects for concrete loss,
corruption, duplication, partial-success, and recovery defects.

## Coverage checklist

- **Persistence semantics:** Check change tracking, partial updates, defaults,
  constraints, flushes, commits, rollbacks, and exception exits for silently
  discarded or incorrectly persisted supported state.
- **Transaction ownership:** Check that the established request, worker,
  service, or CRUD owner commits or rolls back the complete intended unit and
  does not expose a partial intermediate state.
- **Concurrency and transitions:** Check read-check-write invariants, locks,
  autocommit boundaries, rollout overlap, and concurrent writers through the
  final protected transition rather than only at the initial check. For each
  precondition around a commit or autocommit boundary, identify when its lock
  or guard releases and prove writers remain constrained until the protected
  transition is complete.
- **Retries and duplicate execution:** Check reconnects, redelivery, worker
  restart, and retry paths for the idempotency and side-effect behavior required
  by the current workflow.
- **Partial success and recovery:** Check every multi-step failure exit for the
  established atomic, compensating, resumable, or observable recovery behavior.
- **Synchronization and caches:** Check success, error, reconnect, and stale
  paths for required invalidation, reconciliation, and terminal state changes.

Inspect unchanged model hooks, transaction owners, retry configuration,
constraints, and callers only as needed to prove the realistic failure path.

## Calibration boundaries

Clearing a persistence layer's committed or dirty history after assigning a
new value is a material true-positive pattern when it can erase the update. A
single in-process assignment with no retry, concurrency, persistence, or
external side effect is not a blocker merely because an imagined crash could
interrupt it.

## Exclude

- Hypothetical distributed failure modes that the supported workflow cannot
  encounter.
- Requests for generalized state machines, retries, locks, or idempotency
  frameworks without a current duplicate or partial-success trigger.
- Standalone test gaps, cleanup, naming, or transaction-style preferences that
  do not expose a concrete state defect.
- Migration mechanics, security boundaries, or performance concerns unless
  they directly prove data loss, corruption, duplication, or failed recovery.
