---
name: battlecard-doc
description: Visual competitive battlecard document rendered as interactive HTML with expandable sections and color-coded comparisons. Use when user says "battlecard document", "visual battlecard", "competitive reference doc", or wants a formatted HTML version of competitive intelligence. Do NOT use for text-based competitive analysis — use /octave:battlecard instead.
---

# /octave:battlecard-doc - Visual Competitive Battlecard

Generate polished, self-contained HTML competitive battlecard documents powered by your Octave GTM knowledge base. Designed to be bookmarked and referenced during live competitive deals. Sticky sidebar navigation, color-coded win/loss indicators, expandable objection handlers, and visual scorecard bars make these documents scannable under pressure.

Unlike `/octave:battlecard` which outputs text-based competitive intelligence, this skill renders that intelligence as a styled, interactive HTML document with visual hierarchy. Unlike `/octave:deck` which builds presentations for audiences, this is an internal reference document for individual use.

## Usage

```
/octave:battlecard-doc [--competitor <name>] [--style <preset>]
```

## Examples

```
/octave:battlecard-doc --competitor "Gong"                # Deep-dive battlecard for vs Gong
/octave:battlecard-doc                                    # Pick competitor interactively
/octave:battlecard-doc --competitor "all"                  # Full competitive landscape doc
/octave:battlecard-doc --competitor "Gong" --style neon-pulse
```

## Instructions

When the user runs `/octave:battlecard-doc`:

### Step 1: Identify Competitor(s)

If `--competitor` is not specified, fetch the competitor list and let the user choose:

```
# Get all competitors
list_all_entities({ entityType: "competitor" })
```

Present:

```
Which competitor are you building a battlecard for?

COMPETITORS IN YOUR LIBRARY
1. [Competitor 1] - [Brief description]
2. [Competitor 2] - [Brief description]
3. [Competitor 3] - [Brief description]

OTHER
4. Full competitive landscape (all competitors)

Your choice:
```

If they pick a single competitor, confirm the scope:

```
What kind of document do you want?

1. Full battlecard — comprehensive reference with all sections
2. Quick reference — positioning + objections + trap questions only

Your choice:
```

If they pick "all" or "Full competitive landscape," confirm:

```
I'll create a landscape overview with condensed battlecards for each competitor.
This includes a market map, per-competitor cards, and cross-competitor patterns.

Sound good? (y/n)
```

### Step 2: Octave Context Gathering

Based on the competitor(s) selected, use Octave MCP tools to build rich competitive context. **Always tell the user what you're researching and why.**

**Call as many tools as needed to build a complete picture.** The best battlecard documents come from layering multiple sources -- competitor profiles + deal outcomes + conversation evidence + proof points all combine to create a reference grounded in real data. Don't stop at one tool when three would give you a stronger document.

See [tool-reference.md](references/tool-reference.md) for the list-vs-search guidance and the tool reference tables for single-competitor and landscape modes.

**Output of this step:** Present a structured content brief to the user:

```
BATTLECARD OUTLINE: vs [Competitor]
====================================

Competitor: [Competitor name]
Data Sources: [N] deals analyzed, [N] conversation mentions, [N] proof points
Date Range: Last 180 days
Win Rate: [X%] ([N] wins / [N] losses)

---

SECTIONS
--------
1. Quick Positioning — one-liner + 30-second pitch
2. Competitor Overview — what they do, target, pricing, key customers
3. Where We Win — strengths table + real deal evidence
4. Where They Win — honest assessment + how to counter each
5. Objection Handlers — organized by category (pricing, feature, relationship, risk)
6. Trap Questions — discovery questions that expose weaknesses
7. Landmines to Set — evaluation criteria to plant early
8. Proof Points — switching stories, competitive wins, metrics
9. Win/Loss Scorecard — visual scoreboard with win rate and factors
10. Displacement Playbook — how to unseat them when entrenched

Octave Sources Used:
- Competitor entity: [name]
- Deals analyzed: [N] wins, [N] losses
- Conversation mentions: [N] findings
- Proof points: [N] relevant
- Playbooks: [list]

---

Does this outline look good? I can:
1. Proceed to style selection and generation
2. Add/remove sections
3. Go deeper on any area
4. Switch to landscape overview
```

**Wait for user approval before proceeding.**

### Step 3: Style Selection

Ask the user to select a visual style. Default recommendation for battlecards is `neon-pulse` (dark + neon green/cyan, high-energy) or `electric-studio` (pure black + electric blue).

```
Pick a style for your battlecard:

DARK (recommended for battlecards)
  1. neon-pulse       — Dark + neon green/cyan. High-energy. [DEFAULT]
  2. electric-studio  — Pure black + electric blue. Tech-forward.
  3. midnight-pro     — Dark navy + blue accents. Executive feel.
  4. executive-dark   — Charcoal + gold. Premium boardroom.

LIGHT
  5. swiss-modern     — White + red accent. Clean minimal.
  6. soft-light       — Warm white + sage green. Calm.
  7. paper-minimal    — Off-white + black type. Editorial.

VIBRANT
  8. solar-flare      — Deep orange gradients. Bold.
  9. aurora-gradient   — Purple-to-teal. Visionary.
  10. monochrome-bold — High-contrast B&W. Statement typography.

Your choice (number or name, or press Enter for neon-pulse):
```

If `--style` was provided via flag, skip this prompt and use that preset.

Full CSS variable definitions for each preset are in the deck skill's [style-presets.md](../deck/references/style-presets.md). Apply the same CSS variable system.

