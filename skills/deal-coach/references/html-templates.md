# Coaching HTML Templates

This reference provides HTML section templates for both the Coaching Microsite and Coaching Deck output modes. Templates use CSS variables from the style preset system and bracket placeholders for dynamic content.

All templates follow the same conventions:
- Self-contained HTML with inline `<style>` blocks
- CSS variable theming via `:root` (populated from style presets)
- `<details class="section">` for collapsible sections (microsite) — all collapsed by default
- `scroll-snap` slide architecture (deck)
- `clamp()` for all font sizes and spacing
- Print-friendly via `@media print`
- Responsive via `@media (max-width: 768px)`
- Reduced motion via `@media (prefers-reduced-motion: reduce)`

## Design Principles (Microsite)

The microsite is organized around the **three coaching outputs** (Buyer Mindset / Value Propositions / Talking Points), NOT around methodology framework names. The structure is:

```
Header + Deal Brief    — NOT collapsible. Full-width gradient hero.
Priority Actions       — Collapsible <details> with +/− toggle. Exactly 3 actions.
Deal Activity          — Collapsible <details> with +/− toggle. Compact vertical timeline of deal events.
Journey Map            — Collapsible <details> with +/− toggle. 3-phase coaching journey
                         (Resonate → Elevate → Compel) showing where the deal is and why.
Section 01: Stage Assessment     — Collapsible. Evidence + confidence calibration.
Section 02: Buyer Mindset        — Collapsible. Psychology assessment, signals, adaptation guidance.
Section 03: Value Propositions   — Collapsible. Stage-appropriate props with evidence inline.
Section 04: Talking Points       — Collapsible. Talk tracks with strategic point + quote + evidence.
Section 05: Objection Handling   — Collapsible. Objections grounded in buyer's decision frame.
Section 06: Next Stage Preview   — Collapsible. Transition checklist + next agent.
[Optional] Section 07: Deal Gaps (MEDDPICC) — Collapsible. Coverage assessment (if requested).
The Play                         — NOT collapsible. Full-width gradient footer.
```

**All sections collapsed by default.** The reader clicks to expand what they need. Priority Actions, Deal Activity, and Journey Map use `<details>` with the same +/− toggle as the numbered sections.

**No duplicate content.** Each piece of information appears exactly once. Evidence and objections are integrated into What to Say, not in standalone sections. Discovery questions are organized by job-to-be-done in What to Do, not in a standalone section.

**Tone and posture:**
- This is a **selling tool**. Orient language around advancing the deal. Do not soften with partnership framing when the context is clearly a sales motion.
- Use **"perspective-shifting question"** framing, not "trap question." Tone should be collaborative and consultative, never adversarial.
- **Objections must be grounded in the buyer's actual decision** — identify what the buyer is deciding (build vs. buy, do-nothing vs. act, this vendor vs. that) and tailor responses to that frame.
- **Evidence includes usage context** — each proof point should note whether to deploy now, save for a later stage, or if it's already been shared.

---

## Part 1: Coaching Microsite Templates

