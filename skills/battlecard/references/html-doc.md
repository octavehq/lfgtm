# HTML Battlecard Document (--format doc)

How to render the battlecard intelligence as a self-contained HTML reference document. The content itself comes from the Step 2 research plan and follows the same section logic as [full-battlecard.md](full-battlecard.md) (single competitor) and [competitive-landscape.md](competitive-landscape.md) (landscape) — this file covers the document-specific structure, components, and scaffold.

## Content Brief Template

Present before generating and wait for approval:

```
BATTLECARD OUTLINE: vs [Competitor]
====================================

Competitor: [Competitor name]
Data Sources: [N] deals analyzed, [N] conversation mentions, [N] proof points
Date Range: Last 180 days
Win Rate: [X%] ([N] wins / [N] losses)

---

SECTIONS
--------
1. Quick Positioning — one-liner + 30-second pitch
2. Competitor Overview — what they do, target, pricing, key customers
3. Where We Win — strengths table + real deal evidence
4. Where They Win — honest assessment + how to counter each
5. Objection Handlers — organized by category (pricing, feature, relationship, risk)
6. Trap Questions — discovery questions that expose weaknesses
7. Landmines to Set — evaluation criteria to plant early
8. Proof Points — switching stories, competitive wins, metrics
9. Win/Loss Scorecard — visual scoreboard with win rate and factors
10. Displacement Playbook — how to unseat them when entrenched

Octave Sources Used:
- Competitor entity: [name]
- Deals analyzed: [N] wins, [N] losses
- Conversation mentions: [N] findings
- Proof points: [N] relevant
- Motions / Motion ICPs: [list of Motions and ICP cells]
- Custom Motion Playbooks (COMPETITIVE narrative): [list]

---

Does this outline look good? I can:
1. Proceed to style selection and generation
2. Add/remove sections
3. Go deeper on any area
4. Switch to landscape overview
```

For a "quick reference" variant, trim to Quick Positioning + Objection Handlers + Trap Questions only.

## Single Competitor — Document Sections

**1. Header Banner**
- "vs [Competitor]" title with your product name
- Last updated date
- Data sources badges: "[N] deals | [N] calls | [N] proof points"

**2. Quick Positioning**
- Highlighted callout box with brand accent border: the risk moment ("When [Competitor] comes up...") and the lead angle
- One-liner: single strongest differentiator
- 30-second positioning: the 2-3 beats to hit in your own words — talking points, not a script to recite

**3. Competitor Overview**
- What they do, target market, pricing, key customers, recent moves
- Card-based grid layout (2-3 columns)

**4. Where We Win**
- Comparison table: capability rows with green checkmarks (us) and red crosses (them)
- Win themes from actual deals: numbered list with quoted conversation evidence

**5. Where They Win (Be Honest)**
- Their genuine strengths listed honestly
- For each: a "How to counter/reframe" response
- Color-code: amber for their strengths, green counter callouts

**6. Objection Handlers**
- Expandable `<details>/<summary>` accordion elements
- Organized by category: Pricing, Feature, Relationship, Risk (with category badges)
- Summary line = the risk or situation ("They anchor on price"), never a quote in the prospect's voice
- Expanded body: "You'll hear" (the likely prospect line) → response points the rep adapts → proof point
- Include real conversation evidence when available

**7. Trap Questions**
- 5-8 discovery questions as numbered cards
- Each with: the question (ask near-verbatim — trap questions are the one scripted element), why it works, expected response, follow-up

**8. Landmines to Set**
- Evaluation criteria to plant early that favor you
- Each with: criterion, why it matters, how it plays to your strength

**9. Proof Points**
- Customers who switched, competitive win stories, head-to-head metrics
- Card layout with metric highlights

**10. Win/Loss Scorecard**
- Visual win rate bar: CSS-based div widths (green for wins, red for losses)
- Win rate percentage displayed prominently
- Common win factors (green accent) and loss factors (red accent)

**11. Displacement Playbook**
- How to unseat entrenched competitors
- Migration story, switching cost offsets, success timeline
- Sequential step layout

## Landscape Overview — Document Sections

**1. Header** — "Competitive Landscape" title + date + competitor count

**2. Market Map** — Table: competitor, focus, threat level (color-coded badge), win rate mini-bar

**3. Per-Competitor Cards** — Condensed card per competitor: name, positioning, key differentiator, top objection risk + counter points, win rate bar. Grid layout.

**4. Cross-Competitor Patterns** — Themes across multiple competitors, common objection categories, universal differentiators

