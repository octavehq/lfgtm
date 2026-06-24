---
name: meeting-prep
description: Grounded, strategic prep for a specific meeting — verified stakeholders, why-this-company intel (fit, recent news, similar customers), why-us for each persona at the table, the winning story, likely objections and competitors, and how to run the conversation as talking points and beats (not a script) — rendered as self-contained HTML. Use when user says "meeting prep", "prep me for my meeting", "prep for my call", "battle plan", or wants a coached prep for an upcoming meeting. Do NOT use for static account reference documents — use /octave:brief instead.
---

# /octave:meeting-prep - Strategic Meeting Prep

Build a grounded, strategic prep for a specific upcoming meeting, rendered as a self-contained HTML document. Unlike `/octave:brief` (a static account dossier), meeting-prep is built for the conversation in front of you: it verifies who's actually in the room, establishes why this company and why now, makes the case for the product **for each persona at the table**, frames the winning story around their business pain, anticipates the objections and competitors you'll face, and hands you talking points and beats to run the conversation — **not a word-for-word script**.

The skill reads two coaching reference files at runtime:
- `references/strategic-coach.md` — Enterprise strategic sales coaching (ideal-customer fit, ecosystem positioning, pain-led Socratic discovery)
- `references/positioning-coach.md` — Product positioning coaching based on April Dunford's methodology (the positioned narrative, competitive alternatives, feature→value→emotion)

If a user replaces these files with their own coaching frameworks, the skill adapts automatically.

**Key differentiators:**
- vs `/octave:brief` — brief is a static reference dossier; meeting-prep is a coached prep tuned to one specific conversation, with a winning story and conversation beats
- vs `/octave:research` — research outputs plain text; meeting-prep renders a styled HTML document with grounded GTM intelligence
- vs `/octave:deck` — deck is a slide presentation for the audience; meeting-prep is internal prep for the seller

## Ground everything — verify before you generate

This document goes into a live meeting. A single invented name, wrong title, or hallucinated "fact" destroys trust in the entire prep — and in the seller who walks in repeating it. **Every person, company fact, news item, metric, quote, and reference must trace to a real source: an Octave tool result or verified web research. Never invent, never guess, never "round up" a fact.**

- **People are the #1 trap.** Confirm each named stakeholder actually exists *before* putting them in the doc — resolve them (`resolve_profile_from_email`, `enrich_person`, or `find_person`) and link their real LinkedIn URL. If you cannot confirm a person, do **not** present them as fact: either omit them, or list them under a clear *"⚠ Unconfirmed — verify before the call"* flag. Never fabricate a contact, title, or "the seller you'll meet."
- **Separate internal from customer before you flag anyone.** A named "contact" or "champion" is often actually *your own* team — the deal owner / AE / SE. Internal people resolve to your company's domain (e.g. `@<your-domain>`) or show up as the CRM deal/record owner. They are the rep this prep is *for*, not a customer stakeholder to verify: name them in the header ("Prepared for"), and **never** flag a colleague with a ⚠ as if they were an unverifiable prospect — that reads as a glaring error. The CRM's synthesized "champion/primary contact" field frequently mislabels the internal rep as a customer champion; treat that field as a hypothesis to check, not a fact.
- **Company & news.** Link the company's website. Every news item carries a **date and a source link** (`deep_web_research`, `scrape_website`). No undated "recently they…" claims.
- **Proof & metrics.** Every reference, customer name, logo, quote, and metric comes from Octave (`proof_point` / `reference` entities or enrichment). No invented logos, no paraphrased quotes presented as verbatim, no made-up numbers.
- **Link cited entities to source (internal doc, so do it).** This prep is internal, so link each cited library entity (proof point, reference, persona, competitor, objection, use case, Motion ICP cell) to `https://app.octavehq.com/entity/{oId}` using the `oId` from its tool result — one click to verify. (Never put these `app.octavehq.com` links in a customer-facing asset.)
- **When in doubt, mark it.** A clearly flagged "unverified — confirm live" beats a confident fabrication every time.

## On-brand styling — internal doc, so default to YOUR brand

A meeting-prep is **internal seller collateral**, so it should look like the **sender's own brand** (your workspace's company), not the target account's. Branding an internal prep in the prospect's colors is the wrong default — the prospect's brand is for *customer-facing* assets (deck, one-pager, microsite, proposal). Don't ask whose brand for this doc; default to your own.

