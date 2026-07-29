# Validation Ledger

Build validation from the approved plan and live project instructions before
editing.

## Ledger Entry

Record for each check:

- stable identifier;
- owning Git repository;
- exact command or observable inspection;
- checkpoint, delivery slice, or final phase when due;
- behavior and failure mode covered;
- prerequisites or external services;
- status: pending, passed, failed, blocked, or invalidated;
- source snapshot or commit;
- result evidence; and
- invalidation trigger.

## Validation Levels

Use the smallest level that proves the behavior:

1. **Checkpoint checks:** focused tests, static checks, schema validation, or
   build steps required before accepting one checkpoint.
2. **Delivery-slice gates:** integration behavior spanning checkpoints or
   repositories.
3. **Repository closeout:** project-required repository-wide checks for all
   changed repositories.
4. **Operational checks:** migrations, background jobs, external providers,
   compatibility, or recovery when the plan and authority require them.

Do not defer all testing to final closeout. Run behavior-owning tests in the
checkpoint that introduces the behavior.

## Command Discovery

Prefer commands declared in `AGENTS.md`. When missing, inspect:

- package and build metadata;
- CI workflows;
- existing scripts;
- contributor documentation; and
- nearby tests for established invocation patterns.

Do not invent a broad expensive suite when focused checks are established.
Do not silently substitute a weaker command for a required check.

## Failure Handling

A due failed check blocks checkpoint acceptance. Fix an in-scope implementation
failure and rerun the affected entry. If failure is pre-existing, external, or
outside scope:

- capture concise evidence;
- determine whether it prevents proving the checkpoint;
- run a legitimate narrower check only when it still proves the intended
  behavior; and
- stop when acceptance would otherwise rely on assumption.

Never mark an unrun or interrupted check as passed.

## Invalidation

Invalidate an entry when a later change can affect the behavior it covered.
Typical triggers include:

- edits to its source or test scope;
- changed generated output or schema;
- changed dependencies, configuration, or base commit; and
- material review-triggered fixes.

Rerun invalidated entries before accepting the affected checkpoint or final
state.
