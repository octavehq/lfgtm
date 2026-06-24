---
name: meeting-prep
description: Strategic meeting prep with coaching frameworks, table-format cards, and outcome-driven game plan — rendered as self-contained HTML. Use when user says "meeting prep", "battle plan", "prep me for my meeting", "prep for my call", or wants a coached game plan for an upcoming meeting. Do NOT use for account reference documents — use /octave:brief instead.
---

# /octave:meeting-prep - Strategic Meeting Prep

Build a coached, strategic meeting prep rendered as a self-contained HTML document. Unlike `/octave:brief` (a reference dossier), this skill produces a prep document — combining intelligence with coaching frameworks to generate table-format cards for pains, beliefs, objections, and themes, each with adaptive action guidance, discovery questions, and response points tied to deal-specific status.

The skill reads three reference files at runtime:
- `references/strategic-coach.md` — Enterprise strategic sales coaching (ideal-customer fit, ecosystem/enhancement positioning, pain-led Socratic discovery)
- `references/positioning-coach.md` — Product positioning coaching based on April Dunford's methodology (the positioned narrative as talking points — not scripts, competitive alternatives, feature→value→emotion)
- `../get-brand-components/references/presentation-principles.md` — the shared output-formatting rules (labeling, scannability, no tool jargon, confirmed vs hypothesized tagging). Used across all asset skills.

**Read `../get-brand-components/references/presentation-principles.md` before generating any output. Every rule in that file is mandatory.**

If a user replaces the coaching files with their own frameworks, the skill adapts automatically.

**Key differentiators:**
- vs `/octave:brief` — brief is a reference dossier; meeting-prep is a coached prep with table-cards and outcome-driven goals
- vs `/octave:research` — research outputs plain text; meeting-prep renders a styled HTML document with coaching intelligence
- vs `/octave:deck` — deck is a slide presentation for the audience; meeting-prep is internal prep for the seller

## Ground everything — verify before you generate

This prep walks into a live meeting. A single invented name, wrong title, or hallucinated "fact" destroys trust in the whole document. **Every person, company fact, news item, metric, and entity must trace to a real source — an Octave tool result or verified web research. Never invent, never guess.** This is the generation-time enforcement of the "confirmed vs hypothesized" rule in `presentation-principles.md`.

- **People are the #1 trap.** Confirm each named stakeholder exists *before* putting them in the doc — `resolve_profile_from_email`, `enrich_person`, or `find_person` — and use the **real LinkedIn URL the tool returns** (never construct one). If a person can't be confirmed, mark them Hypothesized / "Potential fit", never state them as fact.
- **Separate internal from customer.** A CRM "champion/primary contact" is often *your own* AE/SE (resolves to your domain or is the deal owner). They're who the prep is *for* — name them in the header, never flag a colleague as an unverified prospect. Treat the CRM's synthesized champion field as a hypothesis to check.
- **Link every cited library entity back to its source.** Octave entities (proof point, reference, persona, competitor, objection, use case, Motion ICP cell) carry an `oId` in every tool result. Link each one to **`https://app.octavehq.com/entity/{oId}`** — a naked deep link that resolves to the reader's own workspace and the right entity. This makes every claim one click from its source, and lets the seller verify before the call. **(meeting-prep is an internal seller doc, so these links belong here — but never put Octave links in a customer-facing asset like a deck, one-pager, or proposal.)**
- **News carries a date and a source link**; proof/metrics come from Octave; mark speculation as speculation ("Unknown — potential: …", never "Likely: …").

## Usage

```
/octave:meeting-prep <target> [--type <meeting-type>] [--style <preset>]
```

## Examples

```
/octave:meeting-prep acme.com                                    # General meeting prep
/octave:meeting-prep jane@acme.com --type discovery              # Discovery call prep
/octave:meeting-prep acme.com --type demo                        # Demo prep with talk tracks
/octave:meeting-prep acme.com --type executive                   # Executive meeting with board framing
/octave:meeting-prep jane@acme.com --type follow-up              # Follow-up with prior call context
/octave:meeting-prep acme.com --type qbr --style executive-dark  # QBR prep with specific style
/octave:meeting-prep "meeting with VP Sales at Acme"             # Context-based prep
```