1. Resolve the **sender** — your workspace's own company (`get_workspace_company`) — to a `<slug>` and check for a cached kit at `~/.octave/brands/<sender-slug>/manifest.json`.
2. **If the sender's kit exists → use it by default** (no need to ask): inline its `tokens.css` (`:root` + `@font-face`) **and** `get-brand-components/assets/kit_base.css`, follow `brand-kit.md` → **Signature moves**, and reuse the real **logo** so the prep reads like the sender's own collateral.
3. **If no sender kit is cached →** offer to capture it once (`/octave:get-brand-components <your-domain>`), or fall back to a readable `--style` preset for now.
4. Respect an explicit `--style <preset>` or brand override. (A target-company kit is fine only if the user explicitly asks for it.)

> The brand kit is the strongest styling signal — when one is available, prefer it over generic `--style` presets. See the `get-brand-components` skill for the kit format, token contract, and renderer.

> **Craft it like real collateral, don't fill a template.** The output should look like the sender's brand — inline their real logo, map their tokens, vary layout to fit the occasion. The `html-scaffold.md` is a **component-pattern reference to adapt**, not a fixed stylesheet to reproduce verbatim. A reader should be able to tell at a glance whose document this is. (See `presentation-principles.md` → "Look like the brand, not like a template.")

## Optional review pass

After generating the asset, **offer** an optional review (don't force it): *"Want me to run a quick review pass over this — groundedness, layout, brand, narrative, and AI-slop?"* If yes, follow [`get-brand-components/references/asset-review.md`](../get-brand-components/references/asset-review.md): render/screenshot the output, inspect it across the dimensions (render the pixels and actually look — overflow and white-on-white only show in the render), report a short scorecard of specific located findings, then fix and re-verify. The **groundedness/verification** dimension matters most here — re-check that every named person, news item, and metric is real and sourced. Skip silently if the user declines.

## Usage

```
/octave:meeting-prep <target> [--type <meeting-type>] [--style <preset>] [--research <deep|standard|fast>]
```

## Examples

```
/octave:meeting-prep acme.com                                    # General meeting prep
/octave:meeting-prep jane@acme.com --type discovery              # Discovery call prep
/octave:meeting-prep acme.com --type demo                        # Demo prep with conversation beats
/octave:meeting-prep acme.com --type executive                   # Executive meeting, business-pain framing
/octave:meeting-prep jane@acme.com --type follow-up              # Follow-up with prior call context
/octave:meeting-prep acme.com --type qbr --style executive-dark  # QBR prep with specific style
/octave:meeting-prep "meeting with VP Sales at Acme"             # Context-based prep
```

## Meeting Types

| Type | Primary Focus |
|------|--------------|
| `discovery` | Pain-led discovery questions, why-now, fit — light on pitch |
| `demo` | Why-us per persona, conversation beats, objections/landmines |
| `follow-up` | Updated pain from prior calls, what changed, next advance |
| `executive` | Concise snapshot, the winning story, business-pain framing |
| `qbr` | Value delivered, expansion angles, references |
| `general` | Balanced across all sections (default) |

## Instructions

When the user runs `/octave:meeting-prep`:

### Step 1: Understand the Context

**1.1 Identify the target:**
- Email address -> Person-targeted prep (enrich person + company)
- Domain -> Company-targeted prep (enrich company + find key contacts)
- LinkedIn URL -> Person-targeted prep
- Meeting description -> Extract company/people from context

**1.2 Detect or ask meeting type:**

If `--type` is given, use it. Otherwise **infer first, then confirm — don't ask cold.** Do a quick deal/CRM peek (`get_deal_deep_dive` / `list_events` / `list_findings`) and let it pre-select the likely type: no prior meetings / early stage → Discovery; a demo already happened → Follow-up; an exec or economic buyer is involved / late stage → Executive; existing customer → QBR. Present your inference as the default ("Looks like a **follow-up** — 3 prior calls, last was a demo. Go with that, or pick another?"). The same peek can pre-fill attendees (from CRM contacts) and a sensible duration, so Step 1 is mostly confirmation, not interrogation. If there's no deal/CRM signal, fall back to asking:

```
What type of meeting are you prepping for?

1. Discovery — First conversation, understanding their world
2. Demo — Showing the product, proving value
3. Follow-up — Continuing a conversation, advancing the deal
4. Executive — High-level strategic conversation
5. QBR — Quarterly business review with existing customer
6. General — Balanced prep (default)

Your choice:
```

**1.3 Ask meeting duration:**

Duration drives how much to cover and how many conversation beats to plan — not a minute-by-minute timeline.

```
How long is this meeting?

1. 30 minutes
2. 45 minutes
3. 60 minutes
4. 90 minutes

Your choice:
```

**1.4 Collect user context:**

Ask if the user has any prior context to incorporate:

```
Do you have any prior context to fold in?

1. Call transcript or recording notes
2. Email thread or meeting notes
3. My own notes / talking points
4. No prior context — use Octave intel + coaching frameworks

Paste or describe (or press Enter to skip):
```

If the user provides a transcript, notes, or email thread, synthesize that context alongside Octave data — and mine it for the customer's **exact language** about their pain and goals. If they skip, proceed with Octave intel and coaching frameworks only.

**1.5 Identify attendees:**

```
Who's attending? (names, titles, emails — or "I don't know yet")
```

Whatever they give you, **verify it** in Step 2 before it lands in the doc. If attendees are unknown, build a *likely* buying committee from Octave contacts — clearly labeled as inferred, not confirmed.

**1.6 Read coaching reference files:**

Read the reference files:
- `references/strategic-coach.md` — Extract: ideal-customer fit, ecosystem/enhancement positioning, pain-led Socratic discovery
- `references/positioning-coach.md` — Extract: the positioned narrative (status quo → problem → category → why-us → proof), feature→value→emotion, competitive alternatives, category framing, language mining
- `../get-brand-components/references/presentation-principles.md` — the shared output rules (label every value, no tool jargon, confirmed vs hypothesized, links open in a new tab, themed scrollbars, **look like the brand not a template**). Mandatory for the generation step.

If the coaching files are not found, fall back to general sales coaching best practices.

### Step 2: Octave Context Gathering

The research is a layered blend: **live external web** (`deep_web_research`, `scrape_website`) + **Octave enrichment** (`enrich_company`/`qualify_company`/`find_person`) + **the Octave library** (Motions / Motion ICP cells, proof points, references, competitors, objections, use cases) + **CRM & conversation intel** (`get_deal_deep_dive`, `list_events`, `list_findings`). The mix shifts by situation — a net-new prospect leans on web + enrichment + library; an existing customer adds rich CRM/findings.

#### Research depth — default: deep

Run a **deep** research pass by default. As you start, tell the user in one line what you're doing and how to dial it down, then **proceed** (don't wait for a reply unless they ask to change it):

