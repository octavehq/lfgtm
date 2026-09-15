# win-loss-report: task method

Load [analytics-contract.md](../../shared/analytics-contract.md). Specify offering/Motion, included
pipelines/stages, close-date window, timezone, reporting cutoff, currency,
and requested segment/persona/competitor filters. Retrieve CRM outcomes and
supporting calls; create one normalized row per opportunity ID with final
status as of cutoff, close date, account, amount/currency, loss reason,
and linked persona/segment/use-case/competitor IDs. Resolve duplicate events
and reopenings using CRM history; open-at-cutoff opportunities are excluded
from the closed win-rate denominator and reported separately when useful.

Win rate = won / (won + lost). Count every included opportunity once in the
headline. For multi-valued personas/competitors, label breakdowns overlapping:
a deal can appear in several groups, so group totals are not additive.
Include unknown attribution explicitly rather than assigning a guessed
competitor/persona. No-decision is a separate recorded loss subtype only
when CRM or sourced operator clarification supports it.

For each normalized row attach call/evidence availability. Do not conflate
missing conversation evidence with missing outcome. Reconcile totals against
retrieved CRM rows; disclose capped samples, excluded records, currency
handling, and unresolved IDs. Ask targeted questions for material outcome
ambiguities or supplementary business-value context, incorporate sourced
answers, and regenerate dependent metrics before proceeding.

For each theme/objection compute unique supported deals, won/lost counts,
loss rate with theme, comparable loss rate without theme, and percentage-
point difference. Absence requires assessable source coverage; unobserved
themes remain unknown, not automatically absent. Match offering/Motion/
segment and window before comparing;
if comparability/support is weak, mark exploratory and avoid a reliable
ranking. Show uncertainty and alternate explanations: deal difficulty,
late-stage exposure, acquisition mix, and sales execution may confound it.

Prioritize an intervention using excess-loss association, affected volume/
value, evidence strength, and practical actionability; explain the choice.
Do not rank 4/5 above 6/20 solely because 80% exceeds 30%. Read underlying
buyer exchanges to distinguish product gap, value/price, readiness, process,
and competition. A recommended counter must address the observed mechanism.
Replace speculative “Winnable if” with “Intervention to test.” Retain a
buyer-stated necessary condition only when sourced, without claiming that
satisfying it would guarantee the win. Each action names owner, next step,
validation event, and the condition that would change the recommendation.
