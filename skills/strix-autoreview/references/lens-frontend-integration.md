# Frontend Integration Lens

Review changed frontend behavior for concrete API-contract, async-state,
cache, lifecycle, and accessibility regressions.

## Coverage checklist

- **API and query contract:** Check request and response fields, error shapes,
  query keys, enabled conditions, defaults, and every supported caller. For
  state-dependent actions, verify eligible entity statuses, every operation
  invalidated by the request, and whether queued, partial, and completed
  responses drive distinct truthful UI outcomes. Trace shared request and
  mutation wrappers end to end: preserve HTTP failure semantics across every
  supported error shape, cancellation or abort propagation, wrapper-owned
  callback precedence, and ordering between cache reconciliation and caller
  continuations.
- **Cache continuity:** Check mutation and realtime success, background failure,
  retry, and reconnect behavior across every cache entry that can display the
  entity. Distinguish initial loading/error from a failed background refetch:
  preserve and visibly qualify usable cached data unless the product contract
  invalidates it. When migrating cache or state ownership, inventory both
  producers and consumers of legacy reload/update signals. Compare exact query key prefix
  and matching semantics. Verify every supported mutation reaches the
  replacement owner.
- **Async and mutation lifecycle:** Check optimistic state, request identity,
  aborts, stale responses, and in-flight refs or loading locks across success,
  error, retry, navigation, component teardown, and page restoration. For each
  acquired UI lock, enumerate its release paths; navigation alone is not
  cleanup when browser restoration can resume the prior page. Treat modal
  dismissal and responsive-owner replacement as lifecycle transitions: do not
  abandon a lock while its side effect is live. If the request may outlive its
  UI owner, preserve a durable post-settlement reconciliation path for the
  captured cache scope; pre-teardown invalidation is sufficient only when
  cancellation guarantees no later server commit. Preserving local state is
  not sufficient when its backing record disappears: verify clean fallback
  identity before the next edit and ensure dirty state has a supported
  create, restore, retry, or discard path instead of invoking an update on a
  record known to be unavailable.
- **Presentation lifecycle:** Check loading, error, empty, suspense, mobile,
  desktop, modal, drawer, and pop-out conditionals against sibling
  presentations. Check breakpoint overlap and whether switching presentation
  unmounts or duplicates a stateful owner, loses reachable state, or leaves an
  entered mode without its controls or exit. For a replacement presentation,
  inventory material data, actions, and status context from the existing
  presentation and verify parity or an intentional product-contract omission.
  When a migration rewires a shared input or state component, compare its exact
  value, callback, icon, and event signatures rather than assuming native DOM
  prop semantics.
  Prove inactive variants are actually non-rendered and non-interactive after
  CSS/display precedence, and that supported keyboard, external, realtime, and
  restored-page entry points select the visible owner.
- **Overlay interaction:** Check initial focus, focus containment, Escape and
  close behavior, background interaction, nested overlays, and focus
  restoration for every changed dialog, sheet, drawer, or pop-out.
- **Interaction accessibility:** Check keyboard reachability, labels,
  announcements, disabled/loading protection, and recovery from failed actions
  in material workflows. On touch presentations, check that material actions
  are not hover-only and that fixed action rows do not clip supported controls.

Inspect unchanged API types, query-key owners, hooks, sibling presentations,
and shared state components only far enough to prove the integration failure.

## Calibration boundaries

Applying mobile-only loading, error, or empty branches to the default desktop
calendar/suspense presentation is a material true-positive regression. A local
color, spacing, icon, copy, animation, or responsive layout change is not an
integration blocker when it preserves data, state, focus, and interaction
semantics.

## Exclude

- Visual polish, typography, color, spacing, breakpoint, motion, or component
  taste without a concrete behavior or accessibility regression.
- Hypothetical stale state with no supported cache entry, event, async race, or
  user sequence.
- A preference for another hook, state library, component composition, or API
  abstraction when the current integration remains correct.
- Backend transaction, migration, security, or server-performance critique
  unless it directly breaks the changed frontend contract.
