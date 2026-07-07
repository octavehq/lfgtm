---
name: meeting-prep
description: Grounded, strategic prep for a specific meeting — verified stakeholders, why-this-company intel (fit, recent news, similar customers), why-us for each persona at the table, the winning story, likely objections and competitors, and how to run the conversation as talking points and beats (not a script) — rendered as self-contained HTML. Use when user says "meeting prep", "prep me for my meeting", "prep for my call", "battle plan", or wants a coached prep for an upcoming meeting. Do NOT use for static account reference documents — use /octave:brief instead.
argument-hint: "<company-or-email> [--type <meeting-type>] [--style <preset>] [--research <deep|standard|fast>] [--skip-review]"
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

A meeting-prep is **internal seller collateral**, so it should look like the **sender's own brand** (your workspace's company), not the target account's — don't ask whose brand. Resolve the sender with `get_workspace_company` and follow the kit lookup and defaults in [../shared/brand-kit-usage.md](../shared/brand-kit-usage.md). Respect an explicit `--style` or brand override.

> **Craft it like real collateral, don't fill a template.** The output should look like the sender's brand — inline their real logo, map their tokens, vary layout to fit the occasion. The `html-scaffold.md` is a **component-pattern reference to adapt**, not a fixed stylesheet to reproduce verbatim. A reader should be able to tell at a glance whose document this is. (See [../shared/presentation-principles.md](../shared/presentation-principles.md) → "Look like the brand, not like a template.")

## Review pass (runs by default)

Run the default review pass after generating — the always-on preflight plus the visual render-and-inspect pass, per [../shared/review-pass.md](../shared/review-pass.md). Opt out with `--skip-review`; the visual pass defaults off in a `--research fast` run.

## Usage

```
/octave:meeting-prep <target> [--type <meeting-type>] [--style <preset>] [--research <deep|standard|fast>] [--skip-review]
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
- [`../shared/presentation-principles.md`](../shared/presentation-principles.md) — the shared output rules (label every value, no tool jargon, confirmed vs hypothesized, links open in a new tab, themed scrollbars, **look like the brand not a template**). Mandatory for the generation step.

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

**Call as many tools as needed to build a thorough, grounded prep.** The best preps layer multiple sources — company enrichment + person verification + recent news + segment research + Motion ICP persona narratives + value props + proof points + competitive intel + conversation findings all combine into a document grounded in real data. Not every tool applies to every meeting; pick the combination that gives you the richest, most verifiable context:

- **List-vs-search guidance and the common tool tables:** [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md).
- **The prep's ordered tool tables** — 2a verify people/company first, 2b why-this-company/why-now, 2c why-us per persona, 2d proof/objections/competitors, 2e deal state & conversation history (always attempt with a 90-day window; silently omit if empty) — plus the internal-vs-customer check: [references/tool-reference.md](references/tool-reference.md).

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

The prep uses the same CSS variable / style preset system as the other document skills. Full preset definitions are in [../shared/style-presets.md](../shared/style-presets.md).

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

If the user selects "Use my brand," follow the brand extraction tiers in [../shared/brand-kit-usage.md](../shared/brand-kit-usage.md). If they select "Match my deck," ask for the deck file path and extract its CSS variables.

### Step 4: Generate HTML

Build a single self-contained HTML file. The prep is a scrollable reference document — not a slide deck. Natural page scroll, sticky sidebar navigation, collapsible sections, and a print-friendly layout.

#### Output Directory

```
.octave-meeting-prep/
└── <kebab-case-name>-<YYYY-MM-DD>/
    └── <name>.html
```

Example: `/octave:meeting-prep acme.com --type discovery` -> `.octave-meeting-prep/acme-discovery-2026-02-27/acme-discovery.html`

Make sure `.octave-meeting-prep/` is ignored by your project's `.gitignore` (an `.octave-*/` pattern covers all Octave output dirs) so generated preps don't get committed.

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

The full specification for each section — Header, Snapshot, Why This Company/Why Now, Stakeholders, Why-[Product]-per-Persona, The Winning Story, How to Run the Conversation, Discovery Questions, Objections & Competitors, and The Line — is in [references/prep-sections.md](references/prep-sections.md). Read it before generating; it carries the grounding rules per section (verified people only, dated/linked news, real references, confirmed-vs-speculative competition).

#### HTML Architecture

Build on the shared scaffold in [../shared/doc-scaffold.md](../shared/doc-scaffold.md); prep-specific components (snapshot strip, persona blocks, story beats, the run-the-conversation beats, objection/competitor rows, status tags) are in [html-scaffold.md](references/html-scaffold.md). Treat them as patterns to **adapt**, not a fixed stylesheet: drive the palette, type, and logo from the brand kit so the output looks like the sender's real collateral. Required chrome regardless of brand: **every link `target="_blank" rel="noopener noreferrer"`**, and **themed scrollbars** (never the bare default OS scrollbar on a dark surface).

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

Common research, library, signals, and generation tools: see [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md). Meeting-prep-specific additions:

### Verification & Live Research
- `resolve_profile_from_email` / `resolve_email_from_profile` — Confirm a person exists and capture their LinkedIn
- `deep_web_research` — Recent news (company-level) and segment/market research, dated and sourced
- `scrape_website` — Verified, linkable facts from the company's own site
- `get_external_brand_logo` — Company logo for the header / domain check
- `get_workspace_company` — Resolve the sender's own company for brand styling

### Competitive & Deal Intelligence
- `get_competitive_insights` — Where competitors win/lose, differentiation
- `get_deal_deep_dive` / `list_deal_health` — Deal state for the Snapshot

## Error Handling

Standard responses (company not found, no matching Motion ICP cell): see [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md) → Standard error handling. Meeting-prep-specific:

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

**No Findings / Deal Data:**
> No conversation signals or deal record found for [company/person] in the last 90 days.
>
> The Snapshot will present this as a new prospect and flag what to uncover. The prep leans on enrichment, live research, positioning, and your provided context.

## Related Skills

- `/octave:brief` — Static internal account dossier (reference doc, no coaching frameworks)
- `/octave:research` — Deep-dive research on a company or person
- `/octave:battlecard` — Competitive intelligence and displacement strategy
- `/octave:deck` — Full slide presentation for the audience
- `/octave:one-pager` — Customer-facing leave-behind document
- `/octave:pipeline` — Deal-level coaching and pipeline strategy
- `/octave:abm` — Account-based planning with stakeholder mapping
