# insights: task method

Load [analytics-contract.md](../../shared/analytics-contract.md) before computing frequencies/trends.
Normalize the user's topic, offering/Motion, persona, segment, account/deal,
start/end dates, timezone, and requested comparison into one filter record.
Carry every applicable constraint into each query using the current tool's
supported schema. If a filter is unsupported server-side, filter complete
returned records locally using verified IDs, or disclose the restriction;
do not silently drop it. Resolve named entities before querying.

Retrieve events/findings for the current window. For requested trends,
retrieve an equal comparable baseline with identical eligibility/coverage.
Use supported pagination; record pages, unique event/account/deal counts,
limits, and retrieval completeness. A semantic result list is a ranked
sample, not a population aggregate. If full coverage cannot be obtained,
label the sample and avoid claims of population prevalence or trend.

Use findings to identify themes, then inspect underlying event details or
transcript receipts for the most consequential claims and counterexamples.
Deduplicate finding/event IDs and repeated excerpts. For each theme count
unique eligible conversations and accounts/deals, not extraction snippets.
Keep counts by seller/buyer speaker side. Baseline absence is an explicit
unknown, not a zero. Ask targeted supplementary questions only where an
answer changes the requested conclusion; continue through supplied answers.

For a value-prop presentation, classify the observed exchange:
used by seller; acknowledged by buyer; challenged; resolved with evidence;
unresolved; or next action committed/completed. Quote the supporting turn
and record event/date/role. Seller usage alone is not resonance; a delivered
counter alone is not successful objection handling. Treat deal outcomes as
associations unless the evidence supports a stronger explanation.

For an objection, distinguish: objection observed; response attempted;
buyer explicitly accepted/resolved; remains open; insufficient exchange.
Report response-attempt rate over eligible objections and observed-resolution
rate over assessable exchanges separately, with counts and unknowns.

Before declaring a library gap, load [gtm-context.md](../../shared/gtm-context.md) and hydrate
the relevant offering, persona/segment, objection, and Motion ICP narrative.
Create a match row: theme/evidence → entity/cell/field → existing guidance →
coverage (complete/partial/absent/unverified) → proposed specific improvement.
Do not call content missing when it was not retrieved. Repeated seller use
of existing guidance plus buyer rejection is a conflict to investigate,
not evidence that the guidance works or should automatically be deleted.
