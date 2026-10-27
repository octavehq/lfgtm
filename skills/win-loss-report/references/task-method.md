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

Run two cohort checks on every report, before any driver analysis, and
report both in the cohort section even when they find nothing:
- **Bulk close dates.** Count closed deals per close date. A date holding
  many times the typical daily count of losses is most likely a pipeline
  cleanup sweep: name the dates and counts, show the win rate with and
  without the swept deals, and treat their loss reasons as likely CRM
  defaults rather than buyer explanations.
- **Ownership.** Split the cohort by whether the opportunity had an assigned
  owner (or any owner activity) and give the won count over the total for
  each side, for example "owned deals won 8 of 25, unowned deals 3 of 90".
  A large gap here usually explains more of the headline rate than any theme.

Drop any stage finding that follows from what the stage means. Deals that
reached the final stage (negotiation, contract sent) mostly won because
reaching it is close to winning, so "every deal that reached negotiation
won" is circular and never leads. A stage finding counts only when it
compares like with like: conversion between two stages by segment, persona
or competitor, or time spent in a stage for wins against losses.

For each theme/objection compute unique supported deals, won/lost counts,
loss rate with theme, comparable loss rate without theme, and percentage-
point difference. Absence requires assessable source coverage; unobserved
themes remain unknown, not automatically absent. Match offering/Motion/
segment and window before comparing;
if comparability/support is weak, mark exploratory and avoid a reliable
ranking. Show uncertainty and alternate explanations: deal difficulty,
late-stage exposure, acquisition mix, and sales execution may confound it.

A theme is a loss driver only when its loss rate is above the baseline loss
rate, and a win driver only when its win rate is above the baseline win
rate; show the baseline beside each driver's rate, and a theme on the wrong
side of it is reported as neutral or as counterevidence, never as a driver
([rule 28](../../shared/information-principles.md#claims-against-the-data)).
Before finishing, read every section title, summary line and chart title
against the numbers under it: a claimed range or "every band" must hold for
each bar shown, or the headline names the exception (rule 27).

Group losses by the loss reasons the CRM recorded, quoted as recorded, and by the workspace's own library entities. The product gap / value / readiness / process / competition split below is your reading of buyer exchanges, labeled as such; apply a sales methodology or loss taxonomy only when the workspace has one on file ([rule 18](../../shared/information-principles.md#reading-calls-and-deals)). Every driver, pattern and counter links to the quote or deal behind it, and the evidence list states how many quotes back the report (rule 20). Personal facts stay out of quotes and patterns (rule 19).

Prioritize an intervention using excess-loss association, affected volume/
value, evidence strength, and practical actionability; explain the choice.
Do not rank 4/5 above 6/20 solely because 80% exceeds 30%. Read underlying
buyer exchanges to distinguish product gap, value/price, readiness, process,
and competition. A recommended counter must address the observed mechanism.
Replace speculative “Winnable if” with “Intervention to test.” Retain a
buyer-stated necessary condition only when sourced, without claiming that
satisfying it would guarantee the win. Each action names owner, next step,
validation event, and the condition that would change the recommendation.

Use [Ask Octave first](../../shared/octave-research-toolkit.md#ask-octave-first-for-questions-that-span-records) for orientation before building the cohort: ask `ask_octave` which objections, competitors, personas, and proof points are most tied to won and to lost deals in the scope. Use the answer to form hypotheses and decide which cuts and deal deep dives to examine. Every figure in the report still comes from the normalized opportunity rows and the analytics contract; a graph ranking or count is never the headline number, and outcomes the answer names are read from each deal with `get_deal` before they shape a line. If the tool is unavailable, build from the CRM rows and findings and say so.
