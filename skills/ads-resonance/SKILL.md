---
name: ads-resonance
description: Analyze ad performance and feed the learnings back into your Octave library — the resonance loop. Pulls performance data from Google Ads MCP, BigQuery Data Transfer, direct API, or manual paste; maps winners back to the source cards behind each ad variant; generates library update recommendations and a sales intelligence brief; writes falsifiable prediction cards and accumulates a calibration track record over time. Use when user says "analyze ad performance", "resonance loop", "score predictions", "evaluate my ads", or asks to turn ad performance into GTM intelligence. Do NOT use to build a new ad campaign — use /octave:ads instead.
argument-hint: "[--min-impressions N] [--min-clicks N] [--min-conversions N] [--mode smoke-test|ad-group|ad|full-resonance]"
---

# Octave Ads Resonance Loop — Performance → Library Intelligence

Turn ad performance data into GTM intelligence: pull performance from whichever source is available, map winners and losers back to the source cards that produced them, recommend library updates, brief the sales team on what language the market responds to, and write falsifiable prediction cards so the loop builds a verifiable track record over time.

**Companion skill**: `/octave:ads` builds the campaigns this loop analyzes. Campaigns generated there persist source cards to `~/.octave/source_cards/` (the data contract is defined in `/octave:ads` Step 2G and [source-cards.template.json](../ads/references/source-cards.template.json)), which unlocks this loop's strongest analysis path. The loop also works on campaigns created outside `/octave:ads` via reverse-inference.

**MCP Server**: Library updates (Step 3) require the Octave MCP server. Look for available MCP tools that match the Octave tool names (e.g., `update_entity`, `update_motion_playbook`). The MCP server prefix varies by workspace. If multiple Octave-like MCP servers are available and you're unsure which to use, ask the user which workspace to target.

---

**Output principles**: every output follows the shared principles — [presentation principles](../shared/presentation-principles.md) for visuals (the HTML dashboard, tables), [editorial rules](../shared/editorial-rules.md) for text (the brief, recommendations, prediction cards).

**Review pass**: before final delivery, run the preflight from [protocol.md](../shared/protocol.md) (em dashes, leaked internals, placeholders) over the text output. Any HTML dashboard generated in Step 6 takes the full protocol as a mandatory gate: it is not opened or delivered until the combined scorecard has printed.

## Step 1: Detect Performance Data Source

Performance data can come from four places, in order of preference:

1. **MCP** (live Google Ads / Meta / LinkedIn API via an installed MCP server) — real-time, but most likely to fail at runtime
2. **BigQuery Data Transfer Service** (~24h delayed managed pipeline) — the recommended default for read-only resonance analysis, no developer token approval required
3. **Direct API** (curl/Python against the Google Ads API, no MCP) — when the user has an approved developer token but no MCP installed
4. **Manual** (paste CSV / screenshot / verbal) — last resort

**Read `references/performance-data-sources.md` for setup instructions, smoke-test queries, table layouts, and the troubleshooting table.** That doc is the source of truth for everything in this section.

**Critical principle**: never tell the user "I can pull your data" without running a smoke test first. A path that *looks* available (the MCP tool exists, the dataset exists, the dev token is set) can still fail at query time. Probe first, then commit.

Walk through the four paths in order. For each one, first detect, then smoke-test. The first path that passes its smoke test wins — use it. If all four fail, fall through to manual.

#### Detection patterns

| Path | What to look for |
|------|------------------|
| 1 — MCP | MCP tools matching `google_ads`, `googleads`, `adwords`, `google_campaigns`, `meta_ads`, `facebook_ads`, `linkedin_ads` |
| 2 — BigQuery | A BigQuery MCP tool (`bigquery`, `bq`, `mcp__bigquery*`), OR the `bq` CLI on PATH and authenticated, OR a known dataset like `google_ads` containing `ads_Campaign_*` / `ads_CampaignBasicStats_*` tables |
| 3 — Direct API | The user mentions they have an approved developer token + a refresh token, but no MCP. Or earlier in the conversation they shared API credentials |
| 4 — Manual | Always available |

#### Path 1 — MCP smoke test

If a Google Ads MCP tool is detected, before promising data:

```
→ {google_ads_mcp}__list_accessible_customers()
```

If that succeeds, pick one accessible customer ID and run the simplest possible query:

```
→ {google_ads_mcp}__search(
    customer_id: "{id}",
    query: "SELECT customer.id, customer.descriptive_name FROM customer"
  )
```

**Interpret the result:**
- Success → Path 1 is good. Use it for all subsequent queries.
- `CUSTOMER_NOT_FOUND` + "missing authentication credential" → wrong `login-customer-id`. Tell the user the exact fix (set `GOOGLE_ADS_LOGIN_CUSTOMER_ID` to the MCC, not a sub-account) and fall through to Path 2.
- `DEVELOPER_TOKEN_NOT_APPROVED` "only approved for use with test accounts" → the developer token is in Test tier and cannot query production accounts. Tell the user they need to apply for Basic Access in API Center (~3 days) and fall through to Path 2.
- `invalid_scope` or 403 → ADC missing the `adwords` scope. Reference the Python refresh-token snippet in the data sources doc and fall through to Path 2.
- `404` on a versioned path → API version sunset. Note the current version (v21 as of 2026-04) and fall through to Path 2.

