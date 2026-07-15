---
name: battlecard-doc
description: Visual competitive battlecard document rendered as interactive HTML with expandable sections and color-coded comparisons. Use when user says "battlecard document", "visual battlecard", "competitive reference doc", or wants a formatted HTML version of competitive intelligence. Do NOT use for text-based competitive analysis — use /octave:battlecard-doc instead.
---

# /octave:battlecard-doc - Visual Competitive Battlecard

Generate polished, self-contained HTML deal cards powered by your Octave GTM knowledge base. Deal-specific competitive weapons designed to be picked up before a call and immediately tell you what to say. Side-by-side comparison grids, scannable sub-cards, and layered pitch sections make these documents usable under pressure.

Unlike `/octave:battlecard-doc` which outputs text-based competitive intelligence, this skill renders that intelligence as a styled, interactive HTML document with visual hierarchy. Unlike `/octave:deck` which builds presentations for audiences, this is an internal reference document for individual use.

## On-brand styling — brand kit first, then generate

**Resolve the brand before generating (do not skip this step).** The document brand should be the **workspace company's brand** — that is, the Octave customer whose workspace you are operating in. The **target company's logo** (the prospect/competitor) can appear in the deal context section (1-2 places) but does not control the document's design system.

**Step 1: Identify the workspace company.** Call `get_workspace_company` to get the company name, domain/URL, and positioning. This is the company whose brand the document should use (whatever get_workspace_company returns is the brand, not the target account).

**Step 2: Resolve the workspace company's brand kit.** Slugify the workspace company name and check for a cached brand kit at `~/.octave/brands/<slug>/manifest.json`. If a complete kit exists (has `manifest.json` and `tokens.css`), use it automatically:
   - inline the kit's `tokens.css` (`:root` + the embedded `@font-face`) **and** `get-brand-components/assets/kit_base.css` into the output `<style>`;
   - follow `brand-kit.md` → **Signature moves**, and reuse the kit's real **logo** for topbar and footer, `images/`, and `icons.json`.
   **If no complete kit exists → build one.** Run the `get-brand-components` skill (read `../../skills/get-brand-components/SKILL.md` and follow it) for the workspace company's domain. If the first attempt returns incomplete results (no logo, no colors, partial data) → retry up to 3 times with different approaches (root domain, `www.` prefix, `/about` subpage). Only fall back to a generic preset after 3 genuine failures.

**Step 3: Fetch the target company's logo.** Use `get_external_brand_logo` or `get_external_brand_assets` to get the prospect's logo. Place it in the topbar "prepared for" area and optionally in the deal context section. Do not use it for the document's overall design system — that uses the workspace company's brand.
   - If the first attempt returns no logo → retry up to 3 times.

**Step 4: Only use a generic preset as a last resort** — after the workspace company's brand kit cannot be built.

> **⚠️ STRONG DEFAULT:** The document is always branded as the workspace company (the Octave customer). The prospect's logo appears in the topbar and content to personalize the battlecard, but the overall look and feel — fonts, colors, topbar, footer — is the workspace company's brand. This is not the prospect's document; it is the workspace company's document about them.

## Quality principles -- load before generating

**Read these files before writing any HTML. They govern language, layout, and content decisions during generation -- not just during review.**

- [Editorial rules](../shared/editorial-rules.md) -- language quality, AI-ism kill list, banned vocabulary
- [Presentation principles](../shared/presentation-principles.md) -- universal visual rules, spacing, restraint
- [Information principles](../shared/information-principles.md) -- content structure, narrative arc, evidence quality
- [Format rules: HTML document](../shared/formats/html-document.md) -- format-specific rules for scrollable docs
- [Octave value](../shared/octave-value.md) -- prioritize grounded workspace data over generic AI content

Apply these rules during generation, not just at review. After generating, the **review pipeline is a mandatory gate** (see Step 4) -- the battlecard is not opened or delivered until the scorecard is produced.

## Usage

```
/octave:battlecard-doc [--competitor <name(s)>]
```

## Examples

```
/octave:battlecard-doc --competitor "Gong"                      # Deal card vs Gong
/octave:battlecard-doc --competitor "Auth0,FusionAuth"           # Multi-competitor deal card
/octave:battlecard-doc                                           # Pick account + competitors interactively
/octave:battlecard-doc --competitor "all"                        # Full competitive landscape doc
```

