---
name: battlecard
description: Generate competitive battlecards, displacement campaigns, trap questions, and objection counters grounded in library data and real deal evidence — as inline text analysis or a polished HTML battlecard document. Use when user says "battlecard for [competitor]", "how do we beat [competitor]", "competitive intel", "trap questions", "displacement campaign", "visual battlecard", "battlecard document", "competitive reference doc", or mentions competing against a rival.
argument-hint: "[mode] [--competitor <name>] [--persona <name>] [--format text|doc] [--style <preset>]"
---

# /octave:battlecard - Competitive War Room

Dedicated competitive intelligence skill that generates living competitive artifacts — battlecards, displacement campaigns, trap questions, objection counters, and side-by-side comparisons — all grounded in your library's competitive data and real conversation evidence.

One intelligence pipeline, two output formats:
- **Text (default)** — inline analysis, fast to iterate on and easy to paste anywhere.
- **Doc (`--format doc`)** — a self-contained HTML reference document with sticky sidebar navigation, color-coded win/loss indicators, expandable objection handlers, and a visual scorecard. Designed to be bookmarked and referenced during live competitive deals.

## Usage

```
/octave:battlecard [mode] [--competitor <name>] [--persona <name>] [--format text|doc] [--style <preset>]
```

## Modes

```
/octave:battlecard                                        # Interactive - pick competitor and mode
/octave:battlecard battlecard --competitor "Acme"         # Full competitive battlecard
/octave:battlecard displacement --competitor "Acme"       # Displacement campaign
/octave:battlecard traps --competitor "Acme"              # Trap questions to expose weaknesses
/octave:battlecard objections --competitor "Acme"         # Objection counters
/octave:battlecard compare --competitor "Acme"            # Side-by-side comparison
/octave:battlecard landscape                              # Full competitive landscape overview
/octave:battlecard --competitor "Acme" --format doc       # HTML battlecard document
/octave:battlecard landscape --format doc --style neon-pulse
```

## Instructions

When the user runs `/octave:battlecard`:

### Step 1: Identify Competitor, Mode, and Format

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
4. Objection Counters - Paired risk-and-response guidance
5. Side-by-Side Compare - Feature/capability comparison
6. Competitive Landscape - Overview of all competitors

Your choice:
```

**Output format.** Default is text. Switch to the HTML document when the user passes `--format doc` or asks for a "battlecard document", "visual battlecard", or something to bookmark and share. The doc format applies to the Full Battlecard and Competitive Landscape modes; the other modes (displacement, traps, objections, compare) are text-first — offer to fold their content into a full document if the user wants one.

### Step 2: Gather Competitive Intelligence

This research plan feeds both formats. Layer multiple sources — competitor profile + deal outcomes + conversation evidence + proof points combine into intelligence grounded in real data. Don't stop at one tool when three would give a stronger picture.

```
# Get competitor entity
get_entity({ oId: "<competitor_oId>" })

# Find Custom Motion Playbooks for this competitor (narrative type COMPETITIVE)
list_motions()
list_motion_playbooks({ motionOId: "<motion_oId>" })
# Filter for narrativeType === "COMPETITIVE" and matching competitor
get_motion_playbook({ motionPlaybookOId: "<motion_playbook_oId>" })

# Also pull the Default Motion Playbook's Motion ICPs for general positioning
list_motion_icps({ motionOId: "<motion_oId>" })
find_motion_icp({ motionIcpOId: "<motion_icp_oId>", includeLearnings: true })

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

Also useful: `list_entities({ entityType: "proof_point" })` and `list_entities({ entityType: "reference" })` for switching stories, and `search_resources({ query: "<competitor>" })` for uploaded analyst reports or competitive docs. For landscape mode, run the deal and findings queries without the competitor filter and fetch `list_entities({ entityType: "competitor" })` for full profiles.

### Step 3: Generate Mode-Specific Output (text format)

**Output discipline.** A battlecard is an internal seller tool, so follow the shared output rules in [../shared/presentation-principles.md](../shared/presentation-principles.md), with two that bite competitive content most:
- **Talking points, not scripts.** Positioning, objection responses, and the displacement "if they respond" flow are **points the rep adapts**, never word-for-word lines to recite. Objection titles describe the *risk* ("They anchor on price"), never quote the prospect — the actual line goes in "You'll hear". **The one exception: trap questions**, which are precision instruments meant to be asked nearly verbatim. (Email/LinkedIn copy generated via `generate_email` is a written deliverable — that stays written, just keep it human.)
- **Link cited entities (internal only).** Since this is an internal doc, link each cited competitor, proof point, reference, or objection entity to `https://app.octavehq.com/entity/{oId}` (the `oId` from its tool result) so the rep is one click from the source. Never put these links in a customer-facing asset.

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

