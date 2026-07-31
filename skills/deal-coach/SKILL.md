---
name: deal-coach
description: "Per-deal coaching plan built around the Resonate → Elevate → Compel methodology, rendered as a self-contained HTML coaching microsite grounded in your Octave library. Use when user says 'deal coach', 'coach this deal', 'coaching plan', 'coaching microsite', 'how do I advance this deal', 'what stage is this deal', or asks to be coached on a specific opportunity. Do NOT use for live-deal next-step strategy (use /octave:pipeline) or generic role-play/quiz practice (use /octave:train)."
argument-hint: "[domain|email] [--stage resonate|elevate|compel]"
---

# /octave:deal-coach — Per-Deal Coaching Microsite

Generate a coaching plan for a specific deal, rendered as a scrollable, self-contained HTML **coaching microsite** and grounded in your Octave GTM intelligence. This is the doc a rep opens before their next call, or a manager hands a rep to coach the deal forward.

The methodology is **Resonate → Elevate → Compel**:

| Stage | Objective |
|-------|-----------|
| **Resonate** | Drive awareness — get the buyer to agree the problem is real and worth solving |
| **Elevate** | Drive urgency — disrupt the status quo, differentiate on value |
| **Compel** | Drive action — build the business case, enable the champion |

The output is built around **six jobs**, not a kitchen-sink of sections: (1) where this deal stands, (2) where the buyer's head is, (3) what to do now, (4) the path to close, (5) top risks, (6) practice and what good looks like. The full spec — job order, density caps, groundedness rules, and the review checklist — lives in [coaching-microsite-sections.md](references/coaching-microsite-sections.md). The CSS and HTML skeleton live in [html-scaffold.md](references/html-scaffold.md).

**The crown-jewel move:** `find_motion_icp({ ..., includeLearnings: true })` returns a `salesMethodology` block for the matched persona × segment cell, with Resonate / Elevate / Compel stages, each carrying **Buyer Mindset**, **Value Propositions**, and **Talking Points**. That maps almost 1:1 onto the coaching jobs. This is what makes the plan read as "only Octave could write this," not a generic methodology handout.

**How this differs from neighboring skills:**
- `/octave:pipeline` gives live-deal next-step strategy (rescue a stalled deal, multi-thread). This produces a coaching plan organized around the methodology stages.
- `/octave:train` is generic practice (role-play, quiz) on your GTM. This is deal-specific and stage-structured.
- `/octave:meeting-prep` is a battle plan for one upcoming meeting. This coaches the whole stage of the deal.

## On-brand styling — brand kit first, then generate

**Resolve the brand before generating (do not skip this step).** The coaching microsite is an **internal** asset, styled in the **workspace company's brand** (the Octave customer whose workspace you are operating in). The target account is named in the content, never in the design system.

**Step 1: Identify the workspace company.** Call `get_workspace_company` for the company name, domain/URL, and positioning.

**Step 2: Resolve the workspace company's brand kit.** Slugify the workspace company name and check for a cached kit at `~/.octave/brands/<slug>/manifest.json`. If a complete kit exists (has `manifest.json` and `tokens.css`), use it automatically:
   - inline the kit's `tokens.css` (`:root` + the embedded `@font-face`) **and** `../get-brand-components/assets/kit_base.css` into the output `<style>`;
   - follow the kit's `brand-kit.md` → **Signature moves**; embed the kit's real **logo** as a data URI in the hero. **Before embedding a logo, open it and confirm it is actually the workspace company's mark** — cached kits can carry a mislabeled or contaminated asset. If a logo file looks wrong or ambiguous, verify it (a white wordmark on a transparent PNG reads blank on a white background; composite it on a dark background to inspect), and fall back to the kit's text `wordmark` in the display font rather than ship the wrong logo. Embed the brand-defining display font as a data URI (commercial fonts are not on Google Fonts); Inter / mono fallbacks may load from Google Fonts.
   **If no complete kit exists → build one.** Run the `get-brand-components` skill for the workspace company's domain. Retry up to 3 times (root domain, `www.`, `/about`). Only fall back to a generic preset after 3 genuine failures.

