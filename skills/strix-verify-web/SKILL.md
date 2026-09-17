---
name: strix-verify-web
description: "Inspect or verify web application behavior through the project-owned runtime and browser. Use for requested browser checks or visual and interaction uncertainty; PR creation alone is not a trigger."
---

# Strix verify web

Read the project's runtime, browser, credentials, fixture, and cleanup owners.
Use its existing verifier and feature map when available. Do not introduce a
second server launcher or browser stack merely to perform verification.

Choose diagnostic inspection or formal acceptance proof. Diagnostics stay
narrow and need no full recording by default. Formal proof follows a source-based
assessment of changed behavior after repairs settle. Name required scenarios;
a full feature-map audit is reserved for an explicit audit or proven broad drift.
Deterministic coverage can support a not-required decision without a waiver.

## Execution ownership

When delegation is available and authorized, assign a dedicated browser worker
with project-approved model and effort; honor direct execution and user overrides.
An assigned worker executes directly without spawning agents. A standalone
diagnostic request does not add a code-review prerequisite.

At implementation closeout, the source-capable code reviewer assesses applicability,
named scenarios, and observable outcomes from source. When a structured review
engine cannot return that assessment, the resident supplies it from source and
deterministic evidence without adding a full review. Pass that assessment, selected
root and candidate snapshot, fixture constraints, relevant feature recipes, and
retained artifacts to the browser owner after repairs settle. Feature recipes
supply navigation and prerequisites, not mandatory unrelated smoke checks.

Confirm access to browser tools, the selected runtime, and evidence storage
before delegation. Missing capabilities are a blocker; do not silently switch
to a different runtime or reviewer. Assign exclusive browser and verification
runtime control. Do not allow another actor to edit source, mutate fixtures or
the database, or drive the browser while proof is being collected.

The worker may operate the prescribed runtime and create safe evidence. It must
not edit application source, stage, commit, spawn agents, publish, or perform
lifecycle actions beyond authorized launch and cleanup. UI writes still need
fixture and action authority. Return tested source, tab and runtime identities,
scenario outcomes, artifact references, cleanup status, and blockers.

The resident checks evidence completeness and routes failures to the repair owner.
For ambiguous outcomes, have the code reviewer inspect captured evidence before
changing expectations. If that reviewer was an ephemeral engine invocation, use
a focused source-capable assessment of the disputed outcome, not another complete
review. Yield browser/runtime ownership before repairs, then rerun
only invalidated scenarios. Never convert a failed or blocked scenario into a
pass through a model verdict or repeated unexplained retries.

## Drive and evidence

Verify the selected runtime's root, source version, owned listener, health,
fixture readiness, and actual browser origin before interaction. Check secure
context when the scenario needs it. Use the declared credentials source without
printing secrets. Stop dependent scenarios if setup is unavailable; do not
silently substitute production or a different workspace.

Own a dedicated browser tab or an explicitly assigned idle tab. Do not drive
another participant's session or sign it out. Prefer semantic locators from a
fresh snapshot over coordinates. After a surprising state, inspect application
and browser health before restarting anything. Dismiss overlays through visible
controls and verify dismissal before the next scenario.

Exercise the real user path and observe both action and result, including
material side effects. Internal state setters and a final screenshot alone do
not prove the interaction. Use approved test fixtures for writes; external or
destructive actions require their appropriate authority.

Record source identity, runtime and fixture state, actual viewport and theme,
scenario, actions, observed result, and safe artifact locations for formal proof.
Distinguish pass, fail, blocked, waived, and not-required. Keep credentials,
cookies, tokens, customer data, and production captures out of evidence. Preserve
artifact identifiers when browser-owned files are not mounted locally.

Stop only resources this verification owns; preserve evidence and verify it
survives teardown. Never delete worktrees, databases, or volumes as browser
cleanup. Reuse proof only while its behavior, fixtures, and runtime assumptions
remain valid. A new commit needs a fresh applicability assessment, not an
automatic repeat drive. Report unverified scenarios and exact prerequisites.
