# Entry and State

## Entry Requirements

Begin only when:

- a complete implementation plan is identified;
- the user approves implementation, directly or through a still-applicable
  resolved delivery request when project policy permits;
- delivery slices and checkpoints have acceptance criteria, dependencies,
  validation, material edge cases, and safe repository-owned boundaries;
- material product and architecture decisions are resolved;
- current source supports important assumptions; and
- local repository state can be preserved.

Plan authorship and an execution-ready review verdict are not user approval.

Stop before editing when:

- approval is missing or ambiguous;
- the plan has unresolved material decisions;
- target ownership cannot be resolved;
- a required base or branch cannot be established safely;
- current source materially invalidates the plan;
- overlapping local work cannot be separated;
- required credentials, services, or external inputs are unavailable and no
  independent checkpoint can proceed; or
- the plan requires unauthorized destruction, production access, deployment,
  push, merge, or history rewriting.

## Session Fingerprint

Record:

- plan path and SHA-256;
- user approval evidence;
- commit mode, checkout mode, and stop boundary;
- repository roots, branches, bases, integration targets, initial HEADs, and
  pre-existing staged, unstaged, and untracked paths;
- ordered slices and checkpoints with cross-repository dependency edges;
- current checkpoint and accepted checkpoint commits;
- validation-ledger statuses and evidence fingerprints;
- review routes, reports, per-lens snapshot validity, pass counts, convergence
  audits, and usage metrics;
- owned uncommitted paths, failed diffs, and quarantined repositories; and
- unresolved advisories or blockers.

Keep this in the session plan/task-state mechanism. Do not create a repository
journal unless the user or project explicitly requires one.

## Continuation Capsule

When context pressure rises, record:

- current slice and checkpoint, owning repository, branch, and HEAD;
- accepted commits or no-commit evidence;
- checkpoint-owned and unrelated paths;
- currently due validation and evidence state;
- completed, invalidated, and required review lenses;
- unresolved findings and convergence state;
- active process identifier and required poll action;
- blocker or missing authority; and
- one exact next safe action.

The capsule is an execution cursor, not a stopping reason. Consume it by
continuing work after compaction.

## Repository Behavior

Use the existing safe checkout by default. Create or operate an isolated
workspace only when the user or project authority permits it.

Independently resolve every repository's branch, base, initial HEAD, and
unrelated status. Run Git commands inside the owner. Never stage a nested Git
repository from its parent.

Before every authorized commit:

- inspect status and complete checkpoint diff;
- confirm the plan fingerprint;
- stage explicit checkpoint-owned paths only;
- preserve unrelated changes; and
- confirm a due slice gate already passed.

Record commit hashes in accepted-checkpoint mode. In no-commit mode, retain
scoped diff and validation/review evidence. A failed checkpoint leaves
accepted work intact and blocks only its dependency chain.

## Snapshot Validity

Validation and review evidence applies only to the exact source it examined.
Material edits, changed bases, or changed supplemental evidence invalidate
affected coverage. A new commit requires an applicability assessment; unchanged
behavior and inputs can retain prior checks with a documented reason.

Do not reuse prior-session evidence unless its source fingerprint and results
are reconstructable. Mark uncertain evidence unresolved and rerun it before
acceptance.

## Compaction Recovery

After compaction:

1. Recover only missing or changed phase-relevant instructions.
2. Verify the capsule against the plan hash, repository status, accepted
   commits, and current source.
3. Reconstruct checkpoint and validation state from reliable evidence.
4. Poll any recorded active process first.
5. Otherwise execute the exact next safe action.

Do not return a status-only response while executable work remains.

## Stop Boundary and Handoff

An explicit stop boundary may name a checkpoint or slice. Complete and accept
that boundary, run due gates, and preserve later work as pending.

When stopping, report:

- termination reason and evidence;
- accepted checkpoints and commits or no-commit evidence by repository;
- current uncommitted checkpoint diff;
- blocked checkpoints and transitive dependencies;
- exact blocker;
- completed validation and review;
- current reviewed snapshot and invalidated or required lenses; and
- the smallest user decision or external change needed to resume.
