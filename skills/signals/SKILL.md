---
name: signals
description: Morning intelligence briefing that surfaces the deals and signals demanding attention right now. Use when user says "what should I focus on", "morning briefing", "what happened", "signals", "what needs attention", "daily update", or asks what changed since they last checked. Flips from pull-based to push-based — the data tells you what to work on.
argument-hint: "[--period today|3d|week|2w] [--focus deals|patterns|pipeline|content] [--segment <name>] [--motion <name>]"
---

# /octave:signals - Morning Intelligence Briefing

Your daily command center. Surfaces the deals that moved, objections trending up, competitors appearing, stakeholders going silent, and messaging themes gaining or losing traction — so you know exactly what to work on today.

## Usage

```
/octave:signals [--period <time-range>] [--focus <area>]
```

## Options

- `--period <range>` - Lookback window (today, 3d, week, 2w — default: week)
- `--focus <area>` - Zoom into one section (deals, patterns, pipeline, content)
- `--segment <name>` - Filter by segment
- `--motion <name>` - Filter by Motion

## Examples

```
/octave:signals                          # Full morning briefing (last 7 days)
/octave:signals --period today           # What happened since yesterday
/octave:signals --period 2w              # Broader two-week view
/octave:signals --focus deals            # Just the deals that need attention
/octave:signals --focus patterns         # Just emerging patterns
```

## Instructions

When the user runs `/octave:signals`:

### Step 1: Gather All Signal Data

Run these queries **in parallel** to gather the full picture. Use the period option to set date ranges (default: last 7 days). Note the call shapes: `list_events` takes event types inside `filters`; `list_findings` requires a natural-language `query` with any filters inside `eventFilters`.

**A. Recent Events (activity stream)**
```
list_events({
  startDate: "<period start>",
  endDate: "<today>",
  limit: 100,
  filters: {
    eventTypes: ["CALL_TRANSCRIPT", "EMAIL_SENT", "EMAIL_REPLY_RECEIVED", "DEAL_WON", "DEAL_LOST", "OPPORTUNITY_CREATED", "MEETING_BOOKED"]
  }
})
```

**B. Current Period Findings (signal extraction)**
```
list_findings({
  query: "objections, pain points, questions or confusion about the offering, competitor mentions, value props presented, proof points cited, use cases discussed",
  startDate: "<period start>",
  endDate: "<today>",
  limit: 200
})
```

**C. Previous Period Findings (for trend comparison)**
```
list_findings({
  query: "objections, competitor mentions, value props presented, proof points cited",
  startDate: "<two periods ago>",
  endDate: "<period start>",
  limit: 200
})
```

Bucket the returned findings by type yourself (objections, competitors, value props, proof points, and so on), then diff the current-period buckets against the previous-period buckets to detect trends.

**D. Library Context (for gap detection)**
```
list_entities({ entityType: "persona" })
list_entities({ entityType: "segment" })
list_entities({ entityType: "use_case" })
list_entities({ entityType: "competitor" })
list_entities({ entityType: "objection" })
list_entities({ entityType: "proof_point" })
```

### Step 2: Analyze and Prioritize Signals

Process the raw data into four signal categories. **Prioritize by urgency** — things that need action today come first.

**Signal Priority Rules:**
1. **CRITICAL** — Champion went silent, competitor entered a deal, deal moved backward, new objection not in Motion ICP / Objection entity
2. **HIGH** — Deal advanced (opportunity to accelerate), objection frequency spiking, stakeholder engagement dropped
3. **MEDIUM** — New patterns emerging, content performance shifts, pipeline health changes
4. **INFO** — Positive confirmations, stable trends, wins

### Step 3: Present the Briefing

Use the `--focus` flag to show only the requested section, or show all four sections for the full briefing.

---

#### Full Briefing Output

See [briefing-output-template.md](references/briefing-output-template.md) for the full morning briefing output template.

### Step 4: Handle Focus Mode

When `--focus` is specified, show only that section with expanded detail:

**`--focus deals`**: Show the Deals section with additional context per deal — include last 3 interactions, all stakeholders, full finding history.

**`--focus patterns`**: Show the Patterns section with full finding breakdowns — include specific quotes, event links, week-over-week trend charts.

**`--focus pipeline`**: Show Pipeline Health with deal-level detail — list every deal that moved, every deal at risk, every new deal.

**`--focus content`**: Show Content Performance with usage rankings across all proof points, value props, and Motion ICPs.

### Step 5: Drill Down

When user asks to dive deeper into any signal:

```
get_event_detail({
  eventOId: "<event_oId>"
})
```

Present full context for the signal — the event, the finding, the deal history, and recommended actions.

