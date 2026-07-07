# Positioning System HTML Scaffold

The positioning system is a scrollable reference document built on the shared scaffold in [../../shared/doc-scaffold.md](../../shared/doc-scaffold.md) — Google Fonts head, preset `:root` variables, reset, themed scrollbars, sticky nav dots with Intersection Observer, `<details>`/`<summary>` collapsible sections, cards, callouts, data tables, grids, print and responsive rules. This file lists only what's **positioning-specific** on top of that base. Section-specific CSS (message-framework bands, funnel columns, timelines, canvases) is in [section-layouts.md](section-layouts.md); full per-section HTML is in [section-templates.md](section-templates.md).

**Layout delta:** `max-width: 1100px` container (wider than the other doc skills — positioning frameworks need horizontal space for grids).

```css
/* === Section numbering ("Section 01" progression labels) === */
.section-number { font-family: var(--font-mono); font-size: 0.75rem; color: var(--brand-primary); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.25rem; }
.section-subtitle { font-size: clamp(0.85rem, 1.2vw, 1rem); color: var(--text-secondary); margin-bottom: 1.5rem; }

/* === Header Banner === */
.header-banner { padding: clamp(2rem, 5vh, 4rem) 0; border-bottom: 1px solid var(--border); margin-bottom: clamp(2rem, 4vh, 3rem); }
.header-banner h1 { font-family: var(--font-display); font-size: clamp(2rem, 4vw, 3.2rem); font-weight: 700; margin-bottom: 0.5rem; }
.header-banner .subtitle { font-size: clamp(1rem, 1.5vw, 1.25rem); color: var(--text-secondary); }
.meta-badges { display: flex; gap: 0.75rem; margin-top: 1.25rem; flex-wrap: wrap; }
.meta-badge { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.25rem 0.75rem; border-radius: var(--radius-pill); background: var(--bg-card); border: 1px solid var(--border); font-size: 0.8rem; color: var(--text-secondary); }

/* === Wide grids (persona columns, awareness stages) === */
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: clamp(0.75rem, 1.5vw, 1.25rem); }
.grid-5 { display: grid; grid-template-columns: repeat(5, 1fr); gap: clamp(0.75rem, 1.5vw, 1rem); }

/* === Persona Color System (consistent across all 8 sections) === */
.persona-user { border-color: #34d399; }
.persona-user .persona-dot { background: #34d399; }
.persona-champion { border-color: #60a5fa; }
.persona-champion .persona-dot { background: #60a5fa; }
.persona-decision { border-color: #f59e0b; }
.persona-decision .persona-dot { background: #f59e0b; }
.persona-financial { border-color: #f87171; }
.persona-financial .persona-dot { background: #f87171; }
.persona-technical { border-color: #a78bfa; }
.persona-technical .persona-dot { background: #a78bfa; }
.persona-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 0.4rem; }

/* === Highlighted Text (positioning anchor keywords) === */
.highlight { padding: 0.1rem 0.4rem; border-radius: 3px; font-weight: 600; }
.highlight-category { background: rgba(168, 85, 247, 0.2); color: #c084fc; }
.highlight-persona { background: rgba(59, 130, 246, 0.2); color: #93c5fd; }
.highlight-usecase { background: rgba(52, 211, 153, 0.2); color: #6ee7b7; }
.highlight-problem { background: rgba(248, 113, 113, 0.2); color: #fca5a5; }
.highlight-feature { background: rgba(251, 191, 36, 0.2); color: #fcd34d; }

/* === Responsive deltas === */
@media (max-width: 768px) {
  .grid-4, .grid-5 { grid-template-columns: 1fr; }
  .funnel-grid { grid-template-columns: 1fr; }
  .canvas-split { grid-template-columns: 1fr; }
  .timeline-phases { overflow-x: auto; }
}
```

**Body structure deltas from the shared scaffold:**

```html
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
<!-- See section-templates.md for full HTML per section -->
```

**Key differences from the other doc skills:**
- **Max-width 1100px** (wider — positioning frameworks need horizontal space for grids)
- **Persona color system** — consistent color coding across all 8 sections (User=green, Champion=blue, Decision Maker=amber, Financial Buyer=red, Technical Influencer=purple)
- **Highlight classes** — for styling positioning anchor keywords (category, persona, use case, problem, feature)
- **Grid-4 and Grid-5** — for persona columns and awareness stage columns
- **Section numbering** — "Section 01" labels for clear progression through the exercise
