---
name: campaign
description: Plan and generate multi-channel campaign content including email sequences, LinkedIn, ads, social, blog, and landing pages. Use when user says "create a campaign", "campaign for launch", "multi-channel outreach", "demand gen", or asks for coordinated content across channels. Do NOT use for single emails or messages — use /octave:generate instead.
---

# /octave:campaign - Campaign Architect

Plan and generate integrated campaign content across channels — emails, LinkedIn, ads, social, blog, and landing pages — all grounded in your library's personas, playbooks, competitive positioning, and proof points.

## Usage

```
/octave:campaign [topic] [--channels <list>] [--persona <name>] [--playbook <name>]
```

## Examples

```
/octave:campaign                                             # Interactive mode
/octave:campaign "AI feature launch"                         # Campaign around a topic
/octave:campaign "Q1 pipeline push" --persona "VP Engineering"
/octave:campaign "competitive displacement" --playbook "Enterprise" --channels email,linkedin,ads
/octave:campaign "customer expansion" --channels email,social
```

## Channel Options

| Channel | What's Generated |
|---------|-----------------|
| `email` | Multi-step email sequence (default: 4 emails) |
| `linkedin` | Connection request + follow-up messages + post drafts |
| `ads` | 2-3 ad copy variants (headline, body, CTA) |
| `social` | 3-5 social posts (LinkedIn, Twitter/X) |
| `blog` | Full blog post outline with key sections |
| `landing-page` | Landing page copy (hero, benefits, CTA, proof points) |

Default: `email,linkedin` if no channels specified.

## Instructions

When the user runs `/octave:campaign`:

### Step 1: Define Campaign Scope

If no topic provided, ask:

```
What's the campaign about?

GROWTH
1. New product/feature launch
2. Pipeline acceleration (drive meetings)
3. Customer expansion / upsell
4. Event promotion (webinar, conference)

COMPETITIVE
5. Competitive displacement
6. Market positioning / thought leadership

LIFECYCLE
7. Re-engagement (cold leads, churned accounts)
8. Nurture sequence (educate and warm)

9. Something else - describe your campaign goal

Your choice:
```

### Step 2: Gather Campaign Parameters

Ask targeted questions based on campaign type:

```
Let's shape this campaign. A few questions:

1. Target audience?
   [List personas from library or "new/custom"]

2. Which product/solution?
   [List products from library]

3. Key message or angle?
   [Suggest based on playbook value props or "custom"]

4. Which channels?
   [email, linkedin, ads, social, blog, landing-page]
   Default: email + linkedin

5. Timeframe?
   - Sprint (1-2 weeks)
   - Standard (3-4 weeks)
   - Extended (6-8 weeks)

6. Any competitive context?
   [List competitors or "none"]
```

### Step 3: Gather Library Intelligence

This is what makes the campaign intelligence-grounded, not just templated:

```
# Get persona details
get_entity({ oId: "<persona_oId>" })

# Get product details
get_entity({ oId: "<product_oId>" })

# Get matching playbook and value props
search_knowledge_base({ query: "<campaign topic> <persona>", entityTypes: ["playbook"] })
get_playbook({ oId: "<playbook_oId>", includeValueProps: true })

# Get proof points for credibility
search_knowledge_base({ query: "<campaign topic>", entityTypes: ["proof_point", "reference"] })

# Get competitive positioning if relevant
get_entity({ oId: "<competitor_oId>" })

# Get brand voice
list_brand_voices()

# Get writing style
list_writing_styles()

# Search for conversation insights on this topic
search_knowledge_base({ query: "<campaign topic> objections pain points" })
```

### Step 4: Generate Campaign Strategy

Present the campaign plan before generating content:

```
CAMPAIGN PLAN: [Campaign Name]
==============================

OBJECTIVE
---------
[One-sentence goal]

TARGET AUDIENCE
---------------
Persona: [Persona name]
Segment: [Segment if applicable]
Key Pain Points:
• [Pain point 1 from persona]
• [Pain point 2 from persona]

STRATEGIC ANGLE
---------------
Playbook: [Playbook name]
Lead Value Prop: [Primary value prop]
Supporting Props:
• [Value prop 2]
• [Value prop 3]

PROOF POINTS
------------
• [Proof point 1 — metric or customer story]
• [Proof point 2]
• [Reference customer if relevant]

COMPETITIVE POSITIONING
-----------------------
[If competitive context exists]
Key Differentiators:
• [Differentiator 1]
• [Differentiator 2]

CHANNEL PLAN
------------
| Channel | Timing | Purpose |
|---------|--------|---------|
| [Channel 1] | [When] | [Role in campaign] |
| [Channel 2] | [When] | [Role in campaign] |
| ... | ... | ... |

---

Ready to generate content for each channel? [Y/n]
```

