# HTML Win/Loss Report (--format report)

How to render the win/loss analysis as a self-contained visual HTML report with CSS-based charts — designed for leadership reviews, team retrospectives, and strategic planning. The analysis itself comes from the same research and pattern work as the text format; this file covers the report-specific intake, structure, and scaffold. The chart component system lives in [report-charts.md](report-charts.md).

## Scope Intake

If not provided via flags, ask interactively:

**Period — "What time range?"**

```
What time range should this report cover?

1. Last 30 days
2. Last 60 days
3. Last 90 days (default)
4. Last 6 months
5. Specific quarter (e.g., Q4 2025)
6. Custom date range

Your choice:
```

**Filter — "Any specific focus?"**

```
Do you want to filter the analysis?

1. All deals — full cross-deal analysis
2. Specific competitor — focus on deals involving a competitor
3. Specific segment — filter by market segment
4. Specific rep — filter by sales rep
5. Custom filter — describe what you want

Your choice:
```

If competitor or segment is selected, use `list_all_entities({ entityType: "competitor" })` or `list_all_entities({ entityType: "segment" })` to show available options.

**Depth — "How detailed?"**

```
What level of detail?

1. Executive summary — 1-page overview with key metrics and takeaways
2. Full report — detailed analysis with all sections and drill-downs

Your choice:
```

| Depth | Sections Included | Best For |
|-------|-------------------|----------|
| Executive summary | Header, Summary, Win Rate, Win Patterns (condensed), Loss Patterns (condensed), Recommendations | Board updates, weekly stand-ups |
| Full report | All 12 sections | QBRs, strategy sessions, enablement |

## Outline Template

Present after data gathering and **wait for user approval** before generating:

```
REPORT OUTLINE: Win/Loss Report
================================

Period: [Date range]
Scope: [All deals / Competitor: X / Segment: Y]
Depth: [Executive Summary / Full Report]

Data Gathered:
- Won deals: [N] ($[total])
- Lost deals: [N] ($[total])
- Findings analyzed: [N]
- Competitors identified: [list]
- Segments covered: [list]

---

PLANNED SECTIONS
-----------------

1. Header & Report Metadata
2. Executive Summary (4-5 key takeaways)
3. Win Rate Overview (headline metric + visual)
4. Win/Loss by Competitor (horizontal bar chart)
5. Win/Loss by Segment (horizontal bar chart)
6. Win/Loss by Persona (breakdown chart)
7. Win Pattern Analysis (top themes + evidence)
8. Loss Pattern Analysis (top themes + evidence)
9. Objection Analysis (frequency + correlation)
10. Notable Deals (3-5 spotlighted stories)
11. Recommendations (3-5 actionable items)
12. Data Sources & Methodology

---

Does this look good? I can:
1. Proceed to style selection and generation
2. Add/remove sections
3. Expand a specific area
4. Adjust the scope or period
```

## HTML Architecture

Multi-section scrollable report. Key structural requirements:

- **Max-width 900px** centered container
- **Sticky sidebar** with section navigation dots (fixed left, vertically centered)
- **CSS variables** from the chosen preset (see `../../shared/style-presets.md`) or brand kit tokens, plus the chart variables defined in [report-charts.md](report-charts.md)
- **All font sizes use `clamp()`** — responsive to viewport
- **Self-contained HTML**, inline CSS (except Google Fonts link)
- **Print-friendly** — CSS charts print well since they're just styled divs. Include `@media print` rules to hide navigation, set `print-color-adjust: exact`, and `page-break-inside: avoid` on sections.
- **Responsive** — `@media (max-width: 768px)` collapses grids to single column, hides sidebar nav

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
    /* Component classes from report-charts.md */
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

## Report Sections (Full Report)

Generate all 12 sections in order:

**Section 1: Header**
- Report title: "Win/Loss Report"
- Period displayed as human-readable range
- Scope badge (`.pill` with filter description)
- Generation date and deal count

**Section 2: Executive Summary**
- 4-5 takeaway cards in a responsive grid
- Each card: one key finding with supporting number
- Use `.win`, `.loss`, `.neutral` border color modifiers

**Section 3: Win Rate Overview**
- Large win rate ring (conic-gradient, no JS) + metric cards grid
- Metrics: deals won, deals lost, total pipeline, average deal size
- Trend indicator vs previous period if data available

**Section 4: Win/Loss by Competitor**
- Horizontal stacked bar chart
- Each competitor: green (wins) + red (losses) bars with win rate percentage
- Sorted by total deal volume

**Section 5: Win/Loss by Segment**
- Same bar chart treatment broken by segment
- Sorted by total deals

**Section 6: Win/Loss by Persona**
- Bar chart showing win/loss by buyer persona
- Highlight personas with notably high or low win rates

**Section 7: Win Pattern Analysis**
- Top 3-5 win themes as pattern cards
- Each: rank, title, frequency ("8 of 12 wins"), progress bar, evidence quotes from calls
- Framing: "When we win, it's because..."

**Section 8: Loss Pattern Analysis**
- Top 3-5 loss themes as pattern cards
- Same structure as win patterns with evidence quotes
- Framing: "When we lose, it's because..."

**Section 9: Objection Analysis**
- Data table: objection, frequency, win rate when raised, revenue impact
- Sorted by frequency descending

**Section 10: Notable Deals**
- 3-5 deal spotlight cards (mix of wins and losses)
- Each: company name, status badge, deal size, key narrative, lessons learned

**Section 11: Recommendations**
- 3-5 actionable recommendations as numbered cards
- Each: title, rationale grounded in report data, suggested action
- Mirror these in the conversation and offer to apply library updates (Step 6 of the skill)

**Section 12: Data Sources**
- Data used, deal count, date range, filters applied
- Caveats and methodology notes

## Executive Summary Report (Condensed)

When the user selects "Executive Summary" depth, generate only:

1. Header (Section 1)
2. Executive Summary (Section 2)
3. Win Rate Overview (Section 3)
4. Win Pattern Analysis — condensed to top 3, no evidence quotes (Section 7)
5. Loss Pattern Analysis — condensed to top 3, no evidence quotes (Section 8)
6. Recommendations (Section 11)

Single-column layout, no sidebar navigation. Target a single printable page.

## Delivery Summary Template

```
REPORT READY
=============

File:    .octave-reports/win-loss-<date>/win-loss-report.html
Period:  [Date range]
Deals:   [N] won, [N] lost ([N]% win rate)
Style:   [Preset or brand kit name]
Depth:   [Executive Summary / Full Report]

Key Findings:
- Win rate: [N]% ([trend vs previous period])
- Top win factor: [Factor] ([N]% of wins)
- Top loss factor: [Factor] ([N]% of losses)
- Biggest competitor threat: [Competitor] ([N] losses)

Navigation:
- Scroll to navigate between sections
- Sidebar dots show your position

---

Want me to:
1. Drill into a specific competitor
2. Drill into a specific segment
3. Expand the time period
4. Add more detail to any section
5. Generate an executive summary version (or full version)
6. Apply the recommendations to the library
7. Export as PDF
8. Done
```