### Step 4: Doc Format (--format doc)

When the format is `doc`, gather intelligence exactly as in Step 2, then:

1. **Content brief + approval.** Present a structured outline (competitor, data sources, win rate, planned sections) and **wait for user approval** before generating. See [html-doc.md](references/html-doc.md) for the brief template and section specs.
2. **Brand styling.** This is an internal document, so default to **your own company's** brand kit if one exists; follow [../shared/brand-kit-usage.md](../shared/brand-kit-usage.md) for kit lookup, offer, and fallback.
3. **Style selection.** If no kit is used, pick a preset from [../shared/style-presets.md](../shared/style-presets.md). Dark presets (`neon-pulse`, `electric-studio`) suit battlecards; skip the prompt if `--style` was provided.
4. **Generate HTML.** Build a single self-contained file per [html-doc.md](references/html-doc.md) — no external dependencies except Google Fonts. Save under:
   ```
   .octave-battlecards/
   └── battlecard-<competitor-kebab>-<YYYY-MM-DD>/
       └── battlecard-<competitor-kebab>.html
   ```
   Landscape mode: `.octave-battlecards/battlecard-landscape-<YYYY-MM-DD>/battlecard-landscape.html`. The `.octave-battlecards/` directory is gitignored — nothing here gets committed.
5. **Review pass (runs by default).** Follow [../shared/review-pass.md](../shared/review-pass.md): the preflight always runs; the visual pass runs unless the user opts out with `--skip-review` or "skip review". Tell the user at intake that you'll review before finishing.
6. **Delivery.** Open the document in the default browser and present a summary (file path, style, sections, data sources, win rate, navigation tips). For PDF export, run the plugin's export helper: `bash "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/export-pdf.sh <path-to-html>` — or Cmd+P / Ctrl+P → Save as PDF (the sidebar is hidden in print).

The output-discipline rules from Step 3 apply in full — talking points not scripts, entity deep-links, label every value.

### Step 5: Offer Follow-Up Actions

```
What would you like to do next?

1. Deep dive on a specific area
2. Generate displacement outreach for a specific person
3. Create a persona-specific version
4. Re-generate any piece using a saved agent
5. Update competitor entity with new insights
6. Render as an HTML document (or refresh the doc)
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
- `list_entities` (competitor / product / proof_point / reference) - Full entity data
- `get_entity` - Get competitor or product details
- `search_knowledge_base` - Find competitive positioning, proof points
- `list_findings` - Real conversation mentions and objections
- `list_events` - Deal win/loss data against competitor
- `get_event_detail` - Deep dive into specific competitive deals
- `search_resources` - Uploaded analyst reports and competitive docs

### Library Context
- `list_motions` - List Motions in the workspace
- `list_motion_playbooks` - Surface Custom Motion Playbooks (narrative type COMPETITIVE) layered onto each Motion
- `get_motion_playbook` - Full details for a Custom Motion Playbook (competitive narrative)
- `list_motion_icps` - List Motion ICP cells (persona × segment) for a Motion
- `find_motion_icp` - Motion ICP narrative + Learning Loop learnings

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

**No Conversation Evidence:**
> No conversation mentions found for [Competitor].
>
> The objection handlers and trap questions will be based on library data and general competitive positioning rather than real conversation evidence. They'll improve as your team logs more calls where this competitor comes up.

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The battlecard builder needs Octave data to pull competitor profiles, deal outcomes, and conversation evidence.
>
> To reconnect: check your MCP configuration or run `/octave:workspace status`

## Related Skills

- `/octave:research` - Research a specific account in a competitive deal
- `/octave:brief` - Account-focused dossier for a specific competitive deal
- `/octave:deck` - Competitive presentation for an audience (the battlecard doc is a reference, not a deck)
- `/octave:campaign` - Generate competitive campaign content
- `/octave:insights` - Surface competitive mentions from conversations
- `/octave:wins-losses` - Analyze win/loss patterns against competitors
- `/octave:enablement` - Package competitive intel for the team
