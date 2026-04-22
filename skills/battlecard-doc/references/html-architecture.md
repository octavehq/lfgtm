# HTML Architecture

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
    /* === CSS Variables (from chosen style preset — see style-presets.md) === */
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
        <p style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 0.5rem;">When you hear "[Competitor]", say:</p>
        <p style="font-size: 1.1rem; font-weight: 600;">"[One-liner]"</p>
      </div>
      <div class="card" style="margin-top: 1rem;">
        <p style="color: var(--text-secondary); font-size: 0.85rem;">30-Second Pitch</p>
        <p>"[Elevator pitch positioned against this competitor]"</p>
      </div>
    </section>

    <!-- 3. Competitor Overview (card grid) -->
    <!-- 4. Where We Win (comparison table + deal evidence) -->
    <!-- 5. Where They Win (honest strengths + counter cards) -->
    <!-- 6. Objection Handlers (details/summary accordion by category) -->
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

Populate each placeholder section (`<!-- 3 -->` through `<!-- 11 -->`) with real content from the Octave context gathered in Step 2, using the component patterns shown above.

For **landscape overview** documents, replace the per-competitor sections with:
- **Market Map** -- `<table class="comparison-table">` with competitor rows, threat-level badges, and inline score bars
- **Per-Competitor Cards** -- `<div class="grid-2">` of `.card` elements, each with: name, positioning, differentiator, top objection/counter, win rate mini-bar
- **Cross-Competitor Patterns** -- themes, universal differentiators, common objections

---

#### Key HTML/CSS Principles

1. **Single page, natural scrolling** -- not a slide deck, a vertical reference document
2. **Sticky sidebar** with section navigation dots (hidden on mobile and print)
3. **Same CSS variable system as `/octave:deck`** -- apply the preset's `:root` block from style-presets.md
4. **Max-width 950px** centered on the page
5. **Objection handlers as `<details>/<summary>`** -- native HTML expand/collapse, no JS required
6. **Win/loss scorecard using CSS bars** -- div widths as percentages, green wins, red losses
7. **Color coding:** `--success` (green) for wins/strengths, `--error` (red) for losses/weaknesses, `--warning` (amber) for neutral
8. **Self-contained** -- all CSS inline in `<style>`, only external dependency is Google Fonts
9. **Responsive** -- grids collapse to single column below 768px
10. **Print-friendly** -- sidebar hidden, details preserved
