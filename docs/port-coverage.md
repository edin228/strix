# Workflow port coverage

This update deliberately adapts the private source workflows as of 2026-09-09.
It does not copy private runtime scripts, issue content, deployment machinery,
product source, credentials, design assets, or generated evidence. The source
and public collection remain independently maintained.

| Source capability | Public owner | Adaptation |
| --- | --- | --- |
| Planning and readiness audit | strix-plan, strix-plan-review | Source verification; separate readiness and approval |
| Checkpoint implementation | strix-implement | Optional commits and one combined closeout review |
| Structured AI review | strix-autoreview | Existing isolated runner and provenance retained |
| Branch review and defect hunting | strix-branch-review, strix-bug-hunt | Combined requests repair locally; explicit read-only honored |
| Ordinary local delivery | strix-deliver | Project-selected workspace and proportionate planning |
| Bounded repair through PR | strix-fix-to-pr | Publication authority limited to the requested correction |
| Worktree development | strix-worktree | Existing coordinator or native source-only worktree operations |
| PR handoff and babysitting | strix-publish-pr | Exact reviewed head, fast-forward updates, partial-success recovery |
| Shipping | strix-ship | Project-protected merge route; no assumed controller |
| Integration and retirement | strix-close-worktree | Proven disposition, separate reconciliation and cleanup scope |
| Production release | strix-release | Trusted project release mechanism and ambiguity recovery |
| Named defect resolution | strix-resolve-issue | Exact issue set, sanitized evidence, current-source confirmation |
| HTTP and caller impact | strix-code-impact | Project analyzer or bounded source tracing; explicit unknown edges |
| Product UI and UX | strix-ui | Existing design system and consumer contracts; no brand rules |
| Live browser verification | strix-verify-web | Project-owned runtime, focused proof, surviving artifacts |
| Verification generation and maintenance | strix-create-verifier, strix-maintain-verifier | Source-backed maps and honest live coverage |
| Error-monitoring triage | strix-sentry-triage | Optional Sentry adapter; no fixed organization or mutation |
| Color work | strix-oklch | Optional web-color adapter; actual contrast and gamut evidence |
| Complexity review | strix-trim-complexity | Read-only evidence-backed cuts |
| Delivery reflection | strix-retrospective | One outer-boundary reflection; no automatic skill changes |
| Writing cleanup | strix-unslop | Natural prose without overriding the requested voice |

The additional source principles, historical backlog-discovery workflows, and
product-specific impact engines are not exported as automatically selected
skills. Their useful scope, correctness, evidence, and state-ownership rules
are incorporated into the relevant workflows. A repository-wide backlog hunt,
framework analyzer, design-system implementation, or infrastructure controller
would need its own separately scoped adapter.

The new workflow text is adapted from the repository author's private workflow
collection. Existing third-party notices for the autoreview implementation
remain intact. The color adapter is newly written; it does not copy the source
color reference pack or its framework-specific thresholds.
