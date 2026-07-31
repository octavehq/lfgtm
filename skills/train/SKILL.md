---
name: train
description: Onboarding GTM primer generator. Produces a self-contained, interactive slide lesson a new rep works through to learn the whole go-to-market: what we sell, who we sell to, how to position to each buyer, who we compete with, and proof, with checkpoint questions they must clear to advance and a score at the end. Use when user says "onboarding primer", "GTM primer", "onboard a new rep", "ramp doc", "train a new hire", or "GTM 101".
argument-hint: "[--personas <name,name,...>] [--style <preset>]"
---

# /octave:train - Onboarding GTM Primer

Generate the one lesson a new rep completes on day one to learn how your company sells. The primer turns your Octave library into a self-contained, **gated interactive slide lesson**: five teaching topics, one per slide, each ending with checkpoint questions the rep must clear before Next unlocks, then a score. The topics are what we sell and the problem it solves, who we sell to, how to position to each buyer (an interactive per-persona selector), who we compete with and how we win (a tabbed competitor deep-dive), and the proof to point to (tabbed by lens).

This is a **workspace-level, evergreen** lesson, not an account plan. There is no target company. It is grounded entirely in the library's own GTM: the workspace company positioning, personas and segments, Motion ICP cell narratives, competitors, proof points, and references. The full spec, slide order, interaction model, and review checklist live in [primer-sections.md](references/primer-sections.md).

## On-brand styling — brand kit first, then generate

**Resolve the brand before generating (do not skip this step).** The primer is an internal enablement document for the **workspace company's own team**, so it goes out on the **workspace company's brand** (the Octave customer whose workspace you are operating in). There is no target account.

**Step 1: Identify the workspace company.** Call `get_workspace_company` to get the company name, domain/URL, and positioning. This is the company whose brand the primer uses and whose GTM it teaches.

**Step 2: Resolve the workspace company's brand kit.** Slugify the workspace company name AND its domain, and check for a cached brand kit at `~/.octave/brands/<slug>/manifest.json` (try both slugs). If a complete kit exists (has `manifest.json` and `tokens.css`), use it automatically:
   - inline the kit's `tokens.css` (`:root` + the embedded `@font-face`) **and** `../get-brand-components/assets/kit_base.css` into the output `<style>`;
   - follow the kit's `brand-kit.md` → **Signature moves**.
   - **Use the kit's real logo, resolved dynamically (never hardcode a logo).** The logo changes per company, so read it from the resolved kit's `manifest.json` `logo` block. Use the **onLight** variant on light surfaces (the topbar over content slides) and the **onDark** / white variant on the dark gradient bands (cover, completion, and the topbar while those are showing). **Inline the logo as a base64 data URI** in the HTML so the file stays self-contained and survives sharing (do not reference a local file path in the delivered file). If the kit only has one logo variant, use it as-is on light and recolor to white for dark bands (`filter: brightness(0) invert(1)`) only as a fallback.
   - **Verify the logo is actually the workspace company's mark before using it.** Cached kits can contain a mislabeled or stray asset (a real example: the cached Octave kit's `*-logo-white.png` was actually a WorkSpan logo). Open/preview the resolved logo file; if a variant is the wrong company or clearly wrong, use another variant, another cached kit for the same company, or recolor the known-good variant. Never ship a logo you have not eyeballed.
   **If no complete kit exists → build one.** Run the `get-brand-components` skill (read its SKILL.md and follow it) for the workspace company's domain, which captures the real logo among other assets. If the first attempt returns incomplete results, retry up to 3 times with different approaches (root domain, `www.` prefix, `/about` subpage). Only fall back to a style preset after 3 genuine failures.

**Step 3: Style presets are a last resort** — only after the workspace company's brand kit cannot be built (see Step 3 in Instructions).

## Principles

Follow these standards during generation. Read each before producing output.

