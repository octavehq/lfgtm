# Proposal — Document Structure

Structure and content spec for the proposal HTML document. Visual/CSS rules come from the shared layers (`../shared/presentation-principles.md`, `../shared/formats/html-document.md`) plus the workspace company's brand kit. This file defines what sections exist, in what order, and what earns space in each.

## What this document is (and isn't)

The proposal is a **customer-facing closing document**: the thing a champion circulates internally and an executive reads to sign off. It has one job overall: move the buyer from "interested" to "yes." Every section either advances that decision or gets cut.

It is built around six jobs, not eleven sections. The narrative spine is fixed:

> here's your problem → here's what we'd do → here's why it pays off → here's proof → here's how it goes → here's the next step.

**The lean test (persuasion version):** every line either informs the buyer's world, substantiates a claim, or de-risks the decision. Persuasive is fine, padded is not. A proposal fails the same way an account plan does: prose that restates the heading, a second sentence that repeats the first, a section that exists because the template had one. Cut it.

**Not a one-pager, not a deck.** The one-pager is the summary; the deck is for live presenting. The proposal is the comprehensive async document. But comprehensive means complete, not long. Half the length your first instinct produces is usually right.

## Section Order

Chrome is Cover + TOC. The six jobs follow. Order is fixed except for the Proof pull-up (see the pacing rule).

| # | Section | Job | Condition |
|---|---------|-----|-----------|
| 0a | Cover | chrome | Always |
| 0b | Table of Contents (sticky sidebar) | chrome | Always |
| 1 | The Bottom Line | exec summary — the one thing to remember | Always |
| 2 | The Problem We're Solving | their pain, in their words | Always |
| 3 | What We'd Do | solution scoped to them + per-persona framing | Always |
| 4 | Why It's Worth It | the business case / ROI | Always |
| 5 | Proof It Works | results from similar companies | When proof points/references exist |
| 6 | How It Goes | implementation timeline + the next step | Always |

**Stage trims the lineup** (see the Section Selection table in SKILL.md). Early-exploration proposals drop Job 4's deep ROI. Late-stage proposals lead with Jobs 4 and 6. Renewals reframe Job 1 around results achieved. Never pad a stage back to all six if the content isn't there.

**Pacing rule — never stack three prose-dominant sections.** Bottom Line + Problem + What We'd Do as three back-to-back walls of text loses the reader before the first evidence. Break the run: pull Proof (Job 5) up to directly after the Bottom Line when the front half runs text-heavy, or lean harder on visual treatments (cards, timeline, per-persona strip) in Jobs 2 and 3.

**Component fatigue rule — don't reuse one card treatment section after section.** By the third identical tile grid the reader stops seeing them. Each job earns a distinct visual treatment: Bottom Line = takeaway box; Problem = challenge blocks; What We'd Do = capability cards + per-persona strip; Why It's Worth It = business-case figures, not a tile grid; Proof = results cards + logo row; How It Goes = timeline. If two jobs would look identical, one of them is redundant — cut, don't restyle.

---

## Section Specs

### 0a. Cover

Headline (a compelling line, not just "Proposal for [Company]"), "Prepared for [Company] by [Workspace Company]", date, workspace-company logo, champion name + title if known. The target's logo may appear in the "prepared for" line; the document chrome is workspace-company branded.

- **No inside-baseball metadata on the cover.** This document goes to the customer, not to the deal desk. Do NOT show a "Stage" chip, deal-stage label, or any run/sales-process metadata. It reads like the seller forgot to take the CRM off.
- **Confidential notice is optional, and off by default.** Do not stamp "Confidential" on the cover or footer unless the operator asks. The recipient adds their own classification if their process requires it.

### 0b. Table of Contents

Clickable anchor links to the six jobs, sticky sidebar on wide screens. TOC labels match the on-page section titles (see Titles and labels below), not "Section 3."

### Titles and labels

- **Section titles are plain, standard proposal headings, not casual or clickbait phrasings.** This is a customer-facing business document. Use "Executive summary", "The problem", "What we propose", "The business case", "Proof", "Implementation". Do NOT use conversational or salesy titles like "The bottom line", "What we'd do", "Why it's worth it", "How it goes", "Proof it works". They read as a pitch, not a proposal. (The six-job names elsewhere in this file are the internal job descriptions, not the display titles.)
- **One label per heading, never a stacked eyebrow that repeats the title.** A mono eyebrow reading "01 · The bottom line" directly above an `<h2>` reading "The bottom line" is redundant. Pick one: the plain title alone is the safe default. A bare section number in the TOC is fine; do not also echo it as a worded eyebrow over the title.
- The brand's one-highlighted-word treatment still applies to the single title (highlight the key noun).

### 1. The Bottom Line

The standalone block an executive reads instead of the whole document. Assume they read only this.

- **3 short paragraphs, 2-3 sentences each — half the length your first instinct produces:**
  1. The situation + the gap (what's happening, what's at stake).
  2. What we propose, in one clear statement.
  3. The expected outcome, stated as concretely as the grounded data allows.
