---
name: wins-losses
description: Analyze won and lost deals for win/loss patterns, insights, and actionable learnings — as inline text analysis or a visual HTML report with CSS charts. Use when user says "win/loss analysis", "win/loss report", "why did we lose", "win themes", "deal report", or asks about deal outcome trends. Do NOT use for aggregate conversation trends unrelated to deal outcomes — use /octave:insights instead.
argument-hint: "[--status won|lost|both] [--period <range>] [--competitor <name>] [--segment <name>] [--company <domain>] [--format text|report] [--style <preset>]"
---

# /octave:wins-losses - Deal Intelligence

Analyze your won and lost deals to understand what's working, why you're losing, and how to improve win rates. Surface patterns, competitor intelligence, and actionable recommendations.

One analysis pipeline, two output formats:
- **Text (default)** — inline analysis for working sessions, drill-downs, and applying library updates as you go.
- **Report (`--format report`)** — a self-contained visual HTML report with CSS-based charts, progress indicators, comparison bars, and metric cards — built for leadership reviews, team retrospectives, and strategic planning.

## Usage

```
/octave:wins-losses [--status won|lost|both] [--period <time-range>] [--format text|report]
```

## Options

- `--status <status>` - Focus on won, lost, or both (default: both)
- `--period <range>` - Time range (month, quarter, year, custom)
- `--competitor <name>` - Filter by competitor involvement
- `--segment <name>` - Filter by segment
- `--min-amount <amount>` - Minimum deal size
- `--company <domain>` - Analyze specific deal
- `--format text|report` - Inline text analysis (default) or visual HTML report
- `--style <preset>` - Style preset for the HTML report

## Examples

```
/octave:wins-losses                                  # Overview of recent wins/losses
/octave:wins-losses --status lost --period quarter   # Lost deals this quarter
/octave:wins-losses --competitor "Salesforce"        # Deals involving Salesforce
/octave:wins-losses --segment "Enterprise"           # Enterprise deals analysis
/octave:wins-losses --company acme.com               # Deep dive on Acme deal
/octave:wins-losses --format report --period "Q4 2025"        # Visual HTML report
/octave:wins-losses --format report --competitor "Acme" --style paper-minimal
```

## Instructions

When the user runs `/octave:wins-losses`:

### Step 1: Determine Focus and Format

If no options provided, show overview:

```
What would you like to analyze?

1. Full Analysis - Compare wins and losses
2. Win Analysis - What's working, why we win
3. Loss Analysis - Why we're losing, patterns
4. Competitor Analysis - Win/loss by competitor
5. Deal Deep Dive - Analyze specific deal

Your choice:
```

**Output format.** Default is text. Switch to the HTML report when the user passes `--format report` or asks for a "win/loss report", "deal report", or something visual for leadership. The report format covers the full analysis, win analysis, loss analysis, and competitor analysis; the deal deep dive is text-first — offer to spotlight the deal inside a full report if the user wants a document.

### Step 2: Query Deal Data

Call shapes: `list_events` takes event-type and entity filters inside `filters`; `list_findings` requires a natural-language `query` and takes the same filters inside `eventFilters`. The single full tool table — core deal data, conversation intelligence, library context, competitor-focused, and deep-dive queries — is in [tool-reference.md](references/tool-reference.md).

**For Overview:**
```
# Get won deals
list_events({
  startDate: "<period start>",
  endDate: "<today>",
  filters: { eventTypes: ["DEAL_WON"] },
  limit: 50
})

# Get lost deals
list_events({
  startDate: "<period start>",
  endDate: "<today>",
  filters: { eventTypes: ["DEAL_LOST"] },
  limit: 50
})

# Get findings from won deals
list_findings({
  query: "objections raised, value props presented, proof points cited, competitors mentioned",
  startDate: "<period start>",
  endDate: "<today>",
  eventFilters: { outcomeFilters: ["WON"] },
  limit: 100
})

# Get findings from lost deals
list_findings({
  query: "objections raised, value props presented, competitors mentioned, loss reasons",
  startDate: "<period start>",
  endDate: "<today>",
  eventFilters: { outcomeFilters: ["LOST"] },
  limit: 100
})
```

**For Competitor Analysis:**
```
list_findings({
  query: "<competitor name> mentions, comparisons, and competitive objections",
  startDate: "<period start>",
  endDate: "<today>",
  eventFilters: {
    competitors: ["<competitor_oId>"]
  }
})
```

**For Deal Deep Dive:**
```
list_events({
  startDate: "<lookback>",
  filters: {
    eventTypes: ["DEAL_WON", "DEAL_LOST", "CALL_TRANSCRIPT", "EMAIL_SENT", "EMAIL_REPLY_RECEIVED"],
    companyDomains: ["<domain>"]
  }
})

list_findings({
  query: "objections, pain points, decision criteria, competitors, commitments",
  eventFilters: {
    companyDomains: ["<domain>"]
  }
})

get_event_detail({
  eventOId: "<event_oId>",
  includeTranscript: true
})
```

### Step 3: Analyze Patterns

Bucket the returned findings yourself — group by theme (objection types, value props, competitors, loss reasons), then compare the won-deal buckets against the lost-deal buckets. For each theme, track: frequency in wins vs losses, associated deal value, and representative quotes. This won/lost contrast is the core of the analysis; supplement with `get_event_detail` on the 3-5 most instructive deals.

### Step 4: Present Analysis (text format)

---

