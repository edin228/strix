---
name: strix-publish-pr
description: "Publish or refresh an exact reviewed branch tip as a pull request, or babysit it when requested. Use for PR-only handoffs; do not merge, deploy, or retire the workspace."
---

# Strix publish pr

Resolve the repository, remote, target branch, source request or issue, exact
reviewed tip, current remote head, and any matching open PR. Inspect project
publication rules and required evidence. Reject ambiguous identities and
preserve unrelated work. Do not assume a branch name or hosting provider.

Require explicit publication authority and validated, reviewed committed bytes.
Stage or commit only with appropriate authority. Complete due evidence before
asking for a missing approval. Reuse checks whose inputs still apply; advancing
the target alone does not require integrating it just to publish. Respect any
project-required base comparison or integration gate.

Prepare a concrete PR title and body describing the problem, resulting behavior,
validation, remaining risks, and safe provenance. Preserve existing human prose.
Keep private reports and credentials out of prose and attachments. Do not use
issue-closing keywords unless that issue mutation is authorized. For visual
claims use safe readable captures, with an honest before/after or after-only
label. Do not manufacture runtime proof or passing waivers.

Use a normal push of the exact reviewed commit to the intended feature ref.
If the remote already equals it, skip the push. If the remote differs, prove
its history is expected and the update is a fast-forward; otherwise stop with
both identities. Never force, push directly to the integration branch, or
rewrite another actor's work.

Re-read remote state after pushing and require the PR head to equal the reviewed
tip. Create or update the single matching PR with structured arguments or a
body file. After an ambiguous response, discover whether that exact PR exists
before retrying. Preserve partial success and refresh concurrent body edits.
Use a project receipt format when one exists; do not hand-edit its lineage.

Stop after publication unless babysitting or shipping was requested.
Babysitting authorizes scoped conflict and CI repairs, local repair commits,
ordinary pushes, and PR updates until the current head is mergeable and required
checks pass. Inspect both sides before resolving conflicts. Renew affected
validation and review for a repair; stop on unknown remote work, unresolved
behavior, scope expansion, or an external blocker. Do not keep retrying an
unchanged failure.

Report PR URL, base, reviewed and remote SHAs, evidence, and CI state if checked.
PR publication and babysitting do not authorize merge, production, issue
mutation, branch deletion, or worktree retirement.
