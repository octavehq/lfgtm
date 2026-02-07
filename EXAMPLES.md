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
| Plan a multi-channel campaign | `/octave:campaign "Q1 pipeline push"` |
| Build a messaging framework | `/octave:messaging framework` |
| Create a competitive battlecard | `/octave:battlecard battlecard --competitor "Acme"` |
| Plan an account approach | `/octave:abm acme.com` |
| Coach on a stalled deal | `/octave:pipeline stalled acme.com` |
| Generate enablement materials | `/octave:enablement objections --persona "CTO"` |
| Plan a product launch | `/octave:launch "New AI feature"` |
| Refine your ICP | `/octave:icp-refine --period 90` |
| See what objections are trending | `/octave:insights --type objections` |
| Understand why you're losing deals | `/octave:wins-losses --status lost` |
| Run a saved agent | `/octave:explore-agents run "Enterprise Outreach" --to john@acme.com` |
| Run a multi-step workflow | `/octave:workflow run "Full Outbound Pipeline" --company acme.com` |

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

## Campaign Planning

### Plan a Multi-Channel Campaign

```
# Interactive mode
/octave:campaign

# Campaign around a topic
/octave:campaign "AI feature launch"

# Target specific persona and channels
/octave:campaign "Q1 pipeline push" --persona "VP Engineering" --channels email,linkedin,ads,social

# Competitive displacement campaign
/octave:campaign "competitive displacement" --playbook "Enterprise"
```

Example flow:
```
/octave:campaign "Q1 pipeline push" --persona "CTO"

[Gathers library intelligence: persona, playbooks, proof points, brand voice]

CAMPAIGN PLAN: Q1 Pipeline Acceleration
========================================

OBJECTIVE: Drive discovery meetings with CTOs at enterprise SaaS companies

TARGET AUDIENCE: CTO persona, Enterprise segment
STRATEGIC ANGLE: Lead with "engineering velocity" value prop
PROOF POINTS: TechCorp case study (40% deployment speed increase)

CHANNEL PLAN:
| Channel   | Timing    | Purpose                |
|-----------|-----------|------------------------|
| Email     | Week 1-3  | Primary outreach       |
| LinkedIn  | Week 1-4  | Warm + thought leader  |
| Social    | Week 1-4  | Awareness              |
| Ads       | Week 2-4  | Retargeting            |

Ready to generate content for each channel? [Y/n]

[Generates: 4-email sequence, LinkedIn messages + post, 5 social posts, 3 ad variants]
```

---

## Messaging & Positioning

### Build a Messaging Framework

```
# Full messaging framework
/octave:messaging framework

# Positioning statement
/octave:messaging positioning --product "Platform"

# Persona x use case messaging matrix
/octave:messaging matrix

# Elevator pitches in multiple lengths
/octave:messaging elevator

# Company narrative arc
/octave:messaging narrative

# Value proposition hierarchy
/octave:messaging value-props
```

Example output:
```
/octave:messaging framework --product "Platform"

MESSAGING FRAMEWORK: Platform
===============================

CORE POSITIONING
For [revenue teams] who [struggle with manual research and generic outreach],
[Platform] is a [GTM intelligence engine] that [makes every prospect
interaction smarter]. Unlike [static templates and tribal knowledge],
we [learn from every conversation to improve over time].

PILLAR 1: Intelligence Depth
Core Message: "Know more about your prospects than they expect"
...

PILLAR 2: Living Knowledge
Core Message: "Your GTM strategy gets smarter with every deal"
...

KEY MESSAGES BY AUDIENCE
For CTO: Lead with engineering efficiency...
For VP Sales: Lead with pipeline velocity...
```

---

## Competitive Intelligence

### Create a Battlecard

```
# Full battlecard
/octave:battlecard battlecard --competitor "Acme"

# Displacement campaign
/octave:battlecard displacement --competitor "Acme"

# Trap questions
/octave:battlecard traps --competitor "Acme"

# Objection counters
/octave:battlecard objections --competitor "Acme"

# Side-by-side comparison
/octave:battlecard compare --competitor "Acme"

# Full competitive landscape
/octave:battlecard landscape
```

Example battlecard output:
```
BATTLECARD: Platform vs Acme
==============================

QUICK POSITIONING
When you hear: "Acme"
Lead with: "Acme automates content, but without real research depth"

WHERE WE WIN
| Capability      | Us                    | Them              |
|-----------------|-----------------------|-------------------|
| Research Depth  | ✓ Autonomous agents   | ✗ CRM data only   |
| Qualification   | ✓ Signal-based scoring| ~ Basic scoring   |
| Personalization | ✓ Research-grounded   | ✗ Template-based  |

COMMON OBJECTIONS
"Acme is cheaper"
→ "Compare total cost including the research tools you'd need alongside..."

TRAP QUESTIONS
1. "How does your current tool research prospects beyond CRM data?"
   Why: Exposes their lack of autonomous research agents
```

---

## Account-Based Planning

### Create an Account Plan

```
# Full account plan
/octave:abm acme.com

# Quick assessment
/octave:abm acme.com --depth quick

# Map more stakeholders
/octave:abm acme.com --stakeholders 8

# Use specific playbook
/octave:abm acme.com --playbook "Enterprise"
```

