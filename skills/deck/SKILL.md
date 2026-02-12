---
name: deck
description: Octave-powered presentation builder that researches, structures, and generates self-contained HTML slide decks. Use when user says "build a deck", "create a presentation", "pitch deck", "QBR slides", "sales deck", or asks for slides on any topic.
---

# /octave:deck - Octave-Powered Deck Builder

Build compelling, self-contained HTML presentations powered by your Octave GTM knowledge base. Unlike generic slide builders, this skill leverages your library's personas, competitors, playbooks, proof points, and real conversation data to research, structure, and generate presentations grounded in your actual go-to-market intelligence.

> HTML presentation engine inspired by [frontend-slides](https://github.com/zarazhangrui/frontend-slides) by Zara Zhang (MIT license).

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

### Step 2: Octave-Powered Context Gathering

Based on purpose, goal, and audience, use Octave MCP tools to build rich context for the deck. **Always tell the user what you're researching and why.**

**Call as many tools as needed to build a complete picture.** The best decks come from layering multiple sources — company enrichment + playbook messaging + proof points + conversation intel all combine to create slides grounded in real data. Don't stop at one tool when three would give you a stronger narrative.

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
| All playbooks | `list_all_entities({ entityType: "playbook" })` | Quick scan of available playbooks to find the right one |
| Matching playbook | `search_knowledge_base({ query: "<industry> <persona>", entityTypes: ["playbook"] })` | When you have a concept and need the best-fit playbook |
| Playbook details | `get_playbook({ oId, includeValueProps: true })` | After finding a relevant playbook — gets full content + value props |
| Value props | `list_value_props({ playbookOId })` | Fetch value props for a specific playbook (requires playbook oId) |
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
| Positioning by topic | `search_knowledge_base({ query: "<topic>", entityTypes: ["playbook", "product"] })` | When you have a concept and need relevant positioning |
| Proof points | `list_entities({ entityType: "proof_point" })` | Fetch all proof points with full data for credibility slides |
| References | `list_entities({ entityType: "reference" })` | Fetch customer references for social proof slides |
| Value props | `list_value_props({ playbookOId })` | Value props for a specific playbook |
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
| Competitive positioning | `search_knowledge_base({ query: "<competitor> differentiation", entityTypes: ["playbook", "competitor"] })` | When you have a concept — "how do we beat them on security?" |
| Our products | `list_entities({ entityType: "product" })` | Full product data for side-by-side comparison slides |
| Proof points (competitive wins) | `list_entities({ entityType: "proof_point" })` | Fetch all proof points — filter for competitive wins |
| Win/loss data | `list_events({ filters: { eventTypes: ["DEAL_WON", "DEAL_LOST"], competitors: ["<oId>"] } })` | Real deal outcomes against this competitor |
| Conversation evidence | `list_findings({ query: "<competitor>", eventFilters: { competitors: ["<oId>"] } })` | Real objections and mentions from calls |
| Value props | `list_value_props({ playbookOId })` | Differentiators from a specific playbook |
| Competitive resources | `search_resources({ query: "<competitor>" })` | Uploaded battlecards, analyst reports, or competitive docs |

---

#### For Enablement Decks (training, sales kickoff)

Mix playbook content with real deal examples:

| What you need | Tool | When to use |
|---------------|------|-------------|
| All playbooks | `list_all_entities({ entityType: "playbook" })` | Scan available playbooks to decide which to teach |
| Playbook full content | `get_playbook({ oId, includeValueProps: true })` | Full playbook with value props for training slides |
| Playbook by topic | `search_knowledge_base({ query: "<topic>", entityTypes: ["playbook"] })` | When you need the playbook most relevant to a concept |
| Personas | `list_entities({ entityType: "persona" })` | Full persona data for "know your buyer" slides |
| Competitors | `list_entities({ entityType: "competitor" })` | Full competitor data for competitive handling slides |
| All proof points | `list_entities({ entityType: "proof_point" })` | Fetch proof points with full data for example slides |
| Proof points by topic | `search_knowledge_base({ query: "results metrics", entityTypes: ["proof_point", "reference"] })` | When you need proof points *about* specific outcomes |
| Recent wins | `list_events({ filters: { eventTypes: ["DEAL_WON"] } })` | Success stories to use as examples |
| Win details | `get_event_detail({ eventOId })` | Deep dive on a notable win for a case study slide |
| Training resources | `search_resources({ query: "<topic>" })` | Uploaded enablement docs, playbook PDFs, or training assets |

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
• Playbook: [Playbook name] — [key messaging angle]
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
Do you want to use your company's brand styling?

1. Yes — extract from my website (provide URL)
2. Yes — I'll provide brand assets (colors, fonts, logo)
3. No — I'll pick from style presets
4. Use Octave brand styling

Your choice:
```

If user wants brand extraction:

**Tier 1: browser-use (best quality, if available)**
```
1. browser-use open <website-url>
2. browser-use screenshot brand-capture.png
3. browser-use eval "(() => {
     const styles = getComputedStyle(document.documentElement);
     const body = getComputedStyle(document.body);
     return {
       bgColor: body.backgroundColor,
       textColor: body.color,
       fontFamily: body.fontFamily,
       links: getComputedStyle(document.querySelector('a') || document.body).color,
       headings: getComputedStyle(document.querySelector('h1,h2,h3') || document.body).fontFamily,
       logos: [...document.querySelectorAll('img[src*=logo], svg[class*=logo], header img')].map(e => e.src || 'inline-svg').slice(0, 3)
     };
   })()"
