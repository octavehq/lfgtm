---
name: brainstorm
description: Brainstorm campaigns, playbook ideas, lead magnets, CTAs, and growth experiments using your GTM library. Use when user says "brainstorm ideas", "campaign ideas", "growth experiments", "what content should we create", or asks for creative ideation.
---

# /octave:brainstorm - GTM Ideation Engine

Interactive brainstorming for campaigns, playbook concepts, lead magnets, CTAs, offers, and growth experiments—all grounded in your Octave library context.

## Usage

```
/octave:brainstorm [topic]
```

## Examples

```
/octave:brainstorm                           # Open-ended, asks what to brainstorm
/octave:brainstorm campaigns for enterprise  # Campaign ideas for enterprise segment
/octave:brainstorm lead magnets              # Content offer ideas
/octave:brainstorm playbook pack             # Generate playbook concepts for TAM
/octave:brainstorm CTAs for CFOs             # Call-to-action ideas for persona
```

## Instructions

When the user runs `/octave:brainstorm`:

### Step 1: Determine Brainstorm Type

If no topic provided, ask:

```
What would you like to brainstorm?

1. Campaign Ideas - Outreach campaigns for specific segments/personas
2. Playbook Concepts - New playbook ideas to cover your TAM
3. Lead Magnets - Content offers to attract prospects
4. CTAs & Offers - Calls-to-action and promotional offers
5. Growth Experiments - Test ideas to improve conversion
6. Messaging Angles - New positioning approaches
7. Something else - Tell me what you're thinking

Your choice (or describe freely):
```

If topic is provided, infer the type and confirm:

```
I'll brainstorm lead magnet ideas for you. Sound good?
(Or tell me more about what you're looking for)
```

### Step 2: Gather Context

Use MCP tools based on brainstorm type:

**For Campaigns:**
```
- list_all_entities({ entityType: "segment" })
- list_all_entities({ entityType: "persona" })
- list_all_entities({ entityType: "playbook" })
- list_all_entities({ entityType: "use_case" })
```

**For Playbook Concepts:**
```
- list_all_entities({ entityType: "segment" })
- list_all_entities({ entityType: "persona" })
- list_all_entities({ entityType: "product" })
- list_all_entities({ entityType: "use_case" })
- list_all_entities({ entityType: "playbook" })  # To see existing coverage
```

**For Lead Magnets:**
```
- list_all_entities({ entityType: "persona" })
- list_all_entities({ entityType: "use_case" })
- list_all_entities({ entityType: "proof_point" })
- search_knowledge_base({ query: "pain points challenges problems" })
```

**For CTAs & Offers:**
```
- list_all_entities({ entityType: "persona" })
- list_all_entities({ entityType: "product" })
- list_all_entities({ entityType: "proof_point" })
```

**For Growth Experiments:**
```
- list_all_entities({ entityType: "playbook" })
- list_all_entities({ entityType: "segment" })
- list_all_entities({ entityType: "persona" })
```

### Step 3: Ask Scoping Questions (Optional)

If the request is broad, narrow the focus:

**For Campaigns:**
```
Let me tailor these campaign ideas. Quick questions:

1. Target segment? (e.g., Enterprise SaaS, Healthcare, All)
2. Target persona? (e.g., CTOs, VP Sales, Multiple)
3. Campaign goal? (e.g., awareness, demos, pipeline)
4. Channel preference? (e.g., email, LinkedIn, multi-channel)

(Answer any/all, or say "surprise me")
```

**For Playbook Pack:**
```
To generate playbook concepts for your TAM:

1. What verticals/industries should we cover?
2. Company size focus? (SMB, Mid-market, Enterprise, All)
3. Any specific use cases to emphasize?
4. Gaps you've noticed in current playbook coverage?

(Share what you know, or I'll analyze your library for gaps)
```

### Step 4: Generate Ideas

Present ideas in a structured, actionable format:

---

