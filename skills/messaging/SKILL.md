---
name: messaging
description: Build messaging frameworks, positioning statements, messaging matrices, and narrative arcs from your library
---

# /octave:messaging - Messaging Framework Builder

Generate structured messaging frameworks — positioning statements, messaging matrices, elevator pitches, and narrative arcs — all derived from your library's products, personas, playbooks, and competitive intelligence.

## Usage

```
/octave:messaging [mode] [--product <name>] [--persona <name>] [--competitor <name>]
```

## Modes

```
/octave:messaging                                         # Interactive mode
/octave:messaging matrix                                  # Persona x use case messaging matrix
/octave:messaging framework                               # Full messaging framework
/octave:messaging positioning                             # Positioning statement
/octave:messaging elevator                                # Elevator pitches (15s/30s/60s/2min)
/octave:messaging narrative                               # Company/product narrative arc
/octave:messaging value-props                             # Value proposition hierarchy
```

## Instructions

When the user runs `/octave:messaging`:

### Step 1: Determine Mode and Focus

If no mode specified, ask:

```
What messaging artifact do you need?

STRATEGIC
1. Messaging Framework - Complete: pillars, proof points, key messages by audience
2. Positioning Statement - Problem → solution → differentiation → proof
3. Narrative Arc - Situation → complication → resolution story

TACTICAL
4. Messaging Matrix - Persona × use case grid with tailored messages
5. Value Prop Hierarchy - Primary → secondary → supporting value props
6. Elevator Pitches - 15-second through 2-minute versions

Your choice:
```

Then ask for focus:
```
What's the focus?

1. [Product 1 from library]
2. [Product 2 from library]
3. Entire company / all products
4. Specific use case or segment

Your choice:
```

### Step 2: Gather Library Intelligence

```
# Get all core entities for messaging context
list_all_entities({ entityType: "product" })
list_all_entities({ entityType: "persona" })
list_all_entities({ entityType: "segment" })
list_all_entities({ entityType: "use_case" })
list_all_entities({ entityType: "competitor" })

# Get full product details
get_entity({ oId: "<product_oId>" })

# Get all playbooks and value props
list_all_entities({ entityType: "playbook" })
get_playbook({ oId: "<playbook_oId>", includeValueProps: true })

# Get proof points for evidence
search_knowledge_base({
  query: "<product> results metrics outcomes",
  entityTypes: ["proof_point", "reference"]
})

# Get competitive positioning
search_knowledge_base({
  query: "<product> differentiation unique advantage",
  entityTypes: ["competitor"]
})

# Get brand voice
list_brand_voices()

# Get conversation insights for what resonates
list_findings({
  query: "value propositions that resonated positive reactions",
  startDate: "<90 days ago>",
  eventFilters: { sentiments: ["POSITIVE"] }
})
```

### Step 3: Generate Mode-Specific Output

---

#### Mode: Messaging Framework

```
generate_content({
  instructions: "Generate a comprehensive messaging framework for [product/company].
    Structure:
    - Core positioning statement
    - 3-4 messaging pillars with supporting points
    - Key messages by audience (for each persona)
    - Proof points mapped to each pillar
    - Competitive differentiators
    All grounded in the library data provided.",
  customContext: "<all gathered library intelligence>"
})
```

Present as:
```
MESSAGING FRAMEWORK: [Product/Company]
=======================================

CORE POSITIONING
----------------
For [target audience]
Who [need/pain point]
[Product] is a [category]
That [key benefit]
Unlike [alternative/status quo]
We [key differentiator]

---

MESSAGING PILLARS
-----------------

PILLAR 1: [Theme]
━━━━━━━━━━━━━━━━━
Core Message: "[One-line message]"

Supporting Points:
• [Point 1]
• [Point 2]
• [Point 3]

Proof: [Metric, customer quote, or evidence]

---

PILLAR 2: [Theme]
━━━━━━━━━━━━━━━━━
Core Message: "[One-line message]"

Supporting Points:
• [Point 1]
• [Point 2]
• [Point 3]

Proof: [Evidence]

---

PILLAR 3: [Theme]
━━━━━━━━━━━━━━━━━
Core Message: "[One-line message]"

Supporting Points:
• [Point 1]
• [Point 2]
• [Point 3]

Proof: [Evidence]

---

KEY MESSAGES BY AUDIENCE
------------------------

For [Persona 1 - e.g., "CTO"]:
• Lead with: "[Message aligned to their priorities]"
• Emphasize: [Pillar most relevant to them]
• Proof point: "[Most compelling for this audience]"
• Avoid: "[What doesn't resonate with this persona]"

For [Persona 2 - e.g., "VP Sales"]:
• Lead with: "[Message]"
• Emphasize: [Pillar]
• Proof point: "[Evidence]"
• Avoid: "[What to skip]"

[Repeat for each persona]

---

COMPETITIVE DIFFERENTIATION
----------------------------
vs. [Competitor 1]: "[How we're different]"
vs. [Competitor 2]: "[How we're different]"
vs. Status Quo: "[Why change at all]"

---

WHAT WE SAY / WHAT WE DON'T SAY
---------------------------------
✓ Say: "[Approved language]"
✗ Don't say: "[Language to avoid and why]"

✓ Say: "[Approved language]"
✗ Don't say: "[Language to avoid and why]"

---

Sources Used:
- Products: [list]
- Personas: [list]
- Playbooks: [list]
- Proof Points: [list]
- Competitors: [list]
- Brand Voice: [name]

---

Want me to:
1. Create versions for specific personas
2. Generate elevator pitches from this framework
3. Build a messaging matrix
4. Save key messages as value props in a playbook
```

