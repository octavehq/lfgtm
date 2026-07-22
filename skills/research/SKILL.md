---
name: research
description: Context-aware research and prep for calls, meetings, demos, outreach, and deal reviews. Outputs plain text (default) or a styled, scannable HTML document. Use when user says "research [company]", "prep for my call", "who is [person]", "meeting prep", "demo prep", "brief me on [company]", "account dossier", or asks to research a company or person. Do NOT use for bulk prospecting — use /octave:prospector instead. Do NOT use for customer-facing documents — use /octave:one-pager or /octave:proposal instead.
---

# /octave:research - Context-Aware Research & Prep

Research prospects and prepare for calls, meetings, demos, outreach, and deal reviews. Adapts output based on the occasion and format — whether you're prepping for a discovery call, following up on a deal, or researching a new prospect. Supports two output formats:

- **Text** (default) — plain-text research output, optimized for quick consumption in chat
- **HTML** — a styled, self-contained HTML account brief with sticky navigation, collapsible sections, and print-friendly layout, designed to sit on your second monitor during a call or to review before a meeting

**Key differentiators:**
- vs `/octave:one-pager` — one-pager is customer-facing; research (HTML) is internal prep
- vs `/octave:deck` — deck is a slide presentation; research (HTML) is a scrollable reference document

## On-brand styling (HTML format only): workspace company's brand, target logo in content