4. browser-use extract "List the primary brand colors (hex), fonts, and logo URLs visible on this page"
5. Combine extractions into brand config
6. Show to user for confirmation
```

**Tier 2: WebFetch (if browser-use unavailable)**
```
1. WebFetch the homepage URL
2. Parse HTML/CSS for:
   - CSS custom properties (--brand-*, --color-*, --primary, etc.)
   - font-family declarations from body, h1-h3
   - Logo URLs from <img>, <svg>, og:image meta tags
   - meta theme-color
3. Show extracted brand config to user for confirmation
```

**Tier 3: Manual (if neither works)**
```
I couldn't automatically extract your brand. You can:

1. Share your brand guidelines (PDF or link)
2. Provide hex colors: primary, secondary, background, text
3. Name your fonts (heading + body)
4. Share logo files
5. Try coolors.co/image-picker with a screenshot of your site

Provide what you have:
```

**Always confirm the brand config with the user before proceeding:**

```
BRAND CONFIG EXTRACTED
======================

Colors:
  Primary:    #XXXXXX ██
  Secondary:  #XXXXXX ██
  Background: #XXXXXX ██
  Text:       #XXXXXX ██
  Accent:     #XXXXXX ██

Fonts:
  Headings: [Font name]
  Body: [Font name]

Logo: [URL or file path]

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

Generate **3 single-slide HTML preview files** based on the mood. Use the first slide from the outline as content. Save to `.octave-decks/slide-previews/`:

| Mood | Preview Presets |
|------|----------------|
| Impressed | `midnight-pro`, `executive-dark`, `octave-brand` |
| Excited | `electric-studio`, `neon-pulse`, `solar-flare` |
| Calm | `swiss-modern`, `soft-light`, `paper-minimal` |
| Inspired | `dark-botanical`, `aurora-gradient`, `monochrome-bold` |

If brand was extracted in Step 3, add a **4th brand-themed preview**.

Open all previews in the browser for the user to compare, then ask which they prefer.

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

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Deck Title]</title>
  <!-- Google Fonts (preconnect + stylesheet) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* === CSS Variables (from chosen preset) === */
    :root { ... }

    /* === Reset & Base === */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-snap-type: y mandatory; scroll-behavior: smooth; }

    /* === Slide Container === */
    .slide {
      height: 100vh;
      height: 100dvh;
      width: 100%;
      scroll-snap-align: start;
      overflow: hidden;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    /* === Typography (all clamp-based) === */
    .heading-1 { font-size: clamp(2rem, 5vw, 4rem); }
    .heading-2 { font-size: clamp(1.5rem, 3.5vw, 2.75rem); }
    .heading-3 { font-size: clamp(1rem, 2vw, 1.5rem); }
    .body-text { font-size: clamp(0.85rem, 1.4vw, 1.05rem); }

    /* === Layout Utilities === */
    .slide-inner { max-width: 1100px; width: 100%; padding: clamp(1.5rem, 4vh, 3rem) clamp(2rem, 5vw, 6rem); }
    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: clamp(1rem, 2vw, 2rem); }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: clamp(1rem, 2vw, 2rem); }

    /* === Components (cards, pills, metrics, etc.) === */
    /* === Animations === */
    /* === Navigation (progress bar + nav dots) === */
    /* === Responsive (max-height media queries) === */
    /* === prefers-reduced-motion === */
  </style>
