---
name: launch
description: Product and feature launch planning with full content kit generation across channels and audiences
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
list_all_entities({ entityType: "persona" })
get_entity({ oId: "<primary_persona_oId>" })

# Get relevant playbooks
search_knowledge_base({
  query: "<launch topic> <product>",
  entityTypes: ["playbook"]
})
get_playbook({ oId: "<playbook_oId>", includeValueProps: true })

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
list_brand_voices()
```

### Step 3: Generate Launch Plan

```
LAUNCH PLAN: [Launch Name]
===========================

Type: [Product / Feature / Update / Partnership / Expansion]
Target Date: [Date]
Success Metric: [Metric]

---

POSITIONING
-----------
How this fits into the product story:
[1-2 sentences connecting to existing product narrative]

Launch Positioning Statement:
For [target audience] who [need], [launch item] is [category/description]
that [key benefit]. Unlike [alternative], it [key differentiator].

---

AUDIENCE PRIORITIZATION
-----------------------
| Priority | Persona | Why They Care | Key Message |
|----------|---------|---------------|-------------|
| 1 | [Persona 1] | [Relevance] | [Message] |
| 2 | [Persona 2] | [Relevance] | [Message] |
| 3 | [Persona 3] | [Relevance] | [Message] |

---

MESSAGING BY PERSONA
---------------------

[Persona 1]: [Title]
Pain addressed: [Specific pain this launch solves for them]
Value prop: "[Tailored value statement]"
Proof point: "[Most relevant evidence]"
CTA: "[What you want them to do]"

[Persona 2]: [Title]
Pain addressed: [Pain]
Value prop: "[Value]"
Proof point: "[Evidence]"
CTA: "[Action]"

---

COMPETITIVE POSITIONING
-----------------------
[If competitive context exists:]
How this changes the competitive landscape:
• [Impact on competitive position]
• [New differentiator or widened gap]
Key talking point: "[What to say about competition]"

---

CHANNEL PLAN
------------
| Channel | Timing | Audience | Content Type |
|---------|--------|----------|-------------|
| Email (customers) | Launch day | Current users | Announcement |
| Email (prospects) | Launch day+1 | Target personas | Value-focused |
| Blog | Launch day | Public | Feature story |
| Social | Launch day | Public | Announcement + thread |
| Sales enablement | Pre-launch | Sales team | One-pager + talk track |
| Website | Launch day | Public | Landing page update |

---

TIMELINE
--------

PRE-LAUNCH (2 weeks before)
• [Week -2] Internal briefing: align sales, CS, support
• [Week -2] Prepare all content assets
• [Week -1] Sales enablement training
• [Week -1] Seed content to key customers / beta users
• [Day -1] Final review and staging

LAUNCH DAY
• [Morning] Publish blog post and landing page
• [Morning] Send customer announcement email
• [Midday] Social media posts
• [Afternoon] Send prospect email campaign
• [EOD] Monitor early reactions

POST-LAUNCH (2 weeks after)
• [Week +1] Follow up with engaged prospects
• [Week +1] Gather initial feedback and quotes
• [Week +2] Publish customer story / use case
• [Week +2] Review metrics and iterate messaging

---

Ready to generate the content kit? [Y/n]
```

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
- Playbook: [name]
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

# Add new value props to playbooks
add_value_props({
  playbookOId: "<playbook_oId>",
  instructions: "Add value props related to [launch topic]"
})
```

## Generation Mode Note

This skill uses Octave's `generate_content` and `generate_email` tools by default. Two alternatives:
- **Saved agents**: Check for matching agents with `list_agents` when relevant. See `/octave:explore-agents`.
- **Claude-direct**: Skip `generate_*` calls, gather Octave context, Claude writes directly. Offer when user wants more control.

For the full interactive mode selector, use `/octave:generate`.

## MCP Tools Used

### Library Context
- `list_all_entities` - List products, personas, use cases
- `get_entity` - Full entity details
- `get_playbook` - Playbook with value props
- `search_knowledge_base` - Proof points, references, competitive intel
- `list_brand_voices` - Brand voice consistency

### Content Generation
- `generate_content` - Blog, social, one-pager, FAQ, talking points
- `generate_email` - Announcement and prospect emails

### Library Updates
- `create_entity` - New use cases from launch
- `update_entity` - Update product with new capabilities
- `add_value_props` - New value props for playbooks

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

- `/octave:messaging` - Build messaging framework before the launch
- `/octave:campaign` - Generate ongoing campaign content post-launch
- `/octave:pmm` - Deep-dive on specific collateral (case study, deck, landing page)
- `/octave:battlecard` - Update competitive positioning for the launch
- `/octave:enablement` - Extended sales enablement materials
- `/octave:library` - Update library entities post-launch