### Base HTML Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Deal Name] — Deal Coaching: [Stage Name]</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[Font Query]" rel="stylesheet">
  <style>
    :root {
      /* Populated from style preset or brand extraction */
    }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      font-family: var(--font-body);
      background: var(--bg);
      color: var(--text-primary);
      line-height: 1.6;
    }

    /* Container */
    .coaching-container {
      max-width: 900px;
      margin: 0 auto;
      padding: clamp(1rem, 3vw, 2rem);
    }

    /* Navigation */
    .bp-nav {
      position: fixed;
      right: clamp(0.75rem, 2vw, 1.5rem);
      top: 50%;
      transform: translateY(-50%);
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      z-index: 100;
    }
    .bp-nav a {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--text-muted);
      opacity: 0.4;
      transition: all 0.3s var(--ease);
      display: block;
    }
    .bp-nav a.active {
      opacity: 1;
      background: var(--brand-primary);
      transform: scale(1.3);
    }

    /* Collapsible Sections */
    .section {
      margin-bottom: clamp(1.5rem, 3vw, 2.5rem);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      background: var(--bg-elevated);
      overflow: hidden;
    }
    .section summary {
      padding: clamp(1rem, 2vw, 1.5rem);
      cursor: pointer;
      list-style: none;
      display: flex;
      align-items: center;
      gap: 1rem;
    }
    .section summary::-webkit-details-marker { display: none; }
    .section summary::after {
      content: '';
      width: 0; height: 0;
      border-left: 5px solid transparent;
      border-right: 5px solid transparent;
      border-top: 6px solid var(--text-secondary);
      transition: transform 0.3s var(--ease);
      margin-left: auto;
    }
    .section[open] summary::after { transform: rotate(180deg); }
    .section-number {
      font-size: clamp(0.65rem, 1vw, 0.75rem);
      color: var(--brand-primary);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      font-weight: 700;
    }
    .section-title {
      font-family: var(--font-display);
      font-size: clamp(1.1rem, 2vw, 1.4rem);
      color: var(--text-primary);
      font-weight: 800;
    }
    .section-body {
      padding: 0 clamp(1rem, 2vw, 1.5rem) clamp(1rem, 2vw, 1.5rem);
    }
    .section-subtitle {
      color: var(--text-secondary);
      font-size: clamp(0.85rem, 1.2vw, 0.95rem);
      margin-bottom: 1.5rem;
    }

    /* Cards */
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: clamp(0.75rem, 1.5vw, 1.25rem);
      transition: all 0.2s var(--ease);
    }
    .card:hover { background: var(--bg-card-hover); border-color: var(--border-strong); }

    /* Grids */
    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: clamp(0.75rem, 1.5vw, 1.25rem); }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: clamp(0.75rem, 1.5vw, 1.25rem); }
    .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: clamp(0.75rem, 1.5vw, 1rem); }

    /* Badges */
    .badge {
      display: inline-flex;
      align-items: center;
      padding: 0.2em 0.6em;
      border-radius: var(--radius-pill);
      font-size: clamp(0.65rem, 1vw, 0.75rem);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .badge-primary { background: var(--brand-100); color: var(--brand-primary); }
    .badge-accent { background: rgba(255,85,27,0.12); color: var(--brand-secondary); }
    .badge-teal { background: rgba(26,147,168,0.12); color: var(--brand-tertiary); }
    .badge-success { background: rgba(16,185,129,0.12); color: var(--success); }
    .badge-warning { background: rgba(245,158,11,0.12); color: var(--warning); }
    .badge-error { background: rgba(239,68,68,0.12); color: var(--error); }

    /* Labels (reusable uppercase small label) */
    .talk-track-label {
      font-size: clamp(0.6rem, 0.9vw, 0.7rem);
      color: var(--brand-primary);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 0.5rem;
      font-weight: 700;
    }

    /* Coaching Notes */
    .coaching-note {
      background: var(--brand-100);
      border: 1px solid var(--brand-200);
      border-radius: var(--radius);
      padding: clamp(0.75rem, 1.5vw, 1rem);
      margin-top: 1rem;
    }
    .coaching-note-label {
      font-size: clamp(0.6rem, 0.9vw, 0.7rem);
      color: var(--brand-primary);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 0.25rem;
      font-weight: 700;
    }

    /* Hero Header (full-width gradient) */
    .hero-gradient {
      background: linear-gradient(135deg, var(--brand-primary) 0%, var(--bg) 60%, var(--brand-tertiary, var(--brand-primary)) 100%);
      border-radius: var(--radius-lg);
      padding: clamp(2rem, 5vw, 3rem) clamp(1.5rem, 3vw, 2.5rem);
      margin-bottom: clamp(1.5rem, 3vw, 2.5rem);
      color: #fff;
    }

    /* Deal Stats Grid (inside hero) */
    .stat-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
      gap: clamp(0.5rem, 1vw, 0.75rem);
    }
    .stat-card { text-align: center; padding: clamp(0.5rem, 1vw, 0.75rem); }
    .stat-value {
      font-family: var(--font-display);
      font-size: clamp(1.3rem, 2.5vw, 1.8rem);
      font-weight: 900;
      color: #fff;
    }
    .stat-label {
      font-size: clamp(0.65rem, 0.9vw, 0.75rem);
      color: rgba(255,255,255,0.6);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    /* Collapsible Top Sections (Priority Actions, Deal Activity, Journey Map) */
    .priority-card summary,
    .deal-timeline summary,
    .journey-map summary {
      cursor: pointer;
      list-style: none;
      user-select: none;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .priority-card summary::-webkit-details-marker,
    .deal-timeline summary::-webkit-details-marker,
    .journey-map summary::-webkit-details-marker { display: none; }
    .priority-card summary::after,
    .deal-timeline summary::after,
    .journey-map summary::after {
      content: '+';
      font-size: 1.3rem;
      font-weight: 300;
      color: var(--text-muted);
      transition: transform 0.3s var(--ease);
    }
    .priority-card[open] summary::after,
    .deal-timeline[open] summary::after,
    .journey-map[open] summary::after { content: '\2212'; }

    /* Deal Timeline */
    .deal-timeline {
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: clamp(1rem, 2vw, 1.5rem);
      margin-bottom: clamp(1.5rem, 3vw, 2.5rem);
    }
    .timeline-entry {
      display: grid;
      grid-template-columns: 3.5rem 1.5rem 1fr;
      gap: 0.5rem;
      align-items: start;
      padding-bottom: 1rem;
      position: relative;
    }
    .timeline-entry:last-child { padding-bottom: 0; }
    .timeline-date {
      font-family: var(--font-mono);
      font-size: clamp(0.65rem, 0.85vw, 0.75rem);
      color: var(--text-muted);
      font-weight: 500;
      text-align: right;
    }
    .timeline-dot {
      width: 0.5rem; height: 0.5rem; border-radius: 50%;
      background: var(--text-muted);
      margin-top: 0.35rem; justify-self: center;
      position: relative; z-index: 1;
    }
    .timeline-dot.dot-highlight {
      background: var(--brand-primary);
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
    }
    .timeline-dot.dot-next {
      background: transparent;
      border: 2px solid var(--text-muted);
    }
    .timeline-entry:not(:last-child) .timeline-dot::after {
      content: ''; position: absolute; top: 100%; left: 50%;
      transform: translateX(-50%); width: 1px;
      height: calc(1rem + 0.5rem); background: var(--border);
    }
    .timeline-event { font-weight: 700; font-size: clamp(0.8rem, 1.1vw, 0.9rem); }
    .timeline-detail {
      color: var(--text-secondary); font-size: clamp(0.72rem, 0.95vw, 0.82rem);
      line-height: 1.55; margin-top: 0.15rem;
    }
    .timeline-next .timeline-event,
    .timeline-next .timeline-detail { color: var(--text-muted); }

    /* Journey Map */
    .journey-map {
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: clamp(1.25rem, 2.5vw, 2rem);
      margin-bottom: clamp(1.5rem, 3vw, 2.5rem);
    }
    .journey-phase { display: flex; gap: clamp(0.75rem, 1.5vw, 1.25rem); }
    .phase-indicator { display: flex; flex-direction: column; align-items: center; flex-shrink: 0; width: 2rem; }
    .phase-dot {
      width: 1.5rem; height: 1.5rem; border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-size: 0.7rem; font-weight: 900; flex-shrink: 0; position: relative; z-index: 1;
    }
    .dot-complete { background: var(--success); color: var(--bg); }
    .dot-active { background: var(--brand-primary); color: #fff; box-shadow: 0 0 0 4px rgba(59,130,246,0.25); }
    .dot-future { background: transparent; border: 2px solid var(--text-muted); }
    .phase-connector { width: 2px; flex: 1; min-height: 1rem; }
    .connector-complete { background: var(--success); }
    .connector-future { background: var(--text-muted); opacity: 0.3; }
    .phase-content { padding-bottom: clamp(1.25rem, 2.5vw, 1.75rem); flex: 1; }
    .phase-deal-context {
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: var(--radius); padding: clamp(0.6rem, 1.2vw, 0.85rem);
    }
    .phase-complete .phase-deal-context { border-left: 3px solid var(--success); }
    .phase-active .phase-deal-context { border-left: 3px solid var(--brand-primary); }
    .phase-future .phase-deal-context { border-left: 3px solid var(--text-muted); }

    /* Priority Actions Card */
    .priority-card {
      background: var(--bg-elevated);
      border: 2px solid var(--brand-primary);
      border-radius: var(--radius-lg);
      padding: clamp(1rem, 2vw, 1.5rem);
      margin-bottom: clamp(1.5rem, 3vw, 2.5rem);
    }
    .priority-item {
      display: flex;
      gap: 1rem;
      align-items: flex-start;
      padding: 0.75rem 0;
      border-bottom: 1px solid var(--border);
    }
    .priority-item:last-child { border-bottom: none; }
    .priority-num {
      background: var(--brand-primary);
      color: #fff;
      width: 28px;
      height: 28px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 0.8rem;
      flex-shrink: 0;
    }

    /* Messaging Blocks (What to Say) — strategic point + quote + evidence */
    .msg-block { margin-bottom: 1.5rem; }
    .msg-point {
      font-weight: 700;
      font-size: clamp(0.9rem, 1.3vw, 1rem);
      margin-bottom: 0.5rem;
      color: var(--text-primary);
    }
    .msg-quote {
      background: var(--bg-card);
      border-left: 3px solid var(--brand-primary);
      border-radius: 0 var(--radius) var(--radius) 0;
      padding: clamp(0.6rem, 1.2vw, 1rem);
      font-style: italic;
      color: var(--text-secondary);
      font-size: clamp(0.8rem, 1.1vw, 0.9rem);
      line-height: 1.6;
    }
    .msg-evidence {
      margin-top: 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: clamp(0.75rem, 1vw, 0.8rem);
    }
    .msg-evidence-metric {
      font-weight: 900;
      color: var(--brand-primary);
      font-size: clamp(0.9rem, 1.3vw, 1rem);
    }

    /* Objection Blocks (inline in What to Say) */
    .objection-block {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: clamp(0.75rem, 1.5vw, 1.25rem);
      margin-bottom: 1rem;
    }
    .objection-trigger {
      font-weight: 700;
      color: var(--error);
      font-size: clamp(0.85rem, 1.2vw, 0.95rem);
      margin-bottom: 0.5rem;
    }
    .objection-response {
      font-size: clamp(0.8rem, 1.1vw, 0.9rem);
      color: var(--text-secondary);
      line-height: 1.6;
    }

    /* Job Blocks (What to Do) — coaching actions with discovery questions */
    .job-block {
      margin-bottom: 1.5rem;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow: hidden;
    }
    .job-header {
      background: var(--bg-card);
      padding: clamp(0.75rem, 1.5vw, 1rem);
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border);
    }
    .job-title {
      font-weight: 800;
      font-size: clamp(0.9rem, 1.3vw, 1rem);
    }
    .job-body {
      padding: clamp(0.75rem, 1.5vw, 1rem);
    }
    .job-question {
      display: flex;
      gap: 0.75rem;
      align-items: flex-start;
      padding: 0.5rem 0;
      border-bottom: 1px solid var(--border);
    }
    .job-question:last-child { border-bottom: none; }

    /* Deal Gap Grid (MEDDPICC when included, or stage-gap grid) */
    .meddpicc-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: clamp(0.5rem, 1vw, 0.75rem);
    }
    .meddpicc-item {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: clamp(0.5rem, 1vw, 0.75rem);
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    .meddpicc-letter {
      font-size: clamp(1rem, 1.5vw, 1.2rem);
      font-weight: 900;
      color: var(--brand-primary);
      min-width: 1.5rem;
    }
    .meddpicc-status {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      flex-shrink: 0;
    }
    .meddpicc-status.covered { background: var(--success); }
    .meddpicc-status.partial { background: var(--warning); }
    .meddpicc-status.gap { background: var(--error); }

    /* The Play (full-width gradient footer) */
    .the-play {
      text-align: center;
      padding: clamp(2rem, 4vw, 3rem);
      margin-top: 2rem;
      background: linear-gradient(135deg, var(--brand-primary) 0%, var(--bg) 100%);
      border-radius: var(--radius-lg);
    }
    .the-play-label {
      font-size: clamp(0.7rem, 1vw, 0.8rem);
      color: var(--brand-secondary, var(--brand-primary));
      text-transform: uppercase;
      letter-spacing: 0.15em;
      margin-bottom: 1rem;
      font-weight: 700;
    }
    .the-play-text {
      font-family: var(--font-display);
      font-size: clamp(1.2rem, 2.2vw, 1.6rem);
      color: #ffffff;
      line-height: 1.4;
      font-weight: 800;
    }
    .the-play-action {
      color: rgba(255,255,255,0.7);
      font-size: clamp(0.85rem, 1.2vw, 0.95rem);
      margin-top: 1rem;
      padding-top: 1rem;
      border-top: 1px solid rgba(255,255,255,0.15);
    }

    /* Responsive */
    @media (max-width: 768px) {
      .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
      .bp-nav { display: none; }
      .meddpicc-grid { grid-template-columns: 1fr; }
      .stat-grid { grid-template-columns: repeat(2, 1fr); }
    }

    /* Print */
    @media print {
      .bp-nav { display: none; }
      .section { break-inside: avoid; }
      .card, .msg-block, .objection-block, .job-block { break-inside: avoid; }
      .hero-gradient, .the-play, .priority-card { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    }

    /* Reduced Motion */
    @media (prefers-reduced-motion: reduce) {
      * { transition: none !important; animation: none !important; }
    }
  </style>
</head>
<body>
  <nav class="bp-nav" id="bp-nav"></nav>

  <div class="coaching-container">
    <!-- Header + Deal Brief (NOT a section) -->
    <!-- Priority Actions (NOT a section) -->
    <!-- Sections 01-06 (collapsible) -->
    <!-- The Play (NOT a section) -->
  </div>

  <script>
    const sections = document.querySelectorAll('.section, .the-play');
    const nav = document.getElementById('bp-nav');
    sections.forEach((section) => {
      const dot = document.createElement('a');
      dot.href = '#' + section.id;
      dot.title = section.querySelector('.section-title')?.textContent || 'The Play';
      nav.appendChild(dot);
    });

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          document.querySelectorAll('.bp-nav a').forEach(a => a.classList.remove('active'));
          const activeLink = document.querySelector(`.bp-nav a[href="#${id}"]`);
          if (activeLink) activeLink.classList.add('active');
        }
      });
    }, { threshold: 0.3 });

    sections.forEach(section => observer.observe(section));
  </script>
