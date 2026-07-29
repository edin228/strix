---
name: strix-plan-review
description: Independently review or explicitly repair a written software implementation plan for source freshness, vertical slicing, checkpoint ownership, risk cohesion, validation, acceptance criteria, and execution readiness. Use when a user asks to audit, grade, check, repair, or determine whether a plan is ready to implement. Do not use to approve a plan on the user's behalf or begin implementation.
---

# Strix Plan Review

Audit the plan independently of its author. A well-written plan is not trusted
until current source and project authority support it.

## Resolve the Review Mode

Resolve the plan path and one mode:

- `review-only`: inspect and report without editing; default for review, audit,
  check, grade, or verdict requests;
- `repair`: make targeted plan edits, then audit the revised plan; require an
  explicit request to fix, patch, repair, or rewrite; or
- `structural-only`: assess plan structure without source freshness; use only
  when the user explicitly limits the review.

Use a user-supplied path. Otherwise inspect the project-declared plan
directory, branch-related plan names, and established plan locations. Ask only
when multiple plausible plans remain.

## Load Authority and Intent

Read the complete plan, workspace `AGENTS.md`, repo-local instructions for
every target repository, and only the references required for the planned
behavior.

Extract the outcome, scope, decisions, repositories, delivery slices,
checkpoints, dependencies, files, tests, validation, acceptance criteria,
rollout, edge cases, and open questions.

## Verify Freshness

For an execution-readiness verdict, inspect the smallest current source context
needed to verify:

- named paths and owners still exist;
- APIs, schemas, migrations, components, and tests match current patterns;
- declared validation commands and dependencies remain executable;
- branch or concurrent work has not superseded the plan; and
- important assumptions remain true.

In `structural-only` mode, do not broaden into a source audit. Mark freshness
as unassessed and do not return an execution-ready verdict.

## Audit the Plan

Check:

- independently useful vertical delivery slices;
- explicit, dependency-ordered checkpoints for non-trivial slices;
- one owning Git repository per checkpoint;
- separate commit boundaries for cross-repository capabilities;
- cohesive risk and a proportionate review route;
- exact new-file paths and resolved ownership for modified files;
- inline tests, deterministic validation, and material failure paths;
- observable acceptance criteria;
- safe review and commit boundaries;
- rollout, migration, recovery, and compatibility behavior when material; and
- material decisions incorrectly deferred to implementation.

Do not recommend horizontal splitting merely to reduce size. Reject
checkpoints that mix separable migration, security, external-side-effect,
background, and UI risks. Permit a large atomic transition only when splitting
would create an unsafe or untestable intermediate state.

## Classify and Repair

Use:

- `HIGH`: likely unsafe, non-executable, materially wrong, or likely to cause
  major rework;
- `MEDIUM`: meaningful ambiguity, stale ownership, incomplete checkpoint
  contract, or insufficient validation and commit safety; and
- `LOW`: polish or a small specificity gap that does not block execution.

For each material finding, name the smallest affected location, explain the
consequence, and provide a concrete corrected shape.

In `repair` mode, preserve useful context and resolved decisions. Make only
targeted plan edits. Leave unresolved material choices explicit, then rerun the
audit against the edited plan.

## Return a Verdict

Return exactly one:

- `EXECUTION-READY`: freshness checked, no HIGH or MEDIUM findings, every
  checkpoint is executable, and no material choice is unresolved;
- `NOT EXECUTION-READY`: any HIGH or MEDIUM finding, stale or unverified
  required source, unsafe boundary, or unresolved material choice; or
- `STRUCTURALLY REVIEWED — FRESHNESS NOT ASSESSED`: structural-only mode.

Execution readiness is not user approval and does not authorize implementation.

Report:

1. findings, highest severity first;
2. a concise scorecard for slices, checkpoints, specificity, acceptance,
   edge cases, validation, dependencies, and commit safety;
3. verdict and freshness evidence;
4. recommended plan shape when changes are needed;
5. a rewrite prompt for material findings; and
6. edits only when repair mode changed the plan.
