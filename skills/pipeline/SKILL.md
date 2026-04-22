---
name: pipeline
description: Deal-level coaching with diagnosis, stakeholder strategy, and next-step recommendations. Use when user says "help with this deal", "deal is stalled", "how to close", "competitive deal", "multi-thread", "deal coaching", or mentions a specific stuck deal.
---

# /octave:pipeline - Deal Coach

Deal-level coaching and strategy. Diagnose stalled deals, plan multi-threading, counter competitive threats, engage executives, and generate deal-specific next steps — all informed by your library's playbooks and real conversation data.

## Usage

```
/octave:pipeline [mode] <account> [--contact <email>] [--competitor <name>]
```

## Modes

```
/octave:pipeline                                          # Interactive - describe the deal
/octave:pipeline stalled acme.com                         # Deal is stuck
/octave:pipeline multi-thread acme.com                    # Expand to more stakeholders
/octave:pipeline competitive acme.com --competitor "Acme" # Competitor entered the deal
/octave:pipeline executive acme.com                       # Need executive engagement
/octave:pipeline close acme.com                           # Final stage strategy
/octave:pipeline expand acme.com                          # Customer expansion / upsell
```

## Instructions

When the user runs `/octave:pipeline`:

### Step 1: Understand the Deal Situation

If no mode specified, ask:

```
Tell me about the deal. What's happening?

DEAL CHALLENGES
1. Stalled - Deal has gone quiet or lost momentum
2. Multi-thread - Need to engage more stakeholders
3. Competitive - A competitor has entered or is threatening
4. Executive - Need to get executive buy-in
5. Close - Deal is in final stages, need to close
6. Expand - Existing customer, upsell/cross-sell opportunity

7. Other - Describe the situation

Your choice:
```

Then gather context:
```
A few more details:

1. Account: [company name or domain]
2. Primary contact: [name or email, if known]
3. Deal stage: [Where is it in your pipeline?]
4. How long at this stage: [days/weeks]
5. What happened last: [last interaction or event]
6. Any other context: [budget, timeline, blockers]
```

### Step 2: Research the Deal

```
# Enrich the company
enrich_company({ companyDomain: "<domain>" })

# Qualify the company
qualify_company({ companyDomain: "<domain>" })

# Research the primary contact
enrich_person({
  person: {
    email: "<email>",
    companyDomain: "<domain>"
  }
})

# Qualify the contact
qualify_person({
  person: {
    email: "<email>",
    companyDomain: "<domain>"
  },
  additionalContext: "This is an active deal. Evaluate persona fit and likely buying role."
})

# Check for conversation history
list_events({
  startDate: "<365 days ago>",
  filters: {
    companyDomains: ["<domain>"]
  }
})

# Get findings from past interactions
list_findings({
  query: "objections pain points next steps commitments",
  startDate: "<365 days ago>",
  eventFilters: {
    companyDomains: ["<domain>"]
  }
})

# Match to playbook
search_knowledge_base({
  query: "<company industry> <persona> <deal context>",
  entityTypes: ["playbook"]
})
get_playbook({ oId: "<playbook_oId>", includeValueProps: true })

# Get competitive intel if relevant
search_knowledge_base({
  query: "<competitor name or signals>",
  entityTypes: ["competitor"]
})

# Get proof points for this situation
search_knowledge_base({
  query: "<company industry> <deal stage> results",
  entityTypes: ["proof_point", "reference"]
})
```

### Step 3: Generate Mode-Specific Coaching

#### Mode: Stalled Deal

See [mode-stalled-output.md](references/mode-stalled-output.md) for the Stalled Deal mode output template.

#### Mode: Multi-Thread

See [mode-multi-thread-output.md](references/mode-multi-thread-output.md) for the Multi-Thread mode output template.

#### Mode: Competitive

See [mode-competitive-output.md](references/mode-competitive-output.md) for the Competitive mode output template.

#### Mode: Executive Engagement

See [mode-executive-output.md](references/mode-executive-output.md) for the Executive Engagement mode output template.

#### Mode: Close / Expand

Generate appropriate coaching for closing or expansion scenarios following the same pattern: diagnosis, strategy, specific actions, messaging, and follow-ups.

### Step 4: Offer Follow-Up Actions

Always end with actionable next steps:
```
What would you like to do next?

1. Draft the recommended email/message
2. Generate full call prep for next meeting
3. Research a specific stakeholder
4. Get competitive intelligence
5. Analyze past conversations for patterns
6. Create a deal-specific one-pager
7. Done
```

## MCP Tools Used

### Research
- `enrich_company` - Account intelligence
- `enrich_person` - Stakeholder research
- `qualify_company` - ICP fit assessment
- `qualify_person` - Persona matching
- `find_person` - Stakeholder discovery

### Intelligence
- `list_events` - Conversation and deal history
- `list_findings` - Extracted insights from interactions
- `get_event_detail` - Deep dive into specific interactions
- `search_knowledge_base` - Playbooks, competitors, proof points

### Content Generation
- `generate_email` - Outreach and follow-up drafts
- `generate_content` - Talk tracks, one-pagers, executive messaging
- `generate_call_prep` - Meeting preparation

## Error Handling

**No Conversation History:**
> No previous interactions found with [Company].
>
> I'll base coaching on your library intelligence and general deal patterns.
> As you log calls and emails, coaching will get more contextual.

**Contact Not Found:**
> Couldn't find [contact] at [Company].
>
> Options:
> 1. Provide their email or LinkedIn
> 2. I'll search for stakeholders at the company
> 3. Proceed with company-level coaching

**No Matching Playbook:**
> No playbook matches this deal perfectly.
>
> Using closest match: [Playbook name]
> Consider creating a playbook for this scenario: `/octave:library create playbook`

## Related Skills

- `/octave:research` - Deep research on any stakeholder
- `/octave:battlecard` - Full competitive intelligence
- `/octave:abm` - Complete account plan (broader than deal-level)
- `/octave:generate` - Quick content generation
- `/octave:wins-losses` - Learn from similar deal outcomes
- `/octave:analyzer` - Analyze a specific conversation from this deal
