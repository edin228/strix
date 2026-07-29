# Source–Strix Incubation Model

The private source project and Strix intentionally maintain separate workflow
implementations during incubation.

Initial Strix extraction source:

- extraction date: 2026-07-28
- source areas: implementation planning, plan review, implementation loop,
  autoreview, branch review, bug hunt, and planning policy

No product runtime, production instructions, research artifacts, private
configuration, or product source are included.

## Direction of Change

Do not automatically synchronize the repositories.

When the source project changes:

1. classify the change as a workflow invariant, project adapter, or
   source-only policy;
2. port workflow invariants to Strix deliberately;
3. express reusable variation as a documented project contract or optional
   adapter;
4. leave product topology and operations in the source project; and
5. validate the Strix form without relying on private context.

When Strix changes, adopt it in the source project only after the generic
behavior has been proven and the source project's stricter rules remain
intact.

## Port Checklist

- Compare the complete source workflow, not isolated paragraphs.
- Remove absolute paths, product names, technology assumptions, private
  endpoints, and fixed branch names.
- Preserve safety and acceptance semantics.
- Keep deterministic checks project-owned.
- Verify every AI finding before acting on it.
- Add or update a public generic example when a new abstraction is introduced.
- Record third-party provenance before copying scripts or substantial text.
- Run all skill and plugin validation.

## Future Convergence

Convergence is appropriate after Strix has been exercised in materially
different projects and its project contract can express the source project
without weaker rules. At that point the source project can consume released
Strix skills and retain a thin adapter for repository topology, validation,
domain conventions, runtime, and production operations.