### Step 4: Generate HTML

Build a single, self-contained HTML file. **No external dependencies except Google Fonts.** Everything else inlined.

#### Output Directory

Save the battlecard under `.octave-decks/`:

```
.octave-decks/
└── battlecard-<competitor-kebab>-<YYYY-MM-DD>/
    └── battlecard-<competitor-kebab>.html
```

Example: `/octave:battlecard-doc --competitor "Gong"` produces `.octave-decks/battlecard-gong-2026-02-11/battlecard-gong.html`

For landscape: `.octave-decks/battlecard-landscape-2026-02-11/battlecard-landscape.html`

The entire `.octave-decks/` directory is in `.gitignore` -- nothing here gets committed.

#### Single Competitor -- Document Sections

See [single-competitor-sections.md](references/single-competitor-sections.md) for the single-competitor document section specs.

#### Landscape Overview -- Document Sections

See [landscape-sections.md](references/landscape-sections.md) for the landscape overview document section specs.

#### HTML Architecture

See [html-architecture.md](references/html-architecture.md) for the full HTML/CSS scaffold, landscape-mode component swaps, and key HTML/CSS principles.

### Step 5: Delivery

After generating the HTML file:

1. **Open the document** in the default browser
2. **Present a summary:**

```
BATTLECARD READY
================

Folder: .octave-decks/battlecard-<competitor>-<date>/
File:   .octave-decks/battlecard-<competitor>-<date>/battlecard-<competitor>.html
Style:  [Preset name]
Size:   [file size]

Competitor: [Competitor name]
Sections: [N] sections
Data sources: [N] deals, [N] conversation mentions, [N] proof points
Win rate: [X%] (last 180 days)

Navigation:
- Scroll naturally through the document
- Sidebar dots on the right track your position
- Click any dot to jump to that section
- Objection handlers: click to expand/collapse

---

Want me to:
1. Add more objection handlers
2. Go deeper on any section
3. Create displacement outreach for a specific person
4. Generate a version for a different persona
5. Create a presentation version (/octave:deck)
6. Export as PDF
7. Done
```

**If user requests PDF export:**

```
To save as PDF:
1. Open the file in your browser (should already be open)
2. Press Cmd+P (Mac) or Ctrl+P (Windows)
3. Select "Save as PDF" as the destination
4. Set margins to "Minimum" or "None" for best results
5. The sidebar navigation will be hidden in print
```

## MCP Tools Used

### Competitive Intelligence
- `list_all_entities` (competitor) -- List all competitors for selection or landscape
- `list_entities` (competitor) -- Full competitor profiles with data
- `get_entity` -- Deep dive on a specific competitor
- `search_knowledge_base` -- Competitive positioning, playbook matching, proof point discovery
- `list_findings` -- Real conversation mentions, objections, competitor references from calls
- `list_events` -- Deal win/loss outcomes against specific competitors
- `get_event_detail` -- Deep dive into specific competitive deals for evidence

### Library (Fetching / Searching)
- `get_playbook` -- Competitive playbooks with value props
- `list_value_props` -- Value propositions per playbook
- `list_entities` (product) -- Product capabilities for comparison
- `list_entities` (proof_point) -- Competitive win proof points and switching stories
- `list_entities` (reference) -- Customer references who switched from competitors
- `search_resources` -- Search uploaded analyst reports, battlecards, competitive docs

### Intelligence & Signals
- `list_findings` -- Conversation-based competitive insights and objection patterns
- `list_events` -- Deal stage changes, win/loss events with competitor filters
- `get_event_detail` -- Full details on specific competitive deals

## Error Handling

**No Competitors in Library:**
> No competitors found in your library.
>
> To build a battlecard, I need at least one competitor in your Octave library.
>
> Options:
> 1. Add a competitor first: `/octave:library create competitor`
> 2. Tell me the competitor name and I'll create a basic comparison from web research (limited data)

**No Deal Data for This Competitor:**
> No win/loss data found against [Competitor] in the last 180 days.
>
> I'll build the battlecard from library data, conversation mentions, and positioning. The win/loss scorecard and deal evidence sections will be limited.
>
> As you log deals with this competitor tagged, the battlecard will get richer with real evidence.

**Competitor Not in Library:**
> "[Name]" isn't in your competitor library yet.
>
> Options:
> 1. Create the competitor entity first: `/octave:library create competitor "[name]"`
> 2. I'll generate a basic battlecard from available information (playbooks, conversations, web research)

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The battlecard builder needs Octave data to generate competitive intelligence. Without it, I can't pull competitor profiles, deal outcomes, or conversation evidence.
>
> To reconnect: check your MCP configuration or run `/octave:workspace status`

**No Conversation Evidence:**
> No conversation mentions found for [Competitor].
>
> The objection handlers and trap questions will be based on library data and general competitive positioning rather than real conversation evidence. They'll improve as your team logs more calls where this competitor comes up.

## Related Skills

- `/octave:battlecard` -- Text-based competitive intelligence (this is the visual version)
- `/octave:brief` -- Account-focused dossier (when dealing with a specific account in a competitive deal)
- `/octave:deck` -- Competitive presentation for an audience (this is a reference doc)
- `/octave:wins-losses` -- Text-based win/loss analysis across competitors
- `/octave:campaign` -- Competitive campaign content and displacement outreach
- `/octave:research` -- Deep account research (feeds into account-specific competitive context)
- `/octave:insights` -- Surface competitive mentions from conversations
