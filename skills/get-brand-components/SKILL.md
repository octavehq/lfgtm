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

A capture is a fixed pipeline over five agents in `<plugin-root>/agents/brand-kit/`; the capture scripts and `kit_base.css` ship in this skill's `scripts/` and `assets/`, and the procedure the agents follow is in this skill's references: [capture workflow](references/capture-workflow.md), [fidelity gate](references/fidelity-gate.md), [design judgement](references/design-judgement.md). You are the orchestrator: you dispatch, pass file paths, run the scripts that decide, promote, and report. You do not read the evidence pack, write kit files or score renders yourself. `list`, `show`, `export` and `delete` stay in this session ([cache operations](references/cache-operations.md)).

Four rules hold at every step:

- **The plugin is read-only.** During a capture nothing under `PLUGIN_ROOT` is created, edited or deleted: not `kit_base.css`, not the specs, not the agents, not the scripts. An installed plugin is not a checkout. The kit adapts through tokens, knobs, `render.surfaces` and `hero.html` only; what the renderer cannot express is collected as renderer feedback for the plugin maintainers (below), never applied in the run.
- **Agent tool only.** Dispatch every agent with the Agent tool; never the Workflow tool. No agent spawns agents. Scripts the orchestrator runs itself (`mine`, `judge_context.py`, `gate_decide.py`, `promote`, `mark-ready`) are single commands with their output on disk.
- **Two questions, no more.** Agents cannot ask the user and neither do you, except for an asset-store match (reuse a kit a teammate published, or spend scrape credits) and the closing question (open the kit, or host it).
- **Reports are files** under `RUN_DIR/reports/`; agents return summaries of at most 15 lines ending with the report path. Before the next step you check the file exists; if it does not, save the summary there with a one-line note. Never re-dispatch for a missing report, never paste a report into a prompt.

Agent types are scoped `octave:brand-kit:<name>`; use the name exactly as your host lists it. A host without subagent delegation runs the five agent files as instructions, sequentially, in the same order ([host runtime](../shared/host-runtime.md)).

### Step 0: resolve

`PLUGIN_ROOT` (absolute installed plugin root), `TARGET` (the domain or URL as typed), `REFRESH=yes|no`, `RUN_DIR=${TMPDIR:-/tmp}/brand-kit-<slug>-<timestamp>` (create it, with `reports/`), `BRAND_CACHE` (default `~/.octave/brands`), `WORKSPACE` (from `verify_connection`, else `unknown`). Note the wall-clock; note it again at every step boundary for the timing table in the capture report. `DOMAIN` and `CACHE_ROOT` come back from the home crawler (computed by `brand_cache.py canonical`); adopt them and never derive a hostname yourself.

### Step 1: homepage — `brand-crawler` `TASK=home` (one agent)

Dispatch with the values above and `TASK=home`. It resolves identity, checks the cache and the asset store, scrapes and ingests the homepage once, and runs `pick-pages`. Act on `outcome`: `READY` (the cache already holds a ready kit: go to the closing, no capture report; `refresh` re-walks); `ASSET_MATCH` (the one question: **Use it (Recommended)** or **Rebuild fresh**, then re-dispatch `TASK=home` with `ASSET_DECISION=use|rebuild`); `HOME` (keep `domain`, `cache_root`, `evidence_dir`, `draft_kit` when the cache held a live draft, and `pages`, the picked URLs).

### Step 1b: the other pages — `brand-crawler` `TASK=pages` × up to 3 (one message)

Only when `pages` is not empty. Deal the URLs round-robin over `N = min(3, number of pages)` crawlers (URL `i` goes to crawler `i mod N`; 5 pages give 2, 2, 1) and dispatch all `N` in one message, each with `TASK=pages PAGES=<its URLs, one per line>` plus `PLUGIN_ROOT`, `DOMAIN`, `RUN_DIR`. Each scrapes and ingests its pages and returns `crawled:` and `failed:` lists. A crawler that fails or times out costs its pages only: do not retry, carry its URLs into the capture report under failed pages, and continue. A single-page site (empty `pages`) skips this step entirely.

### Step 1c: mine (orchestrator, one command)

```bash
python3 <PLUGIN_ROOT>/skills/get-brand-components/scripts/prefetch.py mine --pages-dir <RUN_DIR>/evidence/firecrawl --out <RUN_DIR>/evidence
python3 -c "import json;e=json.load(open('<RUN_DIR>/evidence/evidence.json'));h=e['pages'][0];print(json.dumps({'capabilities':e['capabilities'],'top':h.get('screenshotTop'),'strips':h.get('screenshotStrips'),'bottom':h.get('screenshotBottom')}))"
```

