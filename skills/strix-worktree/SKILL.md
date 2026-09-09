---
name: strix-worktree
description: "Create, inspect, operate, or safely retire an isolated development worktree under project procedures. Use for explicit worktree tasks or substantial concurrent work, not automatically for small edits."
---

# Strix worktree

Resolve the owning Git root and read the project's worktree, runtime, database,
and cleanup instructions before a lifecycle action. Prefer an existing project
coordinator. Do not invent its commands, locks, registry, or resource names.
If there is no coordinator, use native worktree operations for source-only
isolation and project-documented commands for any runtime.

Inspect existing worktrees, branches, bases, dirty state, and active ownership.
Reuse only an exact safely attributable match. Resolve the intended base from
project policy and current refs. Do not copy unrelated dirty files or secret
configuration into a new checkout. Required input commits must be reachable
from its selected base, or transferred through an explicitly scoped safe method.

Allocate independent runtime ports, databases, profiles, and output directories
only when needed. Prove resource ownership before using or stopping them. Use
the project's fixture or snapshot policy; source-only work does not need an
application runtime. Never guess credentials or print their values.

Record root, branch, creation base, HEAD, owned resources, readiness checks,
and next resumable action. Preserve immutable creation identity across resumes.
Inspect partial state before retrying setup. A printed URL does not prove
runtime or database readiness. Stop on foreign listeners or ambiguous locks;
use the documented recovery procedure instead of deleting locks blindly.

Before removal, require explicit cleanup authority, a clean target including
untracked files, and one proven Git disposition: integrated work, retained
committed work at an identified surviving ref, or explicitly authorized discard.
Prove merge ancestry or the project's accepted squash-equivalence evidence;
a closed PR alone does not prove integration. Preserve the branch by default.
Database restore, reset, and volume deletion need their own destructive scope
and recovery evidence. Verify resource identity immediately before mutation.

Stop only owned runtime resources, then remove through the project coordinator
or native worktree removal without force. Never recursively delete a workspace
root or kill processes by name. Inspect and resume partial cleanup without
replaying successful phases. Report retained resources and pending recovery.
This workflow does not imply push, PR, merge, or production authority.