</head>
<body>

  <div id="progress-bar"></div>
  <nav id="nav-dots"></nav>

  <!-- Slides -->
  <section class="slide" data-slide="0">
    <div class="bg-mesh">...</div>
    <div class="slide-inner">
      <!-- Slide content -->
    </div>
  </section>

  <!-- Repeat for each slide -->

  <script>
    // Navigation: keyboard (ArrowDown/Up, Space, PageDown/Up), scroll snap, touch
    // Progress bar animation
    // Nav dots generation and active state
    // Intersection Observer for .animate-in elements
    // prefers-reduced-motion check
  </script>

</body>
</html>
```

#### Viewport Fitting Requirements (Critical)

These rules are non-negotiable. Every slide must fit within 100vh/100dvh without scrolling:

1. **All font sizes use `clamp()`** — responsive to viewport, never fixed px
2. **All spacing uses `clamp()`** — padding, margins, gaps scale with viewport
3. **Content density limits per slide type:**

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

4. **If content exceeds limits** — split into multiple slides. Never overflow.
5. **Media queries for short viewports:**
   ```css
   @media (max-height: 700px) { /* Reduce font sizes ~10% */ }
   @media (max-height: 600px) { /* Reduce further, tighten padding */ }
   @media (max-height: 500px) { /* Minimal mode */ }
   ```
6. **`overflow: hidden`** on every `.slide` — content that doesn't fit is invisible, so it must fit

#### Animation Patterns

Staggered entrance animations triggered by Intersection Observer:

```css
.slide .animate-in {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s var(--ease), transform 0.6s var(--ease);
}
.slide.visible .animate-in {
  opacity: 1;
  transform: translateY(0);
}
/* Stagger children */
.slide.visible .animate-in:nth-child(1) { transition-delay: 0.1s; }
.slide.visible .animate-in:nth-child(2) { transition-delay: 0.2s; }
.slide.visible .animate-in:nth-child(3) { transition-delay: 0.3s; }
/* ... up to 8 */
```

Additional animation options (use sparingly):
- **Counter animation** for metrics: numbers count up when slide visible
- **Draw-in** for borders/lines: width/height transitions from 0
- **Fade-scale** for cards: `transform: scale(0.95)` to `scale(1)`

Always respect `prefers-reduced-motion`:
```css
@media (prefers-reduced-motion: reduce) {
  .slide .animate-in { opacity: 1; transform: none; transition: none; }
}
```

#### Navigation Implementation

```javascript
// Generate nav dots from slide count
// Scroll snap handles primary navigation
// Keyboard: ArrowDown/Right/Space = next, ArrowUp/Left = prev
// Progress bar: width = (currentSlide / totalSlides) * 100%
// Intersection Observer triggers .visible class for animations
// Touch support via scroll snap (native)
```

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
• Scroll or swipe to navigate between slides
• Keyboard: Arrow keys, Space, Page Up/Down
• Click nav dots on the right edge

Customization tips:
• Colors: Edit the :root CSS variables at the top of the file
• Content: Each <section class="slide"> is one slide
• Fonts: Change the Google Fonts <link> and font-family values
• Add slides: Copy a <section> block, increment data-slide

---

Want me to:
1. Adjust specific slides
2. Change the style/colors
3. Add or remove slides
4. Create a version for a different audience
5. Export to another format (PPTX, PDF, LinkedIn Carousel, Google Slides, Gamma)
6. Done
```

### Step 7: Export (Optional)

Consult [references/export-guide.md](references/export-guide.md) for detailed export instructions for each format: PDF, LinkedIn Carousel, PPTX, Google Slides, Gamma, and Markdown.

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
- `get_playbook` - Retrieve a playbook with full content and value props
- `list_value_props` - Value propositions for a specific playbook

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
- `list_brand_voices` - Available brand voices in workspace
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

**No Matching Playbook:**
> No playbook matches this audience profile directly.
>
> I'll use your general value props and positioning. After the deck is built, consider creating a playbook for this segment: `/octave:library create playbook`

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
