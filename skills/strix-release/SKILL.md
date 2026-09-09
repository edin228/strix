---
name: strix-release
description: "Preflight, dispatch, or monitor a production release through the project-approved release mechanism. Require explicit release authority for dispatch; status requests remain read-only."
---

# Strix release

Read the project's production procedure before access. Resolve the exact
candidate, environment, trusted release mechanism, and user-authorized mode:
preflight, dispatch, or monitoring. Shipping, a prior release, or a status
request does not authorize a new release. If the project has no release
procedure, inspect available configuration and prepare a proposal; do not invent
provider writes or bypass protections.

Inspect cumulative changes since the deployed versions of affected components,
not only the latest PR. Require candidate-bound tests, compatible component
versions, migration rehearsal and recovery evidence when applicable, and
project-defined queue or concurrency checks. Unknown release state is blocking,
not evidence that no release is active.

Bind readiness to the exact candidate and relevant configuration. Recheck
freshness immediately before one authorized dispatch. Use the trusted protected
workflow and its idempotency or admission mechanism. Preserve a non-secret
record of the intended candidate, dispatch attempt, and returned run identity.
Do not substitute a direct host or provider deployment.

If dispatch times out or returns an ambiguous result, discover matching runs
read-only before any further action. Do not replay an ambiguous write. A new
release or recovery mutation needs the project's explicit recovery authority.
Monitor an existing matching run rather than dispatching another.

Distinguish running, approval-wait, provider-unavailable, failed, and successful
states. An observer timeout does not mean the release stopped. Use documented
polling and resource limits; do not invent numerical limits as measured facts.
Verify the deployed artifact or source identity and health evidence required
by the project before claiming success. Preserve partial component outcomes.

Report candidate, cumulative scope, safety evidence, run URL or identifier,
final status, deployed identities, and the precise recovery step if needed.
Do not clean up workspaces, delete branches, or perform an unrequested rollback.
