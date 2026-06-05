---
name: meeting-prep
description: Strategic meeting prep with coaching frameworks, table-format cards, and outcome-driven game plan — rendered as self-contained HTML. Use when user says "meeting prep", "battle plan", "prep me for my meeting", "prep for my call", or wants a coached game plan for an upcoming meeting. Do NOT use for account reference documents — use /octave:brief instead.
---

# /octave:meeting-prep - Strategic Meeting Prep

Build a coached, strategic meeting prep rendered as a self-contained HTML document. Unlike `/octave:brief` (a reference dossier), this skill produces a prep document — combining intelligence with coaching frameworks to generate table-format cards for pains, beliefs, objections, and themes, each with adaptive action guidance, discovery questions, and response points tied to deal-specific status.

The skill reads three reference files at runtime:
- `references/strategic-coach.md` — Enterprise strategic sales coaching (belief stacking, ecosystem positioning, Socratic discovery)
- `references/positioning-coach.md` — Product positioning coaching based on April Dunford's methodology (positioned sales pitch, competitive alternatives, feature-value-emotion ladder)
- `references/presentation-principles.md` — Output formatting rules (labeling, scannability, no tool jargon, confirmed vs hypothesized tagging)

**Read `references/presentation-principles.md` before generating any output. Every rule in that file is mandatory.**

If a user replaces the coaching files with their own frameworks, the skill adapts automatically.

**Key differentiators:**
- vs `/octave:brief` — brief is a reference dossier; meeting-prep is a coached prep with table-cards and outcome-driven goals
- vs `/octave:research` — research outputs plain text; meeting-prep renders a styled HTML document with coaching intelligence
- vs `/octave:deck` — deck is a slide presentation for the audience; meeting-prep is internal prep for the seller

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

Read the three reference files from the skill directory:
- `references/strategic-coach.md` — Extract: belief stacking, ecosystem positioning, enhancement framing, ideal customer fit, guardrail reframe, Socratic discovery
- `references/positioning-coach.md` — Extract: positioned sales pitch (5 steps), feature->value->emotion, competitive alternatives, category framing, language mining, heads on pillows test
- `references/presentation-principles.md` — Extract: all 12 output formatting rules. These are mandatory for the generation step.

If the coaching files are not found, fall back to general sales coaching best practices. If the presentation principles file is not found, apply the rules from memory — they are embedded in these instructions as well.

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
| Matching playbook | `get_playbook({ oId, includeValueProps: true })` | After identifying relevant playbook — full strategy + value props |
| Playbook search | `search_knowledge_base({ query: "<industry> <persona>", entityTypes: ["playbook"] })` | When you need the best-fit playbook by concept |
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
| All playbooks | `list_all_entities({ entityType: "playbook" })` | Quick scan to find the right strategic approach |
| Playbook details | `get_playbook({ oId, includeValueProps: true })` | Full content + value props for the matching playbook |
| Value props | `list_value_props({ playbookOId })` | Value propositions for the recommended playbook |
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
| ICP cells | `list_entities({ entityType: "icp" })` or `list_motion_icps()` | S1 People ("how we make them the hero"), S2 Recognition cards |
| Competitor entities | `list_entities({ entityType: "competitor" })` | S3 Competitive Position matrix |
| Messaging/positioning | `search_knowledge_base({ query: "<relevant terms>", entityTypes: ["messaging", "positioning"] })` | S2 Positioning Directive, S3 Persona message shifts |
| Playbook value props | `list_value_props({ playbookOId })` | S3 Persona use case hooks |
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

**Before generating, re-read `references/presentation-principles.md` and apply every rule.**

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

#### Design System: Collapsible Hierarchy

The document uses a three-level collapsible hierarchy with smart defaults:

1. **Sections** (`details.prep-section`): open by default — user sees all five sections expanded on load
2. **Card groups** (`details.card-group`): open by default — user sees all group headers and their card titles
3. **Individual cards** (`details.table-card`): CLOSED by default — user sees card titles as a scannable list, one click to expand any card

This means on page load, the user gets a scannable overview of every pain, belief, objection, theme, and risk by title alone, without being overwhelmed by detail. Heavy content (context grids, discovery questions, response lists) is one click away on any individual card.

Sub-sections in Section 1 (Company Context, People, Deal Context) are also `details.card-group` elements, open by default.

#### Design System: Table-Format Cards

Every individual card (pain, belief, objection, theme, risk) uses the same table-card pattern:

```html
<details class="table-card">
  <summary>Card title here</summary>
  <div class="context-grid">
    <div class="cg-row">
      <div class="cg-label">Label</div>
      <div class="cg-value">Value content</div>
    </div>
    <!-- more rows -->
  </div>
</details>
```

The card is a collapsible `<details class="table-card">` element. The title sits in the `<summary>`. The body is a `.context-grid` with `.cg-row` elements (label | value pairs). Row labels vary by card type:

| Card Type | Row Labels |
|-----------|-----------|
| Pain | Context, Status, How to probe, Watch out |
| Belief / Recognition | Context, Status, How to plant, Watch out |
| Persona Message | Pressure, Our story shifts to, Say this, Use case, Don't lead with |
| Competitive | Their positioning, Our counter, Trap question |
| Objection | You'll hear, Response (with `.response-list`), Watch out |
| Theme | Why it matters, Status, How to steer |

There are NO color-coded left borders, NO `data-type` attributes, NO `.context-card` class. The card type is communicated by the card group header it sits under.

#### Design System: Card Groups

Cards are organized under collapsible `<details class="card-group" open>` headers. Each card group has a `.card-group-intro` paragraph explaining the group's purpose. The group header communicates the card type — no legends needed.

Card groups by section:
- **Section 1:** "Company Context", "People", "Deal Context"
- **Section 2:** "What We Need Them to Recognize"
- **Section 3:** "How Our Message Lands by Persona", "Competitive Position", "Pains We Know They Have", "Themes to Steer"
- **Section 4:** Objection table-cards organized under theme tabs

There are NO `.cc-legend`, NO `.legend-swatch`, NO `.legend-divider`, NO `.legend-types`, NO `.legend-statuses` elements anywhere.

```html
<details class="card-group" open>
  <summary>Pains We Know They Have</summary>
  <p class="card-group-intro">Based on [scale / ICP match / signal], they're experiencing these problems. Our posture is confident — these are structural, not hypothetical.</p>

  <details class="table-card">
    <summary>Pain title here</summary>
    <div class="context-grid">
      <div class="cg-row">
        <div class="cg-label">Context</div>
        <div class="cg-value">Why we know this pain exists — grounded in their scale, product complexity, org structure</div>
      </div>
      <div class="cg-row">
        <div class="cg-label">Status</div>
        <div class="cg-value"><span class="cc-status unexplored">Unexplored</span></div>
      </div>
      <div class="cg-row">
        <div class="cg-label">How to probe</div>
        <div class="cg-value">How to surface this pain without naming it for them</div>
      </div>
      <div class="cg-row">
        <div class="cg-label">Watch out</div>
        <div class="cg-value cg-watchout">What NOT to say when probing this pain</div>
      </div>
    </div>
    <details class="cc-questions">
      <summary>2 discovery questions</summary>
      <div class="cc-q-grid">
        <div class="cc-q-header">Ask about</div>
        <div class="cc-q-header">Driving toward</div>
        <div class="cc-q-row">
          <div class="cc-q-cell">Topic to probe</div>
          <div class="cc-q-cell">What the answer reveals</div>
        </div>
      </div>
    </details>
  </details>

  <!-- more table-cards -->
</details>
```

#### Design System: Expand/Collapse All Toggle

A button in the header badge row allows expanding or collapsing all `<details>` elements:

```html
<button class="expand-toggle" id="expand-toggle" onclick="toggleAll()">
  <span class="toggle-icon">&#9660;</span> Expand all
</button>
```

JavaScript toggles all `<details>` elements open/closed and flips the label between "Expand all" and "Collapse all".

#### Design System: Company Identity with Logo

Inside the Company Context card group (after the `<summary>` and before the `.context-grid`), include a company identity block:

```html
<div class="company-identity">
  <img src="[logo_url]" alt="[Company]" class="company-logo">
  <span class="company-name">[Company]</span>
</div>
```

Use the `get_external_brand_logo` MCP tool to fetch the logo URL at generation time. If no logo is found, omit the `<img>` tag and just show the company name in the `<span>`.

#### Design System: Status Tags

Status tags appear inside table-card rows as `.cc-status` pills. Available statuses:

| Status | Used for | Style |
|--------|----------|-------|
| `Unexplored` | Pains/beliefs not yet raised | Warning (amber) |
| `Raised` | Pains/beliefs mentioned but unconfirmed | Brand primary (blue) |
| `Validated` | Confirmed from prior calls/data | Success (green) |
| `Needs Reinforcement` | Was validated but may be fading | Secondary (purple) |
| `Expected` | Objections/themes anticipated | Warning (amber) |

Status tags sit inside a `.cg-value` cell within the Status row of a table-card. They do NOT float as standalone badges.

#### Design System: Discovery Questions Position

Discovery questions are placed OUTSIDE the `.context-grid`, as a direct child of the `<details class="table-card">`:

