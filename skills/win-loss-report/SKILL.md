---
name: win-loss-report
description: Generate visual win/loss analysis reports as self-contained HTML with CSS-based charts and data visualizations. Use when user says "win/loss report", "deal report", "visual analysis", or wants a formatted HTML version of deal outcome analysis. Do NOT use for text-based deal analysis — use /octave:wins-losses instead.
---

# /octave:win-loss-report - Visual Win/Loss Report Builder

Generate beautiful, self-contained HTML win/loss analysis reports powered by your Octave deal intelligence. Unlike `/octave:wins-losses` which outputs text-based analysis, this skill renders structured visual reports with CSS-based charts, progress indicators, comparison bars, and metric cards -- designed for leadership reviews, team retrospectives, and strategic planning.

Uses the same CSS variable / style preset system as `/octave:deck`.

## Usage

```
/octave:win-loss-report [--period <timeframe>] [--segment <filter>] [--competitor <name>] [--style <preset>]
```

## Examples

```
/octave:win-loss-report                                          # Last 90 days, all deals
/octave:win-loss-report --period "Q4 2025"                       # Specific quarter
/octave:win-loss-report --competitor "Gong"                      # Focused on deals vs Gong
/octave:win-loss-report --segment "enterprise"                   # Enterprise segment only
/octave:win-loss-report --period "last 6 months" --style paper-minimal
/octave:win-loss-report --period "2025" --competitor "Salesforce" --segment "mid-market"
```

## Instructions

When the user runs `/octave:win-loss-report`:

### Step 1: Define Scope

If not provided via flags, ask the user interactively:

**Period -- "What time range?"**

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

**Filter -- "Any specific focus?"**

```
Do you want to filter the analysis?

1. All deals -- full cross-deal analysis
2. Specific competitor -- focus on deals involving a competitor
3. Specific segment -- filter by market segment
4. Specific rep -- filter by sales rep
5. Custom filter -- describe what you want

Your choice:
```

If competitor or segment is selected, use `list_all_entities` to show available options:

```
# For competitor filter
list_all_entities({ entityType: "competitor" })

# For segment filter
list_all_entities({ entityType: "segment" })
```

**Depth -- "How detailed?"**

```
What level of detail?

1. Executive summary -- 1-page overview with key metrics and takeaways
2. Full report -- detailed analysis with all sections and drill-downs

Your choice:
```

| Depth | Sections Included | Best For |
|-------|-------------------|----------|
| Executive summary | Header, Summary, Win Rate, Win Patterns (condensed), Loss Patterns (condensed), Recommendations | Board updates, weekly stand-ups |
| Full report | All 12 sections | QBRs, strategy sessions, enablement |

### Step 2: Octave Data Gathering

Based on scope, use Octave MCP tools to gather comprehensive deal intelligence. **Always tell the user what you're researching and why.**

**Call as many tools as needed to build a complete picture.** Win/loss reports are only as good as the data behind them. Layer multiple data sources -- deal outcomes + conversation findings + library context -- to produce analysis grounded in real evidence, not speculation.

**List vs Search -- when to use which:**

| Tool | Purpose | Use when... |
|------|---------|-------------|
| `list_all_entities({ entityType })` | Fetch all entities of a type (minimal fields) | You want a quick inventory -- "show me all competitors" |
| `list_entities({ entityType })` | Fetch entities with full data (paginated) | You need actual content -- "get full persona details" |
| `get_entity({ oId })` | Deep dive on one specific entity | You found something notable and need the complete picture |
| `search_knowledge_base({ query })` | Semantic search across library + resources | You have a concept -- "how do we position against price objections?" |
| `list_resources()` / `search_resources({ query })` | Uploaded docs, URLs, Google Drive files | You need CRM exports, uploaded deal data, or reference docs |

**Rule of thumb:** Use `list_*` when you know *what type* of thing you want. Use `search_*` when you know *what topic* you're looking for.

---

#### Core Deal Data (Always Required)

| What you need | Tool | When to use |
|---------------|------|-------------|
| Won deals | `list_events({ filters: { eventTypes: ["DEAL_WON"] }, startDate, endDate })` | Always -- core data |
| Lost deals | `list_events({ filters: { eventTypes: ["DEAL_LOST"] }, startDate, endDate })` | Always -- core data |
| Pipeline context | `list_events({ filters: { eventTypes: ["DEAL_CREATED"] }, startDate, endDate })` | When you need total pipeline for win rate calculation |
| Notable deal details | `get_event_detail({ eventOId })` | Deep dive on 3-5 notable wins and 3-5 notable losses |

