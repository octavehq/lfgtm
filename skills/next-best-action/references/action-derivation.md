# Action derivation — gap taxonomy, ranking, evidence lanes

How a raw pile of tool results becomes at most three recommended actions. This is the skill's method; follow it in order, don't freestyle.

The core invariant: **an action exists only where a prescription and an observation disagree.** No prescription (nothing in the library covers it) → it's a library gap, not a deal action; note it and move on. No observation (no evidence either way) → it's a discovery question, not an instruction. Both present and aligned → nothing to do; that's success, not a failure to find an action.

## 0. Commitment integrity comes first

Before G1 to G8, reconcile promises and mutually agreed next steps. This is G0, but it is not another
strategy-gap category: a promise already made carries its own prescription.

Classify commitment states with the single vocabulary in
[action-ledger-and-learning.md](action-ledger-and-learning.md) § Commitment ledger — this section
only says how each state ranks against other candidate actions:

- **Internal commitment open:** fulfill it, renegotiate it, or provide a concrete status update.
  This normally outranks a new play because trust is already at stake.
- **External commitment open:** monitor until due; follow up with the promised context after due,
  not with a generic nudge.
- **Mutual next step booked:** treat it as coverage and prepare for it; do not recommend scheduling
  what already exists.
- **Fulfilled/superseded:** retire it with positive evidence.
- **Unobservable:** say the completion channel is not visible. Never call it overdue solely from a
  negative search.

Use the structured commitment extraction types when available. Otherwise mine verbatim transcripts
and CRM/email activity, and label the result caller-supplied or inferred as appropriate.

## 1. Establish position first

Before hunting gaps, fix the deal's position on three axes. Every gap type below reads against this position.

| Axis | Source | Fallback |
|------|--------|----------|
| **CRM stage** | `get_deal_deep_dive` → `stageName`/`stageCategory` + stage history | None (render as explicit gap) |
| **Methodology stage** | Map the buyer's observed mindset onto the Motion ICP cell's `salesMethodology` stages: earliest stage whose Buyer Mindset the evidence does NOT yet confirm is the stage you are in | CRM stage category mapped coarsely (early → first stage, mid → second, late → last) |
| **Buying committee** | `get_deal_deep_dive` → stakeholder rollup, vs the personas the Motion ICP cell / playbook prescribes | Findings participants; else unknown, skip committee gaps |

State the position in one sentence at the top of every output: *"CRM says Negotiation; the buyer's language is still mid-methodology (urgency not yet established); committee is single-threaded below the line."* Divergence between the first two axes is itself gap G2.

## 2. Gap taxonomy

Walk all eight. For each, the **trigger** is a concrete evidence condition — if you can't point to the tool result that fired it, it didn't fire.

**The coverage check** (used by G1, G4, G7): prefer
`get_deal_strategy_evidence({ opportunityOId, entityOIds, occurredAfterIso })` when registered. It
returns the relevant entity-linked findings and explicit zero-evidence rows. These are receipts,
not verdicts. Otherwise, `list_findings({ query: "<play topic>", eventFilters: {
companyDomains } })`, keep `speaker: "internal"` rows, and inspect their `linkedEntities` for the
play's oId. `search_call_transcripts({ entityOId, speakerSide: "internal", companyDomain })` is the
sharper second instrument: the rep's actual on-call moments about the play's entity, with timestamps
to order against the buyer signal. An internal finding or moment linked to that entity = the play
ran — check its timestamp against when the buyer signal surfaced; a proof shown *before* the doubt
doesn't count as an answer to it. Treat zero/thin results as "not shown to have run" unless source
coverage and freshness support an absence claim.

### G1 — Unanswered strategy signal
The buyer voiced something the library has a play for, and no evidence shows the play ran.
- **Trigger:** an external finding (objection, pain agreement, question, competitor mention, excitement) semantically matches a library entity (objection counter, proof point, use case, value prop from the cell), AND no internal finding (`CALL_INTERNAL_*` — objection handling, proof-point presentation, value-prop presentation) or sent-email finding shows it was addressed.
- **Action shape:** run the play — in the buyer's own words. Cite the verbatim moment (`search_call_transcripts` / `get_entity_evidence`, with recording timestamp) and the library play.