**Content and language:**
- [Editorial rules](../shared/editorial-rules.md) — no AI-isms, banned vocabulary, honest tone
- [Information principles](../shared/information-principles.md) — lead with conclusions, evidence-backed claims, narrative arc

**Visual design:**
- [Presentation principles](../shared/presentation-principles.md) — typography, layout, visual restraint
- [Slide deck format](../shared/formats/slide-deck.md) — paginated-slide specifics (the primer is a gated slide lesson, not a scrollable doc)

**Octave data:**
- [Octave value](../shared/octave-value.md) — prioritize grounded workspace data over generic AI content

Apply these rules during generation, not just at review. After generating, the **review pipeline is a mandatory gate** (see Step 5) — the primer is not opened or delivered until the scorecard is produced.

## Usage

```
/octave:train [--personas <name,name,...>] [--style <preset>]
```

## Examples

```
/octave:train                                          # Build the primer, pick featured personas interactively
/octave:train --personas "CISO,Security Engineer"      # Feature specific personas in the selector
/octave:train --style paper-minimal                    # Force a preset if no brand kit exists
```

## Instructions

When the user runs `/octave:train`:

### Step 1: Scope the Primer

The primer teaches the whole GTM, but it cannot feature every persona in a large library without becoming a directory. Scope it first.

**1a: Inventory the personas.**
```
list_entities({ entityType: "persona" })
```

**1b: Choose the featured personas (the persona-narrowing rule).** The persona selector in Job 3 is the crown jewel, and it only works if it is a handful of buyers a new rep can actually hold in their head.

- If the library has **6 or fewer personas**, feature them all.
- If the library has **more than 6 personas**, do NOT dump them all. Surface the list and ask the rep to narrow it:

```
AskUserQuestion({
  questions: [{
    question: "Your library has [N] personas — more than a new rep can learn at once. Which are the core buyers to feature in the primer? (Recommend the economic buyers and champions you actually sell to; the rest stay in the library.)",
    header: "Featured personas",
    options: [ /* the personas most central to the primary Motion's ICP, each: label = persona name, description = title + one-line concern */ ],
    multiSelect: true
  }]
})
```

Recommend the personas most central to the primary Motion's ICP cells (the ones with ready versions and the richest narratives). Cap the featured set at 6. Everything else is still true and still in the library; it just does not earn a card in an onboarding doc.

**1c: Confirm the scope.** Briefly tell the rep which personas will be featured and that the primer covers the full GTM (product, competitors, proof) beyond just those personas.

### Step 2: Octave Context Gathering

Build the primer from the library. **Tell the rep what you are pulling and why.** Each job maps to specific tools:

**Job 1 — What we sell + the problem.**
```
get_workspace_company()                                  # whyWeExist, positioning, whyCustomersBuy, whyCustomersCare
list_entities({ entityType: "product" })             # the product(s)
get_entity({ oId: "<product_oId>" })                     # full product narrative
```

**Slide 1 also needs customer archetypes.** Slide 1 opens with three customer archetype cards (their problem, why they came to us, and the real named customer). Pull these from real references, so grab the reference narratives here too:
```
list_entities({ entityType: "reference" })           # named customers to build archetypes from
get_entity({ oId: "<reference_oId>" })                   # the full story for the 3 archetypes you feature
```

**Slide 2 — Who we sell to.**
```
list_entities({ entityType: "persona" })             # from Step 1
list_entities({ entityType: "segment" })             # the market segments / ICP
get_entity({ oId: "<segment_oId>" })                     # full narrative for the segments you feature as cards
```
Slide 2 teaches the buying committee (with champion vs economic-buyer roles) and the segments as real cards with substance, not just chips. Do NOT surface Motions or other internal platform vocabulary on the slide (it is Octave inside-baseball). `list_motions` is still used behind the scenes to find the primary motion for Slide 3's ICP cells, but it is not shown to the reader.

