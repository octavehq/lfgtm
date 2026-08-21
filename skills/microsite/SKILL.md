---
name: microsite
description: Personalized ABM microsite builder that generates self-contained HTML landing pages using GTM intelligence. Use when user says "microsite for [company]", "personalized landing page", "ABM page", or asks for a personalized web page for a target account.
---

# /octave:microsite - Personalized ABM Microsite Builder

Generate personalized, single-page ABM microsites as beautiful self-contained HTML, powered by your Octave GTM knowledge base. Instead of "Hey, want to see a demo?" you send "We built something for you" with a link. The microsite shows effort, personalization, and immediately demonstrates you understand their business.

**Why microsites work:** They flip the cold outreach dynamic. A personalized landing page — "Built for [Company]" — is a pattern interrupt. It proves you researched the account, tailored your message, and invested time before asking for theirs.

**How this differs from other skills:**
- vs `/octave:one-pager` — one-pager is a post-meeting leave-behind; microsite is a pre-meeting attention grabber for outreach
- vs `/octave:proposal` — proposal is formal and detailed; microsite is concise and designed to generate interest
- vs `/octave:deck` — deck is for presenting; microsite is for sharing a link

## On-brand styling — brand kit first, then generate

**Resolve the brand before generating (do not skip this step).** A champion microsite is styled with the **sender's brand** — the workspace company (the Octave customer whose workspace you are operating in). The target account is centered in the *content* ("Built for [Company]", their pains, their proof points), not in the styling. This is the same brand rule the other showcase skills use, so outputs stay consistent.

**Step 1: Identify the workspace company.** Call `get_workspace_company` to get the company name, domain/URL, and positioning. This is the company whose brand styles the page.

**Step 2: Resolve the workspace company's brand kit.** Slugify the workspace company name and check for a cached brand kit at `~/.octave/brands/<slug>/manifest.json`. If a complete kit exists (has `manifest.json` and `tokens.css`), use it automatically:
   - inline the kit's `tokens.css` (`:root` + the embedded `@font-face`) **and** `../get-brand-components/assets/kit_base.css` into the output `<style>`;
   - follow the kit's `brand-kit.md` → **Signature moves**, and reuse the kit's real **logo**, `images/`, and `icons.json`.
   **If no complete kit exists → build one.** Read and follow the `get-brand-components` SKILL.md for the workspace company's domain. If the first attempt returns incomplete results, retry up to 3 times with variations (root domain, `www.` prefix, `/about` subpage). Only fall back to a generic preset after 3 genuine failures.

**Step 3: Generic preset is a last resort** — only after the workspace company's brand kit cannot be built.

> **Optional override (ABM mirroring):** if the user explicitly asks for the microsite to mirror the *recipient's* brand for maximum personalization, build/resolve a kit for the target account's domain instead. This is opt-in, not the default — do not stop to ask.

## Principles

Follow these standards during generation. Read each before producing output.

**Content and language:**
- [Editorial rules](../shared/editorial-rules.md) — no AI-isms, banned vocabulary, honest analyst tone
- [Information principles](../shared/information-principles.md) — lead with conclusions, evidence-backed claims, narrative arc

**Visual design:**
- [Presentation principles](../shared/presentation-principles.md) — typography, layout, visual restraint
- [Microsite format](../shared/formats/microsite.md) — hero hooks, CTA-driven, scroll narrative, responsive

**Octave data:**
- [Octave value](../shared/octave-value.md) — prioritize grounded workspace data over generic AI content

Apply these rules during generation, not just at review. After generating, the **review pipeline is a mandatory gate** (see Step 5) — the microsite is not opened or delivered until the scorecard is produced.

## Usage

```
/octave:microsite <target> [--angle <approach>] [--style <preset>]
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

1. Pain-point led — address a specific challenge they face
2. Competitive displacement — show a better way than their current approach
3. Value-led — lead with results and metrics from similar companies
4. Trigger-based — connect to a recent event, news, or milestone
5. Industry-specific — demonstrate deep expertise in their vertical

Your choice:
```

**Call to Action — "What should they do next?"**

```
What action should the microsite drive?

1. Book a demo
2. See a case study
3. Watch a video / product tour
4. Start a free trial
5. Reply to an email / start a conversation
6. Custom (describe it)

Your choice:
```

**Brand — resolved automatically, no menu.** Do not ask whose brand to use. The microsite is styled with the workspace company's brand kit per the **On-brand styling** section above (resolve or build it silently). Recipient-brand mirroring is an explicit opt-in only if the user asks for it.

### Step 2: Octave Context Gathering

Based on the target, angle, and CTA, use Octave MCP tools to build deep personalization context. **Always tell the user what you're researching and why.**

**Call as many tools as needed.** The more you know about the account, the more personalized the microsite. A great microsite layers company enrichment + Motion ICP cell narrative + proof points + competitive intel into a narrative that feels hand-crafted. Don't stop at one tool when four would give you a stronger page.

**List vs Search — when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory — "show me all our proof points" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need the actual content — "get full proof point details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something relevant and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept or question — "how do we help healthcare?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need reference material, uploaded assets, or source docs |

---

See [octave-tool-reference.md](references/octave-tool-reference.md) for the full tool reference tables (always-run, person-specific, social proof, competitive, trigger-based, and additional context).

---

**Output of this step:** Present a content outline to the user for approval:

See [microsite-outline-template.md](references/microsite-outline-template.md) for the microsite outline template.

**Wait for user approval before proceeding.**

