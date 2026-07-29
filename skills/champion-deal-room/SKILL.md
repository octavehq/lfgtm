---
name: champion-deal-room
description: A dense internal deal room a rep hands to a champion so they can run the buying-committee sell without you in the room. Quantified business case, stakeholder map with per-seat ammo, objection handling, and a path to yes, rendered as self-contained HTML. Use when user says "champion deal room", "arm my champion", "help my champion sell internally", "internal business case for [deal]", or wants a champion enablement doc. For a customer-facing top-of-funnel page use /octave:microsite; for the formal closing proposal use /octave:proposal.
---

# /octave:champion-deal-room - Champion Deal Room

Generate a dense, self-contained HTML deal room that a rep hands to an internal champion so the champion can run the buying-committee sell without the rep in the room.

**The mental model:** your champion believes, but they now have to convince a CFO, an IT lead, an auditor, and a security engineer who were not on your calls. This is the working document they run that sell from. It is not a pitch and it is not pretty for its own sake. It is facts and ammunition: the number, the map of who must say yes, the exact thing each person needs to hear, the answers to the hard questions, and the path to signature.

**This is a working document, not a landing page.** Dense, scannable, information-first, in the meeting-prep battle-plan style (collapsible sections, sidebar nav, real card vocabulary). The champion opens it to prepare for an internal meeting and to forward pieces to colleagues. Every section must carry a fact, not a talking point.

**How this differs from other skills:**
- vs `/octave:microsite` — that is a customer-facing, top-of-funnel attention grabber for a cold reader. This is an internal, mid-to-late-deal working kit for a reader who already believes.
- vs `/octave:proposal` — proposal is the polished vendor document addressed to the buyer's execs, the formal closing artifact. This is the champion's candid internal kit organized around the committee and the path to consensus, the thing that gets a deal to the point where a proposal lands.
- vs `/octave:abm` — abm is the rep's account plan (how the rep pursues the account). This is written for the champion, in service of the champion's internal sell.
- vs `/octave:meeting-prep` — meeting-prep coaches your rep for one meeting. This coaches the champion for the meetings you are not in.

## The six jobs

Six jobs, one section each. Nothing else earns a place. Each answers a question the champion has to answer for their org when you are not in the room.

1. **The case for change** — the problem in their words, why now, and the one-line version that survives being repeated by people who were not on the calls. The champion carries this up the chain, so engineer it to travel: give them the sentence they say to the board, not just a situation recap. A short verdict up top so a busy reader gets the state of play in five seconds.
2. **Positioning and value** — how to frame the value for the org, with the ROI case where it can be quantified. Reframe value as positioning first, numbers second: the section must work even when hard dollars are not groundable. The numbers come from the offering's *own* value drivers (derive them, never assume a fixed model), and you prompt the user for the 2-3 inputs that quantify them (see Step 2). Where you do quantify, show the arithmetic and label estimates.
3. **Who else to bring in (the committee)** — the seats *beyond the champion* that must weigh in, and how to frame it for each. The champion is the reader, not a card here. **Data-gated (see below):** real names only for people who appear in real deal signals; everyone else is a role to loop in, not an asserted stakeholder.
4. **Objection handling** — the pushback the committee will raise, including the competitive comparison, each answered with a proof anchor.
5. **Proof and references** — the evidence, scaled to their size and industry, that de-risks the decision.
6. **The path forward** — the low-risk next step, the cost of waiting, and the route to a decision.

**The champion is sticking their neck out.** Proof (Job 5), a low-risk first step, and "you can start small" (Job 6) are not just content, they lower the champion's personal risk of backing something that could flop. Weave that through, do not make it a section.

## Groundedness is non-negotiable

Never synthesize a person or a LinkedIn slug. Real objections, pains, and quotes come from actual events (`get_event_detail`) or library entities, never invented.

**The document is addressed to the champion, so the champion is never a card in this section.** Map everyone else. Do not tell the reader who the reader is.

