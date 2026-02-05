# Octave Plugin Examples

Real-world examples of how to use the Octave Claude Code plugin for common GTM workflows.

## Quick Reference

| Task | Command |
|------|---------|
| Check workspace status | `/octave:workspace` |
| Browse personas | `/octave:library list personas` |
| Prep for a call | `/octave:research john@acme.com --for discovery` |
| Generate an email | `/octave:generate email --to "John at Acme" --about "reducing costs"` |
| Analyze a conversation | `/octave:analyzer` |
| See what objections are trending | `/octave:insights --type objections` |
| Understand why you're losing deals | `/octave:wins-losses --status lost` |
| Run a saved agent | `/octave:explore-agents run "Enterprise Outreach" --to john@acme.com` |

---

## Getting Started

### Check Your Workspace

```
/octave:workspace
```

Shows your current Octave MCP server connection status.

---

## Library Management

### Browse Your Library

```
# List all personas
/octave:library list personas

# List playbooks with details
/octave:library list playbooks --detailed

# Search across everything
/octave:library search "enterprise security"

# View a specific entity
/octave:library show pe_abc123
```

### Create New Entities

```
# Create a new persona
/octave:library create persona "VP of Product"

# Create with context
/octave:library create persona "DevOps Engineer" --sources "https://example.com/devops-guide"

# Create a new playbook (will prompt for offering selection)
/octave:library create playbook "Healthcare Vertical"
```

When creating a playbook, you'll be asked to select which product/service it's associated with.

### Update Existing Entities

```
# Update a persona
/octave:library update pe_abc123 --instructions "Add AI adoption as a key priority"

# Update playbook value props
/octave:library update pb_xyz789 --instructions "Make the CTO value prop focus more on cost savings"
```

### Audit Your Library

```
# Full audit
/octave:audit

# Focus on specific entity type
/octave:audit --type personas

# Interactive fix mode
/octave:audit --fix
```

Example output:
```
Library Audit Report
====================
Health Score: 72/100

CRITICAL ISSUES (2)
- Playbook "Enterprise Sales" has no linked personas
- No proof points defined for Healthcare segment

WARNINGS (5)
- Persona "CTO" missing pain points
- Competitor "Acme" not updated in 90 days
- Similar personas detected: "VP Sales" and "Vice President of Sales"

Run /octave:audit --fix to address issues interactively.
```

---

## Research & Preparation

### Discovery Call Prep

```
/octave:research john@acme.com --for discovery
```

Returns:
- Person and company profile
- Matched persona and playbook
- Recommended discovery questions
- Pain points to probe
- Potential objections to prepare for
- Relevant proof points

### Demo Prep

```
/octave:research acme.com --for demo
```

Returns:
- Audience analysis
- Recommended demo flow
- Use cases to highlight
- Proof points to weave in
- Objections to prepare for
- Questions to ask during demo

### Outreach Prep

```
/octave:research john@acme.com --for outreach
```

Returns:
- Personalization hooks
- ICP fit analysis
- Multiple outreach angles
- Recommended CTAs
- Multi-channel sequence suggestion

### Pipeline/Deal Review

```
/octave:research "Acme deal" --for pipeline-review
```

Returns:
- Deal health assessment
- Stakeholder map
- Deal gaps checklist
- Recommended next moves
- Risk mitigation strategies

---

## Content Generation

### Quick Email Generation

```
# Basic email
/octave:generate email --to "John Smith at Acme" --about "reducing deployment time"

# With persona context
/octave:generate email --to "john@acme.com" --persona "CTO" --playbook "Enterprise DevOps"

# LinkedIn message
/octave:generate linkedin --to "Sarah Chen, VP Eng" --about "developer productivity"
```

### Using Saved Agents

```
# List available agents
/octave:explore-agents

# Run an email agent
/octave:explore-agents run "Enterprise Cold Outreach" --to john@acme.com

# Run with additional context
/octave:explore-agents run "Enterprise Cold Outreach" --to john@acme.com --context "Met at AWS re:Invent"

# Get agent suggestions
/octave:explore-agents suggest "I need to re-engage a stalled deal"
```

