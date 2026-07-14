# HTML Architecture

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[One-Pager Title]</title>
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
      font-family: var(--font-body);
      background: var(--bg);
      color: var(--text-primary);
      line-height: 1.6;
    }

    /* === Page Container (narrower than deck) === */
    .page {
      max-width: 800px;
      margin: 0 auto;
      padding: clamp(2rem, 5vw, 4rem) clamp(1.5rem, 4vw, 3rem);
    }

    /* === Typography (all clamp-based) === */
    .heading-1 { font-size: clamp(1.75rem, 4vw, 2.75rem); }
    .heading-2 { font-size: clamp(1.25rem, 2.5vw, 1.75rem); }
    .heading-3 { font-size: clamp(1rem, 1.8vw, 1.25rem); }
    .body-text { font-size: clamp(0.875rem, 1.3vw, 1rem); }
    .body-sm { font-size: clamp(0.75rem, 1.1vw, 0.875rem); }

    /* === Section Spacing === */
    .section { margin-bottom: clamp(2rem, 4vh, 3rem); }
    .section-title {
      font-family: var(--font-display);
      color: var(--brand-primary);
      margin-bottom: clamp(0.75rem, 1.5vh, 1.25rem);
    }

    /* === Components === */
    .card { ... }
    .metric-card { ... }
    .proof-quote { ... }
    .cta-block { ... }
    .divider { ... }

    /* === Print Styles === */
    @media print {
      body { background: white; color: #1a1a1a; }
      .page { max-width: 100%; padding: 0.5in; }
      .card { break-inside: avoid; border: 1px solid #e5e5e5; }
      .section { break-inside: avoid; }
      a { color: inherit; text-decoration: underline; }
    }

    /* === Responsive === */
    @media (max-width: 600px) {
      .grid-3 { grid-template-columns: 1fr; }
      .grid-2 { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="page">
    <!-- Header -->
    <!-- The Challenge -->
    <!-- Our Approach -->
    <!-- Key Differentiators -->
    <!-- Proof Points -->
    <!-- Next Steps -->
  </div>
</body>
</html>
```

Key differences from the deck skill's HTML:
- **No scroll snap** -- natural scrolling, single continuous page
- **No navigation dots or progress bar** -- not a presentation
- **No slide-level animations** -- subtle entrance animations are fine, but no Intersection Observer per-section
- **Narrower container** -- `max-width: 800px` (vs deck's 1100px)
- **Print-friendly** -- includes `@media print` styles for PDF/print output
- **No `overflow: hidden` sections** -- content flows naturally
