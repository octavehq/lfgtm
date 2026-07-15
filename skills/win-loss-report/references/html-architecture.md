# HTML Architecture

4-section scrollable report with tabbed interfaces. Key structural requirements:

- **Max-width 900px** centered container
- **Sticky sidebar** with section navigation dots (fixed left, vertically centered)
- **CSS variables** from workspace company's brand kit, plus chart-specific variables:
  ```css
  --chart-win: #4ade80;    /* green — derive from brand if possible */
  --chart-loss: #f87171;   /* red — derive from brand if possible */
  --chart-neutral: var(--muted);
  --chart-bar-height: 28px;
  --chart-bar-radius: 4px;
  --chart-bar-gap: 6px;
  ```
- **All font sizes use `clamp()`** — responsive to viewport
- **Self-contained HTML**, inline CSS (except Google Fonts / Typekit link)
- **Print-friendly** — CSS charts print well since they're just styled divs. Include `@media print` rules to hide navigation, flatten tabs to labeled blocks, set `print-color-adjust: exact`, and `page-break-inside: avoid` on cards.
- **Responsive** — `@media (max-width: 768px)` collapses grids to single column, hides sidebar nav

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Win/Loss Report - [Period]</title>
  <!-- Brand kit font link (Typekit or Google Fonts) -->
  <style>
    :root { /* brand kit tokens + chart variables */ }
    /* Reset, base body styles, report-container (max-width: 900px) */
    /* Topbar: workspace logo + "Win/Loss Report" | right side empty */
    /* Sidebar nav: fixed left, dot per section, active state via brand accent */
    /* Section styles: padding, border-bottom dividers */
    /* Section numbers: .section-num — 0.95rem, bold 700, accent color */
    /* Dimension labels: .dim-label — 0.82rem, bold 700, accent color, border-bottom */
    /* Tab system: .tab-bar, .tab-btn, .tab-panel */
    /* Typography: report-title, section-title, subsection-title, body-text (all clamp) */
    /* Component classes listed below */
    /* Print + responsive media queries */
  </style>
</head>
<body>
  <!-- Topbar with workspace company logo + report title; right side is empty -->
  <div class="topbar">
    <div class="topbar-left">
      <img src="[workspace-logo-url]" alt="[Company]" />
      <span class="sep"></span>
      <span class="label">Win/Loss Report</span>
    </div>
    <div class="topbar-right"></div>
  </div>

  <nav class="sidebar-nav" id="sidebar-nav"><!-- JS-generated dots --></nav>

  <div class="report-container">
    <!-- Section 1: Scorecard -->
    <section class="report-section" id="scorecard">
      <!-- Section number label "01 Scorecard" -->
      <!-- Headline metrics: win rate ring + 3 metric cards -->
      <!-- Dimension label "WIN RATE BY SEGMENT" -->
      <!-- Segment breakdown (mini bar chart) -->
      <!-- Dimension label "WIN RATE BY PERSONA" -->
      <!-- Persona breakdown -->
      <!-- Dimension label "WIN RATE BY COMPETITOR" -->
      <!-- Competitor breakdown (stacked bar chart) -->
    </section>

    <!-- Section 2: Win/Loss Analysis (tabbed) -->
    <section class="report-section" id="analysis">
      <!-- Section number label "02 Win/Loss Analysis" -->
      <div class="tab-bar" role="tablist">
        <button role="tab" aria-selected="true" aria-controls="panel-win">Win Analysis</button>
        <button role="tab" aria-selected="false" aria-controls="panel-loss">Loss Analysis</button>
      </div>
      <div class="tab-panel" role="tabpanel" id="panel-win" aria-hidden="false">
        <!-- Use Cases Where We Win (cards) -->
        <!-- What to Keep Doing (action list) -->
      </div>
      <div class="tab-panel" role="tabpanel" id="panel-loss" aria-hidden="true">
        <!-- Use Cases Where We Lose (cards) -->
        <!-- What to Stop Doing / Changes to Make (action list) -->
        <!-- Objections (table sorted by loss correlation) -->
      </div>
    </section>

    <!-- Section 3: Head-to-Head Deals (tabbed by dimension) -->
    <section class="report-section" id="head-to-head">
      <!-- Section number label "03 Head-to-Head Deals" -->
      <div class="tab-bar" role="tablist">
        <button role="tab" aria-selected="true" aria-controls="panel-competitor">By Competitor</button>
        <button role="tab" aria-selected="false" aria-controls="panel-segment">By Segment</button>
        <button role="tab" aria-selected="false" aria-controls="panel-persona">By Persona</button>
      </div>
      <div class="tab-panel" role="tabpanel" id="panel-competitor" aria-hidden="false">
        <!-- Aggregate win/loss pattern columns grouped by competitor -->
      </div>
      <div class="tab-panel" role="tabpanel" id="panel-segment" aria-hidden="true">
        <!-- Aggregate win/loss pattern columns grouped by segment -->
      </div>
      <div class="tab-panel" role="tabpanel" id="panel-persona" aria-hidden="true">
        <!-- Aggregate win/loss pattern columns grouped by persona -->
      </div>
    </section>

    <!-- Section 4: Data Sources -->
    <section class="report-section" id="data-sources">
      <!-- Data window, counts, completeness notes -->
    </section>
  </div>

  <!-- Footer with workspace logo + "Generated by Octave" -->
  <footer class="report-footer">
    <img src="[workspace-logo-url]" alt="[Company]" />
    <span>Generated by Octave</span>
  </footer>

  <script>
    // Tab switching (shared across both tab bars)
    // Generate sidebar nav dots from sections
    // Intersection Observer for active section tracking
    // Smooth scroll on dot click
  </script>
