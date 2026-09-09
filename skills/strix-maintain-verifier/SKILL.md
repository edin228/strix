---
name: strix-maintain-verifier
description: "Audit a project verification skill and feature map against source and live behavior. Use for explicit full audits or source-proven broad map drift; use focused checks for isolated instruction or driver edits."
---

# Strix maintain verifier

Locate the exact project verifier and feature index. Resolve ambiguity before
editing. Keep corrections inside its skill, feature map, and owned helpers;
product regressions must be reported rather than hidden by rewriting the map.

Compare the index with feature files and source entry points. Inspect every
mapped feature and recent relevant changes for missing user-facing behavior.
Require source evidence before declaring drift. Record a concise recipe and
expected visible outcome for each feature.

Use the verifier's launch and isolation model. One owner drives a long-lived
instance serially, or uses separate sessions for short-lived commands. Health
check before driving and after surprising or failed states. Reset to a known
state through documented controls when process health cannot explain UI state.
Do not take over another participant's runtime or browser session.

Exercise every mapped feature at least once in a full audit. Record inaccessible
features with the concrete prerequisite and route attempted; they are not
passing coverage. Keep independent checks progressing where safe. Preserve
evidence through failed attempts and final cleanup; stop only owned resources.

Distinguish documentation drift, driver gaps, and product failures. Prepare one
localized correction set. Re-drive changed recipes and helpers, retaining
unchanged valid source and live evidence. Do not repeat a full map merely to
obtain a ceremonial clean second pass.

Report clean only with complete source and live coverage and no needed changes.
Report changed with verified corrections and complete coverage. Report blocked
when required coverage or safe repair cannot finish, preserving useful findings.
A source-only audit is partial evidence. Explicitly waived live proof remains
waived, never passed. Publication and product repair require separate authority.