For all four failure modes, the message to the user should be one sentence: what failed, what the fix is, and "I'll try BigQuery next."

#### Path 2 — BigQuery smoke test

If a BigQuery MCP tool is available, list datasets and look for `google_ads` (or any dataset containing tables prefixed `ads_Campaign_`). If `bq` CLI is available, run:

```
bq ls --project_id=<project>
bq ls <project>:google_ads
```

If you find tables matching `ads_CampaignBasicStats_<MCC>`, run a **two-stage smoke test**. The first stage proves data exists and is fresh. The second stage proves the data is *meaningful* — that it'll actually drive useful resonance analysis, not just produce empty tables.

**Stage 1 — freshness probe:**

```sql
SELECT
  COUNT(*) AS row_count,
  MIN(_DATA_DATE) AS earliest,
  MAX(_DATA_DATE) AS most_recent
FROM `<project>.google_ads.ads_CampaignBasicStats_<MCC>`
WHERE _DATA_DATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
```

**Stage 2 — meaningful-data probe** (the ad-group-level CPC/CTR query). This is the most actionable single query at small spend and immediately exposes whether the data has signal worth analyzing.

**CRITICAL — dim-table snapshot trap.** `ads_AdGroup_<MCC>` and `ads_Campaign_<MCC>` are **daily-snapshotted dimension tables**, not static dim tables. Each ad_group_id has one row per `_DATA_DATE`. Joining to them without a snapshot-dedup step cartesian-explodes your totals: after N days the multiplier is N (or N² if you join both tables). See `references/performance-data-sources.md` § "Gotcha #4: Daily-snapshotted dim tables" for the full writeup. Every query in this skill that reads dim metadata must use the `ag_latest` / `c_latest` CTE pattern shown below — never JOIN the dim tables directly.

```sql
WITH
-- Latest snapshot of the dim tables (one row per ad_group_id / campaign_id).
-- Required: ads_AdGroup_* and ads_Campaign_* are daily-snapshotted.
-- Joining them raw cartesian-explodes totals. Never skip this CTE.
ag_latest AS (
  SELECT * FROM `<project>.google_ads.ads_AdGroup_<MCC>`
  QUALIFY ROW_NUMBER() OVER (PARTITION BY ad_group_id ORDER BY _DATA_DATE DESC) = 1
),
c_latest AS (
  SELECT * FROM `<project>.google_ads.ads_Campaign_<MCC>`
  QUALIFY ROW_NUMBER() OVER (PARTITION BY campaign_id ORDER BY _DATA_DATE DESC) = 1
)
SELECT
  c.campaign_name,
  ag.ad_group_name,
  COUNT(DISTINCT s._DATA_DATE) AS days_active,
  SUM(s.metrics_impressions) AS impressions,
  SUM(s.metrics_clicks) AS clicks,
  ROUND(SAFE_DIVIDE(SUM(s.metrics_clicks), SUM(s.metrics_impressions)) * 100, 2) AS ctr_pct,
  SUM(s.metrics_conversions) AS conversions,
  ROUND(SUM(s.metrics_cost_micros) / 1000000, 2) AS cost_usd,
  ROUND(SAFE_DIVIDE(SUM(s.metrics_cost_micros) / 1000000, SUM(s.metrics_clicks)), 2) AS cpc_usd
FROM `<project>.google_ads.ads_AdGroupBasicStats_<MCC>` s
JOIN ag_latest ag USING (customer_id, ad_group_id, campaign_id)
JOIN c_latest c USING (customer_id, campaign_id)
WHERE s._DATA_DATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY 1, 2
HAVING clicks > 5
ORDER BY cpc_usd DESC
```

**Stage 2b — mandatory sanity cross-check.** Immediately after running Stage 2, run this raw-stats-only query and verify the totals match:

```sql
SELECT
  ad_group_id,
  SUM(metrics_impressions) AS impressions_raw,
  SUM(metrics_clicks) AS clicks_raw
FROM `<project>.google_ads.ads_AdGroupBasicStats_<MCC>`
WHERE _DATA_DATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY 1
```

For each `ad_group_id` present in both results, `clicks_raw` and `impressions_raw` must equal the Stage 2 values **exactly**. If any row differs, **stop the loop and report a dim-join inflation bug** — do not proceed with analysis. The most likely cause is that someone modified the Stage 2 query template and dropped the `ag_latest` / `c_latest` CTE pattern. The fix is to restore the CTEs. The second most likely cause is a new dim table being introduced upstream with the same daily-snapshot shape. Either way, the mismatch is a hard stop: inflated totals will silently corrupt every downstream conclusion (CPC comparisons, prediction cards, library recommendations).

