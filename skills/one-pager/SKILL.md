---
name: one-pager
description: Personalized one-pager / leave-behind generator rendered as self-contained HTML. Use when user says "one-pager for [company]", "leave-behind", "follow-up doc", "demo summary", or asks for a concise customer-facing document.
---

# /octave:one-pager - Personalized One-Pager Builder

Generate personalized, self-contained HTML one-pager documents (leave-behinds) powered by your Octave GTM knowledge base. Unlike generic templates, this skill enriches every section with real account intelligence -- company signals, persona pain points, Motion ICP cell narrative, and proof points -- to create a document that feels written specifically for the recipient.

One-pagers are single scrollable pages designed to be sent after a demo, meeting, or call. They summarize why your product is a fit for this specific account. Think of it as the document you email or print, not present.

## On-brand styling — brand kit first, then generate

**Resolve the brand before generating (do not skip this step).** The document brand should be the **workspace company's brand** — that is, the Octave customer whose workspace you are operating in. The **target company's logo** (the prospect) should appear in content sections (1-2 places) but does not control the document's design system.

**Step 1: Identify the workspace company.** Call `get_workspace_company` to get the company name, domain/URL, and positioning. This is the company whose brand the document should use (whatever get_workspace_company returns is the brand, not the target account).

**Step 2: Resolve the workspace company's brand kit.** Slugify the workspace company name and check for a cached brand kit at `~/.octave/brands/<slug>/manifest.json`. If a complete kit exists (has `manifest.json` and `tokens.css`), use it automatically:
   - inline the kit's `tokens.css` (`:root` + the embedded `@font-face`) **and** `get-brand-components/assets/kit_base.css` into the output `<style>`;
   - follow `brand-kit.md` → **Signature moves**, and reuse the kit's real **logo** for header and footer, `images/`, and `icons.json`;
   - for doc-shaped output you can compose directly with `get-brand-components/scripts/render_kit.py` (hero / split / logos / pricing / cta / footer blocks).
   **If no complete kit exists → build one.** Run the `get-brand-components` skill (read `../../skills/get-brand-components/SKILL.md` and follow it) for the workspace company's domain. If the first attempt returns incomplete results (no logo, no colors, partial data) → retry up to 3 times with different approaches (root domain, `www.` prefix, `/about` subpage). Only fall back to a generic preset after 3 genuine failures.

**Step 3: Fetch the target company's logo.** Use `get_external_brand_logo` or `get_external_brand_assets` to get the prospect's logo. Place it in the content (e.g., next to the company name, in the company context section). Do not use it for the document header/footer — those use the workspace company's brand.
   - If the first attempt returns no logo → retry up to 3 times.

**Step 4: Only use a generic preset as a last resort** — after the workspace company's brand kit cannot be built.

> **⚠️ STRONG DEFAULT:** The document is always branded as the workspace company (the Octave customer). The prospect's logo appears in content to personalize the leave-behind, but the overall look and feel — fonts, colors, header, footer — is the workspace company's brand. This is not the prospect's document; it is the workspace company's document about them.

## Principles

Follow these standards during generation. Read each before producing output.

**Content and language:**
- [Editorial rules](../shared/editorial-rules.md) — no AI-isms, banned vocabulary, honest analyst tone
- [Information principles](../shared/information-principles.md) — lead with conclusions, evidence-backed claims, narrative arc

**Visual design:**
- [Presentation principles](../shared/presentation-principles.md) — typography, layout, visual restraint
- [One-pager format](../shared/formats/one-pager.md) — print-first, above-the-fold, managed density

**Octave data:**
- [Octave value](../shared/octave-value.md) — prioritize grounded workspace data over generic AI content

Apply these rules during generation, not just at review. After generating, the **review pipeline is a mandatory gate** (see Step 5) — the one-pager is not opened or delivered until the scorecard is produced.

**Testing & regression:**
- [Testing protocol](references/testing-protocol.md) — how to improve this skill through real outputs (Phase 1: tear one apart, Phase 2: verify changes generalize)
- [Regression checklist](references/regression-checklist.md) — issues found during testing, verified against every new generation

## Usage

```
/octave:one-pager <target> [--for <occasion>] [--style <preset>]
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

**Call as many tools as needed to build a complete picture.** The best one-pagers come from layering multiple sources -- company enrichment + Motion ICP cell narrative + proof points + conversation intel all combine to create a document that feels genuinely personalized. Don't stop at one tool when three would give you a stronger narrative.

That said, not every tool applies to every one-pager. Use your judgment about which are relevant to *this specific* situation. The tables below show what's available -- pick the combination that gives you the richest context for the occasion and target.

See [tool-reference.md](references/tool-reference.md) for list-vs-search guidance, follow-up grounding tools, and the tool reference tables for account-specific and segment-level one-pagers.

**Output of this step:** Present a content outline to the user for approval. See [outline-template.md](references/outline-template.md) for the outline template.

**Wait for user approval before proceeding.**

### Step 3: Style Selection

One-pagers use the same 12 style presets and brand extraction system as the deck skill. See [style-presets.md](../shared/style-presets.md) for full CSS variable definitions.

Ask the user:

```
How would you like to style the one-pager?

1. Pick from presets — 12 styles from dark executive to light minimal
2. Use a brand — mine (the sender) or the recipient's; extract from a website or provide assets
3. Auto-pick — I'll choose based on the occasion and tone
4. Surprise me

