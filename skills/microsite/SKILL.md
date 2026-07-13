---
name: microsite
description: Personalized ABM microsite builder that generates self-contained HTML landing pages using GTM intelligence. Use when user says "microsite for [company]", "personalized landing page", "ABM page", or asks for a personalized web page for a target account.
argument-hint: "<company-or-email> [--angle <approach>] [--style <preset>] [--skip-review]"
---

# /octave:microsite - Personalized ABM Microsite Builder

Generate personalized, single-page ABM microsites as beautiful self-contained HTML, powered by your Octave GTM knowledge base. Instead of "Hey, want to see a demo?" you send "We built something for you" with a link. The microsite shows effort, personalization, and immediately demonstrates you understand their business.

**Why microsites work:** They flip the cold outreach dynamic. A personalized landing page — "Built for [Company]" — is a pattern interrupt. It proves you researched the account, tailored your message, and invested time before asking for theirs.

**How this differs from other skills:**
- vs `/octave:one-pager` — one-pager is a post-meeting leave-behind; microsite is a pre-meeting attention grabber for outreach
- vs `/octave:proposal` — proposal is formal and detailed; microsite is concise and designed to generate interest
- vs `/octave:deck` — deck is for presenting; microsite is for sharing a link

## On-brand styling

A microsite is **customer-facing and personalized** ("Built for [Company]"), so **default to the recipient's (the target company's) brand** — a page in the prospect's own identity is the whole point of an ABM microsite; the sender's brand is the fallback. Follow the kit lookup, defaults, and extraction tiers in [../shared/brand-kit-usage.md](../shared/brand-kit-usage.md).

## Review pass (runs by default)

Run the default review pass after generating — the always-on preflight plus the visual render-and-inspect pass, per [../shared/review-pass.md](../shared/review-pass.md). Opt out with `--skip-review`. When generating, follow the output rules in [../shared/presentation-principles.md](../shared/presentation-principles.md).

## Usage

```
/octave:microsite <target> [--angle <approach>] [--style <preset>] [--skip-review]
```

## Examples

```
/octave:microsite acme.com                                    # Personalized microsite for Acme
/octave:microsite acme.com --angle competitive                # Competitive angle (they use rival)
/octave:microsite jane@acme.com --angle pain-point            # Person-specific, pain-led
/octave:microsite "enterprise healthcare companies"           # Segment-level microsite template
/octave:microsite acme.com --style octave-brand               # Specific style preset
/octave:microsite acme.com --angle trigger                    # Trigger-based (recent news/event)
```

## Instructions

When the user runs `/octave:microsite`:

### Step 1: Understand the Context

If not provided via flags, ask the user interactively:

**Target — "Who is this for?"**

```
Who is this microsite for?

Provide any of the following:
- Company domain (e.g., acme.com)
- Person email (e.g., jane@acme.com)
- Segment description (e.g., "enterprise healthcare companies")

Target:
```

**Angle — "What approach should this take?"**

```
What angle should the microsite lead with?

1. Pain-point led — address a specific challenge they face (default)
2. Competitive displacement — show a better way than their current approach
3. Value-led — lead with results and metrics from similar companies
4. Trigger-based — connect to a recent event, news, or milestone
5. Industry-specific — demonstrate deep expertise in their vertical

Your choice:
```

**Call to Action — "What should they do next?"**

```
What action should the microsite drive?

1. Book a demo (default)
2. See a case study
3. Watch a video / product tour
4. Start a free trial
5. Reply to an email / start a conversation
6. Custom (describe it)

Your choice:
```

For link-based CTAs (demo, trial, video), also ask for the destination URL — the button has to point somewhere real. If none is provided, use the sender company's website and flag it in the delivery summary as a placeholder to replace before sending.

**Brand — "Whose brand styles the page?"**

```
Whose brand should the microsite reflect?

1. The recipient's brand — mirror the target account's look for maximum ABM
   personalization (default; give *their* URL if no kit is cached)
2. My brand (the sender) — extract from my website (give the URL)
3. I'll provide brand assets directly (colors, fonts, logo)
4. No brand — pick from style presets
5. Use Octave brand styling

Your choice:
```

> **This choice decides which website we fetch for styling** — the target account's domain (option 1, the default) or your own domain (option 2). It's separate from the recipient *context*, which always personalizes the content regardless of whose brand styles the page.

### Step 2: Octave Context Gathering

Based on the target, angle, and CTA, use Octave MCP tools to build deep personalization context. **Always tell the user what you're researching and why.**

**Call as many tools as needed.** The more you know about the account, the more personalized the microsite. A great microsite layers company enrichment + Motion ICP cell narrative + proof points + competitive intel into a narrative that feels hand-crafted.