## Meeting Types

| Type | Primary Focus |
|------|--------------|
| `discovery` | Discovery questions primary, belief framework, qualification |
| `demo` | Positioned pitch tailored to demo flow, demo landmines |
| `follow-up` | Updated pain from prior calls, deal advancement |
| `executive` | Concise situation summary, executive talk tracks, board-level framing |
| `qbr` | Value delivered, renewal/expansion angles |
| `general` | Balanced all sections (default) |

## Instructions

When the user runs `/octave:meeting-prep`:

### Step 1: Understand the Context

**1.1 Identify the target:**
- Email address -> Person-targeted prep (enrich person + company)
- Domain -> Company-targeted prep (enrich company + find key contacts)
- LinkedIn URL -> Person-targeted prep
- Meeting description -> Extract company/people from context

**1.2 Detect or ask meeting type:**

If `--type` not specified, infer from context or ask:

```
What type of meeting are you prepping for?

1. Discovery — First conversation, qualifying the opportunity
2. Demo — Showing the product, proving value
3. Follow-up — Continuing a conversation, advancing the deal
4. Executive — High-level strategic conversation
5. QBR — Quarterly business review with existing customer
6. General — Balanced prep (default)

Your choice:
```

**1.3 Ask meeting duration:**

The duration is displayed as context in the header — it does NOT drive a minute-by-minute timeline.

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
4. No prior context — use available intel + coaching frameworks

