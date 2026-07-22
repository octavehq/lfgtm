---
name: insights
description: Surface findings, trends, and patterns from calls, emails, and deals. Use when user says "what are prospects saying", "common objections", "conversation trends", "field intelligence", "what patterns", or asks about aggregate conversation insights. Do NOT use for deal-level win/loss analysis — use /octave:win-loss-report instead.
---

# /octave:insights - Field Intelligence

Surface insights from your sales conversations—objections, pain points, questions, and what's resonating. Learn from the field to improve your library and messaging.

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
/octave:insights [--type <finding-type>] [--period <time-range>]
```

## Options

- `--type <type>` - Focus on specific finding type (objections, pain-points, questions, competitors, value-props)
- `--period <range>` - Time range (today, week, month, quarter, custom)
- `--segment <name>` - Filter by segment
- `--persona <name>` - Filter by persona
- `--company <domain>` - Filter by company

## Examples

```
/octave:insights                                    # Overview of recent insights
/octave:insights --type objections                  # Top objections
/octave:insights --type pain-points --period month  # Pain points this month
/octave:insights --persona "CTO"                    # Insights from CTO conversations
/octave:insights --company acme.com                 # Insights from Acme conversations
```

## Instructions

When the user runs `/octave:insights`:

### Step 1: Determine Focus

If no options provided, show an overview:

```
What insights would you like to explore?

1. Overview - Summary across all finding types
2. Objections - What objections are prospects raising?
3. Pain Points - What problems are prospects mentioning?
4. Questions - What are prospects asking about?
5. Competitors - Which competitors are coming up?
6. Value Props - Which value props are resonating?
7. Custom - Specific filters

Your choice (or just ask a question):
```

### Step 2: Query Events and Findings

Use the MCP tools to gather data:

**For Overview:**
```
# Get recent events
list_events({
  filters: { eventTypes: ["CALL_TRANSCRIPT", "EMAIL_SENT", "EMAIL_REPLY_RECEIVED"] },
  startDate: "<30 days ago>",
  endDate: "<today>",
  limit: 50
})

# Get finding aggregates
list_findings({
  query: "objections, business problems, questions or confusion about the offering, competitor mentions, and value prop presentations",
  startDate: "<30 days ago>",
  endDate: "<today>",
  limit: 100
})
```

**For Specific Type (e.g., Objections):**
```
list_findings({
  query: "objections and pushback raised by prospects",
  startDate: "<period start>",
  endDate: "<period end>",
  limit: 50
})
```

**With Persona/Segment Filter:**
```
list_findings({
  query: "<topic>",
  eventFilters: {
    personas: ["<persona_oId>"]
  },
  limit: 50
})
```

### Step 3: Present Insights

---

#### Overview Output

See [overview-output.md](references/overview-output.md) for the overview output template.

---

#### Type-Specific Output (Objections)

See [objections-output.md](references/objections-output.md) for the objection-type output template.

### Step 4: Drill Down Options

When user wants to see specific events:

```
get_event_detail({
  eventOId: "<event_oId>"
})
```

When the user wants the exact quote behind a finding, not just the event it came from — "show me what they actually said," "pull the verbatim" — use `search_call_transcripts` instead of (or alongside) `get_event_detail`. It searches across all indexed calls, not just one known event, and returns speaker-attributed moments with `recordingUrl` + `startSec` for jump-to-moment citations. `list_findings` is the paraphrased trend; `search_call_transcripts` is the receipt.

Present the full context:

```
EVENT DETAILS: Call with John Smith (Acme Corp)
===============================================
Date: January 15, 2026
Duration: 32 minutes
Participants:
  - Internal: Sarah (AE), Mike (SE)
  - External: John Smith (VP Ops), Lisa Chen (Director)

Matched Persona: VP Operations
Matched Playbook: Enterprise Efficiency

---

KEY FINDINGS

Objections Raised:
• [12:34] John: "Your pricing is 2x what we're paying now for our current solution"
  → Response: Sarah mentioned ROI payback period

Pain Points Acknowledged:
• [08:15] John: "We're spending 20 hours a week on manual data entry"
  → Matches persona pain point ✓

• [15:42] Lisa: "The biggest issue is data not syncing between systems"
  → Consider adding to persona

