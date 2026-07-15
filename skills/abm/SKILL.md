---
name: abm
description: Account-based planning with stakeholder mapping, persona matching, and coordinated outreach strategy. Use when user says "plan for [company]", "account plan", "stakeholder map", "ABM strategy", or mentions targeting a specific named company.
---

# /octave:abm - Account Planner

Create account plans for target accounts by combining deep research, stakeholder mapping, persona matching, and an engagement sequence — all grounded in your library's Motion ICP cells and proof points. Output is a self-contained HTML account plan.

**What this skill is.** The unit of `/octave:abm` is the **account**. It produces a tight, account-level plan a rep acts on, structured as six jobs: (1) is this account worth it and why now, (2) what's likely driving them / what to explore, (3) who to engage (buying committee), (4) how to position per persona, (5) the engagement plan, (6) what could go wrong. It DOES advise — per-persona positioning and an entry-point engagement plan are the point — but at the **account** level. The distinction from `/octave:meeting-prep` is scope: meeting-prep coaches one scheduled meeting (talk tracks, discovery, room game-plan); abm plans the whole account pursuit across the committee. Single-asset copy still lives in `/octave:generate`.

**Groundedness is non-negotiable.** Every named person, title, employer, and LinkedIn URL in the buying committee must come from a real `find_person`/`enrich_person` result. Never synthesize a person or a LinkedIn slug. Honest gaps beat plausible inventions. A prior run shipped a fabricated committee — do not repeat it.

## Principles

Follow these standards during generation. Read each before producing output.

**Content and language:**
- [Editorial rules](../shared/editorial-rules.md) — no AI-isms, banned vocabulary, honest analyst tone
- [Information principles](../shared/information-principles.md) — lead with conclusions, evidence-backed claims, narrative arc

**Presentation:**
- [Presentation principles](../shared/presentation-principles.md) — universal visual rules, spacing, restraint
- [HTML document format](../shared/formats/html-document.md) — scrollable-document visual rules

**Octave data:**
- [Octave value](../shared/octave-value.md) — prioritize grounded workspace data over generic AI content

## Usage

```
/octave:abm <company> [--stakeholders <N>] [--motion <name>] [--depth quick|full]
```

## Examples

```
/octave:abm acme.com                                      # Full account plan
/octave:abm acme.com --stakeholders 5                     # Map top 5 stakeholders
/octave:abm acme.com --motion "Enterprise Expansion"      # Scope to a specific Motion's ICP matrix
/octave:abm acme.com --depth quick                        # Quick assessment only
/octave:abm "Acme Corp"                                   # Search by company name
```

## Instructions

When the user runs `/octave:abm`:

### Step 1: Identify Target Account

Parse input:
- Domain (e.g., `acme.com`) → Use directly
- Company name → Search for domain
- LinkedIn URL → Extract domain

If company name provided without domain:
```
find_company({ name: "<company_name>" })
```

### Step 2: Deep Account Research

```
# Full company enrichment
enrich_company({ companyDomain: "<domain>" })

# Qualify against ICP
qualify_company({
  companyDomain: "<domain>",
  additionalContext: "Evaluate fit against all segments. Identify which segment, use cases, and Motion ICP cells are most relevant."
})
```

### Step 3: Stakeholder Mapping (buying committee) — GROUNDEDNESS-CRITICAL

Build the committee **persona by persona**. For each relevant persona type in the library, use `find_person` to surface **1-2 strong-match real people** — strong match only, real only. Do not pad to a headcount, and do not invent anyone: if a persona returns no strong match, leave that role as an honest gap.

```
# Persona types to search against
list_entities({ entityType: "persona" })

# For EACH relevant persona, find 1-2 strong matches at the account
find_person({
  searchMode: "people",
  companyDomain: "<domain>",
  fuzzyTitles: ["<titles for persona 1>"],
  limit: 3   // pick the 1-2 strongest from the results; do not list all
})
# Repeat per persona type (champion, economic buyer, evaluator, gatekeeper coverage)
```

**Hard rule:** the buying committee may only contain people `find_person`/`enrich_person` actually returned, with the LinkedIn URLs those tools returned. Never write a name, title, employer, or LinkedIn slug the tools did not give you. Tag anyone you could not confirm with `.unconfirmed`. Name empty roles as gaps ("no economic buyer identified yet").

For each key stakeholder found:
```
# Enrich top stakeholders
enrich_person({
  person: {
    firstName: "<first>",
    lastName: "<last>",
    companyDomain: "<domain>"
  }
})

# Qualify against personas
qualify_person({
  person: {
    firstName: "<first>",
    lastName: "<last>",
    companyDomain: "<domain>",
    jobTitle: "<title>"
  },
  additionalContext: "Match to our buyer personas. Identify their likely role in a buying decision (champion, evaluator, economic buyer, blocker)."
})
```