Your choice:
```

**Option 1: Preset Picker** -- Show the same preset table from the deck skill (see `/octave:deck` Step 4, Option 2).

**Option 2: Brand Extraction** -- Follow the same brand discovery flow from the deck skill (see `/octave:deck` Step 3): Tier 1 `get_external_brand_assets` (colors + logo, with a customer-logo sanity check), Tier 2 `scrape_website` with `includeScreenshot` for fonts + components, then browser-use / WebFetch / manual fallbacks. Confirm brand config with user before proceeding.

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

The entire `.octave-one-pagers/` directory is in `.gitignore` -- nothing here gets committed.

#### HTML Architecture

See [html-architecture.md](references/html-architecture.md) for the HTML/CSS scaffold and key differences from the deck skill's HTML.

#### Document Sections

See [document-sections.md](references/document-sections.md) for per-section HTML templates (Header, The Problem Today, How [Product] Helps, Key Differentiators, What Teams Are Seeing, Next Step).

#### Content Density Rules

Keep it tight. A one-pager should be scannable in under 2 minutes:

| Section | Max Content |
|---------|------------|
| Header | Company name + title + date + "Prepared for" |
| The Problem Today | 2-3 sentences max |
| How [Product] Helps | 3-4 value props, each 1-2 sentences |
| Key Differentiators | 3 cards max, each heading + 1-2 sentences |
| What Teams Are Seeing | 2-3 metrics or quotes |
| Next Step | 1 CTA + contact info |

If content exceeds these limits, prioritize ruthlessly. The one-pager is a teaser, not a whitepaper.

**After writing the file, proceed immediately to Step 5 (Review Pipeline). Do NOT open the file in the browser or present the delivery summary yet.**

### Step 5: Review Pipeline — MANDATORY GATE

**Do NOT open the one-pager in the browser, present the delivery summary, or tell the user it is ready until the review pipeline has completed and you have a scorecard.**

Load the [review protocol](../shared/protocol.md) and execute the review loop against the generated HTML file. One-pager-specific wiring:

**5a: Mechanical lint** (before spawning reviewers):

```bash
bash <skill-dir>/scripts/lint.sh <path-to-one-pager.html>
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
           3. [skill-dir]/references/regression-checklist.md
           A one-pager is a teaser, not a whitepaper — hold every section to its density limit.
           Fix violations inline. Return scorecard."
```

**Presentation reviewer:**
```
Task tool:
  subagent_type: "octave-presentation-reviewer"
  prompt: "Review the file at [FILE PATH].
           Read these docs and run each Review Checklist:
           1. [skill-dir]/../shared/presentation-principles.md
           2. [skill-dir]/../shared/formats/one-pager.md
           3. [skill-dir]/references/html-architecture.md
           4. [skill-dir]/references/document-sections.md
           5. [skill-dir]/references/regression-checklist.md
           Verify it holds up as a print-first, above-the-fold leave-behind.
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

### Research & Enrichment
- `enrich_company` - Full company intelligence profile
- `enrich_person` - Full person intelligence report
- `find_person` - Find contacts at a company by title/role
- `qualify_company` - ICP fit scoring for a company
- `qualify_person` - ICP fit scoring for a person
- `find_company` - Find companies matching criteria

### Library -- Fetching Entities
- `list_entities` - Quick scan of all entities of a type (minimal fields, no pagination)
- `list_entities` - Fetch entities with full data and pagination (proof points, references, personas, etc.)
- `get_entity` - Deep dive on one specific entity

### Motions
- `list_motions` - Motions for the offering
- `list_motion_playbooks` - Default + Custom Motion Playbooks under a Motion
- `get_motion_playbook` - Full Motion Playbook details
- `list_motion_icps` - Persona × segment matrix for a Motion
- `find_motion_icp` - Full per-cell narrative + Learning Loop learnings

### Library -- Searching
- `search_knowledge_base` - Semantic search across library entities and resources
- `list_resources` - Browse uploaded docs, URLs, and Google Drive files
- `search_resources` - Semantic search across uploaded resources

### Intelligence & Signals
- `list_findings` - Recent conversation findings and insights
- `list_events` - Deal events (won, lost, created, etc.)
- `get_event_detail` - Full details for a specific event

### Content Generation
- `generate_call_prep` - Synthesized prep brief for accounts
- `generate_content` - Generate positioning or messaging content

### Brand & Style
- `list_entities` (entityType: "brand_voice") - Available brand voices in workspace
- `list_writing_styles` - Available writing styles in workspace

## Error Handling

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The one-pager builder can still work without Octave -- you'll provide the content manually, and I'll handle structure, style, and HTML generation.
>
> To reconnect: check your Octave MCP configuration and reconnect

**Company/Person Not Found:**
> I couldn't find detailed intelligence for [target].
>
> Options:
> 1. Proceed with what we have -- I'll use general positioning from your library
> 2. Try a different domain or email
> 3. Provide the content manually and I'll build the one-pager

**No Matching Motion ICP Cell:**
> No Motion ICP cell matches this audience profile directly.
>
> I'll use your general positioning. After the one-pager is built, consider layering a Custom Motion Playbook (Thematic / Milestone / Account / Competitive) on the relevant Motion for this angle: `/octave:library create motion-playbook`

**No Proof Points Available:**
> No proof points found matching this account's industry or segment.
>
> Options:
> 1. Proceed without the proof points section
> 2. Use general proof points from your library
> 3. Provide customer results manually and I'll format them

**No Findings for Follow-Up:**
> No conversation findings found for [target] in the recent period.
>
> This means I'll build the one-pager from enrichment data and library content rather than grounding it in specific past conversations. You can provide meeting notes or context manually if you have them.

## Related Skills

- `/octave:deck` - Full presentation deck (when one page isn't enough)
- `/octave:research` - Deeper research on the account
- `/octave:research --format html` - Internal account dossier (vs external leave-behind)
- `/octave:proposal` - Formal business case
- `/octave:microsite` - Personalized web page for ABM
