# Champion Deal-Room Structure

Six jobs, one section each, plus a thin masthead and a verdict banner. Each section answers a question the champion has to answer for their org when the rep is not in the room. This is a dense working document, not a landing page: information-first, scannable, in the meeting-prep battle-plan style.

**This is a working kit the champion completes, not a finished artifact.** Get the content and structure right, ground what can be grounded, and make the fill-in slots honest and visible (blank committee names, business-case inputs, the specific ask). Do not fake precision to look done.

**Density discipline.** Short sentences, one idea per line, fixed card shapes with caps. Numbers and badges do the work prose would. No paragraph over 2 sentences. The test for any line: could a champion repeat it in an internal meeting and have it move someone? If it is generic positioning, cut it.

**Layout:** story mode by default (the screen plan below, rendered with [story-mode.md](../../shared/formats/story-mode.md) and the [visual kit](../../shared/formats/visual-kit.md)). Document mode on request: sticky sidebar nav dots (one per section), collapsible `details` sections (open by default, forced open on print), card vocabulary in [html-scaffold.md](html-scaffold.md). The six jobs, their caps and the groundedness rules are the same in both.

---

## Masthead + verdict (top, not collapsible)

- Workspace-company logo left; "Prepared for [Company]" + target logo small, right; one line: "For [Champion first name], to take to the committee."
- **Verdict banner:** 2 to 3 sentences, the state of play. What is being evaluated, why now, the one-line reason it is worth the committee's time.
- **Deal-intel strip** (stat cards): Compelling event · Champion · Committee (confirmed + roles) · The case. 4 cards max.

---

## Job 1 — The case for change

**Section id:** `case-for-change`.

The narrative the champion retells. Not a deal-status recap (the champion knows the status), the articulated story engineered to **travel up the chain intact** when repeated by people who were not on the calls. The champion's core job is to make others carry this, so arm them with the exact words, not just the situation.

| Element | Content | Cap |
|---|---|---|
| The problem | What hurts today, in the champion's own language (real quote if available) | 2-3 bullets |
| Why now | The compelling event: renewal, audit, incident, mandate | 1 line, from a real trigger or the call |
| The line that travels | The single sentence the champion says to the board / up the chain, built to survive second-hand retelling | 1 line |
| The open question | What the org has to decide | 1 line |

Grounding: the call transcript and findings. No invented history.

---

## Job 2 — Positioning and value

**Section id:** `positioning-value`. **Positioning first, numbers second.** How to frame why this matters to the org, and the ROI case where it can be quantified. This section must work even when hard dollars are not groundable, that is the point of leading with positioning.

**The value drivers are offering-specific. Derive them, do not assume a fixed model.** Work out from the offering + its value props + the matched Motion which 2-3 quantities turn this into money (seats, hours or FTEs recovered, tickets deflected, incidents avoided, tools retired, a volume metric, whatever fits), then prompt the user for the ones tools cannot supply (see SKILL Step 2). Never default to a security or analyst-hours template.

**A. How to position it** (short, the frame the champion uses):
- The one-line value frame for the org, in the offering's terms.
- What it replaces, offsets, or improves, against their actual current approach.

**B. The value case** (stat cards or a small table, where quantifiable):
| Line | Content |
|---|---|
| Cost of the status quo | What the current approach costs, in the offering's own terms |
| The case for acting | What changes, quantified from the derived value drivers + user inputs |

**Honesty rule (hard):** every number is either real (from tools or a user-supplied input) or a clearly-labeled reference outcome / estimate with its basis shown inline (e.g. "[Reference]'s result, your expected direction"). Never present a reference company's number as this account's projection. If you cannot quantify, give the qualitative positioning and name the inputs that would harden it. Do not invent.

Density: ≤6 numbers total, each with a one-line basis.

---

## Job 3 — Who else to bring in  (DATA-GATED)

**Section id:** `committee`. The seats beyond the champion that must weigh in, and how to frame it for each. **The document is addressed to the champion, so the champion is never a card here.** Map everyone else. **Two tiers, visibly separate. Do not blur them.**

