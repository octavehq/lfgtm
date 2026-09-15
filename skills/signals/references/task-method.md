# signals: task method

Load [analytics-contract.md](../../shared/analytics-contract.md) for windows, identity, and coverage.
Retrieve the current active-opportunity roster from accessible CRM data,
not only this period's events; attach account ID, opportunity ID, Motion,
owner, stage, stage history, next step/date, relevant participants, and last
buyer/seller interactions. Retrieve sufficient earlier communication to
assess response baselines and inactivity. Inspect tool schemas for the
available CRM/event operations; do not invent a stage-change event enum.

Create a detector coverage record: required fields, source, observation
window, last sync, eligible population, missingness, and runnable/qualified/
unavailable state. Retrieve relevant Motion/cell narratives for content-gap
detection, not just entity names. Ask grouped targeted questions for material
supplementary usage telemetry, timing exceptions, or process context using
[evidence-and-inputs.md](../../shared/evidence-and-inputs.md). Incorporate supplied data and resume.
When unknown, agree on a qualified observation or instrumentation task;
missing coverage must not become negative evidence about a buyer.

- Champion response overdue: there is an unanswered request for a reply,
  a verified relevant contact, and enough comparable prior exchanges to
  estimate that contact's baseline. Screen at >2× median response interval
  with at least three completed prior exchanges as a configurable initial
  screening heuristic; show support/window and
  honor known absence or agreed future dates. Otherwise use the explicit
  agreed reply date or label timing unknown. Do not diagnose disengagement.
- Stalled opportunity: active roster member with no qualifying interaction
  for 14 days (configurable), after checking next-step dates and sync coverage.
- Stage movement: compare timestamped CRM stages using that pipeline's order;
  include old/new values. Stage changes across pipelines need explicit mapping.
- New opportunity: opportunity creation/first verified CRM identity, not the
  first event at a domain. Renewal and expansion opportunities remain distinct.
- New competitor: first observed active-evaluation evidence in the retrieved
  opportunity history; identify buyer vs seller mention and comparison role.
  Exclude former-employer, incidental, and historical references from urgency.
- Theme trend: unique eligible conversations/accounts with the theme divided
  by all eligible conversations/accounts, using comparable periods. Show both
  counts, rate difference, ratio, and support. A >2× objection rate or >50%
  competitor-rate increase is a screening flag, not proven business change.
- Proof usage: >3 distinct conversations means frequently used, not effective.
  Zero use over 30 days is a review candidate only when relevant interactions
  occurred and usage coverage is complete; never infer poor proof quality.
- Library gap/staleness: compare observed theme and actual cell guidance.
  Zero cell associations does not establish stale content; inspect current
  applicability, source age, conflicting evidence, and Motion activity.

Rank by decision consequence, deadline, affected opportunity value/scope,
evidence quality, and whether a useful action exists. CRITICAL requires a
credible imminent decision/risk, not merely a novel extraction. Distinguish
new, materially changed, unchanged, resolved, and insufficient coverage using
the prior briefing when available. Without prior state, call this a baseline.

Deliver up to three priority actions: source/date; why now; owner/role; exact
next action; expected outcome; dependency; and dismiss/review condition.
Group lower-priority observations separately. No changed actionable signal
is a valid result. Load [output-readiness.md](../../shared/output-readiness.md) at delivery and check
that each diagnosis satisfies its detector prerequisites. If the user asks
to act, continue into the appropriate existing skill with this context;
load [workspace-mutations.md](../../shared/workspace-mutations.md) only for a requested library change.
