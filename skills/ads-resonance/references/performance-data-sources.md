# Ad Performance Data Sources

This reference covers the four ways the Resonance Loop (Step 6) can pull ad performance data, in order of preference. The SKILL detects what's available and falls through this list automatically.

| Priority | Source | Freshness | Setup effort | Best for |
|---------|--------|-----------|--------------|----------|
| 1 | **MCP** (live Google Ads API via `google-ads-mcp`) | Real-time | High (OAuth + dev token tier) | Fresh data, mutating later |
| 2 | **BigQuery Data Transfer Service** | ~24h delayed | Low (~10 min setup, no token approval) | Read-only analysis, the default for resonance loops |
| 3 | **Direct API** (curl/Python, no MCP) | Real-time | Medium (still needs dev token) | Scripted pipelines, MCP not installed |
| 4 | **Manual** (paste CSV/screenshot/verbal) | N/A | Zero | Last resort, validating the loop end-to-end |

The loop should always pick the highest available path, but **smoke-test before promising data**. A path that "looks available" (the MCP tool exists, the dataset exists) can still fail at query time. Always run a minimal probe query first.

---

## Path 1: MCP (Live Google Ads API)

The fastest path *if* it's already configured. Detection patterns: MCP tools matching `google_ads`, `googleads`, `adwords`, `google_campaigns`.

### Smoke test

Before telling the user "I can pull your data," run:

```
{google_ads_mcp}__list_accessible_customers()
```

Then for each accessible customer ID, attempt the simplest possible query:

```sql
SELECT customer.id, customer.descriptive_name, customer.manager
FROM customer
```

If `list_accessible_customers` works but the search query fails with `CUSTOMER_NOT_FOUND` + "Request is missing required authentication credential", the `login-customer-id` is wrong (see Troubleshooting). If it fails with `DEVELOPER_TOKEN_NOT_APPROVED`, the developer token is in Test tier and cannot query production accounts (see Troubleshooting). In either case, fall through to Path 2.

### Setup (if user wants to install it)

Install the official server published by the Google Ads Developer Relations team:

```json
"google-ads-mcp": {
  "command": "pipx",
  "args": ["run", "--spec", "git+https://github.com/googleads/google-ads-mcp.git", "google-ads-mcp"],
  "env": {
    "GOOGLE_APPLICATION_CREDENTIALS": "/Users/<you>/adc-google-ads.json",
    "GOOGLE_PROJECT_ID": "<your-gcp-project>",
    "GOOGLE_ADS_DEVELOPER_TOKEN": "<your-developer-token>",
    "GOOGLE_ADS_LOGIN_CUSTOMER_ID": "<your-MCC-customer-id-no-dashes>"
  }
}
```

The credentials file at `GOOGLE_APPLICATION_CREDENTIALS` must be an Application Default Credentials user-credentials JSON in this exact shape:

```json
{
  "client_id": "...",
  "client_secret": "...",
  "refresh_token": "...",
  "type": "authorized_user"
}
```

The refresh token must be authorized for the `https://www.googleapis.com/auth/adwords` scope. The cleanest way to mint one: create a Desktop OAuth client in GCP, download the client_secret JSON, and run:

```python
from google_auth_oauthlib.flow import InstalledAppFlow
flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json",
    scopes=["https://www.googleapis.com/auth/adwords"],
)
creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")
print(creds.refresh_token, creds.client_id, creds.client_secret)
```

A standard `gcloud auth application-default login` does **not** include the `adwords` scope and will not work — even though the resulting file looks identical.

### Why this path is risky in practice

