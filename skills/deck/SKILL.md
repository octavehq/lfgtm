---
name: deck
description: Octave-powered presentation builder that researches, structures, and generates self-contained HTML slide decks. Use when user says "build a deck", "create a presentation", "pitch deck", "QBR slides", "sales deck", or asks for slides on any topic.
argument-hint: "[topic or file] [--for <purpose>] [--audience <target>] [--style <preset>] [--skip-review]"
---

# /octave:deck - Octave-Powered Deck Builder

Build compelling, self-contained HTML presentations powered by your Octave GTM knowledge base. Unlike generic slide builders, this skill leverages your library's personas, competitors, Motion ICP narratives, proof points, and real conversation data to research, structure, and generate presentations grounded in your actual go-to-market intelligence.

> HTML presentation engine inspired by [frontend-slides](https://github.com/zarazhangrui/frontend-slides) by Zara Zhang (MIT license). Decks render on a **fixed 1920×1080 stage scaled to the viewport** (see [references/viewport-base.css](references/viewport-base.css)).

## On-brand styling

A deck is **customer-facing**, so whose brand it wears is a real choice — **offer the recipient's (the target company's) brand** for a personalized, made-for-you feel; the sender's brand is the standard alternative. Follow the kit lookup, defaults, and extraction tiers in [../shared/brand-kit-usage.md](../shared/brand-kit-usage.md).

## Review pass (runs by default)

Run the default review pass after generating — the always-on preflight plus the visual render-and-inspect pass, per [../shared/review-pass.md](../shared/review-pass.md). Opt out with `--skip-review`. When generating, follow the output rules in [../shared/presentation-principles.md](../shared/presentation-principles.md).

## Usage

```
/octave:deck [topic or file] [--for <purpose>] [--audience <target>] [--style <preset>] [--skip-review]
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

Establish five things before researching — **purpose** (customer pitch / QBR / internal strategy / keynote / launch / competitive / enablement), **goal** (the outcome the deck should drive), **audience** (company, person, role, or general group), **content readiness** (from scratch, notes, pasted content, or a PPTX file), and **length + density** (slide count and speaker-led vs reading-first).

Anything not provided via flags or the prompt, ask interactively using the question menus and per-purpose defaults in [references/intake.md](references/intake.md). If a `.pptx` file is provided, jump to the [PPTX Conversion Path](#pptx-conversion-path) before continuing.

Carry the **density** choice through Step 5: it drives the content limits per slide type (split into more slides rather than shrink text or overflow).

### Step 2: Octave-Powered Context Gathering

Based on purpose, goal, and audience, use Octave MCP tools to build rich context for the deck. **Always tell the user what you're researching and why.**

**Call as many tools as needed to build a complete picture.** The best decks come from layering multiple sources — company enrichment + Motion ICP narrative + proof points + conversation intel all combine to create slides grounded in real data. Don't stop at one tool when three would give you a stronger narrative.

That said, not every tool applies to every deck. Use your judgment about which are relevant to *this specific* situation, and pick the combination that gives you the richest context for the deck type and audience:

- **List-vs-search guidance, follow-up grounding (findings/events), and the common tool tables:** [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md). If this deck follows a previous interaction (QBR, post-demo follow-up, renewal), use the follow-up-grounding tools there to anchor the narrative in what was actually said.
- **Per-deck-type tool tables** (customer-facing, internal, competitive, enablement): [references/tool-reference.md](references/tool-reference.md).

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
```

> **Whose brand decides which website you fetch.** For option 1 run the extraction against *your own* domain; for option 2 run it against the *audience's/recipient's* domain.

Check for a cached brand kit first, and if extraction is needed work down the tiers (Octave brand-assets tool → `scrape_website` → browser-use → WebFetch → manual), then confirm the extracted brand config with the user — all per [../shared/brand-kit-usage.md](../shared/brand-kit-usage.md).

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

**Preview mix:** generate previews from the mood-matched presets in [../shared/style-presets.md](../shared/style-presets.md), optionally swapping one for a custom wildcard:

| Mood | Preview presets |
|------|----------------|
| Impressed | `midnight-pro`, `executive-dark`, `octave-brand` |
| Excited | `electric-studio`, `neon-pulse`, `solar-flare` |
| Calm | `swiss-modern`, `soft-light`, `paper-minimal` |
| Inspired | `dark-botanical`, `aurora-gradient`, `monochrome-bold` |