```html
<details class="table-card">
  <summary>Card title</summary>
  <div class="context-grid">
    <!-- label/value rows -->
  </div>
  <details class="cc-questions">
    <summary>2 discovery questions</summary>
    <div class="cc-q-grid">
      <div class="cc-q-header">Ask about</div>
      <div class="cc-q-header">Driving toward</div>
      <div class="cc-q-row">
        <div class="cc-q-cell">Topic</div>
        <div class="cc-q-cell">What it reveals</div>
      </div>
    </div>
  </details>
</details>
```

This positions the expand trigger on the left side of the card, not buried inside a grid cell.

#### Design System: Response Lists for Objections

Objection cards use a `.response-list` inside the "Response" row value cell:

```html
<div class="cg-row">
  <div class="cg-label">Response</div>
  <div class="cg-value">
    <ul class="response-list">
      <li>First response point</li>
      <li>Second response point with <strong>emphasis</strong></li>
      <li>Third response point</li>
    </ul>
  </div>
</div>
```

Each `<li>` gets an arrow marker (`->`) via CSS `::before` pseudo-element. Use `<strong>` for key phrases within response points.

#### Design System: No Hardcoded Brand

The `:root` CSS variables are populated from the style preset selected in Step 3 OR from a brand kit. The HTML template uses generic variable references (`var(--bg)`, `var(--brand-primary)`, etc.), never specific hex values. Do not hardcode any specific brand or color scheme into the template.

**When using a brand kit** (`~/.octave/brands/<slug>/tokens.css`), map the kit tokens to the meeting prep's `:root` variables:

| Meeting Prep Var | Brand Kit Source |
|---|---|
| `--bg` | `--brand-bg-primary` |
| `--bg-elevated` | `--brand-bg-tint` |
| `--bg-card` | `--brand-bg-secondary` |
| `--bg-panel` | `--brand-bg-panel` |
| `--text-primary` | `--brand-fg-primary` |
| `--text-secondary` | `--brand-gray-60` or mid-tone gray |
| `--text-muted` | `--brand-fg-muted` |
| `--brand-primary` | `--brand-accent` |
| `--brand-primary-soft` | `--brand-state-info-weak` or 12% alpha of accent |
| `--secondary` | `--brand-accent-hover` |
| `--border` | `--brand-border-primary` |
| `--border-strong` | `--brand-border-secondary` |
| `--font-display` / `--font-body` | `--brand-font-sans` |
| `--font-mono` | `--brand-font-mono` |

Also use the kit's `@font-face` declaration (pointing to the CDN or local font file), heading weight (often 600, not 700), and `letter-spacing` for headings.

**⚠️ REQUIRED: When using a brand kit, you MUST include the brand header and brand footer.** See the "Brand Header & Footer" section below for the templates. Read the logo SVG from the kit directory and inline it. When using a generic style preset, omit the brand header/footer.

---

#### Document Structure (Header + Snapshot + 5 Sections)

---

**Header** (not a numbered section — the document frame)

The header answers three questions: What is this? Who is it about? What's the context?

```html
<header class="prep-header">
  <div class="header-badges">
    <span class="meeting-badge">[Meeting Type]</span>
    <span class="duration-badge">[Duration] min</span>
    <button class="expand-toggle" id="expand-toggle" onclick="toggleAll()">
      <span class="toggle-icon">&#9660;</span> Expand all
    </button>
  </div>
  <h1>Meeting Prep: [Company Name]</h1>
  <p class="header-subtitle">[One sentence describing the meeting context]</p>
  <p class="header-meta">[Date] · [Attendee names or "Attendees TBD"]</p>
</header>
```

Rules:
- Title format: "Meeting Prep: [Company]" — not just the company name, not "Battle Plan"
- Meeting type badge: "Discovery Call", "Demo", "Executive Meeting" — plain language, not "Discovery Battle Plan"
- Duration badge: just the number + "min"
- Expand/collapse toggle button sits in the badge row
- Subtitle: one sentence describing the meeting and its purpose — NO deal stats, NO tool names
- No branding, no "powered by" text, no "Stream B", no "Octave intelligence"

**Brand Header & Footer** (REQUIRED when a brand kit is active)

**⚠️ This is mandatory, not optional.** When the meeting prep is styled from a brand kit, you MUST add a sticky brand header at the top and a brand footer at the bottom. These frame the document in the brand's identity. Read the logo SVG from `~/.octave/brands/<slug>/` (e.g. `<slug>-logo.svg`) and inline it into both the header and footer. **Omit these only when using a generic style preset.**

```html
<!-- Brand Header — sticky, frosted glass blur -->
<header class="brand-header">
  <div class="brand-header-inner">
    <a class="brand-header-logo" href="https://[domain]" target="_blank">
      <!-- Inline the brand's real SVG logo from the kit -->
      <svg>...</svg>
      <span>[Company Name]</span>
    </a>
    <div class="brand-header-right">
      <span class="brand-header-tag">Meeting Prep</span>
    </div>
  </div>
</header>
```

```html
<!-- Brand Footer — at the very end, before </body> -->
<footer class="brand-footer">
  <div class="brand-footer-inner">
    <div class="brand-footer-logo">
      <!-- Same logo, smaller -->
      <svg>...</svg>
      <span>[Company Name]</span>
    </div>
    <div class="brand-footer-meta">Prepared [Date]</div>
  </div>
</footer>
```

Rules:
- Logo: inline the real SVG from the brand kit (`<slug>-logo.svg`), never hotlink. Use `fill="currentColor"` so it inherits the text color.
- Header is sticky with `backdrop-filter: blur(12px)` for the frosted glass effect on scroll.
- Footer shows the date the prep was generated.
- Both hidden in `@media print`.
- The header tag says "Meeting Prep" — not the company name again, not "Powered by Octave."

**Deal Snapshot Bar** (directly under header)

A labeled key-value grid showing CRM fields at a glance. Every value has a label.

```html
<div class="snapshot-bar">
  <div class="snapshot-item">
    <span class="snapshot-label">Deal Value</span>
    <span class="snapshot-value">$500,000</span>
  </div>
  <div class="snapshot-item">
    <span class="snapshot-label">Stage</span>
    <span class="snapshot-value">Technical Evaluation</span>
  </div>
  <div class="snapshot-item">
    <span class="snapshot-label">Target Close</span>
    <span class="snapshot-value">Q2 2026</span>
  </div>
  <div class="snapshot-item">
    <span class="snapshot-label">Primary Contact</span>
    <span class="snapshot-value">Jane Smith, VP Eng</span>
  </div>
</div>
```

Rules:
- If a field is unknown, display "Unknown" or "TBD" — never omit the label
- These are the ONE canonical location for deal stats — do not repeat them elsewhere
- If no deal exists yet (net-new prospect), show what's known and label unknowns

---

**Section 1: Context**

*What the seller needs to know about the account, the people, and the deal before the call.*

One-line intro at the top of the section: "Everything you need to know about the account, the people, and the deal going into this call."

Sub-components are organized as card groups (`details.card-group` open by default):

**Company Context** — a card group containing a company identity block and a `.context-grid` with `.cg-row` elements.

```html
<details class="card-group" open>
  <summary>Company Context</summary>
  <div class="company-identity">
    <img src="[logo_url]" alt="[Company]" class="company-logo">
    <span class="company-name">[Company]</span>
  </div>
  <div class="context-grid">
    <div class="cg-row">
      <div class="cg-label">What they do</div>
      <div class="cg-value">[1 sentence description]</div>
    </div>
    <div class="cg-row">
      <div class="cg-label">Scale</div>
      <div class="cg-value">[Employee count, revenue, funding — whatever's known]</div>
    </div>
    <div class="cg-row">
      <div class="cg-label">Why they're a fit</div>
      <div class="cg-value">[Fit reasoning with persona/segment match]</div>
    </div>
    <div class="cg-row">
      <div class="cg-label">Key signal</div>
      <div class="cg-value">[Funding, hiring, tech stack changes, trigger events]</div>
    </div>
    <div class="cg-row">
      <div class="cg-label">Angle</div>
      <div class="cg-value">[The strategic angle for this conversation]</div>
    </div>
  </div>
</details>
```

5-7 grid rows maximum. Add rows as needed (e.g., "Industry", "Tech stack") but keep it tight.

**What's Happening Now** *(conditional — include only when deep research was run)* — a card group placed immediately after Company Context. It surfaces the macro themes and recent signals that a rep would otherwise Google for themselves.

This section has two components:

1. **Macro Themes** — 1-2 big-picture strategic themes for the company this year (e.g., "Preparing for IPO", "First international expansion", "Pivoting to platform model"). These come from deep web research and should be company-level strategic narratives, not product news.

2. **Signal Feed** — 3-5 recent, concrete signals: news, hires, launches, funding, partnerships, regulatory moves. Each signal gets a date (or approximate timeframe) and a one-line "why it matters" tied to the deal angle.

