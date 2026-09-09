---
name: strix-implement
description: Execute an approved software plan through repository-owned checkpoints with focused validation and one combined closeout review. Use for implementing or continuing an approved plan, not discovery or unresolved product decisions.
---

# Strix implement

The resident owns sequencing, acceptance, finding adjudication, and authority.
Use the existing safe checkout unless isolation is requested or project-required.
Default to no commits unless the user or project authorizes checkpoint commits.
Honor an explicit stop-after checkpoint or delivery-slice boundary.

## Preflight

Read the complete approved plan, root and applicable nested instructions, and
[entry-and-state.md](references/entry-and-state.md). Record the exact plan hash,
approval evidence, repository roots, branches, bases, HEADs, initial dirty paths,
commit mode, dependencies, and stop boundary. Approval may come from an active
resolved delivery request when project policy permits; a review verdict alone
is never approval. Require a plan-only seal only when project policy does.

Verify named source owners, infrastructure, callers, acceptance, and failure
paths before coding. Resolve material product, architecture, safety, and rollout
choices first. Build the plan-derived checks using
[validation-ledger.md](references/validation-ledger.md). Read
[review-routing.md](references/review-routing.md) for review timing and coverage.
Every checkpoint owns exactly one Git repository, even across a multi-repository
plan. Subtrees in one repository may share a cohesive checkpoint.

## Checkpoint loop

For each dependency-ready checkpoint:

1. Confirm its repository, branch, current HEAD, owned paths, dependencies,
   acceptance, and due validation. Preserve unrelated changes.
2. Implement the bounded outcome following current owners and patterns.
3. Inspect the complete diff and run focused deterministic checks and any due
   slice integration gate. Fix confirmed in-scope defects and recheck affected
   behavior. Do not invent tests that merely mirror implementation wording.
4. Defer independent review to closeout unless requested or a concrete
   pre-mutation safety or expensive dependent-design risk requires it earlier.
   Record deferred review honestly; do not claim a checkpoint was reviewed.
5. Inspect final status and accepted bytes. In authorized commit mode stage
   only owned paths and use project hooks. Inspect what the hook and commit
   changed, rerunning invalidated checks before acceptance. In no-commit mode
   retain scoped diff evidence without staging.
6. Record acceptance, commands and outcomes, source identity, and next work.

When delegation is available and authorized, use it only for bounded work while
useful independent resident work remains. Keep consequential diagnosis and
architecture decisions resident. Allow at most one writable actor per checkout.
Validate owned paths against symlinks and nested repositories before granting
write scope. A worker may not stage, commit, perform lifecycle actions, or spawn
more workers. Inspect its actual diff and repository state before acceptance;
a worker summary is not proof. Do not choose a fixed model for every project.

Preserve accepted work when a checkpoint fails. Quarantine its unaccepted diff
and block dependents; continue independent work in unaffected repositories when
safe. Never reset, stash, discard, or overwrite unrelated or failed work to
continue. Resolve uncertain writer ownership before another mutation.

## Combined closeout

At the agreed delivery boundary, finish required deterministic and integration
checks. Review each complete repository diff and cross-repository contracts
against the approved acceptance criteria. Use strix-branch-review when installed
or an equivalent source-grounded review. Choose one independent mechanism for
the combined job; do not add checkpoint autoreview or a separate generic hunt.
A complete earlier review may be retained when its inputs still apply.

Verify every reported defect against current source. Repair localized in-scope
findings, rerun affected checks, and inspect direct interactions. Recheck a
materially changed safety boundary independently. Do not restart the whole
review after each edit or seek a numeric confidence threshold. Stop when fixes
oscillate, evidence cannot settle a disagreement, or scope materially expands.

After repairs settle, assess browser evidence from changed behavior. Use the
project verifier or strix-verify-web when installed for required rendered or
interaction proof. Record not-required with source and deterministic evidence
when appropriate; a PR or new SHA alone does not require another live drive.
Retain valid artifacts and repeat only invalidated scenarios. A full verifier
audit needs an explicit request or source-proven broad map drift.

Confirm every acceptance criterion, final status, preserved work, and remaining
limitations. Report commits when authorized, validation, reviewed scope and
method, confirmed findings, retained evidence, and incomplete lanes. Reflect
once at the outermost requested delivery boundary, using strix-retrospective
when installed. Defer that reflection to an active publication or shipping owner.

## Continuation and authority

Keep the continuation capsule current and resume after compaction. Do not replay
accepted checkpoints or reread unchanged instructions still in context. Finish
when the plan or requested stop boundary is accepted, the user ends or replaces
the task, or a verified blocker leaves no safe independent work. Context size,
elapsed effort, and tool completion are not completion conditions.

Material plan changes need renewed readiness and approval binding before their
implementation. Preserve existing authority for unchanged scope. Local execution
does not authorize push, PR mutation, merge, production, branch deletion,
history rewriting, or destructive cleanup.
