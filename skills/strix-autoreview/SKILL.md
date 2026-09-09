---
name: strix-autoreview
description: Run isolated, structured, risk-proportional AI code reviews for local changes, branch diffs, commits, or checkpoint-scoped paths. Use for advisory closeout reviews, focused architecture/security/reliability/migration/performance/frontend-integration review, or a justified early review after deterministic validation. Do not invoke automatically at every implementation checkpoint. Do not use as a replacement for tests, source inspection, or human verification of findings.
---

# Strix Autoreview

Run a read-only advisory review in an isolated Git snapshot. Verify every
finding against current source before changing or reporting code.

Contract version: `1.0.0`

Read `references/operating-reference.md` completely before the first real
review in a session. It owns target selection, provider and data boundaries,
snapshot behavior, sensitive-path rejection, completion semantics, and
provenance.

## Workflow

1. Run focused deterministic validation first.
2. Classify the changed behavior using project policy:
   - high risk: review every non-trivial change with the dominant specialist
     route and any distinct required route;
   - standard risk: review non-trivial behavior with one generalist or dominant
     specialist route; and
   - low risk: skip autoreview unless the user asks or a shared surface raises
     practical risk.
3. Select local, branch, or commit mode. Pass `--base` when the base is not
   unambiguous.
4. Resolve this skill's `scripts/autoreview` path and run it from the Git
   repository being reviewed.
5. Treat P0–P2 findings as blocking candidates, not facts. Reproduce or trace
   each one in current source.
6. Reject speculative hardening, style preferences, hypothetical failure
   modes, and broad rewrites.
7. Treat P3 as nonblocking and do not fix it merely to empty the report.
8. After a confirmed fix, rerun affected deterministic checks and inspect its
   direct interactions. Independently recheck materially changed safety
   boundaries or an explicit re-review request; retain unaffected evidence.
   Do not repeat a whole review merely because a repair changed the tip.

Do not push, merge, deploy, or mutate Git merely to obtain a review.

## Commands

Use the actual installed skill path in place of `<strix-autoreview>`.

Dirty local work:

```bash
python3 <strix-autoreview>/scripts/autoreview --mode local
```

Branch work:

```bash
python3 <strix-autoreview>/scripts/autoreview \
  --mode branch --base <base-ref>
```

Single commit:

```bash
python3 <strix-autoreview>/scripts/autoreview \
  --mode commit --commit HEAD
```

Checkpoint-scoped local work:

```bash
python3 <strix-autoreview>/scripts/autoreview \
  --mode local \
  --scope-path src/owner.ts \
  --scope-path tests/owner.test.ts
```

Focused review:

```bash
python3 <strix-autoreview>/scripts/autoreview \
  --mode branch --base <base-ref> --lens security
```

Built-in lenses are `architecture`, `security`,
`data-integrity-reliability`, `migrations`, `performance`, and
`frontend-integration`. A lens narrows attention but cannot override the
engine's safety, schema, scope, or finding rules.

Bounded parallel stage:

```bash
python3 <strix-autoreview>/scripts/autoreview-stage \
  --mode branch --base <base-ref> \
  --lens generalist --lens security
```

Use one direct review by default. Use the stage only when one stable target
needs two or three distinct routes. It preserves every report, groups only
byte-identical findings, performs no synthesis model call, and rejects a
changing input.

## Reviewer Configuration

The bundled runner currently supports Codex CLI. Pass an explicit
project-approved model for reproducibility, or omit `--model` to use Codex's
service default. User configuration is deliberately ignored by the isolated
review subprocess. Use `--thinking high` for difficult standard-risk and
high-risk review unless the project has validated another setting.

Required Codex capabilities include `exec`, read-only sandboxing, ephemeral
sessions, JSONL events, output schemas, and last-message output. Run:

```bash
codex exec --help
```

before adapting the runner to a materially different Codex version or another
review engine.

Web search is disabled by default. Pass `--web-search` only when a current
public dependency contract materially affects the review and repository policy
allows it. Never use web search to transmit repository content.

## Input Safety

Every real review uses a disposable no-hardlink clone with its remote removed.
Scoped local review copies only scoped overlays while retaining committed
context. Source input is fingerprinted before and after review.

Likely credential paths anywhere in the tracked snapshot, private-key files,
`.env` files other than explicit templates, and common credential stores fail
before reviewer invocation. This name-based gate is defense in depth, not a
secret scanner.

Review only repositories trusted enough for the configured model provider.
Autoreview makes the tracked repository snapshot, selected uncommitted
overlays, and supplemental evidence available to that provider. Do not include
credentials, personal data, customer data, or unnecessary proprietary
material.

## Completion

Exit codes:

- `0`: completed without blocking findings;
- `1`: completed with at least one validated P0–P2 report; and
- stage `2`: incomplete because a reviewer, schema, fingerprint, or cleanup
  failed.

An interrupted, malformed, unstable, or engine-failed review is incomplete,
not clean.

Report the risk classification, exact command, deterministic validation,
accepted and rejected findings, residual P3 advisories, usage metrics or their
unavailability, and the final completion state.
