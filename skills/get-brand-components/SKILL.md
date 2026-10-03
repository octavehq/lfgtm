---
name: get-brand-components
description: Capture a brand's visual design system from its website and build a reusable component kit. Walks key pages on a domain (screenshots + HTML via the Octave scrape tool), derives design tokens (colors, type, spacing, radius, shadow), and produces a minimal component library (buttons, cards, headers, stats, tables, badges, hero, footer) as a self-contained HTML reference plus CSS tokens. Use when the user says "get brand components", "capture the brand", "build a component kit for [domain]", "make outputs look like [company]", wants other skills to generate on-brand HTML for a target company, or wants to reuse an already-published brand kit from the asset store or host/share a kit as a live link (via asset-manager).
argument-hint: <domain-or-url> [refresh] | list | show <slug> | export <slug> | delete <slug>
---

# Get Brand Components — Brand-to-Component-Kit Builder

## Run the task

Read [the task method](references/task-method.md) before selecting context, claims, or output. It is the execution method for this skill. Supporting templates supply structure and styling; populate them from the task method and current evidence, not their illustrative figures or assertions.

Capture only the visual system: logos, colors, typography, layout, assets, components and visual usage rules. Keep voice, proof and messaging outside the kit. Preserve source fidelity; dark surfaces do not imply glow. Validate a staged kit before promoting its canonical domain/workspace identity.

Use [GTM context](../shared/gtm-context.md) for strategic tasks and [evidence and inputs](../shared/evidence-and-inputs.md) for material claims and missing facts. A narrow list/get or a render-only handoff does not require unrelated research. Read [host runtime](../shared/host-runtime.md) for available tools, portable resource paths, routing, and review fallback.

Resolve current tool schemas before execution; use returned IDs and pagination. Inventory rows locate records; hydrate selected entities/resources before relying on their contents. Reuse supplied or inherited context and authorization. Ask grouped questions only for material unresolved inputs, continue independent work, incorporate replies, and recheck affected output.

## Usage

```
/octave:get-brand-components <domain-or-url>     # Walk the site and build a brand component kit
/octave:get-brand-components <domain> refresh    # Force a fresh re-walk, overwriting the cached kit
/octave:get-brand-components list                # List saved brand kits
/octave:get-brand-components show <slug>         # Display a saved kit (and open the gallery)
/octave:get-brand-components export <slug>       # Zip the cached kit to ~/Desktop/<slug>-brand-kit.zip
/octave:get-brand-components delete <slug>       # Remove a saved kit
```

## How the capture runs

A capture is an orchestration over five agents in `<plugin-root>/agents/brand-kit/`. The capture scripts and `kit_base.css` live beside them; the procedure the agents follow is in this skill's references: [capture workflow](references/capture-workflow.md), [fidelity gate](references/fidelity-gate.md) and [design judgement](references/design-judgement.md). You are the orchestrator: you dispatch, pass file paths between phases, write the judge context, decide the gate, apply renderer fixes, and report. You do not read the evidence pack, write kit files or score renders yourself. `list`, `show`, `export` and `delete` stay in this session ([cache operations](references/cache-operations.md)).

Agent types are scoped `octave:brand-kit:<name>`; use the name exactly as your host lists it. A host without subagent delegation runs the five agent files as instructions, sequentially, in the order below ([host runtime](../shared/host-runtime.md)).

**No questions during a capture.** Agents cannot ask the user and neither do you, with one exception: an asset-store match (reuse a kit a teammate already published, or spend scrape credits), which is a cost decision. Everything else, including renderer-level fixes, follows the rules below and is reported at the end.

**Reports are files.** Every agent writes its full report under `RUN_DIR/reports/` and returns a summary of at most 15 lines ending with the report path. Dispatch prompts carry `NAME=value` lines and file paths; never paste a report or a scorecard into a prompt.

