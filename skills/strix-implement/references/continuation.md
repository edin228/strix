# Plan maintenance and handoffs

A plan records approved intent. Preserve the user's scope and existing authority
across checkpoints, compaction, and thread transfers. A hash or baseline revision
identifies evidence; it does not freeze every path or implementation detail.
Require a separate plan-only commit only when project policy requires it.
Otherwise a mixed baseline is valid, and no-commit delivery retains a snapshot.
Never rewrite history to manufacture a plan seal.

Within the authorized outcome, correct stale paths, commands, implementation
details, missing validation, checkpoint boundaries, dependency order, and handoff
metadata from current source. Record the reason and recheck affected decisions.
Do not weaken acceptance to hide failures or repeat unaffected planning and
review. Ask only when an unresolved decision changes behavior, scope, architecture,
data treatment, safety boundaries, or external authority.

## Requested stages

Continue authorized delivery through checks, review, repairs, and due browser
proof unless the user requests a narrower stop or transfer. Planning-only work
stops before implementation. An implementation-only handoff stops before combined
review and formal browser proof; narrow diagnostic inspection may precede it.
Report `implementation complete; closeout pending` when those gates remain.

A closeout recipient completes any pending simplification pass, then one independent
combined review, repairs, and due browser proof. Retain completed passes whose
scope and assumptions still apply. A fresh explicitly assigned independent review
resident can perform the review directly if it has not authored implementation
or simplifications. Assign pending trim to a separate author to retain that
independence; if the resident makes cuts itself, use a different reviewer. Do not
add another reviewer to duplicate an already independent review of the same job. Publication and operations retain their separate authority.

## Transfer record

Use the project's handoff location or existing progress record. A concise Markdown
handoff is sufficient unless project tooling requires another form. Include:

- objective, accepted decisions, constraints, rejected approaches and reasons;
- current phase, completed work, remaining acceptance, and exact next action;
- selected checkout, branch, base, HEAD, plan baseline, dirty paths and ownership;
- validation and review evidence with tested scope and limitations;
- simplification disposition or pending pass, browser scope, and safety evidence;
- running agents or operations, resource ownership, and result collection; and
- inherited authorization with its source and any unresolved decisions.

Verify linked artifacts are accessible; retain useful conclusions and disclose
missing originals. Keep secrets, raw private reports, and unnecessary logs out.
Do not promise a lossless transfer. Helper failure is diagnostic, not a reason
to discard edits or request approval for routine metadata recovery.

The receiver verifies root, branch, HEAD, dirty state, and live writers before
mutation. Investigate differences narrowly and reuse valid evidence. Unknown
ownership or a writer that may resume blocks dependent writes.

## Context pressure

Follow the project's compaction policy. Without one, recommend a fresh thread
when repeated recovery or accumulated irrelevant history materially impedes the
next task. Prepare the usable handoff first and explain the observed reason;
do not invent context percentages or savings. The recommendation is nonblocking:
continue unless the user chooses to transfer, finish first when nearly done,
and do not repeat the warning without new evidence. Never cancel active work
or replay accepted checkpoints merely to refresh context.
