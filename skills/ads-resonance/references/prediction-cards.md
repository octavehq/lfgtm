# Prediction Cards & Calibration

The resonance loop generates **prediction cards** alongside its findings — explicit, falsifiable claims about what specific metrics will do over a specific window, with conditions that would confirm or refute them. The next time the loop runs, it evaluates the previous cards against actual data and reports a track record.

This turns the loop from a one-shot oracle into an iterative scientific instrument with a verifiable history of being right and wrong.

---

## Why predictions

Three things every other AI tool fails to do:

1. **Calibration over time.** After 10+ predictions you can compute hit rates per prediction type and learn what to trust. After 100, you have the only AI tool in GTM with a verifiable track record of its own predictions in your account.
2. **Forced honesty about thin data.** The loop can't claim "this variant won" from 1 conversion if it's also predicting that the conversion data is too thin to validate within 7 days. Pre-committing to specific falsifiability conditions before the data arrives is what scientists do; it's what marketing tools never do.
3. **A reason to re-run the loop.** Predictions have evaluation dates. When a date arrives, you (or a scheduled job — see "Cadence and scheduling" below) re-run the loop to see if the predictions held. Loop becomes a habit instead of an event.

---

## The prediction card schema

Cards live in a JSON file at `~/.octave/predictions/<MCC_ID>.json` (one file per Google Ads manager account). The file is read at the start of every loop run and written back at the end.

Each card has these fields:

| Field | Description |
|---|---|
| `id` | Unique identifier, format `P-YYYY-MM-DD-NNN` |
| `generated_at` | ISO timestamp of the loop run that created the card |
| `generated_by` | Human-readable description of the source run + training window |
| `mode` | The analytical mode the loop was in when the card was generated (`smoke-test` / `ad-group` / `ad` / `full-resonance`) |
| `is_structural` | Boolean — `true` if the claim is about a structural property of the auction, `false` if about a specific named unit |
| `claim` | One sentence describing the testable claim, in plain English |
| `type` | The prediction type (see "Prediction types" below) |
| `evaluation_window` | The date range over which the prediction will be evaluated |
| `evidence_at_prediction` | Snapshot of the data the card was generated from |
| `confirms` | Plain-English condition that, if met, marks the card CONFIRMED |
| `refutes` | Plain-English condition that, if met, marks the card REFUTED |
| `inconclusive` | Plain-English condition under which the card cannot be evaluated (typically a volume gate failure) |
| `evaluation_sql` | **The parameterized SQL query that produces the data needed to apply the confirms/refutes/inconclusive conditions.** Uses placeholders `<project>`, `<dataset>`, `<MCC>`, `<window_start>`, `<window_end>` which the evaluating loop substitutes before running. This field is what makes re-evaluation deterministic across loop runs — without it, two re-evaluations might construct different queries from the natural-language fields and disagree. Always emit the SQL at generation time. See `prediction-cards.template.json` for an example. |
| `confidence` | LOW / MEDIUM / HIGH at the time of generation |
| `rationale` | Why this prediction is worth making — what makes it informative |
| `action_if_confirmed` | What to do if the card lands |
| `action_if_refuted` | What to do if the card fails |
| `action_if_inconclusive` | What to do if the card can't be evaluated |
| `status` | One of: `PENDING`, `CONFIRMED`, `REFUTED`, `INCONCLUSIVE_FAVORABLE`, `INCONCLUSIVE_UNFAVORABLE` |
| `evaluated_at` | ISO timestamp of the evaluation (if any) |
| `evaluated_against` | The data and computed values from the evaluation |
| `evaluation_notes` | Human-readable notes on what happened |

### Status values

