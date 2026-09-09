# Strix

Strix is a portable set of risk-aware workflows for software agents. It turns
good engineering habits into repeatable skills without assuming a particular
language, framework, repository layout, or deployment platform.

The collection contains 24 independently installable skills. Core workflows
read repository instructions for commands, branch policy, runtime ownership,
and authorization. The Sentry and OKLCH skills are optional adapters.

## Workflows

For a resolved change, use `strix-deliver`. Bounded low-risk work uses a short
scope and acceptance note. Larger or riskier work uses a source-verified plan
and `strix-implement`, with focused checks during implementation and one
combined review at closeout. Independent plan review is available on request,
when project-required, or before a concrete irreversible or costly design risk.
Readiness and user approval remain separate.

```text
resolved request → source verification and proportionate planning
                 → authorized implementation + focused checks
                 → combined closeout review + verified repairs
                 → required live proof → local result

explicit PR request → publication
explicit ship request → publication when needed + protected merge
explicit release request → production preflight + authorized dispatch
explicit retirement request → disposition proof + authorized cleanup
```

Each skill also works independently. When copying a subset, install companions
you want to use or follow the project's equivalent procedure. The skills name
fallbacks rather than requiring unavailable private helpers.

| Skill | Purpose |
| --- | --- |
| [`strix-autoreview`](skills/strix-autoreview/SKILL.md) | Run isolated structured code reviews |
| [`strix-branch-review`](skills/strix-branch-review/SKILL.md) | Review and verify branch changes |
| [`strix-bug-hunt`](skills/strix-bug-hunt/SKILL.md) | Find and fix verified product defects |
| [`strix-close-worktree`](skills/strix-close-worktree/SKILL.md) | Integrate and retire a feature workspace |
| [`strix-code-impact`](skills/strix-code-impact/SKILL.md) | Trace routes, callers, consumers, and tests |
| [`strix-create-verifier`](skills/strix-create-verifier/SKILL.md) | Create a source-grounded application verifier |
| [`strix-deliver`](skills/strix-deliver/SKILL.md) | Deliver a change through local completion |
| [`strix-fix-to-pr`](skills/strix-fix-to-pr/SKILL.md) | Take a bounded correction through its PR |
| [`strix-implement`](skills/strix-implement/SKILL.md) | Implement checkpoints and review at closeout |
| [`strix-maintain-verifier`](skills/strix-maintain-verifier/SKILL.md) | Audit verification maps against source and runtime |
| [`strix-oklch`](skills/strix-oklch/SKILL.md) | Evaluate OKLCH colors, contrast, and gamut |
| [`strix-plan`](skills/strix-plan/SKILL.md) | Write source-grounded implementation plans |
| [`strix-plan-review`](skills/strix-plan-review/SKILL.md) | Audit plans for safe implementation |
| [`strix-publish-pr`](skills/strix-publish-pr/SKILL.md) | Publish the exact reviewed branch tip |
| [`strix-release`](skills/strix-release/SKILL.md) | Release an exact approved production candidate |
| [`strix-resolve-issue`](skills/strix-resolve-issue/SKILL.md) | Resolve a named defect or exact issue bundle |
| [`strix-retrospective`](skills/strix-retrospective/SKILL.md) | Reflect on completed work using session evidence |
| [`strix-sentry-triage`](skills/strix-sentry-triage/SKILL.md) | Triage Sentry errors against current source |
| [`strix-ship`](skills/strix-ship/SKILL.md) | Ship reviewed changes through protected merge |
| [`strix-trim-complexity`](skills/strix-trim-complexity/SKILL.md) | Find behavior-preserving simplifications |
| [`strix-ui`](skills/strix-ui/SKILL.md) | Improve interfaces using project conventions |
| [`strix-unslop`](skills/strix-unslop/SKILL.md) | Edit writing for plain and natural language |
| [`strix-verify-web`](skills/strix-verify-web/SKILL.md) | Verify web behavior with focused live evidence |
| [`strix-worktree`](skills/strix-worktree/SKILL.md) | Operate isolated development worktrees |

An ordinary review or investigation is read-only by default. A combined
"bug hunt and branch review" requests one localized review-and-repair pass
unless explicitly read-only. Local commits follow user and project authority.
AI findings require source verification; deterministic checks remain authoritative.
See [the port coverage](docs/port-coverage.md) for retained boundaries and
[adoption examples](docs/adoption-examples.md) for choosing a subset.

## Design

Strix separates two kinds of knowledge:

1. **Workflow invariants** live in the skills: source grounding, approval
   boundaries, checkpoint ownership, risk-proportional validation, finding
   verification, and Git safety.
