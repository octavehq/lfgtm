---
name: win-loss-report
description: Generate visual win/loss analysis reports as self-contained HTML with CSS-based charts and data visualizations. Use when user says "win/loss report", "deal report", "visual analysis", or wants a formatted HTML version of deal outcome analysis. Do NOT use for text-based deal analysis — use /octave:win-loss-report instead.
---

# /octave:win-loss-report - Visual Win/Loss Report Builder

Generate beautiful, self-contained HTML win/loss analysis reports powered by your Octave deal intelligence. Unlike `/octave:win-loss-report` which outputs text-based analysis, this skill renders structured visual reports with CSS-based charts, progress indicators, comparison bars, and metric cards -- designed for leadership reviews, team retrospectives, and strategic planning.

Uses the same CSS variable / style preset system as `/octave:deck`.

## On-brand styling — brand kit first, then generate

**Resolve the brand before generating (do not skip this step).** The report brand should be the **workspace company's brand** — that is, the Octave customer whose workspace you are operating in.

**Step 1: Identify the workspace company.** Call `get_workspace_company` to get the company name, domain/URL, and positioning. This is the company whose brand the report should use (whatever get_workspace_company returns is the brand, not the target account).

**Step 2: Resolve the workspace company's brand kit.** Slugify the workspace company name and check for a cached brand kit at `~/.octave/brands/<slug>/manifest.json`. If a complete kit exists (has `manifest.json` and `tokens.css`), use it automatically:
   - inline the kit's `tokens.css` (`:root` + the embedded `@font-face`) **and** `get-brand-components/assets/kit_base.css` into the output `<style>`;
   - follow `brand-kit.md` → **Signature moves**, and reuse the kit's real **logo** for topbar and footer, `images/`, and `icons.json`.
   **If no complete kit exists → build one.** Run the `get-brand-components` skill (read `../../skills/get-brand-components/SKILL.md` and follow it) for the workspace company's domain. If the first attempt returns incomplete results (no logo, no colors, partial data) → retry up to 3 times with different approaches (root domain, `www.` prefix, `/about` subpage). Only fall back to a generic preset after 3 genuine failures.

**Step 3: Only use a generic preset as a last resort** — after the workspace company's brand kit cannot be built.

> **Strong default:** The report is always branded as the workspace company (the Octave customer). This is an internal report about deal outcomes — the workspace company's fonts, colors, topbar, and footer are used throughout.

## Usage

```
/octave:win-loss-report [--period <timeframe>] [--segment <filter>] [--competitor <name>] [--style <preset>]
```

## Examples

```
/octave:win-loss-report                                          # Last 90 days, all deals
/octave:win-loss-report --period "Q4 2025"                       # Specific quarter
/octave:win-loss-report --competitor "Gong"                      # Focused on deals vs Gong
/octave:win-loss-report --segment "enterprise"                   # Enterprise segment only
/octave:win-loss-report --period "last 6 months" --style paper-minimal
/octave:win-loss-report --period "2025" --competitor "Salesforce" --segment "mid-market"
```

## Instructions

When the user runs `/octave:win-loss-report`:

### Step 1: Define Scope

If not provided via flags, ask the user interactively:

**Period -- "What time range?"**

```
What time range should this report cover?

1. Last 30 days
2. Last 60 days
3. Last 90 days (default)
4. Last 6 months
5. Specific quarter (e.g., Q4 2025)
6. Custom date range

Your choice:
```

**Filter -- "Any specific focus?"**

```
Do you want to filter the analysis?

1. All deals -- full cross-deal analysis
2. Specific competitor -- focus on deals involving a competitor
3. Specific segment -- filter by market segment
4. Specific rep -- filter by sales rep
5. Custom filter -- describe what you want

Your choice:
```

If competitor or segment is selected, use `list_entities` to show available options:

```
# For competitor filter
list_entities({ entityType: "competitor" })

# For segment filter
list_entities({ entityType: "segment" })
```

**Depth -- "How detailed?"**

```
What level of detail?

1. Executive summary -- 1-page overview with key metrics and takeaways
2. Full report -- detailed analysis with all sections and drill-downs

Your choice:
```

| Depth | Sections Included | Best For |
|-------|-------------------|----------|
| Executive summary | Scorecard (headline metrics only), Win/Loss Analysis (top 3 each, no evidence), Data Sources | Board updates, weekly stand-ups |
| Full report | All 4 sections with full detail | QBRs, strategy sessions, enablement |

### Step 2: Octave Data Gathering

Based on scope, use Octave MCP tools to gather comprehensive deal intelligence. **Always tell the user what you're researching and why.**

