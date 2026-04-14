---
name: campaign
description: "Plan and generate multi-channel campaign content including email sequences, LinkedIn, ads, social, blog, and landing pages. Use when user says 'create a campaign', 'campaign for launch', 'multi-channel outreach', 'demand gen', or asks for coordinated content across channels. Do NOT use for single emails or messages — use /octave:generate instead."
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

If no topic provided, ask the user to choose a campaign type:

- **Growth**: New product/feature launch, pipeline acceleration, customer expansion/upsell, event promotion
- **Competitive**: Competitive displacement, market positioning/thought leadership
- **Lifecycle**: Re-engagement (cold leads, churned accounts), nurture sequence
- **Custom**: User describes their own campaign goal

### Step 2: Gather Campaign Parameters

Ask targeted questions based on campaign type:

1. **Target audience** — list personas from library or allow custom
2. **Product/solution** — list products from library
3. **Key message or angle** — suggest from playbook value props or allow custom
4. **Channels** — select from channel options above (default: email + linkedin)
5. **Timeframe** — Sprint (1-2 weeks), Standard (3-4 weeks), or Extended (6-8 weeks)
6. **Competitive context** — list competitors from library or "none"

### Step 3: Gather Library Intelligence

Pull context from the Octave library to ground the campaign in real intelligence:

```
# Core entities
get_entity({ oId: "<persona_oId>" })
get_entity({ oId: "<product_oId>" })

# Playbook and value props
search_knowledge_base({ query: "<campaign topic> <persona>", entityTypes: ["playbook"] })
get_playbook({ oId: "<playbook_oId>", includeValueProps: true })

# Proof points and competitive intel
search_knowledge_base({ query: "<campaign topic>", entityTypes: ["proof_point", "reference"] })
get_entity({ oId: "<competitor_oId>" })  // if competitive context exists

# Brand consistency
list_brand_voices()
list_writing_styles()

# Topic insights
search_knowledge_base({ query: "<campaign topic> objections pain points" })
```

### Step 4: Generate Campaign Strategy

Present the campaign plan before generating content, covering:

- **Objective** — one-sentence campaign goal
- **Target Audience** — persona, segment, key pain points from library
- **Strategic Angle** — playbook, lead value prop, supporting props
- **Proof Points** — metrics, customer stories, references
- **Competitive Positioning** — key differentiators (if applicable)
- **Channel Plan** — table of channels with timing and purpose

Confirm with the user before proceeding to content generation.

### Step 5: Generate Channel Content

For each selected channel, use the appropriate MCP tool (`generate_email` for emails, `generate_content` for all others) with campaign context, persona pain points, value props, and proof points as input.

See `references/CHANNEL-TEMPLATES.md` for detailed MCP tool calls and output formats for each channel.

Key generation principles:
- Each channel's content should reinforce the campaign's strategic angle
- Use proof points progressively across the sequence (don't front-load everything)
- Maintain brand voice consistency across all channels
- Email sequences should build momentum — each email advances the narrative
- Ad copy must respect character limits: Headline (30 chars), Body (90 chars), CTA (15 chars)

### Step 6: Validate Generated Content

After generating content for each channel, verify quality before presenting:

1. **Brand voice check** — does the tone match `list_brand_voices()` output? Flag deviations.
2. **Proof point accuracy** — are all cited metrics, quotes, and customer references drawn from the library? No fabricated stats.
3. **Character limit compliance** — verify ad headlines (30 chars), ad body (90 chars), CTAs (15 chars), LinkedIn connection requests (300 chars).
4. **Cross-channel consistency** — do all channels use the same core messaging, value props, and terminology?
5. **Persona alignment** — does language match the persona's seniority level and domain vocabulary?

If any check fails, revise the affected content before presenting to the user.

### Step 7: Present Campaign Summary

After generating and validating all channels, present a unified view:

- Checklist of channels generated with counts (e.g., "Email sequence — 4 emails")
- Library sources used: persona, playbook, value props, proof points, competitor, brand voice
- Next steps menu:
  1. Revise a specific channel's content
  2. Re-generate using a saved agent
  3. Add more channels
  4. Adapt for a different persona or segment
  5. Export all content
  6. Done

## Generation Mode Note

This skill uses Octave's `generate_content` and `generate_email` tools by default. Two alternatives:
- **Saved agents**: Check for matching agents with `list_agents` when relevant. See `/octave:explore-agents`.
- **Claude-direct**: Skip `generate_*` calls, gather Octave context, Claude writes directly. Offer when user wants more control.

For the full interactive mode selector, use `/octave:generate`.

## Error Handling

- **No personas found** — campaigns work best grounded in persona intelligence. Suggest `/octave:library create persona` or offer to generate generic content.
- **No playbooks found** — fall back to product and persona information for messaging. Suggest `/octave:library create playbook` for better results.
- **Single channel request** — generate the requested channel but suggest complementary channels at the end.

## MCP Tools

See `references/MCP-TOOLS.md` for the complete tool reference. Key tools:

- **Library context**: `get_entity`, `get_playbook`, `search_knowledge_base`, `list_brand_voices`, `list_writing_styles`
- **Generation**: `generate_email` (email sequences), `generate_content` (all other channels)

## Related Skills

- `/octave:brainstorm campaigns` — ideate campaign concepts before building
- `/octave:generate` — quick one-off content generation
- `/octave:pmm` — deep-dive collateral (case studies, one-pagers)
- `/octave:repurpose` — adapt campaign content for new audiences
- `/octave:messaging` — build messaging framework before campaign
