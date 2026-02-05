---
name: pmm
description: Product marketing assistant for creating sales collateral, landing pages, battlecards, and case studies
---

# /octave:pmm - Product Marketing Assistant

Interactive PMM assistant for creating sales collateral, landing pages, battlecards, case studies, one-pagers, and other marketing content—all infused with your brand voice and library messaging.

## Usage

```
/octave:pmm [content-type]
```

## Content Types

```
/octave:pmm                      # Interactive mode - asks what you're creating
/octave:pmm one-pager            # Product one-pager
/octave:pmm battlecard           # Competitive battlecard
/octave:pmm case-study           # Customer case study
/octave:pmm landing-page         # Landing page copy
/octave:pmm deck                 # Sales deck outline
/octave:pmm blog                 # Blog post / thought leadership
/octave:pmm datasheet            # Technical datasheet
/octave:pmm faq                  # FAQ document
/octave:pmm objection-handler    # Objection handling guide
```

## Instructions

When the user runs `/octave:pmm`:

### Step 1: Determine Content Type

If no type specified, ask:

```
What would you like to create?

SALES ENABLEMENT
1. One-Pager - Single page product/solution overview
2. Battlecard - Competitive positioning guide
3. Objection Handler - Response guide for common objections
4. Sales Deck - Presentation outline and talking points

MARKETING CONTENT
5. Landing Page - Web page copy (hero, benefits, CTA)
6. Case Study - Customer success story
7. Blog Post - Thought leadership content
8. Datasheet - Technical specifications

OTHER
9. FAQ - Frequently asked questions
10. Something else - Describe what you need

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

**For Battlecard:**
```
Let's create your battlecard. A few questions:

1. Which competitor?
   [List competitors from library]

2. Target audience for this battlecard?
   - Sales reps (detailed technical)
   - Sales leaders (strategic overview)
   - Both

3. Key scenarios to address?
   - Head-to-head replacement
   - Competitive displacement
   - New evaluation
   - All of the above

4. Include pricing comparison?
   - Yes, with ranges
   - No, keep it positioning-focused
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

# Get competitor info (for battlecards)
get_entity({ oId: "<competitor_oId>" })

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

#### Battlecard Output

```
BATTLECARD: [Your Product] vs [Competitor]
==========================================

[Last Updated: [date]]
[Audience: Sales Reps]

---

QUICK POSITIONING
-----------------
When you hear: "[Competitor]"
Lead with: "[Key differentiator statement]"

One-liner: "[Elevator pitch positioning against competitor]"

---

COMPETITOR OVERVIEW
-------------------
What they do: [Brief description]
Target market: [Their focus]
Pricing model: [If known]
Key customers: [Notable logos]

---

WHERE WE WIN
------------
| Capability | Us | Them |
|------------|-----|------|
| [Feature 1] | ✓ [Our strength] | ✗ [Their weakness] |
| [Feature 2] | ✓ [Our strength] | ~ [Partial] |
| [Feature 3] | ✓ [Our strength] | ✗ [Their weakness] |

Win themes:
1. [Win reason 1 from library]
2. [Win reason 2 from library]
3. [Win reason 3 from library]

---

WHERE THEY WIN (BE HONEST)
--------------------------
| Capability | Them | Us |
|------------|------|-----|
| [Feature] | ✓ [Their strength] | [Our response/roadmap] |

How to handle:
- "[Objection]" → "[Response that reframes]"

---

COMMON OBJECTIONS
-----------------

"[Competitor] is cheaper"
→ [Response about value, TCO, hidden costs]

"[Competitor] has feature X"
→ [Response about why it matters/doesn't, alternatives]

"We already use [Competitor]"
→ [Displacement strategy, migration story]

---

TRAP QUESTIONS TO ASK
---------------------
Ask the prospect these questions to expose competitor weaknesses:

1. "[Question that reveals competitor limitation]"
   Why: [What you're hoping to uncover]

2. "[Question about scalability/support/etc.]"
   Why: [What you're hoping to uncover]

---

PROOF POINTS TO USE
-------------------
• [Customer who switched from competitor]
• [Metric comparing outcomes]
• [Third-party validation]

---

LANDMINES TO SET
----------------
Plant these ideas early in the evaluation:

1. "[Criteria] is critical because..." (plays to our strength)
2. "Make sure to ask about [topic]..." (exposes their weakness)

---

Sources Used:
- Competitor: [competitor name] (strengths, weaknesses, differentiation)
- Win/Loss reasons from library
- Proof points: [list]

---

Want me to:
1. Add more objection handling
2. Create a version for a specific persona
3. Deep dive on a particular comparison area
4. Create trap questions for specific features
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
3. Create version for different persona
4. Make it shorter / longer
5. Add more proof points
6. Strengthen the CTA
7. Done - export final version

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
| Battlecard | Competitor, audience | Competitor (strengths, weaknesses, differentiation) |
| Case Study | Reference customer | Reference (metrics, quotes), use case |
| Landing Page | Product/campaign, persona, CTA | Product, persona, value props |
| Blog Post | Topic, angle, persona | Use cases, proof points, messaging |
| Datasheet | Product | Product (features, specs, capabilities) |
| FAQ | Product/topic | Common objections, use cases |
| Objection Handler | Objections, persona | Persona concerns, proof points, competitors |
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

**Missing Competitor (for battlecard):**
> Competitor "[name]" not found in your library.
>
> Options:
> 1. Add competitor first (/octave:library create competitor)
> 2. I'll research and create a basic battlecard (less accurate)
> 3. Choose from existing: [list competitors]

## Related Skills

- `/octave:brainstorm` - Generate content ideas before creating
- `/octave:generate` - Quick one-off content (emails, LinkedIn)
- `/octave:library` - Add/update entities used in content
- `/octave:analyzer` - Analyze existing content for improvements
