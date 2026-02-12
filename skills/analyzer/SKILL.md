---
name: analyzer
description: Analyze email threads, call transcripts, and conversations for resonance, adherence to messaging, and competitive differentiation. Use when user says "analyze this call", "how did the email land", "score this thread", "conversation analysis", or pastes conversation content to evaluate.
---

# /octave:analyzer - Conversation Analysis

Analyze email threads, call transcripts, and sales conversations against your Octave library. Evaluates messaging resonance, playbook adherence, and competitive differentiation. Provides actionable insights, suggested improvements, and draft follow-ups.

## Usage

```
/octave:analyzer [--type email|call|chat]
```

## Examples

```
/octave:analyzer                              # Interactive - paste content
/octave:analyzer --type email                 # Analyze email thread
/octave:analyzer --type call                  # Analyze call transcript
```

## Instructions

When the user runs `/octave:analyzer`:

### Step 1: Get Content to Analyze

```
What would you like me to analyze?

1. Paste an email thread
2. Paste a call transcript
3. Paste a chat/message thread
4. Provide a file path

(Paste content below or tell me the file path)
```

Accept pasted content or read from file. Content can be:
- Email thread (with headers or without)
- Call transcript (with speaker labels or without)
- Chat/messaging thread
- Meeting notes

### Step 2: Parse and Structure the Content

**For Email:**
Extract:
- Participants (internal vs external)
- Thread direction (outbound, inbound, back-and-forth)
- Key messages from each party
- Current status (awaiting response, ended, etc.)

**For Call Transcript:**
Extract:
- Participants and roles
- Speaker segments
- Key exchanges
- Duration indicators if available

**For Chat:**
Extract:
- Participants
- Message sequence
- Key exchanges

### Step 3: Identify Context

Use MCP tools to gather context:

**Research external participants:**
```
# Get external participant info
find_person({
  searchMode: "specific_person",
  email: "<external email>",  # or
  firstName: "<name>",
  companyName: "<company>"
})

# Get company info
find_company({
  domain: "<domain from email>"  # or inferred from signature
})

# Match to persona
qualify_person({
  person: { email: "<email>", jobTitle: "<title>" },
  additionalContext: "Identify which persona this person matches"
})
```

**Get library context:**
```
# Find relevant playbook
search_knowledge_base({
  query: "<key topics from conversation>",
  entityTypes: ["playbook"]
})
```

### Step 4: Analyze Against Library

Run three analysis dimensions:

---

#### Resonance Analysis
*Did our messaging land? What signals indicate engagement or disengagement?*

Use MCP to get persona details:
```
# Search for messaging we used
search_knowledge_base({
  query: "<key phrases from our messages>",
  entityTypes: ["persona", "playbook", "use_case"]
})

# Compare to persona pain points
get_entity({ oId: "<matched_persona_oId>" })
```

Evaluate:
- Pain points addressed vs. persona's documented pain points
- Value props used vs. available value props
- Questions asked vs. recommended discovery questions
- Response patterns indicating interest/skepticism

---

#### Adherence Analysis
*Did we follow the playbook? What did we miss?*

Use MCP to get playbook details:
```
# Get the relevant playbook
get_playbook({ oId: "<matched_playbook_oId>", includeValueProps: true })
```

Compare conversation to playbook:
- Strategic narrative alignment
- Value props delivered vs. available
- Qualifying questions asked
- Objection handling approach
- Discovery depth

---

#### Differentiation Analysis
*Did we position against competitors effectively?*

Use MCP to get competitor details:
```
# Check for competitor mentions
search_knowledge_base({
  query: "<competitor names or hints from conversation>",
  entityTypes: ["competitor"]
})

# Get competitor details
get_entity({ oId: "<competitor_oId>" })
```

Evaluate:
- Competitor mentions (explicit or implicit)
- Our differentiation points used vs. available
- Landmines set or missed
- Competitive traps addressed

### Step 5: Generate Analysis Report

