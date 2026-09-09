---
name: strix-branch-review
description: Review, verify, and when explicitly requested repair Git branch or working-tree changes with rigor proportional to behavior risk. Use for current-branch reviews, named branch or commit-range audits, plan-compliance checks, pasted review findings, requested ratings, or review-and-fix loops. Combined bug-hunt-and-branch-review requests authorize localized repairs unless explicitly read-only; ordinary reviews remain read-only.
---

# Strix Branch Review

Produce evidence-backed findings about correctness, regressions, security,
reliability, and requirement coverage. Do not turn review into an unsolicited
refactor.

## Resolve Scope and Authority

Choose one mode:

- `review-only`: inspect and report; default for an ordinary review;
- `fix-findings`: verify supplied findings and fix confirmed defects; or
- `review-and-fix`: perform a review, then repair confirmed in-scope defects.

A combined request for a bug hunt and branch review selects one resident
review-and-fix pass unless the user explicitly says read-only, findings-only,
or no edits. This authorizes localized repairs and necessary validation, not
external actions. Commit only when the user or project permits it.

Resolve the owning Git repository, target branch or working tree, comparison
base, intended behavior, applicable plan, and whether local edits already
belong to the user.

Read root and repo-local `AGENTS.md` files plus references relevant to the
changed behavior. Discover base branches from project authority and local Git
state; do not assume `main`, `master`, or `dev`. Do not fetch unless current
remote state is required and network access is authorized.

## Establish the Evidence

Inspect:

- repository status, current branch, HEAD, upstream, and comparison base;
- commits, changed paths, diff summary, and complete relevant diff;
- the plan, issue, acceptance criteria, or stated intent;
- current owning source and tests around the changed behavior; and
- required validation from project instructions.

Keep unrelated working-tree changes intact. In review-only mode, make no
changes.

## Review by Risk

Classify the changed behavior using project policy or these defaults:

- high: security boundaries, destructive actions, money, migrations,
  synchronization, concurrency, external side effects, secrets, production,
  or realistic data-loss paths;
- standard: ordinary workflows, CRUD, APIs, caching, and shared components;
- low: presentation, copy, documentation, and reversible interaction.

Review every change for intended behavior, regressions, error handling,
contract compatibility, and test adequacy. Add focused scrutiny where
applicable:

- authorization and tenant or ownership isolation;
- transaction, retry, idempotency, and partial-success behavior;
- migration compatibility and recovery;
- cache invalidation and stale client state;
- background or external-side-effect duplication;
- concurrency and ordering;
- resource usage on plausible hot paths; and
- accessibility and interaction states for UI changes.

Report only concrete, material issues tied to an executable path. Do not report
style preferences, hypothetical extensibility, or missing tests without a
specific behavior risk.

## Validate Findings

For each candidate finding:

1. reproduce or trace the trigger;
2. verify the cited owner and current behavior;
3. identify user or system impact;
4. check whether existing validation already disproves it; and
5. classify it as confirmed, false positive, already fixed, overstated,
   test-gap-only, needs direction, or deferred.

Use `P0` for catastrophic or actively exploitable failures, `P1` for serious
common failures, `P2` for material limited-path defects, and `P3` for
nonblocking observations.

## Repair Only With Authority

In a fix mode, apply the smallest correction at the owning boundary. Add a
regression test for confirmed behavior defects unless impractical. Do not
broaden scope to improve architecture unrelated to the finding.

Run focused validation after each material fix, then all repository-required
checks for the final changed state. Re-review affected code and invalidate
prior review evidence when the snapshot materially changes.

For a combined delivery closeout, cover correctness, acceptance, defects, and
integration in one pass. Low-risk work normally needs resident inspection.
For standard and high risk, use one permitted independent source-capable reviewer
or strix-autoreview when its exact snapshot and context suffice, following the
project's review policy. If neither is available, report that evidence gap.
Do not add both for the same objective or recursively invoke branch review.
For an explicitly read-only reviewer assignment, return findings without
launching another reviewer or changing files.

After a repair, inspect its direct interactions and rerun affected checks.
Require focused independent recheck for a materially changed safety boundary
or explicit re-review request. Retain unaffected evidence; do not restart a
full review for each fix. Incomplete or engine-failed review is not clean.

Do not commit, amend, push, merge, deploy, delete branches, or rewrite history
unless separately authorized.

## Report

Lead with findings, highest severity first, using `path:line`, impact,
evidence, and smallest safe correction. State `No material findings` when
appropriate.

Then report:

- review mode, target, base, branch, and exact HEAD;
- intended behavior or plan coverage;
- validation commands and results;
- fixes made and residual advisories;
- repository status and snapshot limitations; and
- a requested rating, if any, with no top rating while a real material defect
  remains.
