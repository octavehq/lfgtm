---
name: research
description: Context-aware research and prep for calls, meetings, demos, outreach, and deal reviews. Use when user says "research [company]", "prep for my call", "who is [person]", "meeting prep", "demo prep", or asks to research a company or person. Do NOT use for bulk prospecting — use /octave:prospector instead.
---

# /octave:research - Context-Aware Research & Prep

Research prospects and prepare for calls, meetings, demos, outreach, and deal reviews. Adapts output based on the occasion—whether you're prepping for a discovery call, following up on a deal, or researching a new prospect.

## Usage

```
/octave:research <target> [--for <occasion>]
```

## Examples

```
/octave:research john@acme.com                       # General research
/octave:research acme.com                            # Company research
/octave:research john@acme.com --for discovery       # Discovery call prep
/octave:research "meeting with Acme Corp" --for demo # Demo prep
/octave:research acme.com --for outreach             # Cold outreach angles
```

## Occasions

| Occasion | Output Focus |
|----------|--------------|
| `discovery` | Questions to ask, pain points to probe, qualification criteria |
| `demo` | Use cases to show, proof points to cite, objections to prepare for |
| `follow-up` | Next steps, open questions, momentum builders |
| `outreach` | Hooks, angles, personalization points, CTAs |
| `general` | Comprehensive research (default) |

> **Deal coaching?** Use `/octave:pipeline` for deal-level strategy, stalled deals, multi-threading, and competitive deal coaching.

## Instructions

When the user runs `/octave:research`:

### Step 1: Parse Input and Detect Occasion

**Identify the target:**
- Email address → Person research
- Domain → Company research
- LinkedIn URL → Person research
- Name + company → Person research
- Meeting/deal description → Context-based (extract company/people)

**Detect or ask occasion:**

If `--for` not specified, infer from context or ask:

```
What are you preparing for?

1. Discovery call - First conversation, qualifying the opportunity
2. Demo - Showing the product, proving value
3. Follow-up - Continuing a conversation, next steps
4. Outreach - Cold/warm outreach, getting a response
5. General research - Just want to know more

TIP: For deal coaching and pipeline review, use /octave:pipeline

Your choice:
```

### Step 2: Research the Target

**For Person:**
```
# Try to enrich the person
enrich_person({
  person: {
    email: "<email>",           # if provided
    linkedInProfile: "<url>",   # if provided
    firstName: "<first>",       # if provided
    lastName: "<last>",         # if provided
    companyDomain: "<domain>"   # if provided
  }
})

# Also get company context
enrich_company({ companyDomain: "<domain>" })

# Match to personas
qualify_person({
  person: { ... },
  additionalContext: "Match to our buyer personas and playbooks"
})
```

**For Company:**
```
# Enrich the company
enrich_company({ companyDomain: "<domain>" })

# Qualify against ICP
qualify_company({
  companyDomain: "<domain>",
  additionalContext: "Evaluate fit against our segments and playbooks"
})

# Find key contacts
find_person({
  searchMode: "people",
  companyDomain: "<domain>",
  fuzzyTitles: ["<titles from matching persona>"],
  limit: 5
})
```

**Gather Library Context:**

Use MCP tools:
```
# Find matching playbook
search_knowledge_base({
  query: "<company industry> <persona title> <identified pain points>",
  entityTypes: ["playbook"]
})

# Get relevant proof points
search_knowledge_base({
  query: "<company industry> <company size> results",
  entityTypes: ["proof_point", "reference"]
})

# Get competitor context if detected
search_knowledge_base({
  query: "<any competitor signals>",
  entityTypes: ["competitor"]
})
```

### Step 3: Generate Occasion-Specific Output

---

#### Discovery Call Prep

