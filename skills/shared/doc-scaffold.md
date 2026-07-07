# Document HTML Scaffold (shared)

The canonical scaffold for every **scrollable document** skill (brief, meeting-prep, proposal, positioning, one-pager, microsite, battlecard doc, wins-losses report). Decks are different — they use the fixed 1920×1080 stage in `../deck/references/html-scaffold.md`, not this file.

**This is a component-pattern reference, not a fixed stylesheet to reproduce verbatim.** Adapt it: drive the palette, type, and logo from the brand kit (`~/.octave/brands/<slug>/`, see [brand-kit-usage.md](brand-kit-usage.md)) or the chosen preset ([style-presets.md](style-presets.md)) so the output reads like real collateral, not a generic template. Each skill's own `references/` file lists only its skill-specific components and deltas on top of this base.

Two rules hold regardless of brand (see [presentation-principles.md](presentation-principles.md) → Links and chrome):
1. **Every external `<a>` opens in a new tab** — `target="_blank" rel="noopener noreferrer"` (in-page `#` anchors excepted).
2. **Scrollbars are themed** — never the bare default OS scrollbar on a styled surface.

The `[…]` below are placeholders — fill with real values, never literal brackets.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Document Title]</title>
  <!-- Google Fonts (preconnect + stylesheet) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* === CSS Variables (from brand kit tokens or chosen preset) === */
    :root { ... }

    /* === Reset & Base === */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      background: var(--bg);
      color: var(--text-primary);
      font-family: var(--font-body);
      line-height: 1.6;
    }
    a { color: var(--brand-primary); text-decoration: none; }
    a:hover { text-decoration: underline; }

    /* === Themed scrollbars (mandatory) === */
    html { scrollbar-width: thin; scrollbar-color: var(--border-strong) transparent; }
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 9999px; border: 2px solid var(--bg); }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

    /* === Layout (adjust max-width per skill: 800-1100px) === */
    .doc-container {
      max-width: 900px;
      margin: 0 auto;
      padding: 2rem clamp(1rem, 4vw, 3rem);
    }

    /* === Sticky Sidebar Navigation (dots) === */
    .doc-nav {
      position: fixed;
      top: 50%;
      right: clamp(0.5rem, 2vw, 2rem);
      transform: translateY(-50%);
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      z-index: 100;
    }
    .doc-nav a {
      display: block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--text-muted);
      transition: all 0.3s ease;
    }
    .doc-nav a.active { background: var(--brand-primary); transform: scale(1.4); }

    /* === Sections === */
    .doc-section {
      margin-bottom: 2.5rem;
      padding-bottom: 2rem;
      border-bottom: 1px solid var(--border);
    }

    /* === Collapsible Sections (details/summary) === */
    details.doc-section summary {
      cursor: pointer;
      font-family: var(--font-display);
      font-size: clamp(1.1rem, 2vw, 1.4rem);
      font-weight: 600;
      color: var(--text-primary);
      padding: 0.75rem 0;
      list-style: none;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    details.doc-section summary::before {
      content: "\25B6";
      font-size: 0.7em;
      color: var(--brand-primary);
      transition: transform 0.2s ease;
    }
    details.doc-section[open] summary::before { transform: rotate(90deg); }

    /* === Cards, Callouts & Badges === */
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: clamp(1rem, 2vw, 1.5rem);
    }
    .card:hover { background: var(--bg-card-hover); }
    .callout { padding: clamp(1rem, 2vh, 1.5rem); border-radius: var(--radius-lg); background: var(--bg-card); border-left: 4px solid var(--brand-primary); }
    .badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: var(--radius-pill);
      background: var(--brand-primary);
      color: white;
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    /* === Data tables === */
    .data-table { width: 100%; border-collapse: collapse; }
    .data-table th { text-align: left; padding: 0.75rem; border-bottom: 2px solid var(--border-strong); color: var(--text-secondary); font-size: 0.85rem; text-transform: uppercase; }
    .data-table td { padding: 0.75rem; border-bottom: 1px solid var(--border); vertical-align: top; }

    /* === Grid Utilities === */
    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: clamp(0.75rem, 1.5vw, 1.25rem); }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: clamp(0.75rem, 1.5vw, 1.25rem); }

    /* === Typography === */
    .section-title {
      font-family: var(--font-display);
      font-size: clamp(1.1rem, 2vw, 1.4rem);
      font-weight: 600;
      margin-bottom: 1rem;
    }
    .body-text { font-size: clamp(0.85rem, 1.2vw, 1rem); }
    .text-secondary { color: var(--text-secondary); }
    .text-muted { color: var(--text-muted); }

    /* === Print Styles === */
    @media print {
      .doc-nav { display: none; }
      .doc-container { max-width: 100%; padding: 1rem; }
      details.doc-section[open] { break-inside: avoid; }
      .card { break-inside: avoid; }
      body { color: #111; background: white; }
      .badge { border: 1px solid #111; background: transparent; color: #111; }
    }

    /* === Responsive === */
    @media (max-width: 768px) {
      .grid-2, .grid-3 { grid-template-columns: 1fr; }
      .doc-nav { display: none; }
    }

    /* === prefers-reduced-motion === */
    @media (prefers-reduced-motion: reduce) {
      * { transition: none !important; animation: none !important; }
    }
  </style>
</head>
<body>

  <!-- Sidebar Navigation Dots -->
  <nav class="doc-nav" id="doc-nav"></nav>

  <main class="doc-container">

    <!-- Header -->
    <header class="doc-section">
      <span class="badge">[Doc Type]</span>
      <h1>[Title]</h1>
      <p class="text-secondary">[Generated date] · [Subject / context]</p>
    </header>

    <!-- Sections: use <details class="doc-section" open> for collapsible,
         <section class="doc-section"> for always-open -->
    <details class="doc-section" open id="[section-id]">
      <summary>[Section Title]</summary>
      <!-- Section content -->
    </details>

  </main>

  <script>
    // Sidebar: generate dots from sections, track the active one, smooth-scroll on click,
    // and open all <details> before printing.
    (function() {
      const sections = document.querySelectorAll('.doc-section[id]');
      const nav = document.getElementById('doc-nav');
      sections.forEach((section, i) => {
        const dot = document.createElement('a');
        dot.href = '#' + section.id;
        dot.title = section.querySelector('summary, .section-title, h1, h2')?.textContent || '';
        if (i === 0) dot.classList.add('active');
        nav.appendChild(dot);
      });
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            nav.querySelectorAll('a').forEach(d => d.classList.remove('active'));
            const active = nav.querySelector('a[href="#' + entry.target.id + '"]');
            if (active) active.classList.add('active');
          }
        });
      }, { threshold: 0.25 });
      sections.forEach(s => observer.observe(s));
      window.onbeforeprint = () => {
        document.querySelectorAll('details.doc-section').forEach(d => d.open = true);
      };
    })();
  </script>

</body>
</html>
```

**Self-contained:** inline CSS, zero external dependencies except Google Fonts. No JavaScript frameworks.

**Key differences from deck HTML:**
- No scroll-snap, no slide containers — natural page scrolling, continuous document flow
- Collapsible sections via `<details>`/`<summary>` for quick scanning
- Sticky sidebar dots instead of slide navigation
- Print-friendly with `@media print` (buyers and sellers print these)
- Typography and spacing use `clamp()` reflow, not the fixed px canvas
