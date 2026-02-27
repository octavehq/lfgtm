---
name: pmm
description: Product marketing content generator for case studies, blog posts, datasheets, and FAQs. Use when user says "case study", "blog post", "datasheet", "FAQ", or asks for marketing collateral. For visual document output, prefer /octave:deck, /octave:one-pager, /octave:brief, /octave:proposal, or /octave:microsite.
---

# /octave:pmm - Product Marketing Assistant

Interactive PMM assistant for creating sales collateral, landing pages, case studies, one-pagers, decks, and other marketing content—all infused with your brand voice and library messaging.

## Usage

```
/octave:pmm [content-type]
```

## Content Types

```
/octave:pmm                      # Interactive mode - asks what you're creating
/octave:pmm one-pager            # Product one-pager
/octave:pmm case-study           # Customer case study
/octave:pmm landing-page         # Landing page copy
/octave:pmm deck                 # Sales deck outline
/octave:pmm blog                 # Blog post / thought leadership
/octave:pmm datasheet            # Technical datasheet
/octave:pmm faq                  # FAQ document
```

## Instructions

When the user runs `/octave:pmm`:

### Step 1: Determine Content Type

If no type specified, ask:

```
What would you like to create?

SALES ENABLEMENT
1. One-Pager - Single page product/solution overview
2. Sales Deck - Presentation outline and talking points

MARKETING CONTENT
3. Landing Page - Web page copy (hero, benefits, CTA)
4. Case Study - Customer success story
5. Blog Post - Thought leadership content
6. Datasheet - Technical specifications

OTHER
7. FAQ - Frequently asked questions
8. Something else - Describe what you need

TIP: For competitive battlecards, use /octave:battlecard
TIP: For objection handling guides, use /octave:enablement objections

Your choice:
```

### Step 2: Gather Requirements

Based on content type, ask targeted questions:

---

**For One-Pager:**
```
Let's create your one-pager. A few questions:

1. Which product/solution is this for?
   [List products from library or "new/custom"]

2. Target audience?
   [List personas from library or "general"]

3. Primary use case to emphasize?
   [List use cases or "general overview"]

4. Key CTA (call-to-action)?
   - Schedule a demo
   - Start free trial
   - Contact sales
   - Custom: ___

5. Any specific proof points to include?
   [List available proof points]
```

---

**For Case Study:**
```
Let's create your case study. A few questions:

1. Which customer/reference?
   [List references from library or "new customer"]

2. Primary persona who would read this?
   [List personas]

3. Key metrics to highlight?
   - ROI / cost savings
   - Time savings
   - Performance improvements
   - Custom metrics: ___

4. Desired length?
   - Short (1 page, quick read)
   - Standard (2-3 pages, detailed)
   - Long-form (full story with quotes)
```

---

**For Landing Page:**
```
Let's create your landing page copy. A few questions:

1. What's the page for?
   - Product overview
   - Use case / solution
   - Campaign / promotion
   - Event / webinar
   - Free trial signup

2. Target persona?
   [List personas]

3. Primary CTA?
   - Demo request
   - Free trial
   - Contact us
   - Download resource
   - Register for event

4. Tone?
   - Professional / enterprise
   - Friendly / conversational
   - Bold / challenger
   - Use default brand voice
```

---

**For Blog Post:**
```
Let's create your blog post. A few questions:

1. Topic or theme?
   [Open text or suggest based on library]

2. Content angle?
   - Thought leadership (industry trends)
   - How-to / educational
   - Customer story
   - Product announcement
   - Comparison / versus

3. Target persona?
   [List personas]

4. Desired length?
   - Short (500-800 words)
   - Medium (1000-1500 words)
   - Long-form (2000+ words)

5. SEO keywords to target? (optional)
```

### Step 3: Gather Library Context

Use MCP tools to gather library context:

```
# Always get brand voice
list_brand_voices()

# Get product info
get_entity({ oId: "<product_oId>" })

# Get persona details
get_entity({ oId: "<persona_oId>" })

# Get reference details (for case studies)
get_entity({ oId: "<reference_oId>" })

# Search for relevant proof points
search_knowledge_base({ query: "<topic>", entityTypes: ["proof_point"] })

# Get relevant use cases
search_knowledge_base({ query: "<topic>", entityTypes: ["use_case"] })

# Search for messaging
search_knowledge_base({ query: "<persona> pain points value" })
```

### Step 4: Generate Content

Use `generate_content` with structured instructions:

```
generate_content({
  instructions: "<detailed content brief>",
  person: { ... },  // if persona-targeted
  company: { ... }, // if account-specific
  customContext: "<library context gathered>"
})
```

Present the generated content with clear sections:

---

#### One-Pager Output

```
ONE-PAGER: [Product Name] for [Persona]
=======================================

[Brand Voice: Using "[Brand Voice Name]"]
[Target Persona: [Persona Name]]
[Primary Use Case: [Use Case]]

---

HEADLINE
--------
[Compelling headline addressing key pain point]

SUBHEADLINE
-----------
[Supporting statement with value proposition]

---

THE CHALLENGE
-------------
[2-3 sentences describing the problem, using persona pain points]

THE SOLUTION
------------
[2-3 sentences describing how your product solves it]

---

KEY BENEFITS
------------
✓ [Benefit 1] - [Brief explanation]
✓ [Benefit 2] - [Brief explanation]
✓ [Benefit 3] - [Brief explanation]

---

PROOF POINTS
------------
• [Stat/metric from library]
• [Customer quote or outcome]
• [Third-party validation]

---

[CTA BUTTON TEXT]
[Supporting CTA text]

---

FOOTER
------
[Contact info / URL]

---

Sources Used:
- Persona: [persona name] (pain points, objectives)
- Product: [product name] (features, differentiators)
- Proof Points: [list used]
- Brand Voice: [voice name]

---

Want me to:
1. Adjust the tone or messaging
2. Add/remove sections
3. Create a different version for another persona
4. Export as markdown/text
```

