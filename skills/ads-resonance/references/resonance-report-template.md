# Resonance Report HTML Template

After the resonance loop generates its resonance map, library update recommendations, sales intelligence brief, and next-campaign recommendations (Steps 6B–6E), offer to produce a self-contained HTML report that makes the findings scannable and shareable.

This is the visual analog of what `html-deck-template.md` does for campaign plans. The same aesthetic principles apply: self-contained HTML, print-friendly, sticky navigation, color-coded sections, no external assets except Google Fonts.

## When to generate

Offer as a follow-up action after the resonance loop completes, alongside the existing options in Step 5. A natural prompt:

```
AskUserQuestion({
  questions: [{
    question: "How would you like to receive the resonance loop output?",
    header: "Output format",
    options: [
      { label: "Keep as chat markdown", description: "Tables and text in this conversation — best for quick review and follow-up questions" },
      { label: "Generate HTML report", description: "A self-contained HTML file you can open in your browser, print, share, or archive" },
      { label: "Both", description: "Keep the chat markdown for iteration AND generate the HTML report" }
    ],
    multiSelect: false
  }]
})
```

If the user picks "HTML report" or "Both", generate the file per the template below.

## File output

Save to `~/Desktop/resonance-report-<workspace-slug>-<YYYY-MM-DD>.html`. Tell the user the path and say they can open it with `open` (macOS) or double-click.

## Required sections (in order)

1. **Header band** — workspace name, data window dates, spend total, mode (smoke-test / ad-group / ad / full-resonance), data source (MCP / BigQuery / Direct API / Manual), and a single-line summary of the loop's most actionable finding.

2. **Sticky nav** — anchor links to: Summary, Resonance Map, Library Updates, Sales Brief, Next Campaign, Prediction Outcomes, New Predictions.

3. **Summary cards** — 4-6 large cards showing the headline metrics for the window: total impressions, total clicks, CTR, conversions, spend, CPA (or "N/A — not enough conversions"). Color-code each card based on the confidence the spend tier supports.

4. **Resonance Map section** — the table from Step 6B, with ad groups (or ads, in ad mode) ranked by the primary metric. Use a heatmap for CTR and CPC columns. Highlight the biggest CPC gap finding in a callout box above the table.

5. **Library Update Recommendations section** — each recommendation as a card with: entity type, field, current value, recommended value, evidence, confidence tier. Include an "Apply" button placeholder (the HTML is static — the button exists to show users what actions are available, but clicking it just copies the recommendation text to clipboard).

6. **Sales Intelligence Brief section** — two subsections: "Winning messages" and "Messages that didn't land." Each message in a card with the supporting metric and suggested sales use.

7. **Next Campaign Recommendations section** — three subsections (Double Down, Test Next, Retire). Each recommendation as a bullet with its evidence.

8. **Previous Prediction Outcomes section** — the track record panel from Step 6F.2. Each resolved prediction as a card with: claim, status (color-coded), evaluated-against data, notes. Tentative predictions get a clear visual indicator (diagonal stripes or a "TENTATIVE" banner).

9. **New Predictions section** — the 3-6 new prediction cards generated in Step 6F.3. Each as a card with: claim, type, confidence, evaluation window, confirm/refute conditions, next evaluation date.

10. **Calibration panel** — the self-tuning summary: total predictions, hit rate by type, lessons learned. A small line chart showing hit rate trajectory over time if 3+ prior runs exist.

## Visual design

- **Typography**: Inter for body, JetBrains Mono for numbers/metrics (both from Google Fonts)
- **Color palette**:
  - Background: `#FAFAF9` (warm off-white)
  - Text: `#0A0A0A`
  - Primary accent: `#0F52BA` (confident blue)
  - CONFIRMED: `#16A34A` (green)
  - REFUTED: `#DC2626` (red)
  - INCONCLUSIVE_FAVORABLE: `#84CC16` (lime — "leaning good")
  - INCONCLUSIVE_UNFAVORABLE: `#F59E0B` (amber — "leaning bad")
  - PENDING: `#6B7280` (gray)
  - TENTATIVE indicator: `#8B5CF6` (purple) with a subtle diagonal stripe pattern