- Ends with one highlighted **takeaway box** — the single thing to remember.
- The takeaway box must land **above the fold** (screenshot-test the first viewport). If the paragraphs push it below, cut the paragraphs, not the box.
- No dramatic lead-in ("In today's threat landscape..."). Start with their situation.

### 2. The Problem We're Solving

Their pain, in their words — not a setup for our features. Grounded in real conversation data wherever it exists.

- **2-3 challenge areas**, each a heading + 2-3 supporting points (one line each). Not paragraphs.
- Where a call finding exists, use their actual language. A verbatim pain quote from a real call outperforms any paraphrase — pull it from `list_findings` / `get_event_detail`, attributed honestly.
- One line on **cost of inaction** — what continues to hurt if nothing changes. Quantify only with numbers they gave you or that are defensibly public; do not invent figures.
- Do NOT describe our solution here. This section is entirely their world.

### 3. What We'd Do

The solution, scoped to them, mapped to the problems above. Two components, in this order:

**a. Capability cards** — 3-6 cards, each:
- A heading (the capability, in plain terms).
- A **"Solves for:"** tag naming the specific pain from Job 2 it addresses. This tag is load-bearing — it carries the challenge mapping. Keep it.
- **One sentence** of description. Not two. The tag says what pain it solves; the sentence says what the capability does. A second sentence is where repetition creeps in — cut it.

**b. Per-persona framing strip** — the Octave-unique move. Pulled from the Motion ICP cell (`find_motion_icp`), a compact strip showing how the value frames for each member of the buying committee:
- One row per real persona in the deal (CISO, security lead, economic buyer, etc.) — only personas actually present or named, not a generic set.
- Each row: persona label + **one line** on what this means for *them* specifically ("For your security team: fewer false positives to triage, so the on-call rotation stops drowning in noise").
- 2-4 rows, hard cap. This proves we understand the committee, not just the champion. It is the single most differentiated element of the document — get it grounded and get it tight.

### 4. Why It's Worth It

The business case for *this* company. This is the section that survives forwarding to the CFO.

- Lead with the value, framed against their cost of inaction from Job 2.
- **ROI framing is tight: one sentence setup, one sentence payoff.** No trailing compound sentences stacking three benefits into one clause. "For [investment], you get [value]" — one line, not a paragraph.
- **No separate ROI section elsewhere in the doc.** ROI lives here, once. A late second "ROI Frame" repeats the math at peak reader fatigue.
- **Numbers must be grounded.** Do not fabricate dollar amounts or percentages. Use figures the buyer gave on the call, defensibly public figures, or an explicitly-labeled illustrative model with visible assumptions the buyer can edit. When in doubt, frame qualitatively against their stated pain. (Confirm the numeric approach with the operator at generation time.)
- **Competitive differentiation folds in here, only if a competitor is in the deal.** Honest, respectful, framed as a business advantage for them — not a feature checklist, not a teardown. If no competitor is in the deal, this component does not exist. Do not manufacture a "Why Us" section.
- Investment / pricing: include the pricing table here only if the operator supplied real numbers. Otherwise use a **placeholder block** (see Placeholder rule) that prompts the seller to add pricing and packaging, framed around building the case from the trial. Never invent dollar amounts to fill the space.
- Visual treatment: business-case figures or a cost-vs-cost comparison, NOT another capability-style tile grid.

### 5. Proof It Works

Results from companies like them. Often the most engaging section — when the front half runs prose-heavy, pull this up to directly after the Bottom Line.

- **2-3 results, each: company (or anonymized descriptor), the challenge, the result with a metric.** Industry/size matches prioritized.
- Customer quote only if it traces to a real proof point or reference in the library. No invented quotes.
- Logo row of recognizable customers if the library has them.
- **Side-by-side proof cards must align their internal bands.** When two result cards sit next to each other, their bands (company header, body, the numeric-metric row, the quote) must line up horizontally across cards, not float at different heights. Use CSS subgrid (parent defines the row tracks, each card spans them) or fixed-height bands. Give the cards a **parallel structure**: the same number of numeric metrics each (two is clean), so the metric row reads as one aligned strip, not two ragged ones.
- Every named company, metric, and quote must trace to a real `search_knowledge_base` / proof-point result. A plausible-sounding but fabricated case study is the fastest way to lose the deal. Omit the section rather than invent it. Prefer a real hard number; if none exists, a short honest label beats a fake precise figure.

### 6. How It Goes

De-risks the decision by showing it's achievable, then closes on one action.

