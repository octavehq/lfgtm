---
name: messaging
description: Build messaging frameworks, positioning statements, messaging matrices, elevator pitches, and narrative arcs from your library. Use when user says "messaging framework", "positioning statement", "elevator pitch", "messaging matrix", "narrative arc", or asks to align or structure messaging.
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
list_all_entities(entityType: "brand_voice")

# Get conversation insights for what resonates
list_findings({
  query: "value propositions that resonated positive reactions",
  startDate: "<90 days ago>",
  eventFilters: { sentiments: ["POSITIVE"] }
})
```

### Step 3: Generate Mode-Specific Output

#### Mode: Messaging Framework

See [messaging-framework.md](references/messaging-framework.md) for the messaging framework mode template.

#### Mode: Positioning Statement

See [positioning-statement.md](references/positioning-statement.md) for the positioning statement mode template.

#### Mode: Messaging Matrix

See [messaging-matrix.md](references/messaging-matrix.md) for the messaging matrix mode template.

#### Mode: Elevator Pitches

See [elevator-pitches.md](references/elevator-pitches.md) for the elevator pitches mode template.

#### Mode: Narrative Arc

See [narrative-arc.md](references/narrative-arc.md) for the narrative arc mode template.

#### Mode: Value Prop Hierarchy

See [value-prop-hierarchy.md](references/value-prop-hierarchy.md) for the value prop hierarchy mode template.

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
- `list_all_entities` (entityType: "brand_voice") - Brand voice for tone consistency
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

- `/octave:positioning` - Complete visual positioning system as HTML document (the visual counterpart to this skill)
- `/octave:campaign` - Generate campaign content from your messaging
- `/octave:pmm` - Create collateral that uses this messaging
- `/octave:launch` - Build a launch plan around this messaging
- `/octave:brainstorm messaging-angles` - Brainstorm new angles
- `/octave:library` - Update library entities with finalized messaging