**Call as many tools as needed to build a complete picture.** Win/loss reports are only as good as the data behind them. Layer multiple data sources -- deal outcomes + conversation findings + library context -- to produce analysis grounded in real evidence, not speculation.

See [tool-reference.md](references/tool-reference.md) for list-vs-search guidance and the tool reference tables for core deal data, conversation intelligence, library context, and competitor-focused data.

**Output of this step:** Present a report outline to the user for approval before generating. See [outline-template.md](references/outline-template.md) for the outline template.

**Wait for user approval before proceeding.**

### Step 3: Generate HTML

**Load the shared rules before writing any HTML. Read each before producing output:**
- [Editorial rules](../shared/editorial-rules.md) — universal language rules, AI-ism kill list, banned vocabulary
- [Presentation principles](../shared/presentation-principles.md) — universal visual rules, spacing, restraint
- [Information principles](../shared/information-principles.md) — content structure, narrative arc, evidence quality
- [HTML document format](../shared/formats/html-document.md) — format-specific visual rules for scrollable docs
- [Octave value](../shared/octave-value.md) — prioritize grounded workspace data over generic AI content

Apply these rules during generation, not just during review. The review pipeline catches what slips through — but the generation step should internalize them from the start.

Build a single, self-contained HTML file. **No external dependencies except Google Fonts.** Everything else inlined.

**After writing the file, proceed immediately to Step 4 (Review Pipeline). Do NOT open the file in the browser or present it to the user yet.**

#### Output Directory

Reports go under `.octave-reports/`:

```
.octave-reports/
└── win-loss-<YYYY-MM-DD>/
    └── win-loss-report.html
```

Example: `/octave:win-loss-report --period "Q4 2025"` produces `.octave-reports/win-loss-2026-02-11/win-loss-report.html`

The `.octave-reports/` directory is in `.gitignore` -- nothing here gets committed.

#### HTML Architecture

See [html-architecture.md](references/html-architecture.md) for the HTML architecture, structural requirements, and the CSS component system (metric cards, win rate ring, bar charts, use case cards, pattern cards, objection cards, head-to-head deal grids, tags, tab system).

#### Report Sections (Full Report)

See [sections.md](references/sections.md) for the full 4-section report breakdown and the condensed executive summary variant.

**Key structural principles:**
- Every metric shows BOTH volume and rate with explicit axis labels
- Segments, personas, use cases, and competitors are attributed on every card — not floating as abstract statistics
- Section 2 (Win/Loss Analysis) is a tabbed pair: Win Analysis ←→ Loss Analysis
- Section 3 (Head-to-Head Deals) is tabbed by dimension: By Competitor | By Segment | By Persona
- Objections live inside the Loss tab (sorted by loss correlation, not frequency)
- Actionable changes live inside the Loss tab as "What to Stop Doing / Changes to Make," with an optional one-line "Winnable if: [X]" callout per pattern where the evidence points to a clean turning point
- "No Decision / Stalled" is an optional loss pattern category, included only if the workspace's loss data actually distinguishes no-decision from competitor losses, never fabricated

### Step 4: Review Pipeline — MANDATORY GATE

**Do NOT open the report in the browser, present the delivery summary, or tell the user the report is ready until the review pipeline has completed and you have a scorecard.**

Load the [review protocol](../shared/protocol.md) and execute the review loop against the generated HTML file. The protocol specifies the full process, but here is the win-loss-report-specific wiring:

**4a: Mechanical lint** (before spawning reviewers):

```bash
bash <skill-dir>/scripts/lint.sh <path-to-report.html>
```

Fix every violation the lint surfaces. Deterministic checks: em-dashes, Tier 1 banned words, banned phrases, text density, leaked internals.

**4b: Spawn two reviewers in parallel** (both Task calls in a single message):

**Editorial reviewer:**
```
Task tool:
  subagent_type: "octave-editorial-reviewer"
  prompt: "Review the file at [FILE PATH].
           Read these principle docs and run each Review Checklist:
           1. [skill-dir]/../shared/editorial-rules.md (language quality)
           2. [skill-dir]/../shared/information-principles.md (information structure)
           Fix violations inline. Return scorecard."
```

**Presentation reviewer:**
```
Task tool:
  subagent_type: "octave-presentation-reviewer"
  prompt: "Review the file at [FILE PATH].
           Read these principle docs and run each Review Checklist:
           1. [skill-dir]/../shared/presentation-principles.md (universal visual rules)
           2. [skill-dir]/../shared/formats/html-document.md (format-specific visual rules)
           3. [skill-dir]/references/html-architecture.md (skill-specific CSS)
           4. [skill-dir]/references/sections.md (skill-specific structure)
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
Editorial:
  Mechanical:     [N fixes / PASS]
  Structural:     [N fixes / PASS]
  Quality:        [N fixes / PASS]
  Information:    [N fixes / PASS]

Presentation:
  Visual Rules:   [N fixes / PASS]
  Format Rules:   [N fixes / PASS]
  Design System:  [N fixes / PASS]
  Structure:      [N fixes / PASS]

Total fixes: [N]
Cycles: [1-3]
Status: [CLEAN / N remaining issues]
```