**Tier 1 — Confirmed (from your deal), other than the champion.** People who appear in real deal signals: a call participant, a CRM opp contact, an email thread. Only these are named as being on the deal. Omit this tier (and its label) if there are none, which is common early.

| Element | Content |
|---|---|
| Role badge + name | Seat + real name/title, from the deal signal |
| Position | Not on the page. The committee reads this room, so a stance tag (supporter, neutral, skeptic) beside a name goes in the rep's delivery message only ([rule 22](../../shared/information-principles.md#reading-calls-and-deals)) |
| What they need | The framing for this person, from their Motion ICP cell |

**Tier 2, roles to loop in.** The seats that decide a deal like this, from the ICP / personas (`persona` entity type, see [entity-model.md](../../shared/entity-model.md)). Shown as roles, **name left blank for the champion to fill.**

| Element | Content |
|---|---|
| Role badge | The seat, whichever the ICP says decides a deal like this (e.g. finance, IT, security, procurement, legal, ops) |
| What they'll care about | Their dominant concern, in their language |
| The line that lands | The framing for that seat, from its Motion ICP cell, backed by Job 2 |
| Suggested contact | OPTIONAL: a `find_person` result listed in the delivery message to the rep, marked "you confirm". It stays off the page, where the seat keeps its blank name. |

Cap: any confirmed stakeholders other than the champion (often none early) + up to 4 roles to loop in.

**Groundedness (hard):** a `find_person` result is a suggestion, never a confirmed stakeholder. When in doubt, it is a role, not a name. The champion knows their org better than the tools do, blanks are honest and useful.

---

## Job 4 — Objection handling

**Section id:** `objections`. Q→A cards: the pushback the committee will raise, answered so the champion is never caught flat.

| Element | Content | Cap |
|---|---|---|
| The question | In the skeptical colleague's voice | ≤4 Q→A |
| The answer | Tight, concrete, with a proof anchor where possible | ≤3 lines each |

Grounding: real call objections first, then library objection entities linked to the cell. One Q→A handles the named competitor using real differentiation, not a teardown. No manufactured objections. Each card names the concern in the committee's terms, never who coached it to us or which prep call it came from (rule 22).

---

## Job 5 — Proof and references

**Section id:** `proof`. Reference cards that de-risk the decision.

| Element | Content | Cap |
|---|---|---|
| Company | Reference name (logo if available) | ≤3 cards |
| Outcome | The result as a number or concrete before→after | 1 line |
| Quote | One line, attributed | ≤2 lines |

Grounding: `reference` and `proof_point` entities (see [entity-model.md](../../shared/entity-model.md)) plus any reference named on the call, used only as its record states it: a figure or story the seller told that the record doesn't support stays out ([rule 21](../../shared/information-principles.md#reading-calls-and-deals)). Prefer same-industry and similar-size. Real metrics and quotes only. This also lowers the champion's personal risk, so lead with the most relevant.

---

## Job 6 — The path forward

**Section id:** `path`. The route to a decision, plus the cost of waiting.

**A. The steps** (game-plan timeline):
| Step | Content | Cap |
|---|---|---|
| Each step | Who does what, by when, to reach a decision, starting with a low-risk first step | ≤5 steps, 1 line each |

**B. Cost of waiting** (1-2 lines): what each month of the status quo costs, tied to the real compelling event.

Set the steps by the deal's setting ([Reading Calls and Deals](../../shared/information-principles.md#reading-calls-and-deals)): sale size, which meetings have happened and the stage today. The steps follow the champion's internal path: what they forward, who they show next, what security and procurement will ask later. After a first enterprise meeting, no step asks the buyer for their data, transcripts or a pilot; a hands-on step waits until a sponsor and an agreement exist. Lead with the lowest-risk move that stage supports. A cheap, reversible first move protects the champion and is the easiest internal yes.

---

## Screen plan (story mode)

Seven screens, one job each; the masthead becomes the bar and the verdict opens. Every number keeps its basis on the screen that shows it.