## Instructions

When the user runs `/octave:battlecard-doc`:

### Step 1: Identify Inputs

Parse the user's request for:
- **Account name** (required) -- the deal this card is for
- **Competitor(s)** (required) -- can be 1 or many
- **Context** (optional) -- call notes, deal stage, contacts

If the account and competitors are clear from the user's message or conversation context, proceed directly. Do NOT present a competitor picker, scope selector, or outline approval gate. The goal is zero ceremony -- just output the card.

The document adapts to competitor count and deal shape:
- **1 competitor** -- no tabs, render competitor section directly as a bordered panel
- **2-3 competitors** -- tabbed interface, one tab per competitor
- **4+ competitors** -- tabs still work; lead with primary threats, condense secondary ones
- **Status quo / incumbent** -- the buyer's current state (homegrown, legacy vendor, "doing nothing") is context in the Deal Situation section, NOT a competitor tab -- unless the buyer is genuinely undecided about moving or the incumbent is also being formally evaluated
- **Greenfield** -- no incumbent to replace; the "Current State" sub-card describes what they're doing without the capability and why that's no longer tenable

If truly ambiguous (no account or competitors identifiable), ask once:

```
Who's the account and which competitor(s) are you facing?
```

### Step 2: Octave Context Gathering

Use Octave MCP tools to build rich competitive context. **Always tell the user what you're researching and why.**

**Call as many tools as needed to build a complete picture.** The best battlecard documents come from layering multiple sources -- competitor profiles + deal outcomes + conversation evidence + proof points all combine to create a reference grounded in real data. Don't stop at one tool when three would give you a stronger document.

See [tool-reference.md](references/tool-reference.md) for the list-vs-search guidance and the tool reference tables for single-competitor and landscape modes.

**Do NOT present an outline for approval.** Proceed directly to generation.

### Step 3: Generate HTML

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

#### Deal Card -- Document Sections

See [single-competitor-sections.md](references/single-competitor-sections.md) for the deal card document section specs (handles 1-N competitors).

#### Landscape Overview -- Document Sections

See [landscape-sections.md](references/landscape-sections.md) for the landscape overview document section specs.

#### HTML Architecture

See [html-architecture.md](references/html-architecture.md) for the full HTML/CSS scaffold, landscape-mode component swaps, and key HTML/CSS principles.

**After writing the file, proceed immediately to Step 4 (Review Pipeline). Do NOT open the file in the browser or present the delivery summary yet.**

### Step 4: Review Pipeline — MANDATORY GATE

**Do NOT open the deal card in the browser, present the delivery summary, or tell the user it is ready until the review pipeline has completed and you have a scorecard.**

Load the [review protocol](../shared/protocol.md) and execute the review loop against the generated HTML file. Battlecard-specific wiring:

**4a: Mechanical lint** (before spawning reviewers):

```bash
bash <skill-dir>/scripts/lint.sh <path-to-battlecard.html>
```

Fix every violation the lint surfaces.

**4b: Spawn two reviewers in parallel** (both Task calls in a single message):

**Editorial reviewer:**
```
Task tool:
  subagent_type: "octave-editorial-reviewer"
  prompt: "Review the file at [FILE PATH].
           Read these principle docs and run each Review Checklist:
           1. [skill-dir]/../shared/editorial-rules.md
           2. [skill-dir]/../shared/information-principles.md
           Fix violations inline. Return scorecard."
```

**Presentation reviewer:**
```
Task tool:
  subagent_type: "octave-presentation-reviewer"
  prompt: "Review the file at [FILE PATH].
           Read these docs and run each Review Checklist:
           1. [skill-dir]/../shared/presentation-principles.md
           2. [skill-dir]/../shared/formats/html-document.md
           3. [skill-dir]/references/html-architecture.md
              (skill CSS/structure to reproduce)
           4. [skill-dir]/references/single-competitor-sections.md
              (skill's document section spec)
           Fix violations inline. Return scorecard."
```

**4c: Loop decision.** Read both scorecards:

