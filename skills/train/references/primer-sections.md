# Onboarding GTM Primer — Structure (gated slide lesson)

Structure and content spec for the primer. The primer is **not a scrollable document**: it is a **gated, interactive slide lesson**. A new rep moves through it one topic at a time, and each topic ends with checkpoint questions they must answer before the Next button unlocks. This forces engagement, which is the point of onboarding. Once completed, a review menu lets them jump back to any topic, so it doubles as a reference.

Visual/CSS rules come from the shared layers (`../shared/presentation-principles.md`, `../shared/formats/slide-deck.md`) plus the workspace company's brand kit. This file defines what slides exist, in what order, what earns space in each, the interaction model, and the review checklist. The HTML/CSS/JS scaffold is in [html-scaffold.md](html-scaffold.md).

## What this is (and isn't)

The primer is the **one lesson a new rep completes on day one to learn how the company sells**. It is **workspace-level and evergreen**: no target account, no deal. It teaches the library's own GTM. When the library changes, the primer is re-generated, not hand-edited.

It is built around **five teaching topics**, plus a cover and a completion slide. The spine is fixed:

> what we sell and why it matters, who buys it, how to talk to each buyer, who we compete with and how we win, the proof, then a score.

**The lesson test:** every slide teaches something a rep must know, and every checkpoint is answerable from the slide it sits on. A primer fails if a slide is thin enough to skim (a real rep would not be onboarded by it) or if a checkpoint tests trivia the slide never taught. When in doubt, add substance, not slides.

**Density is richer than a scannable doc.** Because the rep is walking through the lesson slide by slide (not skimming a page), each slide carries more than a density-capped document section would. Aim for a slide that fills roughly one to one-and-a-half screens of real teaching content, then the checkpoints.

## Interaction model (the gate)

- One **topic per slide**. The rep advances with a Next button.
- Each content slide ends with **checkpoints** (multiple choice). **Next stays disabled until every checkpoint on that slide is answered.**
- Answering reveals correct/wrong plus a one-line explanation, and advancing is always allowed once answered (must-answer, not must-be-correct, so nobody gets stuck). Score is first-attempt correctness.
- A **progress dots** row (one per topic) shows position; the rep can click back to any completed topic. Forward is gated.
- The **completion slide** shows the total score and a **review menu** to jump into any topic.
- All client-side JS, no backend, no persistence, self-contained. Keyboard arrows navigate (forward only when unlocked).

## Slide Order

| # | Slide | Type | Job | Condition |
|---|-------|------|-----|-----------|
| 0 | Cover | gradient | title + how the lesson works + Start | Always |
| 1 | What we sell | content | the product, the problem, and who comes to us | Always |
| 2 | Who we sell to | content | buying committee + segments | Always |
| 3 | How to sell to each buyer | content | per-persona positioning (tabbed) | Always |
| 4 | Who we compete with | content | competitor deep-dive (tabbed) | When competitors exist |
| 5 | Proof | content | proof by lens (tabbed) | When proof points/references exist |
| 6 | Completion | gradient | score + review menu + restart | Always |

**Omit, never fabricate.** No competitors in the library, drop Slide 4. No proof, drop Slide 5. Renumber topics and dots to match. Never invent a competitor, customer, or persona talk track to fill a slide.

**Titles are plain teaching titles:** "What we sell", "Who we sell to", "How to sell to each buyer", "Who we compete with", "Proof". Highlight one key noun per title with the brand's emphasis treatment. No dramatic or clickbait phrasings.