- **Heatmap for metric tables**: green for strong, yellow for average, red for weak, using relative ranking within the table
- **Cards**: 1px border `#E5E7EB`, 8px border-radius, 16px padding, subtle box-shadow on hover
- **Print CSS**: `@media print` hides the sticky nav, converts cards to page-break-inside: avoid, black-on-white colors for everything

## Scaffolding to copy

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Resonance Report — {workspace} — {window}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #FAFAF9; --text: #0A0A0A; --muted: #6B7280; --border: #E5E7EB;
    --primary: #0F52BA;
    --confirmed: #16A34A; --refuted: #DC2626;
    --incl-fav: #84CC16; --incl-unfav: #F59E0B;
    --pending: #6B7280; --tentative: #8B5CF6;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; padding: 0; }
  .metric { font-family: 'JetBrains Mono', monospace; font-variant-numeric: tabular-nums; }
  header.report-header { background: white; border-bottom: 1px solid var(--border); padding: 32px 48px; position: sticky; top: 0; z-index: 100; }
  header.report-header h1 { font-size: 24px; font-weight: 700; margin-bottom: 4px; }
  header.report-header .meta { color: var(--muted); font-size: 14px; }
  nav.sticky-nav { background: white; border-bottom: 1px solid var(--border); padding: 12px 48px; display: flex; gap: 24px; position: sticky; top: 89px; z-index: 99; overflow-x: auto; }
  nav.sticky-nav a { color: var(--text); text-decoration: none; font-size: 14px; font-weight: 500; white-space: nowrap; }
  nav.sticky-nav a:hover { color: var(--primary); }
  main { max-width: 1200px; margin: 0 auto; padding: 48px; }
  section { margin-bottom: 64px; }
  section h2 { font-size: 20px; font-weight: 600; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid var(--primary); }
  .summary-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 32px; }
  .summary-card { background: white; border: 1px solid var(--border); border-radius: 8px; padding: 20px; }
  .summary-card .label { font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; }
  .summary-card .value { font-family: 'JetBrains Mono', monospace; font-size: 28px; font-weight: 700; margin-top: 8px; }
  .callout { background: #FEF3C7; border-left: 4px solid var(--incl-unfav); padding: 16px 20px; border-radius: 4px; margin-bottom: 24px; }
  .callout strong { color: #92400E; }
  table.resonance { width: 100%; border-collapse: collapse; font-size: 14px; background: white; border-radius: 8px; overflow: hidden; }
  table.resonance th, table.resonance td { padding: 12px 16px; text-align: left; border-bottom: 1px solid var(--border); }
  table.resonance th { background: #F9FAFB; font-weight: 600; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; color: var(--muted); }
  table.resonance td.num { font-family: 'JetBrains Mono', monospace; text-align: right; }
  .prediction-card { background: white; border: 1px solid var(--border); border-left-width: 4px; border-radius: 8px; padding: 20px; margin-bottom: 16px; }
  .prediction-card.confirmed { border-left-color: var(--confirmed); }
  .prediction-card.refuted { border-left-color: var(--refuted); }
  .prediction-card.incl-fav { border-left-color: var(--incl-fav); }
  .prediction-card.incl-unfav { border-left-color: var(--incl-unfav); }
  .prediction-card.pending { border-left-color: var(--pending); }
  .prediction-card.tentative::before {
    content: "TENTATIVE"; display: inline-block; background: var(--tentative); color: white;
    font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px; margin-bottom: 8px; letter-spacing: 0.5px;
  }
  .prediction-card .claim { font-weight: 600; margin-bottom: 8px; }
  .prediction-card .meta { font-size: 12px; color: var(--muted); display: flex; gap: 16px; margin-bottom: 8px; }
  .prediction-card .notes { font-size: 14px; color: var(--text); }
  footer { text-align: center; padding: 48px; color: var(--muted); font-size: 12px; border-top: 1px solid var(--border); }
  @media print {
    header.report-header, nav.sticky-nav { position: static; }
    section { page-break-inside: avoid; }
    .summary-card, .prediction-card { break-inside: avoid; box-shadow: none; }
    body { background: white; color: black; }
  }
</style>
</head>
<body>

<header class="report-header">
  <h1>Resonance Report — {workspace}</h1>
  <div class="meta">{data window} · Mode: {mode} · Source: {data source} · Spend: <span class="metric">${total spend}</span></div>
</header>

<nav class="sticky-nav">
  <a href="#summary">Summary</a>
  <a href="#resonance-map">Resonance Map</a>
  <a href="#library-updates">Library Updates</a>
  <a href="#sales-brief">Sales Brief</a>
  <a href="#next-campaign">Next Campaign</a>
  <a href="#prediction-outcomes">Prediction Outcomes</a>
  <a href="#new-predictions">New Predictions</a>
  <a href="#calibration">Calibration</a>
</nav>

<main>

<section id="summary">
  <h2>Summary</h2>
  <div class="summary-cards">
    <div class="summary-card"><div class="label">Impressions</div><div class="value">{total}</div></div>
    <div class="summary-card"><div class="label">Clicks</div><div class="value">{total}</div></div>
    <div class="summary-card"><div class="label">CTR</div><div class="value">{%}</div></div>
    <div class="summary-card"><div class="label">Conversions</div><div class="value">{total}</div></div>
    <div class="summary-card"><div class="label">Cost</div><div class="value">${total}</div></div>
    <div class="summary-card"><div class="label">CPA</div><div class="value">{$ or N/A}</div></div>
  </div>
  <p>{One-sentence headline finding — e.g., "The primary actionable finding is a 5x CPC gap between two ad groups targeting similar personas — pause or rework the expensive one."}</p>
</section>

<section id="resonance-map">
  <h2>Resonance Map</h2>
  <div class="callout">
    <strong>Key finding:</strong> {lead with the single biggest actionable insight from the data}
  </div>
  <table class="resonance">
    <thead><tr><th>Unit</th><th>Impr</th><th>Clicks</th><th>CTR</th><th>Conv</th><th>Cost</th><th>CPC</th><th>Confidence</th></tr></thead>
    <tbody>
      <!-- one row per ad group (in ad-group mode) or ad (in ad mode) -->
    </tbody>
  </table>
</section>

<!-- Library Updates, Sales Brief, Next Campaign sections follow the same pattern -->

<section id="prediction-outcomes">
  <h2>Previous Predictions Evaluated</h2>
  <!-- One .prediction-card per resolved prediction, with class for status and optional .tentative class -->
</section>

<section id="new-predictions">
  <h2>New Predictions Generated</h2>
  <!-- One .prediction-card.pending per new prediction -->
</section>

<section id="calibration">
  <h2>Calibration Track Record</h2>
  <!-- Table of hit rates by type + the lessons array -->
</section>

</main>

<footer>
  Generated by /octave:ads resonance · {timestamp} · Data source: {source}
</footer>

</body>
</html>
```

## Implementation notes

- The generator is Claude, not a templating engine. Fill in the placeholders by string substitution after generating the resonance map, library updates, etc.
- The HTML is self-contained: no external CSS files, no JavaScript, no images. Only Google Fonts via CDN.
- For the heatmap in the metric tables, compute relative ranks across the column and apply inline `background-color` via `hsl(120, 60%, X%)` where X varies by rank (120 hue = green).
- For the calibration trajectory chart, use inline SVG — ~50 lines of `<polyline>` and `<circle>` elements. Don't pull in Chart.js or D3.
- The "TENTATIVE" banner uses a `::before` pseudo-element, not a separate DOM node, so it can't be accidentally stripped by the user's markdown copy.
- Test the output locally before handing it over: `open ~/Desktop/resonance-report-*.html` and visually verify sections are readable and the color coding makes sense.
