# HTML Architecture

The proposal uses the same CSS variable system as `/octave:deck` (see [STYLE_PRESETS.md](../deck/STYLE_PRESETS.md)) but with a document layout instead of slides.

**Core structure:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Proposal Title] - [Company Name]</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    /* CSS Variables from chosen preset — :root { ... } */
    /* Reset & Base — smooth scroll, body with --font-body, --bg, --text-primary, line-height: 1.7 */
    /* Document Layout — .proposal-wrapper: flex, max-width 1100px, margin auto */
    /* Sidebar TOC — .toc-sidebar: width 220px, sticky, top 2rem; links with active state via --brand-primary */
    /* Main Content — .proposal-content: max-width 850px, flex 1, clamp padding */
    /* Sections — .proposal-section: margin-bottom clamp, scroll-margin-top for anchor offset */
    /* Cover Page — .cover-page: min-height 100vh, flex center, text-align center */
    /* Typography — h1-h3 with clamp() font sizes, --font-display; p with --text-secondary */
    /* Components — .card, .metric-card, .big-number, .quote-block, .timeline-step, .step-number, .pill, .pricing-table, .logo-grid */
    /* Print Styles (critical) — hide sidebar, full-width content, page-break-after on cover, page-break-inside avoid on sections/cards */
    /* Responsive — hide sidebar below 900px */
    /* prefers-reduced-motion — disable transitions */
  </style>
</head>
<body>
  <div class="proposal-wrapper">
    <nav class="toc-sidebar">
      <h4>Contents</h4>
      <a href="#executive-summary">Executive Summary</a>
      <a href="#the-challenge">The Challenge</a>
      <!-- ... one link per section -->
    </nav>
    <main class="proposal-content">
      <section class="cover-page" id="cover">...</section>
      <section class="proposal-section" id="executive-summary">...</section>
      <!-- Continue for each section -->
    </main>
  </div>
  <script>
    // Intersection Observer for active TOC highlighting
    // Smooth scroll behavior
  </script>
</body>
</html>
```

**Print styles are non-negotiable for proposals.** Buyers print these documents. Always include:
- `page-break-after: always` on cover page
- `page-break-inside: avoid` on sections and cards
- `page-break-after: avoid` on h2 (keep headings with their content)
- Hide sidebar, expand content to full width
- Set body font-size to 11pt for readability
