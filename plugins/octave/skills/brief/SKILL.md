---
name: brief
description: Account dossier rendered as a scannable HTML reference page for internal use. Use when user says "brief me on [company]", "account dossier", "background on [person]", or asks for an internal reference document. Do NOT use for customer-facing documents — use /octave:one-pager or /octave:proposal instead — and for prep tuned to a specific upcoming meeting, use /octave:meeting-prep.
argument-hint: "<company-or-email> [--for <occasion>] [--style <preset>] [--research <deep|standard|fast>] [--skip-review]"
---

# /octave:brief - Account Dossier Builder

Build beautiful, self-contained HTML account briefs powered by your Octave GTM intelligence. Designed to sit on your second monitor during a call or to review before a meeting. Unlike plain-text research, briefs render as scannable, styled reference documents with sticky navigation, collapsible sections, and print-friendly layout — grounded in real enrichment data, Motion ICP narrative, proof points, and conversation intel.

This is an **internal** document for the sales team, not customer-facing collateral.

**Key differentiators:**
- vs `/octave:research` — research outputs plain text; brief renders it as a styled, scannable HTML document
- vs `/octave:one-pager` — one-pager is customer-facing; brief is internal
- vs `/octave:meeting-prep` — meeting-prep is coached prep for one specific conversation; brief is a static account reference
- vs `/octave:deck` — deck is a slide presentation; brief is a scrollable reference document

## On-brand styling — internal doc, so default to YOUR brand

A brief is an **internal reference doc**, so it should look like the **sender's own brand** (your workspace's company), not the target account's — don't ask whose brand. Resolve the sender with `get_workspace_company` and follow the kit lookup and defaults in [../shared/brand-kit-usage.md](../shared/brand-kit-usage.md). Respect an explicit `--style` or brand override.

## Review pass (runs by default)

Run the default review pass after generating — the always-on preflight plus the visual render-and-inspect pass, per [../shared/review-pass.md](../shared/review-pass.md). Opt out with `--skip-review`; the visual pass defaults off in a `--research fast` run. When generating, follow the output rules in [../shared/presentation-principles.md](../shared/presentation-principles.md).

## Usage

```
/octave:brief <target> [--for <occasion>] [--style <preset>] [--research <deep|standard|fast>] [--skip-review]
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
| `discovery` | Company snapshot, ICP fit, discovery questions, Motion ICP narrative, qualification checklist |
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

The research layers **live external web** (`deep_web_research`, `scrape_website`) + **Octave enrichment** + **the Octave library** (Motions / Motion ICP cells, proof points, references, competitors) + **CRM & conversation intel** (`list_events`, `list_findings`). The mix shifts by situation — a net-new prospect leans on web + enrichment + library; an existing account adds CRM/findings.

**Research depth — default: deep.** Run a deep pass by default; as you start, tell the user in one line and offer to dial down, then proceed:
> "Running a **deep** research pass for [Company] — live web + market/segment intel, the full Octave library, and CRM history. Want it faster? Say **standard** (recent company news only) or **fast** (Octave + CRM only, no live web)."

`deep` = all layers + broad `deep_web_research` (news + segment/market trends, 3-5 queries) · `standard` = all layers + focused news/macro themes (1-2 queries) · `fast` = Octave + CRM only, no live web. Honor `--research <deep|standard|fast>` or any in-line switch. **Bound it:** cap live web to the query budget, then start writing; silently skip layers with no data.

Based on the target and occasion, use Octave MCP tools to build a complete intelligence picture. **Tell the user what you're researching and why.**

**Call as many tools as needed to build a thorough brief.** The best briefs layer multiple sources — company enrichment + person enrichment + Motion ICP narrative + proof points + conversation intel all combine to create a document grounded in real data. Not every tool applies to every brief; pick the combination that gives you the richest context for the occasion and target:

- **List-vs-search guidance, follow-up grounding (findings/events), and the common tool tables:** [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md). If this brief follows a previous interaction (follow-up, QBR, deal review), use the follow-up-grounding tools there.
- **Person-targeted and company-targeted tool tables:** [references/tool-reference.md](references/tool-reference.md).

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
5. Recommended Motion & angle — [Motion / ICP cell], strategic angle
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
• Motion: [Motion / ICP cell] — [strategic angle]
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

The brief uses the same CSS variable / style preset system as the other document skills. Full preset definitions are in [../shared/style-presets.md](../shared/style-presets.md).

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

If the user selects "Use my brand," follow the brand extraction tiers in [../shared/brand-kit-usage.md](../shared/brand-kit-usage.md). If they select "Match my deck," ask for the deck file path and extract its CSS variables.

### Step 4: Generate HTML

Build a single self-contained HTML file. The brief is a scrollable reference document — not a slide deck. Natural page scroll, sticky sidebar navigation, collapsible sections, and a print-friendly layout.

#### Output Directory

```
.octave-briefs/
└── <kebab-case-name>-<YYYY-MM-DD>/
    └── <name>.html