**Step 3: Generic preset is a last resort** — only after the brand kit genuinely cannot be built.

## Principles

Follow these standards during generation. Read each before producing output.

**Content and language:**
- [Editorial rules](../shared/editorial-rules.md) — no AI-isms, banned vocabulary, honest analyst tone, no em/en-dashes, conclusion-carrying (not theatrical) headers
- [Information principles](../shared/information-principles.md) — lead with conclusions, evidence-backed claims, narrative arc

**Visual design:**
- [Presentation principles](../shared/presentation-principles.md) — typography, layout, visual restraint
- [HTML document format](../shared/formats/html-document.md) — scrollable internal-document specifics

**Octave data:**
- [Octave value](../shared/octave-value.md) — prioritize grounded workspace data over generic AI content

**Mandatory review:** Every generated microsite goes through the review pipeline (Step 5) before delivery. This is a gate, not an offer — see [review protocol](../shared/protocol.md).

## Usage

```
/octave:deal-coach <domain|email> [--stage resonate|elevate|compel]
```

## Examples

```
/octave:deal-coach acme.com                          # Coach the Acme deal, stage inferred
/octave:deal-coach jane@acme.com                     # Resolve the account from a contact
/octave:deal-coach acme.com --stage elevate          # Force the current stage
/octave:deal-coach "the DataCorp expansion"          # Context-based
```

## Instructions

Follow these steps in order. Do not skip or reorder them.

### Step 1: Identify the Deal

If the user provided a domain, name, or email, use it. Otherwise ask which account to coach (domain or contact email). This skill is deal-specific; for methodology practice with no account, point the user to `/octave:train`.

### Step 2: Octave Context Gathering

Build a complete picture of the deal and the methodology content. **Tell the user what you are researching and why.** Run independent calls in parallel.

**Account and conversation context:**
- `enrich_company({ companyDomain })` — profile, industry, tech stack, strategic context
- `find_crm_records` / `find_crm_activities` / `generate_crm_context` — deal stage, activities, synthesized narrative (may be absent; see below)
- `list_findings({ eventFilters: { companyDomains: [domain] } })` — objections, pain points, competitor mentions, agreements, all traced to real calls
- `list_events({ filters: { companyDomains: [domain] } })` — call history, stage changes
- `get_event_detail({ eventOId })` — deep dive on a specific call to pull exact, verbatim buyer language
- `search_call_transcripts({ companyDomain, query: "<topic>" })` — find the buyer's exact words across every call with this account without already knowing which event to open; returns `recordingUrl` + `startSec` so the plan can cite "jump to 14:20" instead of a paraphrase
- `get_entity_evidence({ entityOId })` — best verbatim quotes for the matched persona's pain point or a competitor named on the calls, to ground Job 3's talking points in the buyer's own language

**Buyer and library context (parallel):**
- `find_person` / `enrich_person` — confirm the real buyer(s); never synthesize a name, title, or LinkedIn slug
- `list_entities({ entityType: "competitor" })` — resolve competitors named on the calls to real library entities

**Motion ICP — the crown jewel:**
```
list_motions()
list_motion_icps({ motionOId })                              # find the persona × segment cell
find_motion_icp({ motionIcpOId, includeLearnings: true })   # returns the salesMethodology R/E/C block
```
Match the cell to the real buyer's persona and the account's segment. The returned `salesMethodology` array is the spine of the coaching content: each stage's Buyer Mindset feeds Job 2, its Value Propositions and Talking Points feed Job 3, and Elevate/Compel feed Job 4.

**Groundedness is a hard bar.** Every named person, title, prior employer, LinkedIn URL, competitor, quote, and count must trace to a real tool result, not a plausible synthesis. Do not assert a call count you have not verified. If deal data is missing, say so and use a placeholder (see Job 1) rather than invent a stage, amount, or date. Honest gaps beat inventions. Tag anything unconfirmed with `.unconfirmed`.