**Slide 3 — How to sell to each buyer (the crown jewel).** For **every** featured persona, pull its Motion ICP cell narrative. This is the per-persona positioning that makes the primer Octave-only, and every persona gets a fully populated panel (not just one).
```
list_motions()                                           # find the primary motion (behind the scenes only)
list_motion_icps({ motionOId: "<primary_motion_oId>", personaOIds: ["<persona_oId>"] })
find_motion_icp({ motionIcpOId: "<micp_oId>", includeLearnings: true })
```
The narrative gives you, per persona: `operatingLandscape` (their world), `painsAndConsequences` (what they care about), `benefitsAndImpacts`, and a full `salesMethodology` (Resonate → Elevate → Compel with Buyer Mindset, Value Propositions, and Talking Points per stage). If a persona has cells in several segments, pick the primary segment (ready version, richest narrative) and note the segment context; do not average across cells. **Call `find_motion_icp` for each featured persona** so every tab is fully populated; a persona with no ready version uses persona-entity data only (their world + pains), tagged `.unconfirmed`, with no fabricated talk track. Slide 3 has **one checkpoint per persona**.

**Slide 4 — Who we compete with + how we win (tabbed deep-dive).**
```
list_entities({ entityType: "competitor" })          # the named competitors
get_entity({ oId: "<competitor_oId>" })                  # each competitor's capabilities + our differentiation
list_findings({ query: "<competitor name>" })            # real deals the competitor came up in (for the "deals came up in" panel)
get_competitive_insights({ ... })                        # if available, competitive deal intel
```
Each featured competitor gets a tab with: a verdict badge (Direct / Adjacent / Build-it-yourself), what they are, a **capability comparison table** (them vs us, every row traced to the entity description, never invented checkmarks), a you'll-hear/what-to-say pair, and a **deals-they-came-up-in** panel from `list_findings`. If findings are unavailable, show a labeled pending panel rather than inventing deals. If a competitor entity says intel is thin ("we lack verified intel"), put it on the honest-gap watchlist, do not invent a wedge.

**Slide 5 — Proof (tabbed by lens).**
```
list_entities({ entityType: "proof_point" })         # the proof points
list_entities({ entityType: "reference" })           # named customer references
get_entity({ oId: "<proof_oId>" })                       # full narrative for the ones you feature
```
Organize proof into lenses (By objection, By buyer, By segment, By outcome). A proof point may appear under more than one lens; that reuse is intentional.

**Checkpoints are woven into the slides, not a separate quiz.** Each content slide ends with checkpoint questions the rep must answer to advance (Slide 3 has one per persona). Every checkpoint and its correct answer must trace to content on that same slide.

**Groundedness is a hard bar.** Every persona, competitor, proof point, customer name, and metric in the primer must trace to a real tool result, not a plausible synthesis. Do not invent a competitor wedge, a customer story, or a metric. Honest gaps ("we do not yet have verified intel on this competitor") beat inventions. Tag anything unconfirmed with `.unconfirmed`. The review pipeline's groundedness check validates the agent's self-reported sources, so verify facts against the actual tool output yourself.

**Output of this step:** Present a short outline to the rep for approval before generating — the five topics, the featured personas, the competitors you will give deep-dive tabs, and the proof lenses. Wait for approval before proceeding.

### Step 3: Resolve the Brand

Follow the "On-brand styling" section at the top of this skill: `get_workspace_company` → cached kit at `~/.octave/brands/<slug>/` (try name-slug and domain-slug) → build via `get-brand-components` (retry up to 3 times) → preset fallback.

**Only if the brand kit genuinely cannot be built**, fall back to a style preset:

| Feel | Fallback Preset |
|----------|-----------------|
| Modern / technical | `midnight-pro` |
| Editorial / clean | `paper-minimal` |
| Executive | `executive-dark` |
| General | `paper-minimal` |

CSS variable definitions for presets are in the shared [style-presets.md](../shared/style-presets.md).

### Step 4: Generate HTML

