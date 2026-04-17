---
name: battlecard
description: "Generate competitive battlecards, displacement campaigns, trap questions, and objection counters as text-based analysis grounded in library data and real deal evidence. Use when user says 'battlecard for [competitor]', 'how do we beat [competitor]', 'competitive intel', 'trap questions', 'displacement campaign', or mentions competing against a rival. Do NOT use for visual HTML battlecard documents — use /octave:battlecard-doc instead."
---

# /octave:battlecard - Competitive War Room

Dedicated competitive intelligence skill that generates living competitive artifacts — battlecards, displacement campaigns, trap questions, objection counters, and side-by-side comparisons — all grounded in your library's competitive data and real conversation evidence.

## Usage

```
/octave:battlecard [mode] [--competitor <name>] [--persona <name>]
```

## Modes

| Mode | Command | Description |
|------|---------|-------------|
| Interactive | `/octave:battlecard` | Pick competitor and mode |
| Full Battlecard | `/octave:battlecard battlecard --competitor "Acme"` | Comprehensive positioning guide for sales |
| Displacement | `/octave:battlecard displacement --competitor "Acme"` | Outreach campaign to win their customers |
| Traps | `/octave:battlecard traps --competitor "Acme"` | Discovery questions exposing weaknesses |
| Objections | `/octave:battlecard objections --competitor "Acme"` | "They say X, we say Y" paired responses |
| Compare | `/octave:battlecard compare --competitor "Acme"` | Side-by-side feature/capability comparison |
| Landscape | `/octave:battlecard landscape` | Full competitive landscape overview |

## Instructions

### Step 1: Identify Competitor and Mode

If no competitor specified, fetch available competitors:

```
list_all_entities({ entityType: "competitor" })
```

Present a numbered list of competitors from the library, plus options to research a new competitor or view the full landscape.

If no mode specified, present the six modes listed above and ask the user to choose.

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

#### Validation Checkpoint

Before generating output, verify data sufficiency:

- **Minimum sources**: At least 2 data sources returned results (competitor entity, playbook, proof points, findings, or deal events). If fewer than 2 sources returned data, warn the user: "Limited competitive data available — output will rely on [available source]. Consider enriching your library with `/octave:library create competitor` for richer results."
- **Deal data gap**: If no win/loss events exist, note: "No deal outcome data found. Battlecard will be built from library positioning and conversation data only."
- **Stale data**: If the most recent finding or event is older than 90 days, flag: "Most recent competitive data is from [date]. Consider refreshing with recent deal outcomes."

### Step 3: Generate Mode-Specific Output

Select the appropriate output format based on the chosen mode. Full output templates with complete structural skeletons are provided in the reference files below.

| Mode | Template Reference | Key Sections |
|------|-------------------|--------------|
| **Full Battlecard** | [full-battlecard-template.md](references/full-battlecard-template.md) | Quick positioning, where we win/lose, objections, trap questions, landmines, proof points, win/loss patterns |
| **Displacement** | [displacement-template.md](references/displacement-template.md) | Positioning strategy, 4-email sequence via `generate_email()`, LinkedIn messages, talk track |
| **Traps** | [traps-template.md](references/traps-template.md) | 5-8 discovery questions with "why this works" rationale and sequencing advice |
| **Objections** | [objections-template.md](references/objections-template.md) | Pricing, feature, relationship, and risk objection categories with proof points |
| **Compare** | [compare-template.md](references/compare-template.md) | Feature comparison table, detailed per-category analysis, honest summary |
| **Landscape** | [landscape-template.md](references/landscape-template.md) | Market map table, key themes, per-competitor snapshots |

**Key principles for all modes:**
- Ground every claim in library data — cite proof points, deal evidence, and conversation findings
- Be honest about competitor strengths (builds credibility with sales teams)
- Include source attribution at the end of each output
- Use `generate_email()` for displacement email content; use `generate_content()` or write directly for other modes

### Step 4: Offer Follow-Up Actions

After delivering any mode's output, offer these next steps:
- Deep dive on a specific area
- Generate displacement outreach for a specific person
- Create a persona-specific version
- Re-generate using a saved agent
- Update competitor entity with new insights
- Export/share with team

## Generation Mode Note

This skill uses Octave's `generate_content` and `generate_email` tools by default. Two alternatives:
- **Saved agents**: Check for matching agents with `list_agents` when relevant. See `/octave:explore-agents`.
- **Claude-direct**: Skip `generate_*` calls, gather Octave context, Claude writes directly. Offer when user wants more control.

For the full interactive mode selector, use `/octave:generate`.

## MCP Tools Used

### Competitive Intelligence
- `list_all_entities` (competitor) — List all competitors
- `get_entity` — Get competitor details
- `search_knowledge_base` — Find competitive positioning, proof points
- `list_findings` — Real conversation mentions and objections
- `list_events` — Deal win/loss data against competitor
- `get_event_detail` — Deep dive into specific competitive deals

### Library Context
- `get_playbook` — Competitive playbooks and value props
- `list_value_props` — Value propositions per persona
- `get_entity` (product) — Product capabilities for comparison

### Content Generation
- `generate_email` — Displacement email campaigns
- `generate_content` — Trap questions, objection guides, comparisons

## Error Handling

- **No competitors in library**: Suggest adding one via `/octave:library create competitor` or offer to build a basic comparison from the provided name
- **No deal data**: Build from library positioning and conversation data; note the battlecard will improve as deals are logged
- **Competitor not in library**: Offer to create the entity via `/octave:library create competitor "[name]"` or generate a basic comparison with available information

## Related Skills

- `/octave:research` — Research a specific account in a competitive deal
- `/octave:campaign` — Generate competitive campaign content
- `/octave:insights` — Surface competitive mentions from conversations
- `/octave:wins-losses` — Analyze win/loss patterns against competitors
- `/octave:enablement` — Package competitive intel for the team
