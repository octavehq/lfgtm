# Meeting layout

Use [meeting-sections.md](meeting-sections.md) as the single content/ID schema. Populate this scaffold from the current method; placeholders describe a scaffold, not verified account facts.


```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Meeting Prep: [Company] — [Meeting Type]</title>
  <!-- Social share (link unfurl) metadata -->
  <meta property="og:title" content="Meeting Prep: [Company]">
  <meta property="og:description" content="[1-2 sentence summary a stranger understands]">
  <meta property="og:image" content="assets/og.png">
  <meta name="twitter:card" content="summary_large_image">
  <!-- Google Fonts (preconnect + stylesheet) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* === CSS Variables (from brand kit or style preset) === */
    :root {
      --bg: /* from brand kit or style preset */;
      --bg-elevated: /* from brand kit or style preset */;
      --bg-card: /* from brand kit or style preset */;
      --bg-panel: /* from brand kit or style preset */;
      --text-primary: /* from brand kit or style preset */;
      --text-secondary: /* from brand kit or style preset */;
      --text-muted: /* from brand kit or style preset */;
      --brand-primary: /* from brand kit or style preset */;
      --brand-primary-soft: /* from brand kit or style preset */;
      --brand-primary-muted: /* 25% alpha of brand-primary */;
      --secondary: /* from brand kit or style preset */;
      --success: #3fb950;
      --success-soft: rgba(63,185,80,0.12);
      --warning: #d29922;
      --warning-soft: rgba(210,153,34,0.12);
      --error: #f85149;
      --error-soft: rgba(248,81,73,0.12);
      --border: /* from brand kit or style preset */;
      --border-strong: /* from brand kit or style preset */;
      --border-soft: /* from brand kit or style preset */;
      --font-display: /* from brand kit or style preset */;
      --font-body: /* from brand kit or style preset */;
      --font-mono: /* from brand kit or style preset */;
      --radius: 6px;
      --radius-lg: 8px;
      --radius-section: 12px;
      --radius-pill: 9999px;
      --shadow-low: 0px 1px 4px -1px rgba(0,0,0,0.09);
      --shadow-medium: 0px 4px 24px rgba(0,0,0,0.2);
      --ease: cubic-bezier(0.25, 0.46, 0.45, 0.94);
      --speed: 0.16s;
    }

    /* === Reset & Base === */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      background: var(--bg);
      color: var(--text-primary);
      font-family: var(--font-body);
      line-height: 1.6;
      font-size: 15px;
    }

    /* === Layout === */
    .prep-container {
      max-width: 900px;
      margin: 0 auto;
      padding: 2rem clamp(1rem, 4vw, 3rem);
    }

    /* === Sidebar Navigation (sticky) === */
    .prep-nav {
      position: fixed;
      top: 50%;
      right: clamp(0.5rem, 2vw, 2rem);
      transform: translateY(-50%);
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
      z-index: 100;
    }
    .prep-nav a {
      display: block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--text-muted);
      transition: all 0.3s ease;
      text-decoration: none;
    }
    .prep-nav a.active {
      background: var(--brand-primary);
      transform: scale(1.5);
    }

    /* === Header === */
    .prep-header { margin-bottom: 1.5rem; padding-bottom: 1rem; }
    .header-badges { display: flex; gap: 0.5rem; margin-bottom: 0.75rem; flex-wrap: wrap; }
    .prep-header h1 {
      font-family: var(--font-display);
      font-size: clamp(1.6rem, 3vw, 2.2rem);
      font-weight: 700;
      margin-bottom: 0.5rem;
      letter-spacing: -0.02em;
    }
    .header-subtitle {
      font-size: clamp(0.9rem, 1.3vw, 1.05rem);
      color: var(--text-secondary);
      margin-bottom: 0.25rem;
      line-height: 1.5;
    }
    .header-meta { font-size: 0.8rem; color: var(--text-muted); }

    /* === Meeting Type & Duration Badges === */
    .meeting-badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: var(--radius-pill);
      background: var(--brand-primary);
      color: white;
      font-size: 0.72rem;
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
      font-size: 0.72rem;
      font-weight: 600;
    }

    /* === Expand/Collapse Toggle === */
    .expand-toggle {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      padding: 0.3rem 0.7rem;
      border-radius: var(--radius-pill);
      background: var(--bg-elevated);
      border: 1px solid var(--border-strong);
      color: var(--text-secondary);
      font-family: var(--font-body);
      font-size: 0.7rem;
      font-weight: 600;
      cursor: pointer;
      transition: color 0.15s ease, border-color 0.15s ease;
    }
    .expand-toggle:hover {
      color: var(--text-primary);
      border-color: var(--brand-primary);
    }
    .expand-toggle .toggle-icon {
      font-size: 0.6rem;
      color: var(--brand-primary);
    }

    /* === Snapshot Bar === */
    .snapshot-bar {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 1rem;
      padding: 1rem 1.25rem;
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      margin-bottom: 2.5rem;
    }
    .snapshot-item { text-align: center; }
    .snapshot-label {
      display: block;
      font-size: 0.65rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-muted);
      margin-bottom: 0.2rem;
    }
    .snapshot-value {
      display: block;
      font-family: var(--font-display);
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--text-primary);
    }

    /* === Section Styles === */
    .prep-section {
      margin-bottom: 2.5rem;
      padding-bottom: 2rem;
      border-bottom: 1px solid var(--border);
    }
    .section-intro {
      font-size: 0.82rem;
      color: var(--text-muted);
      font-style: italic;
      margin-bottom: 1.25rem;
      line-height: 1.5;
    }

    /* === Collapsible Sections (details.prep-section) === */
    details.prep-section {
      border-bottom: 1px solid var(--border);
      margin-bottom: 2.5rem;
      padding-bottom: 1rem;
    }
    details.prep-section > summary {
      cursor: pointer;
      font-family: var(--font-display);
      font-size: clamp(1.1rem, 2vw, 1.35rem);
      font-weight: 600;
      color: var(--text-primary);
      padding: 0.75rem 0;
      list-style: none;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      letter-spacing: -0.01em;
    }
    details.prep-section > summary::-webkit-details-marker { display: none; }
    details.prep-section > summary::before {
      content: "\25B6";
      font-size: 0.65em;
      color: var(--brand-primary);
      transition: transform 0.2s ease;
    }
    details.prep-section[open] > summary::before { transform: rotate(90deg); }

    /* === Sub-section Headers === */
    .sub-section-title {
      font-family: var(--font-display);
      font-size: clamp(0.88rem, 1.4vw, 1.05rem);
      font-weight: 600;
      color: var(--text-primary);
      margin: 1.75rem 0 0.75rem 0;
      padding-bottom: 0.35rem;
      border-bottom: 1px solid var(--border);
    }
    .sub-section-title:first-of-type { margin-top: 0.5rem; }

    /* === Generic Card === */
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: clamp(1rem, 2vw, 1.5rem);
      margin-bottom: 0.75rem;
    }

    /* === Card Groups (collapsible sub-sections) === */
    .card-group {
      margin-bottom: 1.25rem;
    }
    .card-group > summary {
      font-family: var(--font-display);
      font-size: clamp(0.85rem, 1.3vw, 0.98rem);
      font-weight: 600;
      color: var(--text-primary);
      padding: 0.5rem 0;
      cursor: pointer;
      list-style: none;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .card-group > summary::-webkit-details-marker { display: none; }
    .card-group > summary::before {
      content: "\25B6";
      font-size: 0.55em;
      color: var(--brand-primary);
      transition: transform 0.2s ease;
    }
    .card-group[open] > summary::before { transform: rotate(90deg); }
    .card-group-intro {
      font-size: 0.78rem;
      color: var(--text-muted);
      font-style: italic;
      margin-bottom: 0.75rem;
      line-height: 1.5;
    }

    /* === Company Identity === */
    .company-identity {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      margin-bottom: 0.75rem;
    }
    .company-logo {
      width: 28px;
      height: 28px;
      border-radius: 6px;
      object-fit: contain;
      background: white;
      padding: 3px;
    }
    .company-name {
      font-family: var(--font-display);
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text-primary);
    }

    /* === Context Grid (used for Company, Deal, and inside Table Cards) === */
    .context-grid {
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      overflow: hidden;
    }
    .cg-row {
      display: grid;
      grid-template-columns: 140px 1fr;
      border-bottom: 1px solid var(--border);
    }
    .cg-row:last-child { border-bottom: none; }
    .cg-label {
      font-size: 0.72rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-muted);
      padding: 0.6rem 0.9rem;
      background: var(--bg-elevated);
      display: flex;
      align-items: flex-start;
      padding-top: 0.7rem;
    }
    .cg-value {
      font-size: 0.85rem;
      color: var(--text-secondary);
      padding: 0.6rem 0.9rem;
      line-height: 1.5;
    }

    /* === People — Persona Groups === */
    .people-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 0.6rem;
    }
    .persona-group {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      overflow: hidden;
    }
    .persona-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.6rem 1rem;
      border-bottom: 1px solid var(--border);
    }
    .persona-title {
      font-weight: 600;
      font-size: 0.88rem;
      color: var(--text-primary);
    }
    .persona-why {
      padding: 0.45rem 1rem 0.5rem;
      font-size: 0.78rem;
      color: var(--text-muted);
      line-height: 1.45;
      border-bottom: 1px solid var(--border);
    }
    .persona-people {
      padding: 0.35rem 0;
    }
    .persona-person {
      display: flex;
      align-items: center;
      gap: 0.65rem;
      padding: 0.4rem 1rem;
    }
    .persona-person + .persona-person {
      border-top: 1px solid var(--border);
    }
    .pp-avatar {
      width: 30px;
      height: 30px;
      border-radius: 50%;
      background: var(--brand-primary-soft, rgba(99,102,241,0.1));
      border: 1px solid var(--brand-primary-muted, rgba(99,102,241,0.2));
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--brand-primary, #6366f1);
      font-weight: 600;
      font-size: 0.62rem;
      flex-shrink: 0;
      letter-spacing: 0.02em;
    }
    .pp-info { flex: 1; min-width: 0; }
    .pp-name {
      font-weight: 600;
      font-size: 0.82rem;
      color: var(--text-primary);
    }
    .pp-title {
      font-size: 0.72rem;
      color: var(--text-muted);
    }
    .pp-link {
      font-size: 0.68rem;
      color: var(--secondary);
      text-decoration: none;
      transition: color 0.15s ease;
      flex-shrink: 0;
    }
    .pp-link:hover { color: var(--text-primary); text-decoration: underline; }
    .slot-tag {
      font-size: 0.55rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 0.1rem 0.4rem;
      border-radius: var(--radius-pill);
    }
    .slot-tag.potential-fit { background: var(--brand-primary-soft, rgba(99,102,241,0.1)); color: var(--brand-primary, #6366f1); }
    .slot-tag.confirmed-tag { background: var(--success-soft); color: var(--success); }

    /* === Unconfirmed Tag (person/title named but not verified against a real tool result) === */
    .unconfirmed {
      display: inline-flex;
      align-items: center;
      gap: 0.2rem;
      font-size: 0.55rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 0.1rem 0.4rem;
      border-radius: var(--radius-pill);
      background: var(--warning-soft);
      color: var(--warning);
      vertical-align: middle;
    }

    /* === Collapsible Table Cards (individual items) === */
    details.table-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      margin-bottom: 0.75rem;
      overflow: hidden;
    }
    details.table-card > summary {
      padding: 0.7rem 0.9rem;
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--text-primary);
      cursor: pointer;
      list-style: none;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    details.table-card > summary::-webkit-details-marker { display: none; }
    details.table-card > summary::before {
      content: "\25B6";
      font-size: 0.5em;
      color: var(--brand-primary);
      transition: transform 0.2s ease;
      flex-shrink: 0;
    }
    details.table-card[open] > summary::before { transform: rotate(90deg); }
    details.table-card > .context-grid {
      border-radius: 0;
      border: none;
      border-top: 1px solid var(--border);
    }
    details.table-card > .cc-questions {
      padding: 0.5rem 0.9rem 0.7rem;
      border-top: 1px solid var(--border);
    }

    /* === Status Tags (inside table-card rows) === */
    .cc-status {
      font-size: 0.6rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 0.15rem 0.5rem;
      border-radius: var(--radius-pill);
      flex-shrink: 0;
      white-space: nowrap;
    }
    .cc-status.unexplored { background: var(--warning-soft); color: var(--warning); }
    .cc-status.raised { background: var(--brand-primary-soft); color: var(--brand-primary); }
    .cc-status.validated { background: var(--success-soft); color: var(--success); }
    .cc-status.needs-reinforcement { background: rgba(124,108,255,0.12); color: var(--secondary); }
    .cc-status.expected { background: var(--warning-soft); color: var(--warning); }

    /* === Response List (inside objection table-cards) === */
    .response-list {
      list-style: none;
      padding: 0;
      margin: 0;
    }
    .response-list li {
      font-size: 0.85rem;
      color: var(--text-secondary);
      padding: 0.2rem 0;
      padding-left: 1rem;
      position: relative;
      line-height: 1.5;
    }
    .response-list li::before {
      content: "\2192";
      position: absolute;
      left: 0;
      color: var(--brand-primary);
      font-size: 0.8rem;
    }
    .response-list li strong { color: var(--text-primary); }

    /* === Discovery Questions (collapsible, inside table-cards) === */
    .cc-questions { margin-top: 0.5rem; }
    details.cc-questions > summary {
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--brand-primary);
      cursor: pointer;
      list-style: none;
      padding: 0.3rem 0;
    }
    details.cc-questions > summary::-webkit-details-marker { display: none; }
    details.cc-questions > summary::before {
      content: "+";
      font-weight: 700;
      color: var(--brand-primary);
      margin-right: 0.35rem;
      font-size: 0.7rem;
    }
    details.cc-questions[open] > summary::before { content: "\2212"; }
    .cc-q-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0;
      margin-top: 0.4rem;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow: hidden;
    }
    .cc-q-row { display: contents; }
    .cc-q-cell {
      padding: 0.3rem 0.55rem;
      font-size: 0.7rem;
      color: var(--text-secondary);
      line-height: 1.4;
      border-bottom: 1px solid var(--border);
    }
    .cc-q-cell:nth-child(odd) { background: var(--bg-elevated); }
    .cc-q-row:last-child .cc-q-cell { border-bottom: none; }
    .cc-q-header {
      font-size: 0.55rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      padding: 0.25rem 0.55rem;
      background: var(--bg-elevated);
      border-bottom: 1px solid var(--border);
    }

    /* === The Takeaway (featured) === */
    .the-takeaway {
      text-align: center;
      padding: 2.5rem 2rem;
      border: 2px solid var(--brand-primary);
      border-radius: var(--radius-lg);
      margin-top: 1rem;
    }
    .the-takeaway blockquote {
      font-family: var(--font-display);
      font-size: clamp(1.15rem, 2.5vw, 1.5rem);
      font-weight: 500;
      font-style: italic;
      color: var(--text-primary);
      line-height: 1.5;
    }

    /* === Grid Utilities === */
    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem; }

    /* === Brand Header (only when brand kit is active) === */
    .brand-header {
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(8,9,10,0.85);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      padding: 0 clamp(1rem, 4vw, 3rem);
    }
    .brand-header-inner {
      max-width: 900px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 48px;
    }
    .brand-header-logo {
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--text-primary);
      text-decoration: none;
    }
    .brand-header-logo svg { width: 18px; height: 18px; }
    .brand-header-logo span {
      font-family: var(--font-display);
      font-weight: 600;
      font-size: 0.9rem;
      letter-spacing: -0.01em;
    }
    .brand-header-right {
      display: flex;
      align-items: center;
      gap: 1rem;
      font-size: 0.78rem;
      color: var(--text-muted);
    }
    .brand-header-tag {
      font-size: 0.6rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--brand-primary);
      background: var(--brand-primary-soft);
      padding: 0.15rem 0.5rem;
      border-radius: var(--radius-pill);
    }

    /* === What's Happening Now (deep research conditional) === */
    .macro-themes { display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: 1rem; }
    .macro-theme {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-left: 3px solid var(--brand-primary);
      border-radius: var(--radius-lg);
      padding: 0.85rem 1rem;
    }
    .mt-title {
      font-family: var(--font-display);
      font-size: 0.92rem;
      font-weight: 600;
      color: var(--text-primary);
      margin-bottom: 0.3rem;
    }
    .mt-body {
      font-size: 0.82rem;
      color: var(--text-secondary);
      line-height: 1.55;
    }
    .signal-feed { display: flex; flex-direction: column; gap: 0; }
    .signal-item {
      display: grid;
      grid-template-columns: 90px 1fr;
      gap: 0.75rem;
      padding: 0.55rem 0;
      border-bottom: 1px solid var(--border);
    }
    .signal-item:last-child { border-bottom: none; }
    .signal-date {
      font-size: 0.68rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-muted);
      padding-top: 0.1rem;
    }
    .signal-headline {
      font-size: 0.84rem;
      font-weight: 500;
      color: var(--text-primary);
      line-height: 1.4;
    }
    .signal-relevance {
      font-size: 0.76rem;
      color: var(--text-muted);
      font-style: italic;
      line-height: 1.4;
      margin-top: 0.15rem;
    }

    /* === Deal Timeline === */
    .deal-timeline {
      margin-top: 1rem;
      padding: 0.75rem 0;
      overflow-x: auto;
    }
    .tl-track {
      display: flex;
      align-items: flex-start;
      gap: 0;
      min-width: max-content;
      padding: 0 0.5rem;
    }
    .tl-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      min-width: 100px;
      position: relative;
      padding: 0 0.5rem;
    }
    .tl-item::before {
      content: "";
      position: absolute;
      top: 5px;
      left: 0;
      right: 0;
      height: 2px;
      background: var(--border-strong);
    }
    .tl-item:first-child::before { left: 50%; }
    .tl-item:last-child::before { right: 50%; }
    .tl-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--text-muted);
      border: 2px solid var(--bg);
      position: relative;
      z-index: 1;
      flex-shrink: 0;
    }
    .tl-dot.active { background: var(--brand-primary); box-shadow: 0 0 0 3px var(--brand-primary-soft); }
    .tl-date {
      font-size: 0.62rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-muted);
      margin-top: 0.4rem;
      white-space: nowrap;
    }
    .tl-label {
      font-size: 0.72rem;
      color: var(--text-secondary);
      text-align: center;
      margin-top: 0.2rem;
      max-width: 120px;
      line-height: 1.35;
    }
    .tl-item.current .tl-date { color: var(--brand-primary); }
    .tl-item.current .tl-label { color: var(--text-primary); font-weight: 500; }
    .tl-gap {
      display: flex;
      flex-direction: column;
      align-items: center;
      min-width: 80px;
      position: relative;
      padding: 0 0.25rem;
    }
    .tl-gap::before {
      content: "";
      position: absolute;
      top: 5px;
      left: 0;
      right: 0;
      height: 2px;
      background: repeating-linear-gradient(90deg, var(--text-muted) 0, var(--text-muted) 4px, transparent 4px, transparent 8px);
      opacity: 0.4;
    }
    .tl-gap-line { height: 12px; } /* spacer to align with dots */
    .tl-gap-label {
      font-size: 0.62rem;
      color: var(--warning);
      font-style: italic;
      white-space: nowrap;
      margin-top: 0.4rem;
    }
    @media (max-width: 768px) {
      .tl-track { flex-direction: column; min-width: unset; align-items: flex-start; padding-left: 1.5rem; }
      .tl-item, .tl-gap { flex-direction: row; align-items: center; min-width: unset; padding: 0.4rem 0; gap: 0.75rem; }
      .tl-item::before { top: 0; bottom: 0; left: -1rem; right: unset; width: 2px; height: auto; }
      .tl-item:first-child::before { top: 50%; left: -1rem; }
      .tl-item:last-child::before { bottom: 50%; left: -1rem; }
      .tl-gap::before { top: 0; bottom: 0; left: -1rem; right: unset; width: 2px; height: auto;
        background: repeating-linear-gradient(180deg, var(--text-muted) 0, var(--text-muted) 4px, transparent 4px, transparent 8px); }
      .tl-dot { position: absolute; left: -1.35rem; }
      .tl-label { text-align: left; max-width: none; }
      .tl-gap-line { display: none; }
    }

    /* === Brand Footer === */
    .brand-footer {
      border-top: 1px solid var(--border);
      padding: 1.5rem clamp(1rem, 4vw, 3rem);
      margin-top: 2rem;
    }
    .brand-footer-inner {
      max-width: 900px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .brand-footer-logo {
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--text-muted);
    }
    .brand-footer-logo svg { width: 14px; height: 14px; }
    .brand-footer-logo span {
      font-family: var(--font-display);
      font-weight: 600;
      font-size: 0.78rem;
    }
    .brand-footer-meta {
      font-size: 0.68rem;
      color: var(--text-muted);
    }

    /* === Tabs (persona shifts + objection themes) === */
    .tab-bar { display: flex; gap: 4px; overflow-x: auto; padding: 0.3rem 0; margin-bottom: 0.75rem; }
    .tab-btn { font-size: 0.65rem; font-weight: 600; padding: 0.3rem 0.7rem; border-radius: var(--radius-pill);
               border: 1px solid var(--border); background: transparent; color: var(--text-secondary); cursor: pointer;
               font-family: var(--font-body); white-space: nowrap; transition: all 0.15s ease; }
    .tab-btn:hover { border-color: var(--brand-primary); color: var(--text-primary); }
    .tab-btn.active { background: var(--brand-primary-soft); color: var(--brand-primary); border-color: var(--brand-primary); }
    .tab-panel { display: none; }
    .tab-panel.active { display: block; }

    /* === Persona Tags (objection cards) === */
    .persona-tag { font-size: 0.55rem; font-weight: 600; padding: 0.1rem 0.4rem; border-radius: var(--radius-pill);
                   background: var(--bg-elevated); color: var(--text-secondary); margin-left: 0.3rem; }

    /* === Watch Out rows === */
    .cg-watchout { color: var(--text-muted); font-style: italic; font-size: 0.82rem; }

    /* === Persona Hero === */
    .persona-hero {
      padding: 0.35rem 1rem 0.45rem;
      font-size: 0.75rem;
      color: var(--brand-primary);
      font-weight: 500;
      line-height: 1.4;
      border-bottom: 1px solid var(--border);
      background: var(--brand-primary-soft);
    }

    /* === Positioning Directive === */
    .positioning-directive {
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      overflow: hidden;
      margin-bottom: 1.25rem;
    }
    .pd-row {
      display: grid;
      grid-template-columns: 140px 1fr;
      border-bottom: 1px solid var(--border);
    }
    .pd-row:last-child { border-bottom: none; }
    .pd-label {
      font-size: 0.72rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--brand-primary);
      padding: 0.6rem 0.9rem;
      background: var(--bg-elevated);
      display: flex;
      align-items: flex-start;
      padding-top: 0.7rem;
    }
    .pd-value {
      font-size: 0.85rem;
      color: var(--text-secondary);
      padding: 0.6rem 0.9rem;
      line-height: 1.5;
    }

    /* === Print === */
    @media print {
      .prep-nav, .brand-header, .brand-footer { display: none; }
      .prep-container { max-width: 100%; padding: 1rem; }
      details.prep-section[open] { break-inside: avoid; }
      .card, .table-card { break-inside: avoid; }
      body { color: #111; background: white; font-size: 12px; }
      .meeting-badge { border: 1px solid #111; background: transparent; color: #111; }
      .snapshot-bar { background: #f5f5f5; border: 1px solid #ddd; }
    }

    /* === Responsive === */
    @media (max-width: 768px) {
      .grid-2, .cc-q-grid { grid-template-columns: 1fr; }
      .snapshot-bar { grid-template-columns: repeat(2, 1fr); }
      .prep-nav { display: none; }
      .tab-bar { flex-wrap: wrap; }
    }

    @media (prefers-reduced-motion: reduce) {
      * { transition: none !important; animation: none !important; }
    }
  </style>
</head>
<body>

  <!-- REQUIRED when using a brand kit. Read the logo SVG from ~/.octave/brands/<slug>/ and inline it. -->
  <header class="brand-header">
    <div class="brand-header-inner">
      <a class="brand-header-logo" href="https://[domain]" target="_blank">
        <!-- Inline the real SVG logo from the brand kit here -->
        <span>[Company Name]</span>
      </a>
      <div class="brand-header-right">
        <span class="brand-header-tag">Meeting Prep</span>
      </div>
    </div>
  </header>

  <!-- Sidebar Navigation Dots -->
  <nav class="prep-nav" id="prep-nav"></nav>

  <!-- Main Prep Document -->
  <main class="prep-container">

    <!-- Header -->
    <header class="prep-header">
      <div class="header-badges">
        <span class="meeting-badge">[Meeting Type]</span>
        <span class="duration-badge">[Duration] min</span>
        <button class="expand-toggle" id="expand-toggle" onclick="toggleAll()">
          <span class="toggle-icon">&#9660;</span> Expand all
        </button>
      </div>
      <h1>Meeting Prep: [Company Name]</h1>
      <p class="header-subtitle">[One sentence describing the meeting context]</p>
      <p class="header-meta">[Date] · [Attendees]</p>
    </header>

    <!-- Deal Snapshot Bar -->
    <div class="snapshot-bar">
      <div class="snapshot-item">
        <span class="snapshot-label">Deal Value</span>
        <span class="snapshot-value">[value or TBD]</span>
      </div>
      <div class="snapshot-item">
        <span class="snapshot-label">Stage</span>
        <span class="snapshot-value">[stage]</span>
      </div>
      <div class="snapshot-item">
        <span class="snapshot-label">Target Close</span>
        <span class="snapshot-value">[date or TBD]</span>
      </div>
      <div class="snapshot-item">
        <span class="snapshot-label">Primary Contact</span>
        <span class="snapshot-value">[name, title]</span>
      </div>
    </div>

    <details class="prep-section" open id="context">
      <summary>1. Context</summary>
      <!-- Company fit and limits; actual attendees, suggested roles, opportunity and latest commitments. Label account facts and hypotheses separately. Populate from meeting-sections.md and current evidence. -->
    </details>

    <details class="prep-section" open id="goals">
      <summary>2. Goals</summary>
      <!-- Positioning directive and grounded recognition goals with supporting evidence, disconfirming probe and conditional advancement. Populate from meeting-sections.md and current evidence. -->
    </details>

    <details class="prep-section" open id="competitive">
      <summary>3. Competitive</summary>
      <!-- Actual alternative, buyer criteria, supported differences, concessions and facts to verify. Populate from meeting-sections.md and current evidence. -->
    </details>

    <details class="prep-section" open id="say-ask">
      <summary>4. What to Say & Ask</summary>
      <!-- Opening, argument, applicable proof, grounding and branching questions, next-decision ask. Separate spoken wording from rationale. Populate from meeting-sections.md and current evidence. -->
    </details>

    <details class="prep-section" open id="objections">
      <summary>5. Objections</summary>
      <!-- Observed concern or labeled anticipation, distinguishing question, supported response, proof and unresolved limits. Populate from meeting-sections.md and current evidence. -->
    </details>

    <details class="prep-section" open id="takeaway">
      <summary>6. Takeaway</summary>
      <!-- Primary move, observable meeting success condition, and next action with owner. Populate from meeting-sections.md and current evidence. -->
    </details>

  </main>

  <script>
    // Generate nav dots from section IDs
    const nav = document.getElementById('prep-nav');
    const sectionIds = ['context', 'goals', 'competitive', 'say-ask', 'objections', 'takeaway'];
    sectionIds.forEach(id => {
      const a = document.createElement('a');
      a.href = '#' + id;
      a.dataset.section = id;
      a.setAttribute("aria-label", document.getElementById(id).querySelector("summary").textContent);
      nav.appendChild(a);
    });

    // Intersection Observer for active section tracking
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          document.querySelectorAll('.prep-nav a').forEach(a => a.classList.remove('active'));
          const dot = document.querySelector(`.prep-nav a[data-section="${entry.target.id}"]`);
          if (dot) dot.classList.add('active');
        }
      });
    }, { threshold: 0.3 });

    sectionIds.forEach(id => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });

    // Open all details on print
    window.onbeforeprint = () => {
      document.querySelectorAll('details').forEach(d => d.open = true);
    };

    // Expand/Collapse All toggle
    let allExpanded = false;
    function toggleAll() {
      allExpanded = !allExpanded;
      document.querySelectorAll('details').forEach(d => d.open = allExpanded);
      const btn = document.getElementById('expand-toggle');
      btn.innerHTML = allExpanded
        ? '<span class="toggle-icon">&#9650;</span> Collapse all'
        : '<span class="toggle-icon">&#9660;</span> Expand all';
    }

    function switchTab(btn, containerId) {
      const container = document.getElementById(containerId);
      const bar = btn.parentElement;
      bar.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const index = Array.from(bar.children).indexOf(btn);
      container.querySelectorAll('.tab-panel').forEach((p, i) => {
        p.classList.toggle('active', i === index);
      });
    }
  </script>

  <!-- REQUIRED when using a brand kit. Same logo as header, smaller. -->
  <footer class="brand-footer">
    <div class="brand-footer-inner">
      <div class="brand-footer-logo">
        <!-- Inline the real SVG logo from the brand kit here -->
        <span>[Company Name]</span>
      </div>
      <div class="brand-footer-meta">Prepared [Date]</div>
    </div>
  </footer>

</body>
</html>
```

**Self-contained:** Inline CSS, zero external dependencies (except Google Fonts / brand kit webfonts). No JavaScript frameworks.