Before Phase 1 resolve: `PLUGIN_ROOT` (the absolute installed plugin root), `TARGET` (the domain or URL as typed), `REFRESH=yes|no`, `RUN_DIR=${TMPDIR:-/tmp}/brand-kit-<slug>-<timestamp>` (create it, with `reports/` inside), `BRAND_CACHE` (default `~/.octave/brands`) and `WORKSPACE` (the id from `verify_connection` when the Octave tools are available, else `unknown`). `DOMAIN` and `CACHE_ROOT` come back from the crawler, computed by `brand_cache.py canonical`; adopt those values for every later dispatch and never derive a hostname yourself (the seed may carry `www.`, the cache never does).

### Phase 1: fetch — `brand-crawler`

Dispatch in the foreground with the values above and "Follow your instructions and return the BRAND CRAWLER RESULT." Act on `outcome`:

- `READY`: print the summary line, open `components.html`, mention `refresh`, stop.
- `ASSET_MATCH`: the one question. AskUserQuestion with **Use it (Recommended)** or **Rebuild fresh**, then re-dispatch the crawler with `ASSET_DECISION=use|rebuild`.
- `EVIDENCE`: continue. Keep `domain`, `cache_root`, `evidence_dir`, `capabilities`, `source_top`, `source_strips`, `source_bottom`, `draft_kit` (set when the cache held a draft that never passed the gate: Phase 2 runs as usual and Phase 3 re-renders that draft instead of building) and the report path. When `capabilities` says `playwright false`, print the error line it carries; the run continues with the analyst marking values `inferred`.

### Phase 2: evidence — `brand-design-analyst` and `brand-logo-verifier`, in one message

Both get `PLUGIN_ROOT`, `DOMAIN`, `EVIDENCE_DIR=<RUN_DIR>/evidence`, the crawler's `capabilities` line and their own `REPORT` path (`RUN_DIR/reports/brand-design-analyst.md`, `RUN_DIR/reports/brand-logo-verifier.md`). They are read-only and return summaries; the reports are the author's input.

### Phase 3: build — `brand-kit-author`

Dispatch with `TASK=build KIT_VERSION=1`, the identity values (`DOMAIN`, `WORKSPACE`, `BRAND_CACHE`, `CACHE_ROOT`, `RUN_DIR`), `SOURCE_URLS` (the ok pages), `DESIGN_FINDINGS` and `LOGO_FINDINGS` (the two report paths) and `REPORT=RUN_DIR/reports/brand-kit-author-v1.md`. With `draft_kit` from the crawler, dispatch `TASK=render-only BASE=<draft_kit> KIT_VERSION=1` instead. It writes `<RUN_DIR>/kit-v1/`, renders `gallery.png` and `onepager.png` into `RUN_DIR/review-v1/`, runs the pre-gate on both (`gate.json`, `gate-onepager.json`) and the adherence lint, and writes checksums. Nothing is promoted yet: the cache pointer changes only when a version passes the gate (Phase 4), so a refresh never takes a working kit away from consumers while it is judged. The author's summary carries both pre-gate results, its advisory `author view` and `renderer changes needed`.

A pre-gate failure that only the stylesheet can fix, and every item under `renderer changes needed`, go through *Renderer fixes* below, then `TASK=render-only` on the same kit, before any judge runs: a kit the author already knows cannot pass is never judged. At most two such passes per round.

### Phase 4: gate — `brand-kit-judge`

Build one context per artifact and candidate version with one command, never by hand:

```bash
python3 <PLUGIN_ROOT>/agents/brand-kit/scripts/judge_context.py --design <analyst report> --logo <verifier report> --artifact gallery --gate <RUN_DIR>/review-v<v>/gate.json --top <source_top> --strips <source_strips...> --bottom <source_bottom> --hero-visual <from the author summary> --domain <DOMAIN> --round <r> --version <v> --out <RUN_DIR>/reports/judge-context-v<v>-gallery.md
python3 <PLUGIN_ROOT>/agents/brand-kit/scripts/judge_context.py ... --artifact one-pager --gate <RUN_DIR>/review-v<v>/gate-onepager.json ... --out <RUN_DIR>/reports/judge-context-v<v>-onepager.md
```

