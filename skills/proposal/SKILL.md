---
name: proposal
description: Formal business case and proposal generator that produces customer-facing HTML documents with ROI framing and implementation details. Use when user says "create a proposal", "business case", "proposal for [company]", "formal pitch", or asks for a closing document.
---

# /octave:proposal - Octave-Powered Proposal Builder

Generate formal business case and proposal documents powered by your Octave GTM intelligence. These are the documents that close deals — sent to champions to sell internally, shared with procurement, and presented to executives. Unlike a one-pager (summary) or a deck (live presentation), proposals are comprehensive, customer-facing documents built for async review, internal circulation, and executive sign-off.

The output is a multi-section scrollable HTML document with a sticky table of contents, print-friendly layout, and the same CSS variable / style preset system as `/octave:deck`.

## Usage

```
/octave:proposal <target> [--style <preset>]
```

## Examples

```
/octave:proposal acme.com                                # Full proposal for Acme
/octave:proposal acme.com --style executive-dark         # With specific style
/octave:proposal "enterprise security platform deal"     # Context-based
/octave:proposal acme.com --style midnight-pro           # Dark professional style
/octave:proposal "renewal for DataCorp Q2"               # Renewal proposal
```

## Instructions

When the user runs `/octave:proposal`:

### Step 1: Understand the Context

If not provided via flags or obvious from the prompt, ask the user interactively:

**Target — "Who is this proposal for?"**

```
Who is this proposal for?

Provide any of the following:
- Company domain (e.g., acme.com)
- Person name or email (e.g., jane@acme.com)
- Deal context (e.g., "enterprise security platform deal with Acme")

Target:
```

**Stage — "Where is this deal?"**

```
What stage is this deal in?

1. Early exploration — they're interested, you're making the case
2. Mid-funnel evaluation — they're comparing options, full persuasion needed
3. Late-stage decision — they know the product, focus on commercials
4. Renewal — existing customer, results + what's next

Your choice:
```

| Stage | Impact on Proposal |
|-------|-------------------|
| Early exploration | Concise, don't overwhelm. Focus on problem + solution + proof. |
| Mid-funnel evaluation | Comprehensive. Full persuasion with every section. |
| Late-stage decision | Commercial focus. Investment, implementation, next steps. |
| Renewal | Backward-looking results + forward-looking roadmap. |

**Champion — "Who will use this document internally?"**

```
Who is your champion — the person who will circulate this internally?

Provide name, title, or role (e.g., "Sarah Chen, VP Engineering").
If unknown, I'll write for a general executive audience.

Champion:
```

**Key Concerns — "Any known objections or priorities?"**

```
Are there known objections, requirements, or priorities?

Examples:
- "They're worried about implementation timeline"
- "Security compliance is a hard requirement"
- "Competing against Gong and Chorus"
- "Budget is tight, need strong ROI story"

Key concerns (or skip):
```

**Pricing — "Include pricing?"**

```
Should the proposal include a pricing / investment section?

1. Yes — I'll include it (provide pricing details or I'll frame it)
2. No — leave pricing out
3. TBD — include a placeholder section

Your choice:
```

### Step 2: Octave Context Gathering

Based on the target, stage, champion, and concerns, use Octave MCP tools to build rich context. **Always tell the user what you're researching and why.**

**Call as many tools as needed to build a complete picture.** Proposals demand depth — company enrichment + playbook messaging + proof points + conversation intel + competitive context all combine to create a document that feels tailored, not templated. Don't stop at one tool when five would give you a stronger narrative.

Not every tool applies to every proposal. Use your judgment about which are relevant to *this specific* situation. The tables below show what's available — pick the combination that produces the most compelling case.

**List vs Search — when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_all_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory — "show me all our proof points" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content — "get full proof point details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept or question — "how do we help in healthcare?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material, existing proposals, pricing docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

**Follow-up proposals — ground them in what actually happened:**

If this proposal follows previous interactions with the account (demo, discovery call, pilot), pull findings and events to anchor the narrative in real data rather than generic positioning:

- `list_findings({ query: "<company or contact>", startDate: "<relevant period>" })` — surfaces what was actually said in calls: objections raised, features requested, pain points confirmed, competitor mentions
- `list_events({ filters: { accounts: ["<account_oId>"] } })` — deal stage changes, meetings held, emails sent — shows the journey so far
- `get_event_detail({ eventOId })` — deep dive on specific events to pull exact context

