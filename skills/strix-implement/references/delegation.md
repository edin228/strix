# Delegated implementation

Use this reference only when delegation is available and authorized. Keep one
writable actor per checkout. The resident owns sequencing, acceptance, staging,
commits, and authority; the worker owns investigation, implementation, debugging,
and affected checks. Keep trivial edits resident when delegation adds no value.
A worker already assigned this workflow executes directly without spawning agents.

## Assignment and context

Use project-approved models and supported effort settings, honoring user
overrides. Select effort for complexity, uncertainty, and failure consequences;
a failed command alone does not justify escalation. Pass a selected model and
effort explicitly when inheritance would select something else. Verify available
tool capabilities before edits. Missing tools require a capability report, not
repeated unchanged spawns or an unsupported claim about a model's abilities.

Prefer a fresh context for a substantial checkpoint; reuse a worker for repairs
or small continuations needing the same investigation. Explain the choice at the
boundary. Accumulated debugging history or repeated compaction favors replacement
at a safe boundary, not cancellation or replay of accepted work. Keep scheduling
and model choices out of the implementation plan.

Give a self-contained brief with repository root, branch, starting HEAD, current
plan and checkpoint, acceptance, owned paths, exclusions, dependencies, risks,
required instructions, and validation commands with working directories. Include
relevant design references and existing evidence, not the full transcript.

## Write ownership

Before assignment and after return, validate authority-bearing paths from the
owning Git root. Require normalized repository-relative paths within that root.
Reject `.git` components, existing symlink components including leaves, and
paths whose nearest existing ancestor belongs to a different Git owner. For
directory ownership, inspect tracked entries for symlinks and gitlinks and do
not grant scope across nested Git metadata. Preserve ambiguous state and resolve
ownership before another mutation.

The worker edits and tests only owned paths. It must not stage, commit, amend,
reset, restore, clean, stash, change worktree lifecycle state, publish, deploy,
access production, invoke another reviewer, or spawn agents. Use project-owned
cache-safe diagnostic conventions. Remove only exact artifacts it created and
can identify safely. The resident must not edit, stage, commit, or run mutating
checks while the worker owns writes; read-only inspection may continue.

Let the worker finish without routine acknowledgment gates. It reports blockers
promptly and returns concise outcomes and evidence. Use completion notifications
or the longest wait compatible with platform communication requirements; avoid
rapid status polling, process inspection, or empty messages merely to show activity.

## Return and transfer

Require changed paths, source evidence, commands, working directories, exit
statuses, starting commit and returned diff covered by checks, runtime or fixture
prerequisites, edits after testing, blockers, and artifact locations. A normal
return yields writes and leaves the worker idle until reassigned.

Inspect the complete diff, path containment, exclusions, root, branch, HEAD,
index, status, and artifacts. Accept reconstructable evidence rather than an
unsupported verdict. Reuse passing checks on unchanged inputs; agent changes or
a commit alone do not invalidate them. Name the source, hook, runtime, or evidence
change before rerunning. Unexpected commits or unsafe paths require resolution
without rewriting history.

Before replacement or resident fallback, confirm the previous worker has yielded
or cannot resume writes. An interruption or absent process alone is insufficient.
Transfer requirements, current state, completed work, decisions, rejected attempts,
evidence, and the next action. Preserve interrupted work and inspect it before
continuing. Do not introduce a second writer to recover a stalled assignment.

Route verified review findings to the implementation author while its context is
useful, or transfer safely. Prefer the simplification author for findings caused
by its cuts. The resident accepts source and validation evidence and commits only
under existing authority after writes are yielded. A worker cannot provide the
independent review of its own changes.
