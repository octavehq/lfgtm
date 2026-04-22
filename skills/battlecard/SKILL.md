---
name: battlecard
description: Generate competitive battlecards, displacement campaigns, trap questions, and objection counters as text-based analysis grounded in library data and real deal evidence. Use when user says "battlecard for [competitor]", "how do we beat [competitor]", "competitive intel", "trap questions", "displacement campaign", or mentions competing against a rival. Do NOT use for visual HTML battlecard documents — use /octave:battlecard-doc instead.
---

# /octave:battlecard - Competitive War Room

Dedicated competitive intelligence skill that generates living competitive artifacts — battlecards, displacement campaigns, trap questions, objection counters, and side-by-side comparisons — all grounded in your library's competitive data and real conversation evidence.

## Usage

```
/octave:battlecard [mode] [--competitor <name>] [--persona <name>]
```

## Modes

```
/octave:battlecard                                        # Interactive - pick competitor and mode
/octave:battlecard battlecard --competitor "Acme"         # Full competitive battlecard
/octave:battlecard displacement --competitor "Acme"       # Displacement campaign
/octave:battlecard traps --competitor "Acme"              # Trap questions to expose weaknesses
/octave:battlecard objections --competitor "Acme"         # "They say X, we say Y" guide
/octave:battlecard compare --competitor "Acme"            # Side-by-side comparison
/octave:battlecard landscape                              # Full competitive landscape overview
```

## Instructions

When the user runs `/octave:battlecard`:

### Step 1: Identify Competitor and Mode

If no competitor specified, list available competitors:

```
# Get all competitors
list_all_entities({ entityType: "competitor" })
```

Present:
```
Which competitor are you focused on?

COMPETITORS IN YOUR LIBRARY
1. [Competitor 1] - [Brief description]
2. [Competitor 2] - [Brief description]
3. [Competitor 3] - [Brief description]

OTHER
4. Research a new competitor (provide name/domain)
5. Full competitive landscape (all competitors)

Your choice:
```

If no mode specified, ask:
```
What do you need?

1. Full Battlecard - Comprehensive positioning guide for sales
2. Displacement Campaign - Outreach to steal their customers
3. Trap Questions - Discovery questions that expose their weaknesses
4. Objection Counters - "They say X, we say Y" paired responses
5. Side-by-Side Compare - Feature/capability comparison
6. Competitive Landscape - Overview of all competitors

Your choice:
```

### Step 2: Gather Competitive Intelligence

```
# Get competitor entity
get_entity({ oId: "<competitor_oId>" })

# Search for playbooks that mention this competitor
search_knowledge_base({
  query: "<competitor name> competitive positioning",
  entityTypes: ["playbook"]
})

# Get relevant playbook with value props
get_playbook({ oId: "<playbook_oId>", includeValueProps: true })

# Search for proof points (especially competitive wins)
search_knowledge_base({
  query: "<competitor name> win switch migration",
  entityTypes: ["proof_point", "reference"]
})

# Search conversation data for competitor mentions
list_findings({
  query: "<competitor name> objections competitive mentions",
  startDate: "<90 days ago>",
  eventFilters: {
    competitors: ["<competitor_oId>"]
  }
})

# Get won deals where this competitor was present
list_events({
  startDate: "<180 days ago>",
  filters: {
    eventTypes: ["DEAL_WON"],
    competitors: ["<competitor_oId>"]
  }
})

# Get lost deals to this competitor
list_events({
  startDate: "<180 days ago>",
  filters: {
    eventTypes: ["DEAL_LOST"],
    competitors: ["<competitor_oId>"]
  }
})

# Get product details for comparison
list_all_entities({ entityType: "product" })
get_entity({ oId: "<product_oId>" })
```

### Step 3: Generate Mode-Specific Output

---

#### Mode: Full Battlecard

See [full-battlecard.md](references/full-battlecard.md) for the full battlecard template.

---

#### Mode: Displacement Campaign

See [displacement-campaign.md](references/displacement-campaign.md) for the displacement campaign template (generate_email call + email sequence output format).

---

#### Mode: Trap Questions

See [trap-questions.md](references/trap-questions.md) for the trap questions template.

---

#### Mode: Objection Counters

See [objection-counters.md](references/objection-counters.md) for the objection counters template.

---

#### Mode: Side-by-Side Compare

See [side-by-side-compare.md](references/side-by-side-compare.md) for the side-by-side comparison template.

---

#### Mode: Competitive Landscape

See [competitive-landscape.md](references/competitive-landscape.md) for the competitive landscape template.

### Step 4: Offer Follow-Up Actions

```
What would you like to do next?

1. Deep dive on a specific area
2. Generate displacement outreach for a specific person
3. Create a persona-specific version
4. Re-generate any piece using a saved agent
5. Update competitor entity with new insights
6. Share with team (export)
7. Done
```

## Generation Mode Note

This skill uses Octave's `generate_content` and `generate_email` tools by default. Two alternatives:
- **Saved agents**: Check for matching agents with `list_agents` when relevant. See `/octave:explore-agents`.
- **Claude-direct**: Skip `generate_*` calls, gather Octave context, Claude writes directly. Offer when user wants more control.

For the full interactive mode selector, use `/octave:generate`.

## MCP Tools Used

### Competitive Intelligence
- `list_all_entities` (competitor) - List all competitors
- `get_entity` - Get competitor details
- `search_knowledge_base` - Find competitive positioning, proof points
- `list_findings` - Real conversation mentions and objections
- `list_events` - Deal win/loss data against competitor
- `get_event_detail` - Deep dive into specific competitive deals

### Library Context
- `get_playbook` - Competitive playbooks and value props
- `list_value_props` - Value propositions per persona
- `get_entity` (product) - Product capabilities for comparison

### Content Generation
- `generate_email` - Displacement email campaigns
- `generate_content` - Trap questions, objection guides, comparisons

## Error Handling

**No Competitors in Library:**
> No competitors found in your library.
>
> Options:
> 1. Add a competitor first: `/octave:library create competitor`
> 2. Tell me the competitor name and I'll create a basic comparison

**No Deal Data:**
> No win/loss data found against [Competitor].
>
> I'll build the battlecard from library data and general positioning.
> As you log deals, the battlecard will get richer with real evidence.

**Competitor Not in Library:**
> "[Name]" isn't in your library yet.
>
> Options:
> 1. Create the competitor entity first: `/octave:library create competitor "[name]"`
> 2. I'll generate a basic comparison with available information

## Related Skills

- `/octave:research` - Research a specific account in a competitive deal
- `/octave:campaign` - Generate competitive campaign content
- `/octave:insights` - Surface competitive mentions from conversations
- `/octave:wins-losses` - Analyze win/loss patterns against competitors
- `/octave:enablement` - Package competitive intel for the team
