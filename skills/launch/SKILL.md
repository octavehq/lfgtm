---
name: launch
description: Product and feature launch planning with full content kit generation across channels and audiences. Use when user says "launch plan", "product launch", "feature announcement", "GTM plan for launch", "launch content kit", or mentions launching something new.
argument-hint: "[description] [--type product|feature|update|partnership|expansion] [--persona <name>]"
---

# /octave:launch - Launch Command Center

Plan product and feature launches with full content kit generation — positioning, messaging by persona, channel strategy, and a complete set of launch assets — all grounded in your library intelligence.

## Usage

```
/octave:launch [description] [--type product|feature|update|partnership|expansion] [--persona <name>]
```

## Examples

```
/octave:launch                                            # Interactive mode
/octave:launch "New AI analytics feature"                 # Launch a feature
/octave:launch "Enterprise tier" --type product           # New product launch
/octave:launch "Salesforce integration" --type partnership
/octave:launch "APAC expansion" --type expansion
```

## Instructions

When the user runs `/octave:launch`:

### Step 1: Define the Launch

If no description provided, ask:

```
What are you launching?

PRODUCT
1. New product - Full product introduction
2. New feature - Addition to existing product
3. Product update - Major version or improvement

BUSINESS
4. Partnership / integration - New partner or integration
5. Market expansion - New segment, vertical, or geography
6. Pricing change - New plan, tier, or model

7. Something else - describe what you're launching

Your choice:
```

Then gather details:
```
Tell me about the launch:

1. What's being launched? (1-2 sentence description)
2. Which product does this relate to?
   [List products from library]
3. Who are the primary audiences?
   [List personas from library]
4. Target launch date? (for timeline planning)
5. Any competitive context? (e.g., responding to a competitor move)
6. Key metric for success? (e.g., signups, pipeline, awareness)
```

### Step 2: Gather Library Intelligence

```
# Get product details
get_entity({ oId: "<product_oId>" })

# Get all personas (to prioritize which audiences to target)
list_entities({ entityType: "persona" })
get_entity({ oId: "<primary_persona_oId>" })

# Get the relevant Motion(s) and Motion ICP cells for this offering
list_motions()
list_motion_icps({ motionOId: "<motion_oId>" })  # the persona × segment matrix
find_motion_icp({ motionIcpOId: "<motion_icp_oId>", includeLearnings: true })  # full cell narrative per target persona × segment

# Get proof points
search_knowledge_base({
  query: "<launch topic> results metrics",
  entityTypes: ["proof_point", "reference"]
})

# Get competitive context
search_knowledge_base({
  query: "<launch topic>",
  entityTypes: ["competitor"]
})

# Get use cases related to launch
search_knowledge_base({
  query: "<launch topic>",
  entityTypes: ["use_case"]
})

# Get brand voice
list_entities(entityType: "brand_voice")
```

### Step 3: Generate Launch Plan

See [launch-plan-template.md](references/launch-plan-template.md) for the full launch plan output template.

### Step 4: Generate Launch Content Kit

```
LAUNCH CONTENT KIT: [Launch Name]
===================================
```

**Announcement Email (Customers):**
```
generate_content({
  instructions: "Write a customer announcement email for [launch]. Tone: excited but not hypey. Structure: What's new, why it matters to them, what to do next. Keep it concise (150-200 words).",
  customContext: "<product details, launch positioning>"
})
```

**Prospect Email:**
```
generate_email({
  person: { firstName: "[Persona Name]", jobTitle: "[Title]" },
  numEmails: 1,
  sequenceType: "WARM_OUTBOUND",
  allEmailsContext: "New launch: [description]. Position as a reason to re-engage.",
  step1Instructions: "Use the launch as a hook to start a conversation. Don't just announce — connect to their likely pain points."
})
```

**Blog Post:**
```
generate_content({
  instructions: "Write a blog post announcing [launch]. Structure: Hook (why this matters to the reader), The problem, Our approach, What's new (features/capabilities), Early results or vision, CTA. Length: 800-1200 words. Tone: [brand voice].",
  customContext: "<product, use cases, proof points, competitive positioning>"
})
```

**Social Posts:**
```
generate_content({
  instructions: "Write 4 social media posts for [launch]. 1: Announcement post (LinkedIn). 2: Problem/solution angle. 3: Quick demo/feature highlight. 4: Customer/use case angle. Include hashtag suggestions.",
  customContext: "<launch positioning, key benefits>"
})
```

**Sales Enablement One-Pager:**
```
generate_content({
  instructions: "Create a sales enablement one-pager for [launch]. Internal audience (sales reps). Include: What's new (2-3 bullet), Who cares (persona + pain), Elevator pitch, Talk track, Proof points, Objections & responses, Competitive angle, CTA to offer prospects.",
  customContext: "<full library context>"
})
```