**Data-caveat awareness:** some workspaces carry seeded CRM/pipeline data (provider "generic", `seed-*` IDs). Never render seeded pipeline numbers as real. Infer the stage from the calls and hand the deal-record fields back to the seller via the Job 1 placeholder.

Load the methodology references: [frameworks.md](references/frameworks.md), [stage-mapping.md](references/stage-mapping.md), [messaging-narratives.md](references/messaging-narratives.md), and [coaching-agents.md](references/coaching-agents.md) (for buyer psychology and the Job 6 rubric).

**Infer the coaching stage.** If the user passed `--stage`, use it. Otherwise infer with the weighted algorithm in [stage-mapping.md](references/stage-mapping.md) (CRM stage, findings, activities, time in stage). CRM absence is a data-hygiene issue, not a deal signal — redistribute its weight. Present the inferred stage and evidence to the user briefly; proceed unless they override.

### Step 3: Resolve the Brand

Follow the "On-brand styling" section above: `get_workspace_company` → cached kit at `~/.octave/brands/<slug>/` → build via `get-brand-components` (retry up to 3) → preset fallback. Confirm the logo asset is genuinely the workspace company's before embedding it.

### Step 4: Generate HTML

**Load the shared rules before writing any HTML. Read each before producing output:**
- [Editorial rules](../shared/editorial-rules.md)
- [Information principles](../shared/information-principles.md)
- [Presentation principles](../shared/presentation-principles.md)
- [HTML document format](../shared/formats/html-document.md)
- [Octave value](../shared/octave-value.md)

Apply these rules during generation, not just during review.

Build the microsite to the spec in [coaching-microsite-sections.md](references/coaching-microsite-sections.md) (the six jobs, their order, density caps, and groundedness rules) using the CSS and skeleton in [html-scaffold.md](references/html-scaffold.md). Build a single, self-contained HTML file. **No external dependencies** except Google Fonts (plus data-URI-embedded brand font and logo).

**After writing the file, proceed immediately to Step 5. Do NOT open the file or present it yet.**

#### Output Directory

Write to `.octave-deal-coach/` in the user's **home directory** (`~/.octave-deal-coach/`, not the skill or project folder):

```
.octave-deal-coach/
└── <company-kebab>-<stage>-<YYYY-MM-DD>/
    └── <company-kebab>-coaching.html
```

The entire `.octave-deal-coach/` directory is in `.gitignore`.

### Step 5: Review Pipeline — MANDATORY GATE

**Do NOT open the microsite, present the delivery summary, or tell the user it is ready until the review pipeline has completed and you have a scorecard.**

Load the [review protocol](../shared/protocol.md) and execute the review loop against the generated HTML file.

**5a: Mechanical lint** (before spawning reviewers):
```bash
bash <skill-dir>/../shared/scripts/lint.sh <path-to-coaching.html>
```
Fix every violation. The em/en-dash check is a hard gate.

**5b: Spawn two reviewers in parallel** (both Task calls in a single message).

**Editorial reviewer:**
```
Task tool:
  subagent_type: "octave-editorial-reviewer"
Prompt:
Review the file at [FILE PATH]. Read these principle docs and run each Review Checklist:
  1. [skill-dir]/../shared/editorial-rules.md
  2. [skill-dir]/../shared/information-principles.md
  3. [skill-dir]/../shared/octave-value.md (Data Grounding — verify every named
     person, quote, competitor, and count against the real tool results; flag, do not
     invent, anything that reads as synthesized)
Context: this is an INTERNAL coaching plan, so conclusion-carrying plain-English headers
are correct, but reject theatrical / clickbait framing. HARD RULE: no em/en-dashes; if you
edit copy, never introduce one. Fix violations inline. Return a scorecard.
```