## HTML Scaffold

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Battlecard: vs [Competitor]</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* === CSS Variables (from chosen style preset — see ../../shared/style-presets.md) === */
    :root { /* ... paste chosen preset variables here ... */ }

    /* === Reset & Base === */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body { background: var(--bg); color: var(--text-primary); font-family: var(--font-body); line-height: 1.6; }

    /* === Document Layout === */
    .doc-container { max-width: 950px; margin: 0 auto; padding: 2rem clamp(1rem, 4vw, 3rem); }

    /* === Sticky Sidebar Navigation === */
    .sidebar { position: fixed; top: 50%; transform: translateY(-50%); right: clamp(0.5rem, 2vw, 2rem); display: flex; flex-direction: column; gap: 0.25rem; z-index: 100; }
    .sidebar a { display: block; width: 8px; height: 8px; border-radius: 50%; background: var(--text-muted); transition: all 0.2s var(--ease); }
    .sidebar a.active { background: var(--brand-primary); transform: scale(1.5); }

    /* === Sections === */
    .section { margin-bottom: clamp(2rem, 4vh, 4rem); padding-top: 1rem; }
    .section-title { font-family: var(--font-display); font-size: clamp(1.25rem, 2.5vw, 1.75rem); font-weight: 600; margin-bottom: 1rem; }

    /* === Header Banner === */
    .header-banner { padding: clamp(2rem, 4vh, 4rem) 0; border-bottom: 1px solid var(--border); margin-bottom: clamp(2rem, 4vh, 3rem); }
    .header-banner h1 { font-family: var(--font-display); font-size: clamp(2rem, 4vw, 3rem); font-weight: 700; }
    .data-badge { display: inline-flex; padding: 0.25rem 0.75rem; border-radius: var(--radius-pill); background: var(--bg-card); border: 1px solid var(--border); font-size: 0.8rem; color: var(--text-secondary); }

    /* === Callout Box (Quick Positioning) === */
    .callout { padding: clamp(1rem, 2vh, 1.5rem); border-radius: var(--radius-lg); background: var(--bg-card); border-left: 4px solid var(--brand-primary); }

    /* === Cards & Grids === */
    .card { padding: clamp(1rem, 2vh, 1.5rem); border-radius: var(--radius-lg); background: var(--bg-card); border: 1px solid var(--border); }
    .card:hover { border-color: var(--border-strong); }
    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }

    /* === Comparison Table === */
    .comparison-table { width: 100%; border-collapse: collapse; }
    .comparison-table th { text-align: left; padding: 0.75rem; border-bottom: 2px solid var(--border-strong); color: var(--text-secondary); font-size: 0.85rem; text-transform: uppercase; }
    .comparison-table td { padding: 0.75rem; border-bottom: 1px solid var(--border); }
    .win { color: var(--success); }
    .loss { color: var(--error); }
    .partial { color: var(--warning); }

    /* === Expandable Objection Handlers === */
    details { border: 1px solid var(--border); border-radius: var(--radius); margin-bottom: 0.5rem; }
    details[open] { border-color: var(--border-strong); }
    summary { padding: 0.75rem 1rem; cursor: pointer; background: var(--bg-card); font-weight: 500; list-style: none; }
    summary::before { content: '+'; font-family: var(--font-mono); color: var(--brand-primary); font-weight: 700; margin-right: 0.5rem; }
    details[open] summary::before { content: '-'; }
    .detail-body { padding: 1rem; border-top: 1px solid var(--border); }

    /* === Win/Loss Scorecard Bar === */
    .score-bar-container { display: flex; height: 2rem; border-radius: var(--radius); overflow: hidden; background: var(--bg-elevated); }
    .score-bar-win { background: var(--success); display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 0.8rem; }
    .score-bar-loss { background: var(--error); display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 0.8rem; }

    /* === Badges (category + threat level) === */
    .badge { display: inline-block; padding: 0.15rem 0.5rem; border-radius: var(--radius-pill); font-size: 0.7rem; font-weight: 600; text-transform: uppercase; }
    .badge-pricing { background: rgba(251, 191, 36, 0.15); color: var(--warning); }
    .badge-feature { background: rgba(59, 130, 246, 0.15); color: var(--brand-primary); }
    .badge-relationship { background: rgba(168, 85, 247, 0.15); color: #a855f7; }
    .badge-risk { background: rgba(248, 113, 113, 0.15); color: var(--error); }
    .threat-high { background: rgba(248, 113, 113, 0.15); color: var(--error); }
    .threat-medium { background: rgba(251, 191, 36, 0.15); color: var(--warning); }
    .threat-low { background: rgba(52, 211, 153, 0.15); color: var(--success); }

    /* === Step Numbers (Trap Questions, Landmines) === */
    .step-number { display: inline-flex; align-items: center; justify-content: center; width: 2rem; height: 2rem; border-radius: 50%; background: var(--brand-primary); color: var(--bg); font-weight: 700; font-size: 0.85rem; }

    /* === Responsive === */
    @media (max-width: 768px) { .grid-2, .grid-3 { grid-template-columns: 1fr; } .sidebar { display: none; } }
    @media print { .sidebar { display: none; } details { break-inside: avoid; } }
    @media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
  </style>
</head>
<body>

  <nav class="sidebar" id="sidebar-nav">
    <!-- Generated by JS: one dot per section -->
  </nav>

  <div class="doc-container">

    <!-- 1. Header Banner -->
    <header class="header-banner" id="section-header">
      <p style="color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.1em; font-size: 0.8rem;">Competitive Battlecard</p>
      <h1>[Your Product] <span style="color: var(--text-muted);">vs</span> [Competitor]</h1>
      <div style="display: flex; gap: 0.75rem; margin-top: 1rem; flex-wrap: wrap;">
        <span class="data-badge">Updated [Date]</span>
        <span class="data-badge">[N] deals</span>
        <span class="data-badge">[N] calls</span>
        <span class="data-badge">[N] proof points</span>
      </div>
    </header>

    <!-- 2. Quick Positioning -->
    <section class="section" id="section-positioning">
      <h2 class="section-title">Quick Positioning</h2>
      <div class="callout">
        <p style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 0.5rem;">When [Competitor] comes up, lead with:</p>
        <p style="font-size: 1.1rem; font-weight: 600;">[One-line differentiator — a point to make, not a line to recite]</p>
      </div>
      <div class="card" style="margin-top: 1rem;">
        <p style="color: var(--text-secondary); font-size: 0.85rem;">Positioning in 30 seconds (in your own words)</p>
        <p>[The 2-3 beats that position us against this competitor]</p>
      </div>
    </section>

    <!-- 3. Competitor Overview (card grid) -->
    <!-- 4. Where We Win (comparison table + deal evidence) -->
    <!-- 5. Where They Win (honest strengths + counter cards) -->
    <!-- 6. Objection Handlers (details/summary accordion by category; summary = risk title, body = "You'll hear" + response points + proof) -->
    <!-- 7. Trap Questions (numbered step cards) -->
    <!-- 8. Landmines to Set (numbered checklist) -->
    <!-- 9. Proof Points (metric cards) -->
    <!-- 10. Win/Loss Scorecard (score-bar + factor lists) -->
    <!-- 11. Displacement Playbook (sequential steps) -->

  </div>

  <script>
    // Sidebar: generate dots from .section elements
    // Intersection Observer highlights active section dot
    // Smooth scroll on dot click
    (function() {
      const sections = document.querySelectorAll('.section');
      const sidebar = document.getElementById('sidebar-nav');
      sections.forEach((section, i) => {
        const dot = document.createElement('a');
        dot.href = '#' + section.id;
        dot.title = section.querySelector('.section-title')?.textContent || '';
        if (i === 0) dot.classList.add('active');
        sidebar.appendChild(dot);
      });
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            sidebar.querySelectorAll('a').forEach(d => d.classList.remove('active'));
            const active = sidebar.querySelector('a[href="#' + entry.target.id + '"]');
            if (active) active.classList.add('active');
          }
        });
      }, { threshold: 0.3 });
      sections.forEach(s => observer.observe(s));
    })();
  </script>
