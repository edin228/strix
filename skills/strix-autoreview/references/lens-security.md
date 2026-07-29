# Security Lens

Review changed trust-boundary behavior for concrete authorization, isolation,
privacy, injection, and secret-handling defects.

## Coverage checklist

- **Identity and authority:** Check authentication, authorization, roles,
  tenant/organization ownership, user-supplied resource identifiers, and every
  supported entry point that can reach the changed action.
- **Input provenance and interpreters:** Trace attacker-controlled values
  through proxy headers, URLs, redirects, SQL, shells, filesystem paths, HTML,
  deserialization, templates, and other interpreters to the authoritative
  validation or encoding boundary.
- **Data and secret exposure:** Check responses, serializers, logs, caches,
  events, exports, errors, demo paths, credentials, tokens, and cross-tenant
  identifiers for unintended disclosure.
- **Public and external boundaries:** Check endpoints, webhooks, uploads,
  callbacks, and provider events for required signature, replay, size, origin,
  rate, content, and trusted-proxy controls.
- **Enforcement ownership:** Check that the authoritative API, service, worker,
  or storage boundary enforces the control across alternate callers rather
  than relying only on presentation code.

Trace unchanged guards, resource owners, serializers, and callers only far
enough to prove whether the changed path preserves the current boundary.

## Calibration boundaries

A changed organization-scoped lookup that filters only by a caller-supplied
record ID is a material true-positive pattern when another tenant can name that
ID. A constant internal filename, parameterized query, safely escaped rendered
text, or authenticated same-tenant lookup is not a finding merely because it
touches a filesystem, database, HTML, or tenant-aware feature.

## Exclude

- Generic hardening with no supported attacker-controlled path and material
  impact.
- Dependency-version, header, cryptography, or rate-limit preferences not
  implicated by the changed behavior.
- Availability, migration, transaction, or performance critique unless it
  directly creates a security-boundary failure.
- Defense-in-depth additions when the existing required control is already
  enforced at the authoritative boundary.