```

Example: `/octave:brief acme.com --for discovery` -> `.octave-briefs/acme-discovery-2026-02-11/acme-discovery.html`

Make sure `.octave-briefs/` is ignored by your project's `.gitignore` (an `.octave-*/` pattern covers all Octave output dirs) so generated briefs don't get committed.

#### Document Sections (Full Dossier)

Not all sections appear in every brief. The occasion determines emphasis:

| Occasion | Emphasized Sections | De-emphasized / Omitted |
|----------|-------------------|-------------------------|
| Discovery | Company Snapshot, ICP Fit, Talking Points (questions), Recommended Motion, Qualification | Deal Timeline, Competitive |
| Demo | Stakeholders, Value Props, Proof Points, Competitive, Demo Flow | ICP Fit detail |
| Follow-up | Recent Signals, Deal Timeline, Talking Points (next steps), Open Items | Company Snapshot (condensed) |
| QBR | Deal Timeline, Recent Signals, Proof Points, Value Delivered | ICP Fit, Recommended Motion |
| Executive | Company Snapshot (concise), Key Stakeholders, Value Props, Strategic Angles | Technical details, granular signals |
| Deal Review | Deal Timeline, Competitive, Risk Assessment, Stakeholder Map, Next Steps | Company Snapshot (condensed) |
| General | All sections at equal weight | None |

**Section definitions:**

1. **Header** — "Account Brief: [Company]" + generation date + occasion badge (pill label like "Discovery Prep" or "QBR Brief")
2. **Company Snapshot** — Company name, logo (if available), industry, employee count, HQ location, funding stage, tech stack highlights, recent news/signals. Card-based layout.
3. **ICP Fit** — Fit score with a visual progress bar, matched segment name, 3-5 key fit reasons as checkmarks, any red flags as warnings. **Show the composite score *and* the breakdown** — see the `qualify_company` note in [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md): an account can be a strong *product* fit yet score low because it's out of the segment definition by size or model; say which, and frame the wedge rather than just flashing a red number.
4. **Key Stakeholders** — Cards for each person: name, title, LinkedIn URL, matched persona, inferred priorities, communication style notes. Highlight the primary contact.
5. **Recommended Motion & angle** — the matching Motion / Motion ICP cell (plus any Custom Motion Playbook that layers on it), the strategic angle, and key themes to drive. Brief summary of the recommended approach.
6. **Talking Points** — Occasion-specific content:
   - Discovery: open-ended questions organized by category (rapport, pain exploration, qualification, future state)
   - Demo: recommended flow, features to highlight, proof points to weave in
   - Follow-up: recap of what was discussed, open items, proposed next steps
   - QBR: value delivered, metrics to highlight, expansion opportunities
   - Executive: strategic themes, board-level talking points, concise value narrative
7. **Value Props to Lead With** — 3-4 value props tailored to this account, each with a headline, supporting evidence, and **how to frame it** (the point to make in your own words — not a script to read).
8. **Competitive Landscape** — If competitors detected: comparison table with key differentiators, landmine questions to ask, traps to avoid. Omit if no competitive signals.
9. **Proof Points to Reference** — Relevant case studies with metric highlights, customer quotes, and logo. Organized by relevance to this account's industry/size/use case.
10. **Recent Signals** — From findings: what was said in calls, objections raised, features requested, sentiment indicators. Each signal has a date and source. Omit if no findings data.
11. **Deal Timeline** — If existing deal: visual stage history (horizontal timeline or vertical step list), key events, current stage, days in stage, next milestone. Omit for new prospects.
12. **Quick Reference** — Sticky sidebar or footer cheat sheet: key facts at a glance, do's and don'ts for this conversation, one-line reminders. Always visible while scrolling.

#### HTML Architecture

Build on the shared scaffold in [../shared/doc-scaffold.md](../shared/doc-scaffold.md); brief-specific components (occasion badge, stakeholder cards, fit bar, timeline, quick-reference sidebar) are in [html-architecture.md](references/html-architecture.md).

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
- PDF (recommended): bash "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/export-pdf.sh .octave-briefs/<brief-name>-<date>/<brief-name>.html  — or Cmd+P / Ctrl+P -> Save as PDF

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

Common research, library, signals, and generation tools: see [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md). Brief-specific additions:

- `get_workspace_company` — Resolve the sender's own company for brand styling
- `deep_web_research` — Live web research for news and segment/market intel (deep/standard modes)
- `scrape_website` — Verified, linkable facts from the company's own site

## Error Handling

Standard responses (company/person not found, no matching Motion ICP cell, no findings, no proof points): see [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md) → Standard error handling. Brief-specific:

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The brief builder needs Octave data to generate useful content. Without it, most sections would be empty.
>
> To reconnect: check your MCP configuration or run `/octave:workspace status`

**Person Not Found:**
> I couldn't find detailed information for [email/name].
>
> I found their company ([Company]). Would you like me to:
> 1. Proceed with company research + generic persona guidance
> 2. Search for them on LinkedIn (provide URL)
> 3. Create a brief based on their title and company alone

## Related Skills

- `/octave:research` — Text-based research and prep (brief is the visual, rendered version)
- `/octave:meeting-prep` — Coached prep for a specific upcoming meeting
- `/octave:one-pager` — Customer-facing leave-behind document (brief is internal)
- `/octave:deck` — Full slide presentation (brief is a reference document)
- `/octave:battlecard --format doc` — Competitive reference document (brief includes competitive context but is broader)
- `/octave:pipeline` — Deal-level coaching and pipeline strategy
- `/octave:generate` — Generate outreach content with brand voice control
- `/octave:insights` — Conversation intelligence deep dives