</body>
</html>
```

Populate each placeholder section (`<!-- 3 -->` through `<!-- 11 -->`) with real content from the Step 2 research, using the component patterns shown above.

For **landscape overview** documents, replace the per-competitor sections with:
- **Market Map** — `<table class="comparison-table">` with competitor rows, threat-level badges, and inline score bars
- **Per-Competitor Cards** — `<div class="grid-2">` of `.card` elements, each with: name, positioning, differentiator, top objection risk + counter, win rate mini-bar
- **Cross-Competitor Patterns** — themes, universal differentiators, common objection categories

## Key HTML/CSS Principles

1. **Single page, natural scrolling** — not a slide deck, a vertical reference document
2. **Sticky sidebar** with section navigation dots (hidden on mobile and print)
3. **CSS variable system from the shared style presets** — apply the preset's `:root` block from `../../shared/style-presets.md` (or the brand kit tokens when one is used)
4. **Max-width 950px** centered on the page
5. **Objection handlers as `<details>/<summary>`** — native HTML expand/collapse, no JS required
6. **Win/loss scorecard using CSS bars** — div widths as percentages, green wins, red losses
7. **Color coding:** `--success` (green) for wins/strengths, `--error` (red) for losses/weaknesses, `--warning` (amber) for neutral
8. **Self-contained** — all CSS inline in `<style>`, only external dependency is Google Fonts
9. **Responsive** — grids collapse to single column below 768px
10. **Print-friendly** — sidebar hidden, details preserved

## Delivery Summary Template

```
BATTLECARD READY
================

Folder: .octave-battlecards/battlecard-<competitor>-<date>/
File:   .octave-battlecards/battlecard-<competitor>-<date>/battlecard-<competitor>.html
Style:  [Preset or brand kit name]
Size:   [file size]

Competitor: [Competitor name]
Sections: [N] sections
Data sources: [N] deals, [N] conversation mentions, [N] proof points
Win rate: [X%] (last 180 days)

Navigation:
- Scroll naturally through the document
- Sidebar dots on the right track your position
- Click any dot to jump to that section
- Objection handlers: click to expand/collapse

---

Want me to:
1. Add more objection handlers
2. Go deeper on any section
3. Create displacement outreach for a specific person
4. Generate a version for a different persona
5. Create a presentation version (/octave:deck)
6. Export as PDF
7. Done
```