**The committee is data-gated. `find_person` returning a CFO does not make them the CFO on this deal.** Two tiers, and do not blur them:
- **Confirmed stakeholders (other than the champion)** — people who appear in real deal signals (a call participant, a CRM opp contact, an email thread). Only these get named as being on the deal. Omit this tier if there are none.
- **Roles to loop in** — the seats that decide a deal like this (from the ICP / personas), shown as roles with what each cares about and the framing that lands, names left blank for the champion to fill. You MAY attach a `find_person` result as a clearly-marked suggestion ("possible, you confirm"), never as an asserted committee member.

Presenting a `find_person` guess as a confirmed stakeholder is the exact fabrication mode to avoid. When in doubt, it is a role to loop in, not a name.

**The business case (Job 2) must be honest.** Where you have real numbers (headcount, seat/license counts, tools in the stack, a stated deal size, a user-supplied input), use them. Where you derive a figure by scaling from a reference proof point, state the assumption in the doc and label it an estimate. A clearly-labeled estimate is fair; a fabricated precise number is not. Honest gaps ("no finance stakeholder identified yet") beat plausible inventions. Tag anything unconfirmed with `.unconfirmed`. A prior showcase run shipped a fabricated committee, do not repeat it.

## On-brand styling — brand kit first, then generate

Follow the canonical flow in [brand-kit-usage.md](../shared/brand-kit-usage.md). Summary for this skill below; that doc is the source of truth for kit lookup and extraction tiers.

**Resolve the brand before generating (do not skip this step).** The deal room is styled with the **workspace company's brand** (the Octave customer whose workspace you are operating in) because it is your asset that your champion carries. The target account is centered in the content (their people, their pains, their numbers), and their logo appears once in a "prepared for [Company]" masthead, not in the chrome.

**Step 1: Identify the workspace company.** Call `get_workspace_company` for the company name, domain/URL, and positioning.

**Step 2: Resolve the workspace company's brand kit.** Slugify the workspace company name and check `~/.octave/brands/<slug>/manifest.json`. If a complete kit exists (has `manifest.json` and `tokens.css`), use it automatically:
   - inline the kit's `tokens.css` (`:root` + embedded `@font-face`) **and** `../get-brand-components/assets/kit_base.css` into the output `<style>`;
   - follow the kit's `brand-kit.md` → **Signature moves**, and reuse the kit's real **logo**, `images/`, and `icons.json`.
   **If no complete kit exists → build one.** Read and follow the `get-brand-components` SKILL.md for the workspace company's domain. Retry up to 3 times with variations (root domain, `www.`, `/about`) before falling back to a preset.

**Step 3: Generic preset is a last resort** — presets in [../shared/style-presets.md](../shared/style-presets.md).

## Principles

Follow these standards during generation. Read each before producing output.

**Content and language:**
- [Editorial rules](../shared/editorial-rules.md) — no AI-isms, banned vocabulary, honest analyst tone
- [Information principles](../shared/information-principles.md) — lead with conclusions, evidence-backed claims, narrative arc

**Presentation:**
- [Presentation principles](../shared/presentation-principles.md) — universal visual rules, spacing, restraint
- [HTML document format](../shared/formats/html-document.md) — scrollable-document visual rules, this is a dense document in the meeting-prep battle-plan style, not a landing page

**Octave data:**
- [Octave value](../shared/octave-value.md) — prioritize grounded workspace data over generic AI content
- [Octave research toolkit](../shared/octave-research-toolkit.md): tool selection (list vs search), grounding follow-up assets in real events and findings, standard error handling
- [Entity model](../shared/entity-model.md): canonical entity types and oId prefixes for personas, proof points, references, and competitors pulled into the committee and proof sections

