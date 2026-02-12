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

---

#### Mode: Stalled Deal

```
DEAL COACHING: STALLED DEAL
============================

Account: [Company]
Contact: [Name, Title]
Stage: [Stage] | Days in Stage: [N]
Last Activity: [Date and description]

---

DIAGNOSIS
---------
Based on the deal context and conversation history:

Likely Reasons for Stall:
1. [Reason 1] — Evidence: "[From conversation data or context]"
2. [Reason 2] — Evidence: "[...]"
3. [Reason 3] — Evidence: "[...]"

Risk Level: [High / Medium / Low]

---

RE-ENGAGEMENT STRATEGY
-----------------------

APPROACH 1: Value-Add Re-Engagement
Timing: [Now]
Action: Send [specific content/insight] relevant to [their situation]
Why: Adds value without asking for anything, restarts conversation
Draft message: "[Short email or LinkedIn message]"

APPROACH 2: New Information Trigger
Timing: [When available]
Action: Share [industry news, product update, relevant content]
Why: Creates legitimate reason to re-engage
Draft message: "[Short message]"

APPROACH 3: Multi-Thread Around the Stall
Timing: [If approach 1-2 don't work within 1 week]
Action: Reach out to [other stakeholder] with [different angle]
Why: Champion may be blocked; find alternative path
Draft message: "[Short message]"

APPROACH 4: Executive Air Cover
Timing: [If deal is high-value and stall persists]
Action: Have [your exec] reach out to [their exec]
Why: Elevates priority, demonstrates commitment
Draft message: "[Short message]"

---

CONVERSATION STARTERS
---------------------
• "I noticed [company news/signal] — how is that affecting [their initiative]?"
• "We just [published/released/achieved] [relevant thing] — thought of you because [connection]"
• "When we spoke in [month], you mentioned [specific thing]. Has that situation changed?"
• "I've been thinking about [their challenge] — here's an idea: [insight]"

---

THINGS TO AVOID
---------------
• Don't: "[Common mistake for this situation]"
• Don't: "Just checking in" (no value)
• Don't: Pressure tactics (erodes trust)

---

PROOF POINTS TO DEPLOY
-----------------------
• [Relevant proof point for re-engagement]
• [New metric or case study to share]

---

NEXT 3 ACTIONS
--------------
1. [This week] [Specific action] → [Expected outcome]
2. [Next week] [Specific action if #1 doesn't work]
3. [Week after] [Escalation action]

---

Want me to:
1. Draft the re-engagement email
2. Research other stakeholders to multi-thread
3. Generate call prep for when they respond
4. Analyze past conversations for clues
```

---

#### Mode: Multi-Thread

```
DEAL COACHING: MULTI-THREADING
================================

Account: [Company]
Current Contact: [Name, Title]
Deal Stage: [Stage]

---

CURRENT COVERAGE
----------------
Known Stakeholders:
• [Name, Title] — [Role: Champion/Evaluator/etc.] — [Status]

Missing Roles:
⚠ [Economic buyer not identified]
⚠ [Technical evaluator not engaged]
⚠ [End users not involved]

---

RECOMMENDED STAKEHOLDERS
-------------------------
```

```
# Find additional contacts
find_person({
  searchMode: "people",
  companyDomain: "<domain>",
  fuzzyTitles: ["<missing role titles>"],
  limit: 5
})
```

```
| Name | Title | Why Engage | Approach |
|------|-------|-----------|----------|
| [Name 1] | [Title] | [Economic buyer] | [Warm intro via champion] |
| [Name 2] | [Title] | [Technical eval] | [Direct outreach with technical angle] |
| [Name 3] | [Title] | [End user / champion builder] | [Value-add content] |

---

ENGAGEMENT STRATEGY PER STAKEHOLDER
------------------------------------

[Stakeholder 1]: [Name, Title]
Persona Match: [Persona]
Their Priority: [What they care about]
Message: "[Tailored outreach — different angle than primary contact]"
Channel: [Email / LinkedIn / Internal intro]
Ask: "[Specific CTA]"

[Stakeholder 2]: [Name, Title]
[Same structure]

---

MULTI-THREADING SEQUENCE
-------------------------
1. [Action] Ask [Champion] to introduce you to [Stakeholder]
2. [Action] Send [direct outreach] to [Stakeholder] via [channel]
3. [Action] Engage [Stakeholder] with [content/value-add]
4. [Action] Propose [group meeting/demo] with multiple stakeholders

---

TALK TRACK FOR ASKING CHAMPION
-------------------------------
"[How to ask your champion to make introductions]"

---

Want me to:
1. Generate outreach for a specific stakeholder
2. Research a specific person in depth
3. Create stakeholder-specific content
4. Generate call prep for a multi-stakeholder meeting
```

---

#### Mode: Competitive

```
DEAL COACHING: COMPETITIVE THREAT
===================================

Account: [Company]
Competitor: [Competitor Name]
Deal Stage: [Stage]

---

COMPETITIVE SITUATION
---------------------
[Summary of competitive landscape in this deal]

Their Likely Angle: [How the competitor probably positions]
Our Best Counter: [How to reframe]

---

IMMEDIATE ACTIONS
-----------------
1. [Set evaluation criteria that favor us]
2. [Deploy specific proof point]
3. [Ask trap question to expose their weakness]

---

[Pull from /octave:battlecard intelligence for this competitor]

TRAP QUESTIONS FOR THIS DEAL
-----------------------------
Given [company]'s specific situation, ask:
1. "[Contextual trap question]" — exposes [competitor weakness]
2. "[Contextual trap question]" — highlights our advantage in [area]

LANDMINES TO SET
----------------
1. "[Criterion to establish]" — plays to our strength
2. "[Requirement to introduce]" — they can't meet this

---

PROOF POINTS TO DEPLOY
-----------------------
• [Customer similar to this account who chose us over competitor]
• [Metric that beats competitor's claims]

---

DISPLACEMENT MESSAGING
-----------------------
If they're leaning toward [competitor]:
"[Talk track to shift the conversation]"

If they're already using [competitor]:
"[Talk track for switching narrative]"

---

Want me to:
1. Generate a full battlecard for this competitor
2. Draft competitive displacement email
3. Create comparison content for this account
4. Prep for a head-to-head demo
```

---

#### Mode: Executive Engagement

```
DEAL COACHING: EXECUTIVE ENGAGEMENT
=====================================

Account: [Company]
Target Executive: [Name/Title or "identify"]

---

EXECUTIVE BRIEF
---------------
[Research executive if identified, or recommend which exec to target]

Why Executive Engagement Now:
• [Reason: deal size, stall, strategic importance]
• [Trigger: what justifies executive involvement]

---

EXECUTIVE-LEVEL MESSAGING
--------------------------
Executives care about: [Strategic outcomes, not features]
Lead with: "[Business impact statement]"
Proof: "[Executive-level proof point — revenue, competitive advantage, risk reduction]"

Draft Executive Email/Message:
[Short, direct, business-focused message from your exec to their exec]

---

MEETING STRATEGY
----------------
If you get the meeting:
• Open with: [Strategic context, not product pitch]
• Key question: "[Strategic question about their business]"
• Value to present: [Business outcome, not feature demo]
• Ask: "[Executive-level next step]"

---

Want me to:
1. Draft the executive outreach
2. Generate executive meeting prep
3. Create an executive summary one-pager
```

---

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