For the extended enablement package (objection guides, discovery question banks, cheat sheets), use /octave:enablement.

**Customer FAQ:**
```
generate_content({
  instructions: "Generate a customer FAQ for [launch]. 6-8 questions covering: What is it? How does it work? What changes for me? Pricing impact? Timeline? How to get started? Migration/upgrade path?",
  customContext: "<product details, launch specifics>"
})
```

**Competitive Talking Points** (if applicable):
```
generate_content({
  instructions: "Generate competitive talking points for [launch]. How does this change our position vs [competitors]? What can we now say that we couldn't before? New trap questions to ask?",
  customContext: "<competitor details, launch capabilities>"
})
```

### Step 5: Present Content Kit Summary

```
LAUNCH CONTENT KIT SUMMARY
============================

✓ Customer announcement email
✓ Prospect outreach email
✓ Blog post (1,000 words)
✓ Social posts (4 posts)
✓ Sales enablement one-pager
✓ Customer FAQ (8 questions)
✓ Competitive talking points

Sources Used:
- Product: [name]
- Personas: [list]
- Motion: [name] (with [N] Motion ICP cells)
- Proof Points: [list]
- Brand Voice: [name]

---

What would you like to do?

1. Revise any piece of content
2. Re-generate any piece using a saved agent
3. Generate landing page copy
4. Create versions for additional personas
5. Create a sales deck outline
6. Update library with new positioning
7. Export all content
8. Done
```

### Step 6: Library Updates (if requested)

Offer to update the library to reflect the launch:

```
# Create or update use case
create_entity({
  entityType: "use_case",
  name: "<new use case from launch>",
  instructions: "<details>"
})

# Update product with new capabilities
update_entity({
  entityType: "product",
  oId: "<product_oId>",
  instructions: "Add [new feature/capability] to product description and capabilities."
})

# Layer the launch into Motion Playbook narratives. Either:
#  - Update the Default Motion Playbook narrative for an existing Motion (Strategic narrative,
#    Benefits and impacts, Pains and consequences) to reflect the new launch positioning, or
#  - Create a Custom Motion Playbook (THEMATIC / MILESTONE / ACCOUNT / COMPETITIVE) for the launch.
update_motion_playbook({
  motionPlaybookOId: "<motion_playbook_oId>",
  instructions: "Fold [launch topic] into Strategic narrative and Benefits and impacts for the affected Motion ICP cells."
})

# Or, for launches that warrant a dedicated angle:
create_motion_playbook({
  motionOId: "<motion_oId>",
  narrativeType: "THEMATIC",  # or MILESTONE / ACCOUNT / COMPETITIVE
  name: "<launch-themed Motion Playbook name>",
  instructions: "<launch positioning, target audiences, supporting proof>"
})
```

## Generation Mode Note

See [generation-modes.md](../shared/generation-modes.md) for the default generation mode and the saved-agent / Claude-direct alternatives.

## MCP Tools Used

### Library Context
- `list_entities` - List products, personas, use cases
- `get_entity` - Full entity details
- `search_knowledge_base` - Proof points, references, competitive intel
- `list_entities` (entityType: "brand_voice") - Brand voice consistency

### Motions
- `list_motions` - Motions for the offering
- `list_motion_playbooks` - Default + Custom Motion Playbooks under a Motion
- `get_motion_playbook` - Full Motion Playbook details
- `list_motion_icps` - Persona × segment matrix
- `find_motion_icp` - Per-cell narrative + Learning Loop learnings

### Content Generation
- `generate_content` - Blog, social, one-pager, FAQ, talking points
- `generate_email` - Announcement and prospect emails

### Library Updates
- `create_entity` - New use cases from launch
- `update_entity` - Update product with new capabilities
- `create_motion_playbook` - Dedicated Custom Motion Playbook for the launch angle
- `update_motion_playbook` - Update Strategic narrative / Benefits and impacts to reflect launch positioning

## Error Handling

**No Product Selected:**
> Which product is this launch for?
> [List available products]
>
> Or describe the product and I'll work from that.

**No Personas:**
> No personas found. I'll generate launch content for a general audience.
> For persona-specific messaging, add personas: `/octave:library create persona`

**Large Launch Scope:**
> This is a big launch! I'll generate content in stages.
> Let's start with the most critical pieces: [prioritized list]
> Then we'll build out the rest.

## Related Skills

- `/octave:positioning` - Run a full positioning exercise before the launch to establish your messaging foundation
- `/octave:messaging` - Build messaging framework before the launch
- `/octave:campaign` - Generate ongoing campaign content post-launch
- `/octave:pmm` - Deep-dive on specific collateral (case study, deck, landing page)
- `/octave:battlecard` - Update competitive positioning for the launch
- `/octave:enablement` - Extended sales enablement materials
- `/octave:library` - Update library entities post-launch