Questions Asked:
• [18:20] John: "How long does implementation typically take?"
• [22:05] Lisa: "Do you integrate with Salesforce?"

Competitor Mentioned:
• [25:30] John: "We looked at [Competitor] last year but didn't move forward"

Value Props Delivered:
• [10:15] Sarah: "Customers typically see 80% reduction in manual work"
  → Positive response from John

---

[View full transcript] (uses get_event_detail with includeFullContent: true)
```

### Step 5: Apply Updates to Library

If user wants to update library based on insights:

```
Based on this insight, I recommend:

Update Persona: VP Operations
Add pain point: "Data silos causing manual reconciliation work"
Add objection: "Pricing compared to current solution"

Update Playbook: Enterprise Efficiency
Add objection handling: "Pricing 2x current solution"
Response: "Let's look at total cost of ownership including the 20 hours/week
your team spends on manual work. At $X/hour, that's $Y annually..."

Apply these updates?
1. Yes, update both
2. Update persona only
3. Update Motion ICP narrative only
4. Let me customize first
5. Skip
```

If yes, use `update_entity` to apply.

## Finding Types Reference

| Type | Description | Extraction Types |
|------|-------------|------------------|
| objections | Pushback and concerns raised | `CALL_EXTERNAL_OBJECTIONS`, `EMAIL_OBJECTION` |
| pain-points | Problems prospects mention | `CALL_EXTERNAL_BUSINESS_PROBLEMS`, `EMAIL_PAIN_POINT` |
| questions | Questions asked about offering | `CALL_EXTERNAL_QUESTIONS_OR_CONFUSION_ABOUT_OFFERING`, `EMAIL_QUESTION` |
| competitors | Competitor mentions | `CALL_EXTERNAL_COMPETITORS_TO_OUR_OFFERING`, `EMAIL_COMPETITOR_MENTION` |
| value-props | Value props that resonated | `CALL_INTERNAL_VALUE_PROP_PRESENTATIONS`, `EMAIL_VALUE_PROP` |
| use-cases | Use cases discussed | `CALL_INTERNAL_USE_CASES_BROUGHT_UP`, `EMAIL_USE_CASE` |
| proof-points | Proof points referenced | `CALL_INTERNAL_PROOF_POINTS`, `EMAIL_PROOF_POINT` |

## MCP Tools Used

### Event & Finding Access
- `list_events` - Search events with filters
- `list_findings` - Aggregate findings across events
- `get_event_detail` - Get detailed event info with transcript/content
- `search_call_transcripts` - Verbatim, speaker-attributed quotes across all indexed calls (query, persona, sentiment, deal outcome) — the receipt behind a finding, not the paraphrase
- `get_entity_evidence` - Best verbatim quotes evidencing one library entity (persona, competitor, objection, use case)

### Library Context
- `get_entity` - Get persona / segment / competitor / objection details
- `list_motions` / `list_motion_icps` / `find_motion_icp` - Pull the Motion ICP narrative (Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References) for persona × segment context
- `search_knowledge_base` - Find related library content

### Library Updates
- `update_entity` - Apply suggested updates to library entities (personas, segments, objections, etc.)
- `update_motion_playbook` - Edit Motion ICP narrative sections (Strategic narrative, Benefits and impacts, Pains and consequences) with field-informed refinements

## Error Handling

**No Events Found:**
> No events found for the specified period.
>
> This could mean:
> 1. No calls/emails have been synced yet
> 2. The date range is too narrow
> 3. Filters are too restrictive
>
> Try:
> - Expanding the date range
> - Removing filters
> - Check that your CRM/email integration is connected in Octave

**No Findings Extracted:**
> Events found but no findings extracted yet.
>
> Findings are extracted automatically when events are processed.
> Recent events may still be processing.
>
> Check back in a few minutes, or view raw events instead.

## Related Skills

- `/octave:call-analyzer` - Analyze specific conversations in depth
- `/octave:win-loss-report` - Focus on deal outcomes
- `/octave:audit` - Ensure library captures field learnings
- `/octave:library` - Update library with insights
- `/octave:battlecard-doc` - Competitive intelligence from conversation data
- `/octave:icp-refine` - Use conversation patterns to refine ICP
- `/octave:train` - Turn field insights into team training
