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

#### Discovery Call Prep

See [discovery-call-prep.md](references/discovery-call-prep.md) for the discovery call prep output template.

#### Demo Prep

See [demo-prep.md](references/demo-prep.md) for the demo prep output template.

#### Outreach Prep

See [outreach-prep.md](references/outreach-prep.md) for the outreach prep output template.

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
