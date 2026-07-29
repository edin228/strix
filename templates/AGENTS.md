# Project Agent Instructions

## Workspace

Describe the Git repositories in this workspace and the directory owned by
each one. State where implementation plans belong.

## Instruction Hierarchy

Require agents to read this file, then the nearest repo-local `AGENTS.md`.
List reference documents that apply only to migrations, frontend work,
external integrations, production, or other specialized areas.

## Engineering Principles

- Prefer the simplest correct implementation that follows established
  patterns.
- Preserve unrelated user changes.
- Keep changes scoped to the requested outcome.
- Ground decisions in current source and tests.
- Test intended behavior and realistic material failures.

## Risk

- **High:** security boundaries, destructive actions, money, migrations,
  synchronization, concurrency, external side effects, production, and data
  loss.
- **Standard:** ordinary product behavior, CRUD, API integration, caching, and
  shared components.
- **Low:** presentation, copy, documentation, and reversible UI behavior.

Apply rigor to the behavior being changed, not merely its directory.

## Git

For every repository, state:

- feature development base;
- production-fix base;
- branch naming convention;
- commit convention; and
- which actions require explicit user approval.

Do not push, merge, deploy, rewrite history, or delete branches without the
authority declared here.

## Planning

Use independently useful delivery slices. Divide large slices into
risk-cohesive execution checkpoints. Every checkpoint must name:

- one primary outcome and parent delivery slice;
- exactly one owning Git repository;
- explicit dependencies;
- likely modified files and exact paths for new files;
- tests, validation, and material failure behavior;
- acceptance criteria; and
- a safe review and commit boundary.

Separate repositories into dependency-ordered checkpoints and commits.
Require independent plan review and explicit user approval before executing a
large or materially risky plan.

## Validation

List exact focused and repository-wide commands by repository or change type.
State which integration checks, migrations, external services, and CI checks
are required.

Do not report implementation complete without running the required checks or
clearly reporting an external blocker.

## Autoreview

State whether project source may be processed by the configured review-model
provider. Name any prohibited source or data categories.

Choose one reviewer policy:

- use Codex's isolated service default;
- pass an explicitly approved model and reasoning level; or
- use a project-maintained adapter for another read-only review engine.

Web search is disabled by default. Document when it may be enabled for current
public dependency contracts. Keep credentials, personal data, customer data,
and unnecessary proprietary material out of review inputs.

Use `strix-autoreview` after deterministic validation for high-risk changes
and non-trivial standard-risk behavior. Treat its findings as advisory:
verify P0–P2 in current source and rerun invalidated checks and lenses after a
material fix.

## Operations

State the rules for production access, deployments, databases, migrations,
background workers, external providers, and destructive cleanup. Explicit
user authorization should be required for production or irreversible actions.
