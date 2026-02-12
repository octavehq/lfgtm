---
name: explore-agents
description: Browse, understand, and run your saved Octave agents. Use when user says "show my agents", "list agents", "run an agent", "which agents do I have", or asks about saved agent configurations.
---

# /octave:explore-agents - Agent Manager

Browse your saved Octave agents, understand what each does, and run them directly from Claude Code. Agents are pre-configured AI workflows for email sequences, content generation, call prep, enrichment, and qualification.

## Usage

```
/octave:explore-agents [subcommand] [options]
```

## Subcommands

```
/octave:explore-agents                      # List all agents
/octave:explore-agents list                 # List all agents (same as above)
/octave:explore-agents list --type email    # List email agents only
/octave:explore-agents show <name>          # Show agent details
/octave:explore-agents run <name> [inputs]  # Run an agent
/octave:explore-agents suggest              # Suggest agents for your task
```

## Examples

```
/octave:explore-agents                                           # See all agents
/octave:explore-agents list --type email                         # Email sequence agents
/octave:explore-agents show "Enterprise Cold Outreach"           # Agent details
/octave:explore-agents run "Enterprise Cold Outreach" --to john@acme.com
/octave:explore-agents suggest "I need to write a cold email"    # Get agent recommendations
```

## Instructions

When the user runs `/octave:explore-agents`:

### Subcommand: list (default)

Show all available agents:

```
list_agents({
  limit: 50
})
```

**Output:**

```
YOUR OCTAVE AGENTS
==================

EMAIL AGENTS (4)
----------------

1. Enterprise Cold Outreach
   oId: ca_abc123
   Sequence: 4 emails
   Description: Cold outreach for enterprise prospects, focuses on ROI and case studies
   Run: /octave:explore-agents run "Enterprise Cold Outreach" --to <email>

2. SMB Quick Touch
   oId: ca_def456
   Sequence: 3 emails
   Description: Fast, value-focused sequence for SMB prospects
   Run: /octave:explore-agents run "SMB Quick Touch" --to <email>

3. Follow-Up Sequence
   oId: ca_ghi789
   Sequence: 3 emails
   Description: Re-engagement sequence for stalled deals
   Run: /octave:explore-agents run "Follow-Up Sequence" --to <email>

4. Inbound Response
   oId: ca_jkl012
   Sequence: 2 emails
   Description: Reply to inbound leads with personalized value prop
   Run: /octave:explore-agents run "Inbound Response" --to <email>

---

CONTENT AGENTS (2)
------------------

1. LinkedIn Message Writer
   oId: ca_mno345
   Description: Personalized LinkedIn connection requests and InMails
   Run: /octave:explore-agents run "LinkedIn Message Writer" --to <person>

2. Executive Brief Generator
   oId: ca_pqr678
   Description: One-page executive briefs for target accounts
   Run: /octave:explore-agents run "Executive Brief Generator" --company <domain>

---

CALL PREP AGENTS (1)
--------------------

1. Discovery Call Prep
   oId: cpa_stu901
   Description: Full discovery call preparation with questions and talking points
   Run: /octave:explore-agents run "Discovery Call Prep" --for <person>

---

ENRICHMENT AGENTS (2)
---------------------

1. Person Deep Dive
   oId: epa_vwx234
   Description: Comprehensive person research and profile
   Run: /octave:explore-agents run "Person Deep Dive" --person <email or linkedin>

2. Company Intelligence
   oId: eca_yza567
   Description: Full company research with competitive context
   Run: /octave:explore-agents run "Company Intelligence" --company <domain>

---

QUALIFICATION AGENTS (2)
------------------------

1. ICP Scorer
   oId: qpa_bcd890
   Description: Score person against ideal customer profile
   Run: /octave:explore-agents run "ICP Scorer" --person <email>

2. Account Fit Check
   oId: qca_efg123
   Description: Score company against target segments
   Run: /octave:explore-agents run "Account Fit Check" --company <domain>

---

Total: 11 agents

Tip: Use /octave:explore-agents suggest "<task>" to get agent recommendations
```

### Subcommand: list --type

Filter by agent type:

```
list_agents({
  type: "EMAIL"  // or "CONTENT", "CALL_PREP", "ENRICH_PERSON", "ENRICH_COMPANY", "QUALIFY_PERSON", "QUALIFY_COMPANY"
})
```