| Cycle | 0 fixes | 1-2 fixes | 3+ fixes |
|---|---|---|---|
| Cycle 1 | CLEAN → 4d | Apply, loop | Apply, loop |
| Cycle 2 | CLEAN → 4d | Apply, STOP | Apply, loop |
| Cycle 3 (cap) | CLEAN → 4d | Apply, STOP | Apply, STOP |

Max 3 cycles. Re-run both reviewers each loop (back to 4b).

**4d: Output combined scorecard** to the user. This is proof the pipeline ran. Step 5 cannot start without it.

```
REVIEW PIPELINE COMPLETE
=========================
Editorial:      [N fixes / PASS]
Presentation:   [N fixes / PASS]

Total fixes: [N]
Cycles: [1-3]
Status: [CLEAN / N remaining issues]
```

### Step 5: Delivery

After the review pipeline scorecard has been output:

1. **Open the document** in the default browser
2. **Present a summary:**

```
DEAL CARD READY
================

Folder: .octave-decks/battlecard-<competitor>-<date>/
File:   .octave-decks/battlecard-<competitor>-<date>/battlecard-<competitor>.html
Size:   [file size]

Account: [Account name]
Competitors: [Competitor name(s)]
Sections: Deal Situation → [N] Competitor Panels → Our Pitch
Data sources: [N] deals, [N] conversation mentions, [N] proof points
Win rate: [X%] vs [Competitor] (last 180 days)

---

Want me to:
1. Go deeper on any section
2. Create displacement outreach for a specific person
3. Create a presentation version (/octave:deck)
4. Export as PDF
5. Done
```

**If user requests PDF export:**

```
To save as PDF:

PDF (recommended): bash "${CLAUDE_PLUGIN_ROOT:-.}"/scripts/export-pdf.sh .octave-decks/battlecard-<competitor>-<date>/battlecard-<competitor>.html
  — or use the manual print dialog below:

1. Open the file in your browser (should already be open)
2. Press Cmd+P (Mac) or Ctrl+P (Windows)
3. Select "Save as PDF" as the destination
4. Set margins to "Minimum" or "None" for best results
5. The sidebar navigation will be hidden in print
```

## MCP Tools Used

### Competitive Intelligence
- `list_entities` (competitor) -- List all competitors for selection or landscape
- `list_entities` (competitor) -- Full competitor profiles with data
- `get_entity` -- Deep dive on a specific competitor
- `search_knowledge_base` -- Competitive positioning, Motion ICP matching, proof point discovery
- `list_findings` -- Real conversation mentions, objections, competitor references from calls
- `list_events` -- Deal win/loss outcomes against specific competitors
- `get_event_detail` -- Deep dive into specific competitive deals for evidence

### Library (Fetching / Searching)
- `list_motions` -- List Motions in the workspace
- `list_motion_playbooks` -- Find Custom Motion Playbooks with narrative type COMPETITIVE
- `get_motion_playbook` -- Full details for a Custom Motion Playbook (competitive narrative)
- `list_motion_icps` -- Motion ICP cells (persona × segment) under a Motion
- `find_motion_icp` -- Motion ICP narrative + Learning Loop learnings
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
> 2. I'll generate a basic battlecard from available information (Motion ICPs, conversations, web research)

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The battlecard builder needs Octave data to generate competitive intelligence. Without it, I can't pull competitor profiles, deal outcomes, or conversation evidence.
>
> To reconnect: check your Octave MCP configuration and reconnect

**No Conversation Evidence:**
> No conversation mentions found for [Competitor].
>
> The objection handlers and trap questions will be based on library data and general competitive positioning rather than real conversation evidence. They'll improve as your team logs more calls where this competitor comes up.

## Related Skills

- `/octave:battlecard-doc` -- Text-based competitive intelligence (this is the visual version)
- `/octave:research` -- Account-focused dossier (when dealing with a specific account in a competitive deal)
- `/octave:deck` -- Competitive presentation for an audience (this is a reference doc)
- `/octave:win-loss-report` -- Text-based win/loss analysis across competitors
- `/octave:generate` -- Competitive displacement outreach content
- `/octave:research` -- Deep account research (feeds into account-specific competitive context)
- `/octave:insights` -- Surface competitive mentions from conversations
