---
name: strix-bug-hunt
description: Investigate a named software feature or subsystem for concrete bugs, regressions, security failures, data loss, race conditions, stale state, missing validation, broken invalidation, and reliability issues. Use when a user asks to hunt for defects or assess a feature's correctness; repair verified issues only when the request also authorizes fixing or correction.
---

# Strix Bug Hunt

Find reproducible or source-provable failures rather than producing a broad
style review.

## Choose the Mode

Use:

- `investigate-only`: map, test, and report; default when the user asks to
  investigate, audit, diagnose, or hunt for bugs; or
- `investigate-and-fix`: repair verified in-scope defects when the user also
  asks to fix, correct, resolve, or implement repairs.

Read root and repo-local `AGENTS.md` files, relevant architecture references,
and current repository status before inspecting the feature.

## Map the Feature

Use source search and current tests to identify:

- entry points and user actions;
- APIs, services, data owners, schemas, and persistence;
- client state, caches, jobs, queues, and external providers;
- permission and ownership boundaries;
- retries, recovery, and partial-success paths; and
- existing tests, plans, and known limitations.

Trace data and control flow across boundaries. Preserve unrelated local work.

## Hunt Concrete Failure Modes

Prioritize:

- authorization bypass or cross-owner access;
- lost, duplicated, corrupted, or incorrectly ordered writes;
- missing null, empty, malformed, timeout, or provider-error handling;
- non-idempotent retry, webhook, sync, or job behavior;
- transaction ownership and partial commits;
- stale caches, query keys, selections, drafts, or optimistic updates;
- missing rollback after failed optimistic behavior;
- race conditions and actions incorrectly enabled while in flight;
- schema, serialization, time-zone, or compatibility mismatches;
- resource amplification on plausible hot paths; and
- inaccessible or misleading UI states that cause wrong actions.

Use project-specific guides to add stack-aware checks. Reject an issue that
cannot be tied to a concrete trigger and material impact.

## Verify and Rank

Confirm candidates through focused tests, reproduction, or complete source
tracing. Use:

- `Critical`: exploitable security breach, cross-owner data exposure, data
  corruption, or widespread outage;
- `High`: common workflow failure, lost or duplicate work, stuck recovery, or
  a serious misleading state;
- `Medium`: meaningful limited-path failure with a practical trigger; and
- `Low`: minor correctness issue with small impact.

For each finding provide `path:line`, trigger, impact, evidence, and the
smallest safe fix. Distinguish confirmed bugs from unverified hypotheses.

## Repair With Explicit Authority

In `investigate-and-fix` mode:

- fix Critical and High issues in scope;
- fix Medium issues when localized and clearly within the requested feature;
- leave Low issues unless the correction is adjacent, cheap, and safe;
- add regression coverage for each repaired behavior when practical; and
- keep refactors limited to what correctness requires.

After fixes, run focused tests and every project-required static or integration
check for changed repositories. Review the final diff for regressions. Use
`strix-autoreview` after high-risk or non-trivial standard-risk fixes, routed
to the dominant changed behavior. Treat its output as advisory and verify
every blocking report in current source.

If autoreview causes a material fix, rerun affected deterministic validation
and invalidated review coverage. Treat an interrupted, malformed, unstable, or
engine-failed autoreview as incomplete, not clean. Skip autoreview for
low-risk presentation-only fixes unless the user asks or a shared surface
raises practical risk.

Do not commit, push, merge, deploy, access production, or perform destructive
cleanup without separate authority.

## Close Out

Report:

- verified bugs found and their severity;
- repairs made and regression coverage;
- bugs intentionally not fixed and why;
- validation commands and results;
- unverified hypotheses separately from findings; and
- repository, branch, exact HEAD, base, and dirty or clean state.

State that the evidence covers the inspected snapshot and may be invalidated by
later changes.
