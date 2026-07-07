---
name: one-pager
description: Personalized one-pager / leave-behind generator rendered as self-contained HTML. Use when user says "one-pager for [company]", "leave-behind", "follow-up doc", "demo summary", or asks for a concise customer-facing document.
argument-hint: "<company-or-email> [--for <occasion>] [--style <preset>] [--skip-review]"
---

# /octave:one-pager - Personalized One-Pager Builder

Generate personalized, self-contained HTML one-pager documents (leave-behinds) powered by your Octave GTM knowledge base. Unlike generic templates, this skill enriches every section with real account intelligence -- company signals, persona pain points, Motion ICP cell narrative, and proof points -- to create a document that feels written specifically for the recipient.

One-pagers are single scrollable pages designed to be sent after a demo, meeting, or call. They summarize why your product is a fit for this specific account. Think of it as the document you email or print, not present.

## On-brand styling

A one-pager is **customer-facing** (a leave-behind for the recipient), so **offer the recipient's (the target company's) brand** for a personalized, "built for you" feel; the sender's brand is the alternative. Follow the kit lookup, defaults, and extraction tiers in [../shared/brand-kit-usage.md](../shared/brand-kit-usage.md).

## Review pass (runs by default)

Run the default review pass after generating — the always-on preflight plus the visual render-and-inspect pass, per [../shared/review-pass.md](../shared/review-pass.md). Opt out with `--skip-review`. When generating, follow the output rules in [../shared/presentation-principles.md](../shared/presentation-principles.md).

## Usage

```
/octave:one-pager <target> [--for <occasion>] [--style <preset>] [--skip-review]
```

## Examples

```
/octave:one-pager acme.com                              # General one-pager for Acme
/octave:one-pager jane@acme.com --for demo-followup     # Post-demo leave-behind
/octave:one-pager acme.com --for discovery              # Post-discovery summary
/octave:one-pager "enterprise healthcare segment"       # Segment-level one-pager
/octave:one-pager acme.com --for renewal --style soft-light  # Renewal doc with specific style
/octave:one-pager jane@acme.com --for event-followup    # Post-conference/event follow-up
```

## Occasions

| Occasion | Output Focus |
|----------|--------------|
| `demo-followup` | Recap what was shown, reinforce value, clear next steps |
| `discovery` | Summarize pain points heard, position solution fit |
| `intro` | General company intro tailored to the account (default) |
| `event-followup` | Post-conference/event personalized summary |
| `renewal` | Reinforce value delivered, expansion opportunities |

## Instructions

When the user runs `/octave:one-pager`:

### Step 1: Understand the Context

If not provided via flags, ask the user interactively:

**Target -- "Who is this for?"**

```
Who is this one-pager for?

Provide any of the following:
- Company domain (e.g., acme.com)
- Person email (e.g., jane@acme.com)
- Segment description (e.g., "enterprise healthcare")

Target:
```

**Occasion -- "What's the context?"**

```
What's the occasion for this one-pager?

1. Demo follow-up - Sent after a product demo
2. Discovery follow-up - Sent after a discovery call
3. General intro - First touch or general positioning
4. Event follow-up - Sent after a conference/event meeting
5. Renewal - Reinforcing value for an existing customer

Your choice:
```

**Tone -- "What tone should it strike?"**

```
What tone fits best?

1. Formal executive - Polished, concise, boardroom-ready
2. Conversational - Warm, approachable, peer-to-peer
3. Technical - Data-driven, detailed, practitioner-focused

Your choice:
```

### Step 2: Octave Context Gathering

Based on target, occasion, and tone, use Octave MCP tools to build rich context for the one-pager. **Always tell the user what you're researching and why.**

**Call as many tools as needed to build a complete picture.** The best one-pagers come from layering multiple sources -- company enrichment + Motion ICP cell narrative + proof points + conversation intel all combine to create a document that feels genuinely personalized. Not every tool applies to every one-pager; pick the combination that gives you the richest context for the occasion and target.

For list-vs-search guidance, follow-up grounding, and the common tool tables, see [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md). For the account-specific and segment-level tool tables, see [tool-reference.md](references/tool-reference.md).

**Output of this step:** Present a content outline to the user for approval. See [outline-template.md](references/outline-template.md) for the outline template.

**Wait for user approval before proceeding.**

### Step 3: Style Selection

One-pagers use the same 12 style presets and brand extraction system as the other document skills. See [../shared/style-presets.md](../shared/style-presets.md) for full CSS variable definitions.

Ask the user:

```
How would you like to style the one-pager?

1. Pick from presets — 12 styles from dark executive to light minimal
2. Use a brand — mine (the sender) or the recipient's; extract from a website or provide assets
3. Auto-pick — I'll choose based on the occasion and tone
4. Surprise me

Your choice:
```