> "Running a **deep** research pass for [Company] — live web + market/segment intel, the full Octave library, and CRM/deal history. It's the most thorough mode and takes a few minutes. Want it faster? Say **standard** (skip the broad market scan) or **fast** (Octave + CRM only, no live web)."

| Mode | What it pulls | Live web |
|------|---------------|----------|
| **deep** (default) | All layers + broad `deep_web_research` — company news **plus segment/market trends and competitor moves** | broad (3-5 targeted queries) |
| **standard** | All layers + `deep_web_research` for recent company news + 1-2 macro themes | focused (1-2 queries) |
| **fast** | Octave library + enrichment + CRM/findings only | none |

Honor an explicit `--research <deep|standard|fast>` flag or any in-line request to switch. A clearly quick internal sync can default to standard; otherwise default deep.

**Bound it — deep is thorough, not unbounded.** Gather what the relevant layers offer, cap live web to the query budget above, then **start writing**. Once you can ground each section, generate — don't keep researching (a thorough prep that ships beats an exhaustive one that stalls). Silently skip layers with no data (a net-new prospect has no CRM/findings).

Based on the target and meeting type, use Octave MCP tools to build a complete intelligence picture. **Tell the user what you're researching and why.**

**Call as many tools as needed to build a thorough, grounded prep.** The best preps layer multiple sources — company enrichment + person verification + recent news + segment research + Motion ICP persona narratives + value props + proof points + competitive intel + conversation findings all combine into a document grounded in real data. Don't stop at one tool when several give you a stronger, better-sourced prep.

Not every tool applies to every meeting. Use judgment about which are relevant to *this specific* situation. The tables below show what's available — pick the combination that gives you the richest, most verifiable context.

**List vs Search — when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_all_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory — "show me all our competitors" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content — "get full proof point / use case details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept or question — "how do we position for healthcare?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material, uploaded assets, or source docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

---

#### 2a. Verify the people and the company (do this first)

Grounding starts here. Before anything names a person or states a "fact," confirm it:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Confirm a person exists + get LinkedIn | `resolve_profile_from_email({ email })` / `resolve_email_from_profile({ ... })` | For every named attendee — confirm identity and capture the real LinkedIn URL to link |
| Person deep-dive | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | After confirming — background, role, priorities, persona match |
| Map the buying committee | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | When attendees are unknown, or to find who else should be in the room |
| Company profile | `enrich_company({ companyDomain })` | Always — industry, size, tech stack, funding, signals |
| Company logo + domain check | `get_external_brand_logo({ domain })` | For the header, and to confirm the domain resolves to a real company |

> **Internal-vs-customer check — do this before flagging anyone.** Resolve each name. If it belongs to your own team (your company domain / the CRM deal owner / AE / SE), it is **internal**: name them in the header as the deal owner, keep them out of the customer stakeholder list, and never put a ⚠ on them. Only genuinely external, unconfirmable people get the **⚠ Unconfirmed** flag — or are left out. Do not invent a contact to fill a slot.

