# Strix

Strix is a portable set of risk-aware workflows for software agents. It turns
good engineering habits into repeatable skills without assuming a particular
language, framework, repository layout, or deployment platform.

The initial release includes:

- `strix-plan`: write source-grounded implementation plans;
- `strix-plan-review`: independently audit plans for execution readiness;
- `strix-autoreview`: run isolated structured reviews over local, branch,
  commit, or checkpoint-scoped changes;
- `strix-implement`: execute approved plans through a validation,
  autoreview, verified-fix, and acceptance loop;
- `strix-branch-review`: review or repair branch changes; and
- `strix-bug-hunt`: investigate concrete defects and optionally repair them.

## How the Workflows Fit Together

The main delivery path is:

```text
requirements
  → strix-plan
  → strix-plan-review
  → explicit user approval
  → strix-implement
      → deterministic validation
      → strix-autoreview
      → verify and fix confirmed findings
      → accept the current checkpoint
  → strix-branch-review
```

Each skill can also be used independently:

| Skill | What it does | Typical result |
|---|---|---|
| `strix-plan` | Turns resolved requirements into source-grounded, dependency-ordered delivery slices and repository-owned checkpoints | An implementation plan with paths, tests, risks, and acceptance criteria |
| `strix-plan-review` | Audits a plan independently before coding | An approval verdict or a precise repair list |
| `strix-implement` | Executes an approved plan checkpoint by checkpoint | Validated changes, optional authorized commits, and resumable checkpoint evidence |
| `strix-autoreview` | Runs an isolated, structured AI review over local, branch, commit, or scoped changes | Verified P0–P3 candidates, a completion state, and usage evidence |
| `strix-branch-review` | Reviews an entire working tree, branch, commit range, or supplied findings | Severity-ranked findings and, when authorized, focused repairs |
| `strix-bug-hunt` | Traces a feature for concrete correctness, security, state, and reliability failures | Reproduced bugs and, when authorized, regression-tested fixes |

The implementation loop treats deterministic tests as authoritative and AI
review as advisory. A reviewer finding is never accepted blindly: the resident
agent must verify its trigger and impact in current source before making a
change.

## Design

Strix separates two kinds of knowledge:

1. **Workflow invariants** live in the skills: source grounding, approval
   gates, checkpoint ownership, risk-proportional validation, finding
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

Show me the proposed project-specific replacements and any unresolved safety
decisions before enabling implementation-loop commits or external review.
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
