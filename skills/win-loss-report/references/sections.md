# Sections (Full Report)

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