### Step 5: Generate Channel Content

Generate content for each selected channel:

---

**Email Sequence:**
```
generate_email({
  person: { firstName: "[Persona Name]", jobTitle: "[Persona Title]" },
  numEmails: 4,
  sequenceType: "COLD_OUTBOUND",  // or WARM_OUTBOUND based on campaign type
  allEmailsContext: "<campaign angle, persona pain points, competitive positioning, proof points>",
  allEmailsInstructions: "Campaign: [name]. Angle: [strategic angle]. Each email should build on the previous. Use proof points progressively."
})
```

Present as:
```
EMAIL SEQUENCE (4 emails)
=========================

EMAIL 1: [Subject Line]
Timing: Day 1
Purpose: [Hook with primary pain point]
---
[Email body]

---

EMAIL 2: [Subject Line]
Timing: Day 3
Purpose: [Social proof / value prop]
---
[Email body]

---

EMAIL 3: [Subject Line]
Timing: Day 6
Purpose: [Differentiator / insight]
---
[Email body]

---

EMAIL 4: [Subject Line]
Timing: Day 10
Purpose: [Direct ask / breakup]
---
[Email body]
```

---

**LinkedIn Messages:**
```
generate_content({
  instructions: "Generate LinkedIn outreach for a campaign targeting [persona]. Create:
    1. Connection request note (300 char max)
    2. Follow-up message after connection (short, value-add)
    3. LinkedIn post draft that the sales rep can publish (thought leadership angle)
    All grounded in: [value props, pain points, proof points]",
  customContext: "<library intelligence gathered>"
})
```

Present as:
```
LINKEDIN CONTENT
================

CONNECTION REQUEST (300 chars)
------------------------------
[Message]

FOLLOW-UP MESSAGE
-----------------
[Message after they accept]

LINKEDIN POST (for rep to publish)
-----------------------------------
[Post draft — thought leadership angle related to campaign theme]

ENGAGEMENT COMMENTS (templates)
-------------------------------
If they post about [topic]: "[Comment]"
If they share [content type]: "[Comment]"
```

---

**Ad Copy:**
```
generate_content({
  instructions: "Generate 3 ad copy variants for a campaign targeting [persona].
    Each variant needs: Headline (30 chars), Body (90 chars), CTA (15 chars).
    Variant 1: Pain-point led. Variant 2: Social-proof led. Variant 3: Curiosity/insight-led.
    All grounded in: [value props, differentiators, proof points]",
  customContext: "<library intelligence>"
})
```

Present as:
```
AD COPY VARIANTS
================

VARIANT 1: Pain-Led
Headline: [30 chars]
Body: [90 chars]
CTA: [15 chars]

VARIANT 2: Proof-Led
Headline: [30 chars]
Body: [90 chars]
CTA: [15 chars]

VARIANT 3: Insight-Led
Headline: [30 chars]
Body: [90 chars]
CTA: [15 chars]
```

---

**Social Posts:**
```
generate_content({
  instructions: "Generate 5 social media posts for a campaign targeting [persona].
    Mix of: 1 stat/insight post, 1 question post, 1 mini case study, 1 hot take, 1 educational tip.
    All connect back to: [campaign theme and value props].
    Include hashtag suggestions.",
  customContext: "<library intelligence>"
})
```

Present as:
```
SOCIAL POSTS
============

POST 1: Stat/Insight
[Post body]
#hashtag1 #hashtag2

POST 2: Question
[Post body]

POST 3: Mini Case Study
[Post body]

POST 4: Hot Take
[Post body]

POST 5: Educational Tip
[Post body]
```

---

**Blog Post:**
```
generate_content({
  instructions: "Generate a full blog post for a campaign targeting [persona].
    Topic: [campaign theme]. Angle: [strategic angle].
    Structure: Title, meta description, intro (hook), 3-4 main sections with subheadings,
    conclusion with CTA. Weave in proof points naturally.
    Length: 1200-1800 words. Tone: [brand voice].",
  customContext: "<library intelligence, proof points, competitive positioning>"
})
```