This turns a generic proposal into "here's what we heard from you, and here's exactly how we're addressing it."

---

See [octave-tool-reference.md](references/octave-tool-reference.md) for the full tool reference tables (company/contact research, playbooks, proof points, competitive context, conversation history, and resources).

---

**Output of this step:** Present a structured proposal outline to the user for approval before generating.

See [proposal-outline-template.md](references/proposal-outline-template.md) for the structured proposal outline template.

**Wait for user approval before proceeding.**

### Step 3: Style Selection

Proposals should feel premium and professional. The default recommendation depends on the audience:

| Audience | Recommended Default |
|----------|-------------------|
| Enterprise / executive | `executive-dark` |
| Technical / modern | `midnight-pro` |
| Conservative / traditional | `paper-minimal` |
| General | `executive-dark` |

Ask the user:

```
How would you like to style the proposal?

1. Use recommended — [preset name] (best for [audience])
2. Pick from presets — show me all 12 options
3. Use my brand — extract from a website or provide brand assets
4. Surprise me — auto-pick based on context

Your choice:
```

**If user picks "Show me all 12 options":**

See [style-presets.md](references/style-presets.md) for the full list of 12 style presets grouped by theme.

Full CSS variable definitions for each preset are in the deck skill's [STYLE_PRESETS.md](../deck/STYLE_PRESETS.md).

**Brand extraction is encouraged for proposals.** A proposal that carries the customer's or your own brand colors looks significantly more professional and intentional. Follow the same brand discovery flow as `/octave:deck` Step 3 (browser-use > WebFetch > manual fallback).

### Step 4: Generate HTML

Build a single, self-contained HTML file. **No external dependencies** except Google Fonts. Everything else inlined.

#### Output Directory

Every proposal gets its own folder under `.octave-proposals/`:

```
.octave-proposals/
└── <kebab-case-name>-<YYYY-MM-DD>/
    ├── <name>.html                    # Final HTML proposal
    └── <name>-content.md              # Markdown export (if requested)
```

Example: `/octave:proposal acme.com` -> `.octave-proposals/acme-corp-proposal-2026-02-11/acme-corp-proposal.html`

The entire `.octave-proposals/` directory is in `.gitignore` — nothing here gets committed.

#### Section Selection by Stage

Not all sections appear in every proposal. Stage determines what's included:

| Stage | Sections Included | Notes |
|-------|-------------------|-------|
| Early exploration | Cover, TOC, Exec Summary, Challenge, Solution, Proof, Next Steps | Keep it concise, don't overwhelm |
| Mid-funnel evaluation | All sections (1-11) | Full persuasion, comprehensive |
| Late-stage decision | Cover, TOC, Exec Summary, Investment, Implementation, Next Steps | They know the product, focus on commercials |
| Renewal | Cover, TOC, Exec Summary (results achieved), Solution (what's new), Investment, Next Steps | Backward-looking + forward |

#### Document Sections — Full Proposal

See [document-sections.md](references/document-sections.md) for the full specification of each of the 11 proposal sections.

#### HTML Architecture

See [html-architecture.md](references/html-architecture.md) for the core HTML structure scaffold and required print styles.

#### Key Differences from Deck HTML

| Concern | Deck | Proposal |
|---------|------|----------|
| Layout | Full-viewport slides, scroll-snap | Scrollable document, max-width content |
| Navigation | Nav dots, keyboard slide-to-slide | Sticky sidebar TOC with anchor links |
| Content density | Strict per-slide limits | Paragraphs, long-form content allowed |
| Print | Not a priority | Critical — buyers print proposals |
| Page breaks | N/A | Between major sections for printing |
| Typography | Display/impact focused | Readability focused, longer line heights |
| Width | Full viewport | Max 850px content + 220px sidebar |
| Animation | Entrance animations per slide | Subtle — scroll-based fade-in at most |

#### Typography Recommendations

Proposals benefit from serif headings paired with sans-serif body text for a formal, authoritative feel:

| Preset | Heading Font | Body Font |
|--------|-------------|-----------|
| executive-dark | Playfair Display | Inter |
| midnight-pro | Inter | Inter |
| paper-minimal | Libre Baskerville | Source Sans 3 |
| swiss-modern | Inter | Inter |

For brand-extracted styles, prefer the brand's own fonts. If none are available, default to the heading/body pairing from the chosen preset.

#### Content Writing Guidelines

Proposals are persuasive documents, not feature lists. Follow these principles:

1. **Lead with their world, not yours.** Open every section from the customer's perspective.
2. **Ground in specifics.** Use company name, industry data, conversation quotes. Generic = ignored.
3. **Quantify everything.** "Reduce onboarding time by 60%" beats "Faster onboarding."
4. **One idea per paragraph.** Executives skim. Make every paragraph earn its place.
5. **Active voice.** "We deploy in 4 weeks" not "Deployment is completed in 4 weeks."
6. **Address objections before they arise.** If you know a concern, handle it in the relevant section.
7. **End every section with a forward pull.** Give the reader a reason to keep going.

### Step 5: Delivery

After generating the HTML file:

1. **Open the proposal** in the default browser
2. **Present a summary:**

See [delivery-summary.md](references/delivery-summary.md) for the PROPOSAL READY summary template.

**Stakeholder variants:** If the user asks for a version for a different audience (e.g., "make one for the CTO"), adjust:
- Emphasis: shift from business value to technical architecture
- Language: match the stakeholder's domain
- Sections: add/remove appendix items, shift proof points to technical ones
- Tone: executive = strategic, technical = detailed, procurement = ROI-focused

**PDF export guidance:**

```
To save as PDF (recommended for sharing):

1. Open the proposal in your browser (already open)
2. Press Cmd+P (Mac) or Ctrl+P (Windows)
3. Set margins to "Default" or "Minimum"
4. Enable "Background graphics" for colors and styling
5. Select "Save as PDF"

The proposal is designed with page breaks between sections for clean printing.
```

## MCP Tools Used

### Research & Enrichment
- `enrich_company` — Full company intelligence profile
- `enrich_person` — Full person intelligence report
- `find_person` — Find contacts at a company by title/role
- `qualify_company` — ICP fit scoring for a company
- `qualify_person` — ICP fit scoring for a person

### Library — Fetching Entities
- `list_all_entities` — Quick scan of all entities of a type (minimal fields)
- `list_entities` — Fetch entities with full data and pagination
- `get_entity` — Deep dive on one specific entity
- `get_playbook` — Retrieve a playbook with full content and value props
- `list_value_props` — Value propositions for a specific playbook

### Library — Searching
- `search_knowledge_base` — Semantic search across library entities and resources
- `list_resources` — Browse uploaded docs, URLs, and Google Drive files
- `search_resources` — Semantic search across uploaded resources

### Intelligence & Signals
- `list_findings` — Recent conversation findings and insights
- `list_events` — Deal events (won, lost, created, stage changes)
- `get_event_detail` — Full details for a specific event

### Content Generation
- `generate_call_prep` — Synthesized prep brief for accounts
- `generate_content` — Generate positioning or messaging content

### Brand & Style
- `list_brand_voices` — Available brand voices in workspace
- `list_writing_styles` — Available writing styles in workspace

## Error Handling

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The proposal builder can still work without Octave — you'll provide the content manually, and I'll handle structure, style, and HTML generation.
>
> To reconnect: check your MCP configuration or run `/octave:workspace status`

**Company Not Found:**
> I couldn't find detailed intelligence for [domain].
>
> Options:
> 1. Proceed with what we have — I'll use general positioning from your library
> 2. Try a different domain
> 3. Provide company context manually and I'll build the proposal

**No Proof Points Available:**
> No proof points or references matched this account's industry or use case.
>
> Options:
> 1. Proceed without a Proof of Results section
> 2. Add generic proof points (I'll use your best available)
> 3. Provide case study details manually
> 4. Skip for now and add later

**No Pricing Information:**
> No pricing resources found in your workspace.
>
> Options:
> 1. Provide pricing details and I'll format them
> 2. Include a TBD placeholder — "Investment details to be discussed"
> 3. Omit the investment section entirely

**No Matching Playbook:**
> No playbook matches this audience profile directly.
>
> I'll use your general value props and positioning. After the proposal is built, consider creating a playbook for this segment.

## Related Skills

- `/octave:deck` — Presentation version of the pitch (for live presenting)
- `/octave:one-pager` — Summary version (when a full proposal is too heavy)
- `/octave:brief` — Internal prep document (for your team, not the customer)
- `/octave:research` — Deeper research on the account before writing
- `/octave:battlecard-doc` — Competitive reference document (if competitor in deal)
- `/octave:generate` — Generate content with brand voice control
- `/octave:pipeline` — Deal-level strategy and coaching