</body>
</html>
```

---

### Header + Deal Brief

The header is NOT a collapsible section. It's a full-width gradient hero with company info, stage explanations, and deal stats.

```html
<header class="hero-gradient">
  <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
    <div>
      <h1 style="font-family: var(--font-display); font-size: clamp(1.8rem, 4vw, 2.5rem); font-weight: 900; margin-bottom: 0.25rem;">[Company Name]</h1>
      <p style="color: rgba(255,255,255,0.6); font-size: clamp(0.8rem, 1.1vw, 0.9rem);">[Employee count] &bull; [Industry] &bull; [Location]</p>
    </div>
    <div style="text-align: right;">
      <p style="color: rgba(255,255,255,0.5); font-size: clamp(0.75rem, 1vw, 0.8rem);">Coaching Brief</p>
      <p style="color: rgba(255,255,255,0.7); font-size: clamp(0.85rem, 1.2vw, 0.95rem); font-weight: 700;">[Date]</p>
    </div>
  </div>

  <!-- Stage badge + deal-specific subtitle -->
  <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.12);">
    <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.75rem;">
      <span class="badge" style="background: rgba(255,255,255,0.15); color: #fff;">Coaching Stage: [Stage Name]</span>
      <span class="badge" style="background: rgba(16,185,129,0.2); color: #7ddde8;">[High|Medium|Low] Confidence</span>
    </div>
    <p style="color: rgba(255,255,255,0.7); font-size: clamp(0.9rem, 1.3vw, 1rem);">
      [Deal-specific subtitle — e.g., "Harvey knows the problem. Build the case for why Octave — and why now." NOT a generic stage description. Ground it in the deal.]
    </p>
  </div>
  <!-- NOTE: Do NOT include a separate "Evaluate Phase" or buyer journey badge here.
       The Journey Map section explains the full Resonate → Elevate → Compel framework
       and the buyer journey mapping. Keep the header clean. -->

  <!-- Deal stats grid -->
  <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.12);">
    <div class="stat-grid">
      <!-- Include 4-6 stats from deal data. Common stats: -->
      <div class="stat-card">
        <p class="stat-value">[N]</p>
        <p class="stat-label">Days Active</p>
      </div>
      <div class="stat-card">
        <p class="stat-value">[N]</p>
        <p class="stat-label">Calls</p>
      </div>
      <div class="stat-card">
        <p class="stat-value">[N]</p>
        <p class="stat-label">Meetings</p>
      </div>
      <div class="stat-card">
        <p class="stat-value" style="color: #34d399;">[N]%</p>
        <p class="stat-label">Positive Calls</p>
      </div>
      <div class="stat-card">
        <p class="stat-value" style="font-size: clamp(0.95rem, 1.8vw, 1.2rem);">[Date]</p>
        <p class="stat-label">Last Contact</p>
      </div>
      <div class="stat-card">
        <p class="stat-value" style="font-size: clamp(0.95rem, 1.8vw, 1.2rem);">[Date]</p>
        <p class="stat-label">First Meeting</p>
      </div>
      <!-- If CRM data: add Deal Amount, Close Date, Pipeline Stage, Pipeline Entry Date -->

    <!-- Key contacts (if known from CRM activities or events) -->
    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.12);">
      <p style="color: rgba(255,255,255,0.5); font-size: clamp(0.7rem, 0.9vw, 0.75rem); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem; font-weight: 700;">Key Contacts</p>
      <div style="display: flex; flex-wrap: wrap; gap: 0.75rem;">
        <!-- Repeat for each known contact (from find_crm_activities, list_events, or enrichment) -->
        <span style="background: rgba(255,255,255,0.1); padding: 0.25rem 0.75rem; border-radius: var(--radius-pill); font-size: clamp(0.75rem, 1vw, 0.85rem); color: rgba(255,255,255,0.8);">[Name — Role]</span>
        <!-- End repeat -->
      </div>
    </div>
    </div>
  </div>
