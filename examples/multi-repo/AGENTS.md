# Example: Multi-Repository Product Workspace

## Workspace

This directory contains independent Git repositories:

- `service/`: API and background jobs;
- `web/`: browser application; and
- `docs/`: product documentation.

Save cross-repository plans under `plans/` in the workspace repository. Run
Git and validation commands inside the repository that owns each change.

## Instruction Hierarchy

Read this file, then the target repository's `AGENTS.md`. Repo-local
instructions own technology, validation, and architecture rules for their
scope.

## Git

The workspace and docs repositories develop from `main`; service and web
develop from `develop`. Production fixes start from `main` in every repository.
Never combine files from multiple Git repositories in one checkpoint or
commit. Do not push, merge, deploy, or delete branches without explicit user
approval.

## Planning

Represent a cross-repository capability as dependency-ordered checkpoints. For
example, stabilize and validate a service contract before implementing the web
consumer. Each checkpoint must remain safe and reviewable at its own committed
state.

## Validation

- `service/`: focused repository-declared tests, then its required static
  checks;
- `web/`: focused UI tests, typecheck, lint, and relevant build checks;
- `docs/`: link and documentation build checks; and
- cross-repository slices: an explicit contract or integration gate after all
  owning checkpoints pass.

## Operations

Database migrations, workers, external providers, deployments, production
access, and destructive cleanup follow repo-local operational guides and
require the authority declared there.