| Screen | Job | Idea | Component | Surface |
|---|---|---|---|---|
| 1 | Verdict | The state of play in one sentence, prepared for the champion | `.vk-tiles` when the case is a share of a known set, else the lede alone | dark |
| 2 | Job 2, the number | The one value figure, with its basis and estimate label | `.vk-stat` | light |
| 3 | Job 1 | The case for change: the problem in their words and the line that travels | `.vk-quote` for the buyer's words, the travelling line as the headline | dark |
| 4 | Job 2, positioning | What it replaces, today against with | `.vk-split` | light |
| 5 | Job 3 | Who else to bring in: the seats around the decision | `.vk-orbit` with the seats as nodes; blank names stay blank in the list beside it | dark |
| 6 | Jobs 4 and 5 | Objections answered and the proof behind the answers | `.vk-quotes` (question, answer, proof anchor) or `.vk-stat-row` for reference outcomes | light |
| 7 | Job 6 | The path forward: steps, where the decision stands, cost of waiting, the first move | `.vk-gantt` or `.vk-stages` with the buyer's own decision steps (never CRM stage names) and the condition that moves to the next one | dark |

The budget is five to eight screens. Six screens merge 3 into 1 when the case has no quotable buyer words, and five also merge 4 into 2; eight add a second proof screen when there are three reference cards. The compelling event, champion and committee count from the intel strip move into the bar title and screen 1's kicker.

## Density ledger

| Section | Hard cap |
|---|---|
| Masthead + verdict | 2 logos, verdict 3 sentences, 4 stat cards |
| 1 Case for change | 3 bullets + 2 lines |
| 2 Positioning and value | position frame + ≤6 numbers, each with a basis |
| 3 Committee | confirmed (as many as real) + ≤4 roles to loop in |
| 4 Objections | ≤4 Q→A |
| 5 Proof | ≤3 cards |
| 6 Path | ≤5 steps + cost-of-waiting |

## Groundedness + honesty checklist (verify before the gate)

- [ ] Champion is a real, confirmed person.
- [ ] Committee Tier 1 names ONLY people from real deal signals (call / CRM / email). No `find_person` guess asserted as a confirmed stakeholder.
- [ ] Tier 2 roles have blank names on the page. A `find_person` suggestion goes in the delivery message to the rep, marked "you confirm", never on the page (rule 22).
- [ ] Every value number is real or a labeled reference outcome / estimate with its basis inline. No reference company's number shown as this account's projection.
- [ ] Every objection traces to a real call moment or a library objection entity.
- [ ] Every proof metric/quote traces to a real entity.
- [ ] Every capability, security, data-handling or results statement traces to a product, proof point or reference record; one heard only on a call is dropped or sent to the rep as a question (rule 21).
- [ ] No internal source shows on the page: no coaching provenance ("anticipating the room", who briefed us), no seller-side call labels or dates, no CRM amounts or deal notes (rule 22).
- [ ] No stakeholder is quoted beyond what the source data supports.
- [ ] No personal fact (health, family, personal life) from a call or CRM note appears anywhere; the count left out goes in the delivery message to the rep, not in the document.
- [ ] The path forward matches the stage: no data, transcript or pilot ask after a first enterprise meeting.
- [ ] A concern that praises the offering's reach is framed in Job 2 as scope, and becomes a Job 4 objection only when it carries a condition that could stop the purchase.
- [ ] No section reads as generic positioning. Each carries a fact a champion could repeat to move someone.
- [ ] Fill-in slots (blank names, missing inputs, the specific ask) are visible and honest, not faked.
- [ ] Each proof card answers the metric the buyer asked about, or says it measures something adjacent ([information principles](../../shared/information-principles.md#claims-against-the-data) rule 27).

## Value and completion

Apply [the account value model](task-method.md#account-value-model): normalize units/periods, include cost/adoption/realization, avoid double counting, and distinguish capacity from cash. Cost of delay is conditional on a valid account model; qualitative urgency is valid. Incorporate worksheet answers and revalidate. This document crosses into the buyer’s organization; seller-internal strategy and private third-party proof stay outside it.
