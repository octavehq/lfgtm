---
name: proposal
description: Formal business case and proposal generator that produces customer-facing HTML documents with ROI framing and implementation details. Use when user says "create a proposal", "business case", "proposal for [company]", "formal pitch", or asks for a closing document.
---

# /octave:proposal - Octave-Powered Proposal Builder

Generate formal business case and proposal documents powered by your Octave GTM intelligence. These are the documents that close deals — sent to champions to sell internally, shared with procurement, and presented to executives. Unlike a one-pager (summary) or a deck (live presentation), proposals are comprehensive, customer-facing documents built for async review, internal circulation, and executive sign-off.

The output is a scrollable HTML document built around **six jobs**, not a kitchen-sink of sections: (1) the bottom line, (2) the problem we're solving, (3) what we'd do, (4) why it's worth it, (5) proof it works, (6) how it goes. Sticky table of contents, print-friendly layout, and the same CSS variable / style preset system as `/octave:deck`. The full spec — job order, density caps, and the review checklist — lives in [document-sections.md](references/document-sections.md).

## On-brand styling — brand kit first, then generate

**Resolve the brand before generating (do not skip this step).** The proposal is sent BY the workspace company TO the prospect — it goes out on the **workspace company's brand** (the Octave customer whose workspace you are operating in), like a proposal on your letterhead. The target company's logo may appear in content sections (cover, "prepared for" line) but does not control the design system.

**Step 1: Identify the workspace company.** Call `get_workspace_company` to get the company name, domain/URL, and positioning.

**Step 2: Resolve the workspace company's brand kit.** Slugify the workspace company name and check for a cached brand kit at `~/.octave/brands/<slug>/manifest.json`. If a complete kit exists (has `manifest.json` and `tokens.css`), use it automatically:
   - inline the kit's `tokens.css` (`:root` + the embedded `@font-face`) **and** `../get-brand-components/assets/kit_base.css` into the output `<style>`;
   - follow the kit's `brand-kit.md` → **Signature moves**; reuse the kit's real **logo** for cover and footer, `images/`, and `icons.json`.
   **If no complete kit exists → build one.** Run the `get-brand-components` skill (read its SKILL.md and follow it) for the workspace company's domain. If the first attempt returns incomplete results, retry up to 3 times with different approaches (root domain, `www.` prefix, `/about` subpage). Only fall back to a style preset after 3 genuine failures.

**Step 3: Style presets are a last resort** — only after the workspace company's brand kit cannot be built (see Step 3 in Instructions).

## Principles

Follow these standards during generation. Read each before producing output.

**Content and language:**
- [Editorial rules](../shared/editorial-rules.md) — no AI-isms, banned vocabulary, honest analyst tone
- [Information principles](../shared/information-principles.md) — lead with conclusions, evidence-backed claims, narrative arc

**Visual design:**
- [Presentation principles](../shared/presentation-principles.md) — typography, layout, visual restraint
- [HTML document format](../shared/formats/html-document.md) — scrollable document specifics

**Octave data:**
- [Octave value](../shared/octave-value.md) — prioritize grounded workspace data over generic AI content

**Mandatory review:** Every generated proposal goes through the review pipeline (Step 5) before delivery. This is a gate, not an offer — see [review protocol](../shared/protocol.md).

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

**Call as many tools as needed to build a complete picture.** Proposals demand depth — company enrichment + Motion ICP cell narrative + proof points + conversation intel + competitive context all combine to create a document that feels tailored, not templated. Don't stop at one tool when five would give you a stronger narrative.

**The crown-jewel move: per-persona framing from the Motion ICP cell.** The single most differentiated element of an Octave proposal is Job 3's per-persona strip — how the value frames for each member of the buying committee (the CISO cares about X, the economic buyer cares about Y). Pull this from `find_motion_icp({ ..., includeLearnings: true })` for the matched persona × segment cell. Only include personas actually present or named in the deal — confirm real people via `find_person` / `enrich_person`, never a generic set. This is what makes the doc read as "they understand our whole committee," not "they sent us a template."

**Groundedness is a hard bar.** Every named person, title, prior employer, LinkedIn URL, proof-point company, metric, and quote in the proposal must trace to a real tool result — not a plausible synthesis. This is a customer-facing document; a fabricated case study or invented stakeholder loses the deal. Verify names against an actual `find_person` result before using them. Honest gaps ("no economic buyer identified yet") beat inventions. Tag anything unconfirmed with `.unconfirmed`.

Not every tool applies to every proposal. Use your judgment about which are relevant to *this specific* situation. The tables below show what's available — pick the combination that produces the most compelling case.

