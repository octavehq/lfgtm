# Report Chart Components (CSS-Only)

All visualizations in the win/loss report are **pure CSS** — no JavaScript charting libraries. This ensures they print cleanly and render everywhere.

## Chart Variables

Add these alongside the style preset variables in `:root`:

```css
--chart-win: var(--success);
--chart-loss: var(--error);
--chart-neutral: var(--text-muted);
--chart-bar-height: 28px;
--chart-bar-radius: 4px;
--chart-bar-gap: 6px;
```

## Components

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