Each carries the analyst's Emphasis and Devices sections verbatim, `heroVisual`, that artifact's pre-gate measurements, the block-to-source map (CTA and footer map to the dedicated bottom strip; without one, a near-blank last strip is flagged and the strip before it named), and the two rules: do not invent a device the brand lacks; do not dock depth for product imagery when `heroVisual` is `none` or `chips`.

Judges per round: round 1 dispatches three in one message (two on `gallery.png`, one on `onepager.png`); later rounds dispatch two (one of each), or three again when the previous gallery mean was within 3 points of 34. Each gets `PLUGIN_ROOT`, `DOMAIN`, `ARTIFACT`, `RENDER`, `SOURCE_TOP`, `SOURCE_STRIPS` (plus `SOURCE_BOTTOM` when the crawler returned one), the matching `CONTEXT` and `REPORT=RUN_DIR/reports/judge-v<v>-r<r>-<gallery-a|gallery-b|onepager>.md`, so two candidates judged in one round never share a file. The judge writes its own scorecard there and returns a six-line summary; never retype a scorecard.

Gallery score = the mean of the gallery judges (one judge: its total), dimensions averaged the same way. Pass ([fidelity gate](references/fidelity-gate.md)), all for the same candidate version: both pre-gate files report `pass: true` (a failing or NOT RUN pre-gate keeps the kit `draft`, with the reason in the report); gallery mean at least 34; no averaged dimension below 3; no `hard_fail: yes`; and not every gallery judge answering `looks_good: no`.

- Pass: promote that exact version, then mark it ready, in this order and never as an agent dispatch:

  ```bash
  python3 <PLUGIN_ROOT>/agents/brand-kit/scripts/brand_cache.py promote <RUN_DIR>/kit-v<v> --domain <DOMAIN> --workspace <WORKSPACE> --base <BRAND_CACHE> --write-checksums
  python3 <PLUGIN_ROOT>/agents/brand-kit/scripts/brand_cache.py mark-ready <CACHE_ROOT> --score <mean>/40
  ```

  Then the final report.
- Fail, round `r` of at most 3: apply *Renderer fixes* when the trigger below is met, then dispatch the author with `TASK=repair KIT_VERSION=<r+1> BASE=<best kit so far> SCORECARDS=<the saved scorecard paths> REPORT=RUN_DIR/reports/brand-kit-author-v<r+1>.md`, and re-judge the new version. Scores compare only across renders made by the same renderer: after a renderer fix, re-render the current best as its own new version (`TASK=render-only BASE=<best> KIT_VERSION=<next>`) and judge it in the same round as the repaired version, with the same judge count; its earlier score is discarded. The best version is the one with the higher gallery mean (ties go to the one judged `looks_good: yes`). After round 3 without a pass: when `brand_cache.py status <CACHE_ROOT>` says `missing`, promote the best version as `draft` (the same `promote` command, without `mark-ready`) so the next run can resume it; when a kit already exists there, leave its pointer untouched (a failed refresh never replaces a working kit) and report the best candidate's path. The final report says which happened and shows the last scorecards.
- Report the one-pager score beside the gallery score every round; a gap of more than a few points is a finding for the next repair.

### Renderer fixes (automatic, no question)