**Resolve the brand before generating (do not skip this step).** The document brand is the **workspace company's brand**: the Octave customer whose workspace is running the skill. The **target company's logo** (the account being researched) appears in content only (e.g., the header's "prepared for" line, the company snapshot card) and never controls the design system. See [brand kit usage](../shared/brand-kit-usage.md) for the full model, cache lookup, and extraction tiers.

1. Call `get_workspace_company` to resolve the workspace company (name, domain, positioning): this is whose brand the brief wears.
2. Slugify the workspace company name and check for a cached brand kit at `~/.octave/brands/<slug>/manifest.json`. If a complete kit exists, use it automatically:
   - inline the kit's `tokens.css` (`:root` + the embedded `@font-face`) **and** `get-brand-components/assets/kit_base.css` into the output `<style>`;
   - follow `brand-kit.md` --> **Signature moves**, and reuse the kit's real **logo**, `images/`, and `icons.json`;
   - for doc-shaped output you can compose directly with `get-brand-components/scripts/render_kit.py` (hero / split / logos / pricing / cta / footer blocks).
3. **If no kit exists -->** offer to build one first: *"No brand kit for <workspace company> yet, want me to capture it (~1 min) so this is on-brand?"* --> run `/octave:get-brand-components <workspace-domain>`, then proceed.
4. **Fetch the target company's logo** with `get_external_brand_logo` / `get_external_brand_assets` and place it in content (company snapshot, header "prepared for" line), not in the chrome.
5. **If the user declines a kit -->** generate with the default style/preset.

> The brand kit is the strongest styling signal — when one is available, prefer it over generic `--style` presets. See the `get-brand-components` skill for the kit format, token contract, and renderer.

## Principles

Follow these standards during generation. Read each before producing output.

**Content and language:**
- [Editorial rules](../shared/editorial-rules.md) — no AI-isms, banned vocabulary, honest analyst tone
- [Information principles](../shared/information-principles.md) — lead with conclusions, evidence-backed claims, narrative arc

**Visual design (HTML format only):**
- [Presentation principles](../shared/presentation-principles.md) — typography, layout, visual restraint
- [HTML document format](../shared/formats/html-document.md) — scrollable document specifics

**Octave data:**
- [Octave value](../shared/octave-value.md) — prioritize grounded workspace data over generic AI content
- [Octave research toolkit](../shared/octave-research-toolkit.md): list vs search, follow-up grounding, standard tool tables and error handling
- [Entity model](../shared/entity-model.md): canonical entity types and oId prefixes for Motions, Motion Playbooks, and Motion ICPs

**Review gate (HTML format only), mandatory:** After generating HTML output, run the [review protocol](../shared/protocol.md) — a mandatory gate with two dedicated reviewer subagents (`octave-editorial-reviewer` for text, `octave-presentation-reviewer` for visuals). Don't ask permission, announce it at intake ("I'll generate this and run the review gate before handing it back") and run it automatically after generation. The HTML is not opened or delivered until the protocol's combined scorecard has printed. Text-format output skips the gate but still gets the protocol's Step 1 mechanical preflight.

## Usage

```
/octave:research <target> [--for <occasion>] [--format text|html] [--style <preset>]
```

- `--format text` (default): plain-text output in chat
- `--format html`: styled HTML document saved to `.octave-briefs/`
- `--style <preset>`: style preset for HTML output (ignored when format is text)

## Examples

```
/octave:research john@acme.com                              # General research (text)
/octave:research acme.com                                   # Company research (text)
/octave:research john@acme.com --for discovery              # Discovery call prep (text)
/octave:research "meeting with Acme Corp" --for demo        # Demo prep (text)
/octave:research acme.com --for outreach                    # Cold outreach angles (text)
/octave:research acme.com --format html                     # Full account dossier (HTML)
/octave:research jane@acme.com --for discovery --format html  # Discovery call prep (HTML)
/octave:research acme.com --for qbr --format html           # QBR prep brief (HTML)
/octave:research acme.com --for executive --format html     # Executive meeting prep (HTML)
/octave:research acme.com --format html --style paper-minimal # Specific style preset (HTML)
```

## Occasions

| Occasion | Output Focus |
|----------|--------------|
| `discovery` | Questions to ask, pain points to probe, qualification criteria |
| `demo` | Use cases to show, proof points to cite, objections to prepare for |
| `follow-up` | Next steps, open questions, momentum builders |
| `outreach` | Hooks, angles, personalization points, CTAs |
| `qbr` | Deal timeline, recent signals, proof points, value delivered, renewal/expansion angles |
| `executive` | Concise company snapshot, key stakeholders, strategic value props, board-level talking points |
| `deal-review` | Full pipeline context, stage history, competitive landscape, risk assessment |
| `general` | Comprehensive research (default) |

> **Deal coaching?** Use `/octave:pipeline` for deal-level strategy, stalled deals, multi-threading, and competitive deal coaching.

## Instructions

When the user runs `/octave:research`:

### Step 1: Parse Input and Detect Occasion

**Identify the target:**
- Email address --> Person research
- Domain --> Company research
- LinkedIn URL --> Person research
- Name + company --> Person research
- Meeting/deal description --> Context-based (extract company/people)

**Detect or ask occasion:**

If `--for` not specified, infer from context or ask:

```
What are you preparing for?

1. Discovery call — First conversation, qualifying the opportunity
2. Demo — Showing the product, proving value
3. Follow-up — Continuing a conversation, advancing the deal
4. Outreach — Cold/warm outreach, getting a response
5. QBR — Quarterly business review with existing customer
6. Executive meeting — High-level strategic conversation
7. Deal review — Internal review of opportunity status
8. General research — Comprehensive account reference (default)

TIP: For deal coaching and pipeline review, use /octave:pipeline

Your choice:
```

**Detect or ask format:**

If `--format` not specified, default to `text`. If the user said "brief me", "account dossier", "call prep doc", or similar phrasing that implies a document, default to `html` instead.

### Step 2: Research the Target

**Call as many tools as needed to build thorough research.** The best output layers multiple sources — company enrichment + person enrichment + Motion ICP narrative + proof points + conversation intel all combine to create output grounded in real data. Don't stop at one tool when several would give you a stronger result.

Not every tool applies to every research task. Use your judgment about which are relevant to *this specific* situation. The tables below show what's available — pick the combination that gives you the richest context for the occasion and target.

**List vs Search — when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory — "show me all our competitors" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content — "get full proof point details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept or question — "how do we position for healthcare?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material, uploaded assets, or source docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

**Follow-up, QBR, and deal-review occasions — ground them in what actually happened:**

If this research follows a previous interaction with the account (follow-up, QBR, deal review), pull findings and events to anchor the output in real data rather than generic positioning:

- `list_findings({ query: "<company or contact>", startDate: "<relevant period>" })` — surfaces what was actually said in calls: objections raised, features requested, pain points confirmed, competitor mentions
- `list_events({ filters: { companyDomains: ["<company_domain>"] } })` — deal stage changes, meetings held, emails sent — shows the journey so far
- `get_event_detail({ eventOId })` — deep dive on specific events (e.g., the discovery call, the demo) to pull exact context
- `search_call_transcripts({ companyDomain, query: "<topic>" })` — pull the verbatim quote behind a finding, or find a moment when you don't yet know which event to open; returns `recordingUrl` + `startSec` for a citable timestamp

This turns a generic "here's what we know" output into "here's what happened and what to do about it" — much more useful walking into the next conversation.

---

#### For Person-Targeted Research

Start with person and company enrichment, then pull positioning context:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Person deep-dive | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | Always for person-targeted research — gives background, role, priorities |
| Company profile | `enrich_company({ companyDomain })` | Always — gives industry, size, tech stack, signals |
| ICP fit (person) | `qualify_person({ person: { ... } })` | When you need persona match and fit assessment |
| ICP fit (company) | `qualify_company({ companyDomain })` | When you need segment match and ICP scoring |
| Additional contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | When you want to map the broader buying committee |
| Find Motion | `list_motions()` | List all Motions to find the relevant offering + motion type |
| Persona x segment matrix | `list_motion_icps({ motionOId })` | See the persona x segment cells available under a Motion |
| Motion ICP narrative | `find_motion_icp({ motionIcpOId, includeLearnings: true })` | Pull the full Target ICP overview, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References, and Learning Loop learnings for the target persona x segment |
| Proof points | `list_entities({ entityType: "proof_point" })` | Fetch all proof points with full data — metrics, quotes, logos |
| References | `list_entities({ entityType: "reference" })` | Customer references with full details |
| Competitive context | `search_knowledge_base({ query: "<signals>", entityTypes: ["competitor"] })` | When competitor is mentioned or likely in the deal |
| Recent intel | `list_findings({ query: "<company or person>", startDate: "<90 days ago>" })` | Conversation-based insights from past interactions |
| Deal history | `list_events({ filters: { companyDomains: ["<company_domain>"] } })` | Timeline of deal events |
| What this person actually said | `search_call_transcripts({ speakerEmail: "<email>" })` or `attributedPersonaOIds: ["<persona_oId>"]` | Verbatim quotes attributed to this contact or their persona, not a paraphrase |
| Synthesized prep | `generate_call_prep({ companyDomain })` | Quick comprehensive brief to use as a starting point |

---

#### For Company-Targeted Research

Start with company enrichment and contact discovery:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Company profile | `enrich_company({ companyDomain })` | Always — gives industry, size, tech stack, funding, signals |
| ICP fit scoring | `qualify_company({ companyDomain })` | Always — segment match, fit score, fit reasons |
| Key contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | Find stakeholders to populate contacts section |
| Enrich contacts | `enrich_person({ person: { ... } })` | Deep dive on each key contact found |
| All Motions | `list_motions()` | Quick scan to find the right Motion (offering + motion type) |
| Motion ICP matrix | `list_motion_icps({ motionOId })` | See the persona x segment matrix under a Motion |
| Motion ICP narrative | `find_motion_icp({ motionIcpOId, includeLearnings: true })` | Full Target ICP overview, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References, plus Learning Loop learnings for the target cell |
| Custom Motion Playbook details | `get_motion_playbook({ motionPlaybookOId })` | When a Custom Motion Playbook (Thematic / Milestone / Account / Competitive) layers on the relevant Motion |
| All competitors | `list_entities({ entityType: "competitor" })` | Quick scan of competitive landscape |
| Competitor details | `get_entity({ oId })` | Deep dive on a specific relevant competitor |
| Proof points | `list_entities({ entityType: "proof_point" })` | Full proof points for the evidence section |
| References | `list_entities({ entityType: "reference" })` | Customer references for social proof |
| Topic search | `search_knowledge_base({ query: "<industry> <use case>", entityTypes: ["proof_point", "reference"] })` | Find proof points relevant to their specific situation |
| Recent intel | `list_findings({ query: "<company>", startDate: "<90 days ago>" })` | Conversation signals from calls and meetings |
| Deal events | `list_events({ filters: { companyDomains: ["<company_domain>"] } })` | Full deal history and timeline |
| Event details | `get_event_detail({ eventOId })` | Deep dive on specific past interactions |
| Verbatim call quotes | `search_call_transcripts({ companyDomain, query: "<topic>" })` | Receipts for the Recent Signals section — real quotes with recording links, not paraphrases |
| Evidence for a matched entity | `get_entity_evidence({ entityOId })` | Best verbatim quotes backing a matched persona pain, competitor claim, or proof point |
| Uploaded resources | `search_resources({ query: "<company or industry>" })` | Relevant uploaded docs and assets |

---

### Step 3: Generate Output (branches by format)

---

## Text Format Output (--format text)

Generate occasion-specific text output directly in chat.

#### Discovery Call Prep

See [discovery-call-prep.md](references/discovery-call-prep.md) for the discovery call prep output template.

#### Demo Prep

See [demo-prep.md](references/demo-prep.md) for the demo prep output template.

#### Outreach Prep

See [outreach-prep.md](references/outreach-prep.md) for the outreach prep output template.

#### Other Occasions (text format)

For `follow-up`, `qbr`, `executive`, `deal-review`, and `general` in text format, produce structured plain-text output following the same pattern as the templates above: clear section headers, bullet points, checklists, and actionable next steps. Adapt the sections to match the occasion's emphasis (see the occasion table above).

### Text Format: Follow-Up Actions

After any text research output, offer relevant next steps:

```
What would you like to do next?

1. Generate outreach content (/octave:generate)
2. Create collateral for this account (/octave:one-pager or /octave:deck)
3. Render this as an HTML brief (/octave:research --format html)
4. Research additional people at the company
5. Deep dive on a specific topic
6. Save notes to [CRM integration if available]
7. Done for now
```

---

## HTML Format Output (--format html)

When `--format html` is selected, generate a styled, self-contained HTML account brief.

### HTML Step A: Content Outline Approval

Present a content outline to the user for approval before generating:

```
BRIEF OUTLINE: [Company/Person] -- [Occasion]
=============================================

Target: [Company name / Person name at Company]
Occasion: [Discovery / Demo / Follow-up / QBR / Executive / Deal Review / General]
Style: [Will be selected next]

---

SECTIONS TO INCLUDE
-------------------

1. Header -- "Account Brief: [Company]" + date + occasion badge
2. Company Snapshot -- industry, size, HQ, funding, tech stack, signals
3. ICP Fit -- fit score, matched segment, key fit reasons
4. Key Stakeholders -- [N] contacts with persona matches
5. Recommended Playbook -- [Playbook name], strategic angle
6. Talking Points -- [occasion-specific: questions / demo flow / next steps]
7. Value Props -- [N] value props tailored to this account
8. Competitive Landscape -- [Competitor names if detected]
9. Proof Points -- [N] relevant case studies and metrics
10. Recent Signals -- [N] findings from conversations
11. Deal Timeline -- [if existing deal]
12. Quick Reference -- cheat sheet with key facts

Octave Sources Used:
- Company enrichment: [Company] -- [key insights]
- Person enrichment: [Person] -- [persona match]
- Playbook: [Playbook name] -- [strategic angle]
- Proof points: [N] references pulled
- Findings: [N] recent signals
- Competitive: [If applicable]

---

Does this look good? I can:
1. Proceed to style selection and generation
2. Add or remove sections
3. Go deeper on any area
4. Change the occasion / emphasis
```

**Wait for user approval before proceeding.**

### HTML Step B: Style Selection

If the workspace company's brand kit was applied in the on-brand styling step above, it takes precedence over the presets below: skip straight to HTML Step C. Presets are the fallback, used when no kit exists and the user declined to build one, or when the user explicitly wants a different look.

The brief uses the same CSS variable / style preset system as `/octave:deck`. Full preset definitions are in the shared [style-presets.md](../shared/style-presets.md).

Briefs default to readability-optimized presets. If `--style` was not provided, ask:

```
Pick a style for your brief:

1. midnight-pro     -- Dark navy, white text, blue accents (default for briefs)
2. paper-minimal    -- Off-white, black type, editorial simplicity
3. executive-dark   -- Charcoal + gold, premium boardroom aesthetic
4. soft-light       -- Warm white + sage green, calm and approachable
5. swiss-modern     -- White + red accent, Bauhaus minimal
6. Use my brand     -- Extract from website or provide colors
7. Match my deck    -- Use the same style as an existing /octave:deck

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

### HTML Step C: Generate HTML

Build a single self-contained HTML file. The brief is a scrollable reference document — not a slide deck. Natural page scroll, sticky sidebar navigation, collapsible sections, and a print-friendly layout.

#### Output Directory

```
.octave-briefs/
  <kebab-case-name>-<YYYY-MM-DD>/
    <name>.html
```

Example: `/octave:research acme.com --for discovery --format html` --> `.octave-briefs/acme-discovery-2026-02-11/acme-discovery.html`

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
10. **Recent Signals** — From findings: what was said in calls, objections raised, features requested, sentiment indicators. Each signal has a date and source. Where available, pull the verbatim quote via `search_call_transcripts` instead of the paraphrase, and link the recording (`recordingUrl` + `startSec`). Omit if no findings data.
11. **Deal Timeline** — If existing deal: visual stage history (horizontal timeline or vertical step list), key events, current stage, days in stage, next milestone. Omit for new prospects.
12. **Quick Reference** — Sticky sidebar or footer cheat sheet: key facts at a glance, do's and don'ts for this conversation, one-line reminders. Always visible while scrolling.

#### HTML Architecture

See [brief-html-architecture.md](references/brief-html-architecture.md) for the full HTML scaffold, inline CSS, and key differences from deck HTML.

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

### HTML Step C.5: Review Pipeline — MANDATORY GATE

After writing the file, run the [review protocol](../shared/protocol.md) against the generated HTML. Do NOT open the file, present the delivery summary, or tell the user it is ready until the protocol has completed and the combined scorecard has printed. There is no opt-out.

Spawn the two dedicated reviewers (`octave-editorial-reviewer` and `octave-presentation-reviewer`) in parallel per the protocol, using:
- Editorial: [editorial-rules.md](../shared/editorial-rules.md), [information-principles.md](../shared/information-principles.md)
- Presentation: [presentation-principles.md](../shared/presentation-principles.md), [html-document.md](../shared/formats/html-document.md), [brief-html-architecture.md](references/brief-html-architecture.md)

Output the combined scorecard before proceeding to Step D.

### HTML Step D: Delivery

After generating the HTML file and completing the review pipeline:

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
- PDF (recommended): bash "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/export-pdf.sh .octave-briefs/<brief-name>-<date>/<brief-name>.html  -- or Cmd+P / Ctrl+P -> Save as PDF

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
- `enrich_person` — Full person intelligence report
- `enrich_company` — Full company intelligence report
- `qualify_person` — ICP scoring for person
- `qualify_company` — ICP scoring for company
- `find_person` — Find contacts at company
- `find_company` — Find companies matching criteria

### Library — Fetching Entities
- `list_entities` — Quick scan of all entities of a type (minimal fields, no pagination)
- `list_entities` — Fetch entities with full data and pagination (proof points, references, etc.)
- `get_entity` — Deep dive on one specific entity (persona, competitor details)
- `list_motions` — List all Motions in the workspace
- `list_motion_playbooks` — List Motion Playbooks (Default + Custom) under a Motion
- `get_motion_playbook` — Full details for a Motion Playbook
- `list_motion_icps` — List Motion ICP cells (persona x segment intersections) for a Motion
- `find_motion_icp` — Full Motion ICP cell narrative (Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References) plus Learning Loop learnings

### Library — Searching
- `search_knowledge_base` — Semantic search across library entities and resources
- `list_resources` — Browse uploaded docs, URLs, and Google Drive files
- `search_resources` — Semantic search across uploaded resources

### Intelligence & Signals
- `list_findings` — Recent conversation findings and insights
- `list_events` — Deal events (stage changes, meetings, outcomes)
- `get_event_detail` — Full details for a specific event
- `search_call_transcripts` — Verbatim, speaker-attributed quotes across indexed calls, with recording links and timestamps — the receipt behind a finding
- `get_entity_evidence` — Best verbatim quotes evidencing a matched persona, competitor, or proof point

### Content Generation
- `generate_call_prep` — Generate full call prep materials
- `generate_content` — Generate positioning or messaging content

## Error Handling

**Person Not Found:**
> I couldn't find detailed information for [email/name].
>
> I found their company ([Company]). Would you like me to:
> 1. Proceed with company research + generic persona guidance
> 2. Search for them on LinkedIn (provide URL)
> 3. Create research based on their title alone

**Company Not Found:**
> I couldn't find detailed intelligence for [domain].
>
> Options:
> 1. Check the domain spelling and try again
> 2. Try a different domain or company name
> 3. Provide company details manually and I'll structure the output

**No Matching Motion ICP:**
> No Motion ICP cell matches this audience profile directly.
>
> Closest matches:
> - [Motion ICP 1] (60% fit)
> - [Motion ICP 2] (45% fit)
>
> I'll use [Motion ICP 1] as a guide, but you may want to add the missing persona x segment cell to a Motion (or create a new Motion). Alternatively, consider layering a Custom Motion Playbook (Thematic / Milestone / Account / Competitive) onto an existing Motion to cover this segment.

**Octave Connection Failed (HTML format):**
> Could not connect to your Octave workspace.
>
> The research tool needs Octave data to generate useful content. Without it, most sections would be empty.
>
> To reconnect: check your Octave MCP configuration and reconnect

**No Findings Data:**
> No conversation signals found for [company/person].
>
> This may be a new prospect with no prior interactions. I'll skip the Recent Signals and Deal Timeline sections and focus on enrichment data, Motion ICP narrative, and proof points instead.

**No Proof Points:**
> No proof points found in your library.
>
> The Proof Points section will be omitted. To strengthen future research, add case studies and customer references to your Octave library.

**HTML Write Failure:**
> Could not write to the `.octave-briefs/` directory.
>
> Try:
> 1. Check file system permissions
> 2. Ensure you're in a project directory
> 3. I can output the HTML content directly so you can save it manually

## Related Skills

- `/octave:one-pager` — Customer-facing leave-behind document (research HTML is internal)
- `/octave:deck` — Full slide presentation (research HTML is a reference document)
- `/octave:generate` — Generate outreach content with brand voice control
- `/octave:one-pager` — Account-specific leave-behind collateral
- `/octave:prospector` — Find more prospects like this one
- `/octave:call-analyzer` — Analyze past interactions with this account
- `/octave:pipeline` — Deal-level coaching (stalled deals, multi-threading, competitive)
- `/octave:product-launch` — Product launch planning and execution
- `/octave:abm` — Full account-based planning with stakeholder mapping
- `/octave:battlecard-doc` — Competitive intelligence for deals
- `/octave:battlecard-doc --format html` — Competitive reference document (research includes competitive context but is broader)
- `/octave:insights` — Conversation intelligence deep dives