---

#### Conversation Intelligence (Findings)

| What you need | Tool | When to use |
|---------------|------|-------------|
| Objections in won deals | `list_findings({ opportunityStatus: ["WON"], extractionTypes: ["CALL_EXTERNAL_OBJECTIONS"], startDate })` | Objections that were overcome |
| Objections in lost deals | `list_findings({ opportunityStatus: ["LOST"], extractionTypes: ["CALL_EXTERNAL_OBJECTIONS"], startDate })` | Objections that killed deals |
| Value props presented | `list_findings({ extractionTypes: ["CALL_INTERNAL_VALUE_PROP_PRESENTATIONS"], startDate })` | What messaging worked vs didn't |
| Competitor mentions | `list_findings({ extractionTypes: ["CALL_EXTERNAL_COMPETITORS_TO_OUR_OFFERING"], startDate })` | Competitive landscape in deals |
| Feature requests | `list_findings({ extractionTypes: ["CALL_EXTERNAL_FEATURE_REQUESTS"], startDate })` | Product gaps causing losses |
| Proof points cited | `list_findings({ extractionTypes: ["CALL_INTERNAL_PROOF_POINTS"], startDate })` | Social proof effectiveness |

---

#### Library Context (Enrichment)

| What you need | Tool | When to use |
|---------------|------|-------------|
| All competitors | `list_all_entities({ entityType: "competitor" })` | Quick inventory for breakdown charts |
| Competitor details | `get_entity({ oId })` | Deep dive when a competitor dominates losses |
| All segments | `list_all_entities({ entityType: "segment" })` | Segment breakdown analysis |
| All personas | `list_all_entities({ entityType: "persona" })` | Persona win rate analysis |
| Proof points | `list_entities({ entityType: "proof_point" })` | Evidence for "what's working" section |
| Playbook strategies | `search_knowledge_base({ query: "win loss competitive positioning" })` | Recommendations grounded in existing playbooks |
| Uploaded deal data | `search_resources({ query: "deal data CRM export" })` | Supplementary deal data from uploaded files |

---

#### Competitor-Focused Data (When --competitor is specified)

| What you need | Tool | When to use |
|---------------|------|-------------|
| Competitor profile | `get_entity({ oId })` | Full competitor context |
| Deals vs competitor | `list_events({ filters: { eventTypes: ["DEAL_WON", "DEAL_LOST"], competitors: ["<oId>"] } })` | Win/loss record against this competitor |
| Findings mentioning competitor | `list_findings({ entityMatches: { competitorOIds: ["<oId>"] }, startDate })` | Real objections and mentions from calls |
| Competitive positioning | `search_knowledge_base({ query: "<competitor> differentiation", entityTypes: ["playbook", "competitor"] })` | Existing positioning guidance |

---

**Output of this step:** Present a report outline to the user for approval before generating.

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

**Wait for user approval before proceeding.**

### Step 3: Style Selection

Reports default to clean, data-focused light themes. Ask the user:

```
Which style for the report?

LIGHT THEMES (recommended for reports)
  1. paper-minimal     -- Off-white + black type. Editorial simplicity. (default)
  2. soft-light        -- Warm white + sage green. Calm and approachable.
  3. swiss-modern      -- White + red accent. Bauhaus minimal.

DARK THEMES
  4. midnight-pro      -- Dark navy, white text, blue accents.
  5. executive-dark    -- Charcoal + gold. Premium boardroom.
  6. octave-brand      -- Octave purple on dark navy.

Or provide a number/name from the full preset list (12 options in STYLE_PRESETS.md).

Your choice (default: paper-minimal):
```

Full CSS variable definitions for each preset are in [STYLE_PRESETS.md](../deck/STYLE_PRESETS.md).

### Step 4: Generate HTML

Build a single, self-contained HTML file. **No external dependencies except Google Fonts.** Everything else inlined.

#### Output Directory

Reports go under `.octave-reports/`:

```
.octave-reports/
└── win-loss-<YYYY-MM-DD>/
    └── win-loss-report.html
```