Never pass `--no-playwright`. Keep `capabilities`, `source_top`, `source_strips` and `source_bottom` (paths relative to `<RUN_DIR>/evidence`); print the Playwright error line when `capabilities.playwright` is false.

### Step 2: evidence — `brand-design-analyst` and `brand-logo-verifier` (two agents, one message)

Both get `PLUGIN_ROOT`, `DOMAIN`, `EVIDENCE_DIR=<RUN_DIR>/evidence`, the `capabilities` line and their `REPORT` path (`reports/brand-design-analyst.md`, `reports/brand-logo-verifier.md`). Wait for both reports.

### Step 3: build — `brand-kit-author` (one agent)

`TASK=build KIT_VERSION=1` with `DOMAIN`, `WORKSPACE`, `RUN_DIR`, `SOURCE_URLS` (the crawled pages), `DESIGN_FINDINGS`, `LOGO_FINDINGS` (the two report paths) and `REPORT=reports/brand-kit-author-v1.md`. With `draft_kit` from the home crawler: `TASK=render-only BASE=<draft_kit> KIT_VERSION=1` instead. It writes `kit-v1/`, `review-v1/{gallery,onepager}.png`, `gate.json`, `gate-onepager.json`, lints and checksums. Nothing is promoted yet. Its `renderer feedback` lines go into `RUN_DIR/reports/renderer-feedback.md` (append; one line each) and nowhere else.

### Step 4: judge context (orchestrator, one command per artifact)

```bash
python3 <PLUGIN_ROOT>/skills/get-brand-components/scripts/judge_context.py --design <analyst report> --logo <verifier report> --artifact gallery --gate <RUN_DIR>/review-v<v>/gate.json --top <source_top> --strips <source_strips...> --bottom <source_bottom> --hero-visual <from the author summary> --domain <DOMAIN> --round <r> --version <v> --out <RUN_DIR>/reports/judge-context-v<v>-gallery.md
python3 <PLUGIN_ROOT>/skills/get-brand-components/scripts/judge_context.py ... --artifact one-pager --gate <RUN_DIR>/review-v<v>/gate-onepager.json ... --out <RUN_DIR>/reports/judge-context-v<v>-onepager.md
```

### Step 5: judges — `brand-kit-judge` ×2 (one message)

One on `gallery.png`, one on `onepager.png`. Each gets `PLUGIN_ROOT`, `DOMAIN`, `ARTIFACT`, `RENDER`, `SOURCE_TOP`, `SOURCE_STRIPS`, `SOURCE_BOTTOM`, its `CONTEXT` and `REPORT=RUN_DIR/reports/judge-v<v>-r<r>-<gallery|onepager>.md`. Judges write their own scorecards.

### Step 6: decision (orchestrator, one command)

```bash
python3 <PLUGIN_ROOT>/skills/get-brand-components/scripts/gate_decide.py --round <r> --scorecards <RUN_DIR>/reports/judge-v<v>-r<r>-*.md --gates <RUN_DIR>/review-v<v>/gate.json <RUN_DIR>/review-v<v>/gate-onepager.json --feedback <RUN_DIR>/reports/renderer-feedback.md
```