</header>
```

---

### Priority Actions

Collapsible `<details>` with +/− toggle. Bordered card with exactly 3 quick-hit actions before the next meeting. Place between header and Deal Activity.

```html
<details class="priority-card" id="section-priorities">
  <summary>
    <p style="font-size: clamp(0.65rem, 0.9vw, 0.75rem); color: var(--brand-primary); text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700;">Priority Actions — Before Your Next Meeting</p>
  </summary>
  <!-- Exactly 3 priority actions -->
  <div class="priority-item">
    <span class="priority-num">1</span>
    <div>
      <p style="font-weight: 700; font-size: clamp(0.9rem, 1.2vw, 0.95rem);">[Action title — imperative, specific]</p>
      <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.85rem);">[2-3 sentences: why this matters now, what to do specifically, what happens if you don't]</p>
    </div>
  </div>
  <div class="priority-item">
    <span class="priority-num">2</span>
    <div>
      <p style="font-weight: 700; font-size: clamp(0.9rem, 1.2vw, 0.95rem);">[Action title]</p>
      <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.85rem);">[Context and specifics]</p>
    </div>
  </div>
  <div class="priority-item">
    <span class="priority-num">3</span>
    <div>
      <p style="font-weight: 700; font-size: clamp(0.9rem, 1.2vw, 0.95rem);">[Action title]</p>
      <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.85rem);">[Context and specifics]</p>
    </div>
  </div>