**List vs Search — when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory — "show me all our proof points" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content — "get full proof point details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept or question — "how do we help in healthcare?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material, existing proposals, pricing docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

**Follow-up proposals — ground them in what actually happened:**

If this proposal follows previous interactions with the account (demo, discovery call, pilot), pull findings and events to anchor the narrative in real data rather than generic positioning:

- `list_findings({ query: "<company or contact>", startDate: "<relevant period>" })` — surfaces what was actually said in calls: objections raised, features requested, pain points confirmed, competitor mentions
- `list_events({ filters: { companyDomains: ["<company_domain>"] } })` — deal stage changes, meetings held, emails sent — shows the journey so far
- `get_event_detail({ eventOId })` — deep dive on specific events to pull exact context

This turns a generic proposal into "here's what we heard from you, and here's exactly how we're addressing it."

---

See [octave-tool-reference.md](references/octave-tool-reference.md) for the full tool reference tables (company/contact research, Motions and Motion ICP cells, proof points, competitive context, conversation history, and resources).

---

**Output of this step:** Present a structured proposal outline to the user for approval before generating.

See [proposal-outline-template.md](references/proposal-outline-template.md) for the structured proposal outline template.

**Wait for user approval before proceeding.**

### Step 3: Resolve the Brand

Follow the "On-brand styling" section at the top of this skill: `get_workspace_company` → cached kit at `~/.octave/brands/<slug>/` → build via `get-brand-components` (retry up to 3 times) → preset fallback.

**Only if the brand kit genuinely cannot be built**, fall back to a style preset:

| Audience | Fallback Preset |
|----------|-----------------|
| Enterprise / executive | `executive-dark` |
| Technical / modern | `midnight-pro` |
| Conservative / traditional | `paper-minimal` |
| General | `executive-dark` |

See [style-preset-menu.md](references/style-preset-menu.md) for the picker list; CSS variable definitions are in the shared [style-presets.md](../shared/style-presets.md).

### Step 4: Generate HTML

**Load the shared rules before writing any HTML. Read each before producing output:**
- [Editorial rules](../shared/editorial-rules.md) — universal language rules, AI-ism kill list, banned vocabulary
- [Information principles](../shared/information-principles.md) — lead with conclusions, evidence-backed claims, narrative arc
- [Presentation principles](../shared/presentation-principles.md) — universal visual rules, spacing, restraint
- [HTML document format](../shared/formats/html-document.md) — scrollable-document visual rules
- [Octave value](../shared/octave-value.md) — grounded workspace data over generic AI content
- [Regression checklist](references/regression-checklist.md) — issues found during testing, verified against every new generation

Apply these rules during generation, not just during review.

Build a single, self-contained HTML file. **No external dependencies** except Google Fonts. Everything else inlined.

**After writing the file, proceed immediately to Step 5 (Review Pipeline). Do NOT open the file in the browser or present it to the user yet.**

#### Output Directory

Every proposal gets its own folder under `.octave-proposals/` in the user's **home directory** (`~/.octave-proposals/`, not the skill or project folder):

```
.octave-proposals/
└── <kebab-case-name>-<YYYY-MM-DD>/
    ├── <name>.html                    # Final HTML proposal
    └── <name>-content.md              # Markdown export (if requested)
```

Example: `/octave:proposal acme.com` -> `.octave-proposals/acme-corp-proposal-2026-02-11/acme-corp-proposal.html`

The entire `.octave-proposals/` directory is in `.gitignore` — nothing here gets committed.

#### Job Selection by Stage

The proposal is built around six jobs (plus Cover + TOC chrome). Not every job appears in every proposal — stage trims the lineup. Never pad a stage back to all six if the content isn't there.

| Stage | Jobs Included | Notes |
|-------|---------------|-------|
| Early exploration | Bottom Line, Problem, What We'd Do, Proof, How It Goes | Concise. Skip the deep business case — they're not there yet. |
| Mid-funnel evaluation | All six jobs | Full persuasion, comprehensive. |
| Late-stage decision | Bottom Line, Why It's Worth It, How It Goes | They know the product. Lead with the business case and the plan. |
| Renewal | Bottom Line (results achieved), What We'd Do (what's new), Why It's Worth It, How It Goes | Backward-looking results + forward roadmap. |

#### Document Sections — the Six Jobs

See [document-sections.md](references/document-sections.md) for the full specification: the six jobs, their fixed order, per-job density caps, the pacing and component-fatigue rules, and the review checklist. Read it before generating — it is where the tight-jobs discipline lives.

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

#### Typography Recommendations (preset fallback only)

