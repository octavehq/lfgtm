# Section Layouts Reference

Section-specific CSS patterns for the 8 positioning system frameworks. These extend the base styles defined in the main SKILL.md and should be included inline in the generated HTML `<style>` block.

---

## Section 1: Message Framework — Stacked Bands

Three horizontal bands forming a "house" — Market layer at the top, MVP in the middle, Value Props at the bottom. Each layer has a distinct background intensity.

```css
/* === Message Framework === */
.house-layer {
  border-radius: var(--radius-lg);
  padding: clamp(1rem, 2vh, 1.5rem);
  margin-bottom: 1rem;
}
.house-market {
  background: var(--bg-elevated);
  border: 1px solid var(--border-strong);
}
.house-mvp {
  background: var(--bg-card);
  border: 1px solid var(--border);
}
.house-vps {
  background: transparent;
  border: 1px solid var(--border);
  padding: 0;
  overflow: hidden;
}
.house-layer-label {
  font-family: var(--font-display);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--brand-primary);
  margin-bottom: 0.75rem;
}
.house-cell {
  padding: clamp(0.5rem, 1vw, 0.75rem);
}
.house-cell-label {
  display: block;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  margin-bottom: 0.25rem;
}
.house-cell p {
  font-size: clamp(0.8rem, 1vw, 0.9rem);
  color: var(--text-primary);
}

/* Value Proposition Grid (8-column layout) */
.vp-grid {
  display: grid;
  grid-template-columns: 120px repeat(7, 1fr);
  font-size: clamp(0.7rem, 0.9vw, 0.8rem);
}
.vp-header {
  background: var(--bg-elevated);
  border-bottom: 2px solid var(--border-strong);
}
.vp-header .vp-col-label {
  padding: 0.5rem 0.4rem;
  font-weight: 600;
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--text-secondary);
}
.vp-row {
  border-bottom: 1px solid var(--border);
  transition: background 0.15s ease;
}
.vp-row:hover {
  background: var(--bg-card-hover);
}
.vp-row:last-child {
  border-bottom: none;
}
.vp-cell {
  padding: 0.5rem 0.4rem;
  color: var(--text-primary);
  line-height: 1.4;
}
/* Persona color left border on VP rows */
.vp-row.persona-user { border-left: 3px solid #34d399; }
.vp-row.persona-champion { border-left: 3px solid #60a5fa; }
.vp-row.persona-decision { border-left: 3px solid #f59e0b; }
.vp-row.persona-financial { border-left: 3px solid #f87171; }
.vp-row.persona-technical { border-left: 3px solid #a78bfa; }

@media (max-width: 768px) {
  .vp-grid {
    grid-template-columns: 1fr;
    font-size: 0.8rem;
  }
  .vp-header { display: none; }
  .vp-cell::before {
    content: attr(data-label);
    display: block;
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.15rem;
  }
}
```

---

## Section 2: Positioning Anchors — Highlighted Statements

Large text statements with inline keyword highlights. Uses the `.highlight-*` classes from the base styles.

```css
/* === Positioning Anchors === */
.anchor-statements {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}
.anchor-line {
  padding: 0.75rem 1rem;
  border-radius: var(--radius);
  background: var(--bg-card);
  border: 1px solid var(--border);
  font-size: clamp(0.9rem, 1.3vw, 1.1rem);
  line-height: 1.6;
}
.anchor-line p {
  margin: 0;
}
```

---

## Section 3: Positioning Strategy — Data Table

Full-width comparison table with colored accents. Built on `.data-table` from base styles.

No additional CSS needed beyond `.data-table` — all styling comes from the base. Use inline styles for row-specific coloring (red for "Why That Sucks", green for "Why That's Better").

---

## Section 4: Persona-Based Messaging — Horizontal Card Grid

5-column grid: persona label + 4 messaging dimensions. Each row color-coded by persona.

```css
/* === Persona-Based Messaging === */
.persona-messaging-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.pm-header-row {
  display: grid;
  grid-template-columns: 140px repeat(4, 1fr);
  gap: 0.5rem;
}
.pm-col-header {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  padding: 0.5rem;
  text-align: center;
}
.pm-row {
  display: grid;
  grid-template-columns: 140px repeat(4, 1fr);
  gap: 0.5rem;
  padding: 0.5rem 0;
  border-radius: var(--radius);
}
.pm-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
}
.pm-cell {
  font-size: clamp(0.78rem, 1vw, 0.88rem);
  line-height: 1.4;
}
.pm-divider {
  text-align: center;
  padding: 0.75rem 0;
  border-top: 1px dashed var(--border);
  border-bottom: 1px dashed var(--border);
  margin: 0.25rem 0;
}

@media (max-width: 900px) {
  .pm-header-row { display: none; }
  .pm-row {
    grid-template-columns: 1fr;
    gap: 0.75rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 1rem;
  }
  .pm-cell::before {
    content: attr(data-label);
    display: block;
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.15rem;
  }
}
```

---

## Section 5: Awareness Funnel — 4-Column Grid with Progressive Color

Four columns with a left-to-right color gradient indicating awareness progression. Row labels on the left.