Trigger: two judges name the same fix marked `renderer`, in one round or across consecutive rounds (in a two-judge round the gallery judge and the one-pager judge are the pair); or the author lists an item under `renderer changes needed` (acted on before the first judge round, see Phase 3); or a pre-gate check only the stylesheet can satisfy; or a `looks_good` reason names the stylesheet or a spec. Action: edit `agents/brand-kit/assets/kit_base.css`, the specs or `render_*.py` yourself, as a new token or knob with the old look as the fallback (the [renderer contract](references/renderer-contract.md) lists the existing ones); run `python3 -m unittest discover -s <PLUGIN_ROOT>/agents/brand-kit/tests`; on green, re-render the current best with `TASK=render-only BASE=<best>` as a new version so every judged version comes from the same renderer. A layout problem the judges keep scoring 3 (band rhythm, the pricing block, the stats band, footer corners) is a renderer fix by definition: tokens cannot move it, so do not spend a repair round on it. Record every edit as file, change, why for the final report. The edits stay uncommitted for review.

### Progress and the final report

One line when a phase starts and ends, the page count, and each round's scores with the `looks_good` answers. The final report: gallery mean and one-pager score, pointer status (`ready` or `draft`), kit path, renderer edits made (by file), the author's assumptions, and obstacles. The agent reports themselves stay in `RUN_DIR/reports/`.

## References by task

- [cache operations](references/cache-operations.md)

- [renderer contract](references/renderer-contract.md)

- [capture workflow](references/capture-workflow.md)

- [asset review](references/asset-review.md)

- [fidelity gate](references/fidelity-gate.md)

- [design judgement](references/design-judgement.md)

Read only the reference for the selected mode, then the format/layout references when rendering. Do not repeat intake or change approved claims when routing to a renderer.

## Delivery and changes

Apply [output readiness](../shared/output-readiness.md) to text and artifacts. HTML also uses the [review protocol](../shared/protocol.md) and the matching format checks. A working preview can be shared with its status; unrun checks are NOT RUN. Reviewers return findings on an immutable version; one author applies edits and rechecks the final version.

For visual output, inherit the selected sender/workspace brand through [brand kit usage](../shared/brand-kit-usage.md); honor an explicit override and avoid repeated brand extraction. Public hosting requires the approved audience and publish manifest, followed by URL/access/link verification.

For comparisons, trends or rates, use the [analytics contract](../shared/analytics-contract.md). Only requested persistence loads [workspace mutations](../shared/workspace-mutations.md); report changes as applied only after scoped readback.

## Runtime resources

The capture tooling lives at `<plugin-root>/agents/brand-kit/`, next to the agents that run it; resolve these paths from the installed plugin root, not this skill directory. Inline template JS/CSS into self-contained artifacts; do not add runtime dependencies on the plugin installation.

- Agents: [brand-crawler](../../agents/brand-kit/brand-crawler.md), [brand-design-analyst](../../agents/brand-kit/brand-design-analyst.md), [brand-logo-verifier](../../agents/brand-kit/brand-logo-verifier.md), [brand-kit-author](../../agents/brand-kit/brand-kit-author.md), [brand-kit-judge](../../agents/brand-kit/brand-kit-judge.md)
- Scripts: [prefetch.py](../../agents/brand-kit/scripts/prefetch.py), [gate_check.py](../../agents/brand-kit/scripts/gate_check.py), [render_gallery.py](../../agents/brand-kit/scripts/render_gallery.py), [render_kit.py](../../agents/brand-kit/scripts/render_kit.py), [render.py](../../agents/brand-kit/scripts/render.py), [check_adherence.py](../../agents/brand-kit/scripts/check_adherence.py), [kit_validation.py](../../agents/brand-kit/scripts/kit_validation.py), [brand_cache.py](../../agents/brand-kit/scripts/brand_cache.py), [verify_logos.py](../../agents/brand-kit/scripts/verify_logos.py), [verify-logos.sh](../../agents/brand-kit/scripts/verify-logos.sh)
- Assets: [kit_base.css](../../agents/brand-kit/assets/kit_base.css), [gallery_spec.json](../../agents/brand-kit/assets/gallery_spec.json), [onepager_spec.json](../../agents/brand-kit/assets/onepager_spec.json)
