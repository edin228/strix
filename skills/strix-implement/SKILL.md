---
name: strix-implement
description: Execute an approved software plan through repository-owned checkpoints with focused validation and one combined closeout review. Use for implementing or continuing an approved plan, not discovery or unresolved product decisions.
---

# Strix implement

The resident owns sequencing, evidence acceptance, finding adjudication, and authority.
An assigned implementation worker owns investigation, implementation, debugging,
and affected checks. Keep the user-selected resident and project-approved worker
configuration; direct execution remains supported.
Use the existing safe checkout unless isolation is requested or project-required.
Default to no commits unless the user or project authorizes checkpoint commits.
Honor explicit checkpoint, delivery-slice, and stage handoffs. Read
[continuation.md](references/continuation.md) for plan maintenance or transfer.
Continue authorized work through closeout unless the user sets an earlier boundary.

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
2. Implement the bounded outcome following current owners and patterns. For
   broad rules or codemods, identify preserved behavior families, representative
   consumers, and focused checks before applying the change.
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

When delegation is available and authorized, follow
[delegation.md](references/delegation.md) for checkpoint context, capability
checks, exclusive writes, transfers, and returned evidence. Accept reconstructable
source and passing command evidence without repeating it merely because a worker
produced it. Inspect actual state and the diff before acceptance. Name the missing
or invalidated evidence before rerunning unchanged checks.

Preserve accepted work when a checkpoint fails. Quarantine its unaccepted diff
and block dependents; continue independent work in unaffected repositories when
safe. Never reset, stash, discard, or overwrite unrelated or failed work to
continue. Resolve uncertain writer ownership before another mutation.

## Combined closeout

At the agreed delivery boundary, finish required deterministic and integration
checks. Before independent review, perform one bounded `trim-and-fix` pass
using strix-trim-complexity when installed, or equivalent source-grounded
simplification with affected checks. Cover the complete implementation diff and
necessary callers, retaining a still-valid completed pass across handoff. Use a
separate fresh reviewer for the resulting diff; the simplification author cannot
supply its independent review. Do not restart trim discovery after repairs or
add automatic trim passes to ordinary checkpoints.

Review each complete repository diff and cross-repository contracts
against the approved acceptance criteria. Use strix-branch-review when installed
or an equivalent source-grounded review. Choose one independent mechanism for
the combined job; do not add checkpoint autoreview or a separate generic hunt.
A complete earlier review may be retained when its inputs still apply.

Verify every reported defect against current source. Route repairs to the
implementation worker, or the trim author for trim-related findings, while its
context remains useful; otherwise transfer safely or use direct execution.
Repair localized in-scope findings, rerun affected checks, and inspect direct interactions. Recheck a
materially changed safety boundary independently. Do not restart the whole
review after each edit or seek a numeric confidence threshold. Stop when fixes
oscillate, evidence cannot settle a disagreement, or scope materially expands.

Have the source-capable code reviewer assess browser applicability, named
scenarios, and observable outcomes. If a structured review engine cannot return
that assessment, the resident supplies it from source and deterministic evidence
without adding another full review. After repairs settle, finalize the assessment.
Exclude changes merely imported from the integration branch when selecting live
scenarios, while retaining the complete integrated diff for code review. Use the
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

Recheck materially changed decisions before dependent work. Routine in-scope
plan maintenance preserves existing authority under the continuation reference;
only unresolved changes to the authorized contract require user direction. Local execution
does not authorize push, PR mutation, merge, production, branch deletion,
history rewriting, or destructive cleanup.