2. **Project authority** lives in the adopting project: repository roots,
   branches, test commands, architecture rules, production boundaries, and
   runtime procedures.

Start with [`templates/AGENTS.md`](templates/AGENTS.md), adapt it to the
project, and keep specific commands there. See
[`docs/project-contract.md`](docs/project-contract.md) for the contract the
skills expect.

## Ask an Agent to Adapt Strix

The easiest adoption path is to give this repository to Codex, Claude, or
another capable coding agent while it is working inside the target project.
Replace `<STRIX_GITHUB_URL>` and use a prompt like:

```text
Read <STRIX_GITHUB_URL> and adapt the Strix workflows to this project.

First inspect this project's repository instructions, Git roots, branch
conventions, CI, tests, architecture docs, and data-handling policy. Install
or copy only the Strix skills we need. Fill the adopting-project contract in
our AGENTS.md rather than copying Strix placeholders literally.

Resolve and document:
- repository ownership and plan locations;
- development and production-fix bases;
- validation commands and integration gates;
- project risk rules and operational approval boundaries;
- whether source may be sent to an external review model;
- autoreview model/reasoning and web-search policy; and
- the installed path or invocation for strix-autoreview.

Keep Strix's approval gates, read-only reviewer isolation, input
fingerprinting, finding verification, and current-snapshot review semantics.
If our agent runtime is not Codex CLI, adapt only the review-engine boundary
and preserve the structured output schema, read-only execution, failure
semantics, and tests.

Apply safe project-specific replacements. Ask only about unresolved safety
decisions or authority not supplied by this request before dependent actions.
Do not enable implementation commits or external review without that authority.
Validate the installed skills and run the autoreview unit tests and a safe
dry run before reporting completion.
```

This is intentionally an adaptation prompt, not a blind installation command.
The workflows are portable; repository topology, commands, provider policy,
and authority are not.

## Replacement Checklist

An adopting agent should resolve these project-owned values:

| Concern | Replace or document |
|---|---|
| Repository topology | Git roots, owners, nested instructions, plan directory |
| Git | Feature base, production-fix base, branch and commit conventions |
| Validation | Focused tests, static checks, slice gates, final checks, CI-only checks |
| Risk | Project-specific high-risk behavior and required specialist routes |
| Authority | Commit, push, merge, deployment, production, and destructive-action rules |
| Review provider | Whether project source may be processed by the configured model provider |
| Reviewer | Approved model/reasoning or permission to use Codex's service default |
| Current documentation | Whether reviewer web search is allowed; it is off by default |
| Runtime | Installed skill paths and the command used to launch the review engine |

Do not hardcode the path to the Strix clone into a shared project unless that
path is itself a project convention. Resolve an installed skill directory at
runtime or copy the selected skill into the project's agent-skills location.

## Codex and Claude

`strix-autoreview` ships with a tested Codex CLI runner. It requires current
`codex exec` support for ephemeral read-only sessions, ignored user config,
JSONL events, an output schema, and last-message output. Run
`codex exec --help` during adoption. Authentication still comes from the
user's Codex home, but personal configuration, plugins, and MCP servers do not.

For Claude or another review engine, keep the workflow and replace the engine
adapter deliberately. The replacement must still:

- operate in a disposable repository snapshot with no remote;
- have read-only tools and no approval path for mutations;
- consume the same complete, fingerprinted review input;
- return one object matching the bundled review schema;
- distinguish blocking findings from engine failure; and
- preserve exit codes and current-snapshot invalidation behavior.

Do not translate the runner into an unrestricted one-line model command. The
isolation and completion semantics are part of the workflow's value.

## Distribution

The repository is a Codex plugin and each directory under `skills/` is also a
self-contained skill. This allows the same source to be distributed as one
plugin or selected skill folders. Until Strix is published to a marketplace,
clone the repository and ask your agent to adapt or copy it locally.

The bundled autoreview runner and stage wrapper are Python and use only the
standard library. They never fetch, and web search is disabled by default.

## Status

Strix is experimental. A private source project remains an independent proving
ground during incubation; changes are deliberately ported rather than
synchronized automatically. See [`docs/maintenance.md`](docs/maintenance.md).

## Origins and Attribution

Strix Autoreview is adapted from the MIT-licensed `autoreview` workflow in
[`openclaw/agent-skills`](https://github.com/openclaw/agent-skills). Strix
retains OpenClaw's copyright and license notice, while maintaining a smaller
Codex-first implementation with project-neutral routing, input controls, and
implementation-loop integration.

Thank you to the OpenClaw contributors for making the original workflow
available.

## License

MIT. See [`LICENSE`](LICENSE) and [`THIRD_PARTY_NOTICES`](THIRD_PARTY_NOTICES).
