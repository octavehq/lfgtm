---
name: deck
description: Octave-powered presentation builder that researches, structures, and generates self-contained HTML slide decks. Use when user says "build a deck", "create a presentation", "pitch deck", "QBR slides", "sales deck", or asks for slides on any topic.
---

# /octave:deck - Octave-Powered Deck Builder

Build compelling, self-contained HTML presentations powered by your Octave GTM knowledge base. Unlike generic slide builders, this skill leverages your library's personas, competitors, Motion ICP narratives, proof points, and real conversation data to research, structure, and generate presentations grounded in your actual go-to-market intelligence.

> HTML presentation engine inspired by [frontend-slides](https://github.com/zarazhangrui/frontend-slides) by Zara Zhang (MIT license). Decks render on a **fixed 1920×1080 stage scaled to the viewport** (see [references/viewport-base.css](references/viewport-base.css)).

## On-brand styling — use a brand kit if one exists

Before generating, decide whose brand this deck should match (usually the **target company**; sometimes your own company). Then:

1. Resolve the company to a `<slug>` and check for a cached brand kit at `~/.octave/brands/<slug>/manifest.json`.
2. **If a kit exists →** offer it: *"I found a saved brand kit for <Company> — want this deck rendered in their brand?"* If yes, style the output with the kit instead of a generic preset:
   - inline the kit's `tokens.css` (`:root` + the embedded `@font-face`) **and** `get-brand-components/assets/kit_base.css` into the output `<style>`;
   - follow `brand-kit.md` → **Signature moves**, and reuse the kit's real **logo**, `images/`, and `icons.json`;
   - for doc-shaped output you can compose directly with `get-brand-components/scripts/render_kit.py` (hero / split / logos / pricing / cta / footer blocks).
3. **If no kit exists →** offer to build one first: *"No brand kit for <Company> yet — want me to capture it (~1 min) so this is on-brand?"* → run `/octave:get-brand-components <domain>`, then proceed.
4. **If the user declines →** generate with the default style/preset.

> The brand kit is the strongest styling signal — when one is available, prefer it over generic `--style` presets. See the `get-brand-components` skill for the kit format, token contract, and renderer.

## Optional review pass

After generating the asset, **offer** an optional review (don't force it): *"Want me to run a quick review pass over this — layout, brand, narrative, groundedness, and AI-slop?"* If yes, follow [`get-brand-components/references/asset-review.md`](../get-brand-components/references/asset-review.md): render/screenshot the output, inspect it across the five dimensions (render the pixels and actually look — overflow and white-on-white only show in the render), report a short scorecard of specific located findings, then fix and re-verify. Skip silently if the user declines.

When generating, follow the output rules in [`get-brand-components/references/presentation-principles.md`](../get-brand-components/references/presentation-principles.md) — the generation-time companion to the review pass (label every value, no tool names in the output, confirmed vs hypothesized, lean and deal-specific).

## Usage

```
/octave:deck [topic or file] [--for <purpose>] [--audience <target>] [--style <preset>]
```

## Examples

```
/octave:deck "pitch for Acme Corp"                          # Customer pitch, Octave researches Acme
/octave:deck "Q1 QBR for enterprise segment"                # QBR with real pipeline data
/octave:deck --for competitive "vs Gong"                     # Competitive presentation
/octave:deck "product launch GTM plan"                       # Internal strategy deck
/octave:deck ~/Downloads/existing-deck.pptx                  # Convert PPTX to HTML
/octave:deck "demo day pitch" --style octave-brand           # Specific style preset
/octave:deck "sales kickoff enablement" --audience "new AEs" # Audience-targeted
```

## Instructions

When the user runs `/octave:deck`:

### Step 1: Understand the Purpose & Goal

If not provided via flags, ask the user interactively using AskUserQuestion:

**Purpose — "What kind of deck is this?"**

```
What kind of deck are you building?

1. Customer pitch / pre-demo deck
2. Customer QBR / business review
3. Internal strategy / planning
4. Conference talk / keynote
5. Product launch / GTM plan
6. Competitive battlecard presentation
7. Sales enablement / training
8. Something else (describe it)

Your choice:
```

**Goal — "What's the outcome you want?"**

```
What outcome should this deck drive?

1. Close a deal / advance an opportunity
2. Educate / enable a team
3. Get executive buy-in
4. Win a competitive deal
5. Launch a product or campaign
6. Other (describe it)

Your choice:
```

**Audience — "Who is this for?"**

```
Who's the audience?

Provide any of the following:
• Company name or domain (e.g., acme.com)
• Person name or email (e.g., jane@acme.com)
• Role/title description (e.g., "VP Sales at mid-market SaaS")
• General audience (e.g., "internal sales team", "board of directors")

Target:
```

**Content readiness — "How much do you have already?"**

```
How much content do you have?

1. I have content ready — I'll paste or describe it
2. I have rough notes — I'll share, you help me structure
3. Help me figure it out — Octave drives the content strategy
4. I have a PPTX file — convert and enhance it

Your choice:
```

If a `.pptx` file is provided, jump to the [PPTX Conversion Path](#pptx-conversion-path) before continuing.

**Length — "How long should this be?"**

If the user provided existing content (PPTX, notes, or pasted content), offer to keep, shorten, or expand:

```
Your source has ~[N] slides worth of content. What length do you want?

1. Keep similar — stay around [N] slides
2. Shorter — condense to the essentials
3. Longer — expand with more detail and data
4. Custom — I have a specific slide count in mind

Your choice:
```

If starting from scratch, ask based on purpose:

```
How long should this deck be?

1. Short (5-8 slides) — punchy, high-impact, perfect for pitches and exec summaries
2. Medium (10-15 slides) — standard for most presentations
3. Long (18-25 slides) — detailed deep-dives, enablement, or QBRs
4. Custom — I have a specific slide count in mind

Your choice:
```

| Purpose | Recommended Default |
|---------|-------------------|
| Customer pitch / pre-demo | Short (5-8) |
| Customer QBR / review | Long (18-25) |
| Internal strategy | Medium (10-15) |
| Conference keynote | Medium (10-15) |
| Product launch / GTM | Long (18-25) |
| Competitive battlecard | Short (5-8) |
| Sales enablement | Long (18-25) |

Use the recommended default as the pre-selected option. If the user picks "Custom," ask for a target slide count.

**Density — "How should each slide read?"**

```
How dense should each slide be?

1. Speaker-led (low density) — big ideas, generous space, 1-3 bullets max,
   more slides. Best for live pitches, keynotes, exec rooms.
2. Reading-first (high density) — self-contained, structured grids,
   4-8 bullets or 4-6 cards, tighter spacing. Best for QBRs, async/leave-behind decks.

Your choice:
```

Default by purpose: pitches/keynotes/competitive → **speaker-led**; QBRs/enablement/launch/strategy → **reading-first**. Carry this choice through Step 5: it drives the content density limits per slide type (split into more slides rather than shrink text or overflow). Either way, no scrolling and no cramped text — the fixed stage scales the whole slide, it does not add room.

### Step 2: Octave-Powered Context Gathering

Based on purpose, goal, and audience, use Octave MCP tools to build rich context for the deck. **Always tell the user what you're researching and why.**

**Call as many tools as needed to build a complete picture.** The best decks come from layering multiple sources — company enrichment + Motion ICP narrative + proof points + conversation intel all combine to create slides grounded in real data. Don't stop at one tool when three would give you a stronger narrative.

That said, not every tool applies to every deck. Use your judgment about which are relevant to *this specific* situation. The tables below show what's available — pick the combination that gives you the richest context for the deck type and audience.

**List vs Search — when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_all_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory — "show me all our personas" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content — "get full proof point details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept or question — "how do we compete in healthcare?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material, uploaded assets, or source docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

**Follow-up decks — ground them in what actually happened:**

If this deck follows a previous interaction with the account (QBR, follow-up after a demo, deal review, renewal pitch), pull findings and events to anchor the narrative in real data rather than generic positioning:

- `list_findings({ query: "<company or contact>", startDate: "<relevant period>" })` — surfaces what was actually said in calls: objections raised, features requested, pain points confirmed, competitor mentions
- `list_events({ filters: { accounts: ["<account_oId>"] } })` — deal stage changes, meetings held, emails sent — shows the journey so far
- `get_event_detail({ eventOId })` — deep dive on specific events (e.g., the discovery call, the demo) to pull exact context

This turns a generic "here's our product" deck into "here's what we heard from you, and here's how we're addressing it" — much more compelling for the audience.

---

#### For Customer-Facing Decks (pitch, demo, QBR)

Start with company and person enrichment, then pull positioning context as needed:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Company profile | `enrich_company({ companyDomain })` | Almost always — gives industry, size, tech stack, signals |
| Key contacts | `find_person({ searchMode: "people", companyDomain, fuzzyTitles })` | When audience includes unknown stakeholders |
| Person deep-dive | `enrich_person({ person: { email, firstName, lastName, companyDomain } })` | When a specific person is the target audience |
| ICP fit scoring | `qualify_company({ companyDomain })` | When you need to frame "why us" for this account |
| All Motions | `list_motions()` | Quick scan of Motions to find the right one for this account |
| Motion Playbooks | `list_motion_playbooks({ motionOId })` | Default + Custom Motion Playbooks for the selected Motion |
| Motion Playbook details | `get_motion_playbook({ motionPlaybookOId })` | Full Motion Playbook narrative content |
| Motion ICP cells | `list_motion_icps({ motionOId })` | Persona × segment cells under a Motion |
| Motion ICP narrative | `find_motion_icp({ motionIcpOId, includeLearnings: true })` | Cell-level Target ICP / Strategic narrative / Pains / Benefits / Methodology / References + Learning Loop learnings |
| All proof points | `list_entities({ entityType: "proof_point" })` | Fetch actual proof points with full data — metrics, quotes, logos |
| All references | `list_entities({ entityType: "reference" })` | Fetch customer references with full details |
| Find proof points by topic | `search_knowledge_base({ query: "<industry> results", entityTypes: ["proof_point", "reference"] })` | When you need proof points *about* a specific topic or industry |
| Competitive context | `search_knowledge_base({ query: "<signals>", entityTypes: ["competitor"] })` | When competitor is mentioned or likely in the deal |
| Uploaded resources | `search_resources({ query: "<topic>" })` | When the workspace has uploaded docs, one-pagers, or assets relevant to the deck |
| Recent intel | `list_findings({ query: "<company>", startDate: "<90 days ago>" })` | When you want conversation-based insights |
| Synthesized prep | `generate_call_prep({ companyDomain })` | When you want a single comprehensive brief to work from |

---

#### For Internal Decks (strategy, planning, launch)

Pull from the library to ground the deck in your actual GTM data:

| What you need | Tool | When to use |
|---------------|------|-------------|
| Personas | `list_all_entities({ entityType: "persona" })` | Quick scan of all personas |
| Persona details | `list_entities({ entityType: "persona" })` | Full persona data — pain points, priorities, messaging |
| Segments | `list_all_entities({ entityType: "segment" })` | Quick scan of market segments |
| Competitors | `list_all_entities({ entityType: "competitor" })` | Quick scan of competitive landscape |
| Products | `list_all_entities({ entityType: "product" })` | Quick scan of product capabilities |
| Use cases | `list_all_entities({ entityType: "use_case" })` | When deck covers how customers use the product |
| Entity details | `get_entity({ oId })` | Deep dive on any specific entity found above |
| Positioning by topic | `search_knowledge_base({ query: "<topic>", entityTypes: ["product"] })` | When you have a concept and need relevant positioning |
| Motions | `list_motions()` | Available Motions to ground the deck in |
| Motion Playbooks | `list_motion_playbooks({ motionOId })` and `get_motion_playbook({ motionPlaybookOId })` | Default + Custom Motion Playbook narrative content |
| Motion ICP narratives | `list_motion_icps({ motionOId })` then `find_motion_icp({ motionIcpOId })` | Persona × segment narrative grounded in the library |
| Proof points | `list_entities({ entityType: "proof_point" })` | Fetch all proof points with full data for credibility slides |
| References | `list_entities({ entityType: "reference" })` | Fetch customer references for social proof slides |
| Uploaded docs | `search_resources({ query: "<topic>" })` | Find uploaded strategy docs, market research, or assets |
| Market signals | `list_findings({ query: "<topic>", startDate: "<90 days ago>" })` | Recent conversation-based trends |
| Deal outcomes | `list_events({ startDate: "<90 days ago>", filters: { eventTypes: ["DEAL_WON", "DEAL_LOST"] } })` | Pipeline, revenue, or win/loss data |

---

#### For Competitive Decks (battlecard presentations)

Focus on the specific competitor(s) and evidence from real deals:

| What you need | Tool | When to use |
|---------------|------|-------------|
| All competitors | `list_all_entities({ entityType: "competitor" })` | Quick scan of all competitors |
| Competitor full data | `list_entities({ entityType: "competitor" })` | Full competitor profiles — strengths, weaknesses, positioning |
| Competitor deep dive | `get_entity({ oId })` | Everything about one specific competitor |
| Competitive positioning | `search_knowledge_base({ query: "<competitor> differentiation", entityTypes: ["competitor"] })` | When you have a concept — "how do we beat them on security?" |
| Our products | `list_entities({ entityType: "product" })` | Full product data for side-by-side comparison slides |
| Proof points (competitive wins) | `list_entities({ entityType: "proof_point" })` | Fetch all proof points — filter for competitive wins |
| Win/loss data | `list_events({ filters: { eventTypes: ["DEAL_WON", "DEAL_LOST"], competitors: ["<oId>"] } })` | Real deal outcomes against this competitor |
| Conversation evidence | `list_findings({ query: "<competitor>", eventFilters: { competitors: ["<oId>"] } })` | Real objections and mentions from calls |
| Custom Motion Playbooks (COMPETITIVE) | `list_motions()` then `list_motion_playbooks({ motionOId })` filtered by `narrativeType === "COMPETITIVE"` | Competitive narrative layered onto each Motion |
| Motion Playbook details | `get_motion_playbook({ motionPlaybookOId })` | Full competitive narrative content |
| Competitive resources | `search_resources({ query: "<competitor>" })` | Uploaded battlecards, analyst reports, or competitive docs |

---

#### For Enablement Decks (training, sales kickoff)

Mix Motion ICP narrative content with real deal examples:

| What you need | Tool | When to use |
|---------------|------|-------------|
| All Motions | `list_motions()` | Scan available Motions to decide which to teach |
| Motion Playbooks | `list_motion_playbooks({ motionOId })` and `get_motion_playbook({ motionPlaybookOId })` | Default + Custom Motion Playbook content for training slides |
| Motion ICP narratives | `list_motion_icps({ motionOId })` then `find_motion_icp({ motionIcpOId, includeLearnings: true })` | Cell-level narratives + Learning Loop learnings for training slides |
| Personas | `list_entities({ entityType: "persona" })` | Full persona data for "know your buyer" slides |
| Competitors | `list_entities({ entityType: "competitor" })` | Full competitor data for competitive handling slides |
| All proof points | `list_entities({ entityType: "proof_point" })` | Fetch proof points with full data for example slides |
| Proof points by topic | `search_knowledge_base({ query: "results metrics", entityTypes: ["proof_point", "reference"] })` | When you need proof points *about* specific outcomes |
| Recent wins | `list_events({ filters: { eventTypes: ["DEAL_WON"] } })` | Success stories to use as examples |
| Win details | `get_event_detail({ eventOId })` | Deep dive on a notable win for a case study slide |
| Training resources | `search_resources({ query: "<topic>" })` | Uploaded enablement docs, Motion Playbook reference PDFs, or training assets |

---

**Output of this step:** Present a structured content brief to the user:

```
DECK OUTLINE: [Title]
=====================

Purpose: [Purpose from Step 1]
Audience: [Target audience]
Goal: [Desired outcome]
Length: [Short/Medium/Long/Custom] — [N] slides
Source: [From scratch / User content / PPTX conversion]

---

NARRATIVE ARC
-------------
1. HOOK — [Opening that captures attention]
2. PROBLEM — [Pain point or challenge]
3. SOLUTION — [How you solve it]
4. PROOF — [Evidence and social proof]
5. ASK — [Clear next step / CTA]

---

SLIDE-BY-SLIDE OUTLINE
-----------------------

Slide 1: [Title Slide]
• [Headline]
• [Subtitle/context]

Slide 2: [Problem/Challenge]
• [Key point 1]
• [Key point 2]
• [Data point from Octave]

Slide 3: [Solution Overview]
• [Value prop 1]
• [Value prop 2]
• [Value prop 3]

[Continue for all slides...]

---

Octave Sources Used:
• Company profile: [Company name] — [key insights]
• Motion / Motion ICP: [Motion name + persona × segment cell] — [key messaging angle]
• Proof points: [N] references pulled
• Competitive intel: [If applicable]
• Findings: [N] recent signals

---

Does this outline look good? I can:
1. Proceed to style selection and generation
2. Add/remove/reorder slides
3. Go deeper on any section
4. Change the narrative angle
```

**Wait for user approval before proceeding.**

### Step 3: Brand Discovery (Optional)

Ask the user:

```
Whose brand should this deck reflect — and how should we style it?

1. My brand (the sender) — extract from my website (give the URL)
2. The audience's brand — mirror the recipient's company so the deck feels built for them (give *their* URL). Common for customer pitches and ABM.
3. I'll provide brand assets directly (colors, fonts, logo)
4. No brand — pick from style presets
5. Use Octave brand styling

Your choice:
```

> **Whose brand decides which website you fetch.** This is the key fork: for option 1 run the extraction against *your own* domain; for option 2 run it against the *audience's/recipient's* domain. Everything below targets that chosen domain.

If user wants brand extraction, work down these tiers — start at Tier 1 and only fall through when a tier is unavailable. Tiers 1–2 are the fast, high-quality path; combine both when you can (colors+logo from Tier 1, fonts+components from Tier 2).

**Tier 1: Octave brand-assets tool (first-party, fast — try first)**
```
get_external_brand_assets({ url: "https://<domain>" })
  → colors (primary / secondary / accent), logo variants, backdrop images, brand name
get_external_brand_logo({ domain: "<domain>" })   # if you only need the single best logo
```
This is one call for the visual identity and the right default. **Sanity-check the result — the scraper reads the DOM and can misattribute a homepage logo wall:**
- If `brandName` doesn't match the target company, ignore it (it likely grabbed a customer name).
- A strip of many logos with varied aspect ratios is usually a **"trusted by" customer wall**, not the brand's own logo — don't use those as the deck logo. Prefer the `favicon` / `apple-touch-icon` entries or the nav wordmark.
- The `colors` are usually reliable; still confirm with the user.

**Tier 2: `scrape_website` — components & typography (the "looks like their site" leap)**
```
scrape_website({ url: "https://<domain>",        format: "html", includeScreenshot: true })
scrape_website({ url: "https://<representative-page>", format: "html", includeScreenshot: true })
```
Pull the homepage **and one representative page** (case study, blog post, pricing, or product page). Then:
- **From the screenshot(s):** read the component vocabulary the DOM hides — button shapes, card styles, corner radii, spacing rhythm, type scale, section patterns, use of gradients/imagery. Emulate this *component and layout system*, not just the colors.
- **From the html:** extract exact fonts (`font-family`, Google Fonts `<link>`s / `@font-face`), CSS custom properties (`--brand-*`, `--color-*`), and the real copy tone.

> If `scrape_website` isn't available in this workspace yet, skip to Tier 3.

**Tier 3: browser-use (fallback if `scrape_website` unavailable)**
```
1. browser-use open <website-url>
2. browser-use screenshot brand-capture.png
3. browser-use eval "(() => {
     const body = getComputedStyle(document.body);
     return {
       bgColor: body.backgroundColor, textColor: body.color, fontFamily: body.fontFamily,
       links: getComputedStyle(document.querySelector('a') || document.body).color,
       headings: getComputedStyle(document.querySelector('h1,h2,h3') || document.body).fontFamily,
       logos: [...document.querySelectorAll('header img, img[src*=logo], svg[class*=logo]')].map(e => e.src || 'inline-svg').slice(0, 3)
     };
   })()"
4. browser-use extract "List the primary brand colors (hex), fonts, and logo URLs visible on this page"
```

**Tier 4: WebFetch (fallback if browser-use unavailable)**
```
1. WebFetch the homepage URL
2. Parse HTML/CSS for CSS custom properties (--brand-*, --color-*), font-family on body/h1-h3,
   logo URLs from <img>/<svg>/og:image, and meta theme-color
```

**Tier 5: Manual (if nothing automated works)**
```
I couldn't automatically extract your brand. You can:
1. Share your brand guidelines (PDF or link)
2. Provide hex colors: primary, secondary, background, text
3. Name your fonts (heading + body)   4. Share logo files
```

**Always confirm the brand config with the user before proceeding:**

```
BRAND CONFIG EXTRACTED
======================

Colors:
  Primary:    #XXXXXX ██   Secondary: #XXXXXX ██   Accent: #XXXXXX ██
  Background: #XXXXXX ██   Text:      #XXXXXX ██

Fonts:    Headings: [Font name]    Body: [Font name]

Logo:     [URL or file path]   (verified as the brand's own, not a customer logo)

Components observed (from screenshots, if Tier 2 ran):
  • [e.g. pill buttons, 12px card radius, generous section spacing, gradient accents]

Does this look right? (y/n/adjust)
```

### Step 4: Style Selection

Ask the user how they want to choose their style:

```
How would you like to choose your style?

1. Show me options — I'll generate preview slides based on your mood
2. I know what I want — pick from 12 presets
3. Use my brand — auto-generate from brand extraction
4. Surprise me — I'll pick based on your deck purpose

Your choice:
```

---

#### Option 1: Mood-Based Previews

Ask:
```
What impression should the deck make?

1. Impressed — premium, polished, high-stakes
2. Excited — energetic, bold, forward-looking
3. Calm — clean, trustworthy, understated
4. Inspired — creative, visionary, memorable

Your mood:
```

Generate **3 single-slide HTML preview files** — show, don't tell. Each is a real, animated **title slide using the user's actual first-slide content** (title, subtitle, date, author, logo if available). Never render "Option A", "preview", a preset/template name, or any file path *on the slide itself*. Save to `.octave-decks/slide-previews/` as `style-a.html`, `style-b.html`, `style-c.html`, built on the **fixed 1920×1080 stage** (paste `viewport-base.css`).

**Preview mix:** generate previews from the mood-matched presets in [references/style-presets.md](references/style-presets.md), optionally swapping one for a custom wildcard:

| Mood | Preview presets |
|------|----------------|
| Impressed | `midnight-pro`, `executive-dark`, `octave-brand` |
| Excited | `electric-studio`, `neon-pulse`, `solar-flare` |
| Calm | `swiss-modern`, `soft-light`, `paper-minimal` |
| Inspired | `dark-botanical`, `aurora-gradient`, `monochrome-bold` |

For more range, make one of the three a **custom wildcard** — a self-generated design that follows the no-slop rules (distinctive typography, avoid Inter/Roboto/system fonts; a committed palette, no generic purple-on-white; a recognizable layout system on the fixed 16:9 stage). If brand was extracted in Step 3, add a **4th brand-themed preview**.

Open all previews in the browser for the user to compare, then ask which they prefer (or which elements to mix).

---

#### Option 2: Preset Picker

Show the preset table:

```
STYLE PRESETS
=============

DARK THEMES
  1. midnight-pro      — Dark navy, white text, blue accents. Executive feel.
  2. executive-dark    — Charcoal + gold. Premium boardroom aesthetic.
  3. octave-brand      — Octave purple on dark navy. Product-aligned.
  4. electric-studio   — Pure black + electric blue. Tech-forward.
  5. neon-pulse        — Dark + neon green/cyan. Developer/hacker energy.
  6. dark-botanical    — Dark + warm gold/rose. Elegant and premium.

LIGHT THEMES
  7. swiss-modern      — White + red accent. Bauhaus minimal.
  8. soft-light        — Warm white + sage green. Calm and approachable.
  9. paper-minimal     — Off-white + black type. Editorial simplicity.

VIBRANT THEMES
  10. solar-flare      — Deep orange gradients. Bold and energetic.
  11. aurora-gradient   — Purple-to-teal gradients. Visionary and modern.
  12. monochrome-bold  — High-contrast B&W. Statement typography.

Your choice (number or name):
```

Full CSS variable definitions for each preset are in [references/style-presets.md](references/style-presets.md).

---

#### Option 3: Brand-Generated Style

Auto-generate CSS variables from the brand config extracted in Step 3:

```
- --bg: [brand background or dark variant]
- --bg-elevated: [slightly lighter than bg]
- --bg-card: [semi-transparent card bg]
- --text-primary: [brand text color]
- --text-secondary: [muted variant]
- --brand-primary: [primary brand color]
- --brand-500: [lighter accent]
- --font-display: [brand heading font]
- --font-body: [brand body font]
```

Show the generated style to the user for confirmation.

---

#### Option 4: Auto-Pick

Map deck purpose to recommended presets:

| Purpose | Recommended Preset |
|---------|--------------------|
| Customer pitch | `midnight-pro` |
| Customer QBR | `executive-dark` |
| Internal strategy | `octave-brand` |
| Conference keynote | `electric-studio` |
| Product launch | `aurora-gradient` |
| Competitive battlecard | `neon-pulse` |
| Sales enablement | `soft-light` |

Tell the user what you picked and why. Let them override.

### Step 5: Generate Presentation

Build a single, self-contained HTML file. **No external dependencies.** Everything inlined.

#### Output Directory

Every deck gets its own folder under `.octave-decks/`:

```
.octave-decks/
├── slide-previews/                    # temp style previews (cleaned up after selection)
└── <kebab-case-name>-<YYYY-MM-DD>/   # one folder per deck
    ├── <name>.html                    # final HTML presentation
    ├── <name>.pptx                    # PPTX export (if requested)
    ├── <name>-carousel.html           # LinkedIn carousel version (if requested)
    ├── <name>-content.md              # markdown export (if requested)
    └── assets/                        # images (from PPTX conversion or user-provided)
```

Example: `/octave:deck "pitch for Acme Corp"` → `.octave-decks/acme-corp-pitch-2026-02-07/acme-corp-pitch.html`

The entire `.octave-decks/` directory is in `.gitignore` — nothing here gets committed.

#### HTML Architecture

See [html-scaffold.md](references/html-scaffold.md) for the full scaffold. **Two non-negotiables:**

1. **Paste the entire [viewport-base.css](references/viewport-base.css)** into the `<style>` block. It provides the `.deck-viewport` → `.deck-stage` (1920×1080) → `.slide` system, `.active`/`.visible` visibility, print-one-slide-per-page, and reduced-motion.
2. **Author every slide at 1920×1080 in px** — no `clamp()`, `vw`, or `vh` for layout. The stage scales as a whole to fit any screen.

#### Fixed-Canvas Fitting (Critical)

Every slide is a fixed 1920×1080 canvas; the controller scales the whole stage. Fit is achieved by **density discipline**, not responsive math:

1. **Size in px against the 1920×1080 canvas.** A title is ~96–120px, body ~24–32px, slide padding ~80×140px. Translate any `clamp()`/`vw` from a preset or custom design into fixed px.
2. **`overflow: hidden` on every `.slide`** (from viewport-base.css) — anything that doesn't fit is clipped, so it must fit by design.
3. **Content density limits per slide type** (tighten for *speaker-led*, allow the upper bound for *reading-first* — see Step 1 density choice):

| Slide Type | Max Content |
|-----------|------------|
| Title | 1 heading + 1 subtitle (2-3 lines max) |
| Section Divider | 1 big heading + 1 subtitle. Chapter break. |
| Content | 1 heading + 4-6 bullet points |
| Grid/Cards | 1 heading + 6 cards maximum |
| Quote | 1 quote (3 lines max) + attribution |
| Metric | 1 heading + 3-4 big numbers |
| Comparison | 1 heading + 2-column layout (6 rows max) |
| Timeline/Process | 1 heading + 4-6 steps (label + short description each) |
| Logo Wall | 1 heading + 8-12 logos in a grid |
| Image | 1 heading + 1 image + 1 caption |
| Agenda/TOC | 1 heading + 5-8 agenda items |
| CTA/Closing | 1 heading + 1-2 lines + 1 action |

4. **If content exceeds limits — split into more slides.** Never shrink text below readable size and never overflow.
5. **Verify before delivery.** If browser-use is available, open the deck and screenshot a few slides to check for clipped text or overlapping panels (a card can pass a height check while still being covered by another grid panel). Fix by splitting or reducing content.

#### Animation Patterns

Reveals are triggered by the `.visible` class the controller toggles on the active slide (no Intersection Observer — slides switch via `.active`/`.visible`, not scroll):

```css
.animate-in {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s var(--ease), transform 0.6s var(--ease);
}
.slide.visible .animate-in { opacity: 1; transform: translateY(0); }
/* Stagger children */
.slide.visible .animate-in:nth-child(1) { transition-delay: 0.1s; }
.slide.visible .animate-in:nth-child(2) { transition-delay: 0.2s; }
.slide.visible .animate-in:nth-child(3) { transition-delay: 0.3s; }
/* ... up to 8 */
```

Match motion to the chosen style (see [references/animation-patterns.md](references/animation-patterns.md) for the effect-to-feeling guide and snippets: fade/slide, scale-in, blur-in, gradient-mesh backgrounds, 3D tilt). Use extras sparingly: counter animations for metrics, draw-in for borders, fade-scale for cards. `prefers-reduced-motion` is already handled by viewport-base.css.

#### Navigation Implementation

A small `SlidePresentation` controller (in the scaffold) handles everything — **no scroll-snap, no nav dots**:

```javascript
// 1. Stage scaling: transform = translate(x,y) scale(min(vw/1920, vh/1080)); re-fit on resize
// 2. show(i): toggle .active + .visible on the target slide (re-runs .animate-in reveals)
// 3. Keyboard: ArrowRight/PageDown/Space = next; ArrowLeft/PageUp = prev; Home/End; R = reset
// 4. Touch: swipe left/right
// 5. #deckControls (outside the stage, so it isn't scaled): "n / total" + prev/next buttons
```

#### Avoid AI Slop

Whether using a preset or a custom wildcard, the output should look intentional, not generated:

- **Fonts:** avoid Inter, Roboto, Arial, and raw system fonts for *custom* looks. Reach for distinctive display faces (Fontshare/Google Fonts). (Brand presets that specify a brand font are fine.)
- **Color:** commit to a palette with a sharp accent — avoid generic purple-gradient-on-white and timid washes.
- **Layout:** vary slide types; avoid cookie-cutter "title + 3 bullets" on every slide.
- **Context:** the design should fit the occasion and audience (a board deck and a hackathon demo should not look alike).

**Copy is held to the same bar as visuals.** Every word a viewer reads (headline, body, caption, pill, metric label) must pass the slop standard in [`get-brand-components/references/asset-review.md`](../get-brand-components/references/asset-review.md) → WRITE_LIKE_A_HUMAN. Two rules break most decks, so treat them as hard rules, not preferences, and fix them in the review pass rather than excusing them as "headline style":

1. **No em dashes in deck copy, headlines included.** Both `&mdash;` and the literal `—`. Use a comma, colon, period, or two sentences. Hyphenated compounds (`go-to-market`) and arrows (`6mo → 3wk`) are fine.
2. **At most one negative-contrast construction in the whole deck.** "It's not X, it's Y", "this isn't about X, it's Y", "The X wasn't the hard part. The Y was." Keep the single strongest one (usually the title hook); state every other point positively.

#### Inline Editing (included by default)

Add a lightweight in-browser editor so the user can tweak copy without touching code. Do **not** ask about it during intake — include it unless the user requested a locked/export-only deck. Implementation details (the JS-based hover with a 400ms grace period — **not** a CSS `~` sibling selector, which breaks because `pointer-events:none` drops the hover chain — plus the `E` shortcut and stripping edit state on export) are in [html-scaffold.md](references/html-scaffold.md).

#### Slide Type Templates

Consult [references/slide-templates.md](references/slide-templates.md) for HTML templates for each slide type: title, content, grid/card, metric, quote, comparison, section divider, timeline, logo wall, image, agenda, and CTA. Mix types for visual variety.

### Step 6: Delivery

After generating the HTML file:

1. **Clean up** any preview files from `.octave-decks/slide-previews/`
2. **Open the presentation** in the default browser
3. **Present a summary:**

```
PRESENTATION READY
==================

Folder: .octave-decks/<deck-name>-<date>/
File:   .octave-decks/<deck-name>-<date>/<deck-name>.html
Slides: [N] slides
Style:  [Preset name or "Custom Brand"]
Size:   [file size]

Navigation:
• Arrow keys / Space / Page Up-Down to move; Home/End to jump; R to reset
• Swipe left/right on touch devices
• Prev/next + "n / total" controls at the bottom
• Scales to fit any screen (fixed 16:9 stage, letterboxed)

Editing:
• Hover the top-left corner (or press E) to toggle inline edit mode, then
  click any text to edit. Export saves a clean copy with edit state stripped.

Customization tips:
• Colors/fonts: edit the :root CSS variables at the top of the file
• Content: each <section class="slide"> inside .deck-stage is one slide
• Add slides: copy a <section class="slide"> block (only the first carries
  "active visible")

---

Want me to:
1. Adjust specific slides
2. Change the style/colors
3. Add or remove slides
4. Create a version for a different audience
5. Export or share (PDF, live URL/Vercel, LinkedIn Carousel, PPTX, Google Slides, Gamma)
6. Done
```

### Step 7: Export & Share (Optional)

Consult [references/export-guide.md](references/export-guide.md) for detailed instructions per format:

- **PDF** — `bash "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/export-pdf.sh <deck>.html` (headless Playwright, one slide/page; `--compact` for smaller files). Browser print is the fallback.
- **Live URL** — `bash "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/deploy.sh <deck-folder>/` deploys to Vercel and returns a public link that works on any device.
- **LinkedIn Carousel, PPTX, Google Slides, Gamma, Markdown** — as documented in the export guide.

> `export-pdf.sh` and `deploy.sh` are generic — the same commands work for any HTML output from the other Octave skills (one-pager, proposal, microsite, brief, win-loss-report).

---

## PPTX Conversion Path

When a `.pptx` file is provided:

### Extract Content

```python
# Install if needed: pip install python-pptx Pillow
from pptx import Presentation
from pptx.util import Inches, Pt
import json, os

prs = Presentation("input.pptx")
slides = []
deck_dir = ".octave-decks/<deck-name>-<date>"
os.makedirs(f"{deck_dir}/assets", exist_ok=True)

for i, slide in enumerate(prs.slides):
    slide_data = {"index": i, "shapes": []}
    for shape in slide.shapes:
        if shape.has_text_frame:
            slide_data["shapes"].append({
                "type": "text",
                "text": shape.text_frame.text,
                "paragraphs": [
                    {"text": p.text, "level": p.level}
                    for p in shape.text_frame.paragraphs
                ]
            })
        elif shape.shape_type == 13:  # Picture
            img = shape.image
            ext = img.content_type.split("/")[-1]
            fname = f"{deck_dir}/assets/slide{i}_img{len(slide_data['shapes'])}.{ext}"
            with open(fname, "wb") as f:
                f.write(img.blob)
            slide_data["shapes"].append({"type": "image", "path": fname})
    slides.append(slide_data)
```

### Conversion Flow

1. Extract text and images from PPTX using python-pptx
2. Save images to the `assets/` subdirectory inside the deck folder (`.octave-decks/<deck-name>-<date>/assets/`)
3. Show extracted content structure to the user for review
4. **Still run Step 1** (purpose/goal) — the content comes from the PPTX but context matters
5. **Still offer Step 3** (brand) — the original PPTX style is lost in conversion
6. Proceed to Steps 4-6 as normal, using extracted content instead of Octave-generated content

> **Note:** Images from the PPTX are saved as separate files referenced by the HTML. The output is still a single HTML file, but images are external assets. Mention this to the user.

---

## MCP Tools Used

### Research & Enrichment
- `enrich_company` - Full company intelligence profile
- `enrich_person` - Full person intelligence report
- `find_person` - Find contacts at a company by title/role
- `qualify_company` - ICP fit scoring for a company
- `qualify_person` - ICP fit scoring for a person
- `find_company` - Find companies matching criteria

### Library — Fetching Entities
- `list_all_entities` - Quick scan of all entities of a type (minimal fields, no pagination)
- `list_entities` - Fetch entities with full data and pagination (proof points, references, personas, etc.)
- `get_entity` - Deep dive on one specific entity
- `list_motions` - List Motions in the workspace
- `list_motion_playbooks` - List Motion Playbooks under a Motion (Default + Custom)
- `get_motion_playbook` - Full details for a Motion Playbook
- `list_motion_icps` - List Motion ICP cells (persona × segment) for a Motion
- `find_motion_icp` - Motion ICP narrative + Learning Loop learnings

### Library — Searching
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
- `generate_email` - Generate email content (for follow-up slides)

### Brand & Style
- `get_external_brand_assets` - Scrape a URL for brand colors, logo variants, backdrop images, brand name (Tier 1 brand extraction)
- `get_external_brand_logo` - Single best logo URL for a domain
- `scrape_website` - Fetch a page as markdown/html with an optional screenshot (`{ format, includeScreenshot }`) — used to read components/typography for brand emulation (Tier 2)
- `list_all_entities` (entityType: "brand_voice") - Available brand voices in workspace
- `list_writing_styles` - Available writing styles in workspace

## Error Handling

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The deck builder can still work without Octave — you'll provide the content manually, and I'll handle structure, style, and HTML generation.
>
> To reconnect: check your MCP configuration or run `/octave:workspace status`

**Company/Person Not Found:**
> I couldn't find detailed intelligence for [target].
>
> Options:
> 1. Proceed with what we have — I'll use general positioning from your library
> 2. Try a different domain or email
> 3. Provide the content manually and I'll build the deck

**No Matching Motion ICP:**
> No Motion ICP cell matches this audience profile directly.
>
> I'll use your general positioning. After the deck is built, consider adding the missing persona × segment cell to a Motion (or creating a new Motion).

**PPTX Extraction Failed:**
> Could not parse the PPTX file.
>
> Options:
> 1. Try a different file
> 2. Export as PDF and I'll work from that
> 3. Copy-paste the content manually
> 4. Describe what the deck covers and I'll rebuild from scratch

**Browser-Use Unavailable (Brand Extraction):**
> Browser automation isn't available for brand extraction.
>
> Falling back to web fetch. If that doesn't capture your brand accurately, you can provide colors and fonts manually.

**Style Preview Won't Open:**
> Could not open preview files in browser.
>
> Preview files are saved at:
> [file paths]
>
> Open them manually, or just pick a preset by name/number.

## Related Skills

- `/octave:research` - Deep account research (feeds into deck content)
- `/octave:battlecard` - Competitive intelligence (for competitive decks)
- `/octave:generate` - Generate content with brand voice control
- `/octave:campaign` - Campaign strategy (deck as part of campaign)
- `/octave:enablement` - Sales enablement content packaging
- `/octave:pmm` - Product marketing collateral
- `/octave:insights` - Conversation intelligence for data-driven slides
- `/octave:pipeline` - Pipeline data for QBR decks