```
DISCOVERY CALL PREP: [Person] at [Company]
==========================================

PERSON PROFILE
--------------
Name: [Full name]
Title: [Title]
LinkedIn: [URL]

Background:
• [Career history highlights]
• [Relevant experience]
• [Notable achievements]

Matched Persona: [Persona name]
Confidence: [High/Medium/Low]

---

COMPANY SNAPSHOT
----------------
Company: [Name]
Industry: [Industry]
Size: [Employees]
Stage: [Funding/maturity]
Location: [HQ]

Recent Signals:
• [News, funding, hiring, etc.]
• [Technology changes]
• [Leadership changes]

ICP Fit Score: [X/100]
Matched Segment: [Segment name]

---

RECOMMENDED PLAYBOOK
--------------------
[Playbook name]

Strategic Angle: [Approach angle from playbook]

Key Themes to Explore:
1. [Theme based on persona pain points]
2. [Theme based on company signals]
3. [Theme based on industry trends]

---

DISCOVERY QUESTIONS
-------------------

Opening (Rapport + Context):
• "[Question about their role/background]"
• "[Question about company initiative/news]"

Pain Point Exploration:
• "[Question probing pain point 1 from persona]"
  → Listen for: [Signals that indicate fit]

• "[Question probing pain point 2]"
  → Listen for: [Signals that indicate fit]

• "[Question about current solution/process]"
  → Listen for: [Competitor mentions, gaps]

Qualification:
• "[Budget/authority question from playbook]"
• "[Timeline question]"
• "[Decision process question]"

Future State:
• "[Question about goals/desired outcomes]"
• "[Question about success metrics]"

---

POTENTIAL OBJECTIONS
--------------------
Based on persona and company context, prepare for:

1. "[Likely objection]"
   Response: [Brief response strategy]

2. "[Likely objection]"
   Response: [Brief response strategy]

---

PROOF POINTS TO REFERENCE
-------------------------
• [Relevant customer story for their industry]
• [Metric relevant to their likely pain points]
• [Reference customer of similar size/stage]

---

QUALIFICATION CHECKLIST
-----------------------
□ Confirmed pain point exists
□ Identified decision maker(s)
□ Understood timeline
□ Budget discussion initiated
□ Next step agreed

---

NEXT STEP SUGGESTIONS
---------------------
If qualified: "[Specific next step, e.g., schedule demo with team]"
If not ready: "[Nurture action, e.g., send relevant content]"
If not fit: "[Graceful exit]"

---

Want me to:
1. Generate email to confirm the call
2. Create a leave-behind one-pager
3. Research additional stakeholders
4. Draft follow-up email template
```

---

#### Demo Prep

```
DEMO PREP: [Person/Company]
===========================

AUDIENCE
--------
Primary: [Name, Title] - [Decision maker / Evaluator / User]
Others expected: [If known]

Audience Profile:
• Technical depth: [High / Medium / Low]
• Decision authority: [Final / Influencer / User]
• Key concerns: [From persona]

---

RECOMMENDED DEMO FLOW
---------------------
Based on [Persona] priorities and [Company] context:

1. OPENING (2-3 min)
   - Recap their challenges: [Specific pain points discussed]
   - Confirm goals for the demo: "[What they want to see]"

2. USE CASE 1: [Most relevant use case] (10 min)
   - Show: [Specific feature/workflow]
   - Highlight: [Differentiator that matters to them]
   - Connect to their pain: "[How this solves X]"

3. USE CASE 2: [Second priority use case] (8 min)
   - Show: [Specific feature/workflow]
   - Proof point: "[Relevant metric/customer]"

4. USE CASE 3: [If time allows] (5 min)
   - Quick view of: [Additional capability]

5. CLOSING (5 min)
   - Summarize value for their specific situation
   - Address questions
   - Propose next step

---

PROOF POINTS TO WEAVE IN
------------------------
• During [use case 1]: "[Stat/customer relevant to that use case]"
• During [use case 2]: "[Stat/customer relevant to that use case]"
• In closing: "[Industry-specific reference]"

---

OBJECTIONS TO PREPARE FOR
-------------------------

"How does this integrate with [their tech stack]?"
→ [Response based on product capabilities]

"What about [competitor they mentioned]?"
→ [Key differentiation points]

"This seems complex to implement"
→ [Implementation story, time to value proof point]

"What's the pricing?"
→ [Response strategy per playbook]

---

QUESTIONS TO ASK DURING DEMO
----------------------------
• "Does this address [pain point] we discussed?"
• "Who else on your team would be using this?"
• "How does this compare to your current process?"
• "What would need to be true for you to move forward?"

---

COMPETITIVE LANDMINES
---------------------
If [Competitor] is in the mix, demonstrate:
• [Feature they lack]
• [Workflow that's better in our product]
• [Ask: "Did [competitor] show you how they handle X?"]

---

NEXT STEP TO PROPOSE
--------------------
Primary: [Specific next step with stakeholders]
Backup: [Alternative if they're not ready]

---

Want me to:
1. Create a demo follow-up email template
2. Generate a custom one-pager for this account
3. Research other stakeholders to include
4. Prep for specific objections in more depth
```

---

#### Outreach Prep

