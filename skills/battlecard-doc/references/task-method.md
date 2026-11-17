# battlecard-doc: task method

Select format (HTML/text) and scope before collecting inputs:
- Deal card: named account and selected opportunity, with one/more rivals.
- Reusable competitor card: selected offering/Motion and rival; no account
  is required, and account-specific situation facts are omitted.
- Landscape: all relevant rivals/alternatives for the selected portfolio
  scope; no account is required. --competitor all defaults to this branch.
Honor supplied choices and ask only material unresolved questions.

### Start from what Octave already knows about the competitor

For every competitor on the card, read these three before the library profile, and build on them:

1. **Octave's own battlecard.** `get_entity` on the competitor with `includeBattlecard: true` returns the battlecard Octave generated for it: the executive brief, momentum, the threat assessment and how to respond, by section. When there is one, it is the starting point. Keep its positions, sharpen them for this deal or scope, and do not write a second card beside it that disagrees. `battlecard` is null until the competitor's first intel run; then work from the profile.
2. **Intel on the competitor.** `list_intel` for the competitor, then `get_intel` on the items that bear on this card: what they shipped, changed or announced, with dates and citations. Use the newest relevant items and keep their dates on the page.
3. **How deals against them went.** `get_competitive_insights` for the period gives how often the competitor came up and how those deals ended. Lead the card's "where we win" and "where we lose" with it.

Where the deal's own calls contradict the battlecard or the intel, say which is newer and go with the evidence from this deal. Where none of the three has anything, say nothing about it and work from the library and the calls.

Load [gtm-context.md](../../shared/gtm-context.md). Resolve offering, Motion, buyer cells, and
competitive Custom Playbook. Read full selected offering, competitor,
proof/reference, and cell narratives; list results are discovery only.
For a deal card, resolve the actual account/opportunity through available
CRM/context tools, retrieve its calls/events, and inspect underlying buyer
statements with existing event-detail/transcript tools. Do not substitute
competitor-wide wins for this account's decision criteria.

Build a deal situation record: current system, business consequence,
required outcome, must-have criteria, participants/roles, evaluation/POC,
procurement, timeline, commercial constraints, and partners. Attach source
and date to each fact. Load [evidence-and-inputs.md](../../shared/evidence-and-inputs.md) for missing
material criteria, POC evidence, or process facts; ask grouped questions,
incorporate sourced operator answers, and resume the card. Agree on working
placeholders or general guidance where answers remain unknown.
Read the account's calls in their setting per
[Reading Calls and Deals](../../shared/information-principles.md#reading-calls-and-deals)
rules 16 to 21: a concern praising the product's reach stays out of the
objections, each deal-specific point links to its call or record, and
personal facts stay out of the card.

For each important buyer criterion record: priority and source; our
applicable capability/tier and proof; competitor capability/tier and dated
source; migration/operating tradeoff; discovery question; recommended next
action; and fit/concede condition. Separate confirmed fact, vendor claim,
customer experience, and hypothesis. Refresh mutable disputed feature or
price claims through available authoritative sources, or ask the operator
for current documentation; label unresolved comparison facts explicitly.

For a deal card, and for a reusable card when the workspace has history with the rival, use [Ask Octave first](../../shared/octave-research-toolkit.md#ask-octave-first-for-questions-that-span-records): ask `ask_octave` which deals, calls, objections, and personas the competitor is tied to, and where it won and lost. Treat the result as a map to the calls and events worth reading in full, and as a source of workspace evidence for concessions and counters, not as a replacement for current rival capability checks; verify any claim about this deal with a narrow read before it reaches the card. Landscape cards may ask one question per rival. If the tool is unavailable, use the competitor, findings, and call tools and say so.

Write a counter only when it addresses the actual criterion. A legitimate
rival advantage may require concession, qualification, partner support,
or a proof task. Never manufacture a rhetorical answer to a product gap.
Include status quo/DIY where those are live alternatives. Questions should
reveal decision criteria and evidence, not imply unsupported rival defects.
Use proof relevant to this segment, use case, scale, and switch condition.
When reporting win rates, load [analytics-contract.md](../../shared/analytics-contract.md) and show
closed-deal counts, cohort, and limitations; do not infer from anecdotes.
Read win rates for an alternative or objection from `get_entity_outcome_stats` (with and
without the entity) before saying anything about them, and show the baseline beside the
rate: a rate above the baseline means deals with this alternative win more often, not that
it is hard to beat ([rules 26 and 28](../../shared/information-principles.md#claims-against-the-data)).
"No closed deals" needs that read plus a deal search, not one empty event query.
