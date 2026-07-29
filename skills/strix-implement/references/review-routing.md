# Review Routing and Budgets

Classify changed behavior, not the feature name or directory. Project policy
may require more rigor; a user budget may not lower the minimum.

## Minimum Routes

| Behavior | Minimum route |
|---|---|
| Copy, styling, icons, documentation, local reversible UI | Deterministic validation only |
| Standard-risk behavior without a dominant specialty | One generalist autoreview |
| Shared ownership, layer boundary, or plan-directed architecture | Generalist plus `architecture` |
| Authentication, authorization, privacy, filesystem, shell, or public trust boundary | Generalist plus `security` |
| Transactions, retries, concurrency, background work, synchronization, or realistic data loss | Generalist plus `data-integrity-reliability` |
| Schema or data migration | `migrations` plus `data-integrity-reliability` |
| Narrow query-heavy or realistic hot path | One dominant `performance` specialist |
| Broad standard-risk behavior with secondary performance concerns | One generalist; use `performance` only when dominant |
| Frontend API, cache, async state, overlay, or window integration | One dominant `frontend-integration` specialist |
| Atomic checkpoint crossing trust and state-consistency boundaries | Generalist plus `security` plus `data-integrity-reliability` |
| Atomic checkpoint crossing architecture, trust, and state consistency | `architecture` plus `security` plus `data-integrity-reliability`; omit a fourth generalist |

Split checkpoints that would require more than three initial reviewers unless
splitting creates an unsafe or untestable intermediate state.

Before launching multiple routes, record one distinct coverage justification
per lens: the behavior or boundary it owns, changed paths exposing it, and the
material question not covered by another route.

## Reviewer Configuration

Use a project-approved Codex model when reproducibility matters. When
`--model` is omitted, the isolated runner uses Codex's service default because
it deliberately ignores user configuration. Do not hardcode a Strix model
name.

Use `--thinking high` for high-risk and difficult standard-risk review unless
the project has validated another setting. If a requested budget conflicts
with the risk minimum, stop before editing and request direction.

Initial breadth:

- low risk: zero reviewers by default;
- standard risk: one reviewer by default; and
- high or mixed risk: two reviewers by default, three maximum.

`standard` uses the minimum route. `deep` may add one distinct route up to the
three-reviewer cap; it does not create redundant reviewers.

## Invocation

Resolve the installed `strix-autoreview` skill path.

One route:

```bash
python3 <strix-autoreview>/scripts/autoreview \
  --mode local \
  --scope-path <checkpoint-path> \
  --thinking high
```

Multiple routes:

```bash
python3 <strix-autoreview>/scripts/autoreview-stage \
  --mode local \
  --lens generalist \
  --lens security \
  --scope-path <checkpoint-path> \
  --thinking high
```

Pass every checkpoint-owned file or cohesive directory as a separate literal
scope. Compare scoped status/diff with checkpoint ownership before launch. An
empty, incomplete, or unprovable scope blocks review.

Every stage lens receives the same complete scope. Prefer commit or branch mode
when it isolates the checkpoint more accurately. Never include unrelated dirty
files for convenience.

## Completion Evidence

Exit `1` with a structured blocking report is completed, not an engine failure.
Stage exit `2`, missing or malformed output, inaccessible input, interruption,
unstable fingerprints, or cleanup failure is incomplete.

For each call retain:

- lens, explicit model/reasoning or default status, prompt size, and elapsed
  time;
- available token metrics or explicit unavailability;
- reported and confirmed findings;
- pass number and reviewed fingerprint; and
- whether coverage remains valid for the current snapshot.

Do not write a metrics artifact during routine implementation.

## Snapshot Validity and Convergence

A completed lens verdict applies only to its fingerprinted input. A material
fix invalidates the finding lens and every other lens whose reviewed behavior
or evidence changed. Preserve genuinely unaffected verdicts only with an
explicit coverage reason.

Accept a reviewed checkpoint only when deterministic validation passes and
every required lens has resolved current-snapshot coverage. Coverage resolves
when a completed report has no P0–P2 finding or the resident session rejects
every P0–P2 with source evidence.

Reviewer confidence is confidence in the reported verdict, not a cleanliness
or quality score. Never use a numeric confidence threshold to accept, reject,
or repeat review.

After the second consecutive blocking result, and after each later result,
audit convergence. Continue when source confirms a localized in-scope defect,
deterministic validation can prove the repair, and blockers are narrowing.
Stop when:

- repeated fixes do not narrow the same trigger;
- fixes and findings oscillate;
- correction expands product behavior, scope, ownership, or architecture;
- reviewer disagreement cannot be resolved from source; or
- deterministic validation cannot prove the repair.

Do not rerun after required coverage resolves merely to seek higher confidence
or remove P3 observations.

## Finding Verification

Verify P0–P2 in current source. Require a supported trigger, material impact,
plan relevance, and proportionate fix. Classify each as confirmed, false
positive, already fixed, overstated, test-gap-only, needs direction, or
deferred.

After a confirmed fix, rerun affected validation and invalidated lenses only.
The resident session performs synthesis; do not launch a synthesis model.