Example: `/octave:win-loss-report --period "Q4 2025"` produces `.octave-reports/win-loss-2026-02-11/win-loss-report.html`

The `.octave-reports/` directory is in `.gitignore` -- nothing here gets committed.

#### HTML Architecture

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

#### Report Sections (Full Report)

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

**Section 12: Data Sources**
- Data used, deal count, date range, filters applied
- Caveats and methodology notes

#### Executive Summary Report (Condensed)

When the user selects "Executive Summary" depth, generate only:

1. Header (Section 1)
2. Executive Summary (Section 2)
3. Win Rate Overview (Section 3)
4. Win Pattern Analysis -- condensed to top 3, no evidence quotes (Section 7)
5. Loss Pattern Analysis -- condensed to top 3, no evidence quotes (Section 8)
6. Recommendations (Section 11)

Single-column layout, no sidebar navigation. Target a single printable page.

### Step 5: Delivery

After generating the HTML file:

1. **Open the report** in the default browser
2. **Present a summary:**

```
REPORT READY
=============

File:    .octave-reports/win-loss-<date>/win-loss-report.html
Period:  [Date range]
Deals:   [N] won, [N] lost ([N]% win rate)
Style:   [Preset name]
Depth:   [Executive Summary / Full Report]

Key Findings:
- Win rate: [N]% ([trend vs previous period])
- Top win factor: [Factor] ([N]% of wins)
- Top loss factor: [Factor] ([N]% of losses)
- Biggest competitor threat: [Competitor] ([N] losses)

Navigation:
- Scroll to navigate between sections
- Sidebar dots show your position
- Print-friendly (Cmd+P / Ctrl+P for PDF export)

---

Want me to:
1. Drill into a specific competitor
2. Drill into a specific segment
3. Expand the time period
4. Add more detail to any section
5. Generate an executive summary version (or full version)
6. Export as PDF (print dialog)
7. Done
```

## MCP Tools Used

### Deal Intelligence
- `list_events` - Filter by DEAL_WON, DEAL_LOST, DEAL_CREATED for deal outcomes and pipeline
- `get_event_detail` - Deep dive on notable wins and losses for deal stories

### Conversation Intelligence
- `list_findings` - Objections, value prop presentations, competitor mentions, feature requests, proof points cited in calls

### Library Context
- `list_all_entities` - Quick inventory of competitors, segments, personas
- `list_entities` - Full entity data for proof points, references
- `get_entity` - Deep dive on specific competitors, personas
- `search_knowledge_base` - Semantic search for playbook strategies, positioning
- `search_resources` - Uploaded CRM exports, deal data files

## Error Handling

**No Deal Data in Period:**
> No won or lost deals found for [period].
>
> This could mean:
> 1. CRM integration isn't syncing deal outcomes
> 2. The date range has no closed deals
> 3. Filters are too restrictive
>
> Try:
> 1. Expand the date range
> 2. Remove filters (competitor, segment)
> 3. Check your Octave CRM integration settings

**Insufficient Data (Fewer Than 5 Deals):**
> Only [N] deals found for [period]. Win/loss analysis is most useful with 5+ deals.
>
> Options:
> 1. Proceed anyway -- I'll generate the report with available data (patterns may be unreliable)
> 2. Expand the time period to capture more deals
> 3. Remove filters to include all segments/competitors

**No Findings Data:**
> Deal outcomes found, but no conversation findings available.
>
> The report will include deal metrics and outcomes but won't have:
> - Evidence quotes from calls
> - Objection analysis
> - Value prop effectiveness
>
> For richer analysis, ensure calls are being recorded and findings extraction is enabled in Octave.

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The win/loss report requires deal data from Octave. Check your MCP configuration or run `/octave:workspace status`.

**Missing Competitor/Segment Data:**
> I couldn't find a competitor named "[name]" in your library.
>
> Available competitors:
> - [List from list_all_entities]
>
> Pick one from the list, or proceed with "all deals" and I'll break down by competitor automatically.

## Related Skills

- `/octave:wins-losses` - Text-based win/loss analysis (this is the visual version)
- `/octave:insights` - Conversation intelligence analysis (conversational format)
- `/octave:battlecard-doc` - Competitive deep-dive (when patterns point to a specific competitor)
- `/octave:pipeline` - Current pipeline coaching and deal strategy
- `/octave:deck` - Present win/loss findings to leadership as a slide deck