### Step 4: Match Motion ICP Cell and Gather Intelligence

```
# Find the right Motion for this account (offering + motion type)
list_motions()

# See the persona × segment matrix for the matched Motion
list_motion_icps({ motionOId: "<motion_oId>" })

# Fetch the narrative for the target persona × segment cell
find_motion_icp({ motionIcpOId: "<motion_icp_oId>", includeLearnings: true })

# Find relevant proof points (industry, size match) — one per persona for Section 5
search_knowledge_base({
  query: "<company industry> <company size> results case study",
  entityTypes: ["proof_point", "reference"]
})

# Buying triggers for Section 3: use REAL library triggers if they match; otherwise
# frame pains as "likely / to explore" grounded in the motion cell — do not manufacture certainty
list_entities({ entityType: "buying_trigger" })

# Real engagement history for Section 6 (fold in if present; IGNORE dummy/seed pipeline values)
find_crm_activities({ entityType: "account", recordId: "<crm_account_id>" })   // if a real CRM account resolves
generate_crm_context({ companyDomain: "<domain>", objective: "account plan engagement history" })

# Check for competitive context
search_knowledge_base({
  query: "<company name> <any tech stack signals>",
  entityTypes: ["competitor"]
})

# Check for any existing conversation history
list_events({
  startDate: "<365 days ago>",
  filters: {
    companyDomains: ["<domain>"]
  }
})
```

### Step 5: Resolve the Brand Kit

**Resolve the brand before generating (do not skip this step).** The document brand should be the **workspace company's brand** — that is, the Octave customer whose workspace you are operating in. The target account's logo appears in the masthead, but the document chrome (fonts, colors, header, footer) is workspace-company branded.

**5a: Identify the workspace company.** Call `get_workspace_company` to get the company name, domain/URL, and positioning.

**5b: Resolve the workspace company's brand kit.** Slugify the workspace company name and check for a cached brand kit at `~/.octave/brands/<slug>/manifest.json`. If a complete kit exists (has `manifest.json` and `tokens.css`), use it automatically:
   - inline the kit's `tokens.css` (`:root` + embedded `@font-face`) **and** `../get-brand-components/assets/kit_base.css` into the output `<style>`;
   - follow the kit's `brand-kit.md` → **Signature moves**; reuse the kit's real **logo** for header and footer, `images/`, and `icons.json`.
   **If no complete kit exists → build one.** Run the `get-brand-components` skill (read its SKILL.md and follow it) for the workspace company's domain. If the first attempt returns incomplete results, retry up to 3 times with different approaches (root domain, `www.` prefix, `/about` subpage). Only fall back to a clean default style after 3 genuine failures.

**5c: Generic default is a last resort** — only after the workspace company's brand kit cannot be built.

### Step 6: Generate the Account Plan HTML

