---
name: strix-branch-review
description: Review, verify, and when explicitly requested repair Git branch or working-tree changes with rigor proportional to behavior risk. Use for current-branch reviews, named branch or commit-range audits, plan-compliance checks, pasted review findings, requested ratings, or review-and-fix loops. Default to review-only unless the user clearly authorizes fixes.
---

# Strix Branch Review

Produce evidence-backed findings about correctness, regressions, security,
reliability, and requirement coverage. Do not turn review into an unsolicited
refactor.

## Resolve Scope and Authority

Choose one mode:

- `review-only`: inspect and report; default;
- `fix-findings`: verify supplied findings and fix confirmed defects; or
- `review-and-fix`: perform a review, then repair confirmed in-scope defects.

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

After a high-risk fix or non-trivial standard-risk behavior fix, use
`strix-autoreview` from the owning repository unless project policy requires a
different closeout. Skip it for low-risk presentation-only fixes unless the
user asks or a broadly shared surface raises practical risk. Verify every
blocking report in current source. If a confirmed finding causes a material
fix, rerun affected deterministic validation and invalidated review coverage.

Do not run autoreview for review-only work that changed no files unless the
user explicitly asks for that independent review. Do not recursively invoke
`strix-branch-review`. Treat an interrupted, malformed, unstable, or
engine-failed autoreview as incomplete, not clean.

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