```
CONVERSATION ANALYSIS
=====================

Analyzed: [Email thread / Call transcript / Chat]
Date: [If available]
Duration/Length: [X messages / X minutes]

---

PARTICIPANTS
------------
Internal:
• [Name] ([Role]) - [# of messages/speaking time]

External:
• [Name] ([Title] at [Company]) - [# of messages/speaking time]
  Matched Persona: [Persona name] ([Confidence])

---

CONTEXT IDENTIFIED
------------------
Company: [Company name]
ICP Fit: [Score/100]
Stage: [Discovery / Demo / Negotiation / etc.]
Playbook Match: [Playbook name]

---

EXECUTIVE SUMMARY
-----------------
[2-3 sentence summary of what happened, key outcomes, and overall assessment]

---

RESONANCE ANALYSIS
==================
Score: [X/10] - [Strong / Moderate / Weak]

What Resonated (Positive Signals):
✓ [Signal 1] - [Quote or evidence]
  "[Exact quote from prospect showing interest]"

✓ [Signal 2] - [Quote or evidence]
  "[Exact quote showing engagement]"

What Didn't Land (Concerns):
✗ [Issue 1] - [Quote or evidence]
  "[Quote showing skepticism or disengagement]"
  Suggestion: [How to address this]

✗ [Issue 2] - [Quote or evidence]
  Suggestion: [How to address this]

Pain Points Addressed:
┌──────────────────────────────────────────────┐
│ Persona Pain Point          │ Addressed?     │
├──────────────────────────────────────────────┤
│ [Pain point 1]              │ ✓ Yes          │
│ [Pain point 2]              │ ✗ No           │
│ [Pain point 3]              │ ~ Partially    │
└──────────────────────────────────────────────┘

Recommendations:
• [Specific action to improve resonance]
• [Topic to explore in next conversation]

---

ADHERENCE ANALYSIS
==================
Score: [X/10] - [Strong / Moderate / Weak]
Playbook: [Playbook name]

Playbook Elements Used:
✓ [Element 1] - Used effectively
✓ [Element 2] - Used effectively

Playbook Elements Missed:
✗ [Element 3] - Not addressed
  Why it matters: [Impact of missing this]
  Add in follow-up: [Suggestion]

✗ [Element 4] - Not addressed
  Why it matters: [Impact]
  Add in follow-up: [Suggestion]

Value Props Delivered:
┌────────────────────────────────────────────────────┐
│ Value Prop                   │ Delivered? │ Impact │
├────────────────────────────────────────────────────┤
│ [VP 1 for this persona]      │ ✓ Strong   │ Positive │
│ [VP 2 for this persona]      │ ✗ No       │ Opportunity │
│ [VP 3 for this persona]      │ ~ Weak     │ Reinforce │
└────────────────────────────────────────────────────┘

Discovery Questions:
┌─────────────────────────────────────────────────┐
│ Recommended Question          │ Asked? │ Answer │
├─────────────────────────────────────────────────┤
│ [Question 1 from playbook]    │ ✓ Yes  │ [Summary] │
│ [Question 2 from playbook]    │ ✗ No   │ -         │
│ [Question 3 from playbook]    │ ✗ No   │ -         │
└─────────────────────────────────────────────────┘

Recommendations:
• Ask "[missed question]" in follow-up
• Reinforce "[underdelivered value prop]" with proof point

---

DIFFERENTIATION ANALYSIS
========================
Score: [X/10] - [Strong / Moderate / Weak]

Competitors Detected:
• [Competitor 1] - [How mentioned: explicit / implicit / inferred]
• [Competitor 2] - [How mentioned]

Differentiation Points Used:
✓ [Differentiator 1] - "[Quote where we differentiated]"
✓ [Differentiator 2] - "[Quote]"

Differentiation Opportunities Missed:
✗ [Differentiator 3] - Not mentioned
  When to use: [Trigger from conversation where this would fit]

✗ [Differentiator 4] - Not mentioned
  When to use: [Trigger]

Competitive Positioning:
┌────────────────────────────────────────────┐
│ Our Differentiator    │ Mentioned? │ Impact │
├────────────────────────────────────────────┤
│ [Diff 1 vs competitor]│ ✓ Yes      │ Strong │
│ [Diff 2 vs competitor]│ ✗ No       │ Missed │
│ [Diff 3 vs competitor]│ ✗ No       │ Missed │
└────────────────────────────────────────────┘

Competitive Risks:
⚠ [Risk identified from conversation]
  Counter: [How to address]

Recommendations:
• In follow-up, plant this landmine: "[Question that exposes competitor weakness]"
• Reference: "[Proof point of competitive win]"

---

ACTION ITEMS IDENTIFIED
=======================

From Prospect (They Committed To):
□ [Action item prospect mentioned]
□ [Action item prospect mentioned]

From Us (We Should Do):
□ [Action we committed to]
□ [Implied action to take]

Open Questions (Need Answers):
? [Unresolved question from conversation]
? [Question we should have asked]

---

FOLLOW-UP RECOMMENDATIONS
=========================

Immediate (Within 24 Hours):
1. [Specific action]
   Why: [Reason/urgency]

This Week:
2. [Action to advance the conversation]
3. [Content to send based on conversation]

Topics for Next Conversation:
• [Topic 1 to address]
• [Topic 2 to explore]
• [Objection to preempt]

---

SUGGESTED FOLLOW-UP MESSAGE
===========================

Based on this conversation, here's a draft follow-up:

---
Subject: [Subject line]

[Personalized opening referencing specific moment from conversation]

[Address any open questions or commitments]

[Reinforce key value prop that resonated]

[Add missed value prop or proof point naturally]

[Clear next step / CTA]

[Sign off]
---

Want me to:
1. Refine this follow-up
2. Create a different style of follow-up
3. Generate content for a specific gap identified
4. Analyze another conversation
```