#### Full Win/Loss Analysis

See [full-win-loss-report.md](references/full-win-loss-report.md) for the full win/loss analysis template.

---

#### Loss Analysis (--status lost)

See [loss-analysis.md](references/loss-analysis.md) for the loss analysis template.

---

#### Deal Deep Dive (--company)

See [deal-deep-dive.md](references/deal-deep-dive.md) for the deal deep dive template.

### Step 5: Report Format (--format report)

When the format is `report`, run the same data gathering and pattern analysis (Steps 2-3), then:

1. **Scope intake + outline approval.** Confirm period, filters, and depth (executive summary vs full report), then present the report outline and **wait for user approval**. See [html-report.md](references/html-report.md) for the intake prompts, outline template, and all 12 section specs.
2. **Brand styling.** This is an internal report, so default to **your own company's** brand kit if one exists; follow [../shared/brand-kit-usage.md](../shared/brand-kit-usage.md) for kit lookup, offer, and fallback.
3. **Style selection.** If no kit is used, pick a preset from [../shared/style-presets.md](../shared/style-presets.md). Clean light presets (`paper-minimal`, `soft-light`) suit data-heavy reports; skip the prompt if `--style` was provided.
4. **Generate HTML.** Build a single self-contained file per [html-report.md](references/html-report.md), using the pure-CSS chart components in [report-charts.md](references/report-charts.md) — no external dependencies except Google Fonts. Save under:
   ```
   .octave-reports/
   └── win-loss-<YYYY-MM-DD>/
       └── win-loss-report.html
   ```
   The `.octave-reports/` directory is gitignored — nothing here gets committed.
5. **Review pass (runs by default).** Follow [../shared/review-pass.md](../shared/review-pass.md): the preflight always runs; the visual pass runs unless the user opts out with `--skip-review` or "skip review". Tell the user at intake that you'll review before finishing.
6. **Delivery.** Open the report in the default browser and present the summary from [html-report.md](references/html-report.md). For PDF export, run the plugin's export helper: `bash "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/export-pdf.sh <path-to-html>` — or Cmd+P / Ctrl+P → Save as PDF.

Step 6 (recommendations and library updates) applies to both formats — after delivering a report, offer to apply its recommendations to the library in the conversation.

### Step 6: Generate Recommendations

Based on analysis, offer actionable next steps:

```
Based on this analysis, I recommend:

IMMEDIATE ACTIONS
-----------------
1. Create Competitor A TCO battlecard section
   → /octave:battlecard --competitor "Competitor A"

2. Update Motion ICP discovery guidance with budget qualification
   → update_motion_playbook with new methodology/objection content for the relevant Motion ICP cell

3. Review current pipeline for similar patterns
   → /octave:research --for pipeline-review

STRATEGIC RECOMMENDATIONS
-------------------------
1. Consider pricing/packaging review for competitive segment
2. Create "pilot program" offer for price-sensitive deals
3. Develop CFO-specific value story

Would you like me to execute any of these?
```

Apply approved library updates via `update_entity` (competitors, personas, segments) and `update_motion_playbook` (Motion ICP narrative sections).

## MCP Tools Used

### Deal & Event Access
- `list_events` - Deal outcomes and activity (event types via `filters.eventTypes`)
- `list_findings` - Conversation findings (natural-language `query` + `eventFilters`)
- `get_event_detail` - Detailed event info with transcript/content

### Library Context
- `get_entity` - Competitor, persona details
- `list_all_entities` / `list_entities` - Competitor, segment, persona, proof point inventories
- `list_motions` - List Motions in the workspace
- `list_motion_icps` - List Motion ICP cells under a Motion
- `find_motion_icp` - Motion ICP narrative + Learning Loop learnings
- `search_knowledge_base` - Find related content
- `search_resources` - Uploaded CRM exports, deal data files

### Library Updates
- `update_entity` - Apply recommendations to library
- `update_motion_playbook` - Edit Motion Playbook narrative sections based on win/loss findings

## Error Handling

**No Deals Found:**
> No won/lost deals found for this period.
>
> This could mean:
> 1. CRM integration isn't syncing deal outcomes
> 2. Date range has no closed deals
> 3. Filters are too restrictive
>
> Check your Octave CRM integration settings, or expand the date range.

**Insufficient Data (Fewer Than 5 Deals):**
> Only [N] deals found for [period]. Win/loss analysis is most useful with 5+ deals.
>
> Options:
> 1. Proceed anyway — I'll analyze what's there (patterns may be unreliable)
> 2. Expand the time period to capture more deals
> 3. Remove filters to include all segments/competitors

**Missing Deal Data:**
> Deal found but limited conversation data.
>
> For better analysis, ensure:
> - Calls are being recorded and synced
> - Emails are connected
> - Findings extraction is enabled

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> Win/loss analysis requires deal data from Octave. Check your MCP configuration or run `/octave:workspace status`.

## Related Skills

- `/octave:insights` - Broader findings across all events
- `/octave:analyzer` - Deep dive on specific conversations
- `/octave:battlecard` - Competitive battlecards from win/loss data (text or HTML doc)
- `/octave:research` - Research for current pipeline deals
- `/octave:icp-refine` - Refine ICP definitions from deal patterns
- `/octave:pipeline` - Current pipeline coaching and deal strategy
- `/octave:deck` - Present win/loss findings to leadership as a slide deck
- `/octave:enablement` - Turn win/loss learnings into training materials
