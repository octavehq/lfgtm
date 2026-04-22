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

See [tool-reference.md](references/tool-reference.md) for list-vs-search guidance and the tool reference tables for core deal data, conversation intelligence, library context, and competitor-focused data.

**Output of this step:** Present a report outline to the user for approval before generating. See [outline-template.md](references/outline-template.md) for the outline template.

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

See [html-architecture.md](references/html-architecture.md) for the HTML architecture, structural requirements, and the CSS component system (metric cards, win rate ring, bar charts, progress bars, takeaway cards, pattern cards, deal cards, recommendation cards, data tables, trend indicators).

#### Report Sections (Full Report)

See [sections.md](references/sections.md) for the full 12-section report breakdown and the condensed executive summary variant.

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
