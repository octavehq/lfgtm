---
name: brief
description: Account dossier and call prep document rendered as a scannable HTML reference page for internal use. Use when user says "brief me on [company]", "account dossier", "call prep doc", "background on [person]", or asks for an internal reference document. Do NOT use for customer-facing documents — use /octave:one-pager or /octave:proposal instead.
---

# /octave:brief - Account Dossier & Call Prep Builder

Build beautiful, self-contained HTML account briefs powered by your Octave GTM intelligence. Designed to sit on your second monitor during a call or to review before a meeting. Unlike plain-text research, briefs render as scannable, styled reference documents with sticky navigation, collapsible sections, and print-friendly layout — grounded in real enrichment data, playbook strategy, proof points, and conversation intel.

This is an **internal** document for the sales team, not customer-facing collateral.

**Key differentiators:**
- vs `/octave:research` — research outputs plain text; brief renders it as a styled, scannable HTML document
- vs `/octave:one-pager` — one-pager is customer-facing; brief is internal prep
- vs `/octave:deck` — deck is a slide presentation; brief is a scrollable reference document

## Usage

```
/octave:brief <target> [--for <occasion>] [--style <preset>]
```

## Examples

```
/octave:brief acme.com                                # Full account dossier
/octave:brief jane@acme.com --for discovery           # Discovery call prep
/octave:brief acme.com --for demo                     # Demo prep brief
/octave:brief acme.com --for qbr                      # QBR prep brief
/octave:brief jane@acme.com --for follow-up           # Follow-up with prior call context
/octave:brief acme.com --for executive                # Executive meeting prep
/octave:brief "meeting with VP Sales at Acme"         # Context-based brief
/octave:brief acme.com --style paper-minimal          # Specific style preset
```

## Occasions

| Occasion | Output Focus |
|----------|--------------|
| `discovery` | Company snapshot, ICP fit, discovery questions, playbook strategy, qualification checklist |
| `demo` | Stakeholder cards, value props, proof points, competitive landmines, demo flow |
| `follow-up` | Recent signals from calls, deal timeline, open items, next steps |
| `qbr` | Deal timeline, recent signals, proof points, value delivered, renewal/expansion angles |
| `executive` | Concise company snapshot, key stakeholders, strategic value props, board-level talking points |
| `deal-review` | Full pipeline context, stage history, competitive landscape, risk assessment |
| `general` | Comprehensive account dossier with all sections (default) |

## Instructions

When the user runs `/octave:brief`:

### Step 1: Understand the Context

**Identify the target:**
- Email address -> Person-targeted brief (enrich person + company)
- Domain -> Company-targeted brief (enrich company + find key contacts)
- LinkedIn URL -> Person-targeted brief
- Meeting description -> Extract company/people from context

**Detect or ask occasion:**

If `--for` not specified, infer from context or ask:

```
What are you preparing for?

1. Discovery call — First conversation, qualifying the opportunity
2. Demo — Showing the product, proving value
3. Follow-up — Continuing a conversation, advancing the deal
4. QBR — Quarterly business review with existing customer
5. Executive meeting — High-level strategic conversation
6. Deal review — Internal review of opportunity status
7. General dossier — Comprehensive account reference

Your choice:
```

Each occasion changes which sections are emphasized and which are de-emphasized or omitted. See the section emphasis table in Step 4.

### Step 2: Octave Context Gathering

Based on the target and occasion, use Octave MCP tools to build a complete intelligence picture. **Tell the user what you're researching and why.**

**Call as many tools as needed to build a thorough brief.** The best briefs layer multiple sources — company enrichment + person enrichment + playbook messaging + proof points + conversation intel all combine to create a document grounded in real data. Don't stop at one tool when several would give you a stronger brief.

Not every tool applies to every brief. Use your judgment about which are relevant to *this specific* situation. The tables below show what's available — pick the combination that gives you the richest context for the occasion and target.

**List vs Search — when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_all_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory — "show me all our competitors" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content — "get full proof point details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept or question — "how do we position for healthcare?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material, uploaded assets, or source docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

