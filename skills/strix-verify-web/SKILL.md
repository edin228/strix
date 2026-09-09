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
