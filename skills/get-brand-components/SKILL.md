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

A capture is a fixed pipeline over five agents in `<plugin-root>/agents/brand-kit/`; the capture scripts and `kit_base.css` live beside them, and the procedure the agents follow is in this skill's references: [capture workflow](references/capture-workflow.md), [fidelity gate](references/fidelity-gate.md), [design judgement](references/design-judgement.md). You are the orchestrator: you dispatch, pass file paths, run the decision script, apply at most one renderer fix, promote, and report. You do not read the evidence pack, write kit files or score renders yourself. `list`, `show`, `export` and `delete` stay in this session ([cache operations](references/cache-operations.md)).

Three rules hold at every step:

- **Agent tool only.** Dispatch every agent with the Agent tool; never the Workflow tool. No agent spawns agents. Promotion and `mark-ready` are two direct commands you run yourself.
- **No questions.** Agents cannot ask the user and neither do you, except for an asset-store match (reuse a kit a teammate published, or spend scrape credits).
- **Reports are files** under `RUN_DIR/reports/`; agents return summaries of at most 15 lines ending with the report path. Before the next step you check the file exists; if it does not, save the summary there with a one-line note. Never re-dispatch for a missing report, never paste a report into a prompt.

Agent types are scoped `octave:brand-kit:<name>`; use the name exactly as your host lists it. A host without subagent delegation runs the five agent files as instructions, sequentially, in the same order ([host runtime](../shared/host-runtime.md)).

### Step 0: resolve

`PLUGIN_ROOT` (absolute installed plugin root), `TARGET` (the domain or URL as typed), `REFRESH=yes|no`, `RUN_DIR=${TMPDIR:-/tmp}/brand-kit-<slug>-<timestamp>` (create it, with `reports/`), `BRAND_CACHE` (default `~/.octave/brands`), `WORKSPACE` (from `verify_connection`, else `unknown`). Note the wall-clock; note it again at every step boundary for the timing table in the final report. `DOMAIN` and `CACHE_ROOT` come back from the crawler (computed by `brand_cache.py canonical`); adopt them and never derive a hostname yourself.

### Step 1: fetch — `brand-crawler` (one agent)

Dispatch with the values above and "Follow your instructions and return the BRAND CRAWLER RESULT." Inside the agent the homepage is fetched alone, then the picked pages in batches of at most 4 parallel `scrape_website` calls. Act on `outcome`: `READY` (print the summary line, open `components.html`, mention `refresh`, stop); `ASSET_MATCH` (the one question: **Use it (Recommended)** or **Rebuild fresh**, then re-dispatch with `ASSET_DECISION=use|rebuild`); `EVIDENCE` (keep `domain`, `cache_root`, `evidence_dir`, `capabilities`, `source_top`, `source_strips`, `source_bottom`, `draft_kit` when the cache held a live draft, and the report path; print the error line when `capabilities` says `playwright false`).

### Step 2: evidence — `brand-design-analyst` and `brand-logo-verifier` (two agents, one message)

Both get `PLUGIN_ROOT`, `DOMAIN`, `EVIDENCE_DIR=<RUN_DIR>/evidence`, the `capabilities` line and their `REPORT` path (`reports/brand-design-analyst.md`, `reports/brand-logo-verifier.md`). Wait for both reports.

### Step 3: build — `brand-kit-author` (one agent)

`TASK=build KIT_VERSION=1` with `DOMAIN`, `WORKSPACE`, `RUN_DIR`, `SOURCE_URLS` (the ok pages), `DESIGN_FINDINGS`, `LOGO_FINDINGS` (the two report paths) and `REPORT=reports/brand-kit-author-v1.md`. With `draft_kit` from the crawler: `TASK=render-only BASE=<draft_kit> KIT_VERSION=1` instead. It writes `kit-v1/`, `review-v1/{gallery,onepager}.png`, `gate.json`, `gate-onepager.json`, lints and checksums. Nothing is promoted yet.

**Step 3a, the renderer pass (optional, at most one per capture).** When the author's summary lists `renderer changes needed` or a pre-gate failure only the stylesheet can fix: edit `agents/brand-kit/assets/kit_base.css`, the specs or `render_*.py` yourself, as a new token or knob with the old look as the fallback ([renderer contract](references/renderer-contract.md)); run `python3 -m unittest discover -s <PLUGIN_ROOT>/agents/brand-kit/tests -k Renderer -k ThirdPass -k GateCheck`; on green dispatch `TASK=render-only BASE=<RUN_DIR>/kit-v1 KIT_VERSION=2`. Record the edit (file, change, why) for the final report. If 3a ran, step 7 never does.

### Step 4: judge context (orchestrator, one command per artifact)

```bash
python3 <PLUGIN_ROOT>/agents/brand-kit/scripts/judge_context.py --design <analyst report> --logo <verifier report> --artifact gallery --gate <RUN_DIR>/review-v<v>/gate.json --top <source_top> --strips <source_strips...> --bottom <source_bottom> --hero-visual <from the author summary> --domain <DOMAIN> --round <r> --version <v> --out <RUN_DIR>/reports/judge-context-v<v>-gallery.md
python3 <PLUGIN_ROOT>/agents/brand-kit/scripts/judge_context.py ... --artifact one-pager --gate <RUN_DIR>/review-v<v>/gate-onepager.json ... --out <RUN_DIR>/reports/judge-context-v<v>-onepager.md
```

