---
name: insights
description: Surface findings, trends, and patterns from calls, emails, and deals
---

# /octave:insights - Field Intelligence

Surface insights from your sales conversations—objections, pain points, questions, and what's resonating. Learn from the field to improve your library and messaging.

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
  eventTypes: ["CALL_TRANSCRIPT", "EMAIL_SENT", "EMAIL_REPLY_RECEIVED"],
  dateRange: { start: "<30 days ago>", end: "<today>" },
  limit: 50
})

# Get finding aggregates
list_findings({
  extractionTypes: [
    "CALL_EXTERNAL_OBJECTIONS",
    "CALL_EXTERNAL_BUSINESS_PROBLEMS",
    "CALL_EXTERNAL_QUESTIONS_OR_CONFUSION_ABOUT_OFFERING",
    "CALL_EXTERNAL_COMPETITORS_TO_OUR_OFFERING",
    "CALL_INTERNAL_VALUE_PROP_PRESENTATIONS"
  ],
  dateRange: { start: "<30 days ago>", end: "<today>" },
  groupBy: "extractionType",
  limit: 100
})
```

**For Specific Type (e.g., Objections):**
```
list_findings({
  extractionTypes: ["CALL_EXTERNAL_OBJECTIONS", "EMAIL_OBJECTION"],
  dateRange: { start: "<period start>", end: "<period end>" },
  limit: 50
})
```

**With Persona/Segment Filter:**
```
list_findings({
  extractionTypes: ["<types>"],
  entityMatches: {
    personaOIds: ["<persona_oId>"]
  },
  limit: 50
})
```

### Step 3: Present Insights

---

#### Overview Output

```
FIELD INSIGHTS: Last 30 Days
============================

Activity Summary
----------------
Total Events Analyzed: 127
- Calls: 45
- Emails Sent: 62
- Email Replies: 20

Companies Engaged: 34
Personas Reached: 5 types

---

TOP OBJECTIONS (12 instances)
-----------------------------
1. "Pricing seems high compared to alternatives" (5x)
   Companies: Acme, TechCorp, DataFlow
   Trend: ↑ Increasing from last month

2. "Concerned about implementation timeline" (4x)
   Companies: BigCo, Enterprise Inc
   Trend: → Stable

3. "Need to involve more stakeholders" (3x)
   Companies: Acme, CloudBase
   Trend: ↓ Decreasing

Library Gap: Objection #1 not addressed in current playbooks
→ Suggestion: Add pricing justification to Enterprise playbook

---

TOP PAIN POINTS (18 instances)
------------------------------
1. "Manual processes taking too much time" (7x)
   Personas: VP Operations, Director of Ops
   ✓ Matches persona: VP Operations pain points

2. "Data silos across departments" (6x)
   Personas: CTO, VP Engineering
   ⚠ Not in current personas - consider adding

3. "Compliance reporting is painful" (5x)
   Personas: CFO, VP Finance
   ✓ Matches persona: CFO pain points

---

TOP QUESTIONS (15 instances)
----------------------------
1. "How does integration with [X] work?" (6x)
   Topics: Salesforce (3), HubSpot (2), Slack (1)

2. "What's the typical implementation timeline?" (5x)

3. "Can you share customer references in [industry]?" (4x)
   Industries requested: Healthcare (2), Finance (2)

---

COMPETITORS MENTIONED (8 instances)
-----------------------------------
1. Competitor A (4x)
   Context: Price comparison, feature parity questions

2. Competitor B (3x)
   Context: Already using, considering switch

3. Competitor C (1x)
   Context: Mentioned as alternative

---

VALUE PROPS THAT RESONATED
--------------------------
Based on positive responses and engagement:

1. "Reduce manual work by 80%" - Strong positive response (4 instances)
2. "Single source of truth" - Good engagement (3 instances)
3. "ROI within 90 days" - Generated follow-up questions (3 instances)

---

RECOMMENDATIONS
===============

Library Updates Suggested:
1. ADD: "Integration complexity concerns" to CTO persona objections
2. ADD: "Data silos" as pain point to VP Engineering persona
3. UPDATE: Enterprise playbook with pricing justification talk track

Content Gaps Identified:
1. Need Healthcare industry references (requested 2x)
2. Need Salesforce integration documentation (asked 3x)

