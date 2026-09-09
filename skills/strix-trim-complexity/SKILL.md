---
name: strix-trim-complexity
description: Review an exact diff for evidence-backed removal of unnecessary structure without changing behavior. Use when a user requests complexity trimming or resident inspection identifies concrete unnecessary structure. Do not invoke automatically at every checkpoint.
---

# Trim complexity

Review one exact diff and its necessary source context. Stay read-only.

## Invocation boundary

Use a bounded pass when the user requests it or resident diff inspection finds
concrete unnecessary structure. Ordinary implementation-loop checkpoints and
lightweight delivery do not invoke this skill automatically. Inspect only the
named diff and necessary callers, return the inventory, and do not reopen
discovery after a repair. A direct invocation grants no edit, commit,
publication, or other mutation authority.

## Inspect the evidence

Read the changed implementation plus the callers, configurations, tests, and
sealed contracts needed to judge behavior. Use these labels to organize possible
cuts, never as proof:

- `delete`: remove behavior or structure with no required consumer.
- `stdlib`: replace custom code with an equivalent standard-library operation.
- `native`: use an existing language, framework, or repository capability.
- `yagni`: remove flexibility unsupported by a current requirement.
- `shrink`: collapse indirection or duplication while preserving ownership.

Report a cut only when source evidence proves the proposed form preserves
validation, ordering, authorization, tenancy, migration safety, retries,
recovery, observability, actionable failures, accessibility behavior, and
useful tests. Preserve defensive code tied to a reproduced provider failure.
Reject a shorter standard-library expression when it truncates input or changes
validation. Net lines are not a score.

A one-caller wrapper is removable only when the direct call preserves its
contract. Keep the same shape when a second implementation or sealed contract
requires the abstraction.

## Return the inventory

Complete one bounded pass. For every finding, report:

- exact location and category label;
- proposed cut;
- callers or configurations inspected;
- behavior that remains equivalent; and
- focused validation required after removal.

If inspection proves that each triggered structure earns its cost, return
`No evidence-backed cuts.` Do not block on a category label or style preference.
Do not reopen trim discovery recursively after a repair exposes optional cleanup.

Every invocation is read-only. The implementation resident decides whether to
accept a cut and owns any repair, validation, staging, and commit.