```css
/* === Awareness Funnel === */
.funnel-grid {
  display: grid;
  grid-template-columns: 120px repeat(4, 1fr);
  gap: 0.5rem;
  align-items: start;
}
.funnel-header {
  padding: 0.75rem;
  text-align: center;
  border-radius: var(--radius) var(--radius) 0 0;
  font-weight: 600;
}
.funnel-stage-label {
  font-size: 0.85rem;
  font-weight: 600;
}
/* Progressive intensity: lightest on left, strongest on right */
.funnel-stage-1 .funnel-stage-label,
.funnel-cell.funnel-stage-1 { opacity: 0.7; }
.funnel-stage-2 .funnel-stage-label,
.funnel-cell.funnel-stage-2 { opacity: 0.8; }
.funnel-stage-3 .funnel-stage-label,
.funnel-cell.funnel-stage-3 { opacity: 0.9; }
.funnel-stage-4 .funnel-stage-label,
.funnel-cell.funnel-stage-4 { opacity: 1.0; }

/* Stage header background colors */
.funnel-header.funnel-stage-1 { background: rgba(251, 191, 36, 0.1); color: var(--warning); }
.funnel-header.funnel-stage-2 { background: rgba(248, 113, 113, 0.1); color: var(--error); }
.funnel-header.funnel-stage-3 { background: rgba(59, 130, 246, 0.1); color: var(--brand-primary); }
.funnel-header.funnel-stage-4 { background: rgba(52, 211, 153, 0.1); color: var(--success); }

.funnel-row-label {
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-secondary);
  padding: 0.75rem 0.5rem 0.75rem 0;
  align-self: center;
}
.funnel-cell {
  font-size: clamp(0.8rem, 1vw, 0.88rem);
  line-height: 1.4;
}

@media (max-width: 768px) {
  .funnel-grid {
    grid-template-columns: 1fr;
  }
  .funnel-row-label {
    font-size: 1rem;
    padding: 1rem 0 0.25rem;
    border-top: 1px solid var(--border);
  }
  .funnel-header { display: none; }
  .funnel-cell::before {
    content: attr(data-stage);
    display: block;
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.25rem;
  }
}
```

---

## Section 6: Use Case Canvas — Split-View Comparison

Two-column layout: "The Current Way" (left, red-tinted) and "The New Way" (right, blue/green-tinted). Each side flows left to right through steps.

```css
/* === Use Case Canvas === */
.canvas-split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}
.canvas-current {
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  background: rgba(248, 113, 113, 0.04);
  border: 1px solid rgba(248, 113, 113, 0.15);
}
.canvas-new {
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  background: rgba(59, 130, 246, 0.04);
  border: 1px solid rgba(59, 130, 246, 0.15);
}
.canvas-label {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.canvas-label-current { color: var(--error); }
.canvas-label-new { color: var(--brand-primary); }

.canvas-flow {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.canvas-cell {
  padding: 0.75rem;
  border-radius: var(--radius);
  background: var(--bg-card);
  border: 1px solid var(--border);
  font-size: clamp(0.78rem, 1vw, 0.88rem);
}
.canvas-cell-label {
  display: block;
  font-size: 0.65rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  margin-bottom: 0.25rem;
}
.canvas-problem { border-left: 3px solid var(--error); }
.canvas-limitation { border-left: 3px solid var(--warning); }
.canvas-capability { border-left: 3px solid var(--brand-primary); }
.canvas-outcome { border-left: 3px solid var(--success); }
.canvas-arrow {
  text-align: center;
  color: var(--text-muted);
  font-size: 0.9rem;
  padding: 0.15rem 0;
}

@media (max-width: 768px) {
  .canvas-split { grid-template-columns: 1fr; }
}
```

---

## Section 7: Use Case Lifecycle — Horizontal Timeline

Horizontal scrollable phase timeline. Each phase is a column card with header, activity, tools, and stakeholder dots.

```css
/* === Use Case Lifecycle === */
.timeline-phases {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
  -webkit-overflow-scrolling: touch;
}
.timeline-phases::-webkit-scrollbar {
  height: 4px;
}
.timeline-phases::-webkit-scrollbar-track {
  background: var(--bg-elevated);
  border-radius: 2px;
}
.timeline-phases::-webkit-scrollbar-thumb {
  background: var(--border-strong);
  border-radius: 2px;
}
.phase {
  min-width: 160px;
  flex: 1;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  overflow: hidden;
}
.phase-header {
  padding: 0.6rem 0.75rem;
  background: var(--bg-elevated);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.phase-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: var(--brand-primary);
  color: var(--bg);
  font-weight: 700;
  font-size: 0.7rem;
  flex-shrink: 0;
}
.phase-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-primary);
}
.phase-body {
  padding: 0.75rem;
}
.phase-activity {
  font-size: 0.78rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
  line-height: 1.4;
}
.phase-tools {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  margin-bottom: 0.5rem;
}
.phase-stakeholders {
  display: flex;
  gap: 0.25rem;
  padding-top: 0.25rem;
  border-top: 1px solid var(--border);
}
```

---

## Section 8: Homepage Messaging — Template Cards

Two-column layout: primary (homepage) and secondary (other pages). Uses a "We are..." / "That helps..." / "Dealing with..." / "Solved by..." template structure.

```css
/* === Homepage Messaging === */
.homepage-template {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.homepage-row {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
}
.homepage-label {
  font-family: var(--font-display);
  font-size: clamp(0.85rem, 1.2vw, 1rem);
  font-weight: 600;
  color: var(--text-secondary);
  min-width: 100px;
  padding-top: 0.75rem;
  flex-shrink: 0;
}
.homepage-row .card {
  flex: 1;
}

@media (max-width: 768px) {
  .homepage-row {
    flex-direction: column;
    gap: 0.25rem;
  }
  .homepage-label {
    min-width: auto;
    padding-top: 0;
  }
}
```

---

## Including These Styles

When generating the positioning system HTML, **include all relevant section CSS inline** in the `<style>` block. Only include CSS for sections being generated:

- Full exercise: include all 8 section layouts
- Single section mode: include only that section's layout

Copy the CSS blocks above directly into the `<style>` element after the base styles from the SKILL.md template.