**Presentation reviewer:**
```
Task tool:
  subagent_type: "octave-presentation-reviewer"
Prompt:
Review the file at [FILE PATH]. Read these docs and run each Review Checklist:
  1. [skill-dir]/../shared/presentation-principles.md
  2. [skill-dir]/../shared/formats/html-document.md
  3. [skill-dir]/references/html-scaffold.md
  4. [skill-dir]/references/coaching-microsite-sections.md
Verify responsive behavior at 375px (no horizontal overflow), print styles, keyboard focus,
token-based colors, and that any CSS-grid list item wrapping inline <em> keeps it inline
(wrap item text in a <span>). Fix violations inline. Return a scorecard.
```

**5c: Loop decision.** Max 3 cycles. Re-run both reviewers each loop.

| Cycle | 0 fixes | 1-2 fixes | 3+ fixes |
|---|---|---|---|
| Cycle 1 | CLEAN → 5d | Apply, loop | Apply, loop |
| Cycle 2 | CLEAN → 5d | Apply, STOP | Apply, loop |
| Cycle 3 (cap) | CLEAN → 5d | Apply, STOP | Apply, STOP |

**5d: Output the combined scorecard** to the user. This is proof the pipeline ran. Step 6 cannot start without it.

```
REVIEW PIPELINE COMPLETE
=========================
Mechanical lint: [PASS / N fixed]
Editorial:       [N fixes / PASS]
Presentation:    [N fixes / PASS]
Total fixes: [N]   Cycles: [1-3]   Status: [CLEAN / N remaining]
```

### Step 6: Delivery

After the scorecard is output:

1. **Open the microsite** in the default browser (serve the output folder over `http://127.0.0.1:<port>` so embedded fonts and the logo load; opening the `file://` path also works).
2. **Present a short summary:**

```
COACHING MICROSITE READY
========================
File:     [path]
Account:  [Company]  ·  Buyer: [Name, Title]
Stage:    [Resonate / Elevate / Compel] — [objective]
Cell:     [Persona] × [Segment]

Next: 1) practice this stage with /octave:train  2) prep the next meeting with
/octave:meeting-prep  3) live-deal strategy with /octave:pipeline
```

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `get_workspace_company` | Workspace company identity for brand resolution |
| `enrich_company` | Company profile, industry, tech stack |
| `find_crm_records` / `find_crm_activities` / `generate_crm_context` | Deal stage, activities, narrative |
| `find_person` / `enrich_person` | Confirm the real buyer(s) — groundedness |
| `list_findings` | Objections, pains, competitor mentions, agreements from real calls |
| `list_events` / `get_event_detail` | Call history and verbatim call language |
| `search_call_transcripts` | Find the buyer's exact words across all calls with this account, with recording links + timestamps |
| `get_entity_evidence` | Best verbatim quotes evidencing the matched persona's pain or a named competitor |
| `list_motions` / `list_motion_icps` / `find_motion_icp` | The Motion ICP cell + `salesMethodology` R/E/C block (crown jewel) |
| `list_entities` / `get_entity` | Competitors, proof points, personas |
| `search_knowledge_base` | Semantic search across library and resources |

## Error Handling

> **No CRM / deal record:** Infer the stage from calls and findings; render the Job 1 deal-data placeholder rather than invent a stage, amount, or date.

> **No Motion ICP cell:** Coach from the general framework in `frameworks.md` and note the limitation. The talk tracks will lack the cell's specific Value Propositions and Talking Points. Suggest creating a Motion for this offering.

> **No findings / events:** Stage inference relies on CRM stage; note that thinner call data means thinner coaching.

> **Reference file missing:** Fall back to general coaching methodology and note it.

> **MCP connection failed:** This skill requires Octave MCP tools. Ask the user to check their Octave MCP configuration and reconnect.

## Related Skills

- `/octave:pipeline` — Live-deal strategy: stalled-deal rescue, multi-threading, closing
- `/octave:next-best-action` — Recurring strategy-gap next actions with a watchlist and scheduled sweeps
- `/octave:train` — Generic role-play and quiz practice on your GTM
- `/octave:meeting-prep` — Battle plan for one upcoming meeting
- `/octave:proposal` — Customer-facing business case for the Compel stage
- `/octave:battlecard-doc` — Visual competitive reference (if a competitor is in the deal)