**Interpret the result:**
- Stage 1 returns rows > 0 and `most_recent` within the last 2 days → freshness OK, continue to Stage 2.
- Stage 2 returns ≥ 2 ad groups with `clicks > 5` → Path 2 is good. Use the BigQuery queries from `references/performance-data-sources.md` for all subsequent fetches. Note in your report what the data window covers and how many ad groups have meaningful volume.
- Stage 2 returns 0 or 1 rows with meaningful volume → the data is fresh but too thin for cross-ad-group comparisons. Tell the user explicitly: "I have data, but only N days / N ad groups have enough clicks to draw real conclusions. I can run the loop in **smoke test mode** (verifies the pipes work, conclusions are unreliable) or **partial mode** (only report findings I can stand behind). Which?"
- Stage 1 returns rows == 0 or `most_recent` is more than 2 days old → the transfer exists but has stalled or hasn't backfilled yet. Tell the user and offer to either trigger a backfill (`bq mk --transfer_run ...`) or fall through to Path 3 / Path 4.
- Permission denied on either query → the calling identity (user or service account) lacks `roles/bigquery.dataViewer` on the dataset. Tell the user the exact fix and fall through.
- No matching dataset/tables → Path 2 isn't set up yet. **Offer to walk the user through setup interactively** (this is the first-run path). The full setup steps are documented in `references/performance-data-sources.md` § "Path 2: BigQuery Data Transfer Service". Read that section and execute it step by step with the user — enable the APIs, create the dataset, create the transfer in the BigQuery console (this requires the user to click through the OAuth grant), trigger a backfill, then re-run the smoke test once data starts landing. Setup is ~10 minutes of clicks plus ~17 hours for the full 30-day backfill (most-recent days land first, so analysis can begin within ~30 min). Do not skip to Path 3 or Path 4 unless the user explicitly declines the setup.

#### Path 3 — Direct API smoke test

If the user has shared API credentials earlier in the conversation (developer token + refresh token + client id/secret), or has a `~/adc-google-ads.json` ADC file, you can hit the API directly with `curl` or Python. Same smoke test as Path 1: mint an access token from the refresh token, hit `listAccessibleCustomers`, then run a `customer` query against an accessible ID.

Same failure modes as Path 1 (login-customer-id, dev token tier, scope, API version) — see the data sources doc for the curl invocations.

#### Path 4 — Manual

If all programmatic paths fail (or the user explicitly requests manual), ask:

```
AskUserQuestion({
  questions: [{
    question: "How would you like to provide ad performance data?",
    header: "Performance Data",
    options: [
      {
        label: "Paste a CSV or table",
        description: "Paste performance data from your ad platform (needs: variant/headline, impressions, clicks, conversions)"
      },
      {
        label: "Paste a screenshot",
        description: "Share a screenshot of your ad platform dashboard — I'll extract the metrics"
      },
      {
        label: "Summarize verbally",
        description: "Tell me which variants won and lost, with approximate numbers"
      },
      {
        label: "Skip — I'll come back later",
        description: "Run the resonance loop when you have performance data"
      }
    ],
    multiSelect: false
  }]
})
```

#### What to fetch (any path)

Whichever path wins, fetch these per-variant metrics so the resonance map (Step 2) has what it needs:
- Impressions
- Clicks / CTR
- Conversions / conversion rate
- Cost per click (CPC) / cost per conversion (CPA)
- Ad creative content (RSA headlines and descriptions for matching back to source cards)
- Quality Score (Google) or Relevance Score (Meta/LinkedIn) if available

Match fetched data back to the variants generated by `/octave:ads` (its Step 3) by **headline text** (most reliable across paths), then by ad set name, then by campaign ID if the user stored it during export.

## Step 2: Map Performance Back to Source Cards

This is the core of the resonance loop. Before generating the map, decide which **analytical mode** the data supports — the wrong mode produces confident-sounding noise. Then decide whether the campaign was generated by `/octave:ads` (source cards exist) or is legacy/external (source cards must be reverse-inferred).

#### 2.1: Pick the analytical mode based on volume

Different volumes stabilize different metrics. **Volume — not spend — is what determines statistical confidence.** $100/day on $50 CPC enterprise keywords is 2 clicks; $100/day on $0.50 CPC long-tail keywords is 200 clicks. Same dollar amount, totally different reliability. Use the volume thresholds below as the primitives. Spend amounts are listed only as rough orientation.

**Read this table and pick the most conservative mode that fits the *unit being compared*.**

| Mode | Volume threshold (the actual gate) | Rough spend orientation | What's stable | What's still noise |
|---|---|---|---|---|
| **Smoke-test** | <500 impressions OR <20 clicks total in the window across all units | < $100/day | Almost nothing | Conversions, CTR, CPC at any level |
| **Ad-group** | ≥2 ad groups each with **500+ impressions and 20+ clicks** in the window | $100–$500/day | Ad-group-level CTR and CPC | Conversion rate at any level, ad-level metrics, CPA |
| **Ad** | Per-ad: **1,000+ impressions and 30+ clicks** for the ad in question | $500–$2,000/day | Ad-level CTR (only for ads meeting the threshold) | Conversion rate, CPA, ad-level CPC for low-volume ads |
| **Full resonance** | All ad-mode thresholds met **+ 30+ total conversions** in the window | > $2,000/day | All of the above + ad-level conversion rate | Headline-level attribution (Google does not expose this) |