Your choice (or press Enter to skip):
```

If the user provides a transcript, notes, or email thread, synthesize that context alongside enrichment data. If they skip, proceed with available intelligence and coaching frameworks only.

**1.5 Identify attendees:**

```
Who's attending? (names, titles, emails — or "I don't know yet")
```

If attendees are unknown, build a general stakeholder map from available contacts.

**1.6 Read reference files:**

Read the reference files:
- `references/strategic-coach.md` — Extract: ideal-customer fit, ecosystem/enhancement positioning, pain-led Socratic discovery, belief stacking
- `references/positioning-coach.md` — Extract: the positioned narrative as **talking points/beats** (status quo → problem → category → why-us → proof, not word-for-word scripts), feature→value→emotion, competitive alternatives, category framing, language mining
- `../get-brand-components/references/presentation-principles.md` — Extract: all 12 output formatting rules. Shared across the asset skills and mandatory for the generation step.

If the coaching files are not found, fall back to general sales coaching best practices. If the presentation principles file is not found, apply the rules from the "Anti-Patterns" section below — they are embedded in these instructions as well.

### Step 2: Context Gathering

Based on the target and meeting type, use Octave MCP tools to build a complete intelligence picture. **Tell the user what you're researching and why.**

**Call as many tools as needed to build a thorough prep.** The best meeting preps layer multiple sources — company enrichment + person enrichment + playbook messaging + proof points + conversation intel + coaching frameworks all combine to create a document grounded in real data. Don't stop at one tool when several would give you a stronger prep.

Not every tool applies to every meeting. Use your judgment about which are relevant to *this specific* situation. The tables below show what's available — pick the combination that gives you the richest context for the meeting type and target.

**List vs Search — when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_all_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory — "show me all our competitors" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content — "get full proof point details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept or question — "how do we position for healthcare?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material, uploaded assets, or source docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

**Findings and events — always attempt, gracefully skip:**

ALWAYS try to pull findings and events if you have a company domain or contact emails. Use a 90-day window. If data exists, it feeds into the Situation section (deal context) and informs context card statuses. If not, silently omit — no error message.

- `list_findings({ query: "<company or contact>", startDate: "<90 days ago>" })` — surfaces what was actually said in calls: objections raised, features requested, pain points confirmed, competitor mentions
- `list_events({ filters: { accounts: ["<account_oId>"] } })` — deal stage changes, meetings held, emails sent
- `get_event_detail({ eventOId })` — deep dive on specific past interactions

---

#### For Person-Targeted Preps

Start with person and company enrichment, then pull positioning context:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Person deep-dive | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | Always for person-targeted preps — gives background, role, priorities |
| Company profile | `enrich_company({ companyDomain })` | Always — gives industry, size, tech stack, signals |
| ICP fit (person) | `qualify_person({ person: { ... } })` | When you need persona match and fit assessment |
| ICP fit (company) | `qualify_company({ companyDomain })` | When you need segment match and ICP scoring |
| Additional contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | When you want to map the broader buying committee |
| Matching Motion ICP cell | `find_motion_icp({ motionIcpOId, includeLearnings: true })` | The per-persona narrative — pains, Benefits and impacts (value), methodology, references + learnings |
| Find the right Motion / cell | `list_motions()` → `list_motion_icps({ motionOId })` | Locate the persona × segment cell that matches this person |
| Proof points | `list_entities({ entityType: "proof_point" })` | Fetch all proof points with full data — metrics, quotes, logos |
| References | `list_entities({ entityType: "reference" })` | Customer references with full details |
| Competitive context | `search_knowledge_base({ query: "<signals>", entityTypes: ["competitor"] })` | When competitor is mentioned or likely in the deal |
| Recent intel | `list_findings({ query: "<company or person>", startDate: "<90 days ago>" })` | Conversation-based insights from past interactions |
| Deal history | `list_events({ filters: { accounts: ["<account_oId>"] } })` | Timeline of deal events |
| Synthesized prep | `generate_call_prep({ companyDomain })` | Quick comprehensive brief to use as a starting point |
| Deep web research | `deep_web_research({ query: "<company name> news strategy 2026" })` | Live web intelligence for macro themes and signals — feeds "What's Happening Now" section |

---

#### For Company-Targeted Preps

Start with company enrichment and contact discovery:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Company profile | `enrich_company({ companyDomain })` | Always — gives industry, size, tech stack, funding, signals |
| ICP fit scoring | `qualify_company({ companyDomain })` | Always — segment match, fit score, fit reasons |
| Key contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | Find stakeholders to populate the People sub-section |
| Enrich contacts | `enrich_person({ person: { ... } })` | Deep dive on each key contact found |
| All Motions | `list_motions()` | Find the Motion(s) covering this offering / motion type |
| Motion ICP matrix | `list_motion_icps({ motionOId })` → `find_motion_icp({ motionIcpOId, includeLearnings: true })` | The persona × segment grid; pull the cell narrative for the buying committee |
| Motion Playbooks | `list_motion_playbooks({ motionOId })` + `get_motion_playbook` | Thematic / Milestone / Account / Competitive angles layered on the Motion |
| Value props (per persona) | from `find_motion_icp` → **Benefits and impacts** | The current source for value props — **not** the deprecated `list_value_props` |
| Similar customers | `list_entities({ entityType: "reference" })` | Reference customers most like this account — "companies like you chose us" (not `find_similar_companies`, which returns prospects) |
| All competitors | `list_all_entities({ entityType: "competitor" })` | Quick scan of competitive landscape |
| Competitor details | `get_entity({ oId })` | Deep dive on a specific relevant competitor |
| Proof points | `list_entities({ entityType: "proof_point" })` | Full proof points for the evidence section |
| References | `list_entities({ entityType: "reference" })` | Customer references for social proof |
| Topic search | `search_knowledge_base({ query: "<industry> <use case>", entityTypes: ["proof_point", "reference"] })` | Find proof points relevant to their specific situation |
| Recent intel | `list_findings({ query: "<company>", startDate: "<90 days ago>" })` | Conversation signals from calls and meetings |
| Deal events | `list_events({ filters: { accounts: ["<account_oId>"] } })` | Full deal history and timeline |
| Event details | `get_event_detail({ eventOId })` | Deep dive on specific past interactions |
| Uploaded resources | `search_resources({ query: "<company or industry>" })` | Relevant uploaded docs and assets |
| Deep web research | `deep_web_research({ query: "<company name> news strategy 2026" })` | Live web intelligence for macro themes and signals — feeds "What's Happening Now" section |

---

#### New Octave Integration Points

These additional pulls power the restructured sections:

| What you need | Tool | Powers |
|---------------|------|--------|
| Motion ICP cells | `list_motion_icps({ motionOId })` → `find_motion_icp({ motionIcpOId, includeLearnings: true })` | S1 People ("how we make them the hero"), S2 Recognition cards |
| Competitor entities | `list_entities({ entityType: "competitor" })` | S3 Competitive Position matrix |
| Messaging/positioning | `search_knowledge_base({ query: "<relevant terms>", entityTypes: ["messaging", "positioning"] })` | S2 Positioning Directive, S3 Persona message shifts |
| Per-persona value | `find_motion_icp` → **Benefits and impacts** | S3 Persona use case hooks (not the deprecated `list_value_props`) |
| Objection entities | `list_entities({ entityType: "objection" })` | S4 Objection cards with theme grouping + persona tags |

**Conditional richness:** These pulls enrich the prep when data exists. When data is thin:
- Persona message shifts: show only personas with strong data, omit thin ones
- Competitive position: if no competitor entities, keep single Competition row in Deal Context and note "No confirmed competitors"
- Objection entities: if none in library, synthesize from deal context and coaching frameworks

---

**Output of this step:** Present a content outline to the user for approval before generating:

```
MEETING PREP OUTLINE: [Company/Person] — [Meeting Type]
========================================================

