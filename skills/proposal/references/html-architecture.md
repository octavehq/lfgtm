# HTML Architecture

The proposal uses the same CSS variable system as `/octave:deck` (see the shared [style-presets.md](../../shared/style-presets.md)) but with a document layout instead of slides.

**Core structure:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Proposal Title] - [Company Name]</title>
  <meta property="og:title" content="[Proposal Title]: [Company Name]">
  <meta property="og:description" content="[1-2 sentence summary a stranger understands]">
  <meta property="og:image" content="assets/og.png">
  <meta name="twitter:card" content="summary_large_image">
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
    /* Components — .card, .solves-for (pain-mapping tag on capability cards), .persona-frame (per-persona framing strip, one row per real persona), .metric-card, .big-number, .quote-block, .pricing-table, .logo-grid, .placeholder (LITERAL prominent panel: dashed accent border, "Your input goes here" tag + display-size "( Add your ___ )" cue, for spots where the seller's input beats ours like pricing and rollout timing; never fabricate to fill, never bury in small print), .unconfirmed (tag for any person/detail not confirmed via a real tool result) */
    /* Side-by-side proof/result cards: align internal bands (header, body, metric row, quote) across cards via CSS subgrid — parent sets the row tracks, each card sets grid-template-rows: subgrid and spans them. Give cards a parallel metric count so the number row reads as one strip. */
    /* Cover: no Stage/deal-process chip; no Confidential stamp unless requested. Section titles are standard proposal headings, one label per heading (no eyebrow that repeats the title). */
    /* Print Styles (critical) — hide sidebar, full-width content, page-break-after on cover, page-break-inside avoid on sections/cards */
    /* Responsive — hide sidebar below 900px */
    /* prefers-reduced-motion — disable transitions */
  </style>
</head>
<body>
  <div class="proposal-wrapper">
    <nav class="toc-sidebar">
      <h4>Contents</h4>
      <a href="#bottom-line">Executive summary</a>
      <a href="#problem">The problem</a>
      <a href="#what-wed-do">What we propose</a>
      <a href="#worth-it">The business case</a>
      <a href="#proof">Proof</a>
      <a href="#how-it-goes">Implementation</a>
      <!-- Stage-trimmed proposals show only the jobs they include -->
    </nav>
    <main class="proposal-content">
      <section class="cover-page" id="cover">...</section>
      <section class="proposal-section" id="bottom-line">...</section>
      <!-- Continue for each of the six jobs -->
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
