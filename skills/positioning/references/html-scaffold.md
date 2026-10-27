# Positioning System HTML Scaffold

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Positioning System: [Product/Company]</title>
  <meta property="og:title" content="Positioning System: [Product/Company]">
  <meta property="og:description" content="[1-2 sentence summary a stranger understands]">
  <meta property="og:image" content="assets/og.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* === CSS Variables (from chosen preset — see style-presets.md) === */
    :root { /* ... paste chosen preset variables here ... */ }

    /* === Reset & Base === */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body { background: var(--bg); color: var(--text-primary); font-family: var(--font-body); line-height: 1.6; }

    /* === Document Layout (wider than brief — positioning is grid-heavy) === */
    .doc-container { max-width: 1100px; margin: 0 auto; padding: 2rem clamp(1rem, 4vw, 3rem); }

    /* === Sticky Sidebar Navigation === */
    .sidebar { position: fixed; top: 50%; transform: translateY(-50%); right: clamp(0.5rem, 2vw, 2rem); display: flex; flex-direction: column; gap: 0.35rem; z-index: 100; }
    .sidebar a { display: block; width: 8px; height: 8px; border-radius: 50%; background: var(--text-muted); transition: all 0.2s var(--ease); text-decoration: none; }
    .sidebar a.active { background: var(--brand-primary); transform: scale(1.5); }
    .sidebar a:hover { background: var(--brand-500); transform: scale(1.3); }

    /* === Section Base === */
    .pos-section { margin-bottom: clamp(3rem, 6vh, 5rem); padding-top: 1rem; }
    .section-number { font-family: var(--font-mono); font-size: 0.75rem; color: var(--brand-primary); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.25rem; }
    .section-title { font-family: var(--font-display); font-size: clamp(1.4rem, 2.5vw, 2rem); font-weight: 700; margin-bottom: 0.5rem; }
    /* .section-subtitle is the section's lede inside .section-body: a sentence that adds information, never a muted second half of the title */
    .section-subtitle { font-size: clamp(0.85rem, 1.2vw, 1rem); color: var(--text-secondary); margin-bottom: 1.5rem; }

    /* === Collapsible Sections (details/summary) === */
    details.pos-section { border-bottom: 1px solid var(--border); padding-bottom: 2rem; }
    details.pos-section summary { cursor: pointer; list-style: none; display: flex; align-items: center; gap: 0.75rem; }
    details.pos-section summary::-webkit-details-marker { display: none; }
    details.pos-section summary::before { content: "\25B6"; font-size: 0.6em; color: var(--brand-primary); transition: transform 0.2s ease; }
    details.pos-section[open] summary::before { transform: rotate(90deg); }
    details.pos-section .section-body { margin-top: 1.5rem; }

    /* === Header Banner === */
    .header-banner { padding: clamp(2rem, 5vh, 4rem) 0; border-bottom: 1px solid var(--border); margin-bottom: clamp(2rem, 4vh, 3rem); }
    .header-banner h1 { font-family: var(--font-display); font-size: clamp(2rem, 4vw, 3.2rem); font-weight: 700; margin-bottom: 0.5rem; }
    .header-banner .subtitle { font-size: clamp(1rem, 1.5vw, 1.25rem); color: var(--text-secondary); }
    .meta-badges { display: flex; gap: 0.75rem; margin-top: 1.25rem; flex-wrap: wrap; }
    .meta-badge { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.25rem 0.75rem; border-radius: var(--radius-pill); background: var(--bg-card); border: 1px solid var(--border); font-size: 0.8rem; color: var(--text-secondary); }

    /* === Cards & Grids === */
    .card { padding: clamp(1rem, 2vh, 1.5rem); border-radius: var(--radius-lg); background: var(--bg-card); border: 1px solid var(--border); }
    .card:hover { border-color: var(--border-strong); }
    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: clamp(0.75rem, 1.5vw, 1.25rem); }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: clamp(0.75rem, 1.5vw, 1.25rem); }
    .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: clamp(0.75rem, 1.5vw, 1.25rem); }
    .grid-5 { display: grid; grid-template-columns: repeat(5, 1fr); gap: clamp(0.75rem, 1.5vw, 1rem); }
    .grid-2 > *, .grid-3 > *, .grid-4 > *, .grid-5 > * { min-width: 0; }

    /* === Callout Box === */
    .callout { padding: clamp(1rem, 2vh, 1.5rem); border-radius: var(--radius-lg); background: var(--bg-card); border-left: 4px solid var(--brand-primary); }

    /* === Tables === */
    .data-table { width: 100%; border-collapse: collapse; font-size: clamp(0.8rem, 1vw, 0.9rem); }
    .data-table th { text-align: left; padding: 0.75rem; border-bottom: 2px solid var(--border-strong); color: var(--text-secondary); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }
    .data-table td { padding: 0.75rem; border-bottom: 1px solid var(--border); vertical-align: top; }

    /* === Persona Colors: derived from the brand kit, never a fixed rainbow === */
    /* A kit often allows one accent family, so personas take steps of it plus neutrals; the persona name always sits next to its colour, so colour is never the only cue. */
    :root {
      --persona-user: var(--brand-primary);
      --persona-champion: var(--brand-accent, color-mix(in srgb, var(--brand-primary) 65%, var(--text-primary)));
      --persona-decision: color-mix(in srgb, var(--brand-primary) 45%, var(--bg));
      --persona-financial: var(--text-primary);
      --persona-technical: var(--text-muted);
    }
    .persona-user { border-color: var(--persona-user); }
    .persona-champion { border-color: var(--persona-champion); }
    .persona-decision { border-color: var(--persona-decision); }
    .persona-financial { border-color: var(--persona-financial); }
    .persona-technical { border-color: var(--persona-technical); }
    .persona-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 0.4rem; background: var(--text-muted); }
    .persona-user .persona-dot, .persona-dot-user { background: var(--persona-user); }
    .persona-champion .persona-dot, .persona-dot-champion { background: var(--persona-champion); }
    .persona-decision .persona-dot, .persona-dot-decision { background: var(--persona-decision); }
    .persona-financial .persona-dot, .persona-dot-financial { background: var(--persona-financial); }
    .persona-technical .persona-dot, .persona-dot-technical { background: var(--persona-technical); }

    /* === Badges === */
    .badge { display: inline-block; padding: 0.15rem 0.5rem; border-radius: var(--radius-pill); font-size: 0.75rem; font-weight: 600; } /* no uppercase: badges carry product and feature names in their own case */
    .badge-primary { background: color-mix(in srgb, var(--brand-primary) 15%, transparent); color: var(--brand-primary); }
    .badge-neutral { background: var(--bg-card); border: 1px solid var(--border); color: var(--text-secondary); }
    .badge-success { background: color-mix(in srgb, var(--success) 15%, transparent); color: var(--success); }
    .badge-warning { background: color-mix(in srgb, var(--warning) 15%, transparent); color: var(--warning); }
    .badge-error { background: color-mix(in srgb, var(--error) 15%, transparent); color: var(--error); }

    /* === Highlighted Text (for positioning anchors) === */
    /* Emphasis follows the kit's emphasis rule: its emphasis ink and weight. Add a background wash only when the kit's guardrails allow one; the type classes stay as hooks. */
    .highlight { font-weight: var(--brand-emph-weight, 600); color: var(--brand-emph-ink-light, var(--brand-primary)); }

    /* === Section-specific layouts — see references/section-layouts.md === */
    /* Included inline: message framework bands, funnel columns, timeline, canvas split */

    /* === Responsive === */
    @media (max-width: 768px) {
      .grid-2, .grid-3, .grid-4, .grid-5 { grid-template-columns: 1fr; }
      .sidebar { display: none; }
      .funnel-grid { grid-template-columns: 1fr; }
      .canvas-split { grid-template-columns: 1fr; }
      .timeline-phases { overflow-x: auto; }
    }

    @media (max-width: 520px) { .meta-badges { display: none; } }
    @media (max-width: 375px) { .doc-container { padding-left: 16px; padding-right: 16px; } }

    /* === Print === */
    @media print {
      .sidebar { display: none; }
      details.pos-section { break-inside: avoid; }
      details.pos-section[open] { break-inside: avoid; }
      .card { break-inside: avoid; }
      body { color: #111; background: white; }
      .meta-badge { border: 1px solid #ccc; background: transparent; }
    }

    /* === prefers-reduced-motion === */
    @media (prefers-reduced-motion: reduce) {
      * { transition: none !important; animation: none !important; }
    }
  </style>
</head>
<body>

  <!-- Sidebar Navigation Dots -->
  <nav class="sidebar" id="sidebar-nav">
    <!-- Generated by JS: one dot per section -->
  </nav>

  <div class="doc-container">

    <!-- Header Banner -->
    <header class="header-banner" id="section-header">
      <p style="color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.1em; font-size: 0.8rem; margin-bottom: 0.5rem;">Messaging & Positioning System</p>
      <h1>[Product / Company Name]</h1>
      <p class="subtitle">[Product category] for [primary persona] in [target segment]</p>
      <div class="meta-badges">
        <span class="meta-badge">Generated [Date]</span>
        <span class="meta-badge">[N] Personas</span>
        <span class="meta-badge">[N] Use Cases</span>
        <span class="meta-badge">[N] Value Props</span>
        <span class="meta-badge">[N] Proof Points</span>
      </div>
    </header>

    <!-- Section 1: Message Framework -->
    <!-- Section 2: Positioning Anchors -->
    <!-- Section 3: Positioning Strategy -->
    <!-- Section 4: Persona-Based Messaging -->
    <!-- Section 5: Value Prop by Awareness Stage -->
    <!-- Section 6: Use Case Messaging Canvas -->
    <!-- Section 7: Use Case Lifecycle -->
    <!-- Section 8: Homepage Messaging -->
    <!-- See references/section-templates.md for full HTML per section -->

  </div>

  <script>
    // Sidebar: generate dots from .pos-section elements
    // Intersection Observer highlights active section dot
    // Smooth scroll on dot click
    // Open all details on print
    (function() {
      const sections = document.querySelectorAll('.pos-section');
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
      }, { threshold: 0.2 });
      sections.forEach(s => observer.observe(s));
      window.onbeforeprint = () => {
        document.querySelectorAll('details.pos-section').forEach(d => d.open = true);
      };
    })();
  </script>

</body>
</html>
```

**Robustness:** text containers grow and wide grids scroll inside their own container, never clipped (presentation principles [9i, 9k, 9l](../../shared/presentation-principles.md)). If the user asks for a positioning map or any 2x2, follow principle 15b: labels inside each box, no arrows, the item's current box marked, and the condition that moves it written as text.

**Self-contained:** Inline CSS, zero external dependencies (except Google Fonts). No JavaScript frameworks.

**Key differences from brief/battlecard-doc HTML:**
- **Max-width 1100px** (wider — positioning frameworks need horizontal space for grids)
- **Persona colours from the brand kit**: the `--persona-*` tokens take steps of the kit's primary and accent plus its neutrals, the same in all 8 sections, and each persona keeps its name label so colour is never the only cue
- **Highlight classes**: mark positioning anchor keywords (category, persona, use case, problem, feature) with the kit's emphasis ink, a wash only where the kit allows it
- **Grid-4 and Grid-5** — for persona columns and awareness stage columns
- **Section numbering** — "Section 01" labels for clear progression through the exercise