```
OUTREACH PREP: [Person] at [Company]
====================================

TARGET PROFILE
--------------
Name: [Name]
Title: [Title]
Company: [Company]
LinkedIn: [URL]

Personalization Hooks:
• [Recent activity/post]
• [Career move/milestone]
• [Company news relevant to them]
• [Shared connection/experience]

---

ICP FIT ANALYSIS
----------------
Fit Score: [X/100]

Why they're a fit:
✓ [Fit reason 1]
✓ [Fit reason 2]
✓ [Fit reason 3]

Potential concerns:
⚠ [Any red flags or unknowns]

---

RECOMMENDED PLAYBOOK
--------------------
[Playbook name]

For this [Persona], lead with:
• Primary pain point: "[Pain point most likely to resonate]"
• Value prop: "[Value prop from playbook]"
• Proof point: "[Most relevant social proof]"

---

OUTREACH ANGLES
---------------

ANGLE 1: Pain-Led
"[Opening line addressing pain point]"
Hook: [Why this should resonate]
CTA: [Low-commitment ask]

ANGLE 2: Trigger-Based
"[Opening line referencing company news/trigger]"
Hook: [Why timing is right]
CTA: [Relevant offer]

ANGLE 3: Social Proof
"[Opening line with relevant customer story]"
Hook: [Similar company achieved X]
CTA: [Learn how]

ANGLE 4: Insight-Led
"[Opening line with provocative insight]"
Hook: [Challenges conventional thinking]
CTA: [Discuss further]

---

PERSONALIZATION ELEMENTS
------------------------
Use these in your outreach:

• Company-specific: "[Recent news, initiative, or challenge]"
• Role-specific: "[Something relevant to their title/function]"
• Person-specific: "[LinkedIn activity, podcast appearance, etc.]"
• Timing: "[Why now is relevant - quarter end, planning season, etc.]"

---

MULTI-CHANNEL SEQUENCE SUGGESTION
---------------------------------
Day 1: LinkedIn connection request (personalized note)
Day 2: Email #1 (pain-led angle)
Day 4: LinkedIn engagement (comment on their post)
Day 6: Email #2 (social proof angle)
Day 9: LinkedIn message (direct, different angle)
Day 12: Email #3 (breakup / value-add)

---

CTA OPTIONS
-----------
Low commitment:
• "Worth a 15-min chat?"
• "Open to learning how [Company] did it?"
• "Can I send you [resource]?"

Medium commitment:
• "Can I show you a quick demo?"
• "Want to see your custom ROI analysis?"

High commitment (warm only):
• "Ready to start a pilot?"
• "Can we get your team on a call?"

---

Want me to:
1. Generate the full email sequence
2. Draft LinkedIn messages
3. Research more personalization angles
4. Find additional contacts at this company
```

### Step 4: Offer Follow-Up Actions

After any research output, offer relevant next steps:

```
What would you like to do next?

1. Generate outreach content (/octave:generate)
2. Create collateral for this account (/octave:pmm)
3. Research additional people at the company
4. Deep dive on a specific topic
5. Save notes to [CRM integration if available]
6. Done for now
```

## MCP Tools Used

### Research Operations
- `enrich_person` - Full person intelligence report
- `enrich_company` - Full company intelligence report
- `qualify_person` - ICP scoring for person
- `qualify_company` - ICP scoring for company
- `find_person` - Find contacts at company

### Content Generation
- `generate_call_prep` - Generate full call prep materials

### Library Context
- `get_playbook` - Get recommended playbook
- `get_entity` - Get persona, competitor details
- `search_knowledge_base` - Find proof points, references, messaging

## Error Handling

**Person Not Found:**
> I couldn't find detailed information for [email/name].
>
> I found their company ([Company]). Would you like me to:
> 1. Proceed with company research + generic persona guidance
> 2. Search for them on LinkedIn (provide URL)
> 3. Create research based on their title alone

**Company Not Found:**
> I couldn't find [domain/company name].
>
> Try:
> 1. Check the domain spelling
> 2. Provide the company website URL
> 3. Search by company name instead

**No Matching Playbook:**
> No playbook matches this profile exactly.
>
> Closest matches:
> - [Playbook 1] (60% fit)
> - [Playbook 2] (45% fit)
>
> I'll use [Playbook 1] as a guide, but you may want to create a more specific playbook.

## Related Skills

- `/octave:generate` - Generate outreach content
- `/octave:pmm` - Create account-specific collateral
- `/octave:prospector` - Find more prospects like this one
- `/octave:analyzer` - Analyze past interactions with this account
- `/octave:pipeline` - Deal-level coaching (stalled deals, multi-threading, competitive)
- `/octave:abm` - Full account-based planning with stakeholder mapping
- `/octave:battlecard` - Competitive intelligence for deals
