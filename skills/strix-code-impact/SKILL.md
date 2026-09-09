---
name: strix-code-impact
description: "Trace source-proven impact from a route, file, or diff to handlers, callers, consumers, and focused tests. Use for API-flow changes and ownership questions; results are advisory, not exhaustive or a CI selector."
---

# Strix code impact

Resolve the Git root, exact source snapshot, and requested route, file, or diff.
Read relevant repository instructions. Use a project-maintained read-only
analyzer when available and inspect its supported boundaries. Otherwise use
bounded source search and direct inspection; do not invent an analyzer command.

For a route, trace method, mount prefix, handler, middleware, authorization,
serialization, server callers, and browser callers. For a file, identify every
relevant owned route rather than selecting only the first match. For a diff,
compare before and after, including removed and renamed paths and remounted
routes. Distinguish changed handlers from unrelated same-file owners.

Inspect direct consumers, cache and state effects, tests, and generated
contracts where source supports the relationship. Cite repository-relative
locations and explain each edge. Label dynamic dispatch, generated code,
external consumers, missing source, and unsupported framework behavior as
coverage limits. An empty analyzer result is not proof of no impact.

During implementation, query at useful discovery points and inspect the final
changed relationships at closeout. Rerun when the analyzed source changes;
never combine partial results from different snapshots. Do not start watchers,
build a new index, fetch refs, or access production merely for impact analysis.

Report exact scope, owners, proven callers, affected contracts, suggested
focused tests, and unknown boundaries. Run project-required validation even
when a graph omits its tests. Analysis does not authorize implementation or
external mutation.