```html
<details class="card-group" open>
  <summary>What's Happening Now</summary>
  <p class="card-group-intro">Macro themes and recent signals from deep research — what a rep would find googling [Company] right now.</p>

  <div class="macro-themes">
    <div class="macro-theme">
      <div class="mt-title">[Theme title — e.g., "Path to IPO"]</div>
      <div class="mt-body">[2-3 sentences: what's happening, why it matters for this deal, how to reference it naturally]</div>
    </div>
    <div class="macro-theme">
      <div class="mt-title">[Second theme]</div>
      <div class="mt-body">[2-3 sentences]</div>
    </div>
  </div>

  <div class="signal-feed">
    <div class="signal-item">
      <div class="signal-date">[Month YYYY or "Q1 2026"]</div>
      <div class="signal-body">
        <div class="signal-headline">[What happened — one line]</div>
        <div class="signal-relevance">[Why it matters for this deal — one line]</div>
      </div>
    </div>
    <!-- more signal-items -->
  </div>
</details>
```

Rules:
- Only include this section when `deep_web_research` was called during context gathering. If deep research was not run, omit silently.
- Macro themes should be strategic narratives, not product feature announcements. Think "what would a board member care about."
- Signal feed items must have dates. Undated signals are useless.
- The "why it matters" line must connect to the deal angle — don't just restate the news.
- 1-2 macro themes maximum. 3-5 signals maximum. Tight.

**People** — a card group containing a `.people-grid` with `.persona-group` elements. The structure is **persona-first**: group by the function/role that matters, explain why that persona is relevant, then list the actual people who fit underneath.

*Persona groups:* Each `.persona-group` has a header (persona title + "Potential fits" tag), a `.persona-why` paragraph explaining why this function matters for this specific deal, and a `.persona-people` list of matching individuals.

*When you have real people from research:* Default to showing them. Don't fall back to generic role descriptions when named candidates exist. Include LinkedIn links for every named person. **Always use `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` to find contacts** — this returns LinkedIn profile URLs along with name, title, and location. Use the returned LinkedIn URLs directly in the `.pp-link` elements. Do not guess or construct LinkedIn URLs manually.

*When no people are found:* Still show the persona group with the "why" context, but replace the people list with a single line: "No candidates identified yet — search [title keywords] on LinkedIn."

*Confirmed attendees:* If someone is confirmed for the meeting, add a `.slot-tag.confirmed-tag` next to their name instead of "Potential fits" on the group header.

```html
<details class="card-group" open>
  <summary>People</summary>
  <p class="card-group-intro">No confirmed attendees yet. These are personas most likely to feel the pain, with potential fits at [Company].</p>

  <div class="people-grid">
    <div class="persona-group">
      <div class="persona-header">
        <span class="persona-title">Sales Strategy &amp; Operations</span>
        <span class="slot-tag potential-fit">Potential fits</span>
      </div>
      <div class="persona-why">[2-3 sentences on what this persona owns and why it matters for THIS company. Be specific — reference their product lines, team scale, geo spread, or recent changes that make this role feel the pain.]</div>
      <div class="persona-people">
        <div class="persona-person">
          <div class="pp-avatar">DR</div>
          <div class="pp-info">
            <div class="pp-name">Dan Reddin</div>
            <div class="pp-title">Head of Sales Strategy &amp; Operations &middot; San Francisco</div>
          </div>
          <a class="pp-link" href="https://linkedin.com/in/dan-reddin" target="_blank">LinkedIn &rarr;</a>
        </div>
      </div>
    </div>

    <div class="persona-group">
      <div class="persona-header">
        <span class="persona-title">Product Marketing</span>
        <span class="slot-tag potential-fit">Potential fits</span>
      </div>
      <div class="persona-why">[Why PMM matters here — e.g., owns battle cards and competitive positioning across N competitors, sees content decay daily as product story evolves.]</div>
      <div class="persona-people">
        <div class="persona-person">
          <div class="pp-avatar">HT</div>
          <div class="pp-info">
            <div class="pp-name">Holly Turay Avery</div>
            <div class="pp-title">Enterprise PMM &middot; New York</div>
          </div>
          <a class="pp-link" href="https://linkedin.com/in/holly-turay-avery" target="_blank">LinkedIn &rarr;</a>
        </div>
        <div class="persona-person">
          <div class="pp-avatar">MK</div>
          <div class="pp-info">
            <div class="pp-name">Mike Kim</div>
            <div class="pp-title">Senior PMM, Platform &middot; San Francisco</div>
          </div>
          <a class="pp-link" href="https://linkedin.com/in/mikekim" target="_blank">LinkedIn &rarr;</a>
        </div>
      </div>
    </div>
  </div>
</details>
```

The "why" paragraph is the key value — it should read like a briefing on why you'd want this persona in the room, grounded in the specific company context (their products, scale, org structure, competitive landscape). Generic role descriptions ("owns messaging propagation") are not enough.

*"How we make them the hero":* After the `.persona-why` paragraph, add a `.persona-hero` div — one sentence on how our positioning makes this person look good in their org. Source from ICP cells + playbook value props. This should read like "positions them as..." — the person who solved the problem, freed the team, etc.

```html
<div class="persona-hero">Positions them as the architect of a scalable GTM infrastructure — the person who solved the rebuild problem.</div>
```

**Existing Connections** — If research surfaces relationships, surface them here. If no connections found, omit this sub-section silently.

**Deal Context** — a card group containing a `.context-grid` with `.cg-row` elements (same pattern as Company Context).

```html
<details class="card-group" open>
  <summary>Deal Context</summary>
  <div class="context-grid">
    <div class="cg-row">
      <div class="cg-label">Stage</div>
      <div class="cg-value">Net-New — Discovery</div>
    </div>
    <div class="cg-row">
      <div class="cg-label">Activity</div>
      <div class="cg-value">4 meetings, 12 emails in last 30 days</div>
    </div>
    <div class="cg-row">
      <div class="cg-label">Competition</div>
      <div class="cg-value">[See competition language rules below]</div>
    </div>
    <div class="cg-row">
      <div class="cg-label">Champion</div>
      <div class="cg-value">Not yet identified</div>
    </div>
    <div class="cg-row">
      <div class="cg-label">Compelling Event</div>
      <div class="cg-value">Unknown — probe for reorgs or product launches</div>
    </div>
    <div class="cg-row">
      <div class="cg-label">Buying Triggers</div>
      <div class="cg-value">Fiscal year planning, new product launch, competitor move, reorg — what would trigger action now</div>
    </div>
  </div>
</details>
```

**Competition language rules** for the Competition field in Deal Context:
- If we KNOW who's competing: state it directly (e.g., "Datadog, internal build")
- If we're speculating: "Unknown — Potential: internal build, Glean"
- NEVER use "Likely:" as a prefix when we have no confirmed intel
- General principle: always distinguish confirmed facts from speculation

**Deal Timeline** *(conditional — include when event/finding data exists)* — a visual timeline placed inside or immediately after the Deal Context card group. It shows the engagement arc: when the deal started, key milestones, gaps in activity, and current momentum.

The timeline uses a horizontal dot-and-line pattern. Each milestone gets a dot, a date, and a one-line label. Gaps in engagement are shown as dashed segments with a label (e.g., "6 months — no activity").

```html
<div class="deal-timeline">
  <div class="tl-track">
    <div class="tl-item">
      <div class="tl-dot"></div>
      <div class="tl-date">Feb 2025</div>
      <div class="tl-label">First engagement — intro call</div>
    </div>
    <div class="tl-item">
      <div class="tl-dot"></div>
      <div class="tl-date">Mar 2025</div>
      <div class="tl-label">Discovery + technical deep-dive</div>
    </div>
    <div class="tl-gap">
      <div class="tl-gap-line"></div>
      <div class="tl-gap-label">7 months — no activity</div>
    </div>
    <div class="tl-item">
      <div class="tl-dot active"></div>
      <div class="tl-date">Jan 2026</div>
      <div class="tl-label">Re-engaged — 5 meetings since</div>
    </div>
    <div class="tl-item current">
      <div class="tl-dot active"></div>
      <div class="tl-date">Jun 2026</div>
      <div class="tl-label">Today — Demo</div>
    </div>
  </div>
</div>
```

