# Meeting Prep HTML Scaffold

**This is a component-pattern reference, not a fixed stylesheet to reproduce verbatim.** Adapt it: drive the palette, type, and logo from the brand kit (`~/.octave/brands/<slug>/`) so the output reads like the sender's real collateral, not a generic dark template. Two rules hold regardless of brand: **every `<a>` opens in a new tab** (`target="_blank" rel="noopener noreferrer"`), and **scrollbars are themed** (never the bare default OS scrollbar on a styled surface). The `[…]` are placeholders — fill with real values, never literal brackets.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Meeting Prep: [Company] — [Meeting Type]</title>
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
    /* Links: brand-colored, and every <a> in the markup carries target="_blank" rel="noopener noreferrer" */
    a { color: var(--brand-primary); text-decoration: none; }
    a:hover { text-decoration: underline; }

    /* === Themed scrollbars (never the bare default OS bar on a dark surface) === */
    html { scrollbar-width: thin; scrollbar-color: var(--border-strong) transparent; }
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 9999px; border: 2px solid var(--bg); }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

    /* === Layout === */
    .prep-container {
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
    .card:hover { background: var(--bg-card-hover); }

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
    .stakeholder-card a { color: var(--brand-primary); text-decoration: none; }
    .stakeholder-card a:hover { text-decoration: underline; }

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
    .role-badge.economic-buyer { background: var(--brand-primary); color: white; }
    .role-badge.champion       { background: var(--success); color: white; }
    .role-badge.evaluator      { background: var(--secondary); color: white; }
    .role-badge.influencer     { background: var(--bg-elevated); color: var(--text-secondary); border: 1px solid var(--border-strong); }
    .role-badge.blocker        { background: var(--error); color: white; }

    /* === Unconfirmed flag (grounding) === */
    .unconfirmed {
      display: inline-block;
      padding: 0.15rem 0.5rem;
      border-radius: var(--radius-pill);
      font-size: 0.68rem;
      font-weight: 600;
      background: transparent;
      border: 1px dashed var(--warning);
      color: var(--warning);
    }
    .unconfirmed::before { content: "\26A0 "; }

    /* === Snapshot strip (deal state — merged, not repeated lower) === */
    .snapshot-strip {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: clamp(0.75rem, 1.5vw, 1.25rem);
      margin: 1rem 0;
    }
    .snapshot-cell { text-align: center; padding: 0.75rem; }
    .snapshot-cell .label {
      font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
      letter-spacing: 0.05em; color: var(--text-muted); margin-bottom: 0.25rem;
    }
    .snapshot-cell .value { font-family: var(--font-display); font-size: 1.05rem; font-weight: 600; }
    .outcome-line {
      border-left: 3px solid var(--brand-primary);
      padding: 0.75rem 1rem; background: var(--bg-elevated);
      border-radius: 0 var(--radius) var(--radius) 0; margin-top: 1rem;
    }

    /* === News items (dated + sourced) === */
    .news-item { padding: 0.75rem 0; border-bottom: 1px solid var(--border); }
    .news-item .meta { font-size: 0.75rem; color: var(--text-muted); }
    .news-item .so-what { font-size: 0.85rem; color: var(--text-secondary); font-style: italic; margin-top: 0.25rem; }
    .news-item a { color: var(--brand-primary); }

    /* === Similar-customer / reference cards === */
    .reference-card { border-left: 3px solid var(--success); }

    /* === Per-persona block (why-us per persona) === */
    .persona-block {
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: clamp(1rem, 2vw, 1.5rem);
      margin-bottom: 1rem;
    }
    .persona-block h4 { font-family: var(--font-display); margin-bottom: 0.5rem; }
    .persona-block .lane-label {
      font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
      letter-spacing: 0.05em; color: var(--brand-primary); margin: 0.5rem 0 0.25rem;
    }

    /* === The Winning Story (numbered beats) === */
    .story-beat {
      display: grid; grid-template-columns: 32px 1fr; gap: 0.75rem;
      padding: 0.6rem 0; align-items: start;
    }
    .story-beat .num {
      width: 28px; height: 28px; border-radius: 50%;
      background: var(--brand-primary); color: white;
      display: flex; align-items: center; justify-content: center;
      font-weight: 700; font-size: 0.85rem;
    }

    /* === How to Run the Conversation — beats / listen-for / ask-for === */
    .beat {
      background: var(--bg-elevated);
      border-left: 3px solid var(--brand-primary);
      padding: 0.9rem 1.1rem;
      border-radius: 0 var(--radius) var(--radius) 0;
      margin-bottom: 0.9rem;
    }
    .beat .point { font-weight: 600; }
    .beat .listen-for, .beat .ask-for {
      font-size: 0.82rem; margin-top: 0.4rem; color: var(--text-secondary);
    }
    .beat .listen-for::before { content: "Listen for — "; color: var(--text-muted); font-weight: 600; }
    .beat .ask-for::before    { content: "Ask for — ";    color: var(--success);    font-weight: 600; }

    /* === Discovery questions === */
    .question-item { padding: 0.6rem 0; border-bottom: 1px solid var(--border); }
    .question-item .reveals { font-size: 0.8rem; color: var(--text-muted); font-style: italic; margin-top: 0.2rem; }
    .question-item .reveals::before { content: "Reveals: "; }

    /* === Objections === */
    .objection-item { padding: 0.75rem 0; border-bottom: 1px solid var(--border); }
    .objection-item .obj { font-weight: 600; }
    .objection-item .response { font-size: 0.9rem; color: var(--text-secondary); margin-top: 0.25rem; }
    .objection-item .response::before { content: "\21B3 "; color: var(--success); }

    /* === Competitors / alternatives === */
    .competitor-row {
      display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.75rem;
      padding: 0.75rem 0; border-bottom: 1px solid var(--border);
    }
    .competitor-row .col-label {
      font-size: 0.68rem; font-weight: 600; text-transform: uppercase;
      letter-spacing: 0.05em; color: var(--text-muted);
    }
    .watch-out { border-left: 3px solid var(--warning); padding: 0.6rem 1rem; margin-top: 0.75rem; }

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

    /* === Meeting Type / Duration Badges === */
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

    /* === Print Styles === */
    @media print {
      .bp-nav { display: none; }
      .prep-container { max-width: 100%; padding: 1rem; }
      details.bp-section[open] { break-inside: avoid; }
      .card, .persona-block, .beat { break-inside: avoid; }
      body { color: #111; background: white; }
      .meeting-badge { border: 1px solid #111; background: transparent; color: #111; }
    }

    /* === Responsive === */
    @media (max-width: 768px) {
      .grid-2, .grid-3 { grid-template-columns: 1fr; }
      .competitor-row { grid-template-columns: 1fr; }
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

  <!-- Main Prep -->
  <main class="prep-container">

    <!-- 1. Header -->
    <header class="bp-section">
      <span class="meeting-badge">[Meeting Type] Prep</span>
      <span class="duration-badge">[Duration] min</span>
      <h1>[Company Name] — Meeting Prep</h1>
      <p class="text-secondary">
        [Date] ·
        <!-- Attendees: each linked to verified LinkedIn; ⚠ unconfirmed flag where needed. Every <a> opens in a new tab. -->
        <a href="[linkedin]" target="_blank" rel="noopener noreferrer">[Name]</a> ([Role]) ·
        <a href="[company-website]" target="_blank" rel="noopener noreferrer">[company.com]</a>
      </p>
    </header>

    <!-- 2. Snapshot (merged TL;DR + deal state — do NOT repeat deal intel later) -->
    <section class="bp-section" id="snapshot">
      <h2 class="section-title">Snapshot</h2>
      <p class="body-text">[2-3 sentence situation: who they are, what's at stake, the play]</p>
      <div class="snapshot-strip">
        <!-- Only render the cells that are actually known -->
        <div class="snapshot-cell"><div class="label">Stage</div><div class="value">[…]</div></div>
        <div class="snapshot-cell"><div class="label">Compelling Event</div><div class="value">[…]</div></div>
        <div class="snapshot-cell"><div class="label">Champion</div><div class="value">[…]</div></div>
        <div class="snapshot-cell"><div class="label">Competition</div><div class="value">[…]</div></div>
        <div class="snapshot-cell"><div class="label">Next Milestone</div><div class="value">[…]</div></div>
      </div>
      <div class="outcome-line"><strong>What we want out of this meeting:</strong> [one specific advance]</div>
    </section>

    <!-- 3. Why This Company, Why Now -->
    <details class="bp-section" open id="why-company">
      <summary>Why This Company, Why Now</summary>
      <h3>Fit</h3>
      <!-- segment/ICP match + 3-5 fit reasons -->
      <h3>Why now</h3>
      <!-- trigger / compelling event -->
      <h3>Recent news</h3>
      <div class="news-item">
        <div><strong>[Headline]</strong></div>
        <div class="meta">[Date] · <a href="[source]" target="_blank" rel="noopener noreferrer">[source]</a></div>
        <div class="so-what">[so-what for this meeting]</div>
      </div>
      <h3>Their market</h3>
      <!-- segment-level intel relevant to our value -->
      <h3>Similar customers</h3>
      <div class="grid-2">
        <!-- Internal doc: link the reference entity to its Octave source via /entity/{oId} -->
        <div class="card reference-card"><a href="https://app.octavehq.com/entity/{re_oId}" target="_blank" rel="noopener noreferrer">[Company like them]</a> — [outcome]</div>
      </div>
    </details>

    <!-- 4. Stakeholders -->
    <details class="bp-section" open id="stakeholders">
      <summary>Stakeholders</summary>
      <div class="grid-2">
        <div class="card stakeholder-card">
          <div class="stakeholder-avatar">[Initials]</div>
          <div>
            <div><strong><a href="[verified-linkedin]" target="_blank" rel="noopener noreferrer">[Name]</a></strong> — [Title]
              <span class="role-badge champion">Champion</span>
              <!-- or: <span class="unconfirmed">Unconfirmed — verify before call</span> -->
            </div>
            <div class="text-secondary">[What they care about — role priorities]</div>
            <div class="text-muted">[How to engage]</div>
          </div>
        </div>
      </div>
    </details>

    <!-- 5. Why [Product] for Each Persona -->
    <details class="bp-section" open id="why-us-persona">
      <summary>Why [Product] for Each Persona</summary>
      <div class="persona-block">
        <h4>[Persona type — e.g. Engineering Lead]</h4>
        <div class="lane-label">Why they care</div>
        <p>[their world + pains this role feels]</p>
        <div class="lane-label">Why [Product] for them</div>
        <p>[value framed for this role's outcome]</p>
        <div class="lane-label">Top use cases</div>
        <ul><li>[use case]</li></ul>
      </div>
      <h3>Top use cases for this company</h3>
      <ul><li>[account-level use case]</li></ul>
    </details>

    <!-- 6. The Winning Story -->
    <details class="bp-section" open id="winning-story">
      <summary>The Winning Story</summary>
      <div class="story-beat"><div class="num">1</div><div><strong>Their world today</strong> — […]</div></div>
      <div class="story-beat"><div class="num">2</div><div><strong>What's breaking</strong> — […]</div></div>
      <div class="story-beat"><div class="num">3</div><div><strong>Why now</strong> — […]</div></div>
      <div class="story-beat"><div class="num">4</div><div><strong>Why [Product]</strong> — […]</div></div>
      <div class="story-beat"><div class="num">5</div><div><strong>Proof</strong> — [similar customer + outcome]</div></div>
    </details>

    <!-- 7. How to Run the Conversation (beats — NOT a script, NOT timed) -->
    <details class="bp-section" open id="run-conversation">
      <summary>How to Run the Conversation</summary>
      <div class="beat">
        <div class="point">[Talking point / beat — an idea, not a quote]</div>
        <div class="listen-for">[signal / phrase / reaction to watch for]</div>
        <div class="ask-for">[the specific advance, framed around their problem]</div>
      </div>
    </details>

    <!-- 8. Discovery Questions (pain- and situation-led, NOT sales-process) -->
    <details class="bp-section" open id="discovery">
      <summary>Discovery Questions</summary>
      <div class="question-item">
        <div>[Question that uncovers business pain / use case / who's involved]</div>
        <div class="reveals">[what a good answer tells you]</div>
      </div>
    </details>

    <!-- 9. Objections & Competitors -->
    <details class="bp-section" open id="objections-competitors">
      <summary>Objections &amp; Competitors</summary>
      <h3>Likely objections</h3>
      <div class="objection-item">
        <div class="obj">[objection in their words]</div>
        <div class="response">[grounded response framed around their outcome]</div>
      </div>
      <h3>Competitors &amp; alternatives</h3>
      <div class="competitor-row">
        <div><span class="col-label">Alternative</span><br>[competitor / status quo / build]</div>
        <div><span class="col-label">Where they win</span><br>[…]</div>
        <div><span class="col-label">Where we win</span><br>[the differentiator that matters here]</div>
      </div>
      <div class="watch-out"><strong>Watch-out:</strong> [landmine to avoid in this conversation]</div>
    </details>

    <!-- 10. The Line -->
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