</body>
</html>
```

#### CSS Component System

All visualizations are **pure CSS** — no JavaScript charting libraries. This ensures they print cleanly and render everywhere.

**Section Numbers** (`.section-num`):
Large bold labels like "01 Scorecard", "02 Win/Loss Analysis" that introduce each section.
```css
.section-num { font-size: 0.95rem; font-weight: 700; color: var(--accent); letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px; }
```

**Dimension Labels** (`.dim-label`):
Prominent labels above each bar chart dimension (e.g., "WIN RATE BY SEGMENT", "WIN RATE BY PERSONA"). Accent-colored with a bottom border separator.
```css
.dim-label { font-size: 0.82rem; font-weight: 700; color: var(--accent); border-bottom: 1px solid var(--border); padding-bottom: 6px; margin-bottom: 12px; letter-spacing: 0.06em; text-transform: uppercase; }
```

**Metric Cards** (`.metric-card`):
Large number + label + optional trend badge. Use in grid layouts. 3 cards: Deals Won, Deals Lost, Calls Analyzed. Every metric shows BOTH volume and rate.
```html
<div class="metric-card">
  <div class="metric-value" style="color: var(--chart-win);">12</div>
  <div class="metric-label">Deals Won</div>
  <div class="metric-sublabel">34% of closed deals</div>
</div>
```

**Win Rate Ring** (`.win-rate-ring`):
CSS `conic-gradient` donut chart. Set `--win-pct` as inline style variable.
```html
<div class="win-rate-ring" style="--win-pct: 66;">
  <div class="win-rate-ring-inner">
    <span class="win-rate-number">66%</span>
    <span class="text-muted">Win Rate</span>
    <span class="text-muted">71 of 108 deals</span>
  </div>
</div>
```

**Horizontal Stacked Bar Charts** (`.bar-chart` > `.bar-row`):
3-column grid: label | stacked bar track | value. Green fill for wins, red for losses.
```html
<div class="bar-row">
  <span class="bar-label">[Competitor A]</span>
  <div class="bar-track">
    <div class="bar-fill-win" style="width: 69%;"></div>
    <div class="bar-fill-loss" style="width: 31%;"></div>
  </div>
  <span class="bar-value">69% (20/29)</span>