For list-vs-search guidance and the common tool tables, see [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md). For the microsite-specific tool tables (always-run, person-specific, social proof, competitive, trigger-based, and additional context), see [tool-reference.md](references/tool-reference.md).

**Output of this step:** Present a content outline to the user for approval:

See [microsite-outline-template.md](references/microsite-outline-template.md) for the microsite outline template.

**Wait for user approval before proceeding.**

### Step 3: Style & Brand

Two layers apply to every microsite, and they are independent:

1. **Styling brand** — whose visual identity the page wears. **Default: the recipient's brand** (per the On-brand styling section above); the sender's brand is the fallback when the user prefers it.
2. **Recipient context** — the personalization that shows you researched them. This appears as *content* ("Built for [Company]", their pains, their industry proof) no matter whose brand styles the page.

**If brand extraction is needed (no cached kit):** follow the tiered flow in [../shared/brand-kit-usage.md](../shared/brand-kit-usage.md) — Tier 1 `get_external_brand_assets` (colors + logo, with the customer-logo sanity check), Tier 2 `scrape_website` with `includeScreenshot` (homepage + one representative page; microsites especially benefit — the goal is to *look like the brand's site*, not just borrow its colors), then browser-use / WebFetch / manual fallbacks. Confirm the brand config with the user before proceeding.

**If user chose a style preset:**

Use the shared preset system in [../shared/style-presets.md](../shared/style-presets.md). Recommended defaults for microsites:

| Angle | Recommended Preset |
|-------|--------------------|
| Pain-point led | `midnight-pro` |
| Competitive displacement | `neon-pulse` |
| Value-led | `executive-dark` |
| Trigger-based | `aurora-gradient` |
| Industry-specific | `soft-light` |

Tell the user what you picked and why. Let them override.

### Step 4: Generate HTML

Build a single, self-contained HTML file. A microsite is a single scrolling page — visually striking, mobile-responsive, and heavily personalized.

#### Output Directory

Every microsite gets its own folder under `.octave-microsites/`:

```
.octave-microsites/
└── <kebab-case-company>-<YYYY-MM-DD>/
    └── <company>-microsite.html
```

Example: `/octave:microsite acme.com` produces `.octave-microsites/acme-2026-02-11/acme-microsite.html`

Make sure `.octave-microsites/` is ignored by your project's `.gitignore` (an `.octave-*/` pattern covers all Octave output dirs) so generated microsites don't get committed.

#### Page Sections by Angle

See [page-sections-by-angle.md](references/page-sections-by-angle.md) for page section templates for each angle (pain-point led, competitive displacement, value-led, trigger-based).

#### HTML Architecture

See [html-architecture.md](references/html-architecture.md) for the full HTML/CSS scaffold with sections, typography, and layout components.

#### Key Design Principles

These rules are non-negotiable for microsites:

1. **First impression matters** — the hero must be visually striking with a gradient background, full viewport height, and the company name front and center
2. **Personalization must be visible immediately** — company name in the hero, not buried below the fold
3. **Keep it SHORT** — 4-5 sections max, each scannable in 5 seconds. This is not a blog post.
4. **One CTA, repeated** — the same ask in the hero (subtle) and the closing section (prominent). Do not confuse with multiple different asks.
5. **Mobile-first** — this WILL be opened from email on a phone. All `clamp()` values must work at 375px width. Test aggressively.
6. **No sidebar, no navigation bar** — single vertical scroll. Smooth, clean, focused.
7. **Self-contained** — inline CSS, no external requests beyond Google Fonts. NO tracking pixels, analytics, or third-party scripts.

#### Content Density Limits

| Section | Max Content |
|---------|------------|
| Hero | 1 "Built for" tag + 1 headline (2 lines max) + 1 subhead (2 lines max) |
| Challenge / Gap | 1 heading + 3-4 short paragraphs or bullet points |
| Solution / Cards | 1 heading + 3 cards (icon + title + 2-line description each) |
| Proof / Metrics | 1 heading + 3 proof blocks (metric + company + 1-line quote each) |
| CTA | 1 heading + 1 supporting line + 1 button |

If content exceeds limits, cut ruthlessly. Microsites are scannable, not comprehensive.

#### Animation Patterns

Scroll-triggered entrance animations using Intersection Observer:

```css
.animate-in {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}
.animate-in.visible {
  opacity: 1;
  transform: translateY(0);
}
/* Stagger children within a section */
.animate-in:nth-child(1) { transition-delay: 0.1s; }
.animate-in:nth-child(2) { transition-delay: 0.2s; }
.animate-in:nth-child(3) { transition-delay: 0.3s; }
.animate-in:nth-child(4) { transition-delay: 0.4s; }
```

Additional effects (use sparingly):
- **Counter animation** for metrics: numbers count up when scrolled into view
- **Fade-scale** for cards: `transform: scale(0.96)` to `scale(1)` on reveal
- **Gradient shift** on hero: subtle background gradient animation via CSS keyframes

Always respect `prefers-reduced-motion`:
```css
@media (prefers-reduced-motion: reduce) {
  .animate-in { opacity: 1; transform: none; transition: none; }
}
```

#### Responsive Breakpoints

```css
/* Tablet */
@media (max-width: 768px) {
  .card-grid { grid-template-columns: 1fr; }
  .hero { min-height: 80vh; }
}

/* Mobile */
@media (max-width: 480px) {
  .section { padding: clamp(2rem, 6vh, 3rem) 1.25rem; }
  .heading-1 { font-size: clamp(1.8rem, 8vw, 2.5rem); }
}
```

#### Section Templates

Each section follows the pattern: `<section class="section" id="[id]"><div class="section-inner">...</div></section>`. Hero and CTA sections add the `hero` class for full-viewport layout.

**Hero:** `built-for` tag + `heading-1` headline + `body-lg` subhead + optional soft CTA link to `#cta`
**Challenge / Problem:** `heading-2` + 3 pain-point blocks (each: `heading-3` + `body-text`)
**Solution / Cards:** `heading-2` + `card-grid` with 3 cards (each: icon + `heading-3` + `body-text`)
**Proof / Metrics:** `heading-2` + `proof-grid` with 3 proof blocks (each: `big-number` metric + label + short quote with attribution)
**Process / Steps:** `heading-2` + numbered steps (each: `step-number` + `heading-3` + `body-text`)
**CTA:** `heading-1` headline + `body-lg` supporting line + `cta-button` link + optional contact info

All content elements use the `animate-in` class for scroll-triggered entrance animations.

### Step 5: Delivery

After generating the HTML file:

1. **Open the microsite** in the default browser
2. **Test mobile viewport** if browser-use is available (resize to 375px width)
3. **Present a summary:**

```
MICROSITE READY
===============

Folder: .octave-microsites/<company>-<date>/
File:   .octave-microsites/<company>-<date>/<company>-microsite.html
Target: [Company name]
Angle:  [Pain-point / Competitive / Value-led / Trigger-based]
CTA:    [Book a demo / etc.]
Style:  [Preset name or "Custom Brand"]
Size:   [file size]

How to share:
• Live URL (recommended): bash "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/deploy.sh .octave-microsites/<company>-<date>/  — deploys to Vercel and returns a public link to drop in your outreach
• PDF: bash "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/export-pdf.sh .octave-microsites/<company>-<date>/<company>-microsite.html  — or Cmd+P / Ctrl+P -> Save as PDF
• Host on any static file server, S3 bucket, or Netlify drop
• Or send the HTML file directly as an attachment

---

Want me to:
1. Adjust the messaging or tone
2. Change the angle (e.g., switch from pain-led to value-led)
3. Add or remove sections
4. Create versions for different contacts at the same company
5. Generate the outreach email that includes this link (/octave:generate)
6. Done
```

## MCP Tools Used

Common research, library, signals, and generation tools: see [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md). Microsite-specific additions:

### Brand & Style
- `get_external_brand_assets` / `get_external_brand_logo` / `scrape_website` — Brand extraction (Tiers 1-2)
- `list_entities` (entityType: "brand_voice") - Available brand voices in workspace
- `list_writing_styles` - Available writing styles in workspace

## Error Handling

Standard responses (connection failed, company not found, no matching Motion ICP cell, no proof points): see [../shared/octave-research-toolkit.md](../shared/octave-research-toolkit.md) → Standard error handling. Microsite-specific:

**No Competitor Data (for Competitive Angle):**
> I don't have data on the competitor they likely use.
>
> Options:
> 1. Switch to a different angle (pain-point led or value-led)
> 2. Use general competitive positioning without naming the competitor
> 3. Provide competitor details manually and I'll build the narrative

**Browser-Use Unavailable (Brand Extraction):**
> Browser automation isn't available for brand extraction.
>
> Falling back to web fetch. If that doesn't capture the brand accurately, you can provide colors and fonts manually.

## Related Skills

- `/octave:one-pager` - Post-meeting leave-behind (microsite is pre-meeting)
- `/octave:research` - Deeper research on the account
- `/octave:generate` - Generate the outreach email that includes the microsite link
- `/octave:prospector` - Find more companies to create microsites for
- `/octave:abm` - Full ABM campaign planning with stakeholder mapping
- `/octave:campaign` - Campaign strategy that includes microsites
- `/octave:deck` - Presentation deck (for meetings, not sharing a link)
- `/octave:battlecard` - Competitive intelligence (for competitive angle microsites)