Present as:
```
BLOG POST
=========

Title: [Title]
Meta Description: [155 chars]
Target Persona: [Persona]

---

[Full blog post content with sections]

---

Internal CTA: [What to link to / landing page]
```

---

**Landing Page:**
```
generate_content({
  instructions: "Generate landing page copy for a campaign targeting [persona].
    Sections: Hero (headline, subheadline, CTA), Problem statement, Solution overview,
    3 key benefits with descriptions, Social proof section (quotes, logos, metrics),
    FAQ (3-4 questions), Final CTA.
    Tone: [brand voice]. Focus: [campaign angle].",
  customContext: "<library intelligence, proof points, differentiators>"
})
```

Present as:
```
LANDING PAGE COPY
=================

HERO
----
Headline: [Headline]
Subheadline: [Subheadline]
CTA Button: [CTA text]

PROBLEM
-------
[Problem statement copy]

SOLUTION
--------
[Solution overview]

KEY BENEFITS
------------
✓ [Benefit 1]: [Description]
✓ [Benefit 2]: [Description]
✓ [Benefit 3]: [Description]

SOCIAL PROOF
------------
"[Customer quote]" — [Name, Title, Company]
Metrics: [Key stats]
Logos: [Suggest which reference customers]

FAQ
---
Q: [Question 1]
A: [Answer]

Q: [Question 2]
A: [Answer]

FINAL CTA
---------
Headline: [Closing headline]
CTA Button: [CTA text]
Supporting: [Urgency/value text]
```

### Step 6: Present Campaign Summary

After generating all channels, present a unified view:

```
CAMPAIGN SUMMARY: [Campaign Name]
==================================

Channels Generated:
✓ Email sequence (4 emails)
✓ LinkedIn (connection + follow-up + post)
✓ Ad copy (3 variants)
✓ Social posts (5 posts)
✓ Blog post (1,500 words)
✓ Landing page copy

Library Sources Used:
- Persona: [name]
- Playbook: [name]
- Value Props: [list]
- Proof Points: [list]
- Competitor: [name] (if applicable)
- Brand Voice: [name]

---

What would you like to do?

1. Revise a specific channel's content
2. Re-generate any piece using a saved agent
3. Generate content for additional channels
4. Adapt for a different persona
5. Create a version for a different segment
6. Export all content
7. Done
```

## Generation Mode Note

This skill uses Octave's `generate_content` and `generate_email` tools by default. Two alternatives:
- **Saved agents**: Check for matching agents with `list_agents` when relevant. See `/octave:explore-agents`.
- **Claude-direct**: Skip `generate_*` calls, gather Octave context, Claude writes directly. Offer when user wants more control.

For the full interactive mode selector, use `/octave:generate`.

## MCP Tools Used

### Library Context
- `list_all_entities` - List available personas, products, playbooks
- `get_entity` - Get full entity details
- `get_playbook` - Get playbook with value props
- `list_value_props` - Get value propositions
- `search_knowledge_base` - Find proof points, references, messaging
- `list_brand_voices` - Get brand voice for consistency
- `list_writing_styles` - Get writing style guidelines

### Content Generation
- `generate_email` - Email sequence generation
- `generate_content` - All other content types (ads, social, blog, landing page, LinkedIn)

## Error Handling

**No Personas Found:**
> No personas in your library yet.
>
> Campaigns work best when grounded in persona intelligence.
> Run `/octave:library create persona` to add one, or I can generate generic campaign content.

**No Playbooks Found:**
> No playbooks found matching this campaign topic.
>
> I'll use your product and persona information to ground the messaging.
> For better results, create a playbook: `/octave:library create playbook`

**Single Channel Request:**
> If the user only wants one channel (e.g., "just emails"), generate that channel
> but suggest complementary channels at the end.

## Related Skills

- `/octave:brainstorm campaigns` - Ideate campaign concepts before building
- `/octave:generate` - Quick one-off content generation
- `/octave:pmm` - Deep-dive collateral (case studies, one-pagers)
- `/octave:repurpose` - Adapt campaign content for new audiences
- `/octave:messaging` - Build messaging framework before campaign
