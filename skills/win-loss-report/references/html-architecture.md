# HTML Architecture

Multi-section scrollable report. Key structural requirements:

- **Max-width 900px** centered container
- **Sticky sidebar** with section navigation dots (fixed left, vertically centered)
- **CSS variables** from chosen preset, plus chart-specific variables:
  ```css
  --chart-win: var(--success);
  --chart-loss: var(--error);
  --chart-neutral: var(--text-muted);
  --chart-bar-height: 28px;
  --chart-bar-radius: 4px;
  --chart-bar-gap: 6px;
  ```
- **All font sizes use `clamp()`** -- responsive to viewport
- **Self-contained HTML**, inline CSS (except Google Fonts link)
- **Print-friendly** -- CSS charts print well since they're just styled divs. Include `@media print` rules to hide navigation, set `print-color-adjust: exact`, and `page-break-inside: avoid` on sections.
- **Responsive** -- `@media (max-width: 768px)` collapses grids to single column, hides sidebar nav

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Win/Loss Report - [Period]</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[fonts]&display=swap" rel="stylesheet">
  <style>
    :root { /* preset variables + chart variables */ }
    /* Reset, base body styles, report-container (max-width: 900px) */
    /* Sidebar nav: fixed left, dot per section, active state via brand-primary */
    /* Section styles: padding, border-bottom dividers */
    /* Typography: report-title, section-title, subsection-title, body-text (all clamp) */
    /* Component classes listed below */
    /* Print + responsive media queries */
  </style>
</head>
<body>
  <nav class="sidebar-nav" id="sidebar-nav"><!-- JS-generated dots --></nav>
  <div class="report-container">
    <!-- Sections 1-12 as <section class="report-section"> blocks -->
  </div>
  <script>
    // Generate sidebar nav dots from sections
    // Intersection Observer for active section tracking
    // Smooth scroll on dot click
  </script>
</body>
</html>
```

#### CSS Component System

All visualizations are **pure CSS** -- no JavaScript charting libraries. This ensures they print cleanly and render everywhere.

**Metric Cards** (`.metric-card`):
Large number + label + optional trend badge. Use in grid layouts.
```html
<div class="metric-card">
  <div class="metric-value" style="color: var(--chart-win);">12</div>
  <div class="metric-label">Deals Won</div>
  <div class="metric-trend trend-up">&#9650; 3 vs last quarter</div>
</div>
```

**Win Rate Ring** (`.win-rate-ring`):
CSS `conic-gradient` donut chart. Set `--win-pct` as inline style variable.
```html
<div class="win-rate-ring" style="--win-pct: 34;">
  <div class="win-rate-ring-inner">
    <span class="win-rate-number">34%</span>
    <span class="text-muted">Win Rate</span>
  </div>
</div>
```

**Horizontal Bar Charts** (`.bar-chart` > `.bar-row`):
3-column grid: label | stacked bar track | value. Green fill for wins, red for losses.
```html
<div class="bar-row">
  <span class="bar-label">Competitor A</span>
  <div class="bar-track">
    <div class="bar-fill-win" style="width: 60%;"></div>
    <div class="bar-fill-loss" style="width: 40%;"></div>
  </div>
  <span class="bar-value">60%</span>
</div>
```

**Progress Bars** (`.progress-bar` > `.progress-fill`):
Thin 8px bars for frequency indicators inside pattern cards.

**Takeaway Cards** (`.takeaway-card`):
Left-border accent cards for executive summary. Modifiers: `.win`, `.loss`, `.neutral`.

**Pattern Cards** (`.pattern-card`):
Rank + title + frequency bar + evidence quote block for win/loss pattern sections.

**Deal Cards** (`.deal-card`):
Company name + status badge (`.deal-status.won` / `.deal-status.lost`) + narrative.

**Recommendation Cards** (`.rec-card`):
Numbered circle + title + rationale. 2-column grid layout.

**Data Tables** (`.data-table`):
Standard table for objection analysis. Uppercase muted headers, row dividers.

**Trend Indicators**:
`.trend-up` (green + up arrow), `.trend-down` (red + down arrow), `.trend-flat` (muted).