#### 2b. Why this company, why now (fit + live intel)

| What you need | Tool | When to use |
|---------------|------|-------------|
| ICP fit + reasons | `qualify_company({ companyDomain })` | Always — segment match, fit score, and the 3-5 fit reasons that answer "why them" |
| Person fit | `qualify_person({ person: { ... } })` | Persona match and individual fit |
| Recent news (company) | `deep_web_research({ query: "<Company> news funding launches leadership 90 days" })` | Surface dated, linkable company news — fold the *so-what* for this meeting |
| Segment/market research | `deep_web_research({ query: "<their industry/segment> trends <relevant theme>" })` | Segment-level intel: what's moving in their category that maps to our value |
| Verified site facts | `scrape_website({ url })` | Pull linkable facts from their own site / newsroom |
| Similar customers we've won | `list_entities({ entityType: "reference" })` | Pull the library's **reference customers** and pick the ones most like this account (industry, size, use case) for "companies like you chose us." Do **not** use `find_similar_companies` here — it returns lookalike *prospects*, not customers with deals. |

#### 2c. Why us, for each persona (positioning + use cases)

| What you need | Tool | When to use |
|---------------|------|-------------|
| Motions for the offering | `list_motions()` | Always — find the Motion(s) covering this offering / motion type |
| Persona × segment matrix | `list_motion_icps({ motionOId })` | See which Motion ICP cells exist; pick the cell **per persona** at the table |
| Motion ICP cell narrative | `find_motion_icp({ motionIcpOId, includeLearnings: true })` | Per-persona narrative: Target ICP overview, Operating landscape, Strategic narrative, **Pains and consequences**, **Benefits and impacts**, Methodology, References + Learning Loop learnings |
| Persona definitions | `list_entities({ entityType: "persona" })` | Why each persona type cares — priorities, language, what they're measured on |
| Value props per persona | (from `find_motion_icp` → **Benefits and impacts**) | The current source for value props is the Motion ICP cell narrative — outcomes, not features. Do **not** use `list_value_props` (deprecated; reads old playbooks). |
| Top use cases | `list_entities({ entityType: "use_case" })` | The use cases that matter most — per persona and for this company |
| Custom Motion Playbook | `list_motion_playbooks({ motionOId })` + `get_motion_playbook` | Thematic / Milestone / Account / Competitive angles layered on the Motion |

#### 2d. Proof, objections, competitors

| What you need | Tool | When to use |
|---------------|------|-------------|
| Proof points | `list_entities({ entityType: "proof_point" })` | Metrics, quotes, logos — for the winning story's proof and similar customers |
| References | `list_entities({ entityType: "reference" })` | Customer references with full details |
| Topic-matched proof | `search_knowledge_base({ query: "<industry> <use case> results", entityTypes: ["proof_point", "reference"] })` | Find proof relevant to *their* specific situation |
| Known objections | `list_entities({ entityType: "objection" })` | Likely objections + grounded counters |
| Competitors (scan) | `list_all_entities({ entityType: "competitor" })` | Who's in the landscape |
| Competitor deep-dive | `get_entity({ oId })` / `get_competitive_insights({ ... })` | Where they win, where we win, the one differentiator that matters here |

#### 2e. Deal state & conversation history (for the Snapshot)

ALWAYS try to pull deal context and findings if you have a company domain or contact emails. Use a 90-day window. If data exists, it feeds the **Snapshot**; if not, silently omit — no error message.

| What you need | Tool | When to use |
|---------------|------|-------------|
| Deal deep-dive | `get_deal_deep_dive({ ... })` / `list_deal_health({ ... })` | Stage, risk, compelling event, next milestone — feeds the Snapshot strip |
| Recent findings | `list_findings({ query: "<company or person>", startDate: "<90 days ago>" })` | What was actually said in calls: objections raised, features requested, pain confirmed, competitors mentioned |
| Deal events | `list_events({ filters: { accounts: ["<account_oId>"] } })` | Deal stage changes, meetings held, emails sent |
| Event details | `get_event_detail({ eventOId })` | Deep dive on a specific past interaction |
| Synthesized starting point | `generate_call_prep({ companyDomain })` | A quick comprehensive brief to use as a starting point (still verify its claims) |

---

**Output of this step:** Present a content outline to the user for approval before generating:

