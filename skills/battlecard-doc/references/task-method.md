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

### What a card for one deal shows

A competitor read is strongest where it is specific to how buyers decide. Build the card from these, in this order of weight, and leave out any the evidence does not support:

1. **A read and a play for each part.** Every section pairs what the evidence shows about the competitor there with the move to make, tied to that evidence. A section with a read and no play is unfinished; generic advice is not a play.
2. **What the decision turns on.** The dimensions buyers themselves compare the two on, which side each favored, and which the buyer treated as decisive, in the buyer's words. Search this deal's calls and the calls of deals against the same competitor (`search_call_transcripts`, `get_call_transcript`). This is the centre of the card.
3. **Quotes with their outcome.** Each quote carries who said it, the company, the date, and whether that deal was won, lost or is open. Keep what buyers said apart from what our own reps said. Give what buyers in lost deals said the most weight: it is what the seller has not heard yet.
4. **What happens to deals when they are in it.** Win rate with the competitor present against the baseline, and the change in cycle length and deal size (`get_entity_outcome_stats`, as below, with `get_competitive_insights` for the period's trend), then the same for this deal's own segment and buyer where the tools give it. Every figure names its period and the number of deals behind it; a figure from a handful of deals says so.
5. **How our claims landed.** What our reps claimed against this competitor, how buyers reacted, and what they pushed back with. This replaces a generic objection list.
6. **Their commercial facts as buyers stated them.** Pricing, contract terms, what makes a buyer switch to or from them, what keeps a buyer with them, and what else the buyer is considering. Quote figures as the buyer gave them and say who said so.
7. **What changed recently.** Whether they are coming up more or less, the newest intel with how to counter it (`get_intel`), and any release that closes a gap buyers had named. A beta is called a beta.
8. **Deals like this one.** Won, lost and stalled deals where the same competitor appeared, closest to this deal first, with what decided each (`list_deals`, `get_deal`).
9. **Who they are, in one strip.** Size, funding, founding and headquarters, with estimates marked as estimates. One strip, never a section.

A card for one deal ends on what to do in this deal next: the one thing to say, the one thing to show, and the one question to ask, each traced to something above it.

[single-competitor-sections.md](single-competitor-sections.md) names the page's sections and their markup (the hero, the deal situation, a section per competitor, our pitch). Fill those sections from the nine parts above. Where the two differ, the nine parts decide what leads and what is left out: a strengths and weaknesses grid, a watch-out or a trap question appears only when it carries one of the nine parts, with its evidence, and never to fill the template.

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