The gates are AND, not OR. An ad with 5,000 impressions and 4 clicks doesn't qualify for ad mode (clicks too low). An ad group with 50,000 impressions but only 10 conversions doesn't qualify for full resonance (conversions too low).

**Default thresholds can be overridden** at runtime if the user explicitly says they know their data. Accept arguments like:
- `--min-impressions 200` (lowers the per-unit impression floor)
- `--min-clicks 10`
- `--min-conversions 10`
- `--mode ad-group` / `--mode ad` / `--mode full-resonance` (force a specific mode regardless of volume)

When the user passes an override, **state in the report what was overridden and to what value**, so the user can interpret the confidence accordingly. Do not silently use looser thresholds than the data supports.

**Hard rules — apply regardless of mode:**

1. **Never claim a "winning" or "losing" variant from N < 30 conversions** unless the user has explicitly overridden `--min-conversions`. State the conversion data, but frame any conclusion as "early signal, needs more volume to validate." A single conversion is correlation, not causation.
2. **Always report the data window, total impressions/clicks/conversions, and selected mode at the top of the resonance map.** This calibrates the reader for how much weight to give the conclusions.
3. **CPC gaps between ad groups are usually the biggest finding at small spend.** A 3x+ CPC delta between two ad groups in the same account targeting the same persona is a "rework or kill" signal even with no conversion data, because it reveals a Quality Score / keyword-creative match problem that no amount of creative iteration will fix.
4. **If the smoke test (Step 1 Stage 2) returned only 1 ad group with meaningful volume, you cannot run a real resonance loop.** Report what you have, label it explicitly as "single-ad-group early signal," and offer to re-run when more data is available.
5. **Units below the threshold for the chosen mode get N/A confidence and are excluded from winners/losers tables.** They can appear in an "FYI — insufficient volume" section, but never in the actionable findings.

Pick the mode now and **state it explicitly at the top of the resonance map output** so the user knows the confidence floor before reading the findings.

#### 2.2: Decide whether source cards exist

Two paths into Step 2:

**Path A — Campaign was generated by `/octave:ads`** (source cards exist):

Campaigns generated by `/octave:ads` automatically persist source cards to `~/.octave/source_cards/<workspace_slug>/<campaign_slug>.json` (its Step 2G), with final headlines populated at creative time (its Step 3C). The file contains the campaign metadata, the full source cards, and a `headlines_by_variant` mapping from each variant to the actual headlines that were generated.

To use Path A in the resonance loop:
1. Scan `~/.octave/source_cards/` for subdirectories. Each subdirectory is a workspace slug.
2. Inside each, look at every campaign file. Read the `headlines_by_variant` field.
3. Match each headline string against the headlines observed in BigQuery (via the per-ad query in `references/performance-data-sources.md`). Match by exact headline text — this is reliable because Google preserves headline strings verbatim.
4. When a match is found, you can trace forward from the BigQuery row → the headline → the variant type → the source card → the derivation chain → the original prospect language or proof point. This is the strong direction of inference.

