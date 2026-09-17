---
name: strix-trim-complexity
description: Inspect and optionally simplify an exact diff for evidence-backed removal of unnecessary structure without changing behavior. Use before strix-implement closeout review, when a user requests complexity trimming, or when resident inspection identifies concrete unnecessary structure. Do not invoke automatically at every checkpoint.
---

# Trim complexity

Inspect one exact diff and its necessary source context. Preserve behavior.

## Invocation boundary and modes

- `review-only`: the default for a standalone direct invocation. Return supported
  cuts without editing, committing, or initiating another review.
- `trim-and-fix`: required before strix-implement independent closeout
  review, under the existing implementation authority. Also use when a standalone
  request explicitly asks for fixes. Identify and apply justified simplifications
  within the authorized scope, run affected checks, and return the resulting diff.

Run one bounded pass over the complete implementation diff at closeout.
Ordinary checkpoints and lightweight delivery do not invoke this skill
automatically; use it there on request or for concrete unnecessary structure.
Inspect only the named diff and necessary callers. Do not reopen trim discovery
after repairs. Neither mode grants publication or other external authority.

## Execution

When delegation is available and authorized, use a fresh worker with the
project-approved model and effort, honoring user overrides. Otherwise execute
directly with the same evidence requirements. An assigned worker performs this
pass without spawning agents or launching another review.

Give it the selected root, resolved base and tip or exact local snapshot,
accepted requirements, validation evidence, mode, owned paths, and exclusions.
For `trim-and-fix`, follow the write-ownership, path, and return-state rules in
[delegation.md](../strix-implement/references/delegation.md). If that companion
is not installed, enforce equivalent single-writer ownership, repository and
symlink containment, no worker staging or lifecycle actions, and resident diff
and evidence inspection before accepting the return.

The worker owns investigation, justified cuts, and affected testing. Report
uncertain cuts instead of applying them. Return technical disputes with source
evidence for adjudication. The resident checks scope, state, containment, and
validation completeness, and commits only under user or project authority after
the worker yields. No-commit delivery remains supported.

At implementation closeout, a separate fresh independent reviewer examines the
final diff including simplifications. The trim author cannot review its own work
as that reviewer. Route confirmed trim-related findings back for focused repairs
without restarting discovery. Standalone trimming does not itself initiate branch
review; any required review follows the enclosing repair workflow.

## Inspect the evidence

Read the changed implementation plus the callers, configurations, tests, and
accepted contracts needed to judge behavior. Use these labels to organize possible
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
validation. Favor fewer unnecessary concepts and indirections over denser
expressions. Preserve useful explicit code when it improves readability. Net
lines are not a score.

A one-caller wrapper is removable only when the direct call preserves its
contract. Keep the same shape when a second implementation or accepted contract
requires the abstraction.

## Return the inventory

Complete one bounded pass. Identify the reviewed repository, resolved base and
tip, or the exact local diff snapshot when reviewing uncommitted work. State
the covered scope and any coverage gaps. For every finding, report:

- exact location and category label;
- proposed or applied cut and its disposition;
- callers or configurations inspected;
- behavior that remains equivalent; and
- focused validation required after removal, or commands, working directories,
  exit statuses, and the resulting diff covered when fixes were applied.

In `trim-and-fix`, also report changed paths, unresolved concerns, and any edits
made after validation. Failed or unavailable required checks leave the work
incomplete; do not describe unvalidated simplifications as complete.

If source is missing, the pass is interrupted, or part of the assigned scope
remains unexamined, report `Incomplete` with the gaps and any supported findings.
Do not treat an incomplete pass as clean. Only after completing the assigned
inspection, if each triggered structure earns its cost, return
`No evidence-backed cuts.` Do not block on a category label or style preference.
Do not reopen trim discovery recursively after a repair exposes optional cleanup.

The resident owns staging and commits under the enclosing workflow authority.
A standalone `review-only` request never grants edit authority.