The thresholds live in the script (gallery at least 34, no dimension below 3, no hard fail, the gallery judge's `looks_good`, both pre-gates passing); `--feedback` folds the round's `renderer` fixes into the maintainers' file, deduplicated. Its `next` field is the whole decision:

- `tiebreak` (one gallery judge scored 33 to 35): dispatch one more gallery judge for the same version (`REPORT=...-gallery-b.md`), run the command again with both gallery scorecards; the mean counts.
- `pass`: promote that exact version, then mark it ready, in this order and never as an agent dispatch:

  ```bash
  python3 <PLUGIN_ROOT>/skills/get-brand-components/scripts/brand_cache.py promote <RUN_DIR>/kit-v<v> --domain <DOMAIN> --workspace <WORKSPACE> --base <BRAND_CACHE> --write-checksums
  python3 <PLUGIN_ROOT>/skills/get-brand-components/scripts/brand_cache.py mark-ready <CACHE_ROOT> --score <gallery>/40
  ```

  Then write the capture report and go to the closing.
- `repair`: step 7.
- `stop`: step 8.

### Step 7: repair — `brand-kit-author` (one agent)

`TASK=repair KIT_VERSION=<v+1> BASE=<best so far> SCORECARDS=<this round's scorecard paths> REPORT=reports/brand-kit-author-v<v+1>.md`, then back to step 4. "Best" is the version with the highest gallery score; ties go to `looks_good: yes`. Repairs touch only what the scorecards name, at the token level; a fix marked `renderer` is feedback, not work. At most 3 judge rounds per capture: 2 repairs, 6 judge dispatches, plus at most one tiebreak judge per round. Record the gallery and one-pager scores of every round for the capture report.

### Step 8: stop without a pass

`python3 <PLUGIN_ROOT>/skills/get-brand-components/scripts/brand_cache.py status <CACHE_ROOT>`: `missing` (including a stale pointer) means promote the best version as `draft` (the `promote` command above, no `mark-ready`) so the next run resumes it; anything else means leave the pointer untouched (a failed refresh never replaces a working kit); the best candidate's path then goes in the capture report. Then write the capture report and go to the closing.

### The capture report (a file, not terminal output)

Write `RUN_DIR/reports/capture-report.md` with everything a maintainer or a curious user may want and the terminal must not carry: gallery and one-pager scores per round, pointer status (`ready`, `draft` or untouched), kit path, failed pages, the author's assumptions, obstacles, the timing table (one line per step with its wall-clock duration), and **Renderer feedback for the plugin maintainers**: the contents of `renderer-feedback.md`, each line naming the file, the change and why, for a fix in the repository, never in the installed plugin. One `Write`; the agent reports stay beside it in `RUN_DIR/reports/`.

### The closing (every path that ends with a kit: `READY`, `pass`, `stop`)

Print at most three lines, then ask one question. Nothing from the capture report is repeated here.

```
<domain>: brand kit <ready | saved as draft | kept the previous kit> · gallery <score>/40 <(passed | after 3 rounds, bar is 34)> · <total time>
Kit: <absolute kit directory, ~ expanded>
Details: <RUN_DIR>/reports/capture-report.md        (omit on READY)
```

The question (`AskUserQuestion`, two options):

- **Open in browser (Recommended)**: open `<kit>/components.html` with the host's opener (`open` on macOS, `xdg-open` on Linux, `start` on Windows), print the path, stop.
- **Host on Octave**: hosting below. Print the URL it returns, stop.

When the host has no Octave asset tools, skip the question and open the gallery.

### Hosting via `/octave:asset-manager`

Hosting is the [asset-manager skill](../asset-manager/SKILL.md)'s job; this skill never calls asset tools or upload scripts itself. Invoke it as a user would, `/octave:asset-manager publish <absolute kit directory>` (with a Skill tool: `octave:asset-manager`, args `publish <kit dir>`; without one, read its `SKILL.md` and follow its publish workflow), and hand it these inputs so it asks nothing back:

| Input | Value | Why |
|---|---|---|
| source | the kit directory only (`manifest.json`, `tokens.css`, `components.html`, `brand-kit.md`, fonts, logos, icons, images) | the publish manifest excludes everything in `RUN_DIR` |
| identifier | `<slug>-brand-kit` | readable, and how kits published without a category are still found |
| category | `brand-kit` | what Step 1's asset-store check filters on, so a teammate's next run reuses it |
| type, entry point | `website`, `components.html` | the gallery is the page |
| privacy, status | `workspace`, `published` | teammates can reuse it; not public |
| description | `Brand kit for <domain>, gallery <score>/40`, plus `, draft` when the pointer is not ready | the asset list shows the state |
| existing asset | Step 1 found a hosted kit you own and the answer was *Rebuild fresh*: `update <identifier>` instead of `publish` | one hosted kit per domain |

The asset-manager's own rules apply from there (publish manifest, readback, registry, URL verification).

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

The agents live at `<plugin-root>/agents/brand-kit/`; the scripts and assets they run ship in this skill. Commands address both from the installed plugin root (`<plugin-root>/skills/get-brand-components/scripts/…`) so a dispatched agent resolves the same paths as this session. Inline template JS/CSS into self-contained artifacts; do not add runtime dependencies on the plugin installation.

- Agents, in `<plugin-root>/agents/brand-kit/`: `brand-crawler.md`, `brand-design-analyst.md`, `brand-logo-verifier.md`, `brand-kit-author.md`, `brand-kit-judge.md`
- Scripts: [prefetch.py](scripts/prefetch.py), [gate_check.py](scripts/gate_check.py), [gate_decide.py](scripts/gate_decide.py), [judge_context.py](scripts/judge_context.py), [render_gallery.py](scripts/render_gallery.py), [render_kit.py](scripts/render_kit.py), [render.py](scripts/render.py), [check_adherence.py](scripts/check_adherence.py), [kit_validation.py](scripts/kit_validation.py), [brand_cache.py](scripts/brand_cache.py), [verify_logos.py](scripts/verify_logos.py), [verify-logos.sh](scripts/verify-logos.sh)
- Assets: [kit_base.css](assets/kit_base.css), [gallery_spec.json](assets/gallery_spec.json), [onepager_spec.json](assets/onepager_spec.json)