### Step 5: judges — `brand-kit-judge` ×2 (one message)

One on `gallery.png`, one on `onepager.png`. Each gets `PLUGIN_ROOT`, `DOMAIN`, `ARTIFACT`, `RENDER`, `SOURCE_TOP`, `SOURCE_STRIPS`, `SOURCE_BOTTOM`, its `CONTEXT` and `REPORT=RUN_DIR/reports/judge-v<v>-r<r>-<gallery|onepager>.md`. Judges write their own scorecards.

### Step 6: decision (orchestrator, one command)

```bash
python3 <PLUGIN_ROOT>/agents/brand-kit/scripts/gate_decide.py --round <r> --scorecards <RUN_DIR>/reports/judge-v<v>-r<r>-*.md --gates <RUN_DIR>/review-v<v>/gate.json <RUN_DIR>/review-v<v>/gate-onepager.json
```

The thresholds live in the script (gallery at least 34, no dimension below 3, no hard fail, the gallery judge's `looks_good`, both pre-gates passing). Its `next` field is the whole decision:

- `tiebreak` (one gallery judge scored 33 to 35): dispatch one more gallery judge for the same version (`REPORT=...-gallery-b.md`), run the command again with both gallery scorecards; the mean counts.
- `pass`: promote that exact version, then mark it ready, in this order:

  ```bash
  python3 <PLUGIN_ROOT>/agents/brand-kit/scripts/brand_cache.py promote <RUN_DIR>/kit-v<v> --domain <DOMAIN> --workspace <WORKSPACE> --base <BRAND_CACHE> --write-checksums
  python3 <PLUGIN_ROOT>/agents/brand-kit/scripts/brand_cache.py mark-ready <CACHE_ROOT> --score <gallery>/40
  ```

  Then the final report.
- `repair`: step 7 (round 1 only, if 3a did not run and the decision lists `rendererFixes` or a `looks_good` reason names the stylesheet), then step 8.
- `stop`: step 10.

### Step 7: the renderer pass after round 1 (only if step 3a did not run)

Same procedure as 3a. Renderer edits never happen in rounds 2 or 3. After a renderer fix, only versions rendered by it compete for "best"; earlier scores are discarded, and nothing old is re-judged.

### Step 8: repair — `brand-kit-author` (one agent)

`TASK=repair KIT_VERSION=<v+1> BASE=<best so far> SCORECARDS=<this round's scorecard paths> REPORT=reports/brand-kit-author-v<v+1>.md`. "Best" is the version with the highest gallery score among those rendered by the current renderer; ties go to `looks_good: yes`. Repairs touch only what the scorecards name.

### Step 9: rounds 2 and 3

Repeat steps 4 to 6 for the new version. At most 3 judge rounds per capture: 2 repairs, 6 judge dispatches, plus at most one tiebreak judge per round. Report the gallery and one-pager scores after every round.

### Step 10: stop without a pass

`python3 <PLUGIN_ROOT>/agents/brand-kit/scripts/brand_cache.py status <CACHE_ROOT>`: `missing` (including a stale pointer) means promote the best version as `draft` (the `promote` command above, no `mark-ready`) so the next run resumes it; anything else means leave the pointer untouched (a failed refresh never replaces a working kit) and report the best candidate's path.

### The final report

Gallery and one-pager scores per round, pointer status (`ready` or `draft` or untouched), kit path, renderer edits made (by file), the author's assumptions, obstacles, and the timing table: one line per step with its wall-clock duration. The agent reports stay in `RUN_DIR/reports/`.

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
- Scripts: [prefetch.py](../../agents/brand-kit/scripts/prefetch.py), [gate_check.py](../../agents/brand-kit/scripts/gate_check.py), [gate_decide.py](../../agents/brand-kit/scripts/gate_decide.py), [judge_context.py](../../agents/brand-kit/scripts/judge_context.py), [render_gallery.py](../../agents/brand-kit/scripts/render_gallery.py), [render_kit.py](../../agents/brand-kit/scripts/render_kit.py), [render.py](../../agents/brand-kit/scripts/render.py), [check_adherence.py](../../agents/brand-kit/scripts/check_adherence.py), [kit_validation.py](../../agents/brand-kit/scripts/kit_validation.py), [brand_cache.py](../../agents/brand-kit/scripts/brand_cache.py), [verify_logos.py](../../agents/brand-kit/scripts/verify_logos.py), [verify-logos.sh](../../agents/brand-kit/scripts/verify-logos.sh)
- Assets: [kit_base.css](../../agents/brand-kit/assets/kit_base.css), [gallery_spec.json](../../agents/brand-kit/assets/gallery_spec.json), [onepager_spec.json](../../agents/brand-kit/assets/onepager_spec.json)