**Load the shared rules before writing any HTML. Read each before producing output:**
- [Editorial rules](../shared/editorial-rules.md) — universal language rules, AI-ism kill list, banned vocabulary
- [Information principles](../shared/information-principles.md) — lead with conclusions, evidence-backed claims, narrative arc
- [Presentation principles](../shared/presentation-principles.md) — universal visual rules, spacing, restraint
- [Slide deck format](../shared/formats/slide-deck.md) — paginated-slide visual rules
- [Octave value](../shared/octave-value.md) — grounded workspace data over generic AI content

Apply these rules during generation, not just during review.

Build a single, self-contained HTML file. **No external dependencies** except Google Fonts. Everything else inlined, including the slide navigation, checkpoint gating, and tab-selector JavaScript.

**After writing the file, proceed immediately to Step 5 (Review Pipeline). Do NOT open the file in the browser or present it to the rep yet.**

#### Output Directory

The primer goes under `.octave-primers/` in the user's **home directory** (`~/.octave-primers/`, not the skill or project folder):

```
.octave-primers/
└── <workspace-company-slug>-gtm-primer-<YYYY-MM-DD>/
    └── <slug>-gtm-primer.html
```

Example: `.octave-primers/material-security-gtm-primer-2026-07-09/material-security-gtm-primer.html`

#### Primer Sections — the Six Jobs

See [primer-sections.md](references/primer-sections.md) for the full specification: the six jobs, their fixed order, per-job density caps, the interactive persona selector and quiz specs, the component-fatigue rules, and the review checklist. Read it before generating — it is where the tight-jobs discipline lives.

#### HTML Scaffold

See [html-scaffold.md](references/html-scaffold.md) for the HTML structure, the CSS component library (cards, role badges, the persona selector, aligned proof cards, the quiz), and the required print + interaction scripts.

#### Content Writing Guidelines

The primer is a teaching document, not a feature list. Follow these principles:

1. **Write for a rep on day one.** No prior context assumed. Define the market and the buyer before the pitch.
2. **Lead with the buyer's world.** Every persona section opens from the buyer's perspective (their status quo, their pain), not our capability.
3. **One idea per line.** New reps skim, then re-read. Badges, tags, and short lines beat paragraphs.
4. **Ground every claim.** Real personas, real competitor names, real proof points. Generic = forgettable.
5. **Teach the wedge, not the teardown.** Competitor sections are honest and respectful: how we win, in one line, not a hit piece.
6. **The quiz reinforces, it does not trick.** Every answer is derivable from the primer above it.

### Step 5: Review Pipeline — MANDATORY GATE

**Do NOT open the primer in the browser, present the delivery summary, or tell the rep the primer is ready until the review pipeline has completed and you have a scorecard.**

Load the [review protocol](../shared/protocol.md) and execute the review loop against the generated HTML file. Here is the train-specific wiring:

**5a: Mechanical lint** (before spawning reviewers):

```bash
bash <skill-dir>/../shared/scripts/lint.sh <path-to-primer.html>
```

Fix every violation the lint surfaces.

**5b: Spawn two reviewers in parallel** (both Task calls in a single message). If the `octave-editorial-reviewer` / `octave-presentation-reviewer` subagents are not in the session registry, run them as `general-purpose` agents seeded with the same prompts (their definitions live at `~/.claude/agents/*.md`).

**Editorial reviewer:**
```
Task tool:
  subagent_type: "octave-editorial-reviewer"
  prompt: "Review the file at [FILE PATH].
           Read these principle docs and run each Review Checklist:
           1. [skill-dir]/../shared/editorial-rules.md
           2. [skill-dir]/../shared/information-principles.md
           3. [skill-dir]/../shared/octave-value.md
              (Data Grounding and Framing sections — every persona,
              competitor, proof point, and metric must trace to
              workspace data)
           4. [skill-dir]/references/primer-sections.md
              (Density Rules + Review Checklist)
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
           3. [skill-dir]/references/html-scaffold.md
           4. [skill-dir]/references/primer-sections.md
           Also verify the interactive elements work: the persona
           selector swaps panels, and the quiz scores and reveals
           answers. Fix violations inline. Return scorecard."
```