**Load the shared rules and the document spec. Read each before producing output:**
- [Editorial rules](../shared/editorial-rules.md) — universal language rules, AI-ism kill list, banned vocabulary
- [Information principles](../shared/information-principles.md) — lead with conclusions, evidence-backed claims, no interpretation padding (#7b applies hard here: information, not instructions)
- [Presentation principles](../shared/presentation-principles.md) — universal visual rules, spacing, restraint
- [HTML document format](../shared/formats/html-document.md) — scrollable-document visual rules
- [Octave value](../shared/octave-value.md) — grounded workspace data over generic AI content
- [Account plan structure](references/account-plan-template.md) — the six jobs, per-section specs, density rules, groundedness rule
- [HTML scaffold](references/html-scaffold.md) — the locked CSS + section skeleton + persona-selector JS; reproduce this structure and card vocabulary
- [Regression checklist](references/regression-checklist.md) — issues found during testing, verified against every new generation

Build a single, self-contained HTML file. No external dependencies beyond Google Fonts.

**After writing the file, proceed immediately to Step 7 (Review Pipeline). Do NOT open the file in the browser or present it to the user yet.**

#### Output Directory

```
.octave-abm/
└── <company-slug>-<YYYY-MM-DD>/
    └── account-plan.html
```

Write to the user's home directory (`~/.octave-abm/...`), not the skill or tuning folder.

### Step 7: Review Pipeline — MANDATORY GATE

**Do NOT open the plan in the browser, present the delivery summary, or tell the user the plan is ready until the review pipeline has completed and you have a scorecard.**

Load the [review protocol](../shared/protocol.md) and execute the review loop against the generated HTML file. The protocol specifies the full process; here is the ABM-specific wiring:

**7a: Mechanical lint** (before spawning reviewers):

```bash
bash <skill-dir>/scripts/lint.sh <path-to-account-plan.html>
```

Fix every violation the lint surfaces.

**7b: Spawn two reviewers in parallel** (both Task calls in a single message):

**Editorial reviewer:**
```
Task tool:
  subagent_type: "octave-editorial-reviewer"
  prompt: "Review the file at [FILE PATH].
           Read these principle docs and run each Review Checklist:
           1. [skill-dir]/../shared/editorial-rules.md
           2. [skill-dir]/../shared/information-principles.md
           3. [skill-dir]/references/regression-checklist.md
              (Lean Intelligence section)
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
           3. [skill-dir]/references/account-plan-template.md
           4. [skill-dir]/references/html-scaffold.md
              (structure + card vocabulary to reproduce)
           5. [skill-dir]/references/regression-checklist.md
              (Structure, Tightness, and Section 7 checks)
           Fix violations inline. Return scorecard."
```

**7c: Loop decision.** Read both scorecards:

| Cycle | 0 fixes | 1-2 fixes | 3+ fixes |
|---|---|---|---|
| Cycle 1 | CLEAN → 7d | Apply, loop | Apply, loop |
| Cycle 2 | CLEAN → 7d | Apply, STOP | Apply, loop |
| Cycle 3 (cap) | CLEAN → 7d | Apply, STOP | Apply, STOP |

Max 3 cycles. Re-run both reviewers each loop (back to 7b).

**7d: Output combined scorecard** to the user. This is proof the pipeline ran. Step 8 cannot start without it.

```
REVIEW PIPELINE COMPLETE
=========================
Editorial:      [N fixes / PASS]
Presentation:   [N fixes / PASS]

Total fixes: [N]
Cycles: [1-3]
Status: [CLEAN / N remaining issues]
```

### Step 8: Deliver

After the review pipeline scorecard has been output:

1. **Open the plan** in the default browser.
2. **Present a summary:** file path, ICP score, stakeholders mapped (and missing roles), playbook matched, deal history found (Y/N), entry point.

### Step 9: Sample outreach for the engagement plan (Section 6)

Generate the one or two sample emails that appear in the engagement plan (Section 6), for the entry-point persona. These are part of the document, not a post-delivery add-on — real and specific, grounded in the account's pains and the positioning from Section 5.
```
generate_email({
  person: {
    firstName: "<first>",
    lastName: "<last>",
    companyDomain: "<domain>",
    jobTitle: "<title>"
  },
  numEmails: 4,
  sequenceType: "COLD_OUTBOUND",
  allEmailsContext: "Account plan context: [company signals, persona match, Motion ICP narrative, proof points]",
  allEmailsInstructions: "Personalized to [company] specifically. Reference [relevant signals]. Use [proof points] progressively."
})
```

## MCP Tools Used

### Research
- `enrich_company` - Deep company intelligence
- `enrich_person` - Stakeholder background
- `qualify_company` - ICP fit scoring
- `qualify_person` - Persona matching
- `find_person` - Stakeholder discovery
- `find_company` - Company lookup by name

### Library Context
- `list_entities` (persona) - Get persona definitions for stakeholder matching
- `list_motions` - List all Motions in the workspace
- `list_motion_icps` - List Motion ICP cells (persona × segment intersections) for a Motion
- `find_motion_icp` - Full Motion ICP cell narrative (Target ICP overview, Operating landscape, Strategic narrative, Pains and consequences, Benefits and impacts, Methodology, References) plus Learning Loop learnings
- `search_knowledge_base` - Proof points, references, competitive intel
- `list_events` - Existing conversation history with account
- `get_workspace_company` - Workspace company identity for brand resolution

### Content Generation
- `generate_email` - Outreach sequences
- `generate_content` - Account-specific content
- `generate_call_prep` - Meeting preparation

## Error Handling

**Company Not Found:**
> Couldn't find "[input]".
>
> Try:
> 1. Provide the company's website domain (e.g., acme.com)
> 2. Check spelling
> 3. Search by name: I'll look it up

**No Stakeholders Found:**
> No contacts found at [Company] matching your personas.
>
> Options:
> 1. Broaden the search (search all titles, not just persona matches)
> 2. Search for specific titles you know
> 3. Proceed with company-level plan only

**Low ICP Score:**
> [Company] scored [X/100] against your ICP.
>
> This is below typical qualification thresholds.
> Continue anyway? Or:
> 1. Find similar companies with better fit
> 2. See why the score is low and if any signals are missing
> 3. Proceed with adjusted expectations

## Related Skills

- `/octave:meeting-prep` - Coached prep for a scheduled meeting (talk tracks, objection handling — the layer this skill deliberately omits)
- `/octave:research` - Deep-dive on a specific stakeholder
- `/octave:ads` - Ad campaign targeting this account
- `/octave:battlecard-doc` - Competitive intel if competitor detected
- `/octave:pipeline` - Coach on deal progression after engagement starts
- `/octave:prospector` - Find more accounts like this one
