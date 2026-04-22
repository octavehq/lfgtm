---
name: wins-losses
description: Analyze won and lost deals for patterns, insights, and actionable learnings. Use when user says "win/loss analysis", "why did we lose", "deal patterns", "win themes", or asks about deal outcome trends. Do NOT use for visual HTML reports — use /octave:win-loss-report instead.
---

# /octave:wins-losses - Deal Intelligence

Analyze your won and lost deals to understand what's working, why you're losing, and how to improve win rates. Surface patterns, competitor intelligence, and actionable recommendations.

## Usage

```
/octave:wins-losses [--status won|lost|both] [--period <time-range>]
```

## Options

- `--status <status>` - Focus on won, lost, or both (default: both)
- `--period <range>` - Time range (month, quarter, year, custom)
- `--competitor <name>` - Filter by competitor involvement
- `--segment <name>` - Filter by segment
- `--min-amount <amount>` - Minimum deal size
- `--company <domain>` - Analyze specific deal

## Examples

```
/octave:wins-losses                                  # Overview of recent wins/losses
/octave:wins-losses --status lost --period quarter   # Lost deals this quarter
/octave:wins-losses --competitor "Salesforce"        # Deals involving Salesforce
/octave:wins-losses --segment "Enterprise"           # Enterprise deals analysis
/octave:wins-losses --company acme.com               # Deep dive on Acme deal
```

## Instructions

When the user runs `/octave:wins-losses`:

### Step 1: Determine Focus

If no options provided, show overview:

```
What would you like to analyze?

1. Full Win/Loss Report - Compare wins and losses
2. Win Analysis - What's working, why we win
3. Loss Analysis - Why we're losing, patterns
4. Competitor Analysis - Win/loss by competitor
5. Deal Deep Dive - Analyze specific deal

Your choice:
```

### Step 2: Query Deal Data

**For Overview:**
```
# Get won deals
list_events({
  eventTypes: ["DEAL_WON"],
  dateRange: { start: "<period start>", end: "<today>" },
  limit: 50
})

# Get lost deals
list_events({
  eventTypes: ["DEAL_LOST"],
  dateRange: { start: "<period start>", end: "<today>" },
  limit: 50
})

# Get findings from won deals
list_findings({
  opportunityStatus: ["WON"],
  extractionTypes: [
    "CALL_EXTERNAL_OBJECTIONS",
    "CALL_INTERNAL_VALUE_PROP_PRESENTATIONS",
    "CALL_INTERNAL_PROOF_POINTS",
    "CALL_EXTERNAL_COMPETITORS_TO_OUR_OFFERING"
  ],
  dateRange: { start: "<period start>", end: "<today>" },
  limit: 100
})

# Get findings from lost deals
list_findings({
  opportunityStatus: ["LOST"],
  extractionTypes: [
    "CALL_EXTERNAL_OBJECTIONS",
    "CALL_INTERNAL_VALUE_PROP_PRESENTATIONS",
    "CALL_EXTERNAL_COMPETITORS_TO_OUR_OFFERING"
  ],
  dateRange: { start: "<period start>", end: "<today>" },
  limit: 100
})
```

**For Competitor Analysis:**
```
list_findings({
  extractionTypes: ["CALL_EXTERNAL_COMPETITORS_TO_OUR_OFFERING", "EMAIL_COMPETITOR_MENTION"],
  dateRange: { start: "<period start>", end: "<today>" },
  entityMatches: {
    competitorOIds: ["<competitor_oId>"]
  }
})
```

**For Deal Deep Dive:**
```
list_events({
  eventTypes: ["DEAL_WON", "DEAL_LOST", "CALL", "EMAIL"],
  companyDomains: ["<domain>"]
})

list_findings({
  companyDomains: ["<domain>"]
})

get_event_detail({
  eventOId: "<event_oId>",
  includeTranscript: true
})
```

### Step 3: Analyze Patterns

Aggregate findings across won/lost deals:

```
list_findings({
  eventTypes: ["DEAL_WON", "DEAL_LOST"],
  dateRange: { start: "<period start>", end: "<today>" }
})
```

### Step 4: Present Analysis

---

#### Full Win/Loss Report

See [full-win-loss-report.md](references/full-win-loss-report.md) for the full win/loss report template.

---

#### Loss Analysis (--status lost)

See [loss-analysis.md](references/loss-analysis.md) for the loss analysis template.

---

#### Deal Deep Dive (--company)

See [deal-deep-dive.md](references/deal-deep-dive.md) for the deal deep dive template.

### Step 5: Generate Recommendations

Based on analysis, offer actionable next steps:

```
Based on this analysis, I recommend:

IMMEDIATE ACTIONS
-----------------
1. Create Competitor A TCO battlecard section
   → /octave:pmm battlecard --competitor "Competitor A" --focus pricing

2. Update discovery checklist with budget qualification
   → /octave:library update pb_xxx --add "Budget qualification by meeting 2"

3. Review current pipeline for similar patterns
   → /octave:research --for pipeline-review

STRATEGIC RECOMMENDATIONS
-------------------------
1. Consider pricing/packaging review for competitive segment
2. Create "pilot program" offer for price-sensitive deals
3. Develop CFO-specific value story

Would you like me to execute any of these?
```

## MCP Tools Used

### Deal & Event Access
- `list_events` - Filter by DEAL_WON, DEAL_LOST
- `list_findings` - Get findings from won/lost deals
- `get_event_detail` - Get detailed event info with transcript/content

### Library Context
- `get_entity` - Get competitor, persona details
- `get_playbook` - Get playbook for recommendations
- `search_knowledge_base` - Find related content

### Library Updates
- `update_entity` - Apply recommendations to library

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

**Missing Deal Data:**
> Deal found but limited conversation data.
>
> For better analysis, ensure:
> - Calls are being recorded and synced
> - Emails are connected
> - Findings extraction is enabled

## Related Skills

- `/octave:insights` - Broader findings across all events
- `/octave:analyzer` - Deep dive on specific conversations
- `/octave:battlecard` - Competitive battlecards from win/loss data
- `/octave:research` - Research for current pipeline deals
- `/octave:icp-refine` - Refine ICP definitions from deal patterns
- `/octave:enablement` - Turn win/loss learnings into training materials
