---
name: strix-fix-to-pr
description: "Own one bounded correction through investigation, repair, validation, and pull-request publication when the user explicitly requests both the fix and its PR. Exclude unresolved features and high-risk repairs."
---

# Strix fix to pr

Confirm the request explicitly authorizes a fix and PR publication. That
request covers the scoped local repair, necessary commit, ordinary push, and
creation or update of its PR. A request only to fix locally does not qualify.

Trace the symptom through current source and direct callers. Establish one
incorrect outcome, its expected behavior, the owning paths, realistic failure
states, and focused regression evidence. Screenshots establish symptoms, not
root causes. If already fixed, intentional, or unproved, report that disposition
without manufacturing a branch or PR.

Use this quick route only for a compact low-risk or standard-risk correction.
If investigation exposes security, migrations, concurrency, external effects,
data loss, or material unresolved choices, stop before expanding implementation
and explain the full planning or safety work required. Preserve the original
publication authority if the user continues the same correction.

Check for attributable existing work before choosing a safe checkout or the
project's isolated workspace. Keep unrelated work intact. Capture a truthful
before image for a visual correction when publication needs comparison.

Use strix-deliver when installed, or perform the same scoped implementation,
focused validation, and one combined closeout review. Bounded low-risk work
needs no formal plan. Standard-risk work needs source-verified planning. Use
rendered proof when a visual claim cannot be established by deterministic
checks. Sanitize captures; label an unavailable baseline honestly.

Commit only the accepted repair and publish the exact reviewed tip through
strix-publish-pr when installed, or the project's protected PR procedure.
Describe the trigger, resulting behavior, validation, and material limitations.
Do not ask again for publication authority already supplied by this request.
If push succeeds but PR creation fails, preserve the branch and resume from
fresh remote state rather than duplicating the PR.

Stop at the PR URL and verified remote head. Monitor and repair CI only when
requested. Merge, production release, issue mutation, and workspace retirement
remain separate. Reflect once after the outermost requested boundary completes.