### G2 — Stage mismatch
CRM stage and methodology stage disagree, in either direction.
- **Trigger:** CRM stage implies a methodology stage whose Buyer Mindset the evidence does not confirm (deal is *ahead of the buyer* — highest-risk state), or the buyer's language is ahead of the CRM stage (deal is under-called; less urgent but distorts forecast).
- **Action shape:** the earliest unmet objective from the cell's methodology — e.g. the urgency-building move with the cell's Talking Points — not "update the CRM field" (that's hygiene; mention it in one clause at most).

### G3 — Missing committee coverage
A persona the prescription requires is absent from the observed stakeholders.
- **Trigger:** Motion ICP cell / playbook names buyer personas (economic buyer, user champion); stakeholder rollup + findings show nobody matching one of them (title/seniority match), or `reachedSeniorBuyer: false` / `singleThreaded: true` where the prescription requires more before the current stage's exit. Confirm the absence with `search_call_transcripts({ attributedPersonaOIds: [<prescribed persona>], companyDomain })` — no moment attributed to a contact classified into that persona means the gap is real, not a rollup artifact.
- **Action shape:** who to add (find real candidates via `find_person` — never invent a name), through whom, opening with the cell's value prop *for that persona*. This is what "multi-thread" looks like when it's strategy-grounded.

### G4 — Competitive exposure without a counter
A competitor is live in the deal and the competitive prescription hasn't run.
- **Trigger:** competitor mentions in `get_deal_deep_dive` competitive intel or findings; a `COMPETITIVE` motion playbook or competitor entity with win/loss reasons exists; no internal finding shows the counter-positioning was presented.
- **Action shape:** the specific differentiation angle from the playbook, aimed at what the buyer actually said about the competitor (quote it). Execution hook: `/octave:battlecard-doc`.

### G5 — Momentum decay against benchmark
The deal is slower than the workspace's own pattern, and a strategy-grounded reactivation exists.
- **Trigger:** `get_deal_deep_dive` — days in stage well past `velocityBenchmarks` median, repeated close-date pushes, or activity flatline in `activityContext`.
- **Action shape:** ONLY actionable when paired with a re-entry reason from another gap or change vector (fresh intel, new proof, a buying trigger firing). "It's been quiet, follow up" does not clear the bar; silence is the trigger, never the content.

### G6 — Fresh intel unexploited
Something changed on our side or in their market since the last touch, and the deal hasn't heard it.
- **Trigger:** since the window start — a library revision relevant to this deal's cell (`list_revisions`), an accepted/pending suggestion with mounting evidence (`list_suggestions`), a segment/market item from `get_latest_gtm_report` touching the account's segment, or a new reference/win in the same segment.
- **Action shape:** the outreach this intel justifies, tied to the deal's known pains — not a newsletter. This is the gap type that makes *recurring* runs pay for themselves.

### G7 — Proof gap
The buyer is skeptical on a point we can prove, and the proof was never shown.
- **Trigger:** external finding shows doubt/question on a claim; a proof point or reference matching it exists in the library; internal findings show it was not presented (or was presented before the doubt surfaced).
- **Action shape:** deliver the proof in the channel the deal actually uses (email lane if there are no calls), quoting the doubt back precisely. Execution hook: `generate_email` or `/octave:one-pager`.

### G8 — Precedent divergence
This deal's pattern matches how similar deals were lost, or ignores how they were won.
- **Trigger:** won/lost precedent (Step 4 pulls) in the same segment or against the same competitor shows a pattern — e.g. lost deals with this competitor all stalled at the same stage this deal now sits in; won deals all had a specific persona engaged by now.
- **Action shape:** the specific divergence-correcting move, citing the precedent ("in the last N lost deals against X, ..."). Counts are real counts from tool results, never impressions.

## 3. Evidence lanes — degrade deliberately

| Lane available | G-types in play | Note in output |
|----------------|-----------------|----------------|
| Calls + CRM (full) | All eight | — |
| CRM + emails, no calls | G2 (coarse), G3, G4 (CRM competitive intel only), G5, G6, G7 (email findings), G8 | "No call evidence; buyer-language gaps not assessed" |
| Calls only, no CRM | G1, G2 (methodology axis only), G3 (findings participants), G4, G6, G7, G8 | "No CRM; position inferred from conversations" |
| CRM only, nothing else | G3, G5, G6, G8 | "Position from CRM fields only; no voice-of-buyer evidence" |
| Nothing | none — stop | Refuse honestly (see SKILL.md error handling) |

Caller-supplied lanes (their product-usage MCP, warehouse, support tickets) plug into G5/G6 as additional observation sources when present in the conversation — use them, cite them as the caller's data.

## 4. Ranking and the cap

Score each fired gap 1–3 on three factors; rank by product:

- **Impact** — does closing this gap move the deal's central obstacle? (A G4 counter in a competitive deal beats a G6 nice-to-mention.) Weight by deal size and stage: late-stage large deals amplify.
- **Confidence** — how directly does the evidence support the gap? Verbatim quote + explicit prescription = 3; inference across two weak signals = 1. Below 2, the "action" demotes to a discovery question inside another action.
- **Perishability** — does the value decay? Fresh segment intel (G6) and pre-meeting timing decay in days; a proof gap (G7) keeps. Perishable items jump the queue *only* if confidence ≥ 2.

**Cap: 3 actions. Never pad.** One action is a normal answer. Zero is an honest answer — output the position statement, "no strategy-grounded action clears the bar," and the single most valuable trigger to watch for. A rep who gets three sharp cited moves trusts the fourth run; a rep who gets seven vague ones never runs it again.

**De-dup against the previous run** (watched deals): an action already recommended and still open is *carried*, not re-derived — mark it "still open since <date>" rather than presenting it as new. New evidence strengthening a carried action updates its citation. This is what makes the sweep read as a living system instead of a stateless generator.

## 5. Action anatomy (all four parts, every time)

```
1. THE MOVE       Imperative, specific, doable today. Names a real person only if verified.
2. WHY NOW        The observation: quote + timestamp/link, stage fact, or precedent count.
3. STRATEGY SOURCE The prescription in plain language ("your playbook for CFOs in
                   Mid-Market leads with audit-cost risk") — internal deep-links allowed
                   (seller-facing asset), raw tool/entity jargon not.
4. EXECUTION HOOK  The follow-through: a drafted email (generate_email), /octave:meeting-prep,
                   /octave:battlecard-doc, a find_person shortlist, a one-pager.
```

Groundedness bar (identical to deal-coach): every name, title, quote, count, stage, amount traces to a tool result from this run. Paraphrases are labeled as paraphrases. Unverifiable → flagged or cut, never smoothed over.
