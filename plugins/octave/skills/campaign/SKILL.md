---
name: campaign
description: Plan and generate multi-channel campaign content including email sequences, LinkedIn, ads, social, blog, and landing pages. Use when user says "create a campaign", "multi-channel outreach", "demand gen", or asks for coordinated content across channels. Do NOT use for single emails or messages — use /octave:generate instead. Do NOT use for product/feature launch kits — use /octave:launch instead.
argument-hint: "[topic] [--channels email,linkedin,ads,social,blog,landing-page] [--persona <name>] [--motion <name>]"
---

# /octave:campaign - Campaign Architect

Plan and generate integrated campaign content across channels — emails, LinkedIn, ads, social, blog, and landing pages — all grounded in your library's personas, Motion ICP narratives, competitive positioning, and proof points.

## Usage

```
/octave:campaign [topic] [--channels <list>] [--persona <name>] [--motion <name>]
```

## Examples

```
/octave:campaign                                             # Interactive mode
/octave:campaign "AI feature launch"                         # Campaign around a topic
/octave:campaign "Q1 pipeline push" --persona "VP Engineering"
/octave:campaign "competitive displacement" --motion "Enterprise Outbound" --channels email,linkedin,ads
/octave:campaign "customer expansion" --channels email,social
```

## Channel Options

| Channel | What's Generated |
|---------|-----------------|
| `email` | Multi-step email sequence (default: 4 emails) |
| `linkedin` | Connection request + follow-up messages + post drafts |
| `ads` | 2-3 ad copy variants (headline, body, CTA). For platform-ready ad sets with targeting, negative keywords, and bulk-upload export, use /octave:ads |
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
1. New product/feature launch → use /octave:launch for the launch plan and content kit itself; pick this only for a post-launch campaign push
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
   [Suggest based on the matched Motion ICP narrative (Strategic narrative, Benefits and impacts) or "custom"]

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

# Find the right Motion and Motion ICP cell for this campaign
list_motions()
list_motion_icps({ motionOId: "<motion_oId>" })
find_motion_icp({ motionIcpOId: "<motion_icp_oId>", includeLearnings: true })

# Get proof points for credibility
search_knowledge_base({ query: "<campaign topic>", entityTypes: ["proof_point", "reference"] })

# Get competitive positioning if relevant
get_entity({ oId: "<competitor_oId>" })

# Get brand voice
list_entities(entityType: "brand_voice")

# Get writing style
list_writing_styles()

# Search for conversation insights on this topic
search_knowledge_base({ query: "<campaign topic> objections pain points" })
```

### Step 4: Generate Campaign Strategy

Present the campaign plan before generating content.

See [campaign-plan-output.md](references/campaign-plan-output.md) for the Campaign Plan output template.

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

See [email-sequence-output.md](references/email-sequence-output.md) for the Email Sequence output template.

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

See [linkedin-output.md](references/linkedin-output.md) for the LinkedIn Content output template.

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

See [ad-copy-output.md](references/ad-copy-output.md) for the Ad Copy Variants output template.

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

See [social-posts-output.md](references/social-posts-output.md) for the Social Posts output template.

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

See [blog-post-output.md](references/blog-post-output.md) for the Blog Post output template.

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

See [landing-page-output.md](references/landing-page-output.md) for the Landing Page Copy output template.

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

See [generation-modes.md](../shared/generation-modes.md) for the default generation mode and the saved-agent / Claude-direct alternatives.

## MCP Tools Used

### Library Context
- `list_entities` - List available personas, products
- `get_entity` - Get full entity details
- `list_motions` - List all Motions in the workspace
- `list_motion_icps` - List Motion ICP cells (persona × segment intersections) for a Motion
- `find_motion_icp` - Get full Motion ICP cell narrative (Target ICP overview, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References) plus Learning Loop learnings
- `list_motion_playbooks` - List Default + Custom Motion Playbooks under a Motion (when a Thematic / Milestone / Account / Competitive angle applies)
- `get_motion_playbook` - Full details for a Motion Playbook
- `search_knowledge_base` - Find proof points, references, messaging
- `list_entities` (entityType: "brand_voice") - Get brand voice for consistency
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

**No Matching Motion ICP:**
> No Motion ICP cell matches this campaign topic and persona.
>
> I'll use your product and persona information to ground the messaging.
> For better results, create a Motion for this offering, or layer a Custom Motion Playbook (Thematic / Milestone / Account / Competitive) onto an existing Motion that covers this segment.

**Single Channel Request:**
> If the user only wants one channel (e.g., "just emails"), generate that channel
> but suggest complementary channels at the end.

## Related Skills

- `/octave:brainstorm campaigns` - Ideate campaign concepts before building
- `/octave:generate` - Quick one-off content generation
- `/octave:ads` - Platform-ready ad campaigns (ad sets, targeting, negative keywords, export)
- `/octave:launch` - Launch planning and full launch content kit
- `/octave:pmm` - Deep-dive collateral (case studies, one-pagers)
- `/octave:repurpose` - Adapt campaign content for new audiences
- `/octave:messaging` - Build messaging framework before campaign