**Brand:**
- [Brand kit usage](../shared/brand-kit-usage.md): canonical brand-kit lookup flow (this skill wears the workspace company's brand, per Section 1 of that doc)

Apply these during generation, not just at review. After generating, the **review pipeline is a mandatory gate** (Step 5), the deal room is not opened or delivered until the scorecard is produced.

## Usage

```
/octave:champion-deal-room <target> [--champion <name|email>] [--deal-size <amount>]
```

`<target>` is the account (domain, name, or a person email). If `--champion` is not given, infer the champion from the most engaged real contact on the account and confirm before generating.

## Examples

```
/octave:champion-deal-room acme.com
/octave:champion-deal-room acme.com --champion jane@acme.com
/octave:champion-deal-room acme.com --deal-size 180000
```

## Instructions

### Step 1: Identify the account and the champion

Parse the target. If a name without a domain, `find_company({ name })`.

**Identify the champion by asking, not guessing.** The champion is the spine of the whole document, so ask the user directly, do not infer silently:

```
Who is your champion at [Company]? (name or email) — the person who already
believes and has to sell this internally. The whole deal room is written to them.
```

- Use `--champion` if it was passed.
- Once the user names them, confirm and enrich with `resolve_profile_from_email` / `enrich_person` / `find_person`, and frame the entire document around that person in second person ("you", "your CFO").
- Only if the user cannot name one, offer to suggest the most engaged real contact (`list_events` positive-sentiment call participant / CRM champion) as a candidate for them to confirm, or point to `/octave:microsite` (cold) or `/octave:abm` (rep-side plan).

State the confirmed champion and title back before proceeding.

### Step 2: Octave context gathering

Gather grounding for all six jobs. Tell the user what you are researching and why. Follow [octave-research-toolkit.md](../shared/octave-research-toolkit.md) for tool selection (list vs search), grounding in real events and findings, and the standard error responses if a call comes back empty.

**Situation + fit (Job 1):**
```
enrich_company({ companyDomain })
qualify_company({ companyDomain, additionalContext: "Matched segment, Motion ICP cell, and fit signals." })
list_events({ filters: { companyDomains: ["<domain>"], eventCategories: ["CALL"] }, includeParticipants: true, startDate: "<365 days ago>" })
get_event_detail({ eventOId: "<call>", includeFullContent: true })
list_findings({ query: "<company or contact> pain points and compelling event", startDate: "<365 days ago>" })
```
Mine the transcript and findings for the compelling event, what was established, the pains in the champion's own words, the competitor named, the reference that resonated, and the agreed next step.

**The business case (Job 2) — the substance, and the one place you prompt the user for numbers.**

The value drivers are specific to the offering, so **derive them, never assume a fixed model** (do not default to a security/analyst-hours template). From the offering, its value props, and the matched Motion, work out the 2-3 quantities that turn this into money for *this* product. Examples of what that looks like across offerings, pick what fits, do not use all:
- seats / licenses / users, or headcount in the affected function
- hours or FTEs recovered, tickets or cases deflected, incidents avoided
- tools retired or spend consolidated
- a volume metric that scales the ROI (throughput, transactions, endpoints, whatever the offering acts on)

Assemble what tools give you (size/headcount via `enrich_company`; current tools via named competitors/alternatives; stated deal size via `--deal-size`/CRM), then **prompt the user for the derived inputs you cannot get from tools:**
```
To put a real number on the case for [offering], I need a few inputs:
[the 2-3 you derived, e.g. contract size, current spend on what this replaces,
and <the offering's volume driver>]. Skip any you don't have and I'll fall back
to labeled reference outcomes.
```
Combine tool data + user inputs to quantify cost-of-status-quo and the case-for-acting. Scale from a reference proof point only where needed, and label those figures as estimates with the basis shown. If the user skips the inputs, degrade to labeled reference outcomes and state that the dollar case hardens once they add them.

Pull the proof points and references that carry real metrics:
```
find_motion_icp({ motionIcpOId: "<champion persona x segment>", includeElements: true })
get_entity({ oId: "<proof_point / reference oId>" })
```

**The committee (Job 3) — DATA-GATED, GROUNDEDNESS-CRITICAL:**
```
# Confirmed stakeholders: who actually appears in deal signals
list_events(...) / get_event_detail(...)   # call participants
find_crm_records / find_crm_activities     # CRM opp contacts, if a real opp resolves
# Roles to loop in: the seats that decide a deal like this
list_entities({ entityType: "persona" })
find_motion_icp({ motionIcpOId: "<seat persona x segment>" })   # framing per seat
# OPTIONAL suggestion only (never asserted as on the deal):
find_person({ searchMode: "people", companyDomain, fuzzyTitles: ["<titles>"], limit: 5 })
```
`persona` is the entity type for these seats (see [entity-model.md](../shared/entity-model.md) for the full canonical type list and oId prefixes, e.g. `pe_` for persona, `pp_` for proof point, `re_` for reference, `cp_` for competitor). Confirmed stakeholders (call/CRM/email) get named. Every other seat is a role to loop in with framing from its Motion ICP cell, name blank, optionally a `find_person` suggestion marked "possible, you confirm." The champion's own cell's Compel-stage methodology usually contains an explicit champion-enablement line (how to frame value for IT vs finance vs privacy vs engineering). Use it.

**Objections + competitive (Job 4):**
```
list_findings({ query: "objections and pushback raised by prospects", eventFilters: { companyDomains: ["<domain>"] } })
```
Real call objections (from findings and transcripts) plus the library objection entities linked to the cell; the competitor's differentiation from the cell for the competitive one.

**Path to yes (Job 6):** the agreed next step from the call plus the Compel-stage sequence. Frame the cost of waiting from the real compelling event (a renewal date, an audit, an incident).

### Step 3: Resolve the brand kit

Per the **On-brand styling** section. Resolve or build silently. Do not present a brand menu.

### Step 4: Generate the deal-room HTML

**Load the shared rules and specs. Read each before producing output:**
- [Editorial rules](../shared/editorial-rules.md)
- [Information principles](../shared/information-principles.md)
- [Presentation principles](../shared/presentation-principles.md)
- [HTML document format](../shared/formats/html-document.md)
- [Octave value](../shared/octave-value.md)
- [Deal-room structure](references/deal-room-structure.md) — the six jobs, per-section specs, density rules, business-case quantification, groundedness rule
- [HTML scaffold](references/html-scaffold.md) — the locked CSS + section skeleton + card vocabulary; reproduce this structure

Build a single, self-contained HTML file. No external dependencies beyond Google Fonts.

#### Output Directory
```
.octave-deal-rooms/
└── <company-slug>-<YYYY-MM-DD>/
    └── deal-room.html
```
Write under the user's home directory.

**After writing the file, proceed immediately to Step 5 (Review Pipeline). Do NOT open the file or present it yet.**

### Step 5: Review Pipeline — MANDATORY GATE

**Do NOT open the deal room, present the delivery summary, or tell the user it is ready until the review pipeline has completed and you have a scorecard.**

Load the [review protocol](../shared/protocol.md) and execute the review loop against the generated file.

**5a: Mechanical lint:**
```bash
bash <skill-dir>/../shared/scripts/lint.sh <path-to-deal-room.html>
```
Fix every violation.

**5b: Spawn two reviewers in parallel** (both Task calls in one message):

**Editorial reviewer:**
```
Task tool:
  subagent_type: "octave-editorial-reviewer"
  prompt: "Review the file at [FILE PATH].
           Read these principle docs and run each Review Checklist:
           1. [skill-dir]/../shared/editorial-rules.md
           2. [skill-dir]/../shared/information-principles.md
           3. [skill-dir]/references/deal-room-structure.md (density + groundedness + business-case honesty)
           This is a champion's internal working kit: every section must carry a fact, not a
           talking point. Verify the business case shows its arithmetic and labels estimates,
           no stakeholder is quoted beyond source data, and no section is generic positioning.
           Fix violations inline. Return scorecard."
```

**Presentation reviewer:**
```
Task tool:
  subagent_type: "octave-presentation-reviewer"
  prompt: "Review the file at [FILE PATH].
           Read these docs and run each Review Checklist:
           1. [skill-dir]/../shared/presentation-principles.md
           2. [skill-dir]/../shared/formats/html-document.md
           3. [skill-dir]/references/html-scaffold.md
           4. [skill-dir]/references/deal-room-structure.md
           This is a dense working document (battle-plan style), not a landing page. Verify the
           sidebar nav, collapsible sections, stakeholder cards, and business-case stat cards
           render, that it prints cleanly (all sections open), and that it holds up at 900px and
           on mobile.
           Fix violations inline. Return scorecard."
```

**5c: Loop decision.** Read both scorecards:

| Cycle | 0 fixes | 1-2 fixes | 3+ fixes |
|---|---|---|---|
| Cycle 1 | CLEAN → 5d | Apply, loop | Apply, loop |
| Cycle 2 | CLEAN → 5d | Apply, STOP | Apply, loop |
| Cycle 3 (cap) | CLEAN → 5d | Apply, STOP | Apply, STOP |

Max 3 cycles. Re-run both reviewers each loop.

**5d: Output combined scorecard.** Proof the pipeline ran. Step 6 cannot start without it.
```
REVIEW PIPELINE COMPLETE
=========================
Editorial:      [N fixes / PASS]
Presentation:   [N fixes / PASS]
Total fixes: [N]
Cycles: [1-3]
Status: [CLEAN / N remaining issues]
```

### Step 6: Delivery

After the scorecard:
1. Open the deal room in the browser.
2. Present a summary:
```
CHAMPION DEAL ROOM READY
========================
Folder:    .octave-deal-rooms/<company>-<date>/
File:      .octave-deal-rooms/<company>-<date>/deal-room.html
Account:   [Company]
Champion:  [Name, title] (confirmed via [source])
Committee: [N seats mapped / gaps]
Business case: [headline number, e.g. "~$Xk consolidation + ~Y analyst hours/yr"]
Style:     [Brand kit name]

Want me to:
1. Sharpen the business-case math or assumptions
2. Add or remove a committee seat
3. Draft the note to the champion that carries this link (/octave:generate)
4. Done
```

## MCP Tools Used

### Champion + committee (groundedness-critical)
- `resolve_profile_from_email` / `enrich_person` / `find_person` / `qualify_person`

### Account, situation, and business case
- `find_company`, `enrich_company`, `qualify_company`
- `list_events`, `get_event_detail` - real discovery, objections, compelling event
- `list_findings` - what was actually said in calls: pains, objections, competitor mentions, in the champion's own words
- `get_entity` - proof points and references with real metrics for the business case
- `list_entities({ entityType: "persona" })` - the seats to loop in; see [entity-model.md](../shared/entity-model.md) for entity types and oId prefixes

### Per-seat framing and competitive
- `list_motions`, `list_motion_icps`, `find_motion_icp` - per-cell narrative + champion-enablement framing + linked elements

### Brand
- `get_workspace_company` - see [brand-kit-usage.md](../shared/brand-kit-usage.md) for the full kit-lookup flow

## Error Handling

**No champion identified:**
> A deal room needs a champion, a real person who believes and must sell internally. I couldn't find an engaged contact at [target].
> Options: 1) name them (`--champion <email>`), 2) `/octave:microsite` (cold), 3) `/octave:abm` (rep-side account plan).

**Thin business case:**
> I can map the committee and the story, but I don't have enough to quantify the business case with real numbers (no seat counts, stack, or deal size).
> Options: 1) give me the deal size / their current tools and I'll build the math, 2) proceed with clearly-labeled estimates scaled from references, 3) drop Job 2 to a qualitative case (weaker).

**No Motion ICP cell for a seat:**
> No cell matches one of the committee seats. I'll frame it from workspace positioning and the real concern raised on the call, tagged `.unconfirmed`.

## Related Skills

- `/octave:microsite` - Customer-facing top-of-funnel page (cold reader)
- `/octave:proposal` - Formal vendor business case for the buyer's execs (this precedes it)
- `/octave:abm` - Rep-side account plan for the whole pursuit
- `/octave:meeting-prep` - Coach your own rep for a scheduled meeting
- `/octave:generate` - Draft the note to the champion that carries the link