**No Octave inside-baseball in reader-facing copy.** Do not surface internal platform vocabulary (Motions, Motion ICP cells, Learning Loop, entities) on the slides. The reader is a rep learning to sell, not an Octave operator. Teach the buyer and the pitch; keep the plumbing invisible. (One allowed exception: naming the Resonate to Elevate to Compel methodology on Slide 3, since that is the seller's own framework.)

---

## Slide Specs

### 0. Cover (gradient)

Workspace-company logo, the title "[Company] GTM Primer", a one-line subtitle, a compact "how it works" strip (Read the topic, Clear the checkpoints, Advance), and a Start button. No target-account or deal metadata.

**The whole doc is branded to and about the workspace company** (the company whose MCP connection is active, resolved via `get_workspace_company`). This is an internal enablement doc for that company's own reps, so its logo, title, and subject are always the workspace company, never a customer or target account. Customers appear only as small named proof on Slide 5, never as the brand or subject.

### 1. What we sell

The story a rep must be able to tell, and the customers who prove it. Grounded in `get_workspace_company` (whyWeExist, positioning, whyCustomersBuy, marketDynamics) and the product entity.

- **Lead statement**, 2 to 3 sentences: what we make, the problem it solves, who it is for. Plain language. Follow with the single mantra line as a callout (the one sentence a rep repeats).
- **Customer archetype cards, 3.** The strongest addition, and what makes the slide feel real. Each card: an archetype name (e.g. "The technical founder who tried to build it himself"), **their problem** (one to two lines), **why us** (one line), and the **real customer** it is drawn from (named). Pull these from real references/proof points (`get_entity` on references). Never invent an archetype; each maps to a real customer story.
- **Why now**, 2 to 3 lines from `marketDynamics`: the market shift that makes this urgent.
- **How it works**, a 3-step strip (Structure, Ingest, Propagate, or the workspace's equivalent), one line each, written for a rep with no prior context.
- **The product in one card**: the core capability in plain terms.
- **Checkpoints, ~3.**

### 2. Who we sell to

The map: who is on the buying committee, and what companies are a fit.

- **Buying committee cards**, one per featured persona (the set chosen in Step 1). Each: persona name, a **role badge** (Champion vs Economic buyer vs User, inferred from the persona), the real title(s), and one line on who they are. A short two-line note underneath naming which personas are the champions vs the economic buyers.
- **Segment cards** (the depth to teach here): feature the core segments as uniform cards with a real one-line description of that segment's GTM reality and why they are a fit (from `get_entity` on segments). List remaining fit segments as a chip row. Do NOT tag any segment "Primary" or rank them; all featured segment cards look the same. This section teaches "what kind of company do we sell to" with real substance, not just labels.
- **Do NOT mention Motions or other internal platform vocabulary here.** (Earlier drafts had a "we run two motions" line; it is Octave inside-baseball and was cut.)
- **Checkpoints, ~3**, including one on the economic buyer and one on a real segment.

### 3. How to sell to each buyer — THE CROWN JEWEL

Per-persona positioning as an **interactive tabbed selector**, pulled live from each persona's Motion ICP cell (`find_motion_icp`). Each tab swaps a panel.

**Each persona panel, four parts:** Their world (`operatingLandscape`), What they care about (`painsAndConsequences`), Lead with this (Resonate `Value Propositions`), and a Talk track strip showing Resonate to Elevate to Compel, each stage with its objective and 1 to 2 `Talking Points` from the cell. Caps: their world <=3 lines, pains <=3, lead-with <=3, talk track = 3 stages x <=2 points.

**Every featured persona gets a fully populated panel.** If a persona has cells in several segments, use the primary segment (ready version, richest narrative) and note the segment context. If a persona genuinely has no ready ICP version, build its panel from the persona entity (their world + pains only), tag it `.unconfirmed`, and do not fabricate a talk track.

**Checkpoints: one per persona.** This slide tests that the rep knows *every* buyer, not just one. Each question checks that persona's core pain or how to sell to them, answerable from that persona's panel. So a 6-persona primer has 6 checkpoints here.

### 4. Who we compete with

A **tabbed competitor deep-dive**. One tab per major competitor (feature the direct competitors and the ones that come up most; cap ~5 to 6). Pull from `list_entities({entityType: competitor})` + `get_entity` per competitor, and `list_findings` / `get_competitive_insights` for deal mentions.

**Each competitor panel:**
- A **verdict badge**: Direct competitor / Adjacent / Build-it-yourself, etc.
- **What they are**, one neutral line.
- A **capability comparison table**: rows of capability, "them" vs "Octave" (the workspace company). 3 to 5 rows, grounded in the competitor entity's described capabilities and our stated differentiation. Do not invent feature checkmarks; each row traces to the entity description.
- **You'll hear / What to say**: the buyer's likely line and the rep's honest counter (a wedge, not a teardown).
- **Deals they came up in**: pull real opportunities where the competitor was named from `list_findings` / `get_competitive_insights`. If that data is unavailable, show a labeled pending panel rather than inventing deals.

Below the tabs, a **watchlist line** naming lesser competitors and, critically, the **honest-gap** ones: where a competitor entity says intel is thin, say exactly that ("named in deals but we lack verified intel, qualify the buyer directly") instead of inventing a wedge.

**Checkpoints, ~3**, including the sharpest direct-competitor distinction and the honest-gap behavior.

### 5. Proof

Proof organized as a **tabbed set of lenses**, so a rep can grab the right proof for the room. Tabs: **By objection** (e.g. build vs buy), **By buyer** (e.g. technical or skeptical), **By segment** (e.g. security), **By outcome** (the metrics we can promise). Pull from `list_entities` proof_point + reference, with `get_entity` for the ones featured.

- Each lens shows 2 to 4 proof cards (claim, customer if named, and the result or why-it-matters), or, for the outcome lens, a metric strip (e.g. "6 months to 3 weeks"). A proof card may appear under more than one lens (Descope is both build-vs-buy and technical-buyer); that reuse is the point.
- Side-by-side proof cards align their bands via subgrid.
- A **logo / name row** of nameable customers. **Only list companies that are confirmed customers of the workspace company** (the reference explicitly states the relationship, e.g. "is an Octave customer", or a proof point describes them as a customer). Do NOT treat every `reference` entity as a customer, some are market/company profiles or prospects, not customers. When a company's customer status is not confirmed in the data, omit it. Naming a non-customer as a customer is a groundedness failure (this is what surfaced "WorkSpan" wrongly).
- Every company, metric, and quote traces to a real proof point or reference. No invented case studies. Omit a weak lens rather than pad it.
- **Checkpoints, ~3**, each mapping a lens to a situation ("you are in a security deal with a skeptical buyer, which proof?").

### 6. Completion (gradient)

The total first-attempt score out of all checkpoints, a short message keyed to the score, a **review menu** (jump to any topic), and a Restart. On print, expand all persona/competitor/proof panels and show the checkpoint answers as a key.

---

## Density Rules

- **Teach, don't skim-bait.** Each slide must be substantive enough that a real rep is actually onboarded by it. Thin slides are the failure mode here, the opposite of the doc format.
- **One idea per line inside components.** Substance comes from more real cards, tables, and archetypes, not longer paragraphs.
- **Lead with the buyer's world** in persona panels and archetypes.
- **Ground every claim.** Real personas, competitors, customers, metrics. Honest gaps beat inventions. Tag unconfirmed with `.unconfirmed`; use labeled pending panels when live data (e.g. competitor deal mentions) is unavailable rather than fabricating.
- **No internal platform vocabulary** in reader-facing copy (Motions, ICP cells, entities, Learning Loop). Exception: the Resonate to Elevate to Compel methodology name on Slide 3.
- **Every checkpoint is answerable from its slide.** No trivia, no outside knowledge, no gotchas.

## Validated Formats — Protect These

- **The gated slide lesson** with per-slide checkpoints that unlock Next only when all are answered, a progress-dot rail, and a completion score + review menu.
- **Customer archetype cards** (problem + why-us + named customer) on Slide 1.
- **The tabbed per-persona selector** pulling each buyer's their-world / pains / lead-with / R-E-C talk track, with **one checkpoint per persona**.
- **The tabbed competitor deep-dive** (verdict badge, capability comparison table, you'll-hear/what-to-say, deals-they-came-up-in), plus the honest-gap watchlist.
- **Proof tabbed by lens** (objection / buyer / segment / outcome).

## Review Checklist

- [ ] Cover, five teaching topics (or a subset when competitors/proof are absent), completion. Fixed order.
- [ ] Gate works: Next unlocks only when all checkpoints on the slide are answered; wrong answers still advance; score is first-attempt.
- [ ] Progress dots reflect position and completion; forward is gated, back is allowed; completion shows score + review menu.
- [ ] Titles are plain teaching titles; one highlighted noun each; no eyebrow that repeats the title.
- [ ] No internal platform vocabulary in reader-facing copy (Motions, ICP cells, entities); R-E-C name allowed on Slide 3.
- [ ] Slide 1 has 3 customer archetype cards, each mapped to a real named customer, with problem + why-us.
- [ ] Slide 2 has real segment cards with substance (not just chips) and role badges on the committee; no motions line.
- [ ] Featured personas <=6; if the library had more, the rep was prompted to narrow (Step 1b).
- [ ] Slide 3: every featured persona has a full four-part panel from its ICP cell, and there is one checkpoint per persona.
- [ ] Any persona with no ready ICP version uses persona-entity data only, no fabricated talk track, tagged `.unconfirmed`.
- [ ] Slide 4: tabbed competitor deep-dive with a capability comparison table, you'll-hear/what-to-say, and a deals-came-up-in panel (real findings or a labeled pending panel, never invented deals).
- [ ] Honest-gap competitors are stated as unknown, not given an invented wedge; watchlist names the rest.
- [ ] Slide 5: proof tabbed by lens; every company, metric, and quote traces to a real proof point/reference; cards align bands.
- [ ] Every checkpoint is answerable from its own slide; no trivia or outside knowledge.
- [ ] All interactions work: tab selectors swap panels, checkpoint gating unlocks Next, review menu and restart function.
- [ ] Every persona, competitor, and proof point traces to a real tool result; unconfirmed tagged.
- [ ] No em-dashes or en-dashes anywhere (commas, periods, or "to").