```
MEETING PREP OUTLINE: [Company/Person] — [Meeting Type]
========================================================

Target: [Company name / Person name at Company]
Meeting Type: [Discovery / Demo / Follow-up / Executive / QBR / General]
Duration: [30 / 45 / 60 / 90] minutes
Attendees: [Verified names + roles, ⚠ flag any unconfirmed]
Style: [Will be selected in Step 3]

---

SECTIONS TO INCLUDE
-------------------

1. Header — Meeting details, date, duration, verified + linked attendees
2. Snapshot — Situation + deal state + the one outcome we want (merged; no separate "deal intel")
3. Why This Company, Why Now — fit reasons, recent news (dated/linked), segment intel, similar customers
4. Stakeholders — verified people only, linked LinkedIn, deal role, what each cares about
5. Why [Product] for Each Persona — why they care + why us + top use cases, per persona at the table
6. The Winning Story — the narrative arc grounded in their business pain
7. How to Run the Conversation — talking points & beats, what to listen for, what to ask for
8. Discovery Questions — pain- and situation-led (NOT sales-process)
9. Objections & Competitors — likely objections + responses; likely competitors/alternatives + watch-outs
10. The Line — one memorable sentence

Octave Sources Used:
- Company enrichment + fit: [Company] — [segment, fit score, key reasons]
- People verified: [N confirmed / N unconfirmed]
- Recent news / segment research: [N items, dated + sourced]
- Motion ICP cells (per persona): [Persona × Segment cells pulled]
- Value props / use cases: [N]
- Proof points / references / similar customers: [N]
- Objections / competitors: [N / which]
- Deal state: [stage, compelling event] (or "new prospect — nothing on file")
- Findings: [N recent signals] (or "none found — skipped")
- User context: [Transcript / notes / none]

---

Does this look good? I can:
1. Proceed to style selection and generation
2. Add or remove sections
3. Go deeper on any area
4. Change the meeting type or emphasis
```

**Wait for user approval before proceeding.**

### Step 3: Style Selection

The prep uses the same CSS variable / style preset system as `/octave:deck`. Full preset definitions are in the deck skill's [style-presets.md](../deck/references/style-presets.md).

Preps default to readability-optimized presets. If `--style` was not provided, ask:

```
Pick a style for your meeting prep:

1. midnight-pro     — Dark navy, white text, blue accents (default)
2. paper-minimal    — Off-white, black type, editorial simplicity
3. executive-dark   — Charcoal + gold, premium boardroom aesthetic
4. soft-light       — Warm white + sage green, calm and approachable
5. swiss-modern     — White + red accent, Bauhaus minimal
6. Use my brand     — Extract from website or provide colors
7. Match my deck    — Use the same style as an existing /octave:deck

Your choice (or press Enter for default):
```

| Meeting Type | Recommended Default |
|--------------|-------------------|
| Discovery | `midnight-pro` |
| Demo | `midnight-pro` |
| Follow-up | `midnight-pro` |
| Executive | `executive-dark` |
| QBR | `executive-dark` |
| General | `midnight-pro` |

If the user selects "Use my brand," follow the brand discovery flow from the deck skill (website extraction via browser-use or WebFetch, manual fallback). If they select "Match my deck," ask for the deck file path and extract its CSS variables.

### Step 4: Generate HTML

Build a single self-contained HTML file. The prep is a scrollable reference document — not a slide deck. Natural page scroll, sticky sidebar navigation, collapsible sections, and a print-friendly layout.

#### Output Directory

```
.octave-meeting-prep/
└── <kebab-case-name>-<YYYY-MM-DD>/
    └── <name>.html
```

Example: `/octave:meeting-prep acme.com --type discovery` -> `.octave-meeting-prep/acme-discovery-2026-02-27/acme-discovery.html`

The `.octave-meeting-prep/` directory should be in `.gitignore`.

#### Meeting Type → Section Emphasis

Not all sections are equally weighted in every meeting type. The type determines emphasis:

| Meeting Type | Emphasized Sections | De-emphasized / Condensed |
|--------------|-------------------|---------------------------|
| Discovery | Why This Company, Discovery Questions, Why-Us per Persona (light) | The Winning Story (lighter), Objections (lighter) |
| Demo | Why-Us per Persona, How to Run the Conversation, Objections & Competitors | Discovery Questions (lighter) |
| Follow-up | Snapshot (updated), The Winning Story, How to Run the Conversation | Why This Company (condensed) |
| Executive | Snapshot, The Winning Story, Why This Company, The Line | Discovery Questions (fewer, strategic) |
| QBR | Snapshot, Why-Us per Persona (expansion), Objections (renewal risks) | Discovery Questions (expansion-focused) |
| General | All sections at equal weight | None |

#### Document Sections (10 total)

**1. Header**
Meeting title, generation date, meeting type badge (pill like "Discovery Prep" or "Executive Prep"), duration badge, and the attendee list — each attendee **linked to their verified LinkedIn**, with role. Company name links to their website; use the company logo if `get_external_brand_logo` returned one. Any unconfirmed attendee carries a ⚠ flag.

