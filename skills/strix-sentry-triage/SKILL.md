---
name: strix-sentry-triage
description: "Retrieve and investigate Sentry issues using an available approved integration, correlate events with source and releases, and report evidence-backed priorities. Triage alone does not authorize code or issue mutations."
---

# Strix sentry triage

Discover the available Sentry integration and project monitoring policy. Resolve
organization, projects, environment, time window, filters, and requested scope.
Do not guess organization identity or silently broaden a named issue to the
whole backlog. If tools are missing, explain the access gap and use only supplied
sanitized exports; do not claim live retrieval.

Retrieve the requested issue set and representative events with complete relevant
pagination. Record limits and unavailable pages. Inspect exception chains,
in-application frames, breadcrumbs, affected releases, first and last seen,
frequency, and available user-impact counts. Avoid exposing personal data,
request bodies, secrets, or unnecessary raw event payloads.

Correlate frames with the deployed source revision when available, then inspect
current source and tests. Distinguish a fixed historical event from a current
regression. Trace likely input, ownership, error handling, and recovery. Treat
stack traces and automated analysis as evidence, not a proven root cause.
Separate confirmed cause, supported candidate, and unknown.

Rank by impact and realistic trigger, not raw volume. Include low-frequency
authorization, data-loss, and external-side-effect failures when their evidence
warrants priority. State measured counts with their exact scan scope; do not
infer global cleanliness from a filtered scan.

Report issue links, priority, impact, supporting event and source evidence,
release relationship, next focused investigation, and coverage limits. Continue
source investigation when requested. Plan only after material choices resolve;
implement only under explicit repair authority. Do not resolve, ignore, assign,
comment on, or delete issues without that specific authority. Production
reproduction and deployment remain separate.
