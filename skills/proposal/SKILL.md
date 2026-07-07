---
name: proposal
description: Formal business case and proposal generator that produces customer-facing HTML documents with ROI framing and implementation details. Use when user says "create a proposal", "business case", "proposal for [company]", "formal pitch", or asks for a closing document.
argument-hint: "<company-or-context> [--style <preset>] [--skip-review]"
---

# /octave:proposal - Octave-Powered Proposal Builder

Generate formal business case and proposal documents powered by your Octave GTM intelligence. These are the documents that close deals — sent to champions to sell internally, shared with procurement, and presented to executives. Unlike a one-pager (summary) or a deck (live presentation), proposals are comprehensive, customer-facing documents built for async review, internal circulation, and executive sign-off.

The output is a multi-section scrollable HTML document with a sticky table of contents, print-friendly layout, and the same CSS variable / style preset system as the other document skills.

## On-brand styling

A proposal is **customer-facing** (it goes to the recipient and gets circulated internally), so **offer the recipient's (the target company's) brand** for a personalized feel; the sender's brand is the standard alternative. Follow the kit lookup, defaults, and extraction tiers in [../shared/brand-kit-usage.md](../shared/brand-kit-usage.md). Brand styling is especially encouraged for proposals — a proposal that carries the customer's or your own brand looks significantly more professional and intentional.

## Review pass (runs by default)

Run the default review pass after generating — the always-on preflight plus the visual render-and-inspect pass, per [../shared/review-pass.md](../shared/review-pass.md). Opt out with `--skip-review`. When generating, follow the output rules in [../shared/presentation-principles.md](../shared/presentation-principles.md).

## Usage

```
/octave:proposal <target> [--style <preset>] [--skip-review]
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

**Call as many tools as needed to build a complete picture.** Proposals demand depth — company enrichment + Motion ICP cell narrative + proof points + conversation intel + competitive context all combine to create a document that feels tailored, not templated. Not every tool applies to every proposal; pick the combination that produces the most compelling case.

For list-vs-search guidance, follow-up grounding (anchor the proposal in what was actually said in prior calls), and the common tool tables, see [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md). For the proposal-specific tool tables (company/contact research, Motions and Motion ICP cells, proof points, competitive context, conversation history, and resources), see [tool-reference.md](references/tool-reference.md).

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
3. Use a brand — yours or the customer's; extract from a website or provide assets
4. Surprise me — auto-pick based on context

Your choice:
```

**If user picks "Show me all 12 options":** show the preset menu — full CSS variable definitions are in [../shared/style-presets.md](../shared/style-presets.md).

**If user picks a brand:** follow the tiered brand extraction flow in [../shared/brand-kit-usage.md](../shared/brand-kit-usage.md) (`get_external_brand_assets` → `scrape_website` with `includeScreenshot` → browser-use → WebFetch → manual). Confirm the brand config before proceeding.

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

Make sure `.octave-proposals/` is ignored by your project's `.gitignore` (an `.octave-*/` pattern covers all Octave output dirs) so generated proposals don't get committed.

#### Section Selection by Stage

Not all sections appear in every proposal. Stage determines what's included:

| Stage | Sections Included | Notes |
|-------|-------------------|-------|
| Early exploration | Cover, TOC, Exec Summary, Challenge, Solution, Proof, Next Steps | Keep it concise, don't overwhelm |
| Mid-funnel evaluation | All sections (1-11) | Full persuasion, comprehensive |
| Late-stage decision | Cover, TOC, Exec Summary, Investment, Implementation, Next Steps | They know the product, focus on commercials |
| Renewal | Cover, TOC, Exec Summary (results achieved), Solution (what's new), Investment, Next Steps | Backward-looking + forward |

#### Document Sections — Full Proposal

See [proposal-sections.md](references/proposal-sections.md) for the full specification of each of the 11 proposal sections.

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

Common research, library, signals, and generation tools: see [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md). Proposal-specific additions:

### Brand & Style
- `get_external_brand_assets` / `get_external_brand_logo` / `scrape_website` — Brand extraction (Tiers 1-2)
- `list_all_entities` (entityType: "brand_voice") — Available brand voices in workspace
- `list_writing_styles` — Available writing styles in workspace

## Error Handling

Standard responses (connection failed, company not found, no matching Motion ICP cell, no proof points): see [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md) → Standard error handling. Proposal-specific:

**No Pricing Information:**
> No pricing resources found in your workspace.
>
> Options:
> 1. Provide pricing details and I'll format them
> 2. Include a TBD placeholder — "Investment details to be discussed"
> 3. Omit the investment section entirely

## Related Skills

- `/octave:deck` — Presentation version of the pitch (for live presenting)
- `/octave:one-pager` — Summary version (when a full proposal is too heavy)
- `/octave:brief` — Internal prep document (for your team, not the customer)
- `/octave:research` — Deeper research on the account before writing
- `/octave:battlecard --format doc` — Competitive reference document (if competitor in deal)
- `/octave:generate` — Generate content with brand voice control
- `/octave:pipeline` — Deal-level strategy and coaching