If no source card files exist (the campaigns running in BigQuery weren't generated by this skill — e.g., they were created in the Google Ads UI directly), fall through to Path B (reverse-inference).

**Path B — Legacy or externally created campaign** (no source cards):
For everything currently running in production that wasn't generated by this skill, the resonance loop has to **reverse-infer** the variant type and source card from the headlines themselves. This is a much weaker form of analysis — you're looking at the output and guessing what the brief was. Be honest about this in the report: a winning headline tells you what *worked*, but without the original brief you can only speculate about *which underlying angle made it work*.

The reverse-inference process for legacy campaigns:

1. **Cluster headlines by inferred variant type.** Read the headline pool of each ad and tag it with the closest matching variant type used by `/octave:ads` (pain-focused, outcome-focused, social-proof, competitive, question-based, data-driven, status-quo, authority, brand-only). Most legacy ads will be brand-only or generic-benefit; that's a finding in itself.
2. **Look at headline structure and pinning.** A pinned HEADLINE_1 tells you what the ad creator believed was the lead message. A pool of 15 headlines with no pinning tells you Google was given full optimization latitude. A pool of 5 brand headlines tells you the creator never tested angles at all.
3. **Trace winners backward to *speculative* source cards.** If "Still Prepping Audits By Hand?" wins, the implicit Pain Language Audit might be: emotional core = visceral frustration with manual compliance work; specific dysfunction = audit preparation as an unautomated weeks-long process; data tier = INFERRED (no underlying field finding cited). Mark these reverse-inferred cards clearly so the user knows they're hypotheses, not derivations.
4. **The library-update recommendations are weaker in Path B.** You're recommending changes to personas/Motion ICP narratives based on what *appears* to resonate from external creative — not from creative whose grounding you can verify. Lower the confidence tier on every recommendation by one level (HIGH → MEDIUM, MEDIUM → LOW).
5. **Recommend that the next campaign go through `/octave:ads`** so the next loop iteration can use Path A. The strongest version of the resonance loop requires that the campaign and the analysis share a vocabulary.

#### 2.3: Build the resonance map

For each variant with performance data (Path A) or each ad group (Path B at small spend), produce the map. The template adapts to the mode picked in 2.1 — at small spend, there are no per-variant winners to list; the unit of comparison is ad groups.

**Standard template (ad mode or full resonance mode):**

```markdown
## Resonance Map

**Data window**: {start} – {end} ({N} days) | **Spend**: ${X} | **Total impressions**: {N} | **Total conversions**: {N}
**Mode**: {smoke-test | ad-group | ad | full resonance}
**Path**: {A — source cards exist | B — reverse-inferred from headlines}

### Winners (top performing variants)

| Variant | Type | Ad Set | CTR | Conv Rate | Source Card | Derivation Chain | Confidence |
|---------|------|--------|-----|-----------|-------------|-----------------|------------|
| "Still Prepping Audits By Hand?" | Pain-focused | VP Eng × FinServ | 3.2% | 1.8% | Pain Language Audit | Finding F-123 (call w/ Acme, 2 weeks ago) → emotional core: "fear of failed audits" → headline | HIGH |

**What this tells us**: The pain of manual audit prep resonates more strongly than the cost-of-inaction framing for VP Engineering personas. The winning language traces to a specific finding from a real sales call — this isn't just ad performance, it's market validation of a pain point.

### Underperformers (below-average variants)

| Variant | Type | Ad Set | CTR | Conv Rate | Source Card | Hypothesis for Underperformance | Confidence |
|---------|------|--------|-----|-----------|-------------|-------------------------------|------------|
| "Every Hire Starts From Zero" | Status quo | VP Eng × FinServ | 0.4% | 0.1% | Compounding Cost Model | The compounding narrative may be too abstract for search intent — buyers searching for solutions want immediate pain acknowledgment, not long-term projections | MEDIUM |
```

**Small-spend template (ad-group mode):**

When the data only supports ad-group comparisons, lead with the CPC gap finding instead of variant-level analysis:

```markdown
## Resonance Map

**Data window**: {start} – {end} ({N} days) | **Spend**: ${X} | **Total conversions**: {N}
**Mode**: ad-group (spend too low for ad-level conclusions)
**Path**: {A | B}

### Ad Group Comparison

| Ad Group | Campaign | Impr | Clicks | CTR | Conv | Cost | CPC | Confidence |
|---|---|---|---|---|---|---|---|---|
| VP Eng × Enterprise FinServ | Compliance Automation Q1 | 1,000 | 60 | 6.00% | 1 | $180 | $3.00 | HIGH |
| Director Compliance × Mid-Market | Compliance Automation Q1 | 400 | 15 | 3.75% | 0 | $225 | $15.00 | HIGH |

**Key finding**: The Director Compliance ad group costs ~5x more per click than the VP Eng ad group and converts at 0% vs ~1.5% over the window. This is a Quality Score / keyword-creative match gap, not a creative gap alone — even rewriting the ads will not close a CPC delta this large without keyword changes.

**Actionable**: Pause or rework the Director Compliance ad group. Move budget to VP Eng. Expected effect: ~5x more clicks per dollar at the same total spend.

### Per-ad observations (FYI only — too noisy to act on)

[List ads with their headlines and metrics, but explicitly do NOT rank them or label winners/losers. The ad-group finding is the actionable one.]
```

Confidence tiers for the resonance map:
- **HIGH**: 14+ days of data, 1,000+ impressions on the unit being compared, the metric in question is one the spend tier supports as stable
- **MEDIUM**: 7–14 days, 500+ impressions, OR the metric is borderline for the spend tier
- **LOW**: < 7 days, < 500 impressions, OR the metric is one the spend tier explicitly does not support
- **N/A**: Unit has < 100 impressions or < 5 clicks — Google has not given it a fair test, do not include in winners/losers tables

## Step 3: Generate Library Update Recommendations

Based on the resonance map, generate specific, actionable recommendations for the Octave library:

```markdown
## Library Update Recommendations

### Persona Updates
| Persona | Field | Current | Recommended Update | Evidence |
|---------|-------|---------|-------------------|----------|
| VP Engineering | Primary pain point | "Tool sprawl across compliance stack" | "Manual audit preparation that doesn't scale" | Pain-focused variant at 3.2% CTR vs status-quo at 0.4% — manual process pain resonates 8x stronger than tool sprawl framing |

### Playbook Updates
| Playbook | Update | Evidence |
|----------|--------|----------|
| Enterprise FinServ | Add discovery opener: "How are you handling audit prep today?" | Derived from winning headline "Still Prepping Audits By Hand?" — 3.2% CTR proves this question self-selects the right buyer |

### Value Prop Updates
| Value Prop | Update | Evidence |
|------------|--------|----------|
| Compliance Automation | Reframe from "reduce risk" to "eliminate manual audit prep" | Pain-focused (manual process) outperformed authority (risk reduction) by 4x in CTR |
```

For each recommendation, ask the user whether to apply it:

```
AskUserQuestion({
  questions: [{
    question: "Apply these library updates?",
    header: "Library Updates",
    options: [
      {
        label: "Apply all",
        description: "Update personas and Motion Playbook narratives based on ad performance evidence"
      },
      {
        label: "Let me pick",
        description: "Review each recommendation individually"
      },
      {
        label: "Save as findings only",
        description: "Don't update the library yet — save these as findings for later review"
      },
      {
        label: "Skip",
        description: "Review only, no changes"
      }
    ],
    multiSelect: false
  }]
})
```

If they choose to apply updates, use the appropriate MCP tools. For Motion Playbook narrative edits (Strategic narrative, Benefits and impacts, Pains and consequences sections inside a Motion ICP cell), use `update_motion_playbook`:
```
→ {octave_mcp}__update_entity(oId: "{persona_oId}", instructions: "{update}")
→ {octave_mcp}__update_motion_playbook(motionPlaybookOId: "{motion_playbook_oId}", instructions: "{update}")
```

## Step 4: Feed Winning Language to Sales

Generate a **Sales Intelligence Brief** — a summary designed for sales teams showing what language the market is responding to:

```markdown
## Sales Intelligence Brief — From Ad Performance

### Winning Messages (use these in conversations)
| Message | Where It Won | Suggested Sales Use |
|---------|-------------|-------------------|
| "Still prepping audits by hand?" | Google Search, 3.2% CTR, VP Eng | Discovery opener — ask this in the first 2 minutes |
| "Audit prep: 3 weeks → 2 days" | Google Search, 2.8% CTR, VP Eng | Proof point framing — lead with this specific transformation |

### Messages That Didn't Land (avoid or reframe)
| Message | Where It Failed | Why | Alternative |
|---------|----------------|-----|------------|
| "Every hire starts from zero" | Google Search, 0.4% CTR | Too abstract for search intent | Reframe to concrete: "New hires spend 6 weeks learning your compliance process" |

### Persona Insight
{Persona}: The ad data confirms this buyer responds to **immediate, tangible process pain** over **strategic risk framing**. Lead with "how are you doing X today?" not "what happens if X breaks?"
```

## Step 5: Generate Next Campaign Recommendations

Based on what worked, recommend the next campaign iteration:

```markdown
## Next Campaign Recommendations

### Double Down
- **Pain-focused variants won across all ad sets** → Next campaign: allocate 60% of budget to pain-focused variants, test 3 pain sub-angles (manual process, time waste, audit failure risk)
- **VP Engineering was the top-converting persona** → Consider increasing bid/budget for this ad set

### Test Next
- **Question-based variant showed high CTR but low conversion** → The question stops the scroll but the landing page may not match. Test a dedicated landing page that mirrors the question framing.
- **No data on Meta/LinkedIn yet** → Repurpose the top 3 Google winners as Meta ads to test cross-platform resonance

### Retire
- **Status quo / cost of inaction variants underperformed everywhere** → Retire this variant type for this persona. The Compounding Cost Model may apply better to executive personas (CFO/CEO) who think in longer time horizons.
```

## Step 6: Predictions & Calibration

**This step turns the resonance loop from a one-shot analyzer into an iterative scientific instrument with a verifiable track record.** Read `references/prediction-cards.md` for the full schema, prediction types, persistence model, and the empirical lessons from prior backtests. That doc is the source of truth for everything in this section.

The principle: at the end of every loop run, write down explicit, falsifiable predictions about what specific metrics will do over a specific window. The next time the loop runs, evaluate the previous predictions against actual data and report a track record. Over time, calibration accumulates and the loop tunes its own confidence based on its own history of being right and wrong.

#### 6.1: Read previous predictions FIRST (before generating new findings)

At the start of every loop run, before producing any new resonance map:

**Determine the MCC ID and today's date** (the loop needs both to find the right file and evaluate predictions):
- The MCC ID is the numeric suffix on the BigQuery table names. Run `bq ls <project>:<dataset>` and look for tables matching `ads_Campaign_<digits>`. The digits are the MCC ID. If multiple MCCs are present, ask the user which to analyze.
- Today's date in UTC: run `date -u +%Y-%m-%d` via the Bash tool, OR use the `currentDate` value from the system context if available.

**Then read previous predictions:**

1. Read `~/.octave/predictions/<MCC_ID>.json`. If the file doesn't exist, this is the first run for this account — skip to 6.3 (no previous predictions to evaluate). On first run, copy `references/prediction-cards.template.json` to the destination path as the starter file.
2. Find all cards with `status: PENDING` whose `evaluation_window` end date is on or before today.
3. For each such card, read its `evaluation_sql` field — the loop generates SQL queries at prediction-creation time and stores them in the card so re-evaluation is deterministic. Substitute the placeholders (`<project>`, `<dataset>`, `<MCC>`, `<window_start>`, `<window_end>`) with the actual values, then run via `bq query`.
4. Apply the card's `confirms` / `refutes` / `inconclusive` conditions to the query result. Update the card with one of: `CONFIRMED`, `REFUTED`, `INCONCLUSIVE_FAVORABLE`, `INCONCLUSIVE_UNFAVORABLE`, or leave as `PENDING` with a `partial_evaluation` block if the window data isn't fully landed yet (the BQ data only goes through yesterday — anything past that is `PENDING`).
5. **Apply the refresh-window rule**: if the prediction's `evaluation_window` end date is within the last `refresh_lag_days` (typically 7), set `tentative: true` on the card regardless of which resolution status you assigned. Both CONFIRMED and REFUTED can flip inside the refresh window — late-reported data can push rate metrics in either direction (CTR can drop if impressions grow faster than clicks; conversion rate can rise if late conversions come in; CPC can change as total cost adjusts). Only set `tentative: false` once the evaluation window has aged past `window_end + refresh_lag_days`. Tentative cards are re-evaluated on every subsequent run until they finalize. See `references/prediction-cards.md` § "Common pitfalls" #7 for the full rule and the empirical backtest evidence behind it.
5. Write `evaluated_at`, `evaluated_against`, and `evaluation_notes` for each updated card.
6. Execute the card's `action_if_<status>` instructions — most often this means promoting/demoting source cards in the library, NOT changing campaigns autonomously.

#### 6.2: Show the user the "Previous Predictions Evaluated" panel

Before showing the new resonance map, show the user a summary of what the last run's predictions said and how they resolved:

```markdown
## Previous Predictions Evaluated

| ID | Type | Claim | Status | Notes |
|---|---|---|---|---|
| P-2026-04-03-004 | cpc-efficiency-gap | CPC gap holds at >= 3x | ✅ CONFIRMED | Held at ~5x via a new ad group that didn't exist at prediction time |
| P-2026-04-03-002 | regression-to-mean | Pilot ad group conv rate regresses to 0-3% | 🟡 INCONCLUSIVE_FAVORABLE | Volume gate failed (8 clicks); directional signal supports the prediction |
| P-2026-04-03-001 | regression-to-mean | Pilot ad group CTR regresses to 4-6% | 🟡 INCONCLUSIVE_UNFAVORABLE | Volume gate failed; CTR moved away from prediction |
| P-2026-04-03-003 | exposure-projection | Director Compliance reaches 30 clicks in 7 days | ⏳ PENDING | 4 of 7 days available; on track to refute |

**Track record so far**: 1 confirmed / 0 refuted / 2 inconclusive (1 favorable, 1 unfavorable) / 1 pending
**Strongest type**: cpc-efficiency-gap (1/1 confirmed)
```

This panel is the user-facing magic. It builds trust by being honest about what the loop got right and wrong last time.

#### 6.3: Generate new prediction cards

After producing the new resonance map (Steps 2–5), generate **3–6 new prediction cards** covering the strongest claims in the current run. Read `references/prediction-cards.md` for the full taxonomy of prediction types and the rules for each.

Hard rules for prediction generation:

1. **Every prediction must be a SQL query that returns a boolean.** Vague claims ("the pain framing will keep winning") are not predictions.
2. **Every prediction must specify CONFIRMS, REFUTES, and INCONCLUSIVE conditions** as precise queries the next loop run can execute without additional human input.
3. **Prefer structural predictions over unit-specific predictions** (the structural-over-unit rule). The first backtest empirically validated this: structural predictions generalized to brand new units, unit-specific predictions failed when the named unit lost volume between windows. See `references/prediction-cards.md` § "The structural-over-unit rule" for examples.
4. **Always generate one `field-stability` prediction per run.** It's a meta-prediction about whether the cast of ad groups will change, and it's the first signal the loop has about whether to weight structural vs unit-specific claims more heavily on the next run.
5. **Don't generate `regression-to-mean` predictions for units below the volume gate.** Compute `(current run rate clicks/day) * 7 >= volume_gate`. If false, generate an `exposure-projection` instead — those can be confirmed even at low volume.
6. **Read the calibration block before generating new predictions, and apply self-tuning rules deterministically.** Don't eyeball the hit rate — apply these exact rules, in order:
   - **If a prediction type has fewer than 10 resolved cards** (CONFIRMED + REFUTED + INCONCLUSIVE_FAVORABLE + INCONCLUSIVE_UNFAVORABLE combined), use its default confidence and do not adjust. Small N is not a basis for tuning.
   - **If a prediction type has 10+ resolved cards and hit rate (CONFIRMED / resolved) ≥ 80%**, promote its default confidence by one tier (LOW → MEDIUM → HIGH). Surface findings of this type as "high-trust" in the resonance map.
   - **If a prediction type has 10+ resolved cards and hit rate ≤ 30%**, demote its default confidence by one tier and add a caveat to all findings of this type.
   - **If a prediction type has 10+ resolved cards and hit rate is 0%**, stop generating that type entirely on this run. Note in the calibration `lessons` that the type has been retired.
   - **If INCONCLUSIVE_FAVORABLE outnumbers INCONCLUSIVE_UNFAVORABLE by 3:1 or more across 10+ inconclusive cards of the same type**, the volume gate is too strict for that type. Note this in `lessons` and consider relaxing the gate (with user confirmation) on the next run.
   - **If a type has 10+ resolved with hit rate between 30% and 80%**, no adjustment — the type is calibrated reasonably.

   These rules are deterministic so two future LLM sessions reading the same calibration block will make the same tuning decisions. Always note in the loop output what tuning was applied (e.g., "cpc-efficiency-gap promoted from MEDIUM to HIGH based on 12/14 hit rate").

For each new card, fill in every field of the schema (see `references/prediction-cards.md` § "The prediction card schema"). Required fields: `id`, `generated_at`, `generated_by`, `mode`, `is_structural`, `claim`, `type`, `evaluation_window`, `evidence_at_prediction`, `confirms` (natural language), `refutes` (natural language), `inconclusive` (natural language), `evaluation_sql` (the parameterized SQL query that produces the data needed to apply the confirm/refute/inconclusive conditions — uses placeholders `<project>`, `<dataset>`, `<MCC>`, `<window_start>`, `<window_end>`), `confidence`, `rationale`, `action_if_confirmed`, `action_if_refuted`, `action_if_inconclusive`, `status: PENDING`.

The `evaluation_sql` field is what makes the loop deterministic across runs. Without it, the next session has to interpret the natural-language `confirms` field and reconstruct a query — different sessions may write different queries. Always emit the SQL at generation time so re-evaluation is mechanical, not interpretive. See `references/prediction-cards.template.json` for example schemas with `evaluation_sql` filled in.

#### 6.4: Update the calibration block and write the file

After all evaluation and generation is complete, recompute the `calibration` block at the bottom of the JSON file:
- `total_predictions`, `evaluated`, `pending`, `confirmed`, `refuted`, `inconclusive_favorable`, `inconclusive_unfavorable`
- `directional_hit_rate`: (confirmed + inconclusive_favorable) / (resolved predictions)
- `by_type`: per-prediction-type breakdown with hit rates
- `lessons`: append any new lessons learned from this run (especially if a previously confirmed type just got refuted, or vice versa)

Write the file back to `~/.octave/predictions/<MCC_ID>.json`. Include a brief mention in the loop's user-facing output: "Updated prediction track record at `~/.octave/predictions/<MCC_ID>.json` — N new predictions generated, evaluate by [date]."

#### 6.5: Show upcoming evaluation dates

Tell the user when the next meaningful prediction resolution will occur:

```markdown
## Upcoming Prediction Evaluation Dates

| Earliest evaluation | Predictions resolving |
|---|---|
| 2026-04-13 | P-2026-04-07-001 (CPC gap), P-2026-04-07-002 (CPC tier distribution), P-2026-04-07-003 (VP Eng ad group reaches 100 clicks) |
| 2026-04-13 | P-2026-04-07-004 (conversions reach 5), P-2026-04-07-005 (field stability) |

Re-run `/octave:ads resonance` on or after 2026-04-13 to see how these resolved.
```

This gives the user a reason to come back. It's also a hint for setting up `/schedule` (see "Scheduling" in `references/prediction-cards.md`).

#### 6.6: Offer HTML output

After the chat-markdown resonance map, library updates, sales brief, next-campaign recommendations, and prediction cards have been generated, offer to also produce self-contained HTML reports for longitudinal consumption:

```
AskUserQuestion({
  questions: [{
    question: "Generate HTML reports alongside the chat output?",
    header: "HTML reports",
    options: [
      { label: "Both reports", description: "Resonance report (this run's findings) + Prediction dashboard (full calibration track record)" },
      { label: "Resonance report only", description: "Self-contained HTML of this run's findings, saved to ~/Desktop/" },
      { label: "Prediction dashboard only", description: "Self-contained HTML showing all active and resolved predictions with calibration stats, saved to ~/Desktop/" },
      { label: "Skip", description: "Chat output is enough" }
    ],
    multiSelect: false
  }]
})
```

- **Resonance report**: follow `references/resonance-report-template.md`. Save to `~/Desktop/resonance-report-<workspace-slug>-<YYYY-MM-DD>.html`.
- **Prediction dashboard**: follow `references/prediction-dashboard-template.md`. Save to `~/Desktop/prediction-dashboard-<workspace-slug>-<YYYY-MM-DD>.html`. Reads from `~/.octave/predictions/<MCC_ID>.json`.

Both are styled HTML for internal/stakeholder consumption; apply the workspace company's brand kit per [brand-kit-usage.md](../shared/brand-kit-usage.md) if one is available, falling back to the template's own style otherwise.

Both reports are self-contained single HTML files with inline CSS and inline SVG charts — no external JS, no external images, only Google Fonts via CDN. They work offline after first load, print cleanly, and can be shared as a single file attachment.

Tell the user the path(s) after generating and suggest opening with `open <path>` (macOS) or double-click.

#### 6.7: Failure modes

If the loop cannot read or write the predictions file (permissions, disk full, etc.):
- Continue with the rest of the resonance loop normally
- Tell the user clearly: "Unable to read/write prediction cards at `~/.octave/predictions/<MCC_ID>.json`. Calibration tracking is disabled for this run."
- Do NOT try to recreate the file from scratch (might destroy history)
- Do NOT proceed silently without telling the user the calibration system is broken

If the schema version of an existing file is NEWER than what the current loop knows about (current: v0.2):
- Refuse to write (would lose information from a future schema)
- Read PENDING predictions if possible, evaluate them, but do not append new predictions
- Tell the user the loop and the file are out of sync

---