**2. Snapshot**
The whole situation in one place. This consolidates the opportunity summary and the deal state into a single section **so deal context is never repeated lower in the document**:
- 2-3 sentence situation: who they are, what's at stake, the play.
- A compact deal-state strip — show only the fields that are actually known, omit empties: **Stage · Compelling event · Champion · Economic buyer · Competition · Next milestone** (from `get_deal_deep_dive` / `list_deal_health` / `list_events`). For a brand-new prospect, say so and note what to uncover.
- **What we want out of this meeting** — the single, specific advance/outcome. One line. For a higher-stakes meeting, sharpen this into a 3-part **positioning directive**: *Position us as* … / *Mitigate* … (the risk or competitor to neutralize) / *Advance* … (the specific next step). Outcome-driven, never a minute-by-minute clock.

**3. Why This Company, Why Now**
Make the case that this is a real, well-fit opportunity — grounded, dated, linked:
- **Fit** — segment/ICP match and the 3-5 fit reasons (`qualify_company`). **Show the composite score *and* the breakdown**, because `qualify_company` returns sub-scores (product fit vs segment fit) and the composite can mislead: an account can be a strong *product* fit but score low because it's **out of the segment definition by size or model** (e.g. too large, or B2C). Say which it is — "out-of-segment-by-size, but strong product fit" reads very differently from "bad fit," and a marquee logo deserves the nuance. If it's a genuine strong fit, say so plainly; conviction is persuasive.
- **Why now** — the trigger or compelling event (signals from enrichment, findings, or news).
- **What's happening now** — 1-2 board-level **macro themes** for the company this year (e.g. "path to profitability", "first international expansion"), plus **2-4 recent news items, each with a date and a source link** and the *so-what* for this meeting (`deep_web_research`, `scrape_website`). Macro themes are strategic narratives a board member would care about, not product announcements.
- **Their market** — segment-level intel: what's moving in their category that maps to our value. Keep only what's relevant to the conversation.
- **Similar customers** — 2-3 of our **reference customers** that look most like them (industry, size, use case) and the outcome each saw, selected from the library's `reference` (and `proof_point`) entities. Pick by similarity to this account; don't use `find_similar_companies` (it returns lookalike prospects, not customers). Real references only — no invented logos.

**4. Stakeholders**
A card per **verified, customer-side** attendee or known contact (the internal rep / deal owner belongs in the header's "Prepared for," **not** in this list):
- Name (linked to their real LinkedIn), title, and a deal-role badge: **Economic Buyer**, **Champion**, **Evaluator**, **Influencer**, or **Blocker**.
- What they care about (persona priorities — what this role is measured on), and one note on how to engage them.
- **Unconfirmed people** get a clear ⚠ badge and a "verify before the call" note — never presented as established fact. **But run the internal-vs-customer check first:** a name that resolves to your own team (deal owner / AE / SE) is *internal* — surface it as the deal owner in the header, never as an unconfirmed customer contact. If attendees are unknown, build a *likely* committee from `find_person`, labeled as inferred.

**5. Why [Product] for Each Persona**
A multi-stakeholder meeting (e.g. an eng lead + a head of finance + a head of product) is three different buyers — **don't blur them into one pitch.** For each persona type at the table:
- **Why they care** — their world and the pains this role feels (Motion ICP *Pains and consequences*; `persona` entity).
- **Why [Product] for them** — the value framed for *that role's* outcome, not a feature list (Motion ICP *Benefits and impacts* — the current source for value props; `list_value_props` is deprecated).
- **How we make them the hero** — one line on how our positioning makes *this person* look good in their org (the one who solved the problem / freed the team). Sourced from the Motion ICP cell.
- **Don't lead with** — one thing to avoid with this persona and why (a finance lead doesn't want the developer-velocity pitch).
- **Top use cases** — the 2-3 use cases that matter most to that persona (`use_case` entities; Motion ICP Methodology).

Close with a short **Top use cases for this company** list — the use cases most relevant to *this* account across all personas.

**6. The Winning Story**
The narrative arc to carry through the meeting, grounded in *their* business pain — a story, not a script. Five beats:
1. **Their world today** — how they operate now (the status quo / real alternative, in their language where you have it).
2. **What's breaking** — the business problem and the cost of standing still.
3. **Why now** — the trigger that makes this urgent.
4. **Why [Product]** — the differentiated reason we're the answer for *their* situation (category framing + the one or two things only we do that matter here).
5. **Proof** — a similar customer and the outcome.

One tight paragraph or five short beats. This is the through-line for the whole conversation.