Rules:
- Only include when you have actual event/finding data to populate it. If no deal history exists, omit silently.
- Use `list_events` and `list_findings` data to reconstruct the timeline. Cluster nearby events into single milestones (don't show every individual email).
- Highlight gaps explicitly — a 6-month silence is critical context a rep needs to see.
- The most recent / current item gets a `.current` class and an `.active` dot (brand-colored).
- Keep it to 3-6 milestones. This is a scannable arc, not a CRM activity log.
- On mobile, the timeline stacks vertically.

IMPORTANT: "Their Pains" is NOT a sub-section of Section 1. Pains are table-cards in Section 3. "ICP Indicator" is NOT a separate sub-section — persona/segment match is folded into the "Why they're a fit" row of Company Context.

---

**Section 2: Goals**

*What we need to accomplish in this meeting — our positioning frame, what they need to recognize, and how we advance.*

One-line intro: "What we need to accomplish in this meeting — our positioning frame, what they need to recognize, and how we advance."

Sub-components:

**Positioning Directive** — A concise, structured block that replaces exit criteria. Not a paragraph — a clear three-part frame:

```html
<h3 class="sub-section-title">Positioning Directive</h3>
<div class="positioning-directive">
  <div class="pd-row">
    <div class="pd-label">Position us as</div>
    <div class="pd-value">[One line — the frame we want in their head]</div>
  </div>
  <div class="pd-row">
    <div class="pd-label">Mitigate</div>
    <div class="pd-value">[The specific risk/objection/competitor angle to neutralize]</div>
  </div>
  <div class="pd-row">
    <div class="pd-label">Advance</div>
    <div class="pd-value">[The deal motion — next step, commitment, or validation we need]</div>
  </div>
</div>
```

CSS: `.positioning-directive` (grid container), `.pd-row` (2-column grid like `.cg-row`), `.pd-label` (brand-primary color, uppercase), `.pd-value`. The label column uses `var(--brand-primary)` color to visually distinguish from context grid labels.

This is the messaging/positioning intelligence showing its value. Grounded in Octave's positioning entities + deal context.

**What We Need Them to Recognize** — a card group of recognition table-cards. Reframed from passive "beliefs" to active voice:

```html
<details class="card-group" open>
  <summary>What We Need Them to Recognize</summary>
  <p class="card-group-intro">Conclusions we need them to reach. Active voice, opinionated — we know these are true, we need them to see it too.</p>

  <details class="table-card">
    <summary>GTM context is infrastructure, not content</summary>
    <div class="context-grid">
      <div class="cg-row">
        <div class="cg-label">Context</div>
        <div class="cg-value">Why this recognition matters for this specific deal</div>
      </div>
      <div class="cg-row">
        <div class="cg-label">Status</div>
        <div class="cg-value"><span class="cc-status unexplored">Unexplored</span></div>
      </div>
      <div class="cg-row">
        <div class="cg-label">How to plant</div>
        <div class="cg-value">Specific approach to get them to this conclusion</div>
      </div>
      <div class="cg-row">
        <div class="cg-label">Watch out</div>
        <div class="cg-value cg-watchout">What NOT to say that would undermine this recognition</div>
      </div>
    </div>
    <details class="cc-questions">
      <summary>1 discovery question</summary>
      <!-- cc-q-grid -->
    </details>
  </details>
</details>
```

The "Watch out" row uses `.cg-watchout` styling (muted, italic) and provides a specific anti-pattern — what to avoid saying when trying to plant this recognition.

3-4 recognition cards maximum. Order by importance to this meeting.

---

**Section 3: What to Say & Ask**

*The playbook for the room — how our message lands by persona, where we stand competitively, pains we know they have, and themes to steer.*

One-line intro: "The playbook for the room — how our message lands by persona, where we stand competitively, pains we know they have, and themes to steer."

**How Our Message Lands by Persona** — A tabbed card group. Each tab represents a persona who'll be in the room. The tab bar sits at the top; clicking a tab reveals that persona's messaging card.

```html
<details class="card-group" open>
  <summary>How Our Message Lands by Persona</summary>
  <p class="card-group-intro">Each person in the room hears our story differently. Click a tab to see how to shift the message.</p>

  <div class="tab-bar">
    <button class="tab-btn active" onclick="switchTab(this, 'persona-tabs')">Sales Ops</button>
    <button class="tab-btn" onclick="switchTab(this, 'persona-tabs')">PMM</button>
    <button class="tab-btn" onclick="switchTab(this, 'persona-tabs')">Engineering</button>
  </div>

  <div id="persona-tabs">
    <div class="tab-panel active">
      <div class="context-grid">
        <div class="cg-row"><div class="cg-label">Pressure</div><div class="cg-value">The structural pressure this persona is under</div></div>
        <div class="cg-row"><div class="cg-label">Our story shifts to</div><div class="cg-value">How our narrative changes for this persona</div></div>
        <div class="cg-row"><div class="cg-label">Say this</div><div class="cg-value">One concrete hook line for this persona</div></div>
        <div class="cg-row"><div class="cg-label">Use case</div><div class="cg-value">Specific use case that matters to them</div></div>
        <div class="cg-row"><div class="cg-label">Don't lead with</div><div class="cg-value cg-watchout">What to avoid with this persona and why</div></div>
      </div>
    </div>
    <!-- More tab-panels -->
  </div>
</details>
```

Sources: Octave messaging entities, playbook value props, ICP cells. **Conditional** — show when we have strong Octave data, degrade gracefully when thin. If we only have 1-2 personas with strong data, show those and omit thin ones.

Tab labels should be short persona names (e.g., "Sales Ops", "PMM", "CRO") — not full titles.

**Competitive Position** — A card group with competitive table-cards. For each known or likely competitor:

```html
<details class="card-group" open>
  <summary>Competitive Position</summary>
  <p class="card-group-intro">How to handle each competitive angle in this deal.</p>

  <details class="table-card">
    <summary>Competitor Name (positioning angle)</summary>
    <div class="context-grid">
      <div class="cg-row"><div class="cg-label">Their positioning</div><div class="cg-value">What the competitor claims / what the prospect believes</div></div>
      <div class="cg-row"><div class="cg-label">Our counter</div><div class="cg-value">How we differentiate — architectural, not feature-level</div></div>
      <div class="cg-row"><div class="cg-label">Trap question</div><div class="cg-value">A question that exposes the competitor's weakness without naming them</div></div>
    </div>
  </details>
</details>
```

Sources: Octave competitor entities, battlecard data. **Conditional richness** — if competitor entities exist in the library, build the full matrix. If not, keep the honest single row in Deal Context and note "No confirmed competitors — competitive position section omitted."

Include "Internal Build" as a competitive card when the company has strong engineering culture — this is often the biggest competitor.

**Pains We Know They Have** — a card group of pain table-cards. Moved from Section 2 and reframed with an opinionated posture:

```html
<details class="card-group" open>
  <summary>Pains We Know They Have</summary>
  <p class="card-group-intro">Based on [scale / ICP match / signal], they're experiencing these problems. Our posture is confident — these are structural, not hypothetical.</p>

  <details class="table-card">
    <summary>Cascading rebuild on every strategy change</summary>
    <div class="context-grid">
      <div class="cg-row">
        <div class="cg-label">Context</div>
        <div class="cg-value">Why we know this pain exists — grounded in their scale, product complexity, org structure</div>
      </div>
      <div class="cg-row">
        <div class="cg-label">Status</div>
        <div class="cg-value"><span class="cc-status unexplored">Unexplored</span></div>
      </div>
      <div class="cg-row">
        <div class="cg-label">How to probe</div>
        <div class="cg-value">How to surface this pain without naming it for them</div>
      </div>
      <div class="cg-row">
        <div class="cg-label">Watch out</div>
        <div class="cg-value cg-watchout">What NOT to say when probing this pain</div>
      </div>
    </div>
    <details class="cc-questions">
      <summary>2 discovery questions</summary>
      <!-- cc-q-grid -->
    </details>
  </details>
</details>
```

The intro should read confidently: "Based on [specific evidence], they're experiencing..." not "Hypothesized pains we haven't raised yet." Status tags still exist but the default posture is "we know these are real."

3-4 pain table-cards maximum.

**Themes to Steer** — a card group of theme table-cards. These are conversation topics where we can steer toward our strengths — not pushback, but opportunity.

```html
<details class="card-group" open>
  <summary>Themes to Steer</summary>
  <p class="card-group-intro">Topics that will come up where we can steer the conversation toward our strengths. Not pushback — opportunity.</p>

  <details class="table-card">
    <summary>Agent context and automation governance</summary>
    <div class="context-grid">
      <div class="cg-row">
        <div class="cg-label">Why it matters</div>
        <div class="cg-value">Why this topic matters in this specific deal</div>
      </div>
      <div class="cg-row">
        <div class="cg-label">Status</div>
        <div class="cg-value"><span class="cc-status expected">Expected</span></div>
      </div>
      <div class="cg-row">
        <div class="cg-label">How to steer</div>
        <div class="cg-value">The messaging/positioning angle to pull this topic toward our strengths</div>
      </div>
    </div>
  </details>
</details>
```

2-3 theme table-cards maximum. The row label is "How to steer" (not "How to handle") — reflecting the active steering posture.

**Objection framing rules:** Objection titles must be high-level descriptions of the risk, NOT quotes in the prospect's voice:
- BAD: `"We already use Glean for this"`
- GOOD: `They position this as overlap with existing enterprise search`
- BAD: `"We could build this ourselves"`
- GOOD: `Their engineering team defaults to building internally`

The objection should describe the situation or risk, not put words in the prospect's mouth.

---

**Section 4: Objections**

*Pushback we expect, organized by theme. Have your responses sharp — and know what NOT to say.*

One-line intro: "Pushback we expect, organized by theme. Have your responses sharp — and know what NOT to say."

This section has its own dedicated place (not buried inside Section 3) because objection handling is critical enough to deserve standalone attention.

**Structure:** Theme tabs at the top, objection cards underneath each tab.

**Theme tabs** organize objections by category:
- Status Quo & Inertia
- Technical & Integration
- Competitive
- Pricing & Value
- (additional themes as relevant to the deal)

Each theme tab has a one-line intro explaining why this theme matters in this specific deal.

```html
<details class="prep-section" open id="objections">
  <summary>4. Objections</summary>
  <p class="section-intro">Pushback we expect, organized by theme. Have your responses sharp — and know what NOT to say.</p>

  <div class="tab-bar">
    <button class="tab-btn active" onclick="switchTab(this, 'objection-tabs')">Status Quo & Inertia</button>
    <button class="tab-btn" onclick="switchTab(this, 'objection-tabs')">Technical & Integration</button>
    <button class="tab-btn" onclick="switchTab(this, 'objection-tabs')">Competitive</button>
  </div>

  <div id="objection-tabs">
    <div class="tab-panel active">
      <p class="card-group-intro">Why this theme matters in this specific deal.</p>

      <details class="table-card">
        <summary>
          <span>Objection title (descriptive, not quoted)</span>
          <span class="persona-tag">Sales Ops</span>
          <span class="persona-tag">Engineering</span>
        </summary>
        <div class="context-grid">
          <div class="cg-row">
            <div class="cg-label">You'll hear</div>
            <div class="cg-value">The actual sentence they'll say — in their voice</div>
          </div>
          <div class="cg-row">
            <div class="cg-label">Response</div>
            <div class="cg-value">
              <ul class="response-list">
                <li>First response point</li>
                <li>Second response point with <strong>emphasis</strong></li>
              </ul>
            </div>
          </div>
          <div class="cg-row">
            <div class="cg-label">Watch out</div>
            <div class="cg-value cg-watchout">What NOT to say in response — the thing that would make this objection worse</div>
          </div>
        </div>
      </details>
    </div>
    <!-- More tab-panels for other themes -->
  </div>
</details>
```

**Objection card structure:**
- **Summary:** Descriptive title (same framing rule as before — not quotes in prospect's voice) + `.persona-tag` pill badges indicating who typically raises it
- **"You'll hear"** row: The actual sentence the prospect will say, in their voice. This is where the prospect's words go — not the title.
- **Response** row: Response points using `.response-list` format (same as before)
- **"Watch out"** row: What NOT to say in response, using `.cg-watchout` styling

**Persona tags** are pill badges (`.persona-tag`) that sit inside the `<summary>` element after the title `<span>`. They indicate which personas typically raise this objection.

**Content limits:** Cap at **6-8 objections total** across all themes. Quality over comprehensiveness. Some themes may have 1 card, some may have 3.

**Theme selection:** Choose themes relevant to the deal. Not every deal needs all four standard themes. A startup deal might only have "Status Quo & Inertia" and "Competitive." An enterprise deal might have all four plus a custom theme.

---

**Section 5: The Takeaway**

*The one thing to remember walking into the call.*

One-line intro: "If you remember nothing else, remember this."

One sentence. The thing you'd write on a sticky note and put on your monitor before the call. It should distill the entire prep into a single actionable insight.

Section 5 uses a `<section>` element (not `<details>`) since it's always visible:

```html
<section class="prep-section" id="the-takeaway">
  <h2 style="font-family:var(--font-display);font-size:clamp(1.1rem,2vw,1.35rem);font-weight:600;padding:0.75rem 0;">5. The Takeaway</h2>
  <p class="section-intro">If you remember nothing else, remember this.</p>
  <div class="the-takeaway">
    <blockquote>[One memorable sentence]</blockquote>
  </div>
</section>
```

---

#### HTML Architecture

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Meeting Prep: [Company] — [Meeting Type]</title>
  <!-- Google Fonts (preconnect + stylesheet) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* === CSS Variables (from brand kit or style preset) === */
    :root {
      --bg: /* from brand kit or style preset */;
      --bg-elevated: /* from brand kit or style preset */;
      --bg-card: /* from brand kit or style preset */;
      --bg-panel: /* from brand kit or style preset */;
      --text-primary: /* from brand kit or style preset */;
      --text-secondary: /* from brand kit or style preset */;
      --text-muted: /* from brand kit or style preset */;
      --brand-primary: /* from brand kit or style preset */;
      --brand-primary-soft: /* from brand kit or style preset */;
      --brand-primary-muted: /* 25% alpha of brand-primary */;
      --secondary: /* from brand kit or style preset */;
      --success: #3fb950;
      --success-soft: rgba(63,185,80,0.12);
      --warning: #d29922;
      --warning-soft: rgba(210,153,34,0.12);
      --error: #f85149;
      --error-soft: rgba(248,81,73,0.12);
      --border: /* from brand kit or style preset */;
      --border-strong: /* from brand kit or style preset */;
      --border-soft: /* from brand kit or style preset */;
      --font-display: /* from brand kit or style preset */;
      --font-body: /* from brand kit or style preset */;
      --font-mono: /* from brand kit or style preset */;
      --radius: 6px;
      --radius-lg: 8px;
      --radius-section: 12px;
      --radius-pill: 9999px;
      --shadow-low: 0px 1px 4px -1px rgba(0,0,0,0.09);
      --shadow-medium: 0px 4px 24px rgba(0,0,0,0.2);
      --ease: cubic-bezier(0.25, 0.46, 0.45, 0.94);
      --speed: 0.16s;
    }

    /* === Reset & Base === */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      background: var(--bg);
      color: var(--text-primary);
      font-family: var(--font-body);
      line-height: 1.6;
      font-size: 15px;
    }

    /* === Layout === */
    .prep-container {
      max-width: 900px;
      margin: 0 auto;
      padding: 2rem clamp(1rem, 4vw, 3rem);
    }

    /* === Sidebar Navigation (sticky) === */
    .prep-nav {
      position: fixed;
      top: 50%;
      right: clamp(0.5rem, 2vw, 2rem);
      transform: translateY(-50%);
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
      z-index: 100;
    }
    .prep-nav a {
      display: block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--text-muted);
      transition: all 0.3s ease;
      text-decoration: none;
    }
    .prep-nav a.active {
      background: var(--brand-primary);
      transform: scale(1.5);
    }

    /* === Header === */
    .prep-header { margin-bottom: 1.5rem; padding-bottom: 1rem; }
    .header-badges { display: flex; gap: 0.5rem; margin-bottom: 0.75rem; flex-wrap: wrap; }
    .prep-header h1 {
      font-family: var(--font-display);
      font-size: clamp(1.6rem, 3vw, 2.2rem);
      font-weight: 700;
      margin-bottom: 0.5rem;
      letter-spacing: -0.02em;
    }
    .header-subtitle {
      font-size: clamp(0.9rem, 1.3vw, 1.05rem);
      color: var(--text-secondary);
      margin-bottom: 0.25rem;
      line-height: 1.5;
    }
    .header-meta { font-size: 0.8rem; color: var(--text-muted); }

    /* === Meeting Type & Duration Badges === */
    .meeting-badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: var(--radius-pill);
      background: var(--brand-primary);
      color: white;
      font-size: 0.72rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .duration-badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: var(--radius-pill);
      background: var(--bg-elevated);
      border: 1px solid var(--border-strong);
      color: var(--text-secondary);
      font-size: 0.72rem;
      font-weight: 600;
    }

    /* === Expand/Collapse Toggle === */
    .expand-toggle {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      padding: 0.3rem 0.7rem;
      border-radius: var(--radius-pill);
      background: var(--bg-elevated);
      border: 1px solid var(--border-strong);
      color: var(--text-secondary);
      font-family: var(--font-body);
      font-size: 0.7rem;
      font-weight: 600;
      cursor: pointer;
      transition: color 0.15s ease, border-color 0.15s ease;
    }
    .expand-toggle:hover {
      color: var(--text-primary);
      border-color: var(--brand-primary);
    }
    .expand-toggle .toggle-icon {
      font-size: 0.6rem;
      color: var(--brand-primary);
    }

    /* === Snapshot Bar === */
    .snapshot-bar {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 1rem;
      padding: 1rem 1.25rem;
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      margin-bottom: 2.5rem;
    }
    .snapshot-item { text-align: center; }
    .snapshot-label {
      display: block;
      font-size: 0.65rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-muted);
      margin-bottom: 0.2rem;
    }
    .snapshot-value {
      display: block;
      font-family: var(--font-display);
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--text-primary);
    }

    /* === Section Styles === */
    .prep-section {
      margin-bottom: 2.5rem;
      padding-bottom: 2rem;
      border-bottom: 1px solid var(--border);
    }
    .section-intro {
      font-size: 0.82rem;
      color: var(--text-muted);
      font-style: italic;
      margin-bottom: 1.25rem;
      line-height: 1.5;
    }

    /* === Collapsible Sections (details.prep-section) === */
    details.prep-section {
      border-bottom: 1px solid var(--border);
      margin-bottom: 2.5rem;
      padding-bottom: 1rem;
    }
    details.prep-section > summary {
      cursor: pointer;
      font-family: var(--font-display);
      font-size: clamp(1.1rem, 2vw, 1.35rem);
      font-weight: 600;
      color: var(--text-primary);
      padding: 0.75rem 0;
      list-style: none;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      letter-spacing: -0.01em;
    }
    details.prep-section > summary::-webkit-details-marker { display: none; }
    details.prep-section > summary::before {
      content: "\25B6";
      font-size: 0.65em;
      color: var(--brand-primary);
      transition: transform 0.2s ease;
    }
    details.prep-section[open] > summary::before { transform: rotate(90deg); }

    /* === Sub-section Headers === */
    .sub-section-title {
      font-family: var(--font-display);
      font-size: clamp(0.88rem, 1.4vw, 1.05rem);
      font-weight: 600;
      color: var(--text-primary);
      margin: 1.75rem 0 0.75rem 0;
      padding-bottom: 0.35rem;
      border-bottom: 1px solid var(--border);
    }
    .sub-section-title:first-of-type { margin-top: 0.5rem; }

    /* === Generic Card === */
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: clamp(1rem, 2vw, 1.5rem);
      margin-bottom: 0.75rem;
    }

    /* === Card Groups (collapsible sub-sections) === */
    .card-group {
      margin-bottom: 1.25rem;
    }
    .card-group > summary {
      font-family: var(--font-display);
      font-size: clamp(0.85rem, 1.3vw, 0.98rem);
      font-weight: 600;
      color: var(--text-primary);
      padding: 0.5rem 0;
      cursor: pointer;
      list-style: none;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .card-group > summary::-webkit-details-marker { display: none; }
    .card-group > summary::before {
      content: "\25B6";
      font-size: 0.55em;
      color: var(--brand-primary);
      transition: transform 0.2s ease;
    }
    .card-group[open] > summary::before { transform: rotate(90deg); }
    .card-group-intro {
      font-size: 0.78rem;
      color: var(--text-muted);
      font-style: italic;
      margin-bottom: 0.75rem;
      line-height: 1.5;
    }

    /* === Company Identity === */
    .company-identity {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      margin-bottom: 0.75rem;
    }
    .company-logo {
      width: 28px;
      height: 28px;
      border-radius: 6px;
      object-fit: contain;
      background: white;
      padding: 3px;
    }
    .company-name {
      font-family: var(--font-display);
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text-primary);
    }

    /* === Context Grid (used for Company, Deal, and inside Table Cards) === */
    .context-grid {
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      overflow: hidden;
    }
    .cg-row {
      display: grid;
      grid-template-columns: 140px 1fr;
      border-bottom: 1px solid var(--border);
    }
    .cg-row:last-child { border-bottom: none; }
    .cg-label {
      font-size: 0.72rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-muted);
      padding: 0.6rem 0.9rem;
      background: var(--bg-elevated);
      display: flex;
      align-items: flex-start;
      padding-top: 0.7rem;
    }
    .cg-value {
      font-size: 0.85rem;
      color: var(--text-secondary);
      padding: 0.6rem 0.9rem;
      line-height: 1.5;
    }

    /* === People — Persona Groups === */
    .people-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 0.6rem;
    }
    .persona-group {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      overflow: hidden;
    }
    .persona-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.6rem 1rem;
      border-bottom: 1px solid var(--border);
    }
    .persona-title {
      font-weight: 600;
      font-size: 0.88rem;
      color: var(--text-primary);
    }
    .persona-why {
      padding: 0.45rem 1rem 0.5rem;
      font-size: 0.78rem;
      color: var(--text-muted);
      line-height: 1.45;
      border-bottom: 1px solid var(--border);
    }
    .persona-people {
      padding: 0.35rem 0;
    }
    .persona-person {
      display: flex;
      align-items: center;
      gap: 0.65rem;
      padding: 0.4rem 1rem;
    }
    .persona-person + .persona-person {
      border-top: 1px solid var(--border);
    }
    .pp-avatar {
      width: 30px;
      height: 30px;
      border-radius: 50%;
      background: var(--brand-primary-soft, rgba(99,102,241,0.1));
      border: 1px solid var(--brand-primary-muted, rgba(99,102,241,0.2));
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--brand-primary, #6366f1);
      font-weight: 600;
      font-size: 0.62rem;
      flex-shrink: 0;
      letter-spacing: 0.02em;
    }
    .pp-info { flex: 1; min-width: 0; }
    .pp-name {
      font-weight: 600;
      font-size: 0.82rem;
      color: var(--text-primary);
    }
    .pp-title {
      font-size: 0.72rem;
      color: var(--text-muted);
    }
    .pp-link {
      font-size: 0.68rem;
      color: var(--secondary);
      text-decoration: none;
      transition: color 0.15s ease;
      flex-shrink: 0;
    }
    .pp-link:hover { color: var(--text-primary); text-decoration: underline; }
    .slot-tag {
      font-size: 0.55rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 0.1rem 0.4rem;
      border-radius: var(--radius-pill);
    }
    .slot-tag.potential-fit { background: var(--brand-primary-soft, rgba(99,102,241,0.1)); color: var(--brand-primary, #6366f1); }
    .slot-tag.confirmed-tag { background: var(--success-soft); color: var(--success); }

    /* === Collapsible Table Cards (individual items) === */
    details.table-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      margin-bottom: 0.75rem;
      overflow: hidden;
    }
    details.table-card > summary {
      padding: 0.7rem 0.9rem;
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--text-primary);
      cursor: pointer;
      list-style: none;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    details.table-card > summary::-webkit-details-marker { display: none; }
    details.table-card > summary::before {
      content: "\25B6";
      font-size: 0.5em;
      color: var(--brand-primary);
      transition: transform 0.2s ease;
      flex-shrink: 0;
    }
    details.table-card[open] > summary::before { transform: rotate(90deg); }
    details.table-card > .context-grid {
      border-radius: 0;
      border: none;
      border-top: 1px solid var(--border);
    }
    details.table-card > .cc-questions {
      padding: 0.5rem 0.9rem 0.7rem;
      border-top: 1px solid var(--border);
    }

    /* === Status Tags (inside table-card rows) === */
    .cc-status {
      font-size: 0.6rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 0.15rem 0.5rem;
      border-radius: var(--radius-pill);
      flex-shrink: 0;
      white-space: nowrap;
    }
    .cc-status.unexplored { background: var(--warning-soft); color: var(--warning); }
    .cc-status.raised { background: var(--brand-primary-soft); color: var(--brand-primary); }
    .cc-status.validated { background: var(--success-soft); color: var(--success); }
    .cc-status.needs-reinforcement { background: rgba(124,108,255,0.12); color: var(--secondary); }
    .cc-status.expected { background: var(--warning-soft); color: var(--warning); }

    /* === Response List (inside objection table-cards) === */
    .response-list {
      list-style: none;
      padding: 0;
      margin: 0;
    }
    .response-list li {
      font-size: 0.85rem;
      color: var(--text-secondary);
      padding: 0.2rem 0;
      padding-left: 1rem;
      position: relative;
      line-height: 1.5;
    }
    .response-list li::before {
      content: "\2192";
      position: absolute;
      left: 0;
      color: var(--brand-primary);
      font-size: 0.8rem;
    }
    .response-list li strong { color: var(--text-primary); }

    /* === Discovery Questions (collapsible, inside table-cards) === */
    .cc-questions { margin-top: 0.5rem; }
    details.cc-questions > summary {
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--brand-primary);
      cursor: pointer;
      list-style: none;
      padding: 0.3rem 0;
    }
    details.cc-questions > summary::-webkit-details-marker { display: none; }
    details.cc-questions > summary::before {
      content: "+";
      font-weight: 700;
      color: var(--brand-primary);
      margin-right: 0.35rem;
      font-size: 0.7rem;
    }
    details.cc-questions[open] > summary::before { content: "\2212"; }
    .cc-q-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0;
      margin-top: 0.4rem;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow: hidden;
    }
    .cc-q-row { display: contents; }
    .cc-q-cell {
      padding: 0.3rem 0.55rem;
      font-size: 0.7rem;
      color: var(--text-secondary);
      line-height: 1.4;
      border-bottom: 1px solid var(--border);
    }
    .cc-q-cell:nth-child(odd) { background: var(--bg-elevated); }
    .cc-q-row:last-child .cc-q-cell { border-bottom: none; }
    .cc-q-header {
      font-size: 0.55rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      padding: 0.25rem 0.55rem;
      background: var(--bg-elevated);
      border-bottom: 1px solid var(--border);
    }

    /* === The Takeaway (featured) === */
    .the-takeaway {
      text-align: center;
      padding: 2.5rem 2rem;
      border: 2px solid var(--brand-primary);
      border-radius: var(--radius-lg);
      margin-top: 1rem;
    }
    .the-takeaway blockquote {
      font-family: var(--font-display);
      font-size: clamp(1.15rem, 2.5vw, 1.5rem);
      font-weight: 500;
      font-style: italic;
      color: var(--text-primary);
      line-height: 1.5;
    }

    /* === Grid Utilities === */
    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem; }

    /* === Brand Header (only when brand kit is active) === */
    .brand-header {
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(8,9,10,0.85);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      padding: 0 clamp(1rem, 4vw, 3rem);
    }
    .brand-header-inner {
      max-width: 900px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 48px;
    }
    .brand-header-logo {
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--text-primary);
      text-decoration: none;
    }
    .brand-header-logo svg { width: 18px; height: 18px; }
    .brand-header-logo span {
      font-family: var(--font-display);
      font-weight: 600;
      font-size: 0.9rem;
      letter-spacing: -0.01em;
    }
    .brand-header-right {
      display: flex;
      align-items: center;
      gap: 1rem;
      font-size: 0.78rem;
      color: var(--text-muted);
    }
    .brand-header-tag {
      font-size: 0.6rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--brand-primary);
      background: var(--brand-primary-soft);
      padding: 0.15rem 0.5rem;
      border-radius: var(--radius-pill);
    }

    /* === What's Happening Now (deep research conditional) === */
    .macro-themes { display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: 1rem; }
    .macro-theme {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-left: 3px solid var(--brand-primary);
      border-radius: var(--radius-lg);
      padding: 0.85rem 1rem;
    }
    .mt-title {
      font-family: var(--font-display);
      font-size: 0.92rem;
      font-weight: 600;
      color: var(--text-primary);
      margin-bottom: 0.3rem;
    }
    .mt-body {
      font-size: 0.82rem;
      color: var(--text-secondary);
      line-height: 1.55;
    }
    .signal-feed { display: flex; flex-direction: column; gap: 0; }
    .signal-item {
      display: grid;
      grid-template-columns: 90px 1fr;
      gap: 0.75rem;
      padding: 0.55rem 0;
      border-bottom: 1px solid var(--border);
    }
    .signal-item:last-child { border-bottom: none; }
    .signal-date {
      font-size: 0.68rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-muted);
      padding-top: 0.1rem;
    }
    .signal-headline {
      font-size: 0.84rem;
      font-weight: 500;
      color: var(--text-primary);
      line-height: 1.4;
    }
    .signal-relevance {
      font-size: 0.76rem;
      color: var(--text-muted);
      font-style: italic;
      line-height: 1.4;
      margin-top: 0.15rem;
    }

    /* === Deal Timeline === */
    .deal-timeline {
      margin-top: 1rem;
      padding: 0.75rem 0;
      overflow-x: auto;
    }
    .tl-track {
      display: flex;
      align-items: flex-start;
      gap: 0;
      min-width: max-content;
      padding: 0 0.5rem;
    }
    .tl-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      min-width: 100px;
      position: relative;
      padding: 0 0.5rem;
    }
    .tl-item::before {
      content: "";
      position: absolute;
      top: 5px;
      left: 0;
      right: 0;
      height: 2px;
      background: var(--border-strong);
    }
    .tl-item:first-child::before { left: 50%; }
    .tl-item:last-child::before { right: 50%; }
    .tl-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--text-muted);
      border: 2px solid var(--bg);
      position: relative;
      z-index: 1;
      flex-shrink: 0;
    }
    .tl-dot.active { background: var(--brand-primary); box-shadow: 0 0 0 3px var(--brand-primary-soft); }
    .tl-date {
      font-size: 0.62rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-muted);
      margin-top: 0.4rem;
      white-space: nowrap;
    }
    .tl-label {
      font-size: 0.72rem;
      color: var(--text-secondary);
      text-align: center;
      margin-top: 0.2rem;
      max-width: 120px;
      line-height: 1.35;
    }
    .tl-item.current .tl-date { color: var(--brand-primary); }
    .tl-item.current .tl-label { color: var(--text-primary); font-weight: 500; }
    .tl-gap {
      display: flex;
      flex-direction: column;
      align-items: center;
      min-width: 80px;
      position: relative;
      padding: 0 0.25rem;
    }
    .tl-gap::before {
      content: "";
      position: absolute;
      top: 5px;
      left: 0;
      right: 0;
      height: 2px;
      background: repeating-linear-gradient(90deg, var(--text-muted) 0, var(--text-muted) 4px, transparent 4px, transparent 8px);
      opacity: 0.4;
    }
    .tl-gap-line { height: 12px; } /* spacer to align with dots */
    .tl-gap-label {
      font-size: 0.62rem;
      color: var(--warning);
      font-style: italic;
      white-space: nowrap;
      margin-top: 0.4rem;
    }
    @media (max-width: 768px) {
      .tl-track { flex-direction: column; min-width: unset; align-items: flex-start; padding-left: 1.5rem; }
      .tl-item, .tl-gap { flex-direction: row; align-items: center; min-width: unset; padding: 0.4rem 0; gap: 0.75rem; }
      .tl-item::before { top: 0; bottom: 0; left: -1rem; right: unset; width: 2px; height: auto; }
      .tl-item:first-child::before { top: 50%; left: -1rem; }
      .tl-item:last-child::before { bottom: 50%; left: -1rem; }
      .tl-gap::before { top: 0; bottom: 0; left: -1rem; right: unset; width: 2px; height: auto;
        background: repeating-linear-gradient(180deg, var(--text-muted) 0, var(--text-muted) 4px, transparent 4px, transparent 8px); }
      .tl-dot { position: absolute; left: -1.35rem; }
      .tl-label { text-align: left; max-width: none; }
      .tl-gap-line { display: none; }
    }

    /* === Brand Footer === */
    .brand-footer {
      border-top: 1px solid var(--border);
      padding: 1.5rem clamp(1rem, 4vw, 3rem);
      margin-top: 2rem;
    }
    .brand-footer-inner {
      max-width: 900px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .brand-footer-logo {
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--text-muted);
    }
    .brand-footer-logo svg { width: 14px; height: 14px; }
    .brand-footer-logo span {
      font-family: var(--font-display);
      font-weight: 600;
      font-size: 0.78rem;
    }
    .brand-footer-meta {
      font-size: 0.68rem;
      color: var(--text-muted);
    }

    /* === Tabs (persona shifts + objection themes) === */
    .tab-bar { display: flex; gap: 4px; overflow-x: auto; padding: 0.3rem 0; margin-bottom: 0.75rem; }
    .tab-btn { font-size: 0.65rem; font-weight: 600; padding: 0.3rem 0.7rem; border-radius: var(--radius-pill);
               border: 1px solid var(--border); background: transparent; color: var(--text-secondary); cursor: pointer;
               font-family: var(--font-body); white-space: nowrap; transition: all 0.15s ease; }
    .tab-btn:hover { border-color: var(--brand-primary); color: var(--text-primary); }
    .tab-btn.active { background: var(--brand-primary-soft); color: var(--brand-primary); border-color: var(--brand-primary); }
    .tab-panel { display: none; }
    .tab-panel.active { display: block; }

    /* === Persona Tags (objection cards) === */
    .persona-tag { font-size: 0.55rem; font-weight: 600; padding: 0.1rem 0.4rem; border-radius: var(--radius-pill);
                   background: var(--bg-elevated); color: var(--text-secondary); margin-left: 0.3rem; }

    /* === Watch Out rows === */
    .cg-watchout { color: var(--text-muted); font-style: italic; font-size: 0.82rem; }

    /* === Persona Hero === */
    .persona-hero {
      padding: 0.35rem 1rem 0.45rem;
      font-size: 0.75rem;
      color: var(--brand-primary);
      font-weight: 500;
      line-height: 1.4;
      border-bottom: 1px solid var(--border);
      background: var(--brand-primary-soft);
    }

    /* === Positioning Directive === */
    .positioning-directive {
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      overflow: hidden;
      margin-bottom: 1.25rem;
    }
    .pd-row {
      display: grid;
      grid-template-columns: 140px 1fr;
      border-bottom: 1px solid var(--border);
    }
    .pd-row:last-child { border-bottom: none; }
    .pd-label {
      font-size: 0.72rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--brand-primary);
      padding: 0.6rem 0.9rem;
      background: var(--bg-elevated);
      display: flex;
      align-items: flex-start;
      padding-top: 0.7rem;
    }
    .pd-value {
      font-size: 0.85rem;
      color: var(--text-secondary);
      padding: 0.6rem 0.9rem;
      line-height: 1.5;
    }

    /* === Print === */
    @media print {
      .prep-nav, .brand-header, .brand-footer { display: none; }
      .prep-container { max-width: 100%; padding: 1rem; }
      details.prep-section[open] { break-inside: avoid; }
      .card, .table-card { break-inside: avoid; }
      body { color: #111; background: white; font-size: 12px; }
      .meeting-badge { border: 1px solid #111; background: transparent; color: #111; }
      .snapshot-bar { background: #f5f5f5; border: 1px solid #ddd; }
    }

    /* === Responsive === */
    @media (max-width: 768px) {
      .grid-2, .cc-q-grid { grid-template-columns: 1fr; }
      .snapshot-bar { grid-template-columns: repeat(2, 1fr); }
      .prep-nav { display: none; }
      .tab-bar { flex-wrap: wrap; }
    }

    @media (prefers-reduced-motion: reduce) {
      * { transition: none !important; animation: none !important; }
    }
  </style>
</head>
<body>

  <!-- REQUIRED when using a brand kit. Read the logo SVG from ~/.octave/brands/<slug>/ and inline it. -->
  <header class="brand-header">
    <div class="brand-header-inner">
      <a class="brand-header-logo" href="https://[domain]" target="_blank">
        <!-- Inline the real SVG logo from the brand kit here -->
        <span>[Company Name]</span>
      </a>
      <div class="brand-header-right">
        <span class="brand-header-tag">Meeting Prep</span>
      </div>
    </div>
  </header>

  <!-- Sidebar Navigation Dots -->
  <nav class="prep-nav" id="prep-nav"></nav>

  <!-- Main Prep Document -->
  <main class="prep-container">

    <!-- Header -->
    <header class="prep-header">
      <div class="header-badges">
        <span class="meeting-badge">[Meeting Type]</span>
        <span class="duration-badge">[Duration] min</span>
        <button class="expand-toggle" id="expand-toggle" onclick="toggleAll()">
          <span class="toggle-icon">&#9660;</span> Expand all
        </button>
      </div>
      <h1>Meeting Prep: [Company Name]</h1>
      <p class="header-subtitle">[One sentence describing the meeting context]</p>
      <p class="header-meta">[Date] · [Attendees]</p>
    </header>

    <!-- Deal Snapshot Bar -->
    <div class="snapshot-bar">
      <div class="snapshot-item">
        <span class="snapshot-label">Deal Value</span>
        <span class="snapshot-value">[value or TBD]</span>
      </div>
      <div class="snapshot-item">
        <span class="snapshot-label">Stage</span>
        <span class="snapshot-value">[stage]</span>
      </div>
      <div class="snapshot-item">
        <span class="snapshot-label">Target Close</span>
        <span class="snapshot-value">[date or TBD]</span>
      </div>
      <div class="snapshot-item">
        <span class="snapshot-label">Primary Contact</span>
        <span class="snapshot-value">[name, title]</span>
      </div>
    </div>

    <!-- Section 1: Context -->
    <details class="prep-section" open id="context">
      <summary>1. Context</summary>
      <p class="section-intro">Everything you need to know about the account, the people, and the deal going into this call.</p>

      <details class="card-group" open>
        <summary>Company Context</summary>
        <div class="company-identity">
          <img src="[logo_url]" alt="[Company]" class="company-logo">
          <span class="company-name">[Company]</span>
        </div>
        <div class="context-grid">
          <!-- cg-row elements: What they do, Scale, Why they're a fit, Key signal, Angle -->
        </div>
      </details>

      <!-- What's Happening Now (CONDITIONAL — only when deep research was run) -->
      <details class="card-group" open>
        <summary>What's Happening Now</summary>
        <p class="card-group-intro">Macro themes and recent signals from deep research — what a rep would find googling [Company] right now.</p>
        <div class="macro-themes">
          <!-- macro-theme elements: mt-title + mt-body -->
        </div>
        <div class="signal-feed">
          <!-- signal-item elements: signal-date + signal-body (signal-headline + signal-relevance) -->
        </div>
      </details>

      <details class="card-group" open>
        <summary>People</summary>
        <p class="card-group-intro">[Context about attendees — confirmed or potential fits by persona]</p>
        <div class="people-grid">
          <!-- persona-group elements: persona header + why + persona-hero + people list -->
          <!-- Each persona-group includes:
               <div class="persona-hero">[One sentence: how our positioning makes this persona the hero in their org]</div>
          -->
        </div>
      </details>

      <details class="card-group" open>
        <summary>Deal Context</summary>
        <div class="context-grid">
          <!-- cg-row elements: Stage, Activity, Competition, Champion, Compelling Event, Buying Triggers -->
        </div>
        <!-- Deal Timeline (CONDITIONAL — only when event/finding data exists) -->
        <div class="deal-timeline">
          <div class="tl-track">
            <!-- tl-item elements: tl-dot + tl-date + tl-label -->
            <!-- tl-gap elements: tl-gap-line + tl-gap-label (for periods of no activity) -->
          </div>
        </div>
      </details>
    </details>

    <!-- Section 2: Goals -->
    <details class="prep-section" open id="goals">
      <summary>2. Goals</summary>
      <p class="section-intro">What we need to accomplish in this meeting — our positioning frame, what they need to recognize, and how we advance.</p>

      <h3 class="sub-section-title">Positioning Directive</h3>
      <div class="positioning-directive">
        <div class="pd-row">
          <div class="pd-label">Position us as</div>
          <div class="pd-value">[one line — the frame]</div>
        </div>
        <div class="pd-row">
          <div class="pd-label">Mitigate</div>
          <div class="pd-value">[the risk to neutralize]</div>
        </div>
        <div class="pd-row">
          <div class="pd-label">Advance</div>
          <div class="pd-value">[the next step or commitment]</div>
        </div>
      </div>

      <details class="card-group" open>
        <summary>What We Need Them to Recognize</summary>
        <p class="card-group-intro">[Intro explaining the recognition group]</p>
        <!-- table-card elements (recognition cards with Watch out rows) -->
      </details>
    </details>

    <!-- Section 3: What to Say & Ask -->
    <details class="prep-section" open id="what-to-say">
      <summary>3. What to Say & Ask</summary>
      <p class="section-intro">The playbook for the room — how our message lands by persona, where we stand competitively, pains we know they have, and themes to steer.</p>

      <!-- How Our Message Lands by Persona (tabbed) -->
      <details class="card-group" open>
        <summary>How Our Message Lands by Persona</summary>
        <p class="card-group-intro">[Intro about persona shifts]</p>
        <div class="tab-bar">
          <!-- tab buttons -->
        </div>
        <div id="persona-tabs">
          <!-- tab-panel elements with persona context grids -->
        </div>
      </details>

      <!-- Competitive Position -->
      <details class="card-group" open>
        <summary>Competitive Position</summary>
        <p class="card-group-intro">[Intro about competitive angles]</p>
        <!-- table-card elements (competitive cards) -->
      </details>

      <!-- Pains We Know They Have -->
      <details class="card-group" open>
        <summary>Pains We Know They Have</summary>
        <p class="card-group-intro">[Intro — confident posture]</p>
        <!-- table-card elements (pain cards with Watch out rows) -->
      </details>

      <!-- Themes to Steer -->
      <details class="card-group" open>
        <summary>Themes to Steer</summary>
        <p class="card-group-intro">[Intro about steering themes]</p>
        <!-- table-card elements (theme cards with "How to steer" rows) -->
      </details>
    </details>

    <!-- Section 4: Objections -->
    <details class="prep-section" open id="objections">
      <summary>4. Objections</summary>
      <p class="section-intro">Pushback we expect, organized by theme. Have your responses sharp — and know what NOT to say.</p>

      <div class="tab-bar">
        <!-- theme tab buttons -->
      </div>
      <div id="objection-tabs">
        <!-- tab-panel elements with objection table-cards -->
      </div>
    </details>

    <!-- Section 5: The Takeaway -->
    <section class="prep-section" id="the-takeaway">
      <h2 style="font-family:var(--font-display);font-size:clamp(1.1rem,2vw,1.35rem);font-weight:600;padding:0.75rem 0;">5. The Takeaway</h2>
      <p class="section-intro">If you remember nothing else, remember this.</p>
      <div class="the-takeaway">
        <blockquote>[One memorable sentence]</blockquote>
      </div>
    </section>

  </main>

  <script>
    // Generate nav dots from section IDs
    const nav = document.getElementById('prep-nav');
    const sectionIds = ['context', 'goals', 'what-to-say', 'objections', 'the-takeaway'];
    sectionIds.forEach(id => {
      const a = document.createElement('a');
      a.href = '#' + id;
      a.dataset.section = id;
      nav.appendChild(a);
    });

    // Intersection Observer for active section tracking
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          document.querySelectorAll('.prep-nav a').forEach(a => a.classList.remove('active'));
          const dot = document.querySelector(`.prep-nav a[data-section="${entry.target.id}"]`);
          if (dot) dot.classList.add('active');
        }
      });
    }, { threshold: 0.3 });

    sectionIds.forEach(id => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });

    // Open all details on print
    window.onbeforeprint = () => {
      document.querySelectorAll('details').forEach(d => d.open = true);
    };

    // Expand/Collapse All toggle
    let allExpanded = false;
    function toggleAll() {
      allExpanded = !allExpanded;
      document.querySelectorAll('details').forEach(d => d.open = allExpanded);
      const btn = document.getElementById('expand-toggle');
      btn.innerHTML = allExpanded
        ? '<span class="toggle-icon">&#9650;</span> Collapse all'
        : '<span class="toggle-icon">&#9660;</span> Expand all';
    }

    function switchTab(btn, containerId) {
      const container = document.getElementById(containerId);
      const bar = btn.parentElement;
      bar.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const index = Array.from(bar.children).indexOf(btn);
      container.querySelectorAll('.tab-panel').forEach((p, i) => {
        p.classList.toggle('active', i === index);
      });
    }
  </script>

  <!-- REQUIRED when using a brand kit. Same logo as header, smaller. -->
  <footer class="brand-footer">
    <div class="brand-footer-inner">
      <div class="brand-footer-logo">
        <!-- Inline the real SVG logo from the brand kit here -->
        <span>[Company Name]</span>
      </div>
      <div class="brand-footer-meta">Prepared [Date]</div>
    </div>
  </footer>

</body>
</html>
```

**Self-contained:** Inline CSS, zero external dependencies (except Google Fonts / brand kit webfonts). No JavaScript frameworks.

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
- `get_playbook` — Retrieve a playbook with full content and value props
- `list_value_props` — Value propositions for a specific playbook

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

**No Matching Playbook:**
> No playbook matches this audience profile directly.
>
> I'll use general value props and positioning from the knowledge base, combined with coaching frameworks. Consider creating a playbook for this segment: `/octave:library create playbook`

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