- **Do NOT fabricate the rollout plan.** The phases, milestones, and timing all depend on the customer's team and environment, so the whole rollout is the seller's to build, not ours to invent. Do not generate a "Connect / Validate / Roll out" phase list, and no weeks or calendar dates. Show a single **literal prominent placeholder** ("( Add your rollout plan and timeline )", see the Placeholder rule) that hands this section back to the seller. (A visual timeline is a great format once they fill in their real plan; the generated document just gives them the honest blank.)
- Keep this section lean: the placeholder plus the closing next step. Do not pad it with a generic "what we'd need from you" list (access, a security engineer, reporting format). It reads as filler and states the obvious; cut it.
- **Closing next step: one snappy line.** Write it, then cut it to ½-⅔ length. A two-sentence CTA is a paragraph, not a call to action. State a concrete action without inventing a date ("Start with a read-only trial"); leave the specific date for the seller to fill.
- Do NOT create both an "Implementation" and a separate "Next Steps" section. One closing job, one steps treatment.

---

## Density Rules

- **Half-length is the default.** Whatever the first draft produces, the right length is usually half. This applies hardest to the Bottom Line and the ROI framing.
- **One idea per line.** Executives skim. Badges, tags, and figures do the work prose would.
- **Lead with their world.** Open every section from the customer's perspective, not ours.
- **No dramatic lead-ins.** "In today's landscape", "At its core", "The opportunity is clear" — delete and start with the content.
- **Ground every claim.** Company name, real call quotes, real proof points. Every named person, title, metric, and especially every quote must trace to a real tool result. Honest gaps beat plausible inventions. Tag anything unconfirmed with `.unconfirmed`.
- **Don't pad to look complete.** A tight 4-section proposal for an early-stage deal beats a padded 6-section one. Omit sections with no real content silently.
- **The proposal is a scaffold, so hand back the spots where the seller's own input beats ours.** This document gets the seller 80% of the way. The last 20% is deal-specific detail only they have, and where our version would genuinely be worthless: pricing, the real rollout timeline and dates, negotiated terms. At each of those spots drop a **literal, prominent placeholder** on the page, not a subtle note. It is a large centered panel (dashed accent border, tinted fill) with a mono "Your input goes here" tag, a display-size cue in parentheses like "( Add your pricing )" or "( Add your rollout timeline )", and one line saying plainly that this is theirs to set because a generated version would be noise. Never fabricate a number or a date to fill the gap, and never bury the ask in small print. The reader should not be able to miss that this is a fill-in.

## Validated Formats — Protect These

These were explicitly praised in real outputs. Do not "improve" them away.

- **"Solves for:" tags on capability cards.** The pain-mapping tag is the load-bearing element of each card.
- **Per-persona framing strip from the Motion ICP cell.** The most differentiated element — grounded, committee-aware value framing.
- **Visual implementation timeline** as a format is well-received, but only once it holds the seller's real plan. In generated output do NOT fabricate the phases or timing; hand the section back with a literal placeholder (see Job 6).
- **Proof / "What Teams Are Seeing" results format.** The most-loved section. Candidate for early placement when the front half runs text-heavy.

## Review Checklist

- [ ] Exactly six jobs (plus Cover + TOC chrome), in the fixed order — or a stage-trimmed subset, never padded back
- [ ] Section titles are standard proposal headings (Executive summary, The problem, What we propose, The business case, Proof, Implementation), not casual/salesy phrasings
- [ ] No stacked eyebrow that repeats the section title; one label per heading
- [ ] Cover carries no Stage chip or deal-process metadata; no "Confidential" stamp unless the operator asked
- [ ] Bottom Line: 3 short paragraphs, takeaway box above the fold (screenshot-tested)
- [ ] Problem section is entirely their world — no solution language, real call quotes where they exist
- [ ] Capability cards: "Solves for:" tag + exactly one sentence each
- [ ] Per-persona strip: one row per real persona in the deal, one line each, 2-4 rows, grounded in `find_motion_icp`
- [ ] ROI framing is one setup + one payoff line; no separate ROI section anywhere else
- [ ] No fabricated dollar figures or percentages; numbers trace to the buyer, public data, or a labeled model
- [ ] "Why Us" competitive content appears only if a competitor is in the deal — otherwise absent, not manufactured
- [ ] Proof: every company, metric, and quote traces to a real proof point/reference — section omitted rather than invented
- [ ] Side-by-side proof cards align their bands (metric row, quote) across cards, with a parallel metric count
- [ ] Seller-specific spots (pricing, rollout timing) use a LITERAL prominent placeholder panel with a "( Add your ___ )" cue, never fabricated numbers, dates, or a subtle note
- [ ] Implementation shows a literal placeholder for the rollout plan, with no fabricated phases, weeks, or dates; closing CTA is one line with no invented date
- [ ] Exactly ONE steps/timeline treatment in the closing job — no separate Implementation + Next Steps
- [ ] No three consecutive prose-dominant sections (pull Proof up or add visual treatment)
- [ ] No tile-grid fatigue — each job has a distinct visual treatment
- [ ] Every named person, title, prior employer, and LinkedIn URL traces to a real `find_person`/`enrich_person` result; unconfirmed tagged with `.unconfirmed`
