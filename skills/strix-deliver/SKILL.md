---
name: strix-deliver
description: "Deliver a resolved software change through local implementation, validation, and combined closeout review. Use for build or change requests; diagnosis and planning alone do not authorize implementation."
---

# Strix deliver

Establish the requested outcome, current behavior, acceptance criteria, and
material unresolved decisions from source and repository instructions. Continue
within existing user authority; ask only for decisions that materially affect
scope, behavior, architecture, or safety.

Use the existing safe checkout for contained work. For requested isolation or
concurrent work, follow project worktree procedures, using strix-worktree when
installed. Reuse an attributable workspace instead of creating a duplicate.
Preserve unrelated edits.

For bounded low-risk changes, implement from a short scope and acceptance note.
Do not require a formal plan or plan-only commit. For standard or high risk,
write a source-verified plan with ownership, dependencies, failure paths, and
validation before editing. Use strix-plan when installed. Independent plan
review is due when requested, required by the project, or needed before an
irreversible action or expensive dependent design decision.

Readiness is not approval. An explicit request to implement a resolved outcome
can authorize its in-scope plan unless project policy requires a separate plan
approval. Bind that authority to the exact plan version. Resolve material new
choices before proceeding. Seal the plan in a separate commit only when the
project requires it and local commits are authorized.

Execute dependency-ready work with focused checks. For a substantial approved
plan use strix-implement when installed, otherwise retain one repository owner
per checkpoint and equivalent acceptance evidence. Commit only under user or
project authority; no-commit delivery remains supported.

Finish with one combined correctness, acceptance, and integration review.
Low-risk work normally needs resident inspection; standard and high-risk work
use a permitted independent reviewer with complete relevant source. Review
findings are candidates: verify triggers and impact before repairing. Recheck
repairs and affected tests; do not restart a full review for each edit. Give a
materially changed safety boundary a focused independent recheck.

Assess browser proof from the changed behavior after repairs settle. Use a
project verifier or strix-verify-web when rendered behavior remains uncertain.
Report source-based not-required decisions and itemized waivers accurately.

Report the local result, exact source state, checks, review, acceptance, and
remaining blockers. Reflect once at the outermost completion boundary using
strix-retrospective when installed. Local delivery grants no publication,
merge, production, issue mutation, or destructive cleanup authority.