For more range, make one of the three a **custom wildcard** — a self-generated design that follows the no-slop rules (distinctive typography, avoid Inter/Roboto/system fonts; a committed palette, no generic purple-on-white; a recognizable layout system on the fixed 16:9 stage). If brand was extracted in Step 3, add a **4th brand-themed preview**.

Open all previews in the browser for the user to compare, then ask which they prefer (or which elements to mix).

#### Option 2: Preset Picker

Show the 12-preset menu (6 dark, 3 light, 3 vibrant) with one-line descriptions. Full CSS variable definitions for each preset are in [../shared/style-presets.md](../shared/style-presets.md).

#### Option 3: Brand-Generated Style

Auto-generate CSS variables from the brand config extracted in Step 3 (see [../shared/brand-kit-usage.md](../shared/brand-kit-usage.md) → "Applying an extracted brand"). Show the generated style to the user for confirmation.

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

Make sure `.octave-decks/` is ignored by your project's `.gitignore` (an `.octave-*/` pattern covers all Octave output dirs) so generated decks don't get committed.

#### HTML Architecture

See [html-scaffold.md](references/html-scaffold.md) for the full scaffold. **Two non-negotiables:**

1. **Paste the entire [viewport-base.css](references/viewport-base.css)** into the `<style>` block. It provides the `.deck-viewport` → `.deck-stage` (1920×1080) → `.slide` system, `.active`/`.visible` visibility, print-one-slide-per-page, and reduced-motion.
2. **Author every slide at 1920×1080 in px** — no `clamp()`, `vw`, or `vh` for layout. The stage scales as a whole to fit any screen.

#### Fixed-Canvas Fitting (Critical)

Every slide is a fixed 1920×1080 canvas; the controller scales the whole stage. Fit is achieved by **density discipline**, not responsive math:

1. **Size in px against the 1920×1080 canvas.** A title is ~96–120px, body ~24–32px, slide padding ~80×140px. Translate any `clamp()`/`vw` from a preset or custom design into fixed px.
2. **`overflow: hidden` on every `.slide`** (from viewport-base.css) — anything that doesn't fit is clipped, so it must fit by design.
3. **Content density limits per slide type** (tighten for *speaker-led*, allow the upper bound for *reading-first* — see the Step 1 density choice):

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

**Copy is held to the same bar as visuals.** Every word a viewer reads (headline, body, caption, pill, metric label) must pass the slop standard in [../shared/asset-review.md](../shared/asset-review.md) → WRITE_LIKE_A_HUMAN. Two rules break most decks, so treat them as hard rules, not preferences, and fix them in the review pass rather than excusing them as "headline style":

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

> `export-pdf.sh` and `deploy.sh` are generic — the same commands work for any HTML output from the other Octave skills (one-pager, proposal, microsite, brief, wins-losses reports).

---

## PPTX Conversion Path

When a `.pptx` file is provided:

### Extract Content

Use the bundled extractor (requires `pip install python-pptx`):

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/extract-pptx.py <input.pptx> .octave-decks/<deck-name>-<date>
```

It emits a JSON structure of every slide (title, text paragraphs with levels, speaker notes) and saves embedded images to `assets/` inside the output directory.

### Conversion Flow

1. Extract text and images from the PPTX with the script above
2. Show the extracted content structure to the user for review
3. **Still run Step 1** (purpose/goal) — the content comes from the PPTX but context matters
4. **Still offer Step 3** (brand) — the original PPTX style is lost in conversion
5. Proceed to Steps 4-6 as normal, using extracted content instead of Octave-generated content

> **Note:** Images from the PPTX are saved as separate files referenced by the HTML. The output is still a single HTML file, but images are external assets. Mention this to the user.

---

## MCP Tools Used

Common research, library, signals, and generation tools: see [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md). Deck-specific additions:

### Brand & Style
- `get_external_brand_assets` — Scrape a URL for brand colors, logo variants, backdrop images, brand name (Tier 1 brand extraction)
- `get_external_brand_logo` — Single best logo URL for a domain
- `scrape_website` — Fetch a page as markdown/html with an optional screenshot (`{ format, includeScreenshot }`) — used to read components/typography for brand emulation (Tier 2)
- `list_entities` (entityType: "brand_voice") — Available brand voices in workspace
- `list_writing_styles` — Available writing styles in workspace

## Error Handling

Standard responses (connection failed, company/person not found, no matching Motion ICP cell): see [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md) → Standard error handling. Deck-specific:

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
