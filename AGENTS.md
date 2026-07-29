# Strix Contributor Instructions

## Purpose

Strix packages portable software-delivery workflows as independent agent
skills. Keep reusable process in Strix and keep product topology, technology
commands, runtime operations, and organization policy in the adopting
project's `AGENTS.md` files.

## Repository Rules

- Treat this directory as an independent Git repository.
- Run Git and validation commands from this repository, not its parent.
- Preserve unrelated work and do not push, merge, publish, or tag without
  explicit user approval.
- Use conventional commit messages when a commit is requested.

## Portability Boundary

- Do not add absolute user or repository paths.
- Do not encode product names, private hosts, remote URLs, branch names,
  container names, frameworks, package managers, or test commands in core
  workflow instructions.
- Obtain project facts from the adopting repository's root and repo-local
  `AGENTS.md` files.
- Put optional ecosystem-specific behavior in separately named adapter skills,
  not in the core skills.
- Stop for missing project authority only when the missing decision would make
  an action unsafe or materially change the outcome. Otherwise inspect the
  repository and use the simplest established convention.

## Skill Contract

- Every skill must contain a valid `SKILL.md` with only `name` and
  `description` in frontmatter.
- Keep skill bodies concise and imperative.
- Use `references/` only for details that are conditionally needed.
- Keep `agents/openai.yaml` synchronized with each skill.
- Namespace public skill names with `strix-` so they can coexist with local
  project skills.
- Treat deterministic validation as authoritative. AI review is advisory and
  every reported finding must be verified against current source.

## Workflow Invariants

- Ground plans and reviews in current source.
- Prefer vertical delivery slices and risk-cohesive execution checkpoints.
- Give each checkpoint exactly one owning Git repository.
- Separate plan authoring, independent plan review, user approval, and
  implementation.
- Scale validation and review to the behavior's realistic risk.
- Never infer authority to push, merge, deploy, access production, delete
  branches, or perform destructive cleanup.

## Validation

Before reporting a Strix change complete:

1. Run the skill validator for every skill.
2. Run the plugin validator from the plugin-creator toolchain.
3. Search tracked content for placeholders, private paths, and product-specific
   terms.
4. Inspect the complete diff and repository status.

## Source Evolution

The private source project and Strix are intentionally maintained separately
during incubation. Follow `docs/maintenance.md` when porting a workflow change
between them.