**Follow-up briefs — ground them in what actually happened:**

If this brief follows a previous interaction with the account (follow-up, QBR, deal review), pull findings and events to anchor the brief in real data rather than generic positioning:

- `list_findings({ query: "<company or contact>", startDate: "<relevant period>" })` — surfaces what was actually said in calls: objections raised, features requested, pain points confirmed, competitor mentions
- `list_events({ filters: { accounts: ["<account_oId>"] } })` — deal stage changes, meetings held, emails sent — shows the journey so far
- `get_event_detail({ eventOId })` — deep dive on specific events (e.g., the discovery call, the demo) to pull exact context

This turns a generic "here's what we know" brief into "here's what happened and what to do about it" — much more useful walking into the next conversation.

---

#### For Person-Targeted Briefs

Start with person and company enrichment, then pull positioning context:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Person deep-dive | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | Always for person-targeted briefs — gives background, role, priorities |
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

---

#### For Company-Targeted Briefs

Start with company enrichment and contact discovery:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Company profile | `enrich_company({ companyDomain })` | Always — gives industry, size, tech stack, funding, signals |
| ICP fit scoring | `qualify_company({ companyDomain })` | Always — segment match, fit score, fit reasons |
| Key contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | Find stakeholders to populate the Stakeholders section |
| Enrich contacts | `enrich_person({ person: { ... } })` | Deep dive on each key contact found |
| All playbooks | `list_all_entities({ entityType: "playbook" })` | Quick scan to find the right strategic approach |
| Playbook details | `get_playbook({ oId, includeValueProps: true })` | Full content + value props for the matching playbook |
| Value props | `list_value_props({ playbookOId })` | Fetch value props for the recommended playbook |
| All competitors | `list_all_entities({ entityType: "competitor" })` | Quick scan of competitive landscape |
| Competitor details | `get_entity({ oId })` | Deep dive on a specific relevant competitor |
| Proof points | `list_entities({ entityType: "proof_point" })` | Full proof points for the evidence section |
| References | `list_entities({ entityType: "reference" })` | Customer references for social proof |
| Topic search | `search_knowledge_base({ query: "<industry> <use case>", entityTypes: ["proof_point", "reference"] })` | Find proof points relevant to their specific situation |
| Recent intel | `list_findings({ query: "<company>", startDate: "<90 days ago>" })` | Conversation signals from calls and meetings |
| Deal events | `list_events({ filters: { accounts: ["<account_oId>"] } })` | Full deal history and timeline |
| Event details | `get_event_detail({ eventOId })` | Deep dive on specific past interactions |
| Uploaded resources | `search_resources({ query: "<company or industry>" })` | Relevant uploaded docs and assets |

---

**Output of this step:** Present a content outline to the user for approval before generating:

```
BRIEF OUTLINE: [Company/Person] — [Occasion]
=============================================

Target: [Company name / Person name at Company]
Occasion: [Discovery / Demo / Follow-up / QBR / Executive / General]
Style: [Will be selected in Step 3]

---

SECTIONS TO INCLUDE
-------------------

1. Header — "Account Brief: [Company]" + date + occasion badge
2. Company Snapshot — industry, size, HQ, funding, tech stack, signals
3. ICP Fit — fit score, matched segment, key fit reasons
4. Key Stakeholders — [N] contacts with persona matches
5. Recommended Playbook — [Playbook name], strategic angle
6. Talking Points — [occasion-specific: questions / demo flow / next steps]
7. Value Props — [N] value props tailored to this account
8. Competitive Landscape — [Competitor names if detected]
9. Proof Points — [N] relevant case studies and metrics
10. Recent Signals — [N] findings from conversations
11. Deal Timeline — [if existing deal]
12. Quick Reference — cheat sheet with key facts

Octave Sources Used:
• Company enrichment: [Company] — [key insights]
• Person enrichment: [Person] — [persona match]
• Playbook: [Playbook name] — [strategic angle]
• Proof points: [N] references pulled
• Findings: [N] recent signals
• Competitive: [If applicable]

---

Does this look good? I can:
1. Proceed to style selection and generation
2. Add or remove sections
3. Go deeper on any area
4. Change the occasion / emphasis
```

