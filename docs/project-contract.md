# Adopting Project Contract

Strix discovers project policy from repository instructions instead of a
Strix-specific configuration format. The adopting project's root `AGENTS.md`
is the authority; nested repository instructions may add or override rules for
their scope.

## Required Authority

Document the following when it is relevant:

- repository roots and ownership boundaries;
- development bases and production-fix bases;
- plan directory and planning references;
- required validation commands by repository and change type;
- architecture and code-ownership references;
- risk definitions or project-specific high-risk behavior;
- permitted review providers, source-data eligibility, and whether web search
  is allowed;
- approved reviewer configuration or permission to use the review engine's
  isolated default;
- commit, push, merge, deployment, and destructive-action authority;
- production access rules; and
- migration, background-job, external-side-effect, or runtime procedures.

The project may omit categories it does not use. Strix should inspect ordinary
repository conventions when a harmless detail is missing; it should stop only
when guessing could make the action unsafe or materially alter the outcome.

## Repository Discovery

For one repository, treat the current Git root as the owner. For a workspace
containing nested repositories:

1. read the root `AGENTS.md`;
2. discover relevant Git roots from current source and declared paths;
3. read the repo-local `AGENTS.md` for each affected root; and
4. execute Git, validation, and commit commands inside the owning repository.

One execution checkpoint may depend on another repository, but it may not own
or commit changes from multiple Git repositories.

## Validation Contract

Prefer exact commands. A useful contract distinguishes:

- focused tests required for touched behavior;
- repository-wide static checks;
- integration gates for delivery slices;
- migration or runtime validation;
- checks that require external services; and
- checks that CI, rather than a local agent, owns.

If no command is declared, inspect package metadata, CI configuration, and
existing developer documentation before asking the user.

## Risk Contract

Projects may define their own classes. When they do not, use:

- **High:** security and authorization boundaries, destructive or irreversible
  actions, money, migrations, concurrency, synchronization, external side
  effects, secrets, production operations, and realistic data-loss paths.
- **Standard:** ordinary workflows, CRUD, APIs, caching, shared components,
  and behavior whose failure is recoverable.
- **Low:** local presentation, copy, documentation, and reversible UI details.

Classify the changed behavior, not its directory or feature label.

## Authority Defaults

Local inspection, implementation, and validation are allowed when requested.
Do not infer authority to push, open or merge a change request, deploy, access
production, delete branches, remove worktrees, rewrite history, or destroy
data.

## Autoreview Contract

Autoreview is optional for low-risk work and advisory everywhere. An adopting
project should state:

- whether its source may be processed by the configured model provider;
- source categories that must never leave the local environment;
- whether the bundled Codex runner is approved or another engine adapter is
  required;
- an approved model and reasoning level, or that the review engine's isolated
  default is acceptable;
- whether public web search may be enabled for current dependency contracts;
  and
- any specialist route required beyond Strix's behavior-based defaults.

Strix rejects common credential paths and disables web search by default, but
these controls do not replace the project's data-classification policy.
