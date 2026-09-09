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
Require source-verified readiness before executing a plan. State whether an
explicit request to deliver a resolved outcome also approves its in-scope plan
or whether separate approval is needed. Independent plan review is due when
requested or before a concrete irreversible action or expensive dependent
design decision; projects may require it more broadly.

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

Complete implementation and focused checks, then use one combined independent
review for standard and high-risk behavior. Use a source-capable reviewer or
`strix-autoreview` when its exact scope suffices. Verify findings in source.
Recheck affected behavior after repairs and independently recheck materially
changed safety boundaries. Do not schedule automatic checkpoint autoreview.
Low-risk work normally needs focused checks and resident inspection.

## Operations

State the rules for production access, deployments, databases, migrations,
background workers, external providers, and destructive cleanup. Explicit
user authorization should be required for production or irreversible actions.

## Runtime and verification

Name runtime, port, credential, fixture, browser, and cleanup owners where used.
Assess live proof from changed behavior. Keep not-required decisions and waivers
distinct from passing scenarios. Isolated instruction changes need focused owner
checks; a full verification-map audit is due only when requested or broad drift
is proved. Preserve still-valid source and runtime evidence.

## Workflow routing

Use `strix-deliver` for local delivery and `strix-fix-to-pr` for an explicitly
requested bounded repair through PR creation. PR-only requests use
`strix-publish-pr`; shipping uses `strix-ship`. Production release and terminal
worktree cleanup require separate explicit authority. Do not infer issue
mutation from any of those requests. Reflect once at the outermost completed
boundary with `strix-retrospective`; proposals do not authorize further edits.