### Step 6: Offer Refinements

```
What would you like to do next?

1. Deep dive on a specific analysis area
2. Get more suggestions for [resonance / adherence / differentiation]
3. Refine the follow-up message
4. Generate content to address gaps
5. Compare to another conversation
6. Save insights to deal notes
7. Done

Your choice:
```

## Analysis Scoring Guide

### Resonance Score (1-10)
| Score | Meaning | Signals |
|-------|---------|---------|
| 9-10 | Strong engagement | Multiple questions, shared details, expressed urgency |
| 7-8 | Good engagement | Engaged responses, some interest signals |
| 5-6 | Neutral | Polite but non-committal |
| 3-4 | Weak | Short responses, delayed replies |
| 1-2 | Disengaged | Objections, pushback, ghosting |

### Adherence Score (1-10)
| Score | Meaning | Signals |
|-------|---------|---------|
| 9-10 | Full adherence | All playbook elements used appropriately |
| 7-8 | Good adherence | Most elements used, minor gaps |
| 5-6 | Partial adherence | Some elements used, key gaps |
| 3-4 | Weak adherence | Few elements used, off-playbook |
| 1-2 | Non-adherent | Didn't follow playbook approach |

### Differentiation Score (1-10)
| Score | Meaning | Signals |
|-------|---------|---------|
| 9-10 | Strong positioning | Clear differentiation, competitive landmines set |
| 7-8 | Good positioning | Some differentiation, mostly positioned |
| 5-6 | Neutral | Didn't address competition directly |
| 3-4 | Weak positioning | Competitor strengths uncountered |
| 1-2 | Poor positioning | Lost competitive ground |

## MCP Tools Used

### Research
- `find_person` - Identify external participants
- `find_company` - Get company context
- `qualify_person` - Match to persona

### Library Context
- `get_playbook` - Get playbook for adherence analysis
- `get_entity` - Get persona, competitor details
- `search_knowledge_base` - Find relevant messaging, proof points

### Content Generation
- `generate_content` - Draft follow-up messages
- `generate_email` - Generate email responses

## Input Formats Supported

### Email Thread
```
From: john@acme.com
To: me@company.com
Subject: Re: Quick question about your platform

[Message content]

---
On Jan 15, me@company.com wrote:
> [Previous message]
```

### Call Transcript
```
[00:00] Sales Rep: Thanks for joining...
[00:15] Prospect: Happy to be here...

or

Sales Rep: Thanks for joining...
John (Acme): Happy to be here...
```

### Chat/Message Thread
```
Me: Hey John, following up on our conversation
John: Thanks for reaching out
Me: Did you have a chance to review the proposal?
```

## Error Handling

**No Content Provided:**
> Please paste the content you'd like me to analyze, or provide a file path.
>
> I can analyze:
> - Email threads
> - Call transcripts
> - Chat messages
> - Meeting notes

**Cannot Identify Participants:**
> I couldn't identify the external participant.
>
> Can you tell me:
> 1. Who is the prospect? (name, company, title)
> 2. What stage is this deal in?
>
> This helps me match to the right persona and playbook.

**No Matching Playbook:**
> I couldn't find a playbook that matches this conversation.
>
> I'll analyze against general best practices, but for better insights:
> - Create a relevant playbook (/octave:library create playbook)
> - Or tell me which playbook should apply

## Related Skills

- `/octave:research` - Deep research on participants
- `/octave:generate` - Generate follow-up content
- `/octave:pmm` - Create collateral to address gaps
- `/octave:audit` - Ensure playbooks have complete guidance
- `/octave:pipeline` - Deal coaching based on conversation analysis
- `/octave:insights` - Aggregate patterns across many conversations