Example output:
```
ACCOUNT PLAN: Acme Corp
=========================

ICP FIT: 87/100 (Excellent)
Segment: Enterprise SaaS

BUYING COMMITTEE
| Name       | Title          | Persona    | Buying Role    |
|------------|----------------|------------|----------------|
| Sarah Chen | CTO            | CTO        | Economic Buyer |
| Mike Ross  | VP Engineering | VP Eng     | Champion       |
| Lisa Park  | Dir Security   | Security   | Evaluator      |

ENGAGEMENT STRATEGY
Entry Point: Mike Ross (strongest persona match, likely champion)
Sequence: LinkedIn connect → Personalized email → Discovery call

[Generates tailored outreach for the recommended entry point]
```

---

## Deal Coaching

### Get Deal-Specific Coaching

```
# Stalled deal
/octave:pipeline stalled acme.com

# Multi-thread to more stakeholders
/octave:pipeline multi-thread acme.com

# Competitor entered the deal
/octave:pipeline competitive acme.com --competitor "Acme"

# Need executive engagement
/octave:pipeline executive acme.com

# Closing strategy
/octave:pipeline close acme.com

# Customer expansion
/octave:pipeline expand acme.com
```

Example stalled deal coaching:
```
/octave:pipeline stalled acme.com --contact john@acme.com

DEAL COACHING: STALLED DEAL
============================
Account: Acme Corp | Contact: John Smith, VP Eng
Stage: Evaluation | Days in Stage: 23 (avg: 12)

DIAGNOSIS
Likely Reasons for Stall:
1. Champion went quiet after competitor demo (last email opened, no reply)
2. No economic buyer engaged yet
3. Q1 budget cycle may be blocking

RE-ENGAGEMENT STRATEGY
Approach 1: Share the TechCorp case study (similar company, 40% improvement)
Approach 2: Reach out to Sarah Chen (CTO) with executive angle
Approach 3: Offer a custom ROI analysis as value-add

[Generates draft re-engagement email]
```

---

## Launch Planning

### Plan a Product Launch

```
# Interactive mode
/octave:launch

# Feature launch
/octave:launch "New AI analytics dashboard" --type feature

# Product launch
/octave:launch "Enterprise tier" --type product

# Partnership announcement
/octave:launch "Salesforce integration" --type partnership
```

Example output:
```
/octave:launch "AI Analytics Dashboard" --type feature

LAUNCH PLAN: AI Analytics Dashboard
=====================================

POSITIONING: Extends our intelligence platform with real-time pipeline insights

AUDIENCE PRIORITIZATION
| Priority | Persona       | Key Message                      |
|----------|---------------|----------------------------------|
| 1        | VP Sales      | "See pipeline health in real-time"|
| 2        | RevOps        | "Data-driven forecasting"        |
| 3        | CTO           | "AI-powered revenue intelligence"|

CONTENT KIT
✓ Customer announcement email
✓ Prospect outreach email
✓ Blog post (1,200 words)
✓ 4 social posts
✓ Sales enablement one-pager
✓ Customer FAQ (8 questions)
✓ Competitive talking points
```

---

## Sales Enablement

### Generate Enablement Materials

```
# Quick reference card
/octave:enablement quick-ref --product "Platform"

# Objection handling guide (from real conversations)
/octave:enablement objections --persona "CTO"

# Discovery question bank
/octave:enablement discovery --persona "VP Sales"

# Competitive cheat sheet
/octave:enablement competitive-sheet

# New hire onboarding kit
/octave:enablement onboarding

# Persona deep-dive for reps
/octave:enablement persona-guide --persona "CTO"

# Playbook quick reference
/octave:enablement playbook-summary --playbook "Enterprise"
```

Example objection guide:
```
/octave:enablement objections

OBJECTION HANDLING GUIDE
=========================

PRICING OBJECTIONS
"It's too expensive"
Frequency: High (mentioned in 12 conversations last quarter)
Response: "Let's look at total cost of ownership. Most teams spend..."
Proof: "TechCorp saved $X in research tool costs alone"
From the field: Won deal at FinCorp after demonstrating 8x ROI

"We don't have budget"
Response: "What if we could show ROI within the first quarter?..."

COMPETITIVE OBJECTIONS
"We already use [Competitor]"
Frequency: Medium
Response: "What's your team spending on research alongside that?"
```

---

## ICP Refinement

### Analyze and Refine Your ICP

```
# Full ICP analysis (last 180 days)
/octave:icp-refine

# Last quarter only
/octave:icp-refine --period 90

# Focus on wins only
/octave:icp-refine --focus wins

# Specific segment
/octave:icp-refine --segment "Enterprise"
```

