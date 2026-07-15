---
name: icp-refine
description: Analyze deal outcomes and conversation patterns to refine ICP definitions and targeting criteria. Use when user says "refine ICP", "who should we target", "update our ICP", "ideal customer profile", or asks why deals are being won or lost.
---

# /octave:icp-refine - ICP Intelligence

Analyze deal outcomes, conversation patterns, and qualification scores to refine your ICP definitions. Compares what your library says your ideal customer looks like against what actually wins — then recommends updates.

## Principles

Follow these standards during generation. Read each before producing output.

**Content and language:**
- [Editorial rules](../shared/editorial-rules.md) — no AI-isms, banned vocabulary, honest analyst tone
- [Information principles](../shared/information-principles.md) — lead with conclusions, evidence-backed claims, narrative arc

**Presentation:**
- [Presentation principles](../shared/presentation-principles.md) — use for any visual output (HTML, dashboards, tables); text follows the editorial rules above

**Octave data:**
- [Octave value](../shared/octave-value.md) — prioritize grounded workspace data over generic AI content

## Usage

```
/octave:icp-refine [--period <days>] [--segment <name>] [--focus wins|losses|both]
```

## Examples

```
/octave:icp-refine                                        # Full ICP analysis (last 180 days)
/octave:icp-refine --period 90                            # Last quarter
/octave:icp-refine --segment "Enterprise"                 # Specific segment
/octave:icp-refine --focus wins                           # Only analyze what's working
/octave:icp-refine --focus losses                         # Only analyze what's not working
```

## Instructions

When the user runs `/octave:icp-refine`:

### Step 1: Set Parameters

If no options specified, use defaults and confirm:

```
I'll analyze your deal data to refine your ICP.

Period: Last 180 days (change with --period)
Segments: All (change with --segment)
Focus: Wins and losses

Starting analysis...
```

### Step 2: Gather Current ICP Definition

```
# Get current segments (this IS the ICP definition)
list_entities({ entityType: "segment" })

# Get full segment details
get_entity({ oId: "<segment_oId>" })  // for each segment

# Get current personas
list_entities({ entityType: "persona" })
get_entity({ oId: "<persona_oId>" })  // for key personas

# Get products/services (what we're selling)
list_entities({ entityType: "product" })
list_entities({ entityType: "service" })
```

### Step 3: Analyze Deal Outcomes

```
# Get won deals
list_events({
  startDate: "<period start>",
  filters: {
    eventTypes: ["DEAL_WON"]
  }
})

# Get lost deals
list_events({
  startDate: "<period start>",
  filters: {
    eventTypes: ["DEAL_LOST"]
  }
})

# Get findings from won deals
list_findings({
  query: "why we won success factors decision criteria champion",
  startDate: "<period start>",
  eventFilters: {
    outcomeFilters: ["WON"]
  }
})

# Get findings from lost deals
list_findings({
  query: "why we lost objections blockers competition pricing",
  startDate: "<period start>",
  eventFilters: {
    outcomeFilters: ["LOST"]
  }
})

# Get positive conversation signals
list_findings({
  query: "excited interested positive resonated value",
  startDate: "<period start>",
  eventFilters: {
    sentiments: ["POSITIVE"]
  }
})

# Get negative signals
list_findings({
  query: "concerned hesitant not a fit wrong timing",
  startDate: "<period start>",
  eventFilters: {
    sentiments: ["NEGATIVE"]
  }
})
```

### Step 4: Analyze Patterns

For each won deal, extract:
- Company profile (industry, size, stage, tech stack)
- Persona(s) involved
- Pain points that resonated
- Value props that closed the deal
- Deal cycle length
- Deal size
- Competitors in the deal

For each lost deal, extract:
- Same attributes
- Why it was lost (competitor, timing, budget, fit, champion)

### Step 5: Generate ICP Refinement Report

See [refinement-report-template.md](references/refinement-report-template.md) for the full ICP refinement report template.

### Step 6: Apply Updates (if requested)

```
# Update segment
update_entity({
  entityType: "segment",
  oId: "<segment_oId>",
  instructions: "<specific updates based on findings>"
})

# Update persona
update_entity({
  entityType: "persona",
  oId: "<persona_oId>",
  instructions: "<specific updates>"
})

# Update Motion Playbook narrative sections (Strategic narrative, Pains and consequences, Benefits and impacts, etc.)
# for the Motion ICP cell that corresponds to the refined persona × segment.
update_motion_playbook({
  motionPlaybookOId: "<motion_playbook_oId>",
  instructions: "Update Strategic narrative and Pains and consequences for the [persona] × [segment] Motion ICP based on ICP refinement findings: [evidence]"
})

# Create new persona if recommended
create_entity({
  entityType: "persona",
  name: "<new persona name>",
  instructions: "<details from deal analysis>"
})
```

### Step 7: Offer Follow-Up Actions

```
What would you like to do next?

1. Deep dive on a specific finding
2. Analyze a specific segment or persona
3. Compare current quarter vs. previous
4. Update a specific library entity
5. Generate updated enablement materials
6. Export the full report
7. Done
```

## MCP Tools Used

### Library Context
- `list_entities` - Segments, personas, products
- `get_entity` - Full entity details for ICP definition

### Deal Analytics
- `list_events` - Won/lost deals
- `list_findings` - Conversation insights, objections, signals
- `get_event_detail` - Deep dive into specific deals

### Library Updates
- `update_entity` - Update segments, personas
- `update_motion_playbook` - Edit Motion Playbook narrative sections (Strategic narrative, Pains and consequences, Benefits and impacts, etc.) for a Motion ICP cell
- `create_entity` - New personas or segments

### Motions
- `list_motions` - List Motions in the workspace
- `list_motion_icps` - List Motion ICP cells (persona × segment) for a Motion
- `find_motion_icp` - Fetch a Motion ICP cell narrative + Learning Loop learnings

### Intelligence
- `search_knowledge_base` - Cross-reference patterns

## Error Handling

**No Deal Data:**
> No deal outcomes found in the last [N] days.
>
> ICP refinement requires win/loss data.
> Options:
> 1. Extend the time period (try --period 365)
> 2. Review conversation data instead (calls/emails without deal outcomes)
> 3. Do a manual ICP review using your library definitions

**Insufficient Data:**
> Found only [N] deals. Statistical patterns may not be reliable.
>
> I'll highlight patterns but flag low-confidence findings.
> Consider extending the period or combining with qualitative analysis.

**No Segments Defined:**
> No segments found in your library.
>
> I can still analyze deal patterns, but there's nothing to compare against.
> Consider creating segments first: `/octave:library create segment`
> Or I'll suggest segment definitions based on the deal data.

## Related Skills

- `/octave:win-loss-report` - Deeper win/loss analysis (complements ICP refinement)
- `/octave:insights` - Field intelligence trends
- `/octave:prospector` - Use refined ICP to find new prospects
- `/octave:audit` - Check library health after updates
- `/octave:library` - Manually update entities
