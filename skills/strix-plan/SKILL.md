---
name: strix-plan
description: Write or refine source-grounded software implementation plans after material product and architecture decisions are resolved. Use when a user asks to create an implementation plan, turn agreed requirements into executable delivery slices, or update a draft plan from resolved feedback. Do not use for independent plan auditing, plan approval, implementation, or unresolved product discovery.
---

# Strix Plan

Create an executable draft while distinguishing source-verified readiness,
user approval, and implementation. Independent plan review is due when requested,
project-required, or justified by an irreversible action or expensive dependent
design risk; it is not an automatic extra stage.

## Establish the Contract

Identify:

- intended outcome, scope, and non-goals;
- resolved product and architecture decisions;
- target Git repositories and ownership boundaries;
- dependencies, rollout limits, and validation expectations; and
- requested plan path or the project-declared plan directory.

If no plan location is declared, use an established repository convention or
default to `docs/plans/<concise-kebab-name>.md`.

Stop before drafting when an unresolved choice would materially change product
behavior, scope, destructive-data handling, public contracts, or architecture.
List the decision and its consequences instead of selecting it merely to
complete the plan.

## Read Project Authority

Read the workspace root `AGENTS.md`, then the nearest repo-local `AGENTS.md`
for every target repository. Read only the referenced guides relevant to the
planned behavior.

Treat repository instructions as the authority for risk, validation, branches,
architecture, operations, and planning policy. Do not weaken or duplicate
those rules in the plan.

## Ground the Plan in Source

Inspect the smallest relevant set of current source, tests, schemas,
migrations, configuration, and prior plans needed to:

- identify current owners and extension points;
- distinguish new files from modified files;
- choose between competing ownership candidates;
- name exact paths for every new file;
- identify established patterns to read before writing;
- derive realistic tests, edge cases, and validation commands; and
- expose stale assumptions and cross-repository dependencies.

Keep this phase read-only for product source. Do not implement, generate
migrations, create feature branches, or alter configuration.

## Structure the Draft

Use vertical delivery slices: independently useful product or system
capabilities rather than horizontal model, service, UI, and test phases.

For each non-trivial delivery slice, define dependency-ordered execution
checkpoints. Every checkpoint must state:

- one primary outcome and its parent delivery slice;
- exactly one owning Git repository;
- explicit dependencies;
- likely modified paths and exact new-file paths;
- read-before-write ownership or patterns;
- deterministic validation and relevant test scenarios;
- material edge cases and failure behavior;
- acceptance criteria; and
- why the state is safe to review and commit independently.

A checkpoint may cross layers inside one repository when needed to prove the
outcome. Split cross-repository work into repository-owned checkpoints and
separate commit boundaries.

Keep cohesive atomic changes together. Split unrelated risk domains,
migrations, runtime side effects, background dispatch, security boundaries,
and UI when a safe intermediate state exists. Explain why any large atomic
transition cannot be divided safely.

Include rollout, compatibility, recovery, and integration gates when material.
Do not hide unresolved choices behind phrases such as “if needed” or “use X if
possible.” Inspect and choose, or name the unresolved decision.

## Check Completeness

Before writing the final draft, verify:

- source evidence supports every ownership decision;
- each delivery slice provides an independently useful outcome;
- each checkpoint has one repository owner and an executable dependency order;
- tests and material failure paths appear alongside the behavior they cover;
- acceptance criteria are observable;
- validation is exact enough to execute;
- cross-repository work does not imply a multi-repository commit; and
- no material product or architecture choice was deferred to implementation.

Mark source readiness, any due independent review, and approval status
separately. Plan authorship alone does not authorize implementation.

## Hand Off

Report the plan path, source areas and project rules used, unresolved
non-material questions, and freshness limits. Recommend `strix-plan-review`
when requested, project-required, or justified by a concrete early-review risk.

Do not approve the plan, begin implementation, commit, push, merge, deploy, or
edit product source.