### PMM Content Creation

```
# Create a one-pager
/octave:pmm one-pager

# Create a battlecard
/octave:pmm battlecard --competitor "Salesforce"

# Create a case study
/octave:pmm case-study

# Create landing page copy
/octave:pmm landing-page
```

Example battlecard flow:
```
/octave:pmm battlecard

> Which competitor?
Competitor A

> Target audience for this battlecard?
Sales reps

[Generates comprehensive battlecard with:]
- Quick positioning
- Where we win / where they win
- Common objections + responses
- Trap questions to ask
- Proof points to use
```

---

## Prospecting

### Find ICP-Fit Companies

```
# Using a playbook's ICP
/octave:prospector --playbook "Enterprise Sales"

# Filter by segment
/octave:prospector --segment "Healthcare"

# Find similar companies
/octave:prospector --similar-to stripe.com
```

### Find Decision Makers

```
# Find people at a specific company
/octave:prospector --company acme.com

# Filter by persona
/octave:prospector --persona "CTO" --segment "Enterprise SaaS"
```

Example output:
```
Prospect Results
================

1. TechCorp (techcorp.com)
   Fit Score: 92/100 - EXCELLENT FIT

   Why They Fit:
   ✓ Matches segment: "Scaling SaaS Companies"
   ✓ Right size (450 employees)
   ✓ Growth signals: 50% headcount growth YoY

   Key Contacts:
   - Sarah Chen, CTO
   - Mike Johnson, VP Engineering

Scale This Search (Apollo Filters):
- Industry: Software Development, SaaS
- Employee Count: 100-1000
- Technologies: Kubernetes, AWS
```

---

## Brainstorming & Ideation

### Campaign Ideas

```
/octave:brainstorm campaigns for enterprise
```

Returns 3-5 campaign concepts with:
- Hook and messaging
- Why it works (tied to library)
- Sequence outline
- Recommended CTA

### Playbook Pack Generation

```
/octave:brainstorm playbook pack
```

Analyzes your TAM coverage and suggests new playbooks to fill gaps.

### Lead Magnet Ideas

```
/octave:brainstorm lead magnets for CTOs
```

Returns ideas like:
- Interactive assessments
- ROI calculators
- Industry benchmark reports
- How-to guides

### CTA & Offer Ideas

```
/octave:brainstorm CTAs for CFOs
```

Returns tiered CTAs:
- Low commitment (download resource)
- Medium commitment (get custom analysis)
- High commitment (start pilot)

---

## Conversation Analysis

### Analyze an Email Thread

```
/octave:analyzer --type email
```

