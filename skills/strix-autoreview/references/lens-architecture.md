# Architecture Lens

Review the changed behavior for concrete ownership, dependency, and boundary
defects.

## Coverage checklist

- **Ownership and authority:** Check whether new behavior bypasses or duplicates
  the existing source of truth, invariant owner, or orchestration boundary.
- **Dependency direction:** Check imports, initialization order, runtime
  packaging, and unsupported cross-repository contracts for a concrete cycle
  or deployment mismatch.
- **Lifecycle and side effects:** Check whether state crosses an owner without
  the transaction, cleanup, invalidation, or recovery required by callers.
- **Contract propagation:** Check whether changed schemas, interfaces, events,
  or defaults remain compatible with every supported consumer and producer.
- **Atomicity and intermediate states:** Check whether an abstraction or
  delivery checkpoint splits one invariant across owners or leaves a supported
  deployment observably unsafe or unusable.

Read unchanged callers, shared owners, schemas, repository instructions, and
tests only as needed to prove or disprove one of those triggers.

## Exclude

- Preference for a different but valid architecture.
- Requests for future extensibility, generalized frameworks, broad cleanup, or
  extraction without a present correctness benefit.
- Naming, formatting, file-size, layering, or test-organization opinions that
  do not expose a concrete material defect.
- Domain-specific security, migration, performance, or UI critique unless it
  directly proves an architectural boundary defect. Those concerns belong to
  their specialist lenses.
