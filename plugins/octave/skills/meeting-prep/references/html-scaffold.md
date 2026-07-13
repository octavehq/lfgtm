# Meeting Prep HTML Scaffold

The prep is a scrollable reference document built on the shared scaffold in [../../shared/doc-scaffold.md](../../shared/doc-scaffold.md) — Google Fonts head, preset `:root` variables, reset, themed scrollbars, `target="_blank"` link rule, sticky nav dots with Intersection Observer, `<details>`/`<summary>` collapsible sections, cards, grids, print and responsive rules. This file lists only what's **prep-specific** on top of that base.

**This is a component-pattern reference, not a fixed stylesheet to reproduce verbatim.** Adapt it: drive the palette, type, and logo from the brand kit (`~/.octave/brands/<slug>/`) so the output reads like the sender's real collateral, not a generic dark template. The `[…]` are placeholders — fill with real values, never literal brackets.

```css
/* === Meeting Type / Duration Badges (header) === */
.meeting-badge {
  display: inline-block; padding: 0.25rem 0.75rem;
  border-radius: var(--radius-pill);
  background: var(--brand-primary); color: white;
  font-size: 0.75rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.05em;
}
.duration-badge {
  display: inline-block; padding: 0.25rem 0.75rem;
  border-radius: var(--radius-pill);
  background: var(--bg-elevated); border: 1px solid var(--border-strong);
  color: var(--text-secondary); font-size: 0.75rem; font-weight: 600;
}

/* === Stakeholder Cards === */
.stakeholder-card { display: flex; gap: 1rem; align-items: flex-start; }
.stakeholder-avatar {
  width: 48px; height: 48px; border-radius: 50%;
  background: var(--brand-primary);
  display: flex; align-items: center; justify-content: center;
  color: white; font-weight: 700; flex-shrink: 0;
}

/* === Buying Role Badge === */
.role-badge {
  display: inline-block; padding: 0.2rem 0.6rem;
  border-radius: var(--radius-pill);
  font-size: 0.7rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.05em;
}
.role-badge.economic-buyer { background: var(--brand-primary); color: white; }
.role-badge.champion       { background: var(--success); color: white; }
.role-badge.evaluator      { background: var(--secondary); color: white; }
.role-badge.influencer     { background: var(--bg-elevated); color: var(--text-secondary); border: 1px solid var(--border-strong); }
.role-badge.blocker        { background: var(--error); color: white; }

/* === Unconfirmed flag (grounding) === */
.unconfirmed {
  display: inline-block; padding: 0.15rem 0.5rem;
  border-radius: var(--radius-pill);
  font-size: 0.68rem; font-weight: 600;
  background: transparent; border: 1px dashed var(--warning); color: var(--warning);
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

/* === The Line (featured closing statement) === */
.the-line {
  text-align: center; padding: 2rem;
  border: 2px solid var(--brand-primary);
  border-radius: var(--radius-lg); margin-top: 2rem;
}
.the-line blockquote {
  font-family: var(--font-display);
  font-size: clamp(1.2rem, 2.5vw, 1.6rem);
  font-weight: 500; font-style: italic;
  color: var(--text-primary);
}

/* Responsive delta */
@media (max-width: 768px) { .competitor-row { grid-template-columns: 1fr; } }
/* Print delta */
@media print { .card, .persona-block, .beat { break-inside: avoid; } }
```

**Body structure deltas from the shared scaffold** (section-by-section markup patterns):

```html
<!-- 1. Header -->
<header class="doc-section">
  <span class="meeting-badge">[Meeting Type] Prep</span>
  <span class="duration-badge">[Duration] min</span>
  <h1>[Company Name] — Meeting Prep</h1>
  <p class="text-secondary">
    [Date] ·
    <!-- Attendees: each linked to verified LinkedIn; ⚠ unconfirmed flag where needed. -->
    <a href="[linkedin]" target="_blank" rel="noopener noreferrer">[Name]</a> ([Role]) ·
    <a href="[company-website]" target="_blank" rel="noopener noreferrer">[company.com]</a>
  </p>
</header>

<!-- 2. Snapshot (merged situation + deal state — do NOT repeat deal intel later) -->
<section class="doc-section" id="snapshot">
  <h2 class="section-title">Snapshot</h2>
  <p class="body-text">[2-3 sentence situation]</p>
  <div class="snapshot-strip">
    <!-- Only render the cells that are actually known -->
    <div class="snapshot-cell"><div class="label">Stage</div><div class="value">[…]</div></div>
    <div class="snapshot-cell"><div class="label">Compelling Event</div><div class="value">[…]</div></div>
  </div>
  <div class="outcome-line"><strong>What we want out of this meeting:</strong> [one specific advance]</div>
</section>

<!-- 3. Why This Company, Why Now: fit, why-now, .news-item entries (dated + linked),
        market intel, .reference-card grid of similar customers. Internal doc: link cited
        library entities to https://app.octavehq.com/entity/{oId}. -->
<!-- 4. Stakeholders: .stakeholder-card grid with .role-badge / .unconfirmed flags -->
<!-- 5. Why [Product] for Each Persona: .persona-block per persona with .lane-label lanes -->
<!-- 6. The Winning Story: five .story-beat rows -->
<!-- 7. How to Run the Conversation: .beat blocks (point + listen-for + ask-for) -->
<!-- 8. Discovery Questions: .question-item entries with .reveals notes -->
<!-- 9. Objections & Competitors: .objection-item entries, .competitor-row grid, .watch-out -->
<!-- 10. The Line: .the-line blockquote -->
```