See [campaign-ideas-output.md](references/campaign-ideas-output.md) for the Campaign Ideas output template.

---

See [playbook-pack-output.md](references/playbook-pack-output.md) for the Playbook Pack output template.

---

See [lead-magnet-ideas-output.md](references/lead-magnet-ideas-output.md) for the Lead Magnet Ideas output template.

---

See [cta-offer-ideas-output.md](references/cta-offer-ideas-output.md) for the CTA & Offer Ideas output template.

### Step 5: Refine and Save

After presenting ideas, offer next steps:

```
What would you like to do next?

1. Develop one of these ideas further
2. Generate more ideas (different angle)
3. Save an idea to your library
4. Create content for an idea (/octave:generate or /octave:pmm)
5. Done for now

Your choice:
```

**If "Save to library":**
- Campaign → Create as playbook with campaign details in notes
- Lead Magnet → Create as collateral or resource reference
- Playbook concept → Use `create_playbook` to generate full playbook

**For Playbook Creation:**

1. **First, get available offerings:**
   ```
   list_all_entities({ entityType: "product" })
   ```

2. **Ask user which product/service this playbook is for:**
   ```
   Which product or service is this playbook for?

   1. [Product A] (px_abc123)
   2. [Product B] (px_def456)

   Your choice:
   ```

3. **Create the playbook:**
   ```
   create_playbook({
     name: "Healthcare Digital Transformation",
     description: "Sales playbook for healthcare digital transformation targeting CTO/VP IT personas",
     instructions: "Create a sales playbook for healthcare digital transformation. Target CTO/VP IT personas in healthcare organizations. Focus on HIPAA compliance, interoperability, and patient outcomes. Use the strategic angle of 'secure, compliant foundation for healthcare innovation'.",
     productOId: "<selected product oId>",
     keyContext: "<relevant context from the brainstorm>"
   })
   ```

## MCP Tools Used

### Read Operations
- `list_all_entities` - Get entities for context
- `get_entity` - Deep dive on specific entities
- `get_playbook` - Understand existing playbook coverage
- `search_knowledge_base` - Find relevant messaging and proof points

### Write Operations
- `create_entity` - Create new entities (except playbooks) from ideas
- `create_playbook` - Create new playbooks with offering association
- `add_value_props` - Add value props to new playbooks

## Brainstorm Modes Summary

| Mode | Output | Key Inputs |
|------|--------|------------|
| Campaigns | 3-5 campaign concepts with hooks, sequences, rationale | Segment, persona, channel |
| Playbook Pack | 3-7 playbook concepts covering TAM gaps | Current coverage, target markets |
| Lead Magnets | 3-5 content offer ideas with mechanics | Persona pain points, buying stage |
| CTAs & Offers | Tiered CTA options + promotional offers | Persona, funnel stage |
| Growth Experiments | Test hypotheses with success metrics | Current playbooks, conversion goals |
| Messaging Angles | Alternative positioning approaches | Product, competitors, personas |

## Error Handling

**Empty Library:**
> Your library needs some content for effective brainstorming.
>
> I can still generate ideas, but they'll be more generic.
> For better results, add at least:
> - 1 product
> - 2-3 personas
> - Key pain points
>
> Run /octave:library create to add content, or continue anyway?

**No Relevant Context:**
> I couldn't find [segment/persona] in your library.
>
> Options:
> 1. Brainstorm anyway (I'll use general knowledge)
> 2. Create [segment/persona] first (/octave:library create)
> 3. Choose a different focus

## Related Skills

- `/octave:generate` - Generate content for brainstormed ideas
- `/octave:pmm` - Develop lead magnets and collateral
- `/octave:library` - Create entities from brainstormed concepts
- `/octave:prospector` - Find prospects for brainstormed campaigns
- `/octave:audit` - Identify gaps to brainstorm around
- `/octave:campaign` - Turn brainstormed ideas into full campaigns
- `/octave:messaging` - Build messaging frameworks from brainstormed angles