Then paste your email thread. Returns:
- Resonance analysis (what landed, what didn't)
- Adherence analysis (did you follow the playbook?)
- Differentiation analysis (competitive positioning)
- Action items and follow-up suggestions
- Draft follow-up message

### Analyze a Call Transcript

```
/octave:analyzer --type call
```

Then paste your transcript. Returns similar analysis plus:
- Speaker-by-speaker breakdown
- Questions asked vs recommended
- Objections raised and how they were handled

Example output:
```
CONVERSATION ANALYSIS
=====================

RESONANCE: 7/10 - Good Engagement
✓ Pain point "manual processes" resonated strongly
✓ ROI story generated follow-up questions
✗ Security messaging didn't land

ADHERENCE: 6/10 - Partial
✓ Used playbook value props
✗ Missed qualifying questions about budget
✗ Didn't set competitive landmines

DIFFERENTIATION: 5/10 - Neutral
⚠ Competitor mentioned but not addressed

RECOMMENDED FOLLOW-UP:
[Draft email addressing gaps...]
```

---

## Field Intelligence

### See What's Trending

```
# Overview of recent insights
/octave:insights

# Focus on objections
/octave:insights --type objections

# This month's pain points
/octave:insights --type pain-points --period month

# Insights from CTO conversations
/octave:insights --persona "CTO"
```

Example output:
```
FIELD INSIGHTS: Last 30 Days
============================

TOP OBJECTIONS (12 instances)
1. "Pricing seems high" (5x) ↑ Increasing
2. "Implementation concerns" (4x) → Stable
3. "Need more stakeholders" (3x) ↓ Decreasing

Library Gap: Objection #1 not addressed in playbooks
→ Suggestion: Add pricing justification to Enterprise playbook

TOP PAIN POINTS (18 instances)
1. "Manual processes" (7x) ✓ Matches persona
2. "Data silos" (6x) ⚠ Not in personas - consider adding
```

### Win/Loss Analysis

```
# Full report
/octave:wins-losses

# Focus on losses
/octave:wins-losses --status lost

# Deals involving specific competitor
/octave:wins-losses --competitor "Salesforce"

# Deep dive on specific deal
/octave:wins-losses --company acme.com
```

Example output:
```
WIN/LOSS ANALYSIS: Q4
=====================

Win Rate: 34% (down from 38%)
Deals Won: 12 ($1.2M)
Deals Lost: 23 ($2.8M)

WHY WE WON:
1. Strong champion (67% of wins)
2. Clear ROI story (58% of wins)
3. Competitive differentiation (42% of wins)

WHY WE LOST:
1. Lost to competitor (43% of losses)
   - Competitor A: 5 deals - lost on price
   - Competitor B: 3 deals - existing relationship
2. No decision (35% of losses)
3. Unresolved objections (22% of losses)

RECOMMENDATIONS:
1. Address Competitor A pricing gap
2. Improve qualification on budget
3. Double down on champion development
```

---

## Common Workflows

### New Prospect Research → Outreach

```
# 1. Research the prospect
/octave:research john@acme.com --for outreach

# 2. Generate personalized email
/octave:generate email --to john@acme.com --about "the pain points we discussed"

# Or use a saved agent
/octave:explore-agents run "Enterprise Cold Outreach" --to john@acme.com
```

### Pre-Call Preparation

```
# 1. Research attendees and company
/octave:research john@acme.com --for discovery

# 2. Review relevant playbook
/octave:library show pb_enterprise

# 3. Check recent insights for this persona
/octave:insights --persona "CTO"
```

### Post-Call Follow-Up

```
# 1. Analyze the call
/octave:analyzer --type call
[paste transcript]

# 2. Generate follow-up based on analysis
# (The analyzer suggests a draft follow-up)

# 3. Update library if you learned something new
/octave:library update pe_cto --instructions "Add 'AI governance' as emerging concern"
```

### Deal Review

```
# 1. Review deal status and history
/octave:wins-losses --company acme.com

# 2. Research additional stakeholders
/octave:prospector --company acme.com

# 3. Generate re-engagement content
/octave:explore-agents run "Follow-Up Sequence" --to john@acme.com --context "Stalled after demo"
```

### Library Maintenance

```
# 1. Audit library health
/octave:audit

# 2. Review field insights
/octave:insights

# 3. Apply learnings to library
/octave:library update pe_cto --instructions "Add objection: 'AI governance concerns'"
```

### Competitive Intelligence Update

```
# 1. See how competitor is coming up in deals
/octave:wins-losses --competitor "Competitor A"

# 2. Review current battlecard
/octave:library show cp_competitor_a

# 3. Update with new intelligence
/octave:pmm battlecard --competitor "Competitor A"
# Or
/octave:library update cp_competitor_a --instructions "Add new pricing objection handling"
```

---

## Tips & Best Practices

### Get the Most from Research

- Always specify the occasion (`--for discovery`, `--for demo`, etc.)
- The more context you provide, the better the output
- Use research output to inform your generate commands

### Effective Library Management

- Run `/octave:audit` weekly to catch issues early
- Use `/octave:insights` to discover what to add to your library
- Keep competitor information fresh (update monthly)

### Content Generation Quality

- Reference specific personas and playbooks for consistency
- Use saved agents for repeatable, high-quality output
- Review and customize generated content before sending

### Staying Informed

- Check `/octave:insights` regularly to see what's trending
- Use `/octave:wins-losses` monthly for pattern analysis
- Apply learnings back to your library to improve over time
