---
name: call-analyzer
description: Analyze email threads, call transcripts, and conversations for resonance, adherence to messaging, and competitive differentiation. Use when user says "analyze this call", "how did the email land", "score this thread", "conversation analysis", or pastes conversation content to evaluate.
---

# /octave:call-analyzer - Conversation Analysis

Analyze email threads, call transcripts, and sales conversations against your Octave library. Evaluates messaging resonance, Motion ICP narrative adherence, and competitive differentiation. Provides actionable insights, suggested improvements, and draft follow-ups.

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
/octave:call-analyzer [--type email|call|chat]
```

## Examples

```
/octave:call-analyzer                              # Interactive - paste content
/octave:call-analyzer --type email                 # Analyze email thread
/octave:call-analyzer --type call                  # Analyze call transcript
```

## Instructions

When the user runs `/octave:call-analyzer`:

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
# Find the right Motion + Motion ICP cell for this conversation
list_motions()
list_motion_icps({ motionOId: "<motion_oId>" })
find_motion_icp({ motionIcpOId: "<motion_icp_oId>", includeLearnings: true })
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
  entityTypes: ["persona", "use_case"]
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
*Did we follow the Motion ICP narrative? What did we miss?*

Use MCP to get the Motion ICP cell narrative:
```
# Get the matched Motion ICP cell (persona × segment)
find_motion_icp({ motionIcpOId: "<matched_motion_icp_oId>", includeLearnings: true })
```

Compare conversation to the Motion ICP narrative:
- Strategic narrative alignment
- Benefits and impacts delivered vs. available
- Pains and consequences surfaced
- Methodology / qualifying questions asked
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

See [conversation-output-template.md](references/conversation-output-template.md) for the Conversation Analysis output template.

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

For option 5, pull the other conversation with `search_call_transcripts({ companyDomain, query: "<topic>" })` instead of asking the user to paste it again — it returns verbatim, speaker-attributed moments across every indexed call with that account, so you can compare this thread against what was actually said on past calls.

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
| 9-10 | Full adherence | All Motion ICP narrative elements used appropriately |
| 7-8 | Good adherence | Most elements used, minor gaps |
| 5-6 | Partial adherence | Some elements used, key gaps |
| 3-4 | Weak adherence | Few elements used, off-narrative |
| 1-2 | Non-adherent | Didn't follow the Motion ICP narrative |

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
- `list_motions` - List all Motions in the workspace
- `list_motion_icps` - List Motion ICP cells for a Motion
- `find_motion_icp` - Get full Motion ICP cell narrative (Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References) for adherence analysis
- `get_entity` - Get persona, competitor details
- `search_knowledge_base` - Find relevant messaging, proof points
- `search_call_transcripts` - Pull verbatim moments from other calls with this account (or this persona) to compare against the pasted conversation
- `get_entity_evidence` - Real customer language backing a matched persona's pain point or a competitor's claim, for the resonance/differentiation write-up

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
> This helps me match to the right Motion ICP cell.

**No Matching Motion ICP:**
> I couldn't find a Motion ICP cell that matches this conversation.
>
> I'll analyze against general best practices, but for better insights:
> - Tell me which Motion (offering + motion type) this falls under
> - Or create a Motion for this offering if one don't exist yet

## Related Skills

- `/octave:research` - Deep research on participants
- `/octave:generate` - Generate follow-up content
- `/octave:one-pager` - Create collateral to address gaps
- `/octave:audit` - Ensure Motion ICP cells have complete narratives
- `/octave:pipeline` - Deal coaching based on conversation analysis
- `/octave:insights` - Aggregate patterns across many conversations