</div>
```

**Tab System** (`.tab-bar` > `button` + `.tab-panel`):
Rounded tab buttons with brand accent on active state. Win/Loss tabs use green/red dot indicators. Head-to-Head tabs use neutral dots.
```css
.tab-bar { display: flex; gap: 2px; background: var(--surface-dk); border-radius: var(--radius) var(--radius) 0 0; padding: 8px 8px 0; }
.tab-bar button { font-family: var(--font); font-weight: 600; padding: .6rem 1.2rem; border: none; border-radius: 8px 8px 0 0; cursor: pointer; background: transparent; color: var(--muted); display: inline-flex; align-items: center; gap: 8px; }
.tab-bar button::before { content: ""; width: 8px; height: 8px; border-radius: 50%; }
.tab-bar button[aria-selected="true"] { color: var(--accent); background: var(--surface); }
```

**Use Case Cards** (`.usecase-card`):
Card per use case with volume, rate, segment/persona tags.
```html
<div class="usecase-card">
  <div class="usecase-header">
    <h4 class="usecase-name">Medical Chronology Automation</h4>
    <span class="usecase-rate win">78% win rate</span>
  </div>
  <div class="usecase-volume">14 deals (9 won, 5 lost)</div>
  <div class="usecase-tags">
    <span class="tag segment">[Segment]</span>
    <span class="tag persona">Managing Partner</span>
  </div>
  <p class="usecase-evidence">Wins correlate with firms processing 500+ cases/year where paralegal capacity is the bottleneck.</p>
</div>
```

**Action Lists** (`.action-list` > `.action-item`):
Compact ranked list used in "What to Keep Doing" and "What to Stop Doing." Each item shows a rank number, the pattern text, and a frequency line. No evidence quotes or blockquotes.
```html
<div class="action-list">
  <div class="action-item">
    <div class="action-rank">1</div>
    <div class="action-body">
      <div class="action-text">Champion drove internal business case with ROI proof</div>
      <div class="action-freq">Appeared in 8 of 12 wins (67%)</div>
    </div>
  </div>
  <div class="action-item">
    <div class="action-rank">2</div>
    <div class="action-body">
      <div class="action-text">Ran live demo on prospect's own data during first call</div>
      <div class="action-freq">Appeared in 7 of 12 wins (58%)</div>
    </div>
  </div>
</div>
```
```css
.action-list { display: flex; flex-direction: column; gap: 8px; }
.action-item { display: flex; align-items: flex-start; gap: 12px; padding: 10px 14px; background: var(--surface); border-radius: var(--radius); border: 1px solid var(--border); }
.action-rank { font-size: 0.85rem; font-weight: 700; color: var(--accent); min-width: 20px; }
.action-text { font-size: 0.85rem; font-weight: 600; color: var(--fg); }
.action-freq { font-size: 0.75rem; color: var(--muted); margin-top: 2px; }
```

**Winnable-If Callout** (`.winnable-if`):
Optional one-line callout inside an action item, used where the evidence points to a single clean turning point. Not required on every item.
```html
<div class="action-item">
  <div class="action-rank">1</div>
  <div class="action-body">
    <div class="action-text">No standard pricing response when IT raised budget concerns in week 3</div>
    <div class="action-freq">Appeared in 6 of 9 losses (67%)</div>
    <div class="winnable-if"><strong>Winnable if:</strong> we had addressed price earlier with a TCO story.</div>
  </div>
</div>
```
```css
.winnable-if { font-size: 0.8rem; color: var(--fg); margin-top: 6px; padding-top: 6px; border-top: 1px dashed var(--border); }
.winnable-if strong { color: var(--accent); }
```

**No Decision / Stalled Group** (optional, gated on data):
Only render if loss-reason data distinguishes no-decision from competitor losses. Same `.usecase-card` and `.action-list` markup as other loss patterns, no new structure, just a grouping labeled "No Decision / Stalled" with engagement-signal diagnostics stated as volume + rate.
```html
<div class="usecase-card">
  <div class="usecase-header">
    <h4 class="usecase-name">No Decision / Stalled</h4>
    <span class="usecase-rate loss">22% of losses</span>
  </div>
  <div class="usecase-volume">7 deals (7 of 32 losses)</div>
  <ul class="h2h-pattern-list">
    <li>Avg 34 days between meetings vs. 12 days in won deals</li>
    <li>Single-threaded in 5 of 7 (71%) vs. 3.2 avg stakeholders engaged in wins</li>
    <li>Leadership change mid-cycle in 3 of 7 (43%)</li>
    <li>Budget reallocation or freeze cited in 2 of 7 (29%)</li>
  </ul>
  <div class="winnable-if"><strong>Winnable if:</strong> we'd multi-threaded past the single champion before Q4 budget lockup.</div>