Target: [Company name / Person name at Company]
Meeting Type: [Discovery / Demo / Follow-up / Executive / QBR / General]
Duration: [30 / 45 / 60 / 90] minutes
Attendees: [Names and roles, or "Roles to find"]
Style: [Will be selected in Step 3]

---

SECTIONS
--------

Header — "Meeting Prep: [Company]", meeting type badge, duration badge, expand/collapse toggle, one-sentence context
Deal Snapshot Bar — Deal Value | Stage | Target Close | Primary Contact

1. Context
   - Company context (card group: logo, grid with what they do, scale, fit reasoning, signals, angle)
   - People (card group: persona groups with "how we make them the hero" + ICP cell data)
   - Deal context (card group: grid with stage, activity, competition, champion, compelling event, buying triggers)

2. Goals
   - Positioning directive (structured: position us as / mitigate / advance)
   - What we need them to recognize (card group: [N] table-cards with context, status, planting guidance, "watch out" row, discovery questions)

3. What to Say & Ask
   - How our message lands by persona (tabbed: pressure, story shift, hook line, use case, "don't lead with")
   - Competitive position (card group: [N] table-cards with their positioning, our counter, trap question)
   - Pains we know they have (card group: [N] table-cards with context, status, probe guidance, "watch out" row, discovery questions)
   - Themes to steer (card group: [N] table-cards with relevance, status, steering guidance)

4. Objections
   - Theme tabs (Status Quo & Inertia, Technical & Integration, Competitive, etc.)
   - [N] objection table-cards with persona tags, "you'll hear", response, "watch out"

5. The Takeaway
   - One sentence

Intelligence Sources:
- Company: [key insights]
- Person: [persona match]
- Playbook: [strategic angle]
- Proof points: [N] pulled
- Recent signals: [N] found (or "none — skipped")
- Competitive: [if applicable]
- User context: [transcript / notes / none]

---

Does this look good? I can:
1. Proceed to style selection and generation
2. Add or remove sub-sections
3. Go deeper on any area
4. Change the meeting type or emphasis
```

**Wait for user approval before proceeding.**

### Step 3: Style Selection

**Brand kit check (do this first).** Before asking about style presets, check if a brand kit exists for the target company at `~/.octave/brands/<slug>/`. If a kit exists (has `manifest.json` and `tokens.css`), use it automatically:

1. Read `tokens.css` and `manifest.json` to populate the `:root` variables using the token mapping table below.
2. **MANDATORY: Add the brand header and brand footer.** Read the brand kit's logo SVG file (`<slug>-logo.svg` or similar), inline it into the `<header class="brand-header">` and `<footer class="brand-footer">` templates documented in the "Brand Header & Footer" section below. This is NOT optional — every brand-kit-styled document MUST have the branded header and footer.
3. Tell the user: "Found brand kit for [Company] — applying their design system."
4. Skip the style preset menu.

If no brand kit exists, the prep uses the same CSS variable / style preset system as `/octave:deck`. Full preset definitions are in the deck skill's [STYLE_PRESETS.md](../deck/STYLE_PRESETS.md).

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

If the user selects "Use my brand," check for an existing brand kit first (`~/.octave/brands/<slug>/`). If none exists, offer to run `/octave:get-brand-components <domain>` to build one, or fall back to the brand discovery flow from the deck skill. If they select "Match my deck," ask for the deck file path and extract its CSS variables.

### Step 4: Generate HTML

**Before generating, re-read `../get-brand-components/references/presentation-principles.md` and apply every rule.**

Build a single self-contained HTML file. The prep is a scrollable reference document — not a slide deck. Natural page scroll, sticky sidebar navigation, collapsible sections, and a print-friendly layout.

#### Output Directory

```
.octave-meeting-prep/
└── <kebab-case-name>-<YYYY-MM-DD>/
    └── <name>.html