### Step 3: Style & Brand

The microsite is styled with the **workspace company's brand kit** — resolve or build it per the **On-brand styling** section at the top of this skill. Two layers apply:

1. **Sender styling** (workspace company) — logo, colors, fonts from the brand kit. This is what the page is styled with.
2. **Recipient context** (the target account) — the personalization that shows you researched them. This appears as content, not styling.

Do not present a brand menu or wait for brand approval. Only fall back to a style preset ([style-presets.md](../shared/style-presets.md)) after the workspace company's kit genuinely cannot be built (3 failures). If the user explicitly asked to mirror the recipient's brand, build a kit for the target domain instead.

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

The entire `.octave-microsites/` directory is in `.gitignore` — nothing here gets committed.

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
7. **Self-contained** — inline CSS, no external requests beyond Google Fonts. NO tracking pixels, analytics, or third-party scripts. Exception: `assets/og.png`, the social share image, ships as a sibling file (unfurlers ignore data-URI og:image); reference it relatively per [social-meta.md](../shared/social-meta.md).

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

**After writing the file, proceed immediately to Step 5 (Review Pipeline). Do NOT open the file in the browser or present the delivery summary yet.**

### Step 5: Review Pipeline — MANDATORY GATE

**Do NOT open the microsite in the browser, present the delivery summary, or tell the user it is ready until the review pipeline has completed and you have a scorecard.**

Load the [review protocol](../shared/protocol.md) and execute the review loop against the generated HTML file. Microsite-specific wiring:

**5a: Mechanical lint** (before spawning reviewers):

```bash
bash <skill-dir>/../shared/scripts/lint.sh <path-to-microsite.html>
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
           Microsite copy is short and punchy — hold every line to the density limits.
           Fix violations inline. Return scorecard."
```

**Presentation reviewer:**
```
Task tool:
  subagent_type: "octave-presentation-reviewer"
  prompt: "Review the file at [FILE PATH].
           Read these docs and run each Review Checklist:
           1. [skill-dir]/../shared/presentation-principles.md
           2. [skill-dir]/../shared/formats/microsite.md
           3. [skill-dir]/references/html-architecture.md
           4. [skill-dir]/references/page-sections-by-angle.md
           Verify the page renders correctly at 375px width (mobile-first).
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
  (Vercel serves files verbatim, with none of the asset service's serve-time OG rewriting. After the first deploy returns the URL, set og:image to the absolute <url>/assets/og.png and deploy once more; strict unfurlers like LinkedIn and Facebook require an absolute image URL there. This is a post-gate delivery step: the review gate lints the relative form, and a re-lint of the Vercel copy failing on the absolute-URL check is expected.)
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

### Research & Enrichment
- `enrich_company` - Full company intelligence profile
- `enrich_person` - Full person intelligence report
- `find_person` - Find contacts at a company by title/role
- `qualify_company` - ICP fit scoring for a company
- `qualify_person` - ICP fit scoring for a person

### Library -- Fetching Entities
- `list_entities` - Quick scan of all entities of a type (minimal fields, no pagination)
- `list_entities` - Fetch entities with full data and pagination (proof points, references, etc.)
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
- `get_workspace_company` - Workspace company identity for brand-kit resolution (the sender's brand that styles the page)
- `list_entities` (entityType: "brand_voice") - Available brand voices in workspace
- `list_writing_styles` - Available writing styles in workspace

## Error Handling

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The microsite builder can still work without Octave — you provide the content manually, and I'll handle structure, style, and HTML generation. The result won't have Octave-powered personalization, but it will still look great.
>
> To reconnect: check your Octave MCP configuration and reconnect

**Company Not Found:**
> I couldn't find detailed intelligence for [target].
>
> Options:
> 1. Proceed with general positioning from your library — I'll use your best-fit Motion ICP cell
> 2. Try a different domain or email
> 3. Provide company details manually (industry, size, challenges) and I'll personalize from that

**No Relevant Proof Points:**
> I couldn't find proof points in [their industry / of their size].
>
> Options:
> 1. Use your strongest proof points from adjacent industries
> 2. Use general metrics without company-specific quotes
> 3. Skip the proof section and lead with a stronger solution narrative

**No Competitor Data (for Competitive Angle):**
> I don't have data on the competitor they likely use.
>
> Options:
> 1. Switch to a different angle (pain-point led or value-led)
> 2. Use general competitive positioning without naming the competitor
> 3. Provide competitor details manually and I'll build the narrative

**No Matching Motion ICP Cell:**
> No Motion ICP cell matches this audience profile directly.
>
> I'll use your general positioning. After the microsite is built, consider layering a Custom Motion Playbook (Thematic / Milestone / Account / Competitive) on the relevant Motion for this angle: `/octave:library create motion-playbook`

**Browser-Use Unavailable (Brand Extraction):**
> Browser automation isn't available for brand extraction.
>
> Falling back to web fetch. If that doesn't capture your brand accurately, you can provide colors and fonts manually.

## Related Skills

- `/octave:one-pager` - Post-meeting leave-behind (microsite is pre-meeting)
- `/octave:research` - Deeper research on the account
- `/octave:generate` - Generate the outreach email that includes the microsite link
- `/octave:prospector` - Find more companies to create microsites for
- `/octave:abm` - Full ABM campaign planning with stakeholder mapping
- `/octave:deck` - Presentation deck (for meetings, not sharing a link)
- `/octave:battlecard-doc` - Competitive intelligence (for competitive angle microsites)
