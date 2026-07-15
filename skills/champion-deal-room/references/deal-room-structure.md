# Champion Deal-Room Structure

Six jobs, one section each, plus a thin masthead and a verdict banner. Each section answers a question the champion has to answer for their org when the rep is not in the room. This is a dense working document, not a landing page: information-first, scannable, in the meeting-prep battle-plan style.

**This is a working kit the champion completes, not a finished artifact.** Get the content and structure right, ground what can be grounded, and make the fill-in slots honest and visible (blank committee names, business-case inputs, the specific ask). Do not fake precision to look done.

**Density discipline.** Short sentences, one idea per line, fixed card shapes with caps. Numbers, badges, and status dots do the work prose would. No paragraph over 2 sentences. The test for any line: could a champion repeat it in an internal meeting and have it move someone? If it is generic positioning, cut it.

**Layout:** sticky sidebar nav dots (one per section), collapsible `details` sections (open by default, forced open on print). Card vocabulary in [html-scaffold.md](html-scaffold.md).

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
| Position | Champion / supporter / neutral / skeptic (status dot), only if the signal supports it |
| What they need | The framing for this person, from their Motion ICP cell |

**Tier 2, roles to loop in.** The seats that decide a deal like this, from the ICP / personas (`persona` entity type, see [entity-model.md](../../shared/entity-model.md)). Shown as roles, **name left blank for the champion to fill.**

| Element | Content |
|---|---|
| Role badge | The seat, whichever the ICP says decides a deal like this (e.g. finance, IT, security, procurement, legal, ops) |
| What they'll care about | Their dominant concern, in their language |
| The line that lands | The framing for that seat, from its Motion ICP cell, backed by Job 2 |
| Suggested contact | OPTIONAL: a `find_person` result marked "possible, you confirm" (a `.suggested` tag). Never asserted as on the deal. |

Cap: any confirmed stakeholders other than the champion (often none early) + up to 4 roles to loop in.

**Groundedness (hard):** a `find_person` result is a suggestion, never a confirmed stakeholder. When in doubt, it is a role, not a name. The champion knows their org better than the tools do, blanks are honest and useful.

---

## Job 4 — Objection handling

**Section id:** `objections`. Q→A cards: the pushback the committee will raise, answered so the champion is never caught flat.

| Element | Content | Cap |
|---|---|---|
| The question | In the skeptical colleague's voice | ≤4 Q→A |
| The answer | Tight, concrete, with a proof anchor where possible | ≤3 lines each |

Grounding: real call objections first, then library objection entities linked to the cell. One Q→A handles the named competitor using real differentiation, not a teardown. No manufactured objections.

---

## Job 5 — Proof and references

**Section id:** `proof`. Reference cards that de-risk the decision.

| Element | Content | Cap |
|---|---|---|
| Company | Reference name (logo if available) | ≤3 cards |
| Outcome | The result as a number or concrete before→after | 1 line |
| Quote | One line, attributed | ≤2 lines |

Grounding: `reference` and `proof_point` entities (see [entity-model.md](../../shared/entity-model.md)) plus any reference named on the call. Prefer same-industry and similar-size. Real metrics and quotes only. This also lowers the champion's personal risk, so lead with the most relevant.

---

## Job 6 — The path forward

**Section id:** `path`. The route to a decision, plus the cost of waiting.

**A. The steps** (game-plan timeline):
| Step | Content | Cap |
|---|---|---|
| Each step | Who does what, by when, to reach a decision, starting with a low-risk first step | ≤5 steps, 1 line each |

**B. Cost of waiting** (1-2 lines): what each month of the status quo costs, tied to the real compelling event.

Lead with the lowest-risk next step (e.g. a read-only assessment). A cheap, reversible first move protects the champion and is the easiest internal yes.

---

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
- [ ] Tier 2 roles have blank names (or `find_person` suggestions clearly tagged "possible, you confirm").
- [ ] Every value number is real or a labeled reference outcome / estimate with its basis inline. No reference company's number shown as this account's projection.
- [ ] Every objection traces to a real call moment or a library objection entity.
- [ ] Every proof metric/quote traces to a real entity.
- [ ] No stakeholder is quoted beyond what the source data supports.
- [ ] No section reads as generic positioning. Each carries a fact a champion could repeat to move someone.
- [ ] Fill-in slots (blank names, missing inputs, the specific ask) are visible and honest, not faked.