**Wait for user approval before proceeding.**

### Step 3: Style Selection

The brief uses the same CSS variable / style preset system as `/octave:deck`. Full preset definitions are in the deck skill's [STYLE_PRESETS.md](../deck/STYLE_PRESETS.md).

Briefs default to readability-optimized presets. If `--style` was not provided, ask:

```
Pick a style for your brief:

1. midnight-pro     — Dark navy, white text, blue accents (default for briefs)
2. paper-minimal    — Off-white, black type, editorial simplicity
3. executive-dark   — Charcoal + gold, premium boardroom aesthetic
4. soft-light       — Warm white + sage green, calm and approachable
5. swiss-modern     — White + red accent, Bauhaus minimal
6. Use my brand     — Extract from website or provide colors
7. Match my deck    — Use the same style as an existing /octave:deck

Your choice (or press Enter for midnight-pro):
```

| Occasion | Recommended Default |
|----------|-------------------|
| Discovery | `midnight-pro` |
| Demo | `midnight-pro` |
| Follow-up | `paper-minimal` |
| QBR | `executive-dark` |
| Executive | `executive-dark` |
| Deal review | `paper-minimal` |
| General | `midnight-pro` |

If the user selects "Use my brand," follow the brand discovery flow from the deck skill (website extraction via browser-use or WebFetch, manual fallback). If they select "Match my deck," ask for the deck file path and extract its CSS variables.

### Step 4: Generate HTML

Build a single self-contained HTML file. The brief is a scrollable reference document — not a slide deck. Natural page scroll, sticky sidebar navigation, collapsible sections, and a print-friendly layout.

#### Output Directory

```
.octave-briefs/
└── <kebab-case-name>-<YYYY-MM-DD>/
    └── <name>.html
```

Example: `/octave:brief acme.com --for discovery` -> `.octave-briefs/acme-discovery-2026-02-11/acme-discovery.html`

The `.octave-briefs/` directory should be in `.gitignore`.

#### Document Sections (Full Dossier)

Not all sections appear in every brief. The occasion determines emphasis:

| Occasion | Emphasized Sections | De-emphasized / Omitted |
|----------|-------------------|-------------------------|
| Discovery | Company Snapshot, ICP Fit, Talking Points (questions), Playbook, Qualification | Deal Timeline, Competitive |
| Demo | Stakeholders, Value Props, Proof Points, Competitive, Demo Flow | ICP Fit detail |
| Follow-up | Recent Signals, Deal Timeline, Talking Points (next steps), Open Items | Company Snapshot (condensed) |
| QBR | Deal Timeline, Recent Signals, Proof Points, Value Delivered | ICP Fit, Playbook |
| Executive | Company Snapshot (concise), Key Stakeholders, Value Props, Strategic Angles | Technical details, granular signals |
| Deal Review | Deal Timeline, Competitive, Risk Assessment, Stakeholder Map, Next Steps | Company Snapshot (condensed) |
| General | All sections at equal weight | None |

**Section definitions:**

1. **Header** — "Account Brief: [Company]" + generation date + occasion badge (pill label like "Discovery Prep" or "QBR Brief")
2. **Company Snapshot** — Company name, logo (if available), industry, employee count, HQ location, funding stage, tech stack highlights, recent news/signals. Card-based layout.
3. **ICP Fit** — Fit score with a visual progress bar, matched segment name, 3-5 key fit reasons as checkmarks, any red flags as warnings.
4. **Key Stakeholders** — Cards for each person: name, title, LinkedIn URL, matched persona, inferred priorities, communication style notes. Highlight the primary contact.
5. **Recommended Playbook** — Playbook name, strategic angle, key themes to drive. Brief summary of the recommended approach.
6. **Talking Points** — Occasion-specific content:
   - Discovery: open-ended questions organized by category (rapport, pain exploration, qualification, future state)
   - Demo: recommended flow, features to highlight, proof points to weave in
   - Follow-up: recap of what was discussed, open items, proposed next steps
   - QBR: value delivered, metrics to highlight, expansion opportunities
   - Executive: strategic themes, board-level talking points, concise value narrative