</div>
```

**Objection Table** (`.obj-table`):
Table format for objections, sorted by loss correlation (highest loss rate first). Columns: Objection, Loss Rate, Frequency, Who Raises It, Counter.
```html
<table class="obj-table">
  <thead>
    <tr>
      <th>Objection</th>
      <th>Loss Rate</th>
      <th>Frequency</th>
      <th>Who Raises It</th>
      <th>Counter</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>"How is our data secured and who has access?"</td>
      <td><span class="loss-rate-badge">70%</span></td>
      <td>10 deals (7 lost, 3 won)</td>
      <td>IT Director, Enterprise</td>
      <td>Lead with SOC 2 Type II certification and HIPAA compliance before they ask...</td>
    </tr>
    <tr>
      <td>"We already have a process that works."</td>
      <td><span class="loss-rate-badge">55%</span></td>
      <td>11 deals (6 lost, 5 won)</td>
      <td>Managing Partner, Mid-Market</td>
      <td>Acknowledge their current process, then quantify hidden costs with benchmarks...</td>
    </tr>
  </tbody>
</table>
```
```css
.obj-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
.obj-table th { text-align: left; font-weight: 700; padding: 8px 10px; border-bottom: 2px solid var(--border); color: var(--muted); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em; }
.obj-table td { padding: 10px 10px; border-bottom: 1px solid var(--border); vertical-align: top; }
.loss-rate-badge { font-weight: 700; color: var(--chart-loss); }
```

**Head-to-Head Aggregate Patterns** (`.h2h-group` > `.h2h-patterns`):
Aggregate win/loss pattern columns per grouping (competitor, segment, or persona). Each grouping shows common patterns across all deals in that grouping as bulleted lists, NOT individual paired deal story cards.
```html
<div class="h2h-group">
  <h4 class="h2h-label">vs [Competitor A]</h4>
  <div class="h2h-patterns">
    <div class="h2h-pattern-col won">
      <div class="h2h-pattern-header">
        <span class="h2h-badge won">WON 20</span>
        Why we won
      </div>
      <ul class="h2h-pattern-list">
        <li>Champion drove internal business case with ROI proof showing paralegal time savings</li>
        <li>Ran live demo on prospect's own data during first call</li>
        <li>Engaged IT early to resolve security concerns before they became blockers</li>
      </ul>
    </div>
    <div class="h2h-pattern-col lost">
      <div class="h2h-pattern-header">
        <span class="h2h-badge lost">LOST 9</span>
        Why we lost
      </div>
      <ul class="h2h-pattern-list">
        <li>No standard pricing response when IT raised budget concerns in week 3</li>
        <li>Failed to identify and engage economic buyer before procurement review</li>
        <li>Trial period too short for prospect to validate accuracy on their case types</li>
      </ul>
    </div>
  </div>
</div>
```
```css
.h2h-patterns { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.h2h-pattern-col { padding: 16px; border-radius: var(--radius); border: 1px solid var(--border); }
.h2h-pattern-col.won { border-left: 3px solid var(--chart-win); }
.h2h-pattern-col.lost { border-left: 3px solid var(--chart-loss); }
.h2h-pattern-header { font-size: 0.78rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.h2h-badge { font-size: 0.7rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; }
.h2h-badge.won { background: var(--chart-win); color: #fff; }
.h2h-badge.lost { background: var(--chart-loss); color: #fff; }
.h2h-pattern-list { font-size: 0.82rem; padding-left: 18px; margin: 0; }
.h2h-pattern-list li { margin-bottom: 6px; line-height: 1.45; }
```

**Data Source List** (`.data-sources`):
Clean list with labels and values for the report's data provenance.

**Trend Indicators**:
`.trend-up` (green + up arrow), `.trend-down` (red + down arrow), `.trend-flat` (muted).

**Tags** (`.tag`):
Small pills used to attribute segments and personas to use cases, patterns, objections, and deals. Segment tags use accent color. Persona tags use purple. Both have `::before` pseudo-element prefixes for clarity.
```css
.tag { font-size: .72rem; font-weight: 600; padding: 3px 10px; border-radius: 999px; border: 1px solid var(--border); }
.tag.segment { border-color: var(--accent); color: var(--accent); }
.tag.segment::before { content: "Segment: "; }
.tag.persona { border-color: #8a68f2; color: #8a68f2; }
.tag.persona::before { content: "Persona: "; }
```
