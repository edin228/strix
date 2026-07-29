---
name: strix-implement
description: Execute an explicitly approved software implementation plan through dependency-ordered, repository-owned checkpoints with deterministic validation, risk-routed Strix Autoreview, verified fixes, snapshot-valid review coverage, safe acceptance boundaries, optional checkpoint commits, and final closeout. Use when a user asks to implement or continue an approved plan through the Strix implementation loop. Do not use for discovery, plan authoring, plan approval, or materially unresolved plans.
---

# Strix Implement

Execute the approved plan without reopening resolved discovery. The resident
session implements and verifies findings. Autoreview subprocesses are
ephemeral, read-only advisers.

## Entry

Resolve:

- approved plan path;
- `Review budget: standard|deep`;
- `Commits: accepted-checkpoints|no-commit`;
- existing checkout or explicitly authorized isolation; and
- optional `Stop after: <checkpoint or delivery slice>`.

Default to `Review budget: standard`, the existing safe checkout, and
`Commits: no-commit` unless the user or project instructions explicitly
authorize accepted-checkpoint commits.

Read `references/entry-and-state.md` completely during preflight,
`references/validation-ledger.md` while extracting checks, and
`references/review-routing.md` before classifying the first checkpoint and
whenever risk changes materially.

## Preflight

Before editing:

1. Read the complete plan and verify explicit user approval.
2. Read root and target-repository `AGENTS.md` files plus relevant references.
3. Resolve every repository, branch, base, worktree state, checkpoint,
   dependency, validation, risk, acceptance criterion, and commit mode.
4. Build the plan-derived validation ledger.
5. Verify current source supports named ownership and assumptions.
6. Record the session fingerprint defined by the entry reference.
7. Stop before editing on any entry blocker named there.

For multi-repository plans, build the dependency map first. Every checkpoint
must own exactly one Git repository. Dependencies may cross repositories;
checkpoints and commits may not.

## Checkpoint Loop

For each ready checkpoint in dependency order:

1. Restate its outcome, parent slice, dependencies, expected paths, owning
   repository, acceptance criteria, due validation, dominant risk, and review
   route.
2. Read important existing patterns named by the plan.
3. Enter the owning repository and verify branch, base, HEAD lineage, and
   preserved unrelated status.
4. Implement only the checkpoint and explicit dependencies.
5. Run every validation-ledger entry due now. Fix failures before autoreview.
6. Route the validated checkpoint through `strix-autoreview`. Low-risk work
   normally launches no reviewer.
7. Inspect every P0–P2 finding in current source. Classify it and fix only
   confirmed, localized, in-scope defects.
8. After each material fix, rerun affected deterministic checks, invalidate
   every lens whose evidence changed, and rerun only required or invalidated
   lenses.
9. Before accepting the last checkpoint in a delivery slice, run that slice's
   integration gate. Do not add a redundant review unless risk routing
   requires it.
10. Inspect the final diff and status. Stage only checkpoint-owned paths when
    commits are authorized.
11. Record checkpoint acceptance evidence. Commit with the project's
    convention in accepted-checkpoint mode; otherwise retain scoped-diff and
    validation/review evidence without staging.

Do not accept a checkpoint after a material fix until deterministic validation
passes on the current snapshot and every required lens has resolved coverage
valid for that snapshot. Coverage resolves when a completed report is clean or
every P0–P2 finding has been rejected with source evidence.

Review counts are telemetry, not acceptance limits. After repeated blocking
passes, audit convergence. Continue while confirmed, localized fixes
materially narrow the blocker. Stop when behavior oscillates, fixes cease to
narrow the supported trigger, scope or architecture expands, evidence cannot
be reconciled, or new authority is required. Do not loop for empty P3 output or
higher reviewer confidence.

## Failure Isolation

Preserve accepted commits. When a checkpoint fails:

- mark it and transitive dependents blocked;
- preserve its unaccepted diff;
- quarantine that repository from later checkpoints that could mix with the
  failed diff; and
- continue independent ready checkpoints in unaffected repositories when they
  remain within the requested boundary.

Never reset, overwrite, stash, or discard user or failed-checkpoint work merely
to continue.

## Continuation and Termination

Progress updates, tool completion, context pressure, elapsed time, and token
use are not completion conditions. Keep the compact continuation capsule from
the entry reference current and resume the next ready checkpoint.

Immediately before a final response:

1. Enumerate every unaccepted checkpoint and any in-progress or ready work.
2. Record exactly one permitted termination reason:
   - the approved plan is complete;
   - the requested stop boundary is accepted;
   - user steering replaced or ended the task; or
   - a verified blocker needs user authority or an external change and no
     independent ready checkpoint remains.
3. If work remains ready and no reason applies, execute it instead of ending.

## Finding Synthesis

For each blocking report:

- verify the supported trigger, material impact, and cited ownership;
- classify it as confirmed, false positive, already fixed, overstated,
  test-gap-only, needs direction, or deferred;
- deduplicate semantic overlap without discarding conflicting lens evidence;
  and
- preserve the highest severity supported by source, not the highest reported
  severity.

Do not launch a separate synthesis model. The resident session owns synthesis.

## Steering and Authority

Follow new user steering immediately. Preserve accepted checkpoint commits and
re-evaluate the current checkpoint. Continue only when steering remains
compatible with the approved plan.

Choose local implementation details, deterministic checks, supported review
routes, and the smallest verified fix. Stop for unresolved product behavior,
scope expansion, material architecture change, destructive behavior,
production access, invalidated plan assumptions, or overlapping work that
cannot be preserved.

Do not amend, push, open or merge a change request, deploy, delete branches,
remove worktrees, rewrite history, or access production unless separately
authorized.

## Partial Stop

When `Stop after` ends before the plan:

1. Complete and accept only the named boundary.
2. Run a delivery-slice gate only when the boundary finishes that slice.
3. Do not run full-plan validation or report later checkpoints as defects.
4. Return the stop and continuation state from the entry reference.

## Final Closeout

After the entire plan:

1. Run repository-required final checks and every cross-repository integration
   gate.
2. Review each complete repository diff against the approved plan using
   `strix-branch-review`, then cross-check all repository diffs together for
   dependency and contract coverage.
3. Verify final findings. Reopen only the affected checkpoint for a localized
   fix, then rerun invalidated validation and review coverage.
4. Confirm plan coverage, repository states, branches, bases, accepted
   checkpoints, and absence of unauthorized external actions.

Report validations, review routes and findings, reviewer usage and elapsed
metrics, commits when authorized, residual advisories, snapshot limitations,
and the evidenced termination reason.