7. **Value Props to Lead With** — 3-4 value props tailored to this account, each with a headline, supporting evidence, and a "say this" phrasing.
8. **Competitive Landscape** — If competitors detected: comparison table with key differentiators, landmine questions to ask, traps to avoid. Omit if no competitive signals.
9. **Proof Points to Reference** — Relevant case studies with metric highlights, customer quotes, and logo. Organized by relevance to this account's industry/size/use case.
10. **Recent Signals** — From findings: what was said in calls, objections raised, features requested, sentiment indicators. Each signal has a date and source. Omit if no findings data.
11. **Deal Timeline** — If existing deal: visual stage history (horizontal timeline or vertical step list), key events, current stage, days in stage, next milestone. Omit for new prospects.
12. **Quick Reference** — Sticky sidebar or footer cheat sheet: key facts at a glance, do's and don'ts for this conversation, one-line reminders. Always visible while scrolling.

#### HTML Architecture

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Account Brief: [Company] — [Occasion]</title>
  <!-- Google Fonts (preconnect + stylesheet) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* === CSS Variables (from chosen preset) === */
    :root { ... }

    /* === Reset & Base === */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      background: var(--bg);
      color: var(--text-primary);
      font-family: var(--font-body);
      line-height: 1.6;
    }

    /* === Layout === */
    .brief-container {
      max-width: 900px;
      margin: 0 auto;
      padding: 2rem clamp(1rem, 4vw, 3rem);
    }

    /* === Sidebar Navigation (sticky) === */
    .brief-nav {
      position: fixed;
      top: 50%;
      right: clamp(0.5rem, 2vw, 2rem);
      transform: translateY(-50%);
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      z-index: 100;
    }
    .brief-nav a {
      display: block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--text-muted);
      transition: all 0.3s ease;
    }
    .brief-nav a.active {
      background: var(--brand-primary);
      transform: scale(1.4);
    }

    /* === Section Styles === */
    .brief-section {
      margin-bottom: 2.5rem;
      padding-bottom: 2rem;
      border-bottom: 1px solid var(--border);
    }

    /* === Collapsible Sections (details/summary) === */
    details.brief-section {
      border-bottom: 1px solid var(--border);
      margin-bottom: 2.5rem;
      padding-bottom: 1rem;
    }
    details.brief-section summary {
      cursor: pointer;
      font-family: var(--font-display);
      font-size: clamp(1.1rem, 2vw, 1.4rem);
      font-weight: 600;
      color: var(--text-primary);
      padding: 0.75rem 0;
      list-style: none;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    details.brief-section summary::before {
      content: "\25B6";
      font-size: 0.7em;
      color: var(--brand-primary);
      transition: transform 0.2s ease;
    }
    details.brief-section[open] summary::before {
      transform: rotate(90deg);
    }

    /* === Cards === */
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: clamp(1rem, 2vw, 1.5rem);
    }
    .card:hover {
      background: var(--bg-card-hover);
    }

    /* === Stakeholder Cards === */
    .stakeholder-card {
      display: flex;
      gap: 1rem;
      align-items: flex-start;
    }
    .stakeholder-avatar {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: var(--brand-primary);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: 700;
      flex-shrink: 0;
    }

    /* === Fit Score Bar === */
    .fit-bar {
      height: 8px;
      border-radius: 4px;
      background: var(--bg-elevated);
      overflow: hidden;
      margin: 0.5rem 0;
    }
    .fit-bar-fill {
      height: 100%;
      border-radius: 4px;
      background: var(--success);
      transition: width 0.8s ease;
    }

    /* === Occasion Badge === */
    .occasion-badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: var(--radius-pill);
      background: var(--brand-primary);
      color: white;
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    /* === Timeline === */
    .timeline {
      position: relative;
      padding-left: 2rem;
    }
    .timeline::before {
      content: "";
      position: absolute;
      left: 0.5rem;
      top: 0;
      bottom: 0;
      width: 2px;
      background: var(--border-strong);
    }
    .timeline-event {
      position: relative;
      margin-bottom: 1.5rem;
      padding-left: 1rem;
    }
    .timeline-event::before {
      content: "";
      position: absolute;
      left: -1.75rem;
      top: 0.5rem;
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--brand-primary);
    }

    /* === Grid Utilities === */
    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: clamp(0.75rem, 1.5vw, 1.25rem); }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: clamp(0.75rem, 1.5vw, 1.25rem); }

    /* === Typography === */
    .section-title {
      font-family: var(--font-display);
      font-size: clamp(1.1rem, 2vw, 1.4rem);
      font-weight: 600;
      margin-bottom: 1rem;
    }
    .body-text { font-size: clamp(0.85rem, 1.2vw, 1rem); }
    .text-secondary { color: var(--text-secondary); }
    .text-muted { color: var(--text-muted); }

    /* === Quick Reference Sidebar === */
    @media (min-width: 1200px) {
      .brief-layout {
        display: grid;
        grid-template-columns: 1fr 280px;
        gap: 2rem;
        max-width: 1200px;
        margin: 0 auto;
      }
      .quick-ref {
        position: sticky;
        top: 2rem;
        align-self: start;
        max-height: calc(100vh - 4rem);
        overflow-y: auto;
      }
    }
    @media (max-width: 1199px) {
      .quick-ref {
        margin-top: 2rem;
        border-top: 2px solid var(--border-strong);
        padding-top: 2rem;
      }
    }

    /* === Print Styles === */
    @media print {
      .brief-nav { display: none; }
      .brief-container { max-width: 100%; padding: 1rem; }
      details.brief-section { open; }
      details.brief-section[open] { break-inside: avoid; }
      .card { break-inside: avoid; }
      body { color: #111; background: white; }
      .occasion-badge { border: 1px solid #111; background: transparent; color: #111; }
    }

    /* === Responsive === */
    @media (max-width: 768px) {
      .grid-2, .grid-3 { grid-template-columns: 1fr; }
      .brief-nav { display: none; }
    }

    /* === prefers-reduced-motion === */
    @media (prefers-reduced-motion: reduce) {
      * { transition: none !important; animation: none !important; }
    }
  </style>
</head>
<body>

  <!-- Sidebar Navigation Dots -->
  <nav class="brief-nav" id="brief-nav">
    <!-- Generated by JS: one dot per section -->
  </nav>

  <!-- Main Brief -->
  <div class="brief-layout">
    <main class="brief-container">

      <!-- Header -->
      <header class="brief-header">
        <span class="occasion-badge">[Occasion] Prep</span>
        <h1>[Account Brief: Company Name]</h1>
        <p class="text-secondary">[Generated date] · [Target person if applicable]</p>
      </header>

      <!-- Sections (use <details> for collapsible, <section> for always-open) -->
      <details class="brief-section" open id="company-snapshot">
        <summary>Company Snapshot</summary>
        <div class="grid-2">
          <!-- Company info cards -->
        </div>
      </details>

      <details class="brief-section" open id="icp-fit">
        <summary>ICP Fit</summary>
        <!-- Fit score bar, segment match, fit reasons -->
      </details>

      <!-- Continue for each section... -->

    </main>

    <!-- Quick Reference Sidebar -->
    <aside class="quick-ref">
      <h3>Quick Reference</h3>
      <!-- Key facts, do's/don'ts, one-line reminders -->
    </aside>
  </div>

  <script>
    // Generate nav dots from sections
    // Intersection Observer for active section tracking
    // Smooth scroll on nav dot click
    // Open all details on print (window.onbeforeprint)
  </script>

</body>
</html>
```

**Self-contained:** Inline CSS, zero external dependencies (except Google Fonts). No JavaScript frameworks.

**Key differences from deck HTML:**
- No scroll-snap (natural page scrolling)
- No slide containers (continuous document flow)
- Collapsible sections via `<details>`/`<summary>` for quick scanning
- Sticky sidebar navigation instead of slide nav dots
- Optional sidebar for quick reference (on wide screens)
- Max-width 900px for comfortable reading
- Print-friendly with `@media print`

#### Content Density Guidelines

Briefs are reference documents, not presentations — they can hold more content per section than slides. But keep it scannable:

| Section | Content Limit |
|---------|--------------|
| Company Snapshot | 6-8 data fields in cards, 3-5 recent signals |
| ICP Fit | Score bar + 5 fit reasons max |
| Key Stakeholders | 4-6 stakeholder cards max |
| Talking Points | 8-12 talking points grouped by category |
| Value Props | 3-4 value props with evidence |
| Competitive | Comparison table with 4-6 rows max |
| Proof Points | 3-5 proof point cards |
| Recent Signals | 5-8 most relevant findings |
| Deal Timeline | 6-10 timeline events |
| Quick Reference | 8-12 key facts / reminders |

If a section would exceed its limit, prioritize by relevance to the occasion and trim the rest.

### Step 5: Delivery

After generating the HTML file:

1. **Open the brief** in the default browser
2. **Present a summary:**

```
BRIEF READY
============

Folder: .octave-briefs/<brief-name>-<date>/
File:   .octave-briefs/<brief-name>-<date>/<brief-name>.html
Style:  [Preset name or "Custom Brand"]
Sections: [List of included sections]

Navigation:
- Scroll naturally to read through sections
- Click nav dots on the right edge to jump to sections
- Click section headers to collapse/expand
- Print-friendly: Cmd+P / Ctrl+P for clean PDF output

---

Want me to:
1. Adjust or expand a section
2. Add/remove stakeholders
3. Go deeper on any topic (competitive, signals, value props)
4. Change the style
5. Export as PDF (print dialog)
6. Generate a customer-facing one-pager from this (/octave:one-pager)
7. Build a presentation from this (/octave:deck)
8. Done
```

## MCP Tools Used

### Research & Enrichment
- `enrich_company` — Full company intelligence profile
- `enrich_person` — Full person intelligence report
- `find_person` — Find contacts at a company by title/role
- `find_company` — Find companies matching criteria
- `qualify_company` — ICP fit scoring for a company
- `qualify_person` — ICP fit scoring for a person

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

## Error Handling

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The brief builder needs Octave data to generate useful content. Without it, most sections would be empty.
>
> To reconnect: check your MCP configuration or run `/octave:workspace status`

**Company Not Found:**
> I couldn't find detailed intelligence for [domain].
>
> Options:
> 1. Check the domain spelling and try again
> 2. Try a different domain or company name
> 3. Provide company details manually and I'll structure the brief

**Person Not Found:**
> I couldn't find detailed information for [email/name].
>
> I found their company ([Company]). Would you like me to:
> 1. Proceed with company research + generic persona guidance
> 2. Search for them on LinkedIn (provide URL)
> 3. Create a brief based on their title and company alone

**No Matching Playbook:**
> No playbook matches this audience profile directly.
>
> I'll use your general value props and positioning from the knowledge base. Consider creating a playbook for this segment: `/octave:library create playbook`

**No Findings Data:**
> No conversation signals found for [company/person].
>
> This may be a new prospect with no prior interactions. I'll skip the Recent Signals and Deal Timeline sections and focus on enrichment data, playbook strategy, and proof points instead.

**No Proof Points:**
> No proof points found in your library.
>
> The Proof Points section will be omitted. To strengthen future briefs, add case studies and customer references to your Octave library.

## Related Skills

- `/octave:research` — Text-based research and prep (brief is the visual, rendered version)
- `/octave:one-pager` — Customer-facing leave-behind document (brief is internal)
- `/octave:deck` — Full slide presentation (brief is a reference document)
- `/octave:battlecard-doc` — Competitive reference document (brief includes competitive context but is broader)
- `/octave:pipeline` — Deal-level coaching and pipeline strategy
- `/octave:generate` — Generate outreach content with brand voice control
- `/octave:insights` — Conversation intelligence deep dives