</details>
```

---

### Deal Activity

Collapsible `<details>` with +/− toggle. A compact vertical timeline of key deal events with dates. Place between Priority Actions and Journey Map. Include all known touchpoints (calls, demos, meetings) plus a "Next" entry for upcoming actions.

```html
<details class="deal-timeline">
  <summary>
    <h3 style="font-size: clamp(0.9rem, 1.3vw, 1.05rem); font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; color: var(--brand-primary);">Deal Activity</h3>
  </summary>

  <!-- Repeat for each deal event, chronologically -->
  <div class="timeline-entry">
    <span class="timeline-date">[Date]</span>
    <span class="timeline-dot [dot-highlight if key event]"></span>
    <div>
      <p class="timeline-event">[Event name — e.g., "Discovery call — scored 7.7 / 10"]</p>
      <p class="timeline-detail">[Key details — what happened, what was discussed, what was requested. 1-2 sentences.]</p>
    </div>
  </div>
  <!-- End repeat -->

  <!-- Final entry: What's next -->
  <div class="timeline-entry timeline-next">
    <span class="timeline-date">Next</span>
    <span class="timeline-dot dot-next"></span>
    <div>
      <p class="timeline-event">[Next planned action]</p>
      <p class="timeline-detail">[What needs to happen and what stage it's targeting.]</p>
    </div>
  </div>
</details>
```

---

### Journey Map

Collapsible `<details>` with +/− toggle. A 3-phase coaching journey showing where the deal sits (Resonate → Elevate → Compel). Each phase has:
1. **Generic explanation** — what this phase IS and what it focuses on (for sellers unfamiliar with the methodology)
2. **Deal-specific context** — WHY this deal is in / past / headed toward this phase

The naming convention: stages are named for what the **seller** does (Resonate, Elevate, Compel) while the buyer moves through their own journey (exploring → evaluating → justifying). Make this explicit in the intro text.

```html
<details class="journey-map">
  <summary>
    <h3 style="font-size: clamp(0.9rem, 1.3vw, 1.05rem); font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; color: var(--brand-primary);">Your Deal Coaching Journey</h3>
  </summary>

  <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem); line-height: 1.65; margin-bottom: 1.5rem;">
    Deal coaching follows three stages that mirror how buyers actually make decisions.
    Each stage is named for what the <em>seller</em> needs to do — <strong>Resonate</strong>
    with the problem, <strong>Elevate</strong> the urgency, <strong>Compel</strong> the
    decision — while the buyer moves through their own journey from exploring to evaluating
    to justifying. Here's where [Company] sits and why.
  </p>

  <!-- Phase 1: Resonate -->
  <div class="journey-phase phase-[complete|active|future]">
    <div class="phase-indicator">
      <div class="phase-dot [dot-complete ✓ | dot-active | dot-future]"></div>
      <div class="phase-connector [connector-complete | connector-future]"></div>
    </div>
    <div class="phase-content">
      <p style="font-family: var(--font-mono); font-size: clamp(0.6rem, 0.8vw, 0.7rem); text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; color: [var(--success)|var(--brand-primary)|var(--text-muted)];">Phase 1 — [Complete | You Are Here | What's Next]</p>
      <h4 style="font-family: var(--font-display); font-size: clamp(1.1rem, 1.8vw, 1.35rem); font-weight: 900;">Resonate</h4>
      <p style="font-weight: 600; color: var(--text-secondary); margin-bottom: 0.5rem;">Diagnose the real problem. Build shared understanding of the pain across the buying org.</p>
      <p style="color: var(--text-muted); font-size: clamp(0.78rem, 1.05vw, 0.88rem); line-height: 1.65; margin-bottom: 0.75rem;">
        [Generic explanation of Resonate: discovery, go wide/deep/high, getting the buyer to articulate the problem, multi-stakeholder alignment.]
      </p>
      <div class="phase-deal-context">
        <p style="font-size: clamp(0.65rem, 0.85vw, 0.72rem); text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700; color: [var(--success)|var(--brand-primary)|var(--text-muted)]; margin-bottom: 0.3rem;">
          [Why [Company] has moved past Resonate | Why [Company] is in Resonate | How [Company] gets to Resonate]
        </p>
        <p style="font-size: clamp(0.75rem, 1vw, 0.85rem); color: var(--text-secondary); line-height: 1.6;">
          [Deal-specific evidence for why this phase is complete/active/future]
        </p>
      </div>
    </div>
  </div>

  <!-- Phase 2: Elevate — same structure as Phase 1 -->
  <!-- Phase 3: Compel — same structure, no connector after final dot -->
</details>
```

---

### Section 01: Stage Assessment

Includes evidence grid AND a "why this stage and not another" calibration note.

```html
<details class="section" id="section-stage-assessment">
  <summary>
    <div>
      <p class="section-number">Section 01</p>
      <h2 class="section-title">Stage Assessment</h2>
    </div>
  </summary>
  <div class="section-body">
    <p class="section-subtitle">Where this deal sits in the buying journey, why we landed on this stage, and what would make us reconsider.</p>

    <!-- Stage summary card -->
    <div class="card" style="margin-bottom: 1.5rem; border-left: 3px solid var(--brand-primary);">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
          <span class="badge badge-primary" style="font-size: clamp(0.8rem, 1.2vw, 0.9rem);">[Stage Name]</span>
          <span style="font-family: var(--font-display); font-size: clamp(1.1rem, 1.8vw, 1.3rem); font-weight: 800;">[Stage Name — e.g., Elevate]</span>
        </div>
        <span class="badge [badge-success|badge-warning|badge-error]">[Confidence] Confidence</span>
      </div>
      <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem);">[2-3 sentence summary of why this stage, grounded in deal evidence]</p>
    </div>

    <!-- Evidence grid (4 cards) -->
    <h3 style="font-size: clamp(0.95rem, 1.3vw, 1.05rem); margin-bottom: 1rem; font-weight: 800;">Evidence</h3>
    <div class="grid-2">
      <div class="card">
        <p class="talk-track-label">CRM Stage (40%)</p>
        <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem);">[CRM stage → Deal Coaching mapping, or "No CRM record — data gap, not deal gap" with explanation]</p>
      </div>
      <div class="card">
        <p class="talk-track-label">Conversation Signals (30%)</p>
        <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem);">[Key findings and what they indicate about stage]</p>
      </div>
      <div class="card">
        <p class="talk-track-label">Deal Activities (20%)</p>
        <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem);">[Activity progression — e.g., "Demo → Deep-dive → Workshop planning"]</p>
      </div>
      <div class="card">
        <p class="talk-track-label">Time in Stage (10%)</p>
        <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem);">[Days active, cadence assessment, stall or no stall]</p>
      </div>
    </div>

    <!-- Why this stage and not another — CRITICAL differentiator from old template -->
    <div class="coaching-note" style="margin-top: 1.5rem;">
      <p class="coaching-note-label">Why [Stage Name] and Not Another Stage</p>
      <div style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem);">
        <p style="margin-bottom: 0.5rem;"><strong>Not [Previous Stage — e.g., Resonate]</strong> because [specific evidence that the previous stage's work is done]</p>
        <p style="margin-bottom: 0.5rem;"><strong>Not [Next Stage — e.g., Compel]</strong> because [specific signals that would need to appear for the next stage, and why they haven't yet]</p>
        <p><strong>What would change the assessment:</strong> [Concrete signals to watch for that would shift the stage up or down]</p>
      </div>
    </div>
  </div>
</details>
```

---

### Section 02: Deal Gaps

Optional MEDDPICC overlay or stage-specific gap analysis. Placed early so the gaps inform Buyer Mindset, Value Propositions, and Talking Points sections.

```html
<details class="section" id="section-deal-gaps">
  <summary>
    <div>
      <p class="section-number">Section 02</p>
      <h2 class="section-title">Deal Gaps</h2>
    </div>
  </summary>
  <div class="section-body">
    <p class="section-subtitle">What's covered, what's partial, and what's missing. These gaps drive the discovery questions and actions in the sections that follow.</p>

    <div class="meddpicc-grid">
      <!-- Repeat for each deal gap element. Use MEDDPICC (8 elements) if user opted in, otherwise use stage-specific gaps (3-6 elements based on Resonate/Elevate/Compel criteria) -->
      <div class="meddpicc-item">
        <span class="meddpicc-letter">[ID]</span>
        <span class="meddpicc-status [covered|partial|gap]"></span>
        <div>
          <p style="font-weight: 700; font-size: clamp(0.8rem, 1.1vw, 0.9rem);">[Element Name]</p>
          <p style="color: var(--text-muted); font-size: clamp(0.7rem, 0.9vw, 0.8rem);">[Brief status — e.g., "Strong alignment" or "Not identified"]</p>
        </div>
      </div>
      <!-- End repeat -->
    </div>

    <!-- Gap summary -->
    <div style="margin-top: 1.5rem; padding: 1rem; background: var(--bg-card); border-radius: var(--radius); border: 1px solid var(--border);">
      <p style="font-weight: 700; margin-bottom: 0.5rem; font-size: clamp(0.85rem, 1.2vw, 0.95rem);">Summary: [N] covered, [N] partial, [N] gaps</p>
      <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem);">[2-3 sentences: what the biggest risks are, how gaps connect to each other, and note that What to Do maps actions to these gaps]</p>
    </div>
  </div>
</details>
```

---

### Section 03: What to Know

Buyer situation, your advantages, your vulnerability, and call signals. Coaching methodology informs the content but DON'T appear as headers. No methodology framework names as card titles — use plain language.

```html
<details class="section" id="section-what-to-know">
  <summary>
    <div>
      <p class="section-number">Section 03</p>
      <h2 class="section-title">What to Know</h2>
    </div>
  </summary>
  <div class="section-body">
    <p class="section-subtitle">Key intelligence about this deal, the buyer's situation, and where your advantage lies.</p>

    <!-- Buyer situation -->
    <div class="card" style="margin-bottom: 1rem;">
      <p class="talk-track-label">The Buyer's World</p>
      <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem);">[Company description, core business, current approach, key challenge. From enrichment + findings.]</p>
    </div>

    <!-- Your advantages (informed by differentiated value analysis / value framing, but not labeled as such) -->
    <div class="card" style="margin-bottom: 1rem; border-left: 3px solid var(--brand-secondary);">
      <p class="talk-track-label">Where Your Advantage Lies</p>
      <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem); margin-bottom: 0.75rem;">[Framing sentence — what's unique AND important AND competitors can't match]</p>
      <ol style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem); padding-left: 1.25rem;">
        <li style="margin-bottom: 0.5rem;"><strong>[Differentiator 1 name.]</strong> [What it is, what it does for the buyer, why it matters — translate across Product → Buyer → Executive voices]</li>
        <li style="margin-bottom: 0.5rem;"><strong>[Differentiator 2 name.]</strong> [Same pattern]</li>
        <li><strong>[Differentiator 3 name.]</strong> [Same pattern]</li>
      </ol>
    </div>

    <!-- Table stakes + vulnerability side by side -->
    <div class="grid-2">
      <div class="card">
        <p class="talk-track-label">Table Stakes (Don't Compete Here)</p>
        <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem);">[Capabilities that are parity — every competitor has these. Don't let the conversation settle here.]</p>
      </div>
      <div class="card">
        <p class="talk-track-label">Your Vulnerability (Own It)</p>
        <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem);">[Where you're weak or missing. How to position it — complement, not compete.]</p>
      </div>
    </div>

    <!-- Call signals (from events/findings) -->
    <div class="coaching-note" style="margin-top: 1rem;">
      <p class="coaching-note-label">Signals From the Calls</p>
      <!-- Repeat for each notable call/meeting -->
      <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem); margin-bottom: 0.5rem;"><strong>[Date] ([Event Name]):</strong> [Key takeaway — what was discussed, what the buyer signaled, what changed]</p>
      <!-- End repeat -->
    </div>
  </div>