### Step 5: Delivery

After the review pipeline scorecard has been output:

1. **Open the report** in the default browser
2. **Present a summary:**

```
REPORT READY
=============

File:    .octave-reports/win-loss-<date>/win-loss-report.html
Period:  [Date range]
Deals:   [N] won, [N] lost ([N]% win rate across [N] closed deals)
Style:   [Brand kit name]
Depth:   [Executive Summary / Full Report]

Key Findings:
- Win rate: [N]% ([N] of [N] closed deals)
- Top win use case: [Use case] ([N]% win rate across [N] deals)
- Top loss use case: [Use case] ([N]% loss rate across [N] deals)
- Highest-risk objection: [Objection] ([N]% loss rate when raised)
- Biggest competitor threat: [Competitor] ([N] deals, [N]% win rate)

Sections:
- Scorecard: metrics + segment/persona/competitor breakdowns
- Win/Loss Analysis: tabbed use cases, patterns, objections
- Head-to-Head Deals: tabbed by competitor/segment/persona
- Data Sources

Navigation:
- Scroll to navigate between sections
- Sidebar dots show your position
- Tabs switch between Win/Loss analysis and Head-to-Head dimensions
- PDF: Cmd+P / Ctrl+P -> Save as PDF (tabs flatten to labeled blocks)

---

Want me to:
1. Drill into a specific competitor
2. Drill into a specific segment
3. Add more detail to any section
4. Generate an executive summary version (or full version)
5. Export as PDF
6. Done
```

## MCP Tools Used

### Deal Intelligence
- `list_events` - Filter by DEAL_WON, DEAL_LOST, OPPORTUNITY_CREATED for deal outcomes and pipeline
- `get_event_detail` - Deep dive on notable wins and losses for deal stories

### Conversation Intelligence
- `list_findings` - Objections, value prop presentations, competitor mentions, feature requests, proof points cited in calls

### Library Context
- `list_entities` - Quick inventory of competitors, segments, personas
- `list_entities` - Full entity data for proof points, references
- `get_entity` - Deep dive on specific competitors, personas
- `list_motions` - List Motions in the workspace
- `list_motion_icps` - List Motion ICP cells (persona × segment) under a Motion
- `find_motion_icp` - Motion ICP narrative + Learning Loop learnings
- `search_knowledge_base` - Semantic search for positioning content
- `search_resources` - Uploaded CRM exports, deal data files

## Error Handling

**No Deal Data in Period:**
> No won or lost deals found for [period].
>
> This could mean:
> 1. CRM integration isn't syncing deal outcomes
> 2. The date range has no closed deals
> 3. Filters are too restrictive
>
> Try:
> 1. Expand the date range
> 2. Remove filters (competitor, segment)
> 3. Check your Octave CRM integration settings

**Insufficient Data (Fewer Than 5 Deals):**
> Only [N] deals found for [period]. Win/loss analysis is most useful with 5+ deals.
>
> Options:
> 1. Proceed anyway -- I'll generate the report with available data (patterns may be unreliable)
> 2. Expand the time period to capture more deals
> 3. Remove filters to include all segments/competitors

**No Findings Data:**
> Deal outcomes found, but no conversation findings available.
>
> The report will include deal metrics and outcomes but won't have:
> - Evidence quotes from calls
> - Objection analysis
> - Value prop effectiveness
>
> For richer analysis, ensure calls are being recorded and findings extraction is enabled in Octave.

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The win/loss report requires deal data from Octave. Check your Octave MCP configuration and reconnect.

**Missing Competitor/Segment Data:**
> I couldn't find a competitor named "[name]" in your library.
>
> Available competitors:
> - [List from list_entities]
>
> Pick one from the list, or proceed with "all deals" and I'll break down by competitor automatically.

## Related Skills

- `/octave:win-loss-report` - Text-based win/loss analysis (this is the visual version)
- `/octave:insights` - Conversation intelligence analysis (conversational format)
- `/octave:battlecard-doc` - Competitive deep-dive (when patterns point to a specific competitor)
- `/octave:pipeline` - Current pipeline coaching and deal strategy
- `/octave:deck` - Present win/loss findings to leadership as a slide deck