Example output:
```
ICP REFINEMENT REPORT
======================
Period: Last 90 days | Deals: 15 won, 22 lost | Win Rate: 41%

WINNING CUSTOMER PROFILE
Industry: SaaS (60%), FinTech (25%), HealthTech (15%)
Sweet Spot: 200-800 employees
Common Win Factors:
✓ Had a technical champion (80% of wins)
✓ Were replacing an existing tool (67% of wins)

GAPS: DEFINED ICP vs. REALITY
⚠ FinTech winning but not in current ICP → Recommend: Add to segment
⚠ Companies <100 employees losing at 85% → Recommend: Add as disqualification
⚠ "Active evaluation" signal appears in 73% of wins → Add to qualification

RECOMMENDED UPDATES
1. Add FinTech to Enterprise segment
2. Set minimum company size to 100
3. Add "active tool evaluation" as qualification signal
```

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

# Create a case study
/octave:pmm case-study

# Create landing page copy
/octave:pmm landing-page

# Create a blog post
/octave:pmm blog
```

### Content Repurposing

```
# Repurpose text for a different persona
/octave:repurpose "Our platform reduces deployment time..." --persona "CFO"

# Repurpose a file for a different channel
/octave:repurpose ./content/whitepaper.md --channel "email sequence"

# Repurpose from URL
/octave:repurpose https://blog.company.com/launch-post --persona "CTO"
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

---

## Brainstorming & Ideation

### Campaign Ideas

```
/octave:brainstorm campaigns for enterprise
```

### Playbook Pack Generation

```
/octave:brainstorm playbook pack
```

### Lead Magnet Ideas

```
/octave:brainstorm lead magnets for CTOs
```

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

---

## Workflows

Multi-step workflows chain research, qualification, and generation into reusable recipes.

### Run a Template Workflow

```
# Full outbound pipeline: research → qualify → find contacts → email
/octave:workflow run "Full Outbound Pipeline" --company acme.com

# Deep account research dossier
/octave:workflow run "Account-Based Research" --company stripe.com

# Competitive deal prep with positioning
/octave:workflow run "Competitive Deal Prep" --company acme.com --contact john@acme.com --competitor "Salesforce"

# Find people matching a persona and generate outreach
/octave:workflow run "Persona-Targeted Outreach" --persona "CTO" --industry "SaaS"

# Enter a new market segment
/octave:workflow run "New Market Entry" --market "Healthcare SaaS, 100-500 employees"

# Respond to a competitive move
/octave:workflow run "Competitive Response" --competitor "Acme" --trigger "launched AI feature"

# Accelerate a high-value deal
/octave:workflow run "Deal Acceleration" --company acme.com --contact john@acme.com

# Quarterly GTM review
/octave:workflow run "Quarterly GTM Review" --period 90

# Content sprint around a theme
/octave:workflow run "Content Sprint" --theme "AI-powered analytics" --persona "CTO"
```

### Run in Auto Mode

Skip confirmations and run all steps automatically:

```
/octave:workflow run "Full Outbound Pipeline" --company acme.com --auto
```

### Create a Custom Workflow

```
/octave:workflow create
```

Example interaction:
```
> What should this workflow accomplish?
"Research a company, find their security team, and generate a security-focused email sequence"

> Here's a suggested workflow:
  1. Research company (enrich_company)
  2. Qualify company (qualify_company)
  3. Find security team (find_person)
  4. Enrich top contacts (enrich_person)
  5. Generate security-focused emails (generate_email)

  Look good? (yes/adjust)

> yes

Saved to: ~/.octave/workflows/security-team-outreach.workflow.md
Run it: /octave:workflow run "Security Team Outreach" --company acme.com
```

### List Available Workflows

```
/octave:workflow list
```

Shows both template workflows (shipped with the plugin) and your custom workflows (saved to `~/.octave/workflows/`).

---

## Common Multi-Skill Workflows

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

### Competitive Deal Response

```
# 1. Get competitive intel
/octave:battlecard battlecard --competitor "Acme"

# 2. Generate displacement outreach
/octave:battlecard displacement --competitor "Acme"

# 3. Update the team
/octave:enablement competitive-sheet
```

### Launch → Campaign → Enable

```
# 1. Plan the launch
/octave:launch "New AI Feature" --type feature

# 2. Build the campaign
/octave:campaign "AI Feature Launch" --channels email,linkedin,social,blog

# 3. Create sales enablement
/octave:enablement quick-ref --product "Platform"
```

### Quarterly Review → Refine → Retrain

```
# 1. Analyze the quarter
/octave:wins-losses
/octave:insights

# 2. Refine ICP
/octave:icp-refine --period 90

# 3. Update enablement materials
/octave:enablement onboarding
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
- Run `/octave:icp-refine` quarterly to keep targeting sharp

### Content Generation Quality

- Reference specific personas and playbooks for consistency
- Use saved agents for repeatable, high-quality output
- Review and customize generated content before sending
- Use `/octave:messaging` to build frameworks before `/octave:campaign`

### Competitive Intelligence

- Use `/octave:battlecard landscape` quarterly for a full competitive review
- Set up `/octave:insights` alerts for competitor mentions
- Update battlecards after every competitive deal (win or lose)

### Staying Informed

- Check `/octave:insights` regularly to see what's trending
- Use `/octave:wins-losses` monthly for pattern analysis
- Apply learnings back to your library to improve over time
- Run `/octave:icp-refine` each quarter to validate targeting
