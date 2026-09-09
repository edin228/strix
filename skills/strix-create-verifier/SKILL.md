---
name: strix-create-verifier
description: "Create a project-local skill for launching, driving, observing, and cleaning up real application verification. Use when asked to build a verifier for a UI, CLI, service, or library."
---

# Strix create verifier

Inspect project instructions, entry points, existing tests and runtime helpers
to establish what users operate, how it starts, how an agent can drive it, how
to observe success, and how instances isolate state. Prefer existing runtime,
authentication, fixture, driver, and cleanup owners. Do not invent commands or
selectors and do not repair product code without that authority.

Write the verifier in the project's declared skill location. Include name and
description frontmatter and runtime-appropriate UI metadata. Use the available
skill-creation tooling when useful. Ground each instruction in source:

- launch commands, prerequisites, readiness, and source identity;
- a read-only health check for the correct owned instance;
- real selectors or commands for user actions;
- observable results and material side effects;
- evidence locations outside disposable runtime state; and
- teardown of only the exact processes and scratch resources the run owns.

Seed a feature index and source-backed feature recipes with entry paths,
prerequisites, actions, observable outcomes, and known limitations. State initial
coverage explicitly instead of claiming an exhaustive map. Use stable semantic
handles. Preserve secrets and shared-session ownership. A dry-run mode must be
checked for actual side effects before treating it as safe.

Add executable helpers only for repeated mechanics that need them; document
and test their invocation. Keep product policy in project references rather
than duplicating it in generated instructions.

Run the generated launch, health check, one mapped user path, evidence capture,
and cleanup end to end in an authorized test environment. Verify artifacts
survive teardown, including failed attempts. Re-drive a corrected helper before
claiming it works. If prerequisites prevent runtime proof, provide a structurally
validated draft and name the blocker; do not claim a completed verifier.

Point to strix-maintain-verifier when installed for later audits. Generation
does not authorize production, external messages, destructive fixture changes,
publication, or product repairs.