When a brand kit is in use, the kit's fonts win — skip this table. For preset fallbacks, proposals benefit from serif headings paired with sans-serif body text for a formal, authoritative feel:

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

### Step 5: Review Pipeline — MANDATORY GATE

**Do NOT open the proposal in the browser, present the delivery summary, or tell the user the proposal is ready until the review pipeline has completed and you have a scorecard.**

Load the [review protocol](../shared/protocol.md) and execute the review loop against the generated HTML file. The protocol specifies the full process; here is the proposal-specific wiring:

**5a: Mechanical lint** (before spawning reviewers):

```bash
bash <skill-dir>/scripts/lint.sh <path-to-proposal.html>
```

Fix every violation the lint surfaces.

**5b: Spawn two reviewers in parallel** (both Task calls in a single message):

**Editorial reviewer:**
```
Task tool:
  subagent_type: "octave-editorial-reviewer"
  prompt: "Review the file at [FILE PATH].
           Read these principle docs and run each Review Checklist:
           1. [skill-dir]/../shared/editorial-rules.md
           2. [skill-dir]/../shared/information-principles.md
           3. [skill-dir]/../shared/octave-value.md
              (Data Grounding and Framing sections — this is a
              customer-facing document; every claim must trace to
              workspace data)
           4. [skill-dir]/references/regression-checklist.md
              (Density section)
           Fix violations inline. Return scorecard."
```

**Presentation reviewer:**
```
Task tool:
  subagent_type: "octave-presentation-reviewer"
  prompt: "Review the file at [FILE PATH].
           Read these docs and run each Review Checklist:
           1. [skill-dir]/../shared/presentation-principles.md
           2. [skill-dir]/../shared/formats/html-document.md
           3. [skill-dir]/references/html-architecture.md
           4. [skill-dir]/references/document-sections.md
           5. [skill-dir]/references/regression-checklist.md
              (Structure & Repetition and Validated Formats sections)
           Fix violations inline. Return scorecard."
```

**5c: Loop decision.** Read both scorecards:

| Cycle | 0 fixes | 1-2 fixes | 3+ fixes |
|---|---|---|---|
| Cycle 1 | CLEAN → 5d | Apply, loop | Apply, loop |
| Cycle 2 | CLEAN → 5d | Apply, STOP | Apply, loop |
| Cycle 3 (cap) | CLEAN → 5d | Apply, STOP | Apply, STOP |

Max 3 cycles. Re-run both reviewers each loop (back to 5b).

**5d: Output combined scorecard** to the user. This is proof the pipeline ran. Step 6 cannot start without it.

```
REVIEW PIPELINE COMPLETE
=========================
Editorial:      [N fixes / PASS]
Presentation:   [N fixes / PASS]

Total fixes: [N]
Cycles: [1-3]
Status: [CLEAN / N remaining issues]
```

### Step 6: Delivery

After the review pipeline scorecard has been output:

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

PDF (recommended): bash "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/export-pdf.sh .octave-proposals/<name>-<date>/<name>.html
  — or use the manual print dialog below:

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
- `list_entities` — Quick scan of all entities of a type (minimal fields)
- `list_entities` — Fetch entities with full data and pagination
- `get_entity` — Deep dive on one specific entity

### Motions
- `list_motions` — Motions for the offering
- `list_motion_playbooks` — Default + Custom Motion Playbooks under a Motion
- `get_motion_playbook` — Full Motion Playbook details
- `list_motion_icps` — Persona × segment matrix for a Motion
- `find_motion_icp` — Full per-cell narrative + Learning Loop learnings

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
- `get_workspace_company` — Workspace company identity for brand resolution
- `list_entities` (entityType: "brand_voice") — Available brand voices in workspace
- `list_writing_styles` — Available writing styles in workspace

## Error Handling

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The proposal builder can still work without Octave — you'll provide the content manually, and I'll handle structure, style, and HTML generation.
>
> To reconnect: check your Octave MCP configuration and reconnect

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

**No Matching Motion ICP Cell:**
> No Motion ICP cell matches this audience profile directly.
>
> I'll use your general positioning. After the proposal is built, consider layering a Custom Motion Playbook (Thematic / Milestone / Account / Competitive) on the relevant Motion for this angle.

## Related Skills

- `/octave:deck` — Presentation version of the pitch (for live presenting)
- `/octave:one-pager` — Summary version (when a full proposal is too heavy)
- `/octave:research` — Internal prep document (for your team, not the customer)
- `/octave:research` — Deeper research on the account before writing
- `/octave:battlecard-doc --format html` — Competitive reference document (if competitor in deal)
- `/octave:generate` — Generate content with brand voice control
- `/octave:pipeline` — Deal-level strategy and coaching
