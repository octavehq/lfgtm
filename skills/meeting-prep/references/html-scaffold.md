# Battle Plan HTML Scaffold

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Battle Plan: [Company] — [Meeting Type]</title>
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
    .battle-plan-container {
      max-width: 900px;
      margin: 0 auto;
      padding: 2rem clamp(1rem, 4vw, 3rem);
    }

    /* === Sidebar Navigation (sticky) === */
    .bp-nav {
      position: fixed;
      top: 50%;
      right: clamp(0.5rem, 2vw, 2rem);
      transform: translateY(-50%);
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      z-index: 100;
    }
    .bp-nav a {
      display: block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--text-muted);
      transition: all 0.3s ease;
    }
    .bp-nav a.active {
      background: var(--brand-primary);
      transform: scale(1.4);
    }

    /* === Section Styles === */
    .bp-section {
      margin-bottom: 2.5rem;
      padding-bottom: 2rem;
      border-bottom: 1px solid var(--border);
    }

    /* === Collapsible Sections (details/summary) === */
    details.bp-section {
      border-bottom: 1px solid var(--border);
      margin-bottom: 2.5rem;
      padding-bottom: 1rem;
    }
    details.bp-section summary {
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
    details.bp-section summary::before {
      content: "\25B6";
      font-size: 0.7em;
      color: var(--brand-primary);
      transition: transform 0.2s ease;
    }
    details.bp-section[open] summary::before {
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

    /* === Buying Role Badge === */
    .role-badge {
      display: inline-block;
      padding: 0.2rem 0.6rem;
      border-radius: var(--radius-pill);
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .role-badge.champion { background: var(--success); color: white; }
    .role-badge.budget-owner { background: var(--brand-primary); color: white; }
    .role-badge.evaluator { background: var(--secondary); color: white; }
    .role-badge.gatekeeper { background: var(--warning); color: #1a1a1a; }

    /* === Belief Stack === */
    .belief-item {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.75rem 1rem;
      border-radius: var(--radius);
      margin-bottom: 0.5rem;
    }
    .belief-status {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      flex-shrink: 0;
    }
    .belief-status.proven { background: var(--success); }
    .belief-status.mostly-proven { background: var(--warning); }
    .belief-status.needs-proof { background: var(--error); }

    /* === Talk Track Cards === */
    .talk-track {
      background: var(--bg-elevated);
      border-left: 3px solid var(--brand-primary);
      padding: 1rem 1.25rem;
      border-radius: 0 var(--radius) var(--radius) 0;
      margin-bottom: 1rem;
    }
    .talk-track .label {
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--brand-primary);
      margin-bottom: 0.25rem;
    }
    .coaching-note {
      font-size: 0.8rem;
      color: var(--text-muted);
      font-style: italic;
      margin-top: 0.5rem;
    }

    /* === Risk/Mitigation Grid === */
    .risk-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: clamp(0.75rem, 1.5vw, 1.25rem);
    }
    .risk-item { border-left: 3px solid var(--error); }
    .mitigation-item { border-left: 3px solid var(--success); }

    /* === Game Plan Timeline === */
    .game-plan-phase {
      display: grid;
      grid-template-columns: 100px 1fr;
      gap: 1rem;
      padding: 1rem 0;
      border-bottom: 1px solid var(--border);
    }
    .phase-time {
      font-family: var(--font-mono);
      font-size: 0.85rem;
      color: var(--brand-primary);
      font-weight: 600;
    }

    /* === The Line (featured) === */
    .the-line {
      text-align: center;
      padding: 2rem;
      border: 2px solid var(--brand-primary);
      border-radius: var(--radius-lg);
      margin-top: 2rem;
    }
    .the-line blockquote {
      font-family: var(--font-display);
      font-size: clamp(1.2rem, 2.5vw, 1.6rem);
      font-weight: 500;
      font-style: italic;
      color: var(--text-primary);
    }

    /* === Meeting Type Badge === */
    .meeting-badge {
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
    .duration-badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: var(--radius-pill);
      background: var(--bg-elevated);
      border: 1px solid var(--border-strong);
      color: var(--text-secondary);
      font-size: 0.75rem;
      font-weight: 600;
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

    /* === Deal Intel Cards === */
    .deal-intel-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: clamp(0.75rem, 1.5vw, 1.25rem);
    }
    .deal-intel-card {
      text-align: center;
      padding: 1rem;
    }
    .deal-intel-card .label {
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 0.25rem;
    }
    .deal-intel-card .value {
      font-family: var(--font-display);
      font-size: 1.1rem;
      font-weight: 600;
    }

    /* === Print Styles === */
    @media print {
      .bp-nav { display: none; }
      .battle-plan-container { max-width: 100%; padding: 1rem; }
      details.bp-section { open; }
      details.bp-section[open] { break-inside: avoid; }
      .card { break-inside: avoid; }
      body { color: #111; background: white; }
      .meeting-badge { border: 1px solid #111; background: transparent; color: #111; }
    }

    /* === Responsive === */
    @media (max-width: 768px) {
      .grid-2, .grid-3 { grid-template-columns: 1fr; }
      .risk-grid { grid-template-columns: 1fr; }
      .game-plan-phase { grid-template-columns: 80px 1fr; }
      .bp-nav { display: none; }
    }

    /* === prefers-reduced-motion === */
    @media (prefers-reduced-motion: reduce) {
      * { transition: none !important; animation: none !important; }
    }
  </style>
</head>
<body>

  <!-- Sidebar Navigation Dots -->
  <nav class="bp-nav" id="bp-nav">
    <!-- Generated by JS: one dot per section -->
  </nav>

  <!-- Main Battle Plan -->
  <main class="battle-plan-container">

    <!-- 1. Header -->
    <header class="bp-section">
      <span class="meeting-badge">[Meeting Type] Battle Plan</span>
      <span class="duration-badge">[Duration] min</span>
      <h1>[Company Name] — Meeting Prep</h1>
      <p class="text-secondary">[Date] · [Attendees summary]</p>
    </header>

    <!-- 2. TL;DR -->
    <section class="bp-section" id="tldr">
      <h2 class="section-title">TL;DR</h2>
      <p class="body-text">[2-3 sentence opportunity summary]</p>
    </section>

    <!-- 3. Stakeholder Map -->
    <details class="bp-section" open id="stakeholder-map">
      <summary>Stakeholder Map</summary>
      <div class="grid-2">
        <!-- Stakeholder cards with role badges -->
      </div>
    </details>

    <!-- 4. Their Pain -->
    <details class="bp-section" open id="their-pain">
      <summary>Their Pain</summary>
      <!-- Pain points by stakeholder or theme -->
    </details>

    <!-- 5. What They Need to Believe -->
    <details class="bp-section" open id="belief-stack">
      <summary>What They Need to Believe</summary>
      <!-- Belief items with status indicators -->
    </details>

    <!-- 6. Positioned Sales Pitch -->
    <details class="bp-section" open id="sales-pitch">
      <summary>Positioned Sales Pitch</summary>
      <!-- 5-step talk track cards -->
    </details>

    <!-- 7. Discovery Questions -->
    <details class="bp-section" open id="discovery-questions">
      <summary>Discovery Questions</summary>
      <!-- Questions segmented by stakeholder or category -->
    </details>

    <!-- 8. Landmines & Watch-Outs -->
    <details class="bp-section" open id="landmines">
      <summary>Landmines & Watch-Outs</summary>
      <div class="risk-grid">
        <!-- Risk/mitigation pairs -->
      </div>
    </details>

    <!-- 9. Coach's Corner -->
    <details class="bp-section" open id="coachs-corner">
      <summary>Coach's Corner</summary>
      <div class="grid-2">
        <!-- Strategic coach card + Positioning coach card -->
      </div>
    </details>

    <!-- 10. Meeting Game Plan -->
    <details class="bp-section" open id="game-plan">
      <summary>Meeting Game Plan</summary>
      <!-- Phase timeline matched to duration -->
    </details>

    <!-- 11. Deal Intelligence -->
    <details class="bp-section" open id="deal-intel">
      <summary>Deal Intelligence</summary>
      <div class="deal-intel-grid">
        <!-- Budget, Champion, Decision Maker, Compelling Event cards -->
      </div>
    </details>

    <!-- 12. The Line -->
    <section class="bp-section" id="the-line">
      <div class="the-line">
        <blockquote>"[One memorable sentence]"</blockquote>
      </div>
    </section>

  </main>

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
