# Autoreview Operating Reference

## Contents

1. Target selection
2. Reviewer and provider boundary
3. Focused lenses and parallel stages
4. Complete and scoped inputs
5. Sensitive and supplemental inputs
6. Findings, failures, and metrics
7. Provenance

## Target Selection

Run from the Git repository being reviewed. Target precedence is:

1. local changes when `--mode local` is selected or auto mode sees a dirty
   worktree;
2. the explicit commit in commit mode;
3. an explicit `--base` or `STRIX_AUTOREVIEW_BASE`;
4. the current pull request base when `gh pr view` resolves one;
5. the local `origin/HEAD` symbolic ref; and
6. an existing local conventional base ref among `main`, `master`, `develop`,
   and `dev`, preferring remote-tracking refs.

The helper never fetches. It fails when the selected local ref is unavailable.
Fetch deliberately before review when remote freshness matters.

Auto mode on a clean checkout selects branch mode. A target with no changed
paths fails before reviewer invocation.

## Reviewer and Provider Boundary

The bundled runner invokes Codex CLI with:

- an ephemeral session;
- a read-only sandbox;
- approval policy `never`;
- ignored user configuration while retaining Codex authentication;
- ignored execution-policy rule files;
- JSONL events;
- a strict output schema; and
- a disposable no-hardlink Git clone with its remote removed.

Repository instructions and committed source remain visible so the reviewer
can understand project contracts. User-configured plugins and MCP servers are
not inherited. A trusted project may still expose project-scoped configuration
to Codex, so run autoreview only on a repository trusted not to contain hostile
agent instructions. The prompt tells the reviewer to treat repository content
as evidence, but prompt text cannot turn an untrusted repository into a safe
execution boundary.

The reviewer may inspect unchanged callers, schemas, shared helpers, tests,
and repository instructions when required by a changed path. It may not edit,
run tests or generators, install packages, mutate Git, invoke nested reviewers,
or run write-producing commands.

Web search is off by default. Enabling it exposes the reviewer to current
public web content and must follow project data policy. Do not use it to send
source or private evidence to third parties.

The runner makes the tracked repository snapshot, selected uncommitted
overlays, and supplemental evidence available to Codex's model provider. Its
isolated filesystem and path checks do not anonymize that content. Obtain any
organizational approval required for source processing.

## Focused Lenses and Parallel Stages

`--lens` accepts only built-in names. Absolute paths, traversal, symlinks,
non-regular files, unknown names, and oversized lens files fail before model
invocation.

Lenses supplement the shared engine contract:

- `architecture`: ownership, dependency, lifecycle, and contract boundaries;
- `security`: authentication, authorization, isolation, injection, privacy,
  and secret handling;
- `data-integrity-reliability`: persistence, transactions, retries,
  concurrency, partial success, and recovery;
- `migrations`: schema/data transition compatibility, bounds, and rollback;
- `performance`: realistic hot-path amplification and resource exhaustion; and
- `frontend-integration`: API, cache, async-state, lifecycle, and accessibility
  regressions.

Use `autoreview-stage` for one to three unique routes over the same stable
target. The stage fingerprints the shared prompt and evidence, forwards the
same scopes to every reviewer, executes at most three reviewers concurrently,
preserves each report, and performs no synthesis model call.

Exit `0` means a complete stage without blockers, `1` a complete stage with
blocking reports, and `2` an incomplete stage. Preflight failure, engine
failure, invalid output, interruption, input movement, or cleanup failure is
incomplete.

## Complete and Scoped Inputs

Local bundles contain staged, unstaged, and non-ignored untracked changes.
Branch and commit bundles use local Git refs and never fetch automatically.

Inline size thresholds optimize prompt size; they are not eligibility limits.
Large inputs become repository-backed references containing path, byte count,
and SHA-256. The complete file remains in the isolated review repository and
the reviewer must inspect it there.

`--scope-path` accepts literal repository-relative files or directories, not
Git pathspecs. Absolute paths, traversal, repository root, and `.git` metadata
are rejected. A scope selecting no changed paths fails.

Use scopes to isolate an implementation checkpoint from unrelated dirty or
earlier no-commit work. Include every checkpoint-owned path. The local
snapshot reproduces scoped index state and then final worktree state so staged
and unstaged evidence remain distinct.

Input manifests and prompt fingerprints are checked during snapshot creation
and after the reviewer exits. A changed source or supplemental input rejects
the report.

## Sensitive and Supplemental Inputs

The helper checks every tracked path in the repository snapshot plus every
selected untracked or supplemental path, and rejects likely credential paths
before reviewer invocation, including:

- `.env` and non-template `.env.*` files;
- common credential stores and authentication JSON;
- `.ssh`, `.aws`, `.azure`, and `.gnupg` directories;
- common private-key basenames; and
- `.pem`, `.key`, `.p12`, and `.pfx` files.

Templates ending in `.example`, `.sample`, or `.template` remain eligible.
Rename a confirmed non-secret fixture when its safety-sensitive filename is
rejected; do not add a bypass merely for convenience.

This is a conservative name-based boundary, not content-level secret
detection. A non-secret test fixture with a rejected name must be renamed or
excluded from the repository before review. Ignored files are not included
automatically, but all tracked source and explicit evidence still require
human data judgment.

`--prompt-file` and `--dataset` accept existing regular repository-relative
files outside `.git`, with no symlink components. Absolute paths, traversal,
directories, devices, FIFOs, and sensitive paths fail. Files are opened through
anchored no-follow descriptors where the platform supports them.

## Findings, Failures, and Metrics

Findings are advisory. Verify P0–P2 against current source and require a
supported trigger, concrete material impact, and proportionate fix. Reject
unrealistic paths, style preferences, alternative valid architectures,
speculative hardening, and unrelated redesign.

P3 is nonblocking and never makes an otherwise correct patch fail. Findings
outside changed paths are ignored. A valid report with blocking findings is a
completed review, not an engine failure.

Every successful real review emits an `autoreview usage: {json}` line with
available token counts, elapsed time, prompt size, explicit model and reasoning
configuration, lens, event counts, and process exit code. Missing usage events
do not invalidate an otherwise valid report; unavailable values remain
explicit.

Heartbeat and stage progress output show liveness only. Do not interrupt a
review merely because it is slow. A final validated report is required for a
verdict.

## Provenance

Strix Autoreview is an independently adapted descendant of the MIT-licensed
`autoreview` workflow from `openclaw/agent-skills`. Strix's initial extraction
compared the public upstream repository at commit
`fe588b1a6267eb47f785d0c748db9f6f3e9a3b4f`.

Strix intentionally keeps a smaller Codex-first surface rather than vendoring
the current multi-engine upstream implementation. Preserve this skill's
`THIRD_PARTY_NOTICES` when redistributing it.