---

#### Mode: Positioning Statement

```
POSITIONING STATEMENTS: [Product]
==================================

FORMAL POSITIONING STATEMENT
-----------------------------
For [target audience]
Who [situation / pain point]
[Product] is a [category]
That [primary benefit]
Unlike [competitive alternative]
Our product [key differentiator]

---

VARIATIONS

By Persona:
For [Persona 1]: "[Tailored positioning]"
For [Persona 2]: "[Tailored positioning]"

By Segment:
For [Segment 1]: "[Tailored positioning]"
For [Segment 2]: "[Tailored positioning]"

By Use Case:
For [Use Case 1]: "[Tailored positioning]"
For [Use Case 2]: "[Tailored positioning]"

---

BOILERPLATE (for press, website, etc.)
--------------------------------------
Short (25 words): "[Company boilerplate]"
Medium (50 words): "[Company boilerplate]"
Long (100 words): "[Company boilerplate]"

---

Sources: [Products, personas, competitors, proof points]
```

---

#### Mode: Messaging Matrix

```
MESSAGING MATRIX: [Product]
============================

              | [Use Case 1]        | [Use Case 2]        | [Use Case 3]        |
|-------------|---------------------|---------------------|---------------------|
| [Persona 1] | Pain: [pain]        | Pain: [pain]        | Pain: [pain]        |
|             | Message: [msg]      | Message: [msg]      | Message: [msg]      |
|             | Proof: [proof]      | Proof: [proof]      | Proof: [proof]      |
|             | CTA: [cta]          | CTA: [cta]          | CTA: [cta]          |
|-------------|---------------------|---------------------|---------------------|
| [Persona 2] | Pain: [pain]        | Pain: [pain]        | Pain: [pain]        |
|             | Message: [msg]      | Message: [msg]      | Message: [msg]      |
|             | Proof: [proof]      | Proof: [proof]      | Proof: [proof]      |
|             | CTA: [cta]          | CTA: [cta]          | CTA: [cta]          |
|-------------|---------------------|---------------------|---------------------|
| [Persona 3] | Pain: [pain]        | Pain: [pain]        | Pain: [pain]        |
|             | Message: [msg]      | Message: [msg]      | Message: [msg]      |
|             | Proof: [proof]      | Proof: [proof]      | Proof: [proof]      |
|             | CTA: [cta]          | CTA: [cta]          | CTA: [cta]          |

---

DETAILED BREAKDOWNS
-------------------
[For each cell with highest priority, provide expanded messaging guidance]

[Persona 1] × [Use Case 1]:
Pain Point: "[Detailed pain point description]"
Key Message: "[2-3 sentence message]"
Supporting Points:
• [Point 1]
• [Point 2]
Proof Point: "[Specific evidence]"
Objection to Expect: "[Likely pushback]"
Response: "[How to handle]"
CTA: "[Specific call to action]"

---

COVERAGE GAPS
-------------
[Identify persona × use case combinations with weak or missing messaging]
⚠ [Persona X] × [Use Case Y]: No proof points available
⚠ [Persona X] × [Use Case Z]: No playbook coverage

---

Sources: [Personas, use cases, playbooks, proof points]
```

---

#### Mode: Elevator Pitches

```
ELEVATOR PITCHES: [Product]
============================

15-SECOND VERSION (Tweet-length)
---------------------------------
"[Punchy, memorable pitch]"

30-SECOND VERSION (Networking)
-------------------------------
"[Problem setup + solution + key differentiator]"

60-SECOND VERSION (Conference intro)
-------------------------------------
"[Problem with context + solution + how it works + proof point + CTA]"

2-MINUTE VERSION (Investor / executive)
----------------------------------------
"[Industry context + problem depth + solution vision + how it works +
  differentiation + traction/proof + ask]"

---

PERSONA-SPECIFIC VERSIONS (30-second)

For [Persona 1]:
"[Tailored to their language and priorities]"

For [Persona 2]:
"[Tailored to their language and priorities]"

---

TIPS
----
• Open with: [Best hook based on what resonates in conversations]
• Avoid: [Jargon or framing that falls flat]
• Always end with: [Specific CTA appropriate to context]

---

Sources: [Product, personas, proof points, conversation insights]
```

---

#### Mode: Narrative Arc