**7. How to Run the Conversation**
**Talking points and beats — not a scripted pitch, and not a minute-by-minute timeline.** No timed phases, no word-for-word lines. Three lanes:
- **Talking points / beats** — the 4-6 moments you want to hit, in rough order. Each is a point or idea, *not a quote*. Lead with their business pain and why-[Product] — not closing language. The seller phrases it in their own voice.
- **Listen for** — the signals, phrases, and reactions that tell you where they really are (buying signals, hesitation, the alternative they're comparing against).
- **Ask for** — the specific advance you want, framed around *their* problem and the logical next step — not your internal process.

Scale the number of beats to the meeting length (more for 60/90 min, fewer for 30). Keep the tone consultative, not salesy.

**8. Discovery Questions**
Questions that **uncover the business problem and the pain unique to their situation** — not your sales process.
- Focus on: how the work happens today and where it breaks; the cost/consequences of the status quo; the outcomes and use cases they'd want; who's involved and how the business decides (because it reveals the org, not to qualify your forecast).
- **Avoid process-forcing questions** — budget/legal/procurement timing, "what would it take to sign this week," "what do you need from billing to move forward." Buyers are allergic to them and they surface no pain. Save logistics for after value is established, and keep them out of this prep.
- 8-12 questions, grouped by theme or persona, each with a one-line note on what a good answer reveals.

**9. Objections & Competitors**
- **Likely objections** — 3-5 objections this buyer is likely to raise, each with a grounded, non-defensive response framed around their business outcome (`objection` entities + real ones from `list_findings`).
- **Competitors & alternatives** — who else is likely in the deal, **including the status-quo / do-nothing / build-in-house alternative** (Dunford's "competitive alternative" — often the real one to beat). For each: where they win, where we win, the one differentiator that matters here, and a **trap question** that exposes their weakness without naming them. Mark competition as confirmed vs speculative ("Unknown — potential: …", never "Likely: …"). Sources: `get_competitive_insights`, `competitor` entities, COMPETITIVE Motion Playbooks. For a full displacement plan, point to `/octave:battlecard`.
- **Watch-outs** — one or two landmines or traps to avoid in *this specific* conversation.

**10. The Line**
One memorable sentence that captures the strategic essence of this meeting — the thing you'd write on a sticky note before the call. It distills the whole prep into a single actionable insight.

Examples:
- "They believe the problem exists but don't believe anyone's solved it — that's your opening."
- "The VP is bought in; the Director needs proof it won't break their workflow."
- "This is a displacement deal — lead with what they lose by staying, not what they gain by switching."

#### HTML Architecture

See [html-scaffold.md](references/html-scaffold.md) for the **component-pattern reference** (snapshot strip, persona blocks, story beats, the run-the-conversation table, objection/competitor rows, status tags). Treat it as patterns to **adapt**, not a fixed stylesheet to reproduce: drive the palette, type, and logo from the brand kit so the output looks like the sender's real collateral (see the styling note above). Required chrome regardless of brand: **every link `target="_blank" rel="noopener noreferrer"`**, and **themed scrollbars** (never the bare default OS scrollbar on a dark surface).

#### Content Density Guidelines

Preps are reference documents — thorough but scannable:

| Section | Content Limit |
|---------|--------------|
| Snapshot | 2-3 sentence situation + a deal strip + 1 outcome line |
| Why This Company | 3-5 fit reasons, 2-4 dated news items, 2-3 similar customers |
| Stakeholders | 4-6 stakeholder cards max |
| Why-Us per Persona | up to 3 personas, each: why-they-care + why-us + 2-3 use cases |
| The Winning Story | 5 beats / one short paragraph |
| How to Run the Conversation | 4-6 beats, each with listen-for + ask-for |
| Discovery Questions | 8-12 questions max |
| Objections & Competitors | 3-5 objections, 2-4 competitors/alternatives, 1-2 watch-outs |
| The Line | 1 sentence |

If a section would exceed its limit, prioritize by relevance to the meeting type and trim the rest.

### Step 5: Delivery

After generating the HTML file:

1. **Open the prep** in the default browser
2. **Present a summary:**

```
MEETING PREP READY
==================

Folder: .octave-meeting-prep/<name>-<date>/
File:   .octave-meeting-prep/<name>-<date>/<name>.html
Style:  [Preset name or "Custom Brand"]
Grounding: [N people verified, N news items sourced, N unconfirmed flagged]
Sections: [List of included sections]

Navigation:
- Scroll naturally to read through sections
- Click nav dots on the right edge to jump to sections
- Click section headers to collapse/expand
- PDF (recommended): bash "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/export-pdf.sh .octave-meeting-prep/<name>-<date>/<name>.html  — or Cmd+P / Ctrl+P -> Save as PDF

---

Want me to:
1. Adjust or expand a section
2. Verify or add stakeholders
3. Go deeper on any topic (why-us per persona, the winning story, objections)
4. Change the style
5. Export as PDF (print dialog)
6. Generate a brief for this account (/octave:brief)
7. Build a competitive battlecard (/octave:battlecard)
8. Build a presentation from this (/octave:deck)
9. Done
```

## MCP Tools Used

### Verification & Enrichment
- `resolve_profile_from_email` / `resolve_email_from_profile` — Confirm a person exists and capture their LinkedIn
- `enrich_company` — Full company intelligence profile
- `enrich_person` — Full person intelligence report
- `find_person` — Find contacts at a company by title/role
- `find_company` — Find companies matching criteria
- `qualify_company` — ICP fit scoring + fit reasons for a company
- `qualify_person` — ICP fit scoring for a person
- `get_external_brand_logo` — Company logo for the header / domain check

### Live Research
- `deep_web_research` — Recent news (company-level) and segment/market research, dated and sourced
- `scrape_website` — Verified, linkable facts from the company's own site

### Library — Fetching Entities
- `list_all_entities` — Quick scan of all entities of a type (minimal fields, no pagination)
- `list_entities` — Fetch entities with full data (proof points, references, use cases, objections, personas)
- `get_entity` — Deep dive on one specific entity

### Motions
- `list_motions` — Motions for the offering / motion type
- `list_motion_playbooks` — Default + Custom Motion Playbooks under a Motion
- `get_motion_playbook` — Full Motion Playbook details
- `list_motion_icps` — Persona × segment matrix for a Motion
- `find_motion_icp` — Full per-cell (per-persona) narrative + Learning Loop learnings

### Library — Searching
- `search_knowledge_base` — Semantic search across library entities and resources
- `list_resources` / `search_resources` — Uploaded docs, URLs, Google Drive files

### Competitive
- `get_competitive_insights` — Where competitors win/lose, differentiation

### Deal Intelligence & Signals
- `get_deal_deep_dive` / `list_deal_health` — Deal state for the Snapshot
- `list_findings` — Recent conversation findings and insights
- `list_events` — Deal events (stage changes, meetings, outcomes)
- `get_event_detail` — Full details for a specific event

### Content Generation
- `generate_call_prep` — Synthesized prep brief (useful as a starting point — still verify its claims)
- `generate_content` — Generate positioning or messaging content

## Error Handling

**No user context provided:**
> No prior context provided. I'll build the prep from Octave intelligence, live research, and coaching frameworks.
>
> The prep will be strong on grounded intel and positioning. After the meeting, run this again with your notes for a sharper follow-up prep.

**Person or attendee can't be verified:**
> I couldn't confirm [name] as a real contact at [company]. Rather than guess, I've flagged them as "⚠ Unconfirmed — verify before the call" (or left them out).
>
> If you have their email or LinkedIn, share it and I'll verify and enrich them properly.

**Coaching reference files not found:**
> Coaching reference files not found in `references/`. Using general sales coaching best practices.
>
> To customize coaching frameworks, add `strategic-coach.md` and `positioning-coach.md` to the `skills/meeting-prep/references/` directory.

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> I'll build the prep from your provided context and coaching frameworks. The result will focus on the winning story, conversation beats, and discovery questions without enrichment data — and I'll flag anything I can't verify.
>
> To reconnect: check your MCP configuration or run `/octave:workspace status`

**Company Not Found:**
> I couldn't find detailed intelligence for [domain].
>
> Options:
> 1. Check the domain spelling and try again
> 2. Try a different domain or company name
> 3. Provide company details manually and I'll build the prep

**No Findings / Deal Data:**
> No conversation signals or deal record found for [company/person] in the last 90 days.
>
> The Snapshot will present this as a new prospect and flag what to uncover. The prep leans on enrichment, live research, positioning, and your provided context.

**No Matching Motion ICP Cell:**
> No Motion ICP cell matches a persona at this table directly.
>
> I'll use general positioning from the knowledge base + personas + value props combined with coaching frameworks. Consider layering a Custom Motion Playbook (Thematic / Milestone / Account / Competitive) for this angle: `/octave:library create motion-playbook`

## Related Skills

- `/octave:brief` — Static internal account dossier (reference doc, no coaching frameworks)
- `/octave:research` — Deep-dive research on a company or person
- `/octave:battlecard` — Competitive intelligence and displacement strategy
- `/octave:deck` — Full slide presentation for the audience
- `/octave:one-pager` — Customer-facing leave-behind document
- `/octave:pipeline` — Deal-level coaching and pipeline strategy
- `/octave:abm` — Account-based planning with stakeholder mapping