</details>
```

---

### Section 04: What to Say

Strategic messaging points with the two-layer pattern: **strategic point** (bold, what you're trying to achieve) + **sample quote** (italic, one way to express it) + **evidence inline** (proof point metrics) + **objections inline** at the end.

```html
<details class="section" id="section-what-to-say">
  <summary>
    <div>
      <p class="section-number">Section 04</p>
      <h2 class="section-title">What to Say</h2>
    </div>
  </summary>
  <div class="section-body">
    <p class="section-subtitle">Stage-appropriate talk tracks grounded in deal context. Each has a strategic intent, guidance on when to use it, and sample language you can adapt.</p>

    <!-- Repeat for each messaging point (4-6 points).
         IMPORTANT: Do NOT use methodology framework names as headers (e.g., "The Shift",
         "The Stakes", "The Possibility"). The framework informs the content structure
         but headers should be practical and deal-specific. -->
    <div class="msg-block">
      <p class="msg-point">[N]. [Practical topic — what the talk track is about, in deal language]</p>
      <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem); margin-bottom: 0.5rem;">[When to use this + 1 sentence of context — e.g., "Use early in the conversation to set the stage." or "Use to build urgency after the scale problem lands."]</p>
      <div class="msg-quote">"[Sample language — shorter than old talk tracks. One way to express the point, grounded in playbook messaging.]"</div>
      <!-- Evidence inline (0-2 proof points per message). Include usage note: deploy now / save for later / already shared -->
      <div class="msg-evidence">
        <span class="msg-evidence-metric">[Metric — e.g., 29%]</span>
        <span style="color: var(--text-muted);">[Description — e.g., win rate improvement. (Customer type)] [Usage: Deploy now / Save for Compel / Already shared on Feb 20]</span>
      </div>
    </div>
    <!-- End repeat -->

    <!-- Divider before objections -->
    <div style="height: 1px; background: var(--border); margin: 2rem 0;"></div>

    <!-- Objections inline (NOT a separate section). Ground each in the buyer's ACTUAL decision, not generic competitive framing. -->
    <h3 style="font-size: clamp(0.95rem, 1.3vw, 1.05rem); margin-bottom: 1rem; font-weight: 800;">When They Push Back</h3>

    <!-- Repeat for each objection (3-5 objections). Tailor to the specific decision this buyer is making. -->
    <div class="objection-block">
      <p class="objection-trigger">"[Buyer objection — in their words, specific to this deal's context]"</p>
      <p class="objection-response"><strong>The point:</strong> [How to respond — grounded in the buyer's actual decision frame (build vs. buy, do-nothing vs. act, etc.). Strategic framing first, then specific language. Reference deal context. 2-4 sentences.]</p>
    </div>
    <!-- End repeat -->
  </div>
</details>
```

---

### Section 05: What to Do

Jobs to accomplish, each mapped to a deal gap from Section 02. Each job contains discovery questions specific to that job.

```html
<details class="section" id="section-what-to-do">
  <summary>
    <div>
      <p class="section-number">Section 05</p>
      <h2 class="section-title">What to Do</h2>
    </div>
  </summary>
  <div class="section-body">
    <p class="section-subtitle">Jobs to accomplish to advance this deal. Each job maps to a deal gap from Section 02, with specific discovery questions to get there.</p>

    <!-- Repeat for each job (3-5 jobs) -->
    <div class="job-block">
      <div class="job-header">
        <p class="job-title">[Job Name — e.g., "Shape Decision Criteria"]</p>
        <span class="badge [badge-warning|badge-error|badge-primary]">[Gap Element] &mdash; [Status]</span>
      </div>
      <div class="job-body">
        <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem); margin-bottom: 0.75rem;">[Context: why this job matters, what you know so far, what the risk is if you don't do it]</p>
        <!-- 2-3 discovery questions per job -->
        <div class="job-question">
          <span style="color: var(--brand-primary); font-weight: 900; min-width: 1.5rem;">[N]</span>
          <div>
            <p style="font-size: clamp(0.85rem, 1.2vw, 0.95rem);">"[Question text — in natural language, ready to use verbatim]"</p>
            <p style="color: var(--text-muted); font-size: clamp(0.75rem, 1vw, 0.8rem); margin-top: 0.25rem;">[Why to ask this / what to listen for / what answer means]</p>
          </div>
        </div>
        <!-- End question repeat -->
      </div>
    </div>
    <!-- End job repeat -->

    <!-- Landmine awareness (if relevant to this stage/deal) -->
    <div class="coaching-note" style="border-color: var(--warning);">
      <p class="coaching-note-label" style="color: var(--warning);">Landmines</p>
      <ul style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem); padding-left: 1.25rem;">
        <!-- Topics or areas that could derail the conversation if handled poorly -->
        <li style="margin-bottom: 0.25rem;">[Landmine — e.g., "Don't bring up pricing until they ask. If they bring it up, redirect to value."]</li>
        <!-- End repeat -->
      </ul>
    </div>

    <!-- Tactical moves — before, during, and after the next meeting -->
    <div class="coaching-note">
      <p class="coaching-note-label">Tactical Playbook</p>
      <div style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem);">
        <p style="margin-bottom: 0.5rem;"><strong>Before:</strong> [Pre-meeting preparation — e.g., research, materials to prepare, stakeholders to brief]</p>
        <p style="margin-bottom: 0.5rem;"><strong>During:</strong> [In-meeting tactics — e.g., call control, persona-specific delivery, questions to prioritize]</p>
        <p><strong>After:</strong> [Post-meeting follow-up — e.g., what to send, who to loop in, what to document]</p>
      </div>
    </div>
  </div>
</details>
```

---

### Section 06: Next Stage Preview

Transition checklist + next coaching agent. Same structure as before but renumbered to Section 06.

```html
<details class="section" id="section-next-stage">
  <summary>
    <div>
      <p class="section-number">Section 06</p>
      <h2 class="section-title">Next Stage Preview</h2>
    </div>
  </summary>
  <div class="section-body">
    <p class="section-subtitle">What must be true to advance from [Current Stage] to [Next Stage].</p>

    <div class="grid-2">
      <div class="card">
        <h4 style="font-family: var(--font-display); margin-bottom: 0.75rem; font-weight: 800;">Transition Checklist</h4>
        <ul style="list-style: none; padding: 0;">
          <!-- Repeat for each criterion (4-6 items) -->
          <!-- Use &#10003; for met, ~ for in-progress, &#10007; for not met -->
          <li style="display: flex; gap: 0.75rem; padding: 0.5rem 0; border-bottom: 1px solid var(--border);">
            <span style="color: [var(--success)|var(--warning)|var(--error)]; font-weight: 700;">[&#10003; or ~ or &#10007;]</span>
            <span style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem);">[Criterion text]</span>
          </li>
          <!-- End repeat -->
        </ul>
      </div>
      <div class="card">
        <h4 style="font-family: var(--font-display); margin-bottom: 0.75rem; font-weight: 800;">What Comes Next: [Next Stage Name]</h4>
        <span class="badge badge-primary" style="margin-bottom: 0.75rem;">[Next Stage Name — e.g., Compel]</span>
        <p style="color: var(--text-secondary); font-size: clamp(0.8rem, 1.1vw, 0.9rem); margin-top: 0.75rem;">[What the next coaching agent focuses on, what frameworks apply, what to prepare now]</p>
        <p style="color: var(--text-muted); font-size: clamp(0.75rem, 1vw, 0.8rem); margin-top: 0.75rem;"><strong>Prepare now:</strong> [Specific data or conversations to start now that feed into the next stage]</p>
      </div>
    </div>
  </div>
