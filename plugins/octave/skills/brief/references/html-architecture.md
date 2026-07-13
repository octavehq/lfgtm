# Brief HTML Architecture

The brief is a scrollable reference document built on the shared scaffold in [../../shared/doc-scaffold.md](../../shared/doc-scaffold.md) — Google Fonts head, preset `:root` variables, reset, themed scrollbars, sticky nav dots with Intersection Observer, `<details>`/`<summary>` collapsible sections, cards, grids, print and responsive rules. This file lists only what's **brief-specific** on top of that base.

**Layout:** max-width 900px main column; on wide screens (≥1200px) a two-column `brief-layout` grid adds a sticky Quick Reference sidebar.

```css
/* === Occasion Badge (header pill: "Discovery Prep", "QBR Brief") === */
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

/* === Stakeholder Cards === */
.stakeholder-card { display: flex; gap: 1rem; align-items: flex-start; }
.stakeholder-avatar {
  width: 48px; height: 48px; border-radius: 50%;
  background: var(--brand-primary);
  display: flex; align-items: center; justify-content: center;
  color: white; font-weight: 700; flex-shrink: 0;
}

/* === ICP Fit Score Bar === */
.fit-bar {
  height: 8px; border-radius: 4px;
  background: var(--bg-elevated);
  overflow: hidden; margin: 0.5rem 0;
}
.fit-bar-fill {
  height: 100%; border-radius: 4px;
  background: var(--success);
  transition: width 0.8s ease;
}

/* === Deal Timeline === */
.timeline { position: relative; padding-left: 2rem; }
.timeline::before {
  content: ""; position: absolute;
  left: 0.5rem; top: 0; bottom: 0; width: 2px;
  background: var(--border-strong);
}
.timeline-event { position: relative; margin-bottom: 1.5rem; padding-left: 1rem; }
.timeline-event::before {
  content: ""; position: absolute;
  left: -1.75rem; top: 0.5rem; width: 10px; height: 10px;
  border-radius: 50%; background: var(--brand-primary);
}

/* === Quick Reference Sidebar (wide screens only) === */
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
```

**Body structure deltas from the shared scaffold:**

```html
<div class="brief-layout">
  <main class="doc-container">
    <header>
      <span class="occasion-badge">[Occasion] Prep</span>
      <h1>[Account Brief: Company Name]</h1>
      <p class="text-secondary">[Generated date] · [Target person if applicable]</p>
    </header>
    <!-- Sections: <details class="doc-section" open> per section
         (Company Snapshot, ICP Fit, Stakeholders, Motion & angle, Talking Points,
          Value Props, Competitive, Proof Points, Signals, Timeline) -->
  </main>
  <aside class="quick-ref">
    <h3>Quick Reference</h3>
    <!-- Key facts, do's/don'ts, one-line reminders -->
  </aside>
</div>
```

**Brief-specific notes:**
- Collapsible `<details>` sections for quick scanning during a call; all forced open on print (shared scaffold JS handles this).
- Optional Quick Reference sidebar is always visible while scrolling on wide screens.
- Print-friendly: occasion badge flattens to outlined text; cards and open sections avoid page breaks.