Real users hit four walls in order:
1. ADC missing the `adwords` scope → `invalid_scope`
2. Wrong `GOOGLE_ADS_LOGIN_CUSTOMER_ID` (set to a sub-account, a closed account, or an account the OAuth user can't access) → `CUSTOMER_NOT_FOUND`
3. Developer token still in Test tier → `DEVELOPER_TOKEN_NOT_APPROVED` (every production account)
4. API version sunsets without warning (v18 → 404 by 2026; current is v21)

For users without an approved Basic-tier developer token, **Path 2 is dramatically faster to success.**

---

## Path 2: BigQuery Data Transfer Service (recommended default)

A managed Google service that pushes Google Ads data into a BigQuery dataset on a schedule. **No developer token approval required.** No OAuth scope wrangling. Setup takes ~10 minutes and works for any Google account that already has Ads access.

This is the right path for most resonance loops because:
- Resonance analysis is retrospective ("what worked over the last 30 days") — a 24h delay is irrelevant
- It bypasses the developer-token-tier wall that blocks most new users
- BigQuery is queryable from anywhere: `bq` CLI, BigQuery MCP, direct REST API, dbt, Looker

### Detection

The skill should consider Path 2 available if any of these are true:
- A BigQuery MCP server is installed (tools matching `bigquery`, `bq`, `mcp__bigquery*`)
- The `bq` CLI is available on PATH and the user is authenticated (`bq ls` returns datasets)
- A dataset exists in any accessible GCP project containing tables matching `ads_Campaign_*`, `ads_CampaignBasicStats_*`, `ads_AdGroup_*`, `ads_Ad_*`, etc.

### Smoke test

```
bq ls --project_id=<project> <dataset>
```

If you see tables matching `ads_Campaign_<MCC>` and `ads_CampaignBasicStats_<MCC>`, the transfer is set up and data is landing. Then probe with:

```sql
SELECT COUNT(*) FROM `<project>.<dataset>.ads_CampaignBasicStats_<MCC>`
WHERE _DATA_DATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
```

If the count is zero, the transfer config exists but hasn't completed its first run yet. Fall through to Path 4 with a note that data will be available within ~24h.

### Setup (if user wants to enable it)

Google's official docs for this service: **https://cloud.google.com/bigquery/docs/google-ads-transfer**

Summary of the steps:

```bash
# 1. Enable APIs
gcloud services enable bigquery.googleapis.com bigquerydatatransfer.googleapis.com --project=<PROJECT>

# 2. Create destination dataset
bq --location=US mk --dataset <PROJECT>:google_ads
```

3. Create the transfer in the BigQuery console (the OAuth grant for the Data Transfer Service is easiest there): https://console.cloud.google.com/bigquery/transfers
   - Source: Google Ads
   - Destination dataset: `google_ads`
   - Customer ID: the **MCC (manager) account ID** with no dashes — this pulls the manager + all sub-accounts in one transfer
   - Refresh window: 7 days (see "Refresh window vs backfill" below)
   - Schedule: daily

4. Trigger a backfill so you don't wait 24h for the first run:
   ```bash
   bq mk --transfer_run \
     --start_time=$(date -u -v-30d +%Y-%m-%dT00:00:00Z) \
     --end_time=$(date -u +%Y-%m-%dT00:00:00Z) \
     projects/<PROJECT>/locations/us/transferConfigs/<TRANSFER_CONFIG_ID>
   ```

The transfer config ID is in the URL after creating the transfer. Backfill runs are rate-limited to ~35 min apart by Google, so a 30-day backfill takes ~17 hours total — but the most recent days land first.

### Refresh window vs backfill — these are different things

Two concepts that sound similar but behave very differently:

**Backfill** is a one-time operation that fills historical data when you first set up the transfer. You trigger it via `bq mk --transfer_run`, it runs once per day in the range you specified, and then it's done. After the initial ~30 days of history is loaded, backfill is over.

**Refresh window** is an ongoing setting on the transfer config that tells the daily sync: "on every run, re-fetch the last N days to catch late-reported data." We chose 7 days. This means the transfer runs *forever* (not just during backfill) and every daily run re-reads the most recent 7 days of Google Ads data — overwriting whatever was previously loaded for those dates.

Why this matters: **the last 7 days of data in your BigQuery tables are unstable.** A row for 2026-04-05 might show 100 clicks today, 115 clicks tomorrow, and 118 clicks the day after that as Google catches up on delayed reporting, deduplicates attribution, fires late conversions, and adjusts for currency conversion. Only data *older* than the refresh window is guaranteed stable.

For the resonance loop, this has direct consequences:
- **Query results for the last 7 days can change between runs**, even if no time has passed.
- **Predictions with evaluation windows ending in the last 7 days are tentative** — see `references/prediction-cards.md` § "Common pitfalls" #7.
- **For a stable backward-looking analysis**, query data more than 7 days old.
- **For fresh-as-possible analysis**, query through yesterday but expect the numbers to shift as the transfer refreshes.

The 7-day window is not fixed at 7 — it's a setting in the transfer config. Longer windows (14, 30) catch more late data but make more of your recent data unstable. Shorter windows (3, 5) are more responsive but miss delayed conversions. 7 is Google's recommended default and what we use.

### Table layout (what to query)

The transfer creates ~30 tables in the destination dataset. The ones the resonance loop actually uses:

| Table | Contents |
|-------|----------|
| `ads_Campaign_<MCC>` | Campaign metadata: name, status, type, budget |
| `ads_CampaignBasicStats_<MCC>` | Daily campaign metrics: impressions, clicks, cost_micros, conversions |
| `ads_AdGroup_<MCC>` | Ad group metadata |
| `ads_AdGroupBasicStats_<MCC>` | Daily ad group metrics |
| `ads_Ad_<MCC>` | Ad creative content (RSA headlines, descriptions) |
| `ads_AdBasicStats_<MCC>` | Daily per-ad metrics |
| `ads_Keyword_<MCC>` | Keyword metadata |
| `ads_KeywordBasicStats_<MCC>` | Daily keyword metrics |

The numeric suffix is the **MCC ID** the transfer is bound to. Each table has a `customer_id` column inside it that identifies the actual sub-account each row belongs to — filter by it to scope to a specific Octave sub-account.

Tables are partitioned by `_DATA_DATE` (a DATE column). Always include a date predicate — querying without one scans the entire table.

### Schema gotchas (verified against a live transfer)

The table schemas do **not** match GAQL field names. Four things will trip you up:

1. **Column names use the full Google Ads resource path with underscores**, not the GAQL short form. For example:
   - `ad_group_ad.ad.id` (GAQL) → `ad_group_ad_ad_id` (BQ column)
   - `ad_group_ad.ad.responsive_search_ad.headlines` → `ad_group_ad_ad_responsive_search_ad_headlines`
   - `ad_group_ad.ad.type` → `ad_group_ad_ad_type`
   - `metrics.cost_micros` → `metrics_cost_micros`
   - Always check the actual schema with `bq show --schema --format=prettyjson <project>:<dataset>.<table>` before writing a query.

2. **Headlines and descriptions are JSON-encoded STRINGs**, not BigQuery `ARRAY` columns. The field contains a serialized JSON array of objects shaped like `[{"text": "...", "pinnedField": "HEADLINE_1", "assetPerformanceLabel": "PENDING", "policySummaryInfo": {...}}, ...]`. You **cannot** use `ARRAY_TO_STRING` or `ARRAY_LENGTH` on them — that will fail with `expected array type but found STRING`. Use `JSON_EXTRACT_ARRAY` and `JSON_EXTRACT_SCALAR` to parse them in SQL, or extract the raw STRING and parse client-side in Python. The JSON parsing approach is shown in the queries below.

3. **The Ad join key is `(customer_id, ad_group_ad_ad_id, ad_group_id, campaign_id)`** — all four columns. Dropping `campaign_id` (or using a 3-column USING clause) will fail with `Column ad_id in USING clause not found on left side of join`. The Ad table carries `campaign_id` and the BasicStats table requires it in the join.

4. **The `ads_Campaign_<MCC>`, `ads_AdGroup_<MCC>`, and `ads_Ad_<MCC>` tables are DAILY-SNAPSHOTTED dimension tables, not static dim tables.** Each entity has one row per `_DATA_DATE` — not one row total. After N days of transfer activity, each ad_group_id has N rows in `ads_AdGroup_<MCC>`, each campaign_id has N rows in `ads_Campaign_<MCC>`, and so on. Joining a BasicStats row to these tables without a snapshot-dedup step produces a **cartesian explosion**: each stats row is multiplied by the number of snapshot dates in each joined dim table. If you JOIN both `ads_AdGroup` and `ads_Campaign` raw, the multiplier is approximately N² over time.

   **Symptom**: Your totals look plausible but are wrong by a constant factor. E.g., a raw `SUM(metrics_clicks)` from the stats table returns 66 clicks, but the same SUM with dim joins returns 264 (4× inflated because the dim tables had 2 snapshots each). The bug is invisible if you only trust the joined query — there's nothing in the output that screams "wrong". The only way to catch it is a cross-check against the stats table alone. **The Stage 2 smoke test in `SKILL.md` step 6A enforces this cross-check and will abort the loop if totals diverge. Never skip it.**

   **Fix pattern**: Never JOIN `ads_Campaign_*` or `ads_AdGroup_*` or `ads_Ad_*` directly. Always wrap them in a "latest snapshot" CTE first:

   ```sql
   WITH
   ag_latest AS (
     SELECT * FROM `<project>.google_ads.ads_AdGroup_<MCC>`
     QUALIFY ROW_NUMBER() OVER (PARTITION BY ad_group_id ORDER BY _DATA_DATE DESC) = 1
   ),
   c_latest AS (
     SELECT * FROM `<project>.google_ads.ads_Campaign_<MCC>`
     QUALIFY ROW_NUMBER() OVER (PARTITION BY campaign_id ORDER BY _DATA_DATE DESC) = 1
   ),
   ad_latest AS (
     SELECT * FROM `<project>.google_ads.ads_Ad_<MCC>`
     QUALIFY ROW_NUMBER() OVER (PARTITION BY ad_group_ad_ad_id ORDER BY _DATA_DATE DESC) = 1
   )
   SELECT ...
   FROM `<project>.google_ads.ads_AdGroupBasicStats_<MCC>` s
   JOIN ag_latest ag USING (customer_id, ad_group_id, campaign_id)
   JOIN c_latest c USING (customer_id, campaign_id)
   ...
   ```

   Every sample query below uses this CTE preamble. Do not skip it, even for a "quick" query.

   **Alternative patterns that also work but are less clear**:
   - Add an explicit date-equality predicate: `AND ag._DATA_DATE = s._DATA_DATE` (requires the dim table to have a snapshot for every stats date, which may not hold — if a stats row lands on 2026-04-07 but the dim snapshot for 2026-04-07 has not yet been written, the row silently disappears)
   - Filter to the max snapshot date inline: `AND ag._DATA_DATE = (SELECT MAX(_DATA_DATE) FROM ads_AdGroup_<MCC>)` (fine but harder to read than a CTE, and does not compose cleanly when multiple dim tables are joined)

   **The CTE pattern is the standard**. If you read a query in this codebase that joins dim tables without a CTE, it is broken. File a bug.

### Sample queries the resonance loop will generate

**Top 10 campaigns by spend, last 7 days:**

```sql
-- NOTE: ads_Campaign_<MCC> is daily-snapshotted. Wrap it in c_latest.
-- Raw JOIN would multiply SUMs by the number of snapshot dates. See Gotcha #4.
WITH c_latest AS (
  SELECT * FROM `<project>.google_ads.ads_Campaign_<MCC>`
  QUALIFY ROW_NUMBER() OVER (PARTITION BY campaign_id ORDER BY _DATA_DATE DESC) = 1
)
SELECT
  c.customer_id,
  c.campaign_name,
  SUM(s.metrics_cost_micros) / 1000000 AS cost_usd,
  SUM(s.metrics_impressions) AS impressions,
  SUM(s.metrics_clicks) AS clicks,
  SAFE_DIVIDE(SUM(s.metrics_clicks), SUM(s.metrics_impressions)) AS ctr,
  SUM(s.metrics_conversions) AS conversions
FROM `<project>.google_ads.ads_CampaignBasicStats_<MCC>` s
JOIN c_latest c USING (customer_id, campaign_id)  -- latest-snapshot CTE, not raw dim
WHERE s._DATA_DATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY 1, 2
ORDER BY cost_usd DESC
LIMIT 10
```

**Per-ad performance with creative content (the core resonance query):**

```sql
-- NOTE: ads_Ad_<MCC> and ads_AdGroup_<MCC> are daily-snapshotted. Wrap both.
-- Raw JOINs multiply SUMs by the number of snapshot dates in each dim table.
-- See Gotcha #4.
WITH
ad_latest AS (
  SELECT * FROM `<project>.google_ads.ads_Ad_<MCC>`
  QUALIFY ROW_NUMBER() OVER (PARTITION BY ad_group_ad_ad_id ORDER BY _DATA_DATE DESC) = 1
),
ag_latest AS (
  SELECT * FROM `<project>.google_ads.ads_AdGroup_<MCC>`
  QUALIFY ROW_NUMBER() OVER (PARTITION BY ad_group_id ORDER BY _DATA_DATE DESC) = 1
)
SELECT
  ag.ad_group_name,
  ad.ad_group_ad_ad_id AS ad_id,
  ad.ad_group_ad_ad_type AS ad_type,
  -- Parse the JSON-encoded headline/description arrays into pipe-delimited strings.
  -- The full structured data is in the *_json columns below if you need pinning info.
  (
    SELECT STRING_AGG(JSON_EXTRACT_SCALAR(h, '$.text'), ' | ')
    FROM UNNEST(JSON_EXTRACT_ARRAY(ad.ad_group_ad_ad_responsive_search_ad_headlines)) h
  ) AS headlines,
  (
    SELECT STRING_AGG(JSON_EXTRACT_SCALAR(d, '$.text'), ' | ')
    FROM UNNEST(JSON_EXTRACT_ARRAY(ad.ad_group_ad_ad_responsive_search_ad_descriptions)) d
  ) AS descriptions,
  -- Raw JSON kept around for client-side parsing if you need pinnedField, performance labels, etc.
  ad.ad_group_ad_ad_responsive_search_ad_headlines AS headlines_json,
  ad.ad_group_ad_ad_responsive_search_ad_descriptions AS descriptions_json,
  SUM(s.metrics_impressions) AS impressions,
  SUM(s.metrics_clicks) AS clicks,
  SAFE_DIVIDE(SUM(s.metrics_clicks), SUM(s.metrics_impressions)) AS ctr,
  SUM(s.metrics_conversions) AS conversions,
  SAFE_DIVIDE(SUM(s.metrics_conversions), SUM(s.metrics_clicks)) AS conv_rate,
  SUM(s.metrics_cost_micros) / 1000000 AS cost_usd,
  SAFE_DIVIDE(SUM(s.metrics_cost_micros) / 1000000, SUM(s.metrics_clicks)) AS cpc
FROM `<project>.google_ads.ads_AdBasicStats_<MCC>` s
JOIN ad_latest ad USING (customer_id, ad_group_ad_ad_id, ad_group_id, campaign_id)  -- latest-snapshot CTE
JOIN ag_latest ag USING (customer_id, ad_group_id, campaign_id)                      -- latest-snapshot CTE
WHERE s._DATA_DATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  AND ad.ad_group_ad_ad_type = 'RESPONSIVE_SEARCH_AD'
GROUP BY 1, 2, 3, 4, 5, 6, 7
HAVING impressions > 100
ORDER BY ctr DESC
```

This is the query that powers Step 6B (Map Performance Back to Source Cards). The `headlines` column is what gets matched against the variant headlines generated in Step 3. Keep `headlines_json` if you need the per-headline metadata (pinned fields, performance labels, approval status) — extract it client-side.

**Ad-group-level CPC comparison (the most actionable single query at small spend):**

When spend is small (<$1k/day), conversion data is too noisy to evaluate but **CPC and CTR at the ad group level** stabilize quickly. This query exposes the keyword-auction efficiency gap across ad groups, which is usually the biggest budget leak:

```sql
-- NOTE: ads_AdGroup_<MCC> and ads_Campaign_<MCC> are daily-snapshotted.
-- Wrap both. See Gotcha #4.
WITH
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
  SUM(s.metrics_impressions) AS impressions,
  SUM(s.metrics_clicks) AS clicks,
  ROUND(SAFE_DIVIDE(SUM(s.metrics_clicks), SUM(s.metrics_impressions)) * 100, 2) AS ctr_pct,
  SUM(s.metrics_conversions) AS conversions,
  ROUND(SUM(s.metrics_cost_micros) / 1000000, 2) AS cost_usd,
  ROUND(SAFE_DIVIDE(SUM(s.metrics_cost_micros) / 1000000, SUM(s.metrics_clicks)), 2) AS cpc_usd
FROM `<project>.google_ads.ads_AdGroupBasicStats_<MCC>` s
JOIN ag_latest ag USING (customer_id, ad_group_id, campaign_id)  -- latest-snapshot CTE
JOIN c_latest c USING (customer_id, campaign_id)                  -- latest-snapshot CTE
WHERE s._DATA_DATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY 1, 2
HAVING clicks > 5
ORDER BY cpc_usd DESC
```

A 3x+ CPC gap between ad groups in the same account targeting similar personas is a strong "kill or rework this ad group" signal even with small absolute volume.

**Sanity cross-check (always run this alongside any joined query):**

```sql
SELECT
  ad_group_id,
  SUM(metrics_impressions) AS impressions_raw,
  SUM(metrics_clicks) AS clicks_raw,
  SUM(metrics_conversions) AS conversions_raw,
  ROUND(SUM(metrics_cost_micros) / 1000000, 2) AS cost_raw
FROM `<project>.google_ads.ads_AdGroupBasicStats_<MCC>`
WHERE _DATA_DATE >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY 1
```

This is the ground truth: single table, no joins, nothing to multiply. Every joined query above must produce per-ad-group totals that match this exactly. If they don't, the join inflated the numbers — find the missing CTE. The resonance loop's Stage 2 smoke test runs this automatically and aborts on mismatch.

**Filter to a specific sub-account:**

Add `WHERE s.customer_id = <SUB_ACCOUNT_ID>` to any query.

---

## Path 3: Direct API (curl or Python, no MCP)

For users who haven't installed the MCP but have an approved developer token. Same gotchas as Path 1 (login-customer-id, dev token tier, scope) — the only difference is no MCP wrapper. Useful as a fallback when the user has the token but the MCP is broken.

### Smoke test

Mint an access token from the refresh token and try `listAccessibleCustomers`:

```bash
ACCESS_TOKEN=$(curl -s -X POST https://oauth2.googleapis.com/token \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "refresh_token=$REFRESH_TOKEN" \
  -d "grant_type=refresh_token" | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

curl -s -X GET "https://googleads.googleapis.com/v21/customers:listAccessibleCustomers" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "developer-token: $DEVELOPER_TOKEN"
```

### Per-ad performance query (curl)

```bash
curl -s -X POST "https://googleads.googleapis.com/v21/customers/$CUSTOMER_ID/googleAds:searchStream" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "developer-token: $DEVELOPER_TOKEN" \
  -H "login-customer-id: $LOGIN_CUSTOMER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.responsive_search_ad.headlines, ad_group_ad.ad.responsive_search_ad.descriptions, metrics.impressions, metrics.clicks, metrics.ctr, metrics.conversions, metrics.cost_micros FROM ad_group_ad WHERE segments.date DURING LAST_30_DAYS AND ad_group_ad.ad.type = RESPONSIVE_SEARCH_AD"
  }'
```

### Version pinning

Always use the current API version. As of 2026-04, that's `v21`. Older versions are sunset on a rolling basis with little warning — `v18` returns 404 today. Check https://developers.google.com/google-ads/api/docs/release-notes for the current version before generating a query.

---

## Path 4: Manual Fallback

When no programmatic source is available, ask the user to provide data directly:

- **Paste a CSV or table** — needs at minimum: variant identifier (headline text or ad ID), impressions, clicks, conversions
- **Paste a screenshot** — extract metrics visually from the Google Ads UI
- **Summarize verbally** — "Variant A had ~3% CTR, Variant B was under 0.5%"

Manual data is enough to run the resonance loop, but loses the ability to backfill or re-query as new data arrives.

---

## Troubleshooting

| Error | Most likely cause | Fix |
|-------|-------------------|-----|
| `CUSTOMER_NOT_FOUND` + "Request is missing required authentication credential" | `login-customer-id` is wrong, missing, or set to a sub-account / closed account | Set `GOOGLE_ADS_LOGIN_CUSTOMER_ID` to the **MCC** ID (the active manager account at the top of the Ads account picker), no dashes |
| `DEVELOPER_TOKEN_NOT_APPROVED` "only approved for use with test accounts" | Token is in Test tier | Apply for Basic Access in Google Ads → Tools → API Center → Access Level. Until approved, only test accounts work. Or use Path 2 (BigQuery), which doesn't need an approved token |
| `404` on `/v18/...` or any older API path | API version sunset | Update to current version (v21 as of 2026-04) |
| `invalid_scope` or 403 immediately after auth | ADC missing the `adwords` scope | Re-mint refresh token with the explicit scope using the Python `InstalledAppFlow` snippet above. Standard `gcloud auth application-default login` does NOT include this scope |
| `list_accessible_customers` works but every Search query fails | Same as the first row — wrong `login-customer-id` | Same fix |
| BigQuery transfer config exists but tables are empty | First run hasn't completed yet | Trigger a backfill with `bq mk --transfer_run` or wait ~24h for the first scheduled run |
| BigQuery transfer fails silently when run as a service account | Service account isn't a user in the Google Ads MCC | Add the SA email as a user in ads.google.com → Admin → Access and security → Users with at least Read-only access. Note: some Workspace orgs don't allow inviting `*.gserviceaccount.com` emails — fall back to user OAuth |
| Backfill rate-limited | Google caps backfill runs at ~35 min apart | This is normal — the backfill will complete in N × 35 min. Most-recent days run first |
| Data shown for ad creative is in Spanish/another language | The ad's language setting matches the account default | Pass `customer.tracking_url_template` and check `ad_group_ad.ad.language` if multilingual; or filter by `customer_id` to a single sub-account |