Follow-Up Actions:
1. 3 deals have stalled objections - review with /octave:research
2. 2 competitors gaining mentions - update battlecards with /octave:battlecard

---

Dive deeper:
1. Show me objection details
2. Show me pain point details
3. See specific events
4. Apply updates to library
```

---

#### Type-Specific Output (Objections)

```
OBJECTION INSIGHTS: Last 30 Days
================================

Total Objections: 23 across 18 conversations

---

OBJECTION BREAKDOWN
-------------------

1. PRICING CONCERNS (8 instances - 35%)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 35%

   Examples:
   • "Your pricing is 2x what we're paying now" - Acme Corp, Jan 15
   • "Hard to justify the cost to leadership" - TechCorp, Jan 18
   • "Competitor X is offering a lower rate" - DataFlow, Jan 22

   Personas: CFO (4), VP Operations (3), Procurement (1)

   How We Responded:
   ✓ 3x mentioned ROI/payback period
   ✓ 2x offered pilot/proof of value
   ✗ 3x no documented response

   Playbook Guidance Available: Partial
   → Missing: TCO comparison, hidden cost analysis

2. IMPLEMENTATION CONCERNS (6 instances - 26%)
   ━━━━━━━━━━━━━━━━━━━━━━━━━ 26%

   Examples:
   • "We don't have bandwidth for a long implementation" - BigCo, Jan 12
   • "Last software rollout took 6 months" - Enterprise Inc, Jan 19

   Personas: CTO (3), VP Engineering (2), IT Director (1)

   How We Responded:
   ✓ 4x mentioned typical timeline
   ✓ 2x referenced quick-start option

   Playbook Guidance Available: Yes ✓

3. STAKEHOLDER/TIMING (5 instances - 22%)
   ━━━━━━━━━━━━━━━━━━━━━ 22%

   Examples:
   • "Need to loop in our CTO" - CloudBase, Jan 14
   • "Budget cycle starts in Q2" - Acme, Jan 20

   Personas: VP Sales (2), Director (2), Manager (1)

   This is a buying process objection, not product objection.
   → Suggestion: Multi-threading strategy needed

4. FEATURE GAPS (4 instances - 17%)
   ━━━━━━━━━━━━━━━━━ 17%

   Specific features mentioned:
   • "Do you support SSO?" (2x)
   • "Need on-prem option" (1x)
   • "Looking for [specific integration]" (1x)

---

OBJECTION HANDLING EFFECTIVENESS
--------------------------------

| Objection | Times Handled Well | Times Missed | Success Rate |
|-----------|-------------------|--------------|--------------|
| Pricing | 5 | 3 | 62% |
| Implementation | 4 | 2 | 67% |
| Stakeholder | 2 | 3 | 40% |
| Features | 1 | 3 | 25% |

---

RECOMMENDATIONS
---------------

1. HIGH PRIORITY: Improve pricing objection handling
   - Current playbook response rate: 62%
   - Add: TCO comparison framework
   - Add: "Hidden costs of status quo" talking points

2. MEDIUM PRIORITY: Stakeholder objection strategy
   - Low success rate (40%)
   - Add: Multi-threading guide to playbooks
   - Add: Executive sponsor identification questions

3. TRACK: Feature requests
   - SSO requested 2x - is this on roadmap?
   - On-prem still coming up - competitive disadvantage?

---

Want me to:
1. Draft objection handling language for playbooks
2. Show specific conversations with these objections
3. Compare to last month's objections
4. Update library with recommendations
```

### Step 4: Drill Down Options

When user wants to see specific events:

```
get_event_detail({
  eventOId: "<event_oId>"
})
```

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

[View full transcript] (uses get_event_detail with includeTranscript: true)
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
3. Update playbook only
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

### Library Context
- `get_entity` - Get persona/playbook details
- `search_knowledge_base` - Find related library content

### Library Updates
- `update_entity` - Apply suggested updates

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

- `/octave:analyzer` - Analyze specific conversations in depth
- `/octave:wins-losses` - Focus on deal outcomes
- `/octave:audit` - Ensure library captures field learnings
- `/octave:library` - Update library with insights
- `/octave:battlecard` - Competitive intelligence from conversation data
- `/octave:icp-refine` - Use conversation patterns to refine ICP
- `/octave:enablement` - Turn field insights into team enablement materials
