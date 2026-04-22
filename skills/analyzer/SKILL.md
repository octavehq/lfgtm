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