</details>
```

---

### The Play

NOT a collapsible section. Full-width gradient footer with two parts: strategic one-liner + concrete next move.

```html
<div class="the-play" id="section-the-play">
  <p class="the-play-label">The Play</p>
  <p class="the-play-text">"[One strategic sentence — the distilled coaching insight for this deal at this stage]"</p>
  <p class="the-play-action"><strong>Your next move:</strong> [Concrete, specific action — what to do, when, and what to watch for. 2-3 sentences max.]</p>
</div>

<div style="text-align: center; padding: 2rem 0 1rem; color: var(--text-muted); font-size: clamp(0.7rem, 0.9vw, 0.8rem);">
  Generated by Octave Deal Coach &bull; [Stage Name] &bull; [Date]
</div>
```

---

## Part 2: Coaching Deck Slide Templates

### Base Deck Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Company] — Deal Coaching [Stage Name]</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[Font Query]" rel="stylesheet">
  <style>
    :root {
      /* Populated from style preset */
    }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-snap-type: y mandatory; scroll-behavior: smooth; }
    body {
      font-family: var(--font-body);
      background: var(--bg);
      color: var(--text-primary);
    }

    .slide {
      height: 100vh;
      height: 100dvh;
      overflow: hidden;
      scroll-snap-align: start;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .slide-inner {
      max-width: 1100px;
      width: 100%;
      padding: var(--pad-y) var(--pad-x);
    }
    .bg-mesh {
      position: absolute;
      inset: 0;
      z-index: 0;
      opacity: 0.5;
      pointer-events: none;
    }
    .slide-content { position: relative; z-index: 1; }

    /* Progress Bar */
    #progress-bar {
      position: fixed;
      top: 0;
      left: 0;
      height: 3px;
      background: var(--brand-primary);
      z-index: 200;
      transition: width 0.3s var(--ease);
    }

    /* Nav Dots */
    #nav-dots {
      position: fixed;
      right: clamp(0.75rem, 2vw, 1.5rem);
      top: 50%;
      transform: translateY(-50%);
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      z-index: 100;
    }
    .nav-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--text-muted);
      opacity: 0.3;
      cursor: pointer;
      transition: all 0.3s var(--ease);
    }
    .nav-dot.active {
      opacity: 1;
      background: var(--brand-primary);
      transform: scale(1.4);
    }

    /* Slide Types */
    .slide-title h1 {
      font-family: var(--font-display);
      font-size: clamp(2rem, 5vw, 3.5rem);
      line-height: 1.1;
      margin-bottom: clamp(0.5rem, 1.5vw, 1rem);
    }
    .slide-title p {
      color: var(--text-secondary);
      font-size: clamp(1rem, 2vw, 1.3rem);
    }

    .slide-content h2 {
      font-family: var(--font-display);
      font-size: clamp(1.3rem, 3vw, 2rem);
      margin-bottom: clamp(1rem, 2vw, 1.5rem);
    }

    /* Animations */
    .animate-in {
      opacity: 0;
      transform: translateY(20px);
      transition: opacity 0.6s var(--ease), transform 0.6s var(--ease);
    }
    .animate-in.visible {
      opacity: 1;
      transform: translateY(0);
    }
    .animate-in:nth-child(2) { transition-delay: 0.1s; }
    .animate-in:nth-child(3) { transition-delay: 0.2s; }
    .animate-in:nth-child(4) { transition-delay: 0.3s; }
    .animate-in:nth-child(5) { transition-delay: 0.4s; }

    /* Responsive */
    @media (max-width: 768px) {
      #nav-dots { display: none; }
      .grid-2, .grid-3 { grid-template-columns: 1fr; }
    }
    @media (max-height: 600px) {
      .slide-inner { padding: 1rem 1.5rem; }
      .slide-title h1 { font-size: clamp(1.5rem, 4vw, 2.5rem); }
    }
    @media (prefers-reduced-motion: reduce) {
      html { scroll-snap-type: none; }
      .animate-in { opacity: 1; transform: none; }
      * { transition: none !important; animation: none !important; }
    }
    @media print {
      html { scroll-snap-type: none; }
      .slide { height: auto; min-height: 0; page-break-after: always; overflow: visible; }
      #progress-bar, #nav-dots { display: none; }
      .animate-in { opacity: 1; transform: none; }
    }
  </style>
</head>
<body>
  <div id="progress-bar" style="width: 0%;"></div>
  <div id="nav-dots"></div>

  <!-- Slides go here -->

  <script>
    const slides = document.querySelectorAll('.slide');
    const progressBar = document.getElementById('progress-bar');
    const navDotsContainer = document.getElementById('nav-dots');

    // Generate nav dots
    slides.forEach((_, i) => {
      const dot = document.createElement('div');
      dot.className = 'nav-dot';
      dot.onclick = () => slides[i].scrollIntoView({ behavior: 'smooth' });
      navDotsContainer.appendChild(dot);
    });

    const navDots = document.querySelectorAll('.nav-dot');

    // Intersection Observer
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const idx = Array.from(slides).indexOf(entry.target);
          navDots.forEach((d, i) => d.classList.toggle('active', i === idx));
          progressBar.style.width = ((idx + 1) / slides.length * 100) + '%';
          entry.target.querySelectorAll('.animate-in').forEach(el => el.classList.add('visible'));
        }
      });
    }, { threshold: 0.5 });

    slides.forEach(s => observer.observe(s));

    // Keyboard nav
    document.addEventListener('keydown', (e) => {
      const current = Array.from(slides).findIndex(s => s.getBoundingClientRect().top >= -10);
      if (['ArrowDown', 'PageDown', ' '].includes(e.key) && current < slides.length - 1) {
        e.preventDefault();
        slides[current + 1]?.scrollIntoView({ behavior: 'smooth' });
      }
      if (['ArrowUp', 'PageUp'].includes(e.key) && current > 0) {
        e.preventDefault();
        slides[current - 1]?.scrollIntoView({ behavior: 'smooth' });
      }
    });
  </script>
</body>
</html>
```

---

### Slide 1: Title Slide