**5c: Loop decision.** Read both scorecards:

| Cycle | 0 fixes | 1-2 fixes | 3+ fixes |
|---|---|---|---|
| Cycle 1 | CLEAN → 5d | Apply, loop | Apply, loop |
| Cycle 2 | CLEAN → 5d | Apply, STOP | Apply, loop |
| Cycle 3 (cap) | CLEAN → 5d | Apply, STOP | Apply, STOP |

Max 3 cycles. Re-run both reviewers each loop (back to 5b).

**5d: Output combined scorecard** to the rep. This is proof the pipeline ran. Step 6 cannot start without it.

```
REVIEW PIPELINE COMPLETE
=========================
Editorial:      [N fixes / PASS]
Presentation:   [N fixes / PASS]

Total fixes: [N]
Cycles: [1-3]
Status: [CLEAN / N remaining issues]
```

### Step 6: Delivery

After the review pipeline scorecard has been output:

1. **Open the primer** in the default browser.
2. **Present a short summary:** the featured personas, the competitors and proof covered, the quiz length, and the file path. Offer to adjust the featured personas or add a section.

**PDF export guidance:**

```
To save as PDF: open the primer, press Cmd+P (Mac) or Ctrl+P (Windows),
enable "Background graphics", and Save as PDF. The persona selector prints
with all panels expanded and the quiz prints with answers shown.
```

## MCP Tools Used

### Workspace & Brand
- `get_workspace_company` — workspace company identity, positioning, and brand resolution

### Library — Fetching Entities
- `list_entities` — quick scan of personas, segments, products, competitors, proof points, references
- `get_entity` — full narrative for a persona, product, competitor, proof point, or reference

### Motions
- `list_motions` — the workspace's motions (net-new, upsell)
- `list_motion_icps` — persona × segment cells for a motion
- `find_motion_icp` — full per-cell narrative (operating landscape, pains, benefits, Resonate → Elevate → Compel methodology) + Learning Loop learnings

### Searching
- `search_knowledge_base` — semantic search across library entities when a specific topic needs backfilling

## Error Handling

**Octave Connection Failed:**
> Could not connect to your Octave workspace.
>
> The primer is built from your library, so I need the connection. Reconnect (check your Octave MCP configuration and reconnect) and re-run.

**No Personas in Library:**
> No personas found in your library. The primer's persona selector needs them.
>
> Add personas first with `/octave:library create persona`, or I can build a lighter primer from your product, competitors, and proof only.

**Too Many Personas:**
> Your library has [N] personas — too many to feature in an onboarding doc. I'll ask you to pick the core buyers (see Step 1b) and keep the primer to a handful a new rep can actually learn.

**No Competitors:**
> No competitors in your library. I'll build the primer without the "Who we compete with" section rather than invent one.
>
> Add competitors with `/octave:library create competitor` for a complete primer.

**No Proof Points:**
> No proof points or references in your library. I'll omit the Proof section rather than fabricate customer stories.
>
> Add them with `/octave:library`, or point me at a resource with results.

**No Motion ICP Cells:**
> No Motion ICP cells with ready versions, so the per-persona positioning (Job 3) would be generic.
>
> I'll build the persona selector from the persona entities alone and flag it as thinner. For the full crown-jewel positioning, generate Motion ICP versions first.

## Related Skills

- `/octave:deal-coach` — live practice: role-play, coaching microsites, and methodology drills (Resonate → Elevate → Compel) for reps who have read the primer
- `/octave:battlecard-doc` — a deep competitive reference document for one competitor
- `/octave:library` — create and edit the personas, competitors, and proof points the primer is built from
- `/octave:insights` — real field intelligence to keep the primer current as the market shifts
