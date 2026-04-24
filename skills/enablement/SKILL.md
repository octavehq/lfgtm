---
name: enablement
description: Generate sales enablement materials — cheat sheets, objection guides, discovery question banks, competitive sheets, and onboarding kits from your library. Use when user says "cheat sheet", "objection guide", "discovery questions", "onboarding kit", "enablement materials", or asks for quick-reference sales tools.
---

# /octave:enablement - Sales Enablement Studio

Generate consumable sales enablement materials — quick reference cards, objection handling guides, discovery question banks, competitive cheat sheets, and onboarding kits — all grounded in your library data and real conversation evidence.

## Usage

```
/octave:enablement [type] [--persona <name>] [--competitor <name>] [--product <name>]
```

## Content Types

```
/octave:enablement                                        # Interactive mode
/octave:enablement quick-ref                              # Quick reference card
/octave:enablement objections                             # Objection handling guide
/octave:enablement discovery                              # Discovery question bank
/octave:enablement competitive-sheet                      # Competitive cheat sheet
/octave:enablement onboarding                             # New hire enablement kit
/octave:enablement persona-guide                          # Persona deep-dive for reps
/octave:enablement playbook-summary                       # Playbook quick reference
```

## Instructions

When the user runs `/octave:enablement`:

### Step 1: Determine Content Type

If no type specified, ask:

```
What enablement material do you need?

DAILY REFERENCE
1. Quick Reference Card - One-page cheat sheet for a topic
2. Objection Handling Guide - "They say X, we say Y" from real conversations
3. Discovery Question Bank - Questions organized by persona and stage

COMPETITIVE
4. Competitive Cheat Sheet - Pocket-sized competitive positioning guide

TEAM DEVELOPMENT
5. New Hire Onboarding Kit - Library walkthrough + essentials for new reps
6. Persona Deep-Dive - Everything a rep needs to know about selling to a persona
7. Playbook Quick Reference - Condensed playbook for quick consumption

Your choice:
```

Then ask for focus:
```
What's the focus?

1. Specific persona: [List personas]
2. Specific product: [List products]
3. Specific competitor: [List competitors]
4. Specific playbook: [List playbooks]
5. General / all
```

### Step 2: Gather Intelligence

Enablement materials are unique because they blend library data with conversation evidence:

```
# Get the focus entity
get_entity({ oId: "<entity_oId>" })

# Get related playbook
get_playbook({ oId: "<playbook_oId>", includeValueProps: true })

# Get real objections from conversations
list_findings({
  query: "objections pushback concerns hesitation",
  startDate: "<180 days ago>",
  eventFilters: {
    personas: ["<persona_oId>"]  // if persona-focused
  }
})

# Get positive signals (what's working)
list_findings({
  query: "positive reaction excited interested resonated",
  startDate: "<180 days ago>",
  eventFilters: {
    sentiments: ["POSITIVE"]
  }
})

# Get pain points mentioned
list_findings({
  query: "pain points challenges frustrations problems",
  startDate: "<180 days ago>"
})

# Get proof points
search_knowledge_base({
  query: "<focus area> results metrics",
  entityTypes: ["proof_point", "reference"]
})

# Get competitors for context
list_all_entities({ entityType: "competitor" })

# Get brand voice
list_all_entities(entityType: "brand_voice")
```

### Step 3: Generate Content Type

---

#### Type: Quick Reference Card

See [quick-reference-card-template.md](references/quick-reference-card-template.md) for the generate_content call and the QUICK REFERENCE output template.

---

#### Type: Objection Handling Guide

See [objection-handling-guide-template.md](references/objection-handling-guide-template.md) for the OBJECTION HANDLING GUIDE output template.

---

#### Type: Discovery Question Bank

See [discovery-question-bank-template.md](references/discovery-question-bank-template.md) for the DISCOVERY QUESTION BANK output template.

---

#### Type: Competitive Cheat Sheet

See [competitive-cheat-sheet-template.md](references/competitive-cheat-sheet-template.md) for the COMPETITIVE CHEAT SHEET output template.

---

#### Type: New Hire Onboarding Kit

See [new-hire-onboarding-kit-template.md](references/new-hire-onboarding-kit-template.md) for the NEW HIRE ENABLEMENT KIT output template.

---

#### Type: Persona Deep-Dive

See [persona-deep-dive-template.md](references/persona-deep-dive-template.md) for the PERSONA GUIDE output template.

---

#### Type: Playbook Quick Reference

See [playbook-quick-reference-template.md](references/playbook-quick-reference-template.md) for the PLAYBOOK QUICK REFERENCE output template.

### Step 4: Offer Follow-Up Actions

```
What would you like to do next?

1. Create another enablement piece
2. Re-generate any piece using a saved agent
3. Create a version for a different persona/product
4. Combine into a full enablement package
5. Export as a document
6. Done
```

## Generation Mode Note

This skill uses Octave's `generate_content` and `generate_email` tools by default. Two alternatives:
- **Saved agents**: Check for matching agents with `list_agents` when relevant. See `/octave:explore-agents`.
- **Claude-direct**: Skip `generate_*` calls, gather Octave context, Claude writes directly. Offer when user wants more control.

For the full interactive mode selector, use `/octave:generate`.

## MCP Tools Used

### Library Context
- `list_all_entities` - All entity types for comprehensive coverage
- `get_entity` - Full entity details
- `get_playbook` - Playbook with value props
- `list_value_props` - Value propositions
- `search_knowledge_base` - Proof points, references, messaging

### Conversation Evidence
- `list_findings` - Real objections, pain points, signals from calls/emails
- `list_events` - Deal outcomes for win/loss evidence
- `get_event_detail` - Specific interaction details

### Content Generation
- `generate_content` - All enablement content types
- `list_all_entities` (entityType: "brand_voice") - Brand voice consistency

## Error Handling

**No Conversation Data:**
> No conversation data available yet.
>
> I'll generate enablement materials from your library.
> As your team logs calls and emails, these materials will get richer
> with real-world evidence.

**No Competitors:**
> No competitors in your library for competitive enablement.
>
> Options:
> 1. Add competitors: `/octave:library create competitor`
> 2. Skip competitive sections
> 3. I'll create a general competitive awareness template

**Empty Library:**
> Your library needs more content for a comprehensive enablement kit.
>
> Start with:
> 1. `/octave:library create product` - Add your product
> 2. `/octave:library create persona` - Add buyer personas
> Then run this skill again.

## Related Skills

- `/octave:train` - Practice with role-play simulations and quizzes using your enablement content
- `/octave:battlecard` - Full competitive intelligence (deeper than cheat sheet)
- `/octave:insights` - Surface field intelligence trends
- `/octave:wins-losses` - Win/loss patterns for objection effectiveness
- `/octave:pmm` - Marketing collateral (different audience than enablement)
- `/octave:research` - Deep research for specific accounts
