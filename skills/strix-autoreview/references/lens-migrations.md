# Migrations Lens

Review changed schema and data transitions for concrete upgrade, downgrade,
rollout, locking, and compatibility defects.

## Coverage checklist

- **Data preservation:** Check upgrade and downgrade for loss, truncation,
  reinterpretation, default/nullability changes, and reconstruction required
  by the supported rollback contract.
- **Rolling compatibility:** Check constraints, indexes, enums, columns,
  tables, triggers, and runtime reads/writes while old and new application
  versions coexist.
- **Atomic guards:** Check that precondition reads, writer exclusion, trigger
  changes, autocommit boundaries, and protected transitions cannot be
  invalidated by a concurrent writer.
- **Locking and work bounds:** Check table size, index mode, transaction shape,
  backfill bounds, and failure recovery for realistic production downtime.
- **Revision and model agreement:** Check migration ancestry,
  upgrade/downgrade symmetry, object naming, registration, and current
  model/schema agreement.

Inspect adjacent revisions, current models, constraints, runtime write paths,
and deployment assumptions only as needed to prove the transition failure.
Report a blocker only when the schema/data transition, its revision, or
migration-sensitive model agreement causes the defect. Runtime code is context,
not a second generalist review surface.

## Calibration boundaries

A downgrade that checks for incompatible rows before installing its write
guard or taking the protecting table lock is a material true-positive pattern
when rolling application instances can still write. A small nullable-column
addition or concurrent index operation is not a blocker merely because every
migration briefly consumes database resources.

## Exclude

- A demand for perfectly reversible data when the approved contract explicitly
  declares the transformation irreversible.
- Generic zero-downtime, batching, lock, or index advice without a realistic
  table size, write path, rollout overlap, or failure impact.
- Persistence transaction, request reliability, security, or query-performance
  critique that is not caused by the schema transition. Do not report an
  application service defect merely because its file shares the migration
  bundle; the paired data-integrity/reliability lens owns that behavior.
- Style preferences about revision formatting, helper placement, or comments.