```

Example: `/octave:meeting-prep acme.com --type discovery` -> `.octave-meeting-prep/acme-discovery-2026-02-27/acme-discovery.html`

The `.octave-meeting-prep/` directory should be in `.gitignore`.

#### Meeting Type -> Section Emphasis

Not all sub-sections are equally weighted in every meeting type. The type determines emphasis:

| Meeting Type | Emphasized | De-emphasized / Condensed |
|--------------|-----------|---------------------------|
| Discovery | Pains (Sec 3) + Recognition cards (Sec 2), Positioning Directive | Competitive Position, Objections (Sec 4) lighter |
| Demo | Persona Message Shifts (Sec 3), Objections (Sec 4), People | Recognition cards (fewer), Deal Context |
| Follow-up | Pains (updated statuses), Competitive Position, Deal Context | People (condensed), Persona Shifts (condensed) |
| Executive | Company Context, Positioning Directive, The Takeaway | Card groups (fewer, high-level only) |
| QBR | Deal Context, Positioning Directive, Pains (expansion-focused) | Persona Shifts, Objections (condensed) |
| General | All at equal weight | None |


#### Document structure (overview)

The prep is a **Header + a labeled Snapshot bar + 5 sections**, rendered with a table-card design system (scannable card titles → label/value grids → status tags → nested discovery questions), a three-level collapsible hierarchy (sections + card-groups open, individual cards closed), tabs for persona/objection switching, and an optional brand header/footer.

1. **Context** — company context (logo + "What's Happening Now" macro themes/signals), people (persona-first, with "how we make them the hero"), deal context (+ deal timeline that flags activity gaps).
2. **Goals** — positioning directive (Position us as / Mitigate / Advance) + what we need them to recognize (belief cards).
3. **What to Say & Ask** — how our message lands by persona (tabbed), competitive position (with trap questions), pains we know they have, themes to steer.
4. **Objections** — theme-tabbed objection cards (descriptive title + "you'll hear" + response + watch-out), persona-tagged.
5. **The Takeaway** — one sentence.

**The full per-section content spec, the design system, the status-tag vocabulary, and the complete self-contained HTML + CSS scaffold live in [`references/html-architecture.md`](references/html-architecture.md). Read it before generating — it is the rendering source of truth.** Per-section content limits are in "Content Density Guidelines" below; meeting-type emphasis is in the table above.

#### Content Density Guidelines

The prep should be thorough but scannable. These limits keep sections focused:

| Sub-section | Content Limit |
|-------------|--------------|
| Company Context | 5-7 grid rows |
| What's Happening Now | 1-2 macro themes + 3-5 signals (deep research only) |
| People (persona groups) | One group per relevant persona |
| Deal Context | 5-7 grid rows |
| Deal Timeline | 3-6 milestones (event data only) |
| Positioning Directive | 3 rows (Position / Mitigate / Advance) |
| What We Need Them to Recognize | 3-4 table-cards |
| How Our Message Lands by Persona | One tab per persona in the room |
| Competitive Position | 2-4 table-cards |
| Pains We Know They Have | 3-4 table-cards |
| Themes to Steer | 2-3 table-cards |
| Objections (Sec 4) | 6-8 table-cards across all themes |
| The Takeaway | 1 sentence |

If a sub-section would exceed its limit, prioritize by relevance to the meeting type and trim the rest.

### Anti-Patterns: NEVER Do These in Output

These are real problems observed in generated output. Every one is a hard rule violation.

**Unlabeled data:**
- BAD: A subtitle showing "$500K / Technical Evaluation / Q2 2026" — three values, no labels
- GOOD: A snapshot bar with "Deal Value: $500K | Stage: Technical Evaluation | Target Close: Q2 2026"

**Tool terminology leaking into output:**
- BAD: "Sources: Octave enrichment v2, qualification engine, ask_graph"
- BAD: "Stream B Intelligence" as a section header
- BAD: "Powered by Octave" in the footer
- GOOD: No mention of tools, engines, versions, or streams. The output reads as analyst-written.

**Repeating data across sections:**
- BAD: Deal value in the subtitle AND in a snapshot bar AND in the deal context section
- GOOD: Deal value appears once in the snapshot bar. Other sections reference it if needed but don't restate it.

**Sections that don't earn their keep:**
- BAD: An empty "Prior Intelligence" section that says "No findings in last 90 days"
- BAD: A "Meeting Game Plan" that's just a generic timeline unrelated to the actual goals
- GOOD: If no data exists for a sub-section, omit it silently. Every visible section has real content.

**Walls of text:**
- BAD: A "Coach's Corner" section with two 200-word paragraphs
- GOOD: Coaching intelligence woven into table-card rows — specific, in-context, and actionable

**Generic advice:**
- BAD: "Build rapport early in the call" / "Ask thoughtful questions" / "Don't give a generic pitch"
- GOOD: "Lead with the Datadog displacement angle — they're mid-contract renewal and evaluating alternatives" (specific to this deal)

**Process-driven meeting goals:**
- BAD: "Phase 1 (0-5 min): Rapport building. Phase 2 (5-20 min): Discovery..."
- GOOD: Positioning Directive with "Position us as / Mitigate / Advance" — structured, specific, grounded in the deal

**Quoted objections:**
- BAD: Objection title as a quote in the prospect's voice: `"We already use Glean for this"`
- GOOD: Objection title as a descriptive risk statement: `They position this as overlap with existing enterprise search`
- BAD: `"We could build this ourselves"`
- GOOD: `Their engineering team defaults to building internally`
- The objection should describe the situation or risk, never put words in the prospect's mouth.

**Speculative competition stated as fact:**
- BAD: "Likely: Glean, internal build" — using "Likely" implies we have partial evidence when we have none
- GOOD: "Unknown — Potential: internal build, Glean" — clearly marks this as speculation
- BAD: "Competition: Datadog" when no intel confirms Datadog is in the deal
- GOOD: "Competition: Datadog" ONLY when we have confirmed intel (mentioned in call, CRM data, etc.)
- Always distinguish confirmed facts from speculation in every field, not just competition.

**Separate sections for related content:**
- BAD: Pains in Section 1, beliefs in Section 2, questions about those pains in Section 3, talk tracks about those beliefs in Section 3
- GOOD: Each pain/belief is a self-contained table-card with its own rows and discovery questions

**Scripted talk tracks:**
- BAD: "Say these exact words: 'Most teams today handle...'" — sellers don't read scripts
- GOOD: Response points, talking points, and framing guidance that the seller adapts to their style

**Minute-by-minute timelines:**
- BAD: "Phase 1 (0-5 min): Rapport. Phase 2 (5-20 min): Discovery..."
- GOOD: Exit criteria that define what success looks like, not a process to follow

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
Duration: [30 / 45 / 60 / 90] min

Sections:
1. Context — company context (with logo), people (with hero framing), deal context (with buying triggers)
2. Goals — positioning directive, what we need them to recognize (with watch-out guidance)
3. What to Say & Ask — persona message shifts (tabbed), competitive position, pains we know they have, themes to steer
4. Objections — theme-tabbed objection cards with persona tags, "you'll hear" + response + watch-out
5. The Takeaway — one sentence

Navigation:
- Scroll naturally through sections
- Click nav dots on the right edge to jump between sections
- Click section headers to collapse/expand sections
- Click card group headers to collapse/expand groups
- Click individual card titles to expand details (closed by default)
- Use "Expand all / Collapse all" toggle in the header
- Print-friendly: Cmd+P / Ctrl+P for clean PDF output (auto-expands all)

---

Want me to:
1. Adjust or expand a section
2. Add/remove people or cards
3. Go deeper on a specific pain, belief, or objection
4. Change the style
5. Regenerate for a different meeting type
6. Export as PDF (print dialog)
7. Generate a brief for this account (/octave:brief)
8. Build a presentation from this (/octave:deck)
9. Done
```