**Option 1: Preset Picker** -- Show the 12-preset menu from [../shared/style-presets.md](../shared/style-presets.md).

**Option 2: Brand Extraction** -- Follow the tiered brand extraction flow in [../shared/brand-kit-usage.md](../shared/brand-kit-usage.md): Tier 1 `get_external_brand_assets` (colors + logo, with a customer-logo sanity check), Tier 2 `scrape_website` with `includeScreenshot` for fonts + components, then browser-use / WebFetch / manual fallbacks. Confirm brand config with user before proceeding.

**Option 3: Auto-Pick** -- Map occasion + tone to recommended presets:

| Occasion + Tone | Recommended Preset |
|------------------|--------------------|
| Demo follow-up, formal | `midnight-pro` |
| Demo follow-up, conversational | `soft-light` |
| Discovery, formal | `executive-dark` |
| Discovery, conversational | `swiss-modern` |
| Intro, formal | `midnight-pro` |
| Intro, conversational | `soft-light` |
| Intro, technical | `electric-studio` |
| Event follow-up | `aurora-gradient` |
| Renewal, formal | `executive-dark` |
| Renewal, conversational | `soft-light` |

Tell the user what you picked and why. Let them override.

### Step 4: Generate HTML

Build a single, self-contained HTML file. **No external dependencies** except Google Fonts. This is a single scrollable document -- NOT slides.

#### Output Directory

Every one-pager gets its own folder under `.octave-one-pagers/`:

```
.octave-one-pagers/
└── <kebab-case-name>-<YYYY-MM-DD>/
    └── <name>.html
```

Example: `/octave:one-pager acme.com` produces `.octave-one-pagers/acme-one-pager-2026-02-11/acme-one-pager.html`

Make sure `.octave-one-pagers/` is ignored by your project's `.gitignore` (an `.octave-*/` pattern covers all Octave output dirs) so generated one-pagers don't get committed.

#### HTML Architecture

See [html-architecture.md](references/html-architecture.md) for the HTML/CSS scaffold and key differences from the deck skill's HTML.

#### Document Sections

See [one-pager-sections.md](references/one-pager-sections.md) for per-section HTML templates (Header, The Challenge, Our Approach, Key Differentiators, Proof Points, Next Steps).

#### Content Density Rules

Keep it tight. A one-pager should be scannable in under 2 minutes:

| Section | Max Content |
|---------|------------|
| Header | Company name + title + date + "Prepared for" |
| The Challenge | 2-3 sentences max |
| Our Approach | 3-4 value props, each 1-2 sentences |
| Key Differentiators | 3 cards max, each heading + 1-2 sentences |
| Proof Points | 2-3 metrics or quotes |
| Next Steps | 1 CTA + contact info |

If content exceeds these limits, prioritize ruthlessly. The one-pager is a teaser, not a whitepaper.

### Step 5: Delivery

After generating the HTML file:

1. **Open the one-pager** in the default browser
2. **Present a summary:**

```
ONE-PAGER READY
================

Folder: .octave-one-pagers/<name>-<date>/
File:   .octave-one-pagers/<name>-<date>/<name>.html
Style:  [Preset name or "Custom Brand"]
Size:   [file size]

Viewing:
- Open in any browser -- single scrollable page
- PDF (recommended): bash "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/export-pdf.sh .octave-one-pagers/<name>-<date>/<name>.html  — or Cmd+P / Ctrl+P -> Save as PDF
- Email as attachment or save as PDF

Customization tips:
- Colors: Edit the :root CSS variables at the top of the file
- Content: Each <section class="section"> is one block
- Fonts: Change the Google Fonts <link> and font-family values
- Layout: Adjust max-width in .page for wider/narrower output

---

Want me to:
1. Adjust content or messaging
2. Change the style/colors
3. Export as PDF (print dialog)
4. Create a version for a different contact at the same company
5. Create a full presentation deck for this account (/octave:deck)
6. Done
```

## MCP Tools Used

Common research, library, signals, and generation tools: see [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md). One-pager-specific additions:

### Brand & Style
- `get_external_brand_assets` / `get_external_brand_logo` / `scrape_website` — Brand extraction (Tiers 1-2)
- `list_all_entities` (entityType: "brand_voice") - Available brand voices in workspace
- `list_writing_styles` - Available writing styles in workspace

## Error Handling

Standard responses (connection failed, company/person not found, no matching Motion ICP cell, no proof points, no findings): see [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md) → Standard error handling.

## Related Skills

- `/octave:deck` - Full presentation deck (when one page isn't enough)
- `/octave:research` - Deeper research on the account
- `/octave:brief` - Internal account dossier (vs external leave-behind)
- `/octave:proposal` - Formal business case
- `/octave:microsite` - Personalized web page for ABM