- **`PENDING`** — Card has not yet been evaluated. Either the evaluation window is in the future, or the data for the window hasn't fully landed yet.
- **`CONFIRMED`** — Evaluation conditions were met. The claim held.
- **`REFUTED`** — Evaluation conditions were met but the data contradicted the claim.
- **`INCONCLUSIVE_FAVORABLE`** — Volume gate failed (the unit didn't accumulate enough data to evaluate strictly), but the directional signal in the data we do have *supports* the prediction. Worth tracking separately because if FAVORABLE inconclusives consistently outnumber UNFAVORABLE ones, the volume gate is too strict and should be loosened.
- **`INCONCLUSIVE_UNFAVORABLE`** — Volume gate failed, but the directional signal *contradicts* the prediction. Counts as a "soft refutation" for calibration purposes.

Every status may additionally carry a **`tentative: true`** flag if the evaluation was made while the evaluation window is still within the BigQuery refresh lag (the last `refresh_lag_days`, typically 7). Tentative statuses are the loop's best-available guess and can flip on subsequent runs as the transfer service re-fetches and updates data for the same dates. The loop re-evaluates tentative cards on every run; they become final (`tentative: false`) only after `evaluation_window.end + refresh_lag_days`.

The FAVORABLE/UNFAVORABLE distinction was added in schema v0.2 after the first backtest revealed that many predictions on small accounts will fail the strict volume gate even when their directional signal is meaningful. Tracking direction separately lets the loop calibrate its own thresholds over time.

---

## Prediction types

Not every claim is a prediction. The loop generates cards from a fixed taxonomy of prediction types, each with known strengths and failure modes.

### `cpc-efficiency-gap` (STRUCTURAL — strongest type)

**Claim shape**: "The CPC ratio between the highest-CPC ad group and the lowest-CPC ad group will persist at >= Nx for the next 7 days."

**Why it's strong**: It's about a property of the keyword auction (Quality Score divergence), not about specific named units. When new units appear or old ones get de-prioritized, the structural property usually holds — meaning the prediction generalizes to ad groups that didn't exist at prediction time. This was empirically validated in the v0.1 backtest, where a CPC-gap prediction confirmed against a brand new ad group.

**Volume gates**: Both compared ad groups must have ≥ 10 clicks in the evaluation window for the prediction to be evaluable. Below that, INCONCLUSIVE.

**When to generate**: Whenever two or more ad groups in the same account have meaningfully different CPCs (≥ 3x ratio), with at least one of them carrying ≥ 10 clicks in the training window.

### `cpc-tier-distribution` (STRUCTURAL)

**Claim shape**: "The CPC distribution across active ad groups will remain bimodal (or unimodal, or trimodal): N ad groups in a low tier (CPC ≤ $X), N in a high tier (CPC ≥ $Y), and 0 in between."

**Why it's interesting**: Bimodal CPC distributions are typically caused by Quality Score divergence between keyword sets, not budget/bid choices. If the distribution stays bimodal across multiple windows, that's evidence of two distinct keyword-creative match qualities operating in the account, which is actionable (bridge the middle by deliberately experimenting).

**Volume gates**: All ad groups in the comparison need ≥ 10 clicks.

**When to generate**: When the CPC distribution across ad groups shows clear clusters with empty space between them.

### `regression-to-mean` (UNIT-SPECIFIC — weak type, use sparingly)

**Claim shape**: "Unit X's metric Y of Z% will regress toward the mean (range A-B%) as click volume passes 100."

**Why it's weak**: Almost always lands as INCONCLUSIVE because the named unit doesn't accumulate enough volume to test strictly within the evaluation window. The first backtest confirmed this — both regression-to-mean predictions failed the volume gate even though one of them had a directionally correct signal.

**When to generate**: Only when the unit is currently accumulating volume at a rate that will plausibly carry it past the volume gate within the evaluation window. Compute: `(current run rate clicks/day) * 7 >= volume_gate`. If false, do not generate.

**Better alternative**: For most cases, generate an `exposure-projection` instead, which can be evaluated even at low volume (you're predicting whether the volume itself will materialize, not what will happen at high volume).

### `exposure-projection` (UNIT-SPECIFIC — useful)

**Claim shape**: "Unit X will accumulate ≥ N clicks (or impressions, or conversions) by date D."

**Why it works**: It predicts what's measurable directly — volume — rather than predicting what would happen at high volume. Predicts the analytical mode the unit will be eligible for in the next loop run.

**When to generate**: When you want to know if a current low-volume unit will become eligible for ad-mode or full-resonance analysis by the next run.

### `field-stability` (META — high value despite low confidence)

**Claim shape**: "No new ad group will achieve ≥ 30 clicks during the evaluation window (the field of competing units is stable)."

**Why it matters**: This is a meta-prediction about the loop's own predictive scope. If the field is stable, unit-specific predictions are reliable. If new units emerge frequently, the loop should heavily favor structural predictions over unit-specific ones. Tracking field-stability over time tells the loop how to weight its own outputs.

**When to generate**: Always, on every run. Field stability is a first-class signal even when it's not directly actionable.

### `cpa-stabilization` (FULL RESONANCE MODE ONLY)

**Claim shape**: "Cost per acquisition (CPA) will land within range $X-$Y for ad group Z over the next 7 days."

**Why it's gated**: Requires 30+ existing conversions in the training window AND a projected 30+ in the evaluation window. Almost no small-spend account meets these gates.

**When to generate**: Only when the loop is in full-resonance mode.

### `headline-stability` (NOT YET RELIABLE — needs more data)

**Claim shape**: "Within RSA ad X, headline asset Y will continue to be Google's most-served combination."

**Why it's currently disabled**: Google does not expose per-headline-combination metrics in BigQuery. This type would require a different data source (e.g., direct API access to asset performance reports) and even then is fragile to Google's optimizer changing combinations dynamically.

**When to generate**: Don't, until we figure out how to get reliable headline-level data.

---

## The structural-over-unit rule

**Always prefer claims about structural properties over claims about named units.**

The first backtest made this concrete: a CPC-gap prediction was confirmed via a brand new ad group that didn't exist at prediction time. The structural property ("there's a 3x+ CPC divergence in this account") held even as the cast of characters changed. The unit-specific predictions (regression-to-mean for Test campaign) failed because the named units got de-prioritized between windows.

When generating prediction cards, ask: "Is this claim about *what kind of thing is happening* or *what specific thing is happening*?" The first generalizes; the second is fragile.

**Examples of structural claims** (good):
- "The CPC distribution will remain bimodal."
- "Ad groups with X characteristic will outperform ad groups with Y characteristic by Z%."
- "Conversion velocity across the account will reach >= N by date D."

**Examples of unit-specific claims** (use sparingly, only when you have to):
- "Ad group 'VP Engineering — Enterprise FinServ' will hit 100 clicks."
- "Ad 'Pain-Focused v2' (the responsive search ad with HEADLINE_1 pinned to 'Still Prepping Audits By Hand?') will maintain 6%+ CTR."

The loop's calibration log (the `lessons` array under `calibration` in the JSON file) should accumulate evidence about which claim shapes generalize and which don't. The structural-over-unit rule is currently the strongest one.

---

## Persistence

### File location

`~/.octave/predictions/<MCC_ID>.json`

One file per Google Ads MCC. The file is plain JSON, no database required. It lives under `$HOME/.octave/`, outside any repo, and is user-owned.

### File lifecycle

- **First run**: file does not exist. Loop creates it after generating predictions.
- **Every subsequent run**:
  1. Read the file at startup.
  2. Find all PENDING cards whose `evaluation_window` end date is on or before today.
  3. Run the evaluation queries against current BigQuery data.
  4. Update each card's `status`, `evaluated_at`, `evaluated_against`, `evaluation_notes`.
  5. Run the resonance loop's normal analysis.
  6. Generate new prediction cards based on the new findings.
  7. Append new cards to the file's `predictions` array.
  8. Recompute the `calibration` block.
  9. Write the file.

### Schema versioning

The `schema_version` field at the top of the file tracks which version of the prediction-card schema the file was written against. Current version: `0.2`. Schema migration between versions is not currently implemented — if the schema changes in the future, files using older versions will need manual migration. The loop should refuse to write back a file whose schema version is newer than what the loop knows about (would lose information from a future schema).

---

## Calibration block

After 5+ resolved predictions, the loop maintains aggregate stats:

```json
"calibration": {
  "total_predictions": 9,
  "evaluated": 3,
  "pending": 5,
  "confirmed": 1,
  "refuted": 0,
  "inconclusive_favorable": 1,
  "inconclusive_unfavorable": 1,
  "directional_hit_rate": "2/3",
  "by_type": {
    "cpc-efficiency-gap": {"total": 2, "confirmed": 1, "pending": 1, "calibration_so_far": "1/1"},
    "regression-to-mean": {"total": 2, "inconclusive_favorable": 1, "inconclusive_unfavorable": 1, "lesson": "..."},
    "exposure-projection": {"total": 4, "pending": 4}
  },
  "lessons": [
    "STRUCTURAL PREDICTIONS GENERALIZE; UNIT-SPECIFIC ONES DON'T...",
    "..."
  ]
}
```

### Self-tuning over time

The loop adjusts its default behavior based on its own track record. Don't eyeball the hit rate — apply these exact rules, in order. "Resolved" means CONFIRMED + REFUTED + INCONCLUSIVE_FAVORABLE + INCONCLUSIVE_UNFAVORABLE combined; hit rate is CONFIRMED / resolved.

1. **Fewer than 10 resolved cards for a type**: use its default confidence and do not adjust. Small N is not a basis for tuning.
2. **10+ resolved and hit rate ≥ 80%**: promote the type's default confidence by one tier (LOW → MEDIUM → HIGH). Surface findings of this type as "high-trust" in the resonance map.
3. **10+ resolved and hit rate ≤ 30%**: demote the type's default confidence by one tier and add a caveat to all findings of this type.
4. **10+ resolved and hit rate is 0%**: stop generating that type entirely on this run. Note in the calibration `lessons` that the type has been retired.
5. **INCONCLUSIVE_FAVORABLE outnumbers INCONCLUSIVE_UNFAVORABLE by 3:1 or more across 10+ inconclusive cards of the same type**: the volume gate is too strict for that type. Note this in `lessons` and consider relaxing the gate (with user confirmation) on the next run. Conversely, many INCONCLUSIVE_UNFAVORABLE means the volume gate is fine but the prediction generation is wrong about direction — investigate why.
6. **10+ resolved with hit rate between 30% and 80%**: no adjustment — the type is calibrated reasonably.

These rules are deterministic so two future sessions reading the same calibration block will make the same tuning decisions. Always note in the loop output what tuning was applied (e.g., "cpc-efficiency-gap promoted from MEDIUM to HIGH based on 12/14 hit rate"). This is what calibration over time looks like in practice.

---

## Backtest example (illustrative)

A typical first run of the loop on a small-spend account might generate 4 predictions and resolve them like this on the second run:

| ID | Type | Status | Lesson |
|---|---|---|---|
| P-001 | regression-to-mean | INCONCLUSIVE_UNFAVORABLE | Volume gate failed; the unit had only 8 clicks in the evaluation window. Prediction shouldn't have been generated for a unit at this volume. |
| P-002 | regression-to-mean | INCONCLUSIVE_FAVORABLE | Volume gate failed; directional signal supported the prediction (0% conv rate matches predicted 0-3% range) but couldn't confirm strictly. The hard rule held: never claim a conversion finding from <30 conversions. |
| P-003 | exposure-projection | PENDING | 7-day window, only 4 days of data evaluable so far. Currently on track to refute (~26 clicks projected vs 30 threshold). |
| P-004 | cpc-efficiency-gap | **CONFIRMED** | The gap held at >5x (above the 3x threshold). The original prediction was about specific named ad groups, but one of those ad groups lost volume; the gap was confirmed via a brand new ad group that didn't exist at prediction time — strong evidence that this prediction type captures an auction-structure property, not unit-specific noise. |

**Net calibration after run 1**: 1 CONFIRMED, 0 REFUTED, 2 INCONCLUSIVE (1 favorable, 1 unfavorable), 1 PENDING. Hit rate on the strongest type (cpc-efficiency-gap): 1/1. The structural-over-unit rule is empirically supported even on a single backtest.

This pattern is typical for small-spend accounts: most predictions go to INCONCLUSIVE because of volume gates, but the structural CPC predictions land cleanly because they're about properties of the keyword auction that survive even when individual ad groups change.

---

## Cadence and scheduling

Prediction cards make the loop *worth* running regularly, because each run adds calibration data to the historical record.

### Recommended cadences

| Account spend | Recommended cadence | Why |
|---|---|---|
| < $500/day | Weekly (Monday morning) | Most days don't meaningfully change ad-group-level findings. Weekly gives enough new signal to be worth processing. |
| $500–$2,000/day | Twice weekly (Monday + Thursday) | Enough volume to see ad-level changes mid-week. |
| > $2,000/day | Daily | Conversion data accumulates fast enough that daily checks are useful. |

### How to schedule the loop

**Recommended: a locally scheduled run on the user's machine** (e.g., Claude Code's scheduled tasks feature, or any local scheduler that can invoke `/octave:ads-resonance`). A local run has the two things the loop needs that a cloud-hosted schedule does not:

1. **Local file access** to read and write `~/.octave/predictions/<MCC_ID>.json` — without it, calibration tracking cannot work.
2. **Local Google Cloud credentials**, so the run can execute `bq query` against the user's BigQuery dataset directly — a cloud-hosted run would need credentials baked into the prompt (insecure) or a hosted BigQuery connector.

Session-scoped recurring prompts (ones that die when the working session exits) are fine for short-lived polling but not for a weekly cadence that needs to survive restarts. If prediction storage ever moves from the local filesystem to a shared remote location (e.g., a BigQuery auxiliary table), cloud-hosted schedules become viable.

### What to do when a prediction's evaluation date arrives mid-week

If you don't want to wait for your usual scheduled run, just invoke the loop manually: `/octave:ads-resonance`. It will read the JSON file, find any PENDING cards whose evaluation date has passed, run the evaluation queries against current BigQuery data, and update the file.

Predictions also have a soft "courtesy notification" mechanism: after generating new cards, the loop output should mention upcoming evaluation dates so you know when to expect the next meaningful resolution.

---

## Common pitfalls

1. **Generating regression-to-mean predictions for low-volume units.** Almost always inconclusive. Use `exposure-projection` instead.
2. **Naming specific units in claims when a structural claim would work.** Specific units get de-prioritized; structural properties survive.
3. **Generating too many predictions per run.** 3–6 cards is the sweet spot. More than that dilutes attention. Fewer than that doesn't accumulate enough calibration data.
4. **Not handling partial windows.** Predictions with evaluation windows that extend past the available BigQuery data should stay PENDING with a `partial_evaluation` block, not be force-evaluated.
5. **Forgetting field stability.** Always generate one `field-stability` prediction per run. New units emerging is the most disruptive event for unit-specific predictions, and tracking it is what tells you whether to favor structural claims more heavily.
6. **Not reading the calibration block before generating new predictions.** If a type has a 30% hit rate, the loop should stop generating it (or generate it with much lower confidence). Self-tuning is the whole point.
7. **Finalizing predictions inside the BigQuery refresh window.** The Google Ads → BigQuery Data Transfer Service re-fetches the last N days (typically 7) on *every* daily run to catch late-reported impressions, delayed conversion attribution, and retroactive adjustments. This happens forever — it is NOT a one-time backfill artifact. Any prediction evaluated inside that refresh window can change substantially as the transfer refreshes. **No status is final inside the refresh window.** Both `CONFIRMED` and `REFUTED` can flip:
   - **`REFUTED` can flip to `CONFIRMED`**: a real backtest saw a volume projection look like it would refute (a click count tracking to finish well below its threshold) then confirm cleanly the next day as the transfer filled in previously-under-reported impressions and clicks for the same dates — the click count on the same dates nearly doubled between runs.
   - **`CONFIRMED` can flip to `REFUTED` for rate-based predictions**: imagine a CTR prediction that says "stays above 10%". At day 3 with 1,500 impressions and 225 clicks, CTR is 15% — looks confirmed. Then the transfer catches 10,000 late-reported impressions for the same dates. New CTR: 225 / 11,500 = 1.96%. The prediction should now be refuted. Transfers only *add* data (they don't remove it), but adding data can move a rate in either direction because the denominator grows too.

   **Rule**: every prediction evaluated while `evaluation_window.end` is within the last `refresh_lag_days` must carry a `tentative: true` flag on its status. The loop re-evaluates tentative cards on every subsequent run until the window has fully aged out of the refresh lag, at which point the status becomes final (`tentative: false`). Users see tentative resolutions immediately — they're the best-available-guess — but they know the status might flip. This is more honest than waiting 7+ days to say anything. Finalization happens automatically on later runs once the data has stabilized.
