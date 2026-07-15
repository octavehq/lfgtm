# HTML Architecture

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Account Brief: [Company] — [Occasion]</title>
  <!-- Google Fonts (preconnect + stylesheet) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* === CSS Variables (from chosen preset) === */
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

    /* === Layout === */
    .brief-container {
      max-width: 900px;
      margin: 0 auto;
      padding: 2rem clamp(1rem, 4vw, 3rem);
    }

    /* === Sidebar Navigation (sticky) === */
    .brief-nav {
      position: fixed;
      top: 50%;
      right: clamp(0.5rem, 2vw, 2rem);
      transform: translateY(-50%);
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      z-index: 100;
    }
    .brief-nav a {
      display: block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--text-muted);
      transition: all 0.3s ease;
    }
    .brief-nav a.active {
      background: var(--brand-primary);
      transform: scale(1.4);
    }

    /* === Section Styles === */
    .brief-section {
      margin-bottom: 2.5rem;
      padding-bottom: 2rem;
      border-bottom: 1px solid var(--border);
    }

    /* === Collapsible Sections (details/summary) === */
    details.brief-section {
      border-bottom: 1px solid var(--border);
      margin-bottom: 2.5rem;
      padding-bottom: 1rem;
    }
    details.brief-section summary {
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
    details.brief-section summary::before {
      content: "\25B6";
      font-size: 0.7em;
      color: var(--brand-primary);
      transition: transform 0.2s ease;
    }
    details.brief-section[open] summary::before {
      transform: rotate(90deg);
    }

    /* === Cards === */
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: clamp(1rem, 2vw, 1.5rem);
    }
    .card:hover {
      background: var(--bg-card-hover);
    }

    /* === Stakeholder Cards === */
    .stakeholder-card {
      display: flex;
      gap: 1rem;
      align-items: flex-start;
    }
    .stakeholder-avatar {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: var(--brand-primary);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: 700;
      flex-shrink: 0;
    }

    /* === Fit Score Bar === */
    .fit-bar {
      height: 8px;
      border-radius: 4px;
      background: var(--bg-elevated);
      overflow: hidden;
      margin: 0.5rem 0;
    }
    .fit-bar-fill {
      height: 100%;
      border-radius: 4px;
      background: var(--success);
      transition: width 0.8s ease;
    }

    /* === Occasion Badge === */
    .occasion-badge {
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

    /* === Timeline === */
    .timeline {
      position: relative;
      padding-left: 2rem;
    }
    .timeline::before {
      content: "";
      position: absolute;
      left: 0.5rem;
      top: 0;
      bottom: 0;
      width: 2px;
      background: var(--border-strong);
    }
    .timeline-event {
      position: relative;
      margin-bottom: 1.5rem;
      padding-left: 1rem;
    }
    .timeline-event::before {
      content: "";
      position: absolute;
      left: -1.75rem;
      top: 0.5rem;
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--brand-primary);
    }

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

    /* === Quick Reference Sidebar === */
    @media (min-width: 1200px) {
      .brief-layout {
        display: grid;
        grid-template-columns: 1fr 280px;
        gap: 2rem;
        max-width: 1200px;
        margin: 0 auto;
      }
      .quick-ref {
        position: sticky;
        top: 2rem;
        align-self: start;
        max-height: calc(100vh - 4rem);
        overflow-y: auto;
      }
    }
    @media (max-width: 1199px) {
      .quick-ref {
        margin-top: 2rem;
        border-top: 2px solid var(--border-strong);
        padding-top: 2rem;
      }
    }

    /* === Print Styles === */
    @media print {
      .brief-nav { display: none; }
      .brief-container { max-width: 100%; padding: 1rem; }
      details.brief-section { open; }
      details.brief-section[open] { break-inside: avoid; }
      .card { break-inside: avoid; }
      body { color: #111; background: white; }
      .occasion-badge { border: 1px solid #111; background: transparent; color: #111; }
    }

    /* === Responsive === */
    @media (max-width: 768px) {
      .grid-2, .grid-3 { grid-template-columns: 1fr; }
      .brief-nav { display: none; }
    }

    /* === prefers-reduced-motion === */
    @media (prefers-reduced-motion: reduce) {
      * { transition: none !important; animation: none !important; }
    }
  </style>
</head>
<body>

  <!-- Sidebar Navigation Dots -->
  <nav class="brief-nav" id="brief-nav">
    <!-- Generated by JS: one dot per section -->
  </nav>

  <!-- Main Brief -->
  <div class="brief-layout">
    <main class="brief-container">

      <!-- Header -->
      <header class="brief-header">
        <span class="occasion-badge">[Occasion] Prep</span>
        <h1>[Account Brief: Company Name]</h1>
        <p class="text-secondary">[Generated date] · [Target person if applicable]</p>
      </header>

      <!-- Sections (use <details> for collapsible, <section> for always-open) -->
      <details class="brief-section" open id="company-snapshot">
        <summary>Company Snapshot</summary>
        <div class="grid-2">
          <!-- Company info cards -->
        </div>
      </details>

      <details class="brief-section" open id="icp-fit">
        <summary>ICP Fit</summary>
        <!-- Fit score bar, segment match, fit reasons -->
      </details>

      <!-- Continue for each section... -->

    </main>

    <!-- Quick Reference Sidebar -->
    <aside class="quick-ref">
      <h3>Quick Reference</h3>
      <!-- Key facts, do's/don'ts, one-line reminders -->
    </aside>
  </div>

  <script>
    // Generate nav dots from sections
    // Intersection Observer for active section tracking
    // Smooth scroll on nav dot click
    // Open all details on print (window.onbeforeprint)
  </script>

</body>
</html>
```

**Self-contained:** Inline CSS, zero external dependencies (except Google Fonts). No JavaScript frameworks.

**Key differences from deck HTML:**
- No scroll-snap (natural page scrolling)
- No slide containers (continuous document flow)
- Collapsible sections via `<details>`/`<summary>` for quick scanning
- Sticky sidebar navigation instead of slide nav dots
- Optional sidebar for quick reference (on wide screens)
- Max-width 900px for comfortable reading
- Print-friendly with `@media print`
