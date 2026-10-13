# Performance sources and reconciliation

Choose the connected API/MCP, CSV or BigQuery path that fits the task. Verify actual access with a small read before promising coverage. Infrastructure setup is optional. Discover current schemas and API versions; never expose OAuth credentials in diagnostic output. Bind workspace, platform, child advertising account, currency, timezone, attribution model, requested start/end and source watermark. An MCC is access context, not the measured account.

For CSV/API normalize account/campaign/ad-group/ad IDs; dates; impressions; clicks; integer cost micros and currency; conversions/value; actual creative membership/pins; source freshness. Missing columns limit the claim, not permission to manufacture values. Names and headlines are not identifiers.

## BigQuery pattern

Discover table/field names first. Adapt the following pattern to the actual supported schema, validate read-only SQL and dry-run before execution. Bind @customer_id, @start_date and @end_date; the example uses half-open dates. Keep currency separate and retain cost micros for reconciliation.

```sql
WITH raw AS (
 SELECT customer_id, campaign_id, ad_group_id, ad_group_ad_ad_id,
        SUM(metrics_impressions) impressions, SUM(metrics_clicks) clicks,
        SUM(metrics_cost_micros) cost_micros, SUM(metrics_conversions) conversions
 FROM `PROJECT.DATASET.AD_STATS`
 WHERE customer_id = @customer_id AND _DATA_DATE >= @start_date AND _DATA_DATE < @end_date
 GROUP BY 1,2,3,4
), dimension AS (
 SELECT * FROM `PROJECT.DATASET.AD_DIMENSION`
 WHERE customer_id = @customer_id AND _DATA_DATE >= @start_date AND _DATA_DATE < @end_date
 QUALIFY ROW_NUMBER() OVER (
   PARTITION BY customer_id,campaign_id,ad_group_id,ad_group_ad_ad_id
   ORDER BY _DATA_DATE DESC) = 1
), joined AS (
 SELECT r.*, d.ad_group_ad_ad_id IS NOT NULL AS dimension_found
 FROM raw r LEFT JOIN dimension d
 USING(customer_id,campaign_id,ad_group_id,ad_group_ad_ad_id)
)
SELECT * FROM joined
```

For each additional dimension use its full account-scoped key and a deterministic latest snapshot with an explicit tie-breaker if dates can duplicate. Aggregate stats before joins. Retain orphan stats; missing dimension names/creative block that attribution, not the denominator. Do not apply click/volume filters before reconciliation.

Full-outer-compare raw and joined key sets, row counts, impressions, clicks and cost micros exactly; compare fractional conversions with declared tolerance (for example 1e-6). Any missing/extra/duplicated key or changed metric stops dependent analysis. Run this check before eligibility filtering and retain the result with the source cutoff. Currency is the account currency, never an assumed USD alias.

A CPC gap prompts investigation of query intent, auctions, bids, landing pages, measurement and qualified buyer outcomes. It does not establish persona resonance or justify pausing traffic. Use [the task method](task-method.md) for unit-specific screening and interpretation.
