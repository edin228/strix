# Example: Single-Repository Web Application

## Workspace

This Git repository owns the complete application. Save implementation plans
under `docs/plans/`.

## Risk

Treat authentication, authorization, billing, destructive actions, database
migrations, external side effects, and data loss as high risk. Treat ordinary
application workflows as standard risk and presentation-only changes as low
risk.

## Git

Start feature work from `main` and production fixes from `main`. Use
`type(scope): description` commits. Do not push, merge, deploy, rewrite
history, or delete branches without explicit user approval.

## Planning

Use vertical delivery slices and repository-owned execution checkpoints. Name
exact new-file paths, tests, material failure behavior, acceptance criteria,
and validation in every checkpoint. Require independent plan review and user
approval before executing a large or high-risk plan.

## Validation

- Application changes: `npm test`
- Type safety: `npm run typecheck`
- Lint: `npm run lint`
- Production build when routing or build configuration changes:
  `npm run build`

Run focused tests for touched behavior before the repository-wide checks.

## Operations

Do not access production, run production migrations, rotate secrets, publish
packages, or deploy without explicit user authority.