```html
<section class="slide" data-slide="1">
  <div class="bg-mesh" style="background: radial-gradient(ellipse at 30% 50%, var(--brand-100) 0%, transparent 60%);"></div>
  <div class="slide-inner slide-content">
    <div style="display: flex; gap: 0.75rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
      <span class="badge badge-primary animate-in">Coaching Stage: [Stage Name]</span>
      <span class="badge badge-success animate-in">[Confidence] Confidence</span>
    </div>
    <h1 class="animate-in" style="font-family: var(--font-display); font-size: clamp(2rem, 5vw, 3.5rem);">[Company Name]</h1>
    <p class="animate-in" style="color: var(--text-secondary); font-size: clamp(1rem, 2vw, 1.3rem); margin-top: 0.5rem;">[Stage Name — e.g., Making the Case for Change]</p>
    <p class="animate-in" style="color: var(--text-muted); font-size: clamp(0.8rem, 1.2vw, 0.9rem); margin-top: 1rem;">[Date] | [Coaching Agent Name]</p>
  </div>
</section>
```

---

### Slide 2: Stage Context

```html
<section class="slide" data-slide="2">
  <div class="slide-inner slide-content">
    <h2 class="animate-in" style="font-family: var(--font-display); font-size: clamp(1.3rem, 3vw, 2rem);">Where This Deal Sits</h2>
    <p class="animate-in" style="color: var(--text-secondary); margin-bottom: 2rem;">[Brief context about deal position in the buying journey]</p>
    <div class="grid-2">
      <div class="card animate-in">
        <p class="talk-track-label">CRM Stage</p>
        <p style="font-family: var(--font-display); font-size: clamp(1.1rem, 1.8vw, 1.3rem);">[Stage Name]</p>
        <p style="color: var(--text-muted); font-size: clamp(0.75rem, 1vw, 0.85rem);">[Days in stage, deal amount]</p>
      </div>
      <div class="card animate-in">
        <p class="talk-track-label">Deal Coaching Assessment</p>
        <p style="font-family: var(--font-display); font-size: clamp(1.1rem, 1.8vw, 1.3rem);">[Stage Name — e.g., Resonate]</p>
        <p style="color: var(--text-muted); font-size: clamp(0.75rem, 1vw, 0.85rem);">[Confidence] confidence</p>
      </div>
    </div>
  </div>
</section>
```

---

### Slide 3-7: Coaching Sections (one per slide)

Template per coaching section (e.g., for Elevate: market context, urgency, vision, differentiation, reframe):

```html
<section class="slide" data-slide="[N]">
  <div class="bg-mesh" style="background: radial-gradient(ellipse at [position], var(--brand-100) 0%, transparent 70%);"></div>
  <div class="slide-inner slide-content">
    <span class="badge badge-primary animate-in" style="margin-bottom: 1rem;">[Step N of M]</span>
    <h2 class="animate-in" style="font-family: var(--font-display); font-size: clamp(1.3rem, 3vw, 2rem);">[Framework Step Name]</h2>
    <p class="animate-in" style="color: var(--text-secondary); margin: 1rem 0 1.5rem; font-size: clamp(0.9rem, 1.3vw, 1rem);">
      [Key insight for this step, grounded in deal data]
    </p>
    <div class="card animate-in">
      <p style="font-size: clamp(0.85rem, 1.2vw, 0.95rem); line-height: 1.7;">
        [Detailed content — evidence, data points, context for this framework step]
      </p>
    </div>
    <div class="talk-track animate-in" style="margin-top: 1rem;">
      <p class="talk-track-label">Talk Track</p>
      <p class="talk-track-text">"[Scripted talk track for this step]"</p>
    </div>
  </div>
</section>
```

---

### Slide 8: Talk Track (Full Flow)

```html
<section class="slide" data-slide="8">
  <div class="slide-inner slide-content">
    <h2 class="animate-in" style="font-family: var(--font-display); font-size: clamp(1.3rem, 3vw, 2rem);">Conversation Flow</h2>
    <div style="display: flex; flex-direction: column; gap: 0.75rem; margin-top: 1.5rem;">
      <!-- Repeat for each talk track step -->
      <div class="talk-track animate-in">
        <p class="talk-track-label">[Step — e.g., Step 1: External Pressures]</p>
        <p class="talk-track-text">"[Abbreviated talk track]"</p>
      </div>
      <!-- End repeat -->
    </div>
  </div>
</section>
```

---

### Slide 9: Evidence

```html
<section class="slide" data-slide="9">
  <div class="slide-inner slide-content">
    <h2 class="animate-in" style="font-family: var(--font-display); font-size: clamp(1.3rem, 3vw, 2rem);">Evidence & Proof Points</h2>
    <div class="grid-3" style="margin-top: 1.5rem;">
      <!-- Repeat for each proof point (max 6) -->
      <div class="card animate-in" style="text-align: center;">
        <p style="font-family: var(--font-display); font-size: clamp(1.5rem, 3vw, 2rem); color: var(--brand-primary); font-weight: 700;">[Metric]</p>
        <p style="color: var(--text-secondary); font-size: clamp(0.75rem, 1vw, 0.85rem); margin-top: 0.5rem;">[Description]</p>
        <span class="badge badge-primary" style="margin-top: 0.5rem;">[Framework Slot]</span>
      </div>
      <!-- End repeat -->
    </div>
  </div>
</section>
```

---

### Slide 10: CTA / Next Steps

```html
<section class="slide" data-slide="10">
  <div class="bg-mesh" style="background: radial-gradient(ellipse at 70% 50%, var(--brand-100) 0%, transparent 60%);"></div>
  <div class="slide-inner slide-content" style="text-align: center;">
    <span class="badge badge-primary animate-in" style="margin-bottom: 1.5rem;">Next Steps</span>
    <h2 class="animate-in" style="font-family: var(--font-display); font-size: clamp(1.3rem, 3vw, 2rem); margin-bottom: 1rem;">Advancing to [Next Stage]</h2>
    <p class="animate-in" style="color: var(--text-secondary); font-size: clamp(0.9rem, 1.3vw, 1rem); max-width: 600px; margin: 0 auto 2rem;">
      [Summary of what needs to happen next and what the transition to the next stage requires]
    </p>
    <div style="display: flex; flex-direction: column; gap: 0.75rem; max-width: 500px; margin: 0 auto;">
      <!-- Repeat for each action -->
      <div class="card animate-in" style="display: flex; gap: 1rem; align-items: center;">
        <span style="font-family: var(--font-mono); color: var(--brand-primary); font-weight: 700;">[N]</span>
        <p style="font-size: clamp(0.85rem, 1.2vw, 0.95rem);">[Action item]</p>
      </div>
      <!-- End repeat -->
    </div>
  </div>
</section>
```

---

## Style Defaults per Deal Stage

Each deal stage has a recommended default style preset that matches the psychological tone of the competency:

| Coaching Stage | Default Preset | Rationale |
|---------------|---------------|-----------|
| Resonate | `soft-light` | Exploratory, calm, trust-building |
| Elevate | `midnight-pro` | Urgency, disruption, bold contrast |
| Compel | `executive-dark` | Business gravitas, financial seriousness |

These are defaults only — the user can always override with any preset or brand-extracted theme.