```
NARRATIVE ARC: [Product/Company]
=================================

THE STORY
---------

ACT 1: THE WORLD TODAY (Situation)
[Describe the status quo and why it exists]
"[Current state that everyone recognizes]"

ACT 2: THE BREAKING POINT (Complication)
[What's changing that makes the status quo unsustainable]
"[Trigger events, market shifts, growing pain]"

ACT 3: A NEW WAY (Resolution)
[How your product/company resolves the tension]
"[Vision of the better future your product enables]"

---

NARRATIVE ELEMENTS
------------------

The Villain: [What you're fighting against — a problem, not a competitor]
The Hero: [Your customer — not your product]
The Guide: [Your product/company — enables the hero]
The Stakes: [What happens if nothing changes]
The Transformation: [Before → After with your solution]

---

PROOF THE STORY IS REAL
------------------------
• [Customer who lived this narrative]
• [Metric that validates the transformation]
• [Market data supporting the complication]

---

USING THIS NARRATIVE
--------------------
In sales decks: [Which slides map to which acts]
In blog posts: [How to structure thought leadership around this arc]
In outreach: [How to reference the narrative in 1-2 sentences]
On the website: [How the homepage should flow]

---

Sources: [Product, use cases, proof points, market context]
```

---

#### Mode: Value Prop Hierarchy

```
VALUE PROPOSITION HIERARCHY: [Product]
=======================================

PRIMARY VALUE PROP
------------------
"[The #1 reason customers buy — in one sentence]"

SECONDARY VALUE PROPS
---------------------
1. "[Value prop 2]"
   Evidence: [Proof point]

2. "[Value prop 3]"
   Evidence: [Proof point]

3. "[Value prop 4]"
   Evidence: [Proof point]

SUPPORTING VALUE PROPS
----------------------
• [Additional benefit 1]
• [Additional benefit 2]
• [Additional benefit 3]

---

BY PERSONA PRIORITY
-------------------
[Persona 1] cares most about: [Rank value props 1-N]
[Persona 2] cares most about: [Rank value props 1-N]
[Persona 3] cares most about: [Rank value props 1-N]

---

EVIDENCE MAP
------------
| Value Prop | Proof Points | Confidence |
|-----------|-------------|-----------|
| [VP 1] | [proof 1, proof 2] | High |
| [VP 2] | [proof 1] | Medium |
| [VP 3] | [none yet] | Low - needs evidence |

---

FROM THE FIELD
--------------
[If conversation insights available:]
Most resonating value props (from real conversations):
1. "[VP that gets best reactions]" — mentioned in [N] positive conversations
2. "[VP 2]" — mentioned in [N] positive conversations

Value props that fall flat:
• "[VP that doesn't land]" — [Why, based on conversation data]

---

Sources: [Products, playbooks, value props, proof points, conversation findings]
```

### Step 4: Offer Follow-Up Actions

After generating any messaging artifact:

```
What would you like to do next?

1. Generate another messaging artifact
2. Create a persona-specific version
3. Save key messages to a playbook as value props
4. Generate campaign content from this messaging
5. Export this framework
6. Done
```

If the user wants to save messaging back to the library:
```
# Update playbook value props
add_value_props({
  playbookOId: "<playbook_oId>",
  instructions: "<key messages to add>",
  numValuesPerPersona: 3
})

# Or update product positioning
update_entity({
  entityType: "product",
  oId: "<product_oId>",
  instructions: "Update positioning to: [new positioning statement]"
})
```

## MCP Tools Used

### Library Context
- `list_all_entities` - List products, personas, segments, use cases, competitors
- `get_entity` - Get full entity details
- `get_playbook` - Get playbook with value props
- `list_value_props` - Get existing value propositions
- `search_knowledge_base` - Find proof points, references, competitive intel
- `list_brand_voices` - Brand voice for tone consistency
- `list_findings` - What resonates in real conversations

### Content Generation
- `generate_content` - Generate messaging artifacts

### Library Updates
- `add_value_props` - Save new value props to playbooks
- `update_entity` - Update product positioning

## Error Handling

**No Products Found:**
> No products in your library.
>
> Messaging frameworks need product information as a foundation.
> Run `/octave:library create product` first, or describe your product and I'll work from that.

**No Personas Found:**
> No personas defined yet.
>
> I can generate a basic messaging framework from your product, but persona-specific
> messaging requires persona definitions.
> Run `/octave:library create persona` to add personas.

**No Proof Points:**
> No proof points found to support the messaging.
>
> I'll generate the framework with placeholder evidence.
> Mark items tagged [NEEDS EVIDENCE] and add proof points as they become available.

## Related Skills

- `/octave:campaign` - Generate campaign content from your messaging
- `/octave:pmm` - Create collateral that uses this messaging
- `/octave:launch` - Build a launch plan around this messaging
- `/octave:brainstorm messaging-angles` - Brainstorm new angles
- `/octave:library` - Update library entities with finalized messaging