## MCP Tools Used

### Research & Enrichment
- `enrich_company` — Full company intelligence profile
- `enrich_person` — Full person intelligence report
- `find_person` — Find contacts at a company by title/role
- `find_company` — Find companies matching criteria
- `qualify_company` — ICP fit scoring for a company
- `qualify_person` — ICP fit scoring for a person

### Brand Assets
- `get_external_brand_logo` — Fetch company logo URL for the company identity block

### Library — Fetching Entities
- `list_all_entities` — Quick scan of all entities of a type (minimal fields, no pagination)
- `list_entities` — Fetch entities with full data and pagination (proof points, references, etc.)
- `get_entity` — Deep dive on one specific entity
- `list_motions` — Motions for the offering / motion type
- `list_motion_icps` — Persona × segment matrix for a Motion
- `find_motion_icp` — Full per-persona cell narrative (pains, Benefits and impacts = value props, methodology) + learnings
- `list_motion_playbooks` / `get_motion_playbook` — Default + Custom Motion Playbooks
- `resolve_profile_from_email` / `resolve_email_from_profile` — Confirm a person exists + capture their real LinkedIn

### Library — Searching
- `search_knowledge_base` — Semantic search across library entities and resources
- `list_resources` — Browse uploaded docs, URLs, and Google Drive files
- `search_resources` — Semantic search across uploaded resources