### Step 6: Act on Signals

When user wants to act on a detected gap:

**Library Gap → Create/Update:**
```
# If objection not in a Motion ICP cell, update that cell's narrative
update_motion_playbook({
  motionPlaybookOId: "<motion_playbook_oId>",
  instructions: "Add objection handling for: [detected objection] to the relevant Motion ICP narrative section"
})

# If competitor not tracked
search_knowledge_base({
  query: "<competitor name>",
  entityTypes: ["competitor"]
})
# If not found, suggest:
# /octave:library create competitor "[name]"
```

**Deal Signal → Route to Skill:**
Suggest the appropriate follow-up skill based on signal type:
- Silent champion → `/octave:pipeline stalled <domain>`
- New competitor → `/octave:battlecard --competitor "<name>"`
- Deal advanced → `/octave:pipeline close <domain>`
- New stakeholder needed → `/octave:pipeline multi-thread <domain>`
- Objection spike → `/octave:enablement objections --topic "<topic>"`
- Win pattern → `/octave:wins-losses --status won`

## Signal Detection Logic

### Deal Signals
| Signal | Detection | Priority |
|--------|-----------|----------|
| Champion silent | No reply from primary contact in >2x their avg response time | CRITICAL |
| New competitor | Competitor-mention finding appears for a deal where it wasn't before | CRITICAL |
| Deal moved backward | Deal stage change event where new stage is earlier than previous | CRITICAL |
| Deal advanced | Deal stage change event moving forward | HIGH |
| Stalled deal | Active deal with no events in 14+ days | HIGH |
| New deal | First event for a company domain | MEDIUM |
| Deal won | DEAL_WON event | INFO |
| Deal lost | DEAL_LOST event | INFO |

### Pattern Signals
| Signal | Detection | Priority |
|--------|-----------|----------|
| Objection spike | >2x increase in objection findings vs previous period | HIGH |
| New objection | Objection theme appears that wasn't in previous period | HIGH |
| Competitor trending | Competitor mentions increased >50% vs previous period | HIGH |
| Hot proof point | Proof point cited in >3 conversations this period | MEDIUM |
| Cold proof point | Proof point with 0 citations for 30+ days | MEDIUM |

### Library Gap Signals
| Signal | Detection | Priority |
|--------|-----------|----------|
| Unaddressed objection | Objection finding with no matching Motion ICP narrative content | HIGH |
| Unknown competitor | Competitor mention with no competitor entity in library | HIGH |
| Missing persona | Person qualified to a persona type not in library | MEDIUM |
| Stale Motion ICP | Motion ICP cell with 0 event associations in 30+ days | MEDIUM |

## MCP Tools Used

### Event & Finding Access
- `list_events` - Activity stream with date/type filters
- `list_findings` - Finding aggregates with grouping and trend data
- `get_event_detail` - Drill into specific events

### Library Context
- `list_entities` - Full library inventory for gap detection
- `list_motions` - List Motions in the workspace
- `list_motion_playbooks` - List Motion Playbooks under a Motion
- `list_motion_icps` - List Motion ICP cells under a Motion
- `find_motion_icp` - Fetch Motion ICP narrative + Learning Loop learnings
- `search_knowledge_base` - Match findings to library content
- `get_entity` - Get entity details for context

### Library Updates
- `update_entity` - Apply detected gap fixes
- `create_entity` - Create new entities for detected gaps
- `update_motion_playbook` - Edit Motion Playbook narrative sections (e.g., add objection handling to a Motion ICP)

## Error Handling

**No Events in Period:**
> No activity found in the last [period].
>
> This could mean:
> 1. No calls/emails have been synced recently
> 2. The period is too narrow — try `--period 2w` or `--period month`
> 3. CRM/email integration may need reconnecting
>
> Check your integrations in Octave, or try a wider window.

**No Findings Extracted:**
> Events found but no findings extracted yet.
>
> Recent events may still be processing. Check back in a few minutes.
> In the meantime, here's what happened (raw activity):
> [Show event summary without finding analysis]

**Insufficient Data for Trends:**
> Not enough historical data to detect trends.
>
> I'll show you what's happening now, but trend analysis needs at least 2 weeks of data.
> Keep using Octave and trends will appear in future briefings.

## Related Skills

- `/octave:insights` - Deep dive into specific finding types
- `/octave:pipeline` - Deal-level coaching for flagged deals
- `/octave:wins-losses` - Pattern analysis across deal outcomes
- `/octave:battlecard` - Competitive intelligence for new competitors
- `/octave:enablement` - Turn trending objections into team materials
- `/octave:audit` - Full library health check
- `/octave:library` - Create/update entities for detected gaps