---

#### Case Study Output

```
CASE STUDY: [Customer Name]
===========================

[Industry: [Industry]]
[Company Size: [Size]]
[Use Case: [Primary use case]]

---

HEADLINE
--------
[Outcome-focused headline, e.g., "How [Customer] Reduced [Metric] by X%"]

EXECUTIVE SUMMARY
-----------------
[2-3 sentence overview of challenge, solution, results]

---

ABOUT [CUSTOMER]
----------------
[Brief company description]
[Relevant context about their situation]

---

THE CHALLENGE
-------------
[Customer name] faced several challenges:

• [Challenge 1 - tied to persona pain point]
• [Challenge 2]
• [Challenge 3]

"[Quote from customer about the problem]"
— [Name], [Title]

---

THE SOLUTION
------------
[Customer] chose [Your Product] because:

• [Reason 1 - tied to differentiator]
• [Reason 2]
• [Reason 3]

Implementation highlights:
• [Key implementation detail]
• [Timeline]
• [Any notable approach]

---

THE RESULTS
-----------
After implementing [Your Product], [Customer] achieved:

┌─────────────────────────────────────┐
│  [XX]%     [XX]%      [XX]x        │
│  [Metric]  [Metric]   [Metric]     │
└─────────────────────────────────────┘

Detailed outcomes:
• [Result 1 with specifics]
• [Result 2 with specifics]
• [Result 3 with specifics]

"[Quote about results/satisfaction]"
— [Name], [Title]

---

LOOKING AHEAD
-------------
[Future plans, expansion, next phase]

---

KEY TAKEAWAYS
-------------
1. [Takeaway relevant to target persona]
2. [Takeaway about implementation]
3. [Takeaway about ROI/value]

---

[CTA: Ready to achieve similar results? Contact us.]

---

Sources Used:
- Reference: [reference name] (metrics, quotes, context)
- Use Case: [use case name]
- Product: [product name]

---

Want me to:
1. Adjust the tone (more technical, more executive)
2. Add more detail to a section
3. Create a short version (1-page)
4. Create pull quotes for social
```

### Step 5: Iterate and Refine

After presenting content, offer refinement options:

```
What would you like to do?

1. Adjust tone or style
2. Add/remove/expand sections
3. Re-generate using a saved agent
4. Create version for different persona
5. Make it shorter / longer
6. Add more proof points
7. Strengthen the CTA
8. Done - export final version

Your choice:
```

For each revision request, regenerate the specific section or full content as needed.

### Step 6: Export Options

```
Export Options
==============

1. Copy as Markdown (for docs, Notion, etc.)
2. Copy as plain text
3. Copy as HTML
4. Save to file

Which format?
```

## Brand Voice Integration

Always check for brand voices and apply:

```
list_brand_voices()
```

If multiple voices exist, ask:
```
Which brand voice should I use?

1. [Voice 1 name] - [description]
2. [Voice 2 name] - [description]
3. No specific voice (neutral professional)
```

Apply selected voice guidelines to all generated content.

## Generation Mode Note

This skill uses Octave's `generate_content` and `generate_email` tools by default. Two alternatives:
- **Saved agents**: Check for matching agents with `list_agents` when relevant. See `/octave:explore-agents`.
- **Claude-direct**: Skip `generate_*` calls, gather Octave context, Claude writes directly. Offer when user wants more control.

For the full interactive mode selector, use `/octave:generate`.

## MCP Tools Used

### Library Context
- `list_brand_voices` - Get available brand voices
- `list_all_entities` - List products, personas, etc.
- `get_entity` - Get full entity details
- `search_knowledge_base` - Find relevant messaging, proof points

### Content Generation
- `generate_content` - Primary content generation tool
- `generate_email` - For email-style content within collateral

## Content Type Quick Reference

| Type | Key Inputs | Primary Library Sources |
|------|------------|------------------------|
| One-Pager | Product, persona, use case | Product, persona pain points, proof points |
| Case Study | Reference customer | Reference (metrics, quotes), use case |
| Landing Page | Product/campaign, persona, CTA | Product, persona, value props |
| Blog Post | Topic, angle, persona | Use cases, proof points, messaging |
| Datasheet | Product | Product (features, specs, capabilities) |
| FAQ | Product/topic | Common objections, use cases |
| Sales Deck | Product, persona, playbook | Playbook (narrative, value props), product |

## Error Handling

**Missing Product:**
> No products found in your library.
>
> To create effective collateral, I need product information.
> Run /octave:library create product to add your product first.

**Missing Brand Voice:**
> No brand voice defined. I'll use a neutral professional tone.
>
> For consistent messaging, consider creating a brand voice:
> This is done in the Octave web app under Settings > Brand Voices.

## Related Skills

- `/octave:brainstorm` - Generate content ideas before creating
- `/octave:generate` - Quick one-off content (emails, LinkedIn)
- `/octave:library` - Add/update entities used in content
- `/octave:analyzer` - Analyze existing content for improvements
- `/octave:battlecard` - Competitive battlecards with real deal evidence
- `/octave:enablement` - Sales enablement materials (objection guides, cheat sheets)
- `/octave:positioning` - Complete visual positioning system — message framework, anchors, strategy, persona messaging
- `/octave:messaging` - Build messaging frameworks before creating collateral
- `/octave:campaign` - Multi-channel campaign content