### Intelligence & Signals
- `list_findings` — Recent conversation findings and insights
- `list_events` — Deal events (stage changes, meetings, outcomes)
- `get_event_detail` — Full details for a specific event

### Content Generation
- `generate_call_prep` — Synthesized prep brief (useful as a starting point)
- `generate_content` — Generate positioning or messaging content
- `deep_web_research` — Live web intelligence for macro themes, news, and signals (powers "What's Happening Now" section)

## Error Handling

**No user context provided:**
> No prior context provided. I'll build the prep from available intelligence and coaching frameworks.
>
> The prep will be strong on strategy and positioning. After the meeting, run this again with your notes for a grounded follow-up prep.

**Coaching reference files not found:**
> Coaching reference files not found in `references/`. Using general sales coaching best practices.
>
> To customize coaching frameworks, add `strategic-coach.md` and `positioning-coach.md` to the `skills/meeting-prep/references/` directory.

**Connection Failed:**
> Could not connect to your workspace.
>
> I'll build the prep from your provided context and coaching frameworks. The result will focus on table-cards, discovery questions, and goals without enrichment data.
>
> To reconnect: check your MCP configuration or run `/octave:workspace status`

**Company Not Found:**
> I couldn't find detailed intelligence for [domain].
>
> Options:
> 1. Check the domain spelling and try again
> 2. Try a different domain or company name
> 3. Provide company details manually and I'll build the prep

**No Findings Data:**
> No conversation signals found for [company/person] in the last 90 days.
>
> Skipping prior intelligence. The prep will focus on enrichment data, coaching frameworks, and your provided context.

**Attendees Not Specified:**
> No specific attendees provided. I'll build a general stakeholder map from available contacts and apply coaching frameworks broadly.
>
> Tip: Adding attendee names and roles before the meeting makes the table-cards and action guidance much sharper.

**No Matching Motion ICP cell:**
> No Motion ICP cell matches a persona at this table directly.
>
> I'll use general positioning from the knowledge base + personas + value props (from Motion ICP Benefits and impacts), combined with coaching frameworks. Consider layering a Custom Motion Playbook (Thematic / Milestone / Account / Competitive): `/octave:library create motion-playbook`

**Logo Not Found:**
> No logo found for [company]. The company identity block will display the company name without a logo image.

## Related Skills

- `/octave:brief` — Internal account dossier (reference doc without coaching frameworks)
- `/octave:research` — Deep-dive research on a company or person
- `/octave:deck` — Full slide presentation for the audience
- `/octave:one-pager` — Customer-facing leave-behind document
- `/octave:battlecard` — Competitive intelligence and displacement strategy
- `/octave:pipeline` — Deal-level coaching and pipeline strategy
- `/octave:abm` — Account-based planning with stakeholder mapping