**Types:**
- `email` - Email sequence agents
- `content` - Content generation agents
- `call-prep` - Call preparation agents
- `enrich` - Enrichment agents (person + company)
- `qualify` - Qualification agents (person + company)

### Subcommand: show <name>

Show detailed information about an agent:

```
Agent: Enterprise Cold Outreach
===============================
oId: ca_abc123
Type: EMAIL
Created: 2025-12-01
Last Updated: 2026-01-15

Description:
Cold outreach sequence for enterprise prospects. Focuses on ROI,
executive pain points, and enterprise-grade proof points. Uses
formal professional tone.

Configuration:
- Sequence Length: 4 emails
- Playbook: Enterprise Sales (pb_xyz789)
- Persona Target: CTO, VP Engineering
- Brand Voice: Enterprise Professional
- Writing Style: Consultative

Email Flow:
1. Initial outreach - Pain point + social proof
2. Value follow-up - ROI story + case study
3. Insight share - Industry trend + offer
4. Breakup - Direct ask + value recap

Best For:
- Enterprise prospects ($1M+ revenue)
- Technical decision makers
- Cold outreach (no prior relationship)

---

Run this agent:
/octave:explore-agents run "Enterprise Cold Outreach" --to john@acme.com

Or with context:
/octave:explore-agents run "Enterprise Cold Outreach" --to john@acme.com --context "Met at conference"
```

### Subcommand: run <name>

Run an agent with the specified inputs:

**For Email Agents:**
```
/octave:explore-agents run "Enterprise Cold Outreach" --to john@acme.com
/octave:explore-agents run "Enterprise Cold Outreach" --to "John Smith" --company acme.com
/octave:explore-agents run "Enterprise Cold Outreach" --to john@acme.com --context "Referral from Sarah"
```

Maps to:
```
run_email_agent({
  agent: "Enterprise Cold Outreach",
  person: {
    email: "john@acme.com",
    // or
    firstName: "John",
    lastName: "Smith",
    companyDomain: "acme.com"
  },
  allEmailsContext: "Referral from Sarah"  // if --context provided
})
```

**For Content Agents:**
```
/octave:explore-agents run "LinkedIn Message Writer" --to john@acme.com
/octave:explore-agents run "Executive Brief Generator" --company acme.com
```

Maps to:
```
run_content_agent({
  agent: "LinkedIn Message Writer",
  person: { email: "john@acme.com" }
})

run_content_agent({
  agent: "Executive Brief Generator",
  company: { domain: "acme.com" }
})
```

**For Call Prep Agents:**
```
/octave:explore-agents run "Discovery Call Prep" --for john@acme.com
/octave:explore-agents run "Discovery Call Prep" --for john@acme.com --context "Follow-up from demo"
```

Maps to:
```
run_call_prep_agent({
  agent: "Discovery Call Prep",
  person: { email: "john@acme.com" },
  meetingContext: "Follow-up from demo"
})
```

**For Enrichment Agents:**
```
/octave:explore-agents run "Person Deep Dive" --person john@acme.com
/octave:explore-agents run "Company Intelligence" --company acme.com
```

Maps to:
```
run_enrich_person_agent({
  agent: "Person Deep Dive",
  person: { email: "john@acme.com" }
})

run_enrich_company_agent({
  agent: "Company Intelligence",
  company: { domain: "acme.com" }
})
```

**For Qualification Agents:**
```
/octave:explore-agents run "ICP Scorer" --person john@acme.com
/octave:explore-agents run "Account Fit Check" --company acme.com
```

Maps to:
```
run_qualify_person_agent({
  agent: "ICP Scorer",
  person: { email: "john@acme.com" }
})

run_qualify_company_agent({
  agent: "Account Fit Check",
  company: { domain: "acme.com" }
})
```

**Output Format:**

After running an agent, present the output clearly:

```
AGENT OUTPUT: Enterprise Cold Outreach
======================================
Target: John Smith (john@acme.com)
Company: Acme Corp

---

EMAIL 1: Initial Outreach
-------------------------
Subject: Reducing engineering overhead at Acme

Hi John,

[Generated email content...]

Best,
[Sender]

---

EMAIL 2: Value Follow-Up (Day 3)
--------------------------------
Subject: How TechCorp cut deployment time by 60%

Hi John,

[Generated email content...]

---

[Continue for all emails in sequence]

---

Personalization used:
- Company: Acme Corp (450 employees, Series C)
- Role: VP Engineering
- Matched persona: VP Engineering
- Playbook: Enterprise Sales

Copy these to your outreach tool, or would you like me to adjust any?
```

### Subcommand: suggest

Recommend agents based on task description:

```
/octave:explore-agents suggest "I need to write a cold email to a CTO"
```

**Process:**
1. Parse the task description
2. Match to relevant agent types
3. Return ranked recommendations

**Output:**

```
AGENT RECOMMENDATIONS
=====================
Task: "Write a cold email to a CTO"

Best Matches:
-------------

1. Enterprise Cold Outreach (95% match)
   Type: Email
   Why: Designed for technical decision makers, CTO persona targeting

   Run: /octave:explore-agents run "Enterprise Cold Outreach" --to <cto email>

2. SMB Quick Touch (70% match)
   Type: Email
   Why: Good for email sequences, but less CTO-focused

   Run: /octave:explore-agents run "SMB Quick Touch" --to <email>

---

Alternative Approach:
If you need more control, use /octave:generate email instead.
This generates emails without a pre-configured agent template.

---

Would you like me to run one of these agents?
```

### Smart Agent Selection

When user describes a task without using `/octave:explore-agents`, consider suggesting relevant agents:

```
User: "I need to send a cold email to the CTO at acme.com"

You: I can help with that! You have an agent that's perfect for this:

Enterprise Cold Outreach - designed for technical decision makers

Would you like me to:
1. Run the "Enterprise Cold Outreach" agent for this CTO
2. Generate a custom email instead (more control, less consistency)
3. Show me other email agents first

Your choice:
```

## Agent Types Reference

| Type | MCP Tool | Purpose |
|------|----------|---------|
| EMAIL | `run_email_agent` | Multi-step email sequences |
| CONTENT | `run_content_agent` | General content (LinkedIn, briefs) |
| CALL_PREP | `run_call_prep_agent` | Meeting preparation |
| ENRICH_PERSON | `run_enrich_person_agent` | Person research |
| ENRICH_COMPANY | `run_enrich_company_agent` | Company research |
| QUALIFY_PERSON | `run_qualify_person_agent` | Person ICP scoring |
| QUALIFY_COMPANY | `run_qualify_company_agent` | Company ICP scoring |

## MCP Tools Used

### Agent Management
- `list_agents` - List all agents with optional type filter

### Agent Execution
- `run_email_agent` - Run email sequence agent
- `run_content_agent` - Run content generation agent
- `run_call_prep_agent` - Run call prep agent
- `run_enrich_person_agent` - Run person enrichment agent
- `run_enrich_company_agent` - Run company enrichment agent
- `run_qualify_person_agent` - Run person qualification agent
- `run_qualify_company_agent` - Run company qualification agent

## Error Handling

**Agent Not Found:**
> Agent "XYZ" not found.
>
> Available agents:
> - Enterprise Cold Outreach
> - SMB Quick Touch
> - [list others...]
>
> Use /octave:explore-agents list to see all agents.

**Missing Required Input:**
> Agent "Enterprise Cold Outreach" requires a person to target.
>
> Usage: /octave:explore-agents run "Enterprise Cold Outreach" --to <email or name>
>
> Examples:
> - /octave:explore-agents run "Enterprise Cold Outreach" --to john@acme.com
> - /octave:explore-agents run "Enterprise Cold Outreach" --to "John Smith" --company acme.com

**No Agents Configured:**
> You don't have any agents configured yet.
>
> Agents are created in the Octave web app:
> 1. Go to Agents in Octave
> 2. Create a new agent
> 3. Configure its settings
>
> Once created, you can run them from here.
>
> In the meantime, use /octave:generate for one-off content generation.

## Related Skills

- `/octave:generate` - Generate content with 3-way mode choice (saved agent, Octave default, Claude direct). Its `--mode agent` routes through agent discovery and execution — same agents you manage here.
- `/octave:research` - Research before running agents
- `/octave:pmm` - Create content that could become agent templates
