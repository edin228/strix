# Review timing and coverage

Classify the changed behavior using project policy. Low-risk copy, presentation,
and bounded documentation normally need focused checks and resident inspection.
Standard-risk behavior needs one combined independent closeout review. High-risk
behavior needs that review with the applicable safety evidence and source context.
Safety-policy edits in tooling are classified by their consequences.

## Timing

Complete implementation and focused validation before one combined correctness,
acceptance, and integration review. Do not automatically review each checkpoint,
launch a separate generic bug hunt, or repeat an unchanged clean review. Use an
early review only when explicitly requested, project-required, or source proves
that waiting risks an irreversible action or expensive dependent design mistake.
Name that concrete reason. Pre-mutation security, migration, and destructive-action
evidence remains mandatory regardless of review timing.

Independent plan review is separate from plan readiness and approval. Resident
source verification establishes readiness by default; an independent plan review
is due when requested, project-required, or justified by the early-review rule.
A readiness verdict never supplies user approval.

## Choose one mechanism

Use one permitted read-only source-capable reviewer for integrated work. Include
exact root, base and tip or scoped dirty diff, acceptance, relevant callers,
validation, and prior finding adjudication. The reviewer must not edit, commit,
launch another reviewer, or perform external actions.

When the exact snapshot and available context cover the same objective,
strix-autoreview, when installed, may supply the independent review instead. Read its operating
reference before invoking it and obey provider/data policy. Do not run both
mechanisms for the same job. If the skill or reviewer is unavailable, use an
approved equivalent; otherwise report independent review incomplete rather than
claiming resident inspection supplied it.

## Coverage by changed behavior

| Behavior | Questions to cover |
| --- | --- |
| Ordinary workflow or API | Intended path, common failures, contract compatibility |
| Authorization or tenant scope | Supported identities and entry paths, isolation, read and write callers |
| Transactions, retries, jobs, concurrency | Duplicate execution, ordering, partial success, recovery |
| Migrations | Representative data, graph compatibility, rollout, recovery |
| Queries and hot paths | Representative cardinality, amplification, measured constraints |
| Frontend asynchronous state | Invalidation, stale responses, optimistic rollback, navigation |
| Shared architecture | Ownership, direct consumers, safe intermediate states |

Use a generalist or dominant specialist, adding a distinct lens only when needed
for a material unanswered question. The bundled stage supports up to three
lenses; this is its tool constraint, not a reason to split safe atomic changes
or cap required safety coverage. Use project-approved reviewer configuration;
do not hardcode a preferred model into portable workflow policy.

## Repairs and evidence

Verify each finding's executable trigger, impact, and source owner. Reject
false positives with source evidence. Recheck the repair, direct interactions,
and affected deterministic tests. A new or materially changed safety boundary
requires a focused independent recheck, as does an explicit re-review request.
Retain unaffected coverage with a reason. Do not relaunch a full review simply
because a repair or commit changed the SHA.

A verdict applies only to its examined input. Record exact scope, source
fingerprint, reason, reviewer configuration, findings and adjudication, and
available usage or its unavailability. Missing source, malformed output,
interruption, or engine failure is incomplete evidence, never a clean result.
Stop a nonconverging repair when scope grows, fixes oscillate, or evidence cannot
resolve the same trigger. Do not repeat calls for confidence or to remove minor
nonblocking observations.
